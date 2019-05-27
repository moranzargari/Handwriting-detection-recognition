# Importing the Keras Libraries and packages
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from keras.models import model_from_json
import  pandas as pd
# ignore warning
import os
import cv2

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Part 2
from keras.preprocessing.image import ImageDataGenerator

# predictions
import numpy as np
from keras.preprocessing import image


def run_model(num_of_epochs, train_size, test_size, batch_Size, filters, dropout,kernel, model_number):


    num_of_classes = 27
    image_size = 28  # 28X28 pixels

    # Initializing the CNN
    classifier = Sequential()

    # Step 1 - Convolution
    # input layer
    classifier.add(Convolution2D(filters=filters, kernel_size=kernel, input_shape=(image_size, image_size, 1), activation='relu'))

    # Step 2 - Pooling
    classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # # To increase Efficiency, add another Convolutional layer
    # classifier.add(Convolution2D(filters=32, kernel_size=3, activation='relu'))
    #
    # classifier.add(MaxPooling2D(pool_size=(2, 2)))

    # Step 3 - Flattening
    classifier.add(Flatten())


    # Step 4 - Full Connection
    # add hidden layers

    classifier.add(Dense(units=1024, activation="relu"))
    classifier.add(Dropout(dropout))

    classifier.add(Dense(units=512, activation="relu"))
    classifier.add(Dropout(dropout))

    classifier.add(Dense(units=256, activation="relu"))
    classifier.add(Dropout(dropout))

    classifier.add(Dense(units=128, activation="relu"))
    classifier.add(Dropout(dropout))
    # classifier.add(Dense(units=64, activation="relu"))
    # classifier.add(Dropout(dropout))


    # Output layer
    classifier.add(Dense(units=num_of_classes, activation="softmax"))

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

    # num_of_epochs = 20
    # train_size = 82620
    # test_size = 27540
    # batch_Size = 128

    # the batch_size is similar to k-fold , we choose k batches when k<num of samples and the NN train each k samples each time
    train_datagen = ImageDataGenerator(rescale=1. / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
    test_datagen = ImageDataGenerator(rescale=1. / 255)

    training_set = train_datagen.flow_from_directory('dataset/train', target_size=(image_size, image_size), color_mode= "grayscale",
                                                     batch_size=batch_Size,
                                                     class_mode='categorical')

    test_set = test_datagen.flow_from_directory('dataset/test', target_size=(image_size, image_size), color_mode= "grayscale", batch_size=batch_Size,
                                                class_mode='categorical')

    validation_set = test_datagen.flow_from_directory('dataset/validation', target_size=(image_size, image_size), color_mode= "grayscale",
                                                      batch_size=batch_Size,
                                                      class_mode='categorical')

    # now lets train our neural network
    classifier.fit_generator(training_set, epochs=num_of_epochs, validation_data=validation_set,
                             steps_per_epoch=train_size / batch_Size,
                             validation_steps=test_size / batch_Size,)



    # save train to Json
    model_json = classifier.to_json()
    with open("model"+str(model_number)+".json","w") as json_file:
       json_file.write(model_json)
    # serialize weights to HDF5
    classifier.save_weights("model"+str(model_number)+".h5")
    print("Saved model to disk")

    loss, acc = classifier.evaluate_generator(test_set,steps=batch_Size)
    print("loss:"+ str(loss)+"  ,acc: "+str(acc))
