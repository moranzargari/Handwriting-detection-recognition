# Importing the Keras Libraries and packages
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
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

num_of_classes = 27
image_size = 28  # 28X28 pixels

# Initializing the CNN
classifier = Sequential()

# Step 1 - Convolution
# input layer
classifier.add(Convolution2D(filters=32, kernel_size=3, input_shape=(image_size, image_size, 3), activation='relu'))

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
# classifier.add(Dense(units=27, activation="relu"))

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

num_of_epochs = 10
train_size = 13770
test_size = 4590
batch_Size = 20

# the batch_size is similar to k-fold , we choose k batches when k<num of samples and the NN train each k samples each time
train_datagen = ImageDataGenerator(rescale=1. / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1. / 255)

training_set = train_datagen.flow_from_directory('dataset/train', target_size=(image_size, image_size),
                                                 batch_size=batch_Size,
                                                 class_mode='categorical')

test_set = test_datagen.flow_from_directory('dataset/test', target_size=(image_size, image_size), batch_size=batch_Size,
                                            class_mode='categorical')

validation_set = test_datagen.flow_from_directory('dataset/validation', target_size=(image_size, image_size),
                                                  batch_size=batch_Size,
                                                  class_mode='categorical')

# now lets train our neural network
classifier.fit_generator(training_set, epochs=num_of_epochs, validation_data=validation_set,
                         steps_per_epoch=train_size / batch_Size,
                         validation_steps=test_size / batch_Size)

#Making New Predictions - lets try to predict a letter

ot = 1
test_set.reset()
images = []
for filename in os.listdir("dataset/test/"+str(ot)):
    img = cv2.imread(os.path.join("dataset/test/"+str(ot), filename))
    if img is not None:
        images.append(img)



count=0
for img in images:

    test_image = img
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = classifier.predict(test_image)
    training_set.class_indices

    letters = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת',
               'ך', 'ם', 'ן', 'ף', 'ץ']
    for i, predict in enumerate(result[0]):
        if predict == 1:
            prediction = i
            break
    else:
        prediction = 'none'
    print(prediction)
    if prediction == ot-1:
       count+=1

print("count:         "+str(count))



loss, acc = classifier.evaluate_generator(test_set,steps=batch_Size)
print("loss:"+ str(loss)+"  ,acc: "+str(acc))


# test_set.reset()
# test_pred = classifier.predict_generator(test_set, batch_Size)
#
#
# predicted_class_indices = np.argmax(test_pred, axis=1)
# labels = (training_set.class_indices)
# labels = dict((v,k) for k,v in labels.items())
# predictions = [labels[k] for k in predicted_class_indices]
#
# filnames = test_set.filenames


# results = pd.DataFrame({"filename": filnames, "predictions": predictions})
# results.to_csv("results.csv", index=False)
