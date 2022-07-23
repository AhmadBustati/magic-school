import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # disable tensorflow warnings
import datetime
from transformers import TFT5ForConditionalGeneration, T5Tokenizer
import tensorflow as tf 
model_path = "./models/"
tokenizer_path = "./tokenizer/"


class snapThatT5(TFT5ForConditionalGeneration):
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
        
def encode_text(text, tokenizer):
    encoded_text = tokenizer(
        text,
        padding = "max_length",
        max_length = 512,
        truncation = True,
        return_tensors = "tf"
    )
    input_ids = encoded_text["input_ids"]
    attention_mask = encoded_text["attention_mask"]
    return input_ids, attention_mask
# toc = datetime.datetime.now()
tokenizer = T5Tokenizer.from_pretrained(tokenizer_path)
# tic = datetime.datetime.now() 
# print("time for the tokenizer to load{}".format(tic-toc))
toc =datetime.datetime.now()
model = snapThatT5.from_pretrained(model_path)
tic = datetime.datetime.now()
print("time for the model to load{}".format(tic-toc))
while True :
    s1 = input()
# # if s1 is None:
# #     s1 = "<answer> The commission is set as a percentage of the home's sales price. Most selling agents will ask for a commission of 6%, to be split 50-50 with the buyer's agent who will thus receive 3%. <context> Negotiating the amount you pay to your real estate agent could therefore be the easiest way to save money. In a typical home sale, each party -- the buyer and the seller -- works with his or her own real estate agent. But it's the seller who generally pays the commission for both real estate agents from the proceeds of the sale. When listing your home with an agent, you have an opportunity to set the amount of commission both agents will receive. The commission is set as a percentage of the home's sales price. Most selling agents will ask for a commission of 6%, to be split 50-50 with the buyer's agent (who will thus receive 3%). Reducing your commission as little as 0.5% could result in big savings -- for example, saving 0.5% on a $400,000 home sale would be an additional $2,000 in your pocket."
    if s1 == "exit":
        break
    input_ids, attention_mask = encode_text(s1, tokenizer)
# # toc = datetime.datetime.now()
    output = model.generate(input_ids, attention_mask=attention_mask,training=False)
# # tic = datetime.datetime.now()
# # print("time for the model to generate{}".format(tic-toc))
    print(tokenizer.decode(output[0],skip_special_tokens=True))