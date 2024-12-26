import tensorflow as tf
from keras import datasets, models, layers, preprocessing

max_features = 5000
maxlen = 500

(x_train, y_train), (x_test, y_test) = datasets.imdb.load_data(num_words=max_features)

x_train = preprocessing.sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = preprocessing.sequence.pad_sequences(x_test, maxlen=maxlen)

model = models.Sequential()

model.add(layers.Embedding(input_dim=max_features, output_dim=32, input_length=maxlen))

model.add(layers.SimpleRNN(units=32, return_sequences=False))

model.add(layers.Dense(units=1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.summary()

batch_size = 64
epochs = 3

model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_data=(x_test, y_test))

loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
print(f"Точность на тестовых данных: {accuracy:.4f}")