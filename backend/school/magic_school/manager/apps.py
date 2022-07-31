from django.apps import AppConfig
# # from transformers import T5Tokenizer, TFT5ForConditionalGeneration
# # from django.conf import settings
# # import tensorflow as tf 

# # class snapThatT5(TFT5ForConditionalGeneration):
# #     def __init__(self, *args, log_dir=None, cache_dir= None, **kwargs):
# #         super().__init__(*args, **kwargs)
# #         self.loss_tracker= tf.keras.metrics.Mean(name='loss') 
    
# #     @tf.function
# #     def train_step(self, data):
# #         x = data
# #         y = x["labels"]
# #         y = tf.reshape(y, [-1, 1])
# #         with tf.GradientTape() as tape:
# #             outputs = self(x, training=True)
# #             loss = outputs[0]
# #             logits = outputs[1]
# #             loss = tf.reduce_mean(loss)
            
# #             grads = tape.gradient(loss, self.trainable_variables)
            
# #         self.optimizer.apply_gradients(zip(grads, self.trainable_variables))
# #         lr = self.optimizer._decayed_lr(tf.float32)
        
# #         self.loss_tracker.update_state(loss)        
# #         self.compiled_metrics.update_state(y, logits)
# #         metrics = {m.name: m.result() for m in self.metrics}
# #         metrics.update({'lr': lr})
        
# #         return metrics

# #     def test_step(self, data):
# #         x = data
# #         y = x["labels"]
# #         y = tf.reshape(y, [-1, 1])
# #         output = self(x, training=False)
# #         loss = output[0]
# #         loss = tf.reduce_mean(loss)
# #         logits = output[1]
        
# #         self.loss_tracker.update_state(loss)
# #         self.compiled_metrics.update_state(y, logits)
#          return {m.name: m.result() for m in self.metrics}

class ManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manager'
    # model = snapThatT5.from_pretrained(settings.QUESTION_GENERATOR)
    # tokenizer = T5Tokenizer.from_pretrained(settings.TOKENIZER)
