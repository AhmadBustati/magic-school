import tensorflow as tf 
from datasets import load_dataset
import numpy as np 
import os 
import datetime 
import tensorboard
from transformers import  T5Tokenizer, TFT5ForConditionalGeneration
train_dataset = load_dataset("iarfmoose/question_generator",split="train")
val_dataset = load_dataset("iarfmoose/question_generator",split="validation")
checkpoint ="t5-base"
max_length = 512#@param{type:"slider",min:256,max:512,step:2}
pad_id_mask = -100
warmup_steps = 1e4
train_batch_size = 8
val_batch_size = 16
buffer_size = 1000
ntrain = len(train_dataset)
nvalid = len(val_dataset)
steps = int(np.ceil(ntrain/train_batch_size))
valid_steps = int(np.ceil(nvalid/val_batch_size))
print("Total Steps: ", steps)
print("Total Validation Steps: ", valid_steps)
def encode_text(example,max_length=max_length):
    """
    Tokenizes the data in order to have the data model-ready
     """
    text = example["text"]
    question = example["question"]
    encoded_text= tokenizer(
        text,
        # text["question"],
        padding = "max_length",
        max_length=max_length,
        truncation=True,
        return_tensors='tf'
    )
    encoded_question = tokenizer(
        question,
        padding="max_length",
        max_length=max_length,
        truncation=True,
        return_tensors = "tf"

    )
    input_ids = encoded_text['input_ids'][0]
    input_attention = encoded_text['attention_mask'][0]
    target_ids = encoded_question['input_ids'][0]
    target_attention = encoded_question['attention_mask'][0]
    outputs = {'input_ids':input_ids, 'attention_mask': input_attention, 
               'labels':target_ids, 'decoder_attention_mask':target_attention}
    return outputs

def get_tokenizer(checkpoint) :
    """
    This function adds two special tokens <answer>, <context> since these tokens
    will be used  
     """
    tokenizer = T5Tokenizer.from_pretrained(checkpoint)
    tokenizer.add_special_tokens(
        {'additional_special_tokens': ['<answer>', '<context>']}
    )
    return tokenizer

def create_dataset(dataset, cache_path=None, batch_size=4, 
                   buffer_size= 1000, shuffling=True):    
    if cache_path is not None:
        dataset = dataset.cache(cache_path)        
    if shuffling:
        dataset = dataset.shuffle(buffer_size)
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(tf.data.experimental.AUTOTUNE)
    return dataset

def to_tf_dataset(dataset):  
  columns = ['input_ids', 'attention_mask', 'labels', 'decoder_attention_mask']
  dataset.set_format(type='tensorflow', columns=columns)
  return_types = {'input_ids':tf.int32, 'attention_mask':tf.int32, 
                'labels':tf.int32, 'decoder_attention_mask':tf.int32,  }
  return_shapes = {'input_ids': tf.TensorShape([None]), 'attention_mask': tf.TensorShape([None]), 
                  'labels': tf.TensorShape([None]), 'decoder_attention_mask':tf.TensorShape([None])}
  ds = tf.data.Dataset.from_generator(lambda : dataset, return_types, return_shapes)
  return ds
  

    
class SnapthatT5(TFT5ForConditionalGeneration):
    def __init__(self, *args, log_dir=None, cache_dir= None, **kwargs):
        super().__init__(*args, **kwargs)
        self.loss_tracker= tf.keras.metrics.Mean(name='loss') 
    
    @tf.function
    def train_step(self, data):
        x = data
        y = x["labels"]
        y = tf.reshape(y, [-1, 1])
        with tf.GradientTape() as tape:
            outputs = self(x, training=True)
            loss = outputs[0]
            logits = outputs[1]
            loss = tf.reduce_mean(loss)
            
            grads = tape.gradient(loss, self.trainable_variables)
            
        self.optimizer.apply_gradients(zip(grads, self.trainable_variables))
        lr = self.optimizer._decayed_lr(tf.float32)
        
        self.loss_tracker.update_state(loss)        
        self.compiled_metrics.update_state(y, logits)
        metrics = {m.name: m.result() for m in self.metrics}
        metrics.update({'lr': lr})
        
        return metrics

    def test_step(self, data):
        x = data
        y = x["labels"]
        y = tf.reshape(y, [-1, 1])
        output = self(x, training=False)
        loss = output[0]
        loss = tf.reduce_mean(loss)
        logits = output[1]
        
        self.loss_tracker.update_state(loss)
        self.compiled_metrics.update_state(y, logits)
        return {m.name: m.result() for m in self.metrics}
        

tokenizer = get_tokenizer(checkpoint)
train_ds = train_dataset.map(encode_text)
val_ds = val_dataset.map(encode_text)
tf_train_ds = to_tf_dataset(train_ds)
tf_val_ds = to_tf_dataset(val_ds)

tf_train_ds= create_dataset(tf_train_ds, batch_size=train_batch_size, 
                         shuffling=True, cache_path = None)
tf_val_ds = create_dataset(tf_val_ds, batch_size=val_batch_size, 
                         shuffling=False, cache_path = None)

start_profile_batch = steps+10
stop_profile_batch = start_profile_batch + 100
profile_range = f"{start_profile_batch},{stop_profile_batch}"
log_dir = os.path.join("./logs",
                        # Make it so the logs get tracked whenever we run an experiment 
                        datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
save_path = "./models"#@param {type:"string"}
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1,
                                                      update_freq=20,profile_batch=profile_range)
checkpoint_filepath = save_path + "/" + "T5-{epoch:04d}-{val_loss:.4f}.ckpt"
model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_weights_only=False,
    monitor='val_loss',
    mode='min',
    save_best_only=True)

callbacks = [tensorboard_callback, model_checkpoint_callback] 
metrics = [tf.keras.metrics.SparseTopKCategoricalAccuracy(name='accuracy') ]
optimizer = tf.keras.optimizers.Adam(0.00001)
loss = tf.keras.losses.CategoricalCrossentropy(from_logits=True)
model = SnapthatT5.from_pretrained(checkpoint)
model.compile(optimizer=optimizer, metrics=metrics,loss=loss)
epochs_done = 0
model.fit(tf_train_ds, epochs=20, steps_per_epoch=steps, callbacks=callbacks, 
          validation_data=tf_val_ds, validation_steps=valid_steps, initial_epoch=epochs_done)

model.save_pretrained(save_path)