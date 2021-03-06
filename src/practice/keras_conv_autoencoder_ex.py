# keras convolutional autoencoder for MNIST
# All credit to: https://blog.keras.io/building-autoencoders-in-keras.html

# first imports
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Model
from keras import backend as K

from keras.datasets import mnist
import numpy as np

from keras.callbacks import TensorBoard

from matplotlib import pyplot as plt

import pickle

print("Imports successful")

input_img = Input(shape=(28, 28, 1))  # adapt this if using `channels_first` image data format

x = Conv2D(16, (3, 3), activation='relu', padding='same')(input_img)
print("After conv1 tensor shape: " + str(x.get_shape().as_list()))

x = MaxPooling2D((2, 2), padding='same')(x)
print("After pooling1 tensor shape: " + str(x.get_shape().as_list()))

x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
print("After conv2 tensor shape: " + str(x.get_shape().as_list()))

x = MaxPooling2D((2, 2), padding='same')(x)
print("After pooling2 tensor shape: " + str(x.get_shape().as_list()))

x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
print("After conv3 tensor shape: " + str(x.get_shape().as_list()))

encoded = MaxPooling2D((2, 2), padding='same')(x)
print("After encoding tensor shape: " + str(encoded.get_shape().as_list()))

# at this point the representation is (4, 4, 8) i.e. 128-dimensional

print('\n')

x = Conv2D(8, (3, 3), activation='relu', padding='same')(encoded)
print("After conv3' tensor shape: " + str(x.get_shape().as_list()))

x = UpSampling2D((2, 2))(x)
print("After upsampling3' tensor shape: " + str(x.get_shape().as_list()))

x = Conv2D(8, (3, 3), activation='relu', padding='same')(x)
print("After conv2' tensor shape: " + str(x.get_shape().as_list()))

x = UpSampling2D((2, 2))(x)
print("After upsampling2' tensor shape: " + str(x.get_shape().as_list()))

x = Conv2D(16, (3, 3), activation='relu')(x)
print("After conv1' tensor shape: " + str(x.get_shape().as_list()))

x = UpSampling2D((2, 2))(x)
print("After upsampling1' tensor shape: " + str(x.get_shape().as_list()))

decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)
print("Decoded tensor shape: " + str(decoded.get_shape().as_list()))

autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')


print(autoencoder.summary())

raise SystemExit

# To train it, we will use the original MNIST digits with shape (samples, 3, 28, 28),
# and we will just normalize pixel values between 0 and 1.
(x_train, _), (x_test, _) = mnist.load_data()

x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))  # adapt this if using `channels_first` image data format
x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))  # adapt this if using `channels_first` image data format


print("training shapes: ")
print(x_train.shape)
print(x_test.shape)


# tensorboard backend
# tensorboard --logdir=/tmp/autoencoder
autoencoder.fit(x_train, x_train,
                epochs=5,
                batch_size=128,
                shuffle=True,
                validation_data=(x_test, x_test),
                callbacks=[TensorBoard(log_dir='/tmp/autoencoder')])

# Let's take a look at the reconstructed digits:
decoded_imgs = autoencoder.predict(x_test)

with open("decoded_imgs.pkl", 'wb') as f:
    pickle.dump(decoded_imgs, f, pickle.HIGHEST_PROTOCOL)
with open("x_test.pkl", 'wb') as f:
    pickle.dump(x_test, f, pickle.HIGHEST_PROTOCOL)


