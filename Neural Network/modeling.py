# Importing the Keras Libraries and packages
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

# ignore warning
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


#Part 2
from keras.preprocessing.image import ImageDataGenerator


#predictions
import numpy as np
from keras.preprocessing import image



# Initializing the CNN
classifier = Sequential()

# Step 1 - Convolution
#input layer
classifier.add(Convolution2D(filters=64, kernel_size=3, input_shape=(28, 28, 3), activation='relu'))

# Step 2 - Pooling
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# # To increase Efficiency, add another Convolutional layer
# classifier.add(Convolution2D(filters=32, kernel_size=3, activation='relu'))
#
# classifier.add(MaxPooling2D(pool_size=(2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full Connection
# add first hidden layer
classifier.add(Dense(units=128, activation="relu"))
# Output layer
classifier.add(Dense(units=27, activation="softmax"))


################# Compiling the CNN #################
"""
we need to compile our model. Compiling the model takes three parameters: optimizer, loss and metrics.
The optimizer controls the learning rate. We will be using ‘adam’ as our optmizer. Adam is generally a good optimizer to use for many cases.
The adam optimizer adjusts the learning rate throughout training.
The learning rate determines how fast the optimal weights for the model are calculated.
A smaller learning rate may lead to more accurate weights (up to a certain point), but the time it takes to compute the weights will be longer.
We will use ‘categorical_crossentropy’ for our loss function. This is the most common choice for classification.
A lower score indicates that the model is performing better.
To make things even easier to interpret, we will use the ‘accuracy’ metric to see the accuracy score on the validation set when we train the model.
"""
classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


# Part 2 : Fitting the CNN to the images
# the batch_size is similar to k-fold , we choose k batches when k<num of samples and the NN train each k samples each time
train_datagen = ImageDataGenerator(rescale=1. / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1. / 255)

training_set = train_datagen.flow_from_directory('dataset1/train', target_size=(28, 28), batch_size=30, class_mode='categorical')

test_set = test_datagen.flow_from_directory('dataset1/test', target_size=(28, 28), batch_size=30, class_mode='categorical')

validation_set = test_datagen.flow_from_directory('dataset1/validation', target_size=(28, 28), batch_size=30, class_mode='categorical')


# now lets train our neural network
classifier.fit_generator(training_set, epochs=2, validation_data=validation_set, steps_per_epoch=13770/30, validation_steps=4618/30)





# Making New Predictions - lets try to predict a letter
test_image = image.load_img('dataset1/test/15/4.png', target_size=(28, 28))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis=0)
result = classifier.predict(test_image)
training_set.class_indices

letters = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י','כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת','ך','ם','ן','ף','ץ']
for i,predict in enumerate(result[0]):
    if predict == 1:
        prediction = letters[i]
else:
    prediction = 'none'

print(prediction)
