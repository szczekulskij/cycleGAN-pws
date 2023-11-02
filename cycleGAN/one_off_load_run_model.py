import tensorflow as tf
MODEL_PATH = "/Users/szczekulskij/side_projects/research_projects/cycleGAN-pws/results/decent_results/monet_generator.h5"
model = tf.keras.models.load_model(MODEL_PATH)
# model.summary()