import tensorflow as tf
from tensorflow.keras import layers, models

# Load MNIST data and normalize pixel values to the range [0, 1]
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

model = models.Sequential([
    layers.Input(shape=(28, 28)),
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.2),
    layers.Dense(10, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(x_train, y_train, epochs=3, validation_split=0.1, verbose=2)
_, test_accuracy = model.evaluate(x_test, y_test, verbose=2)
print(f"Image Classification Accuracy: {test_accuracy * 100:.2f}%")
