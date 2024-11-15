
import tensorflow as tf
import tensorflow.keras.layers as layers
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.metrics import CategoricalAccuracy
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split
import numpy as np

x = s1_a1["emg"]
y = s1_a1["repetition"]
y = tf.keras.utils.to_categorical(y)

for i in range(x.shape[1]):
    filtered, _ = conv_RMS(x[:, i], time_step)
    x[:, i] = np.pad(filtered, (0, x.shape[0] - filtered.shape[0]), 'constant')

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)

def create_model(input_shape, classes):
    model = Sequential([
        Dense(128, activation='relu', input_shape=(input_shape,)),
        layers.BatchNormalization(),
        layers.Dropout(0.2),
        Dense(64, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(classes, activation='softmax')
    ])
    return model

num_classes = 7
optimizer = Adam(learning_rate=0.001)
loss = CategoricalCrossentropy()
metrics = [CategoricalAccuracy()]
tf_model = create_model(x_train.shape[1], num_classes)
epochs = 10
batch_size = 16

tf_model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
history = tf_model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.1)

tf_model.evaluate(x_test, y_test)
pred = tf_model.predict(x_test)
pred = np.argmax(pred, axis=1)
acc = np.mean(pred == np.argmax(y_test, axis=1))
print(f"Accuracy: {acc}")
