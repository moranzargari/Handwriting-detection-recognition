
# Importing the Keras Libraries and packages
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

# Initializing the CNN
classifier = Sequential()

# Step 1 - Convolution
#input layer
classifier.add(Convolution2D(filters=64, kernel_size=3, input_shape=(28, 28, 1), activation='relu'))

# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# To increase Efficiency, add another Convolutional layer
classifier.add(Convolution2D(filters=32, kernel_size=3, activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full Connection
classifier.add(Dense(output_dim=128, activation='relu'))
# Output layer
classifier.add(Dense(output_dim=3, activation='softmax'))

# Compiling the CNN
classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

