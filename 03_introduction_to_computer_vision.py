# -*- coding: utf-8 -*-
"""03 - Introduction to Computer Vision.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OQo_Up60RMO5z58UdvlkIn8XrEBXM3BB

## Intro To CNN with Tensorflow

Practise of writing algorithms to discover visual patterns
"""

import zipfile

!wget https://storage.googleapis.com/ztm_tf_course/food_vision/pizza_steak.zip

# Unzip the downloaded file
zip_ref = zipfile.ZipFile("pizza_steak.zip")
zip_ref.extractall()
zip_ref.close()

"""### Get Data

Images are from food 101 but we modified it to just pizza and steak

### Inspect Data

A very crucial step at the begginning of the project is getting to know the data
"""

ls pizza_steak

ls pizza_steak\train

ls pizza_steak\train\steak

import os

#walk through pizza steak directory and list the number of files in os
for dirpath, dirnames, filenames in os.walk("pizza_steak"):
    print(f"There are {len(dirnames)} directories and {len(filenames)} images in '{dirpath}'.")

#how many images are in a file
num_steak_images_train = len(os.listdir("pizza_steak/train/steak"))
num_steak_images_train

"""##### To visualize, let's get class name programmatically"""

#get class names programmatically

import pathlib
import numpy as np
data_dir = pathlib.Path("pizza_steak/train")
class_names = np.array(sorted([item.name for item in data_dir.glob("*")])) #create list of class name in subdirectory
print(class_names)

"""### Let's Visualize our Images`"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random

def view_random_image(target_dir, target_class):
    #set target directory
    target_folder = target_dir + target_class
    
    #get random image path
    random_image = random.sample(os.listdir(target_folder),1)
    
    #read image and plot it using matplotlib
    img = mpimg.imread(target_folder + "/" + random_image[0])
    plt.imshow(img)
    plt.title(target_class)
    plt.axis("off");
    
    print(f"Image Shape:{img.shape}")#show the shape of the image
    
    return img

#view random image
img = view_random_image(target_dir = "pizza_steak/train/", 
                       target_class = "steak")

import tensorflow as tf
tf.constant(img)

#View Image Shape
img.shape #returns width, height, color channels

#Get all the pixel values between 0 and 1
img/255

"""### End to End example

Convolutional neural network to find patterns in our images

* Load our Images
* Preprocess our Images
* Build a CNN to find patterns in our images
* Compile our CNN
* Fit the CNN to our training data
"""

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

#set seed
tf.random.set_seed(42)

#preprocess data (get all pixel values between 0 and 1, normalization / scaling)
train_datagen = ImageDataGenerator(rescale=1./255)
valid_datagen = ImageDataGenerator(rescale=1./255)

#setup paths
train_dir = "pizza_steak/train"
test_dir = "pizza_steak/test"

#Import data from directories and turn it into batches
train_data = train_datagen.flow_from_directory(directory=train_dir,
                                               batch_size=32,
                                               target_size=(224,224),
                                               class_mode="binary",
                                               seed=42)

valid_data = valid_datagen.flow_from_directory(directory = test_dir,
                                              batch_size=32,
                                              target_size=(224,224),
                                              class_mode="binary",
                                              seed=42)

#Building a CNN Model
model1 = tf.keras.Sequential([
    tf.keras.layers.Conv2D(filters=10,
                          kernel_size=3,
                          activation="relu",
                          input_shape=(224, 224, 3)),
    tf.keras.layers.Conv2D(10, 3, activation="relu"),
    tf.keras.layers.MaxPool2D(pool_size = 2, padding = "valid"),
    tf.keras.layers.Conv2D(10,3, activation="relu"),
    tf.keras.layers.Conv2D(10,3, activation="relu"),
    tf.keras.layers.MaxPool2D(2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(1, activation="sigmoid")
])

#Compile CNN
model1.compile(loss="binary_crossentropy",
              optimizer = tf.keras.optimizers.Adam(),
              metrics=["accuracy"])

#fit model
history1 = model1.fit(train_data,
                      epochs = 5,
                      steps_per_epoch = len(train_data),
                      validation_data = valid_data,
                      validation_steps = len(valid_data))

"""## Build same model to see if it works on image"""

#set seed
tf.random.set_seed(42)

#create a model to replicate 
model2 = tf.keras.Sequential([
                              tf.keras.layers.Flatten(input_shape=(224,224,3)),
                              tf.keras.layers.Dense(4, activation = "relu"),
                              tf.keras.layers.Dense(4, activation = "relu"),
                              tf.keras.layers.Dense(1, activation = "sigmoid")
])

model2.compile(loss = "binary_crossentropy",
               optimizer = "adam",
               metrics=["accuracy"])

model2.fit(train_data,
           epochs = 5,
           steps_per_epoch=len(train_data),
           validation_data = valid_data,
           validation_steps=len(valid_data)
           )

#get summary of model2
model2.summary()

#set seed
tf.random.set_seed(42)

#model
model3 = tf.keras.Sequential([
                              tf.keras.layers.Flatten(input_shape = (224, 224, 3)),
                              tf.keras.layers.Dense(100, activation = "relu"),
                              tf.keras.layers.Dense(100, activation = "relu"),
                              tf.keras.layers.Dense(100, activation = "relu"),
                              tf.keras.layers.Dense(1, activation = "sigmoid")
])

#compile the model
model3.compile(loss="binary_crossentropy",
               optimizer = tf.keras.optimizers.Adam(),
               metrics=["accuracy"])

#fit model
history3 = model3.fit(train_data,
                      epochs = 5,
                      steps_per_epoch = len(train_data),
                      validation_data = valid_data,
                      validation_steps = len(valid_data))

#get summary
model3.summary()

"""#### Binary Classification

1. Become one with data
2. Pre Process the data (Prepare it for the model, main step - scaling / normalizing)
3. Create a model (start with baseline)
4. Fit the model
5. Evaluate the model
6. Adjust different parameters and improve the model (try to beat baseline)
7. Repeat until satisfied
"""

# Visualize data
plt.figure()
plt.subplot(1,2,1)
steak_img = view_random_image("pizza_steak/train/","steak")
plt.subplot(1,2,2)
pizza_img = view_random_image("pizza_steak/train/", "pizza")

"""### Preprocess the Data (Preparing it for model)"""

# Define our directory paths
train_dir = "pizza_steak/train/"
test_dir = "pizza_steak/test/"

"""Next step is to convert data into batches

A batch is small subset of Data, Rather than looking at all numbers it will just look at a small portion.

It does for a couple of reason
1. 10000 images or more can't fit in your gpu memory
2. Trying to learn patterns in 10000 images at one shot won't be learning very well

Why 32?
32 is good for your health - Yaan LeCun
"""

#create train and test data generator and rescale the data
from tensorflow.keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(rescale = 1/255.)
test_datagen = ImageDataGenerator(rescale = 1/255.)

#load in our image data and turn it into batches
train_data = train_datagen.flow_from_directory(directory = train_dir, #Target directory of image
                                               target_size = (224, 224), #Target Size
                                               class_mode = "binary", #Type of data we are working with
                                               batch_size = 32) #size of minibatched used to load data


test_data = test_datagen.flow_from_directory(directory = test_dir,
                                             target_size = (224, 224),
                                             class_mode = "binary",
                                             batch_size = 32)

# get a sample of a training data batch
images, labels = train_data.next() #get next batch of images
len(images), len(labels)

# How many batches are there ?
len(train_data)

1500/32

#get first two image
images[:2], images[0].shape

images[7].shape

#View the first batch of labels
labels

""" ### Baseline Model

 A simple model to begin with and then later experiment and try to beat the baseline model
"""

#Make making model easier
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Activation
from tensorflow.keras import Sequential

"""**Why Baseline model?**

There are n number of architecture for deep learning. But we need to get started with a simple architecture and the introduce complexity as required
"""

model4 = Sequential([
                     Conv2D(filters = 10, #no of sliding windows, higher = complex
                            kernel_size=3, #size of sliding window
                            strides = 1, #size of the step the sliding window takes
                            padding = "valid", #if same output will be same as inpu t, if valid, output is compressed
                            activation = "relu",
                            input_shape = (224, 224, 3)), #input layer - specify input shape
                     Conv2D(10, 3, activation = "relu"),
                     Conv2D(10, 3, activation = "relu"),
                     Flatten(),
                     Dense(1,activation = "sigmoid") #output layer (Binary classification)
])

#compiling model

model4.compile(loss="binary_crossentropy",
               optimizer = "adam",
               metrics = ["accuracy"])

model4.summary()

#check length of training and testing data
len(train_data), len(test_data)

#Fit the model
history4 = model4.fit(train_data, #combo of labels and sample data
                     epochs = 5,
                     steps_per_epoch = len(train_data),
                     validation_data = test_data,
                     validation_steps = len(test_data))

model4.evaluate(test_data)

#plotting training curves
import pandas as pd
pd.DataFrame(history4.history).plot(figsize=(10,7));

#Plot validation and training curves separately
def plot_loss_curve(history):
  """
  Returns separate loss curve for training and testing
  """
  loss = history.history["loss"]
  val_loss = history.history["val_loss"]

  accuracy = history.history["accuracy"]
  val_accuracy = history.history["val_accuracy"]

  epochs = range(len(history.history["loss"])) 

  #plot loss
  plt.plot(epochs, loss, label="training_loss")
  plt.plot(epochs, val_loss, label="val_loss")
  plt.title("loss")
  plt.xlabel("epochs")
  plt.legend()

  #plot accuracy
  plt.figure()
  plt.plot(epochs, accuracy, label="training_accuracy")
  plt.plot(epochs, val_accuracy, label="val_accuracy")
  plt.title("accuracy")
  plt.xlabel("epochs")
  plt.legend()

"""When a models **Validation loss starts to increase**, it's likely model is **overfitting** which mean it is learning too well and is not able to generalize unseen data"""

#model loss and accuracy of model4
plot_loss_curve(history4)

"""# 6 Adjust the Model

Fitting model in 3 steps

0. Create Baseline
1. Beat the Baseline by overfitting a large Model
2. Reduce Overfitting

Ways to Reduce Overfitting
* Increase number of Conv Layers
* Increase number of Conv Filters
* Add another dense layer to the output of our flattened layer

Reduce Overfitting
* Add Data augmentation
* Add Regularization Layer(MaxPool2D)
* Add More Data
"""

#create model (New Baseline Model)
tf.random.set_seed(42)
model5 = tf.keras.Sequential([
                              Conv2D(10, 3, activation="relu", input_shape=(224,224,3)),
                              MaxPool2D(pool_size=2),
                              Conv2D(10, 3, activation="relu"),
                              MaxPool2D(),
                              Conv2D(10, 3, activation="relu"),
                              MaxPool2D(),
                              Flatten(),
                              Dense(1, activation="sigmoid")
])

#Compile Model
model5.compile(loss = "binary_crossentropy",
               optimizer = Adam(),
               metrics=["accuracy"])

#Fit the Model
history5 = model5.fit(train_data,
                      epochs=5,
                      steps_per_epoch=len(train_data),
                      validation_data = test_data,
                      validation_steps = len(valid_data))

#model5 Summary
model5.summary()

#plot loss curves
plot_loss_curve(history5)

"""> **Note** Reducing overfitting is also known as Regularization

###### Opening our bag of tricks and finding Data Augmentation
"""

#Set Seed
tf.random.set_seed(42)

#create ImageDataGenerator training instance with data augmentation
train_datagen_augmented = ImageDataGenerator(rescale = 1/255.,
                                             rotation_range = 0.2, #how much to rotate
                                             shear_range = 0.2, #how much do you want to shear the image
                                             zoom_range = 0.2, # Zoom in randomly on a image
                                             width_shift_range = 0.2, #Move image around in X axis
                                             height_shift_range = 0.2, #Move around in Y axis
                                             horizontal_flip = True) #For Flipping the image

#Create ImageDataGenerator without data augmentation
train_datagen = ImageDataGenerator(rescale = 1/255.)

#Create ImageDataGenerator without data augmentation for Test Dataset
test_datagen = ImageDataGenerator(rescale = 1/255.)

"""> **What is Data Augmentation ?**

Process of Altering our training data allowing it to have more ?> > diversity and our models to have more generalizeable pattern.

Altering would be cropping, flipping, rotating it or something > similar
"""

#import  data and augment it 
print("Augmented Training Data")
train_data_augmented = train_datagen_augmented.flow_from_directory(train_dir,
                                                                   target_size=(224,224),
                                                                   batch_size = 32,
                                                                   class_mode = "binary",
                                                                   shuffle=False) #For Demonstration purposes only

#Non Augmented Datagen
print("Non Augmented training data")
train_data = train_datagen.flow_from_directory(train_dir,
                                               target_size=(224,224),
                                               batch_size=32,
                                               class_mode="binary",
                                               shuffle = False)

#Non augmented test data batches
print("Non augmented test data")
test_data = test_datagen.flow_from_directory(test_dir,
                                             target_size=(224,224),
                                              batch_size=32,
                                             class_mode = "binary")

"""Data Augmentation is mostly performed on Training Data.
Using ImageDataGenerator we can modify the image in the model without affecting the original files

Visualizing Augmented data
"""

images, labels = train_data.next()
augmented_images, augmented_labels = train_data_augmented.next() #labels aren't augmented

#show original image and augmented image
import random
random_number = random.randint(0,32) # batch size is 32
print("Showing image number", random_number)
plt.imshow(images[random_number])
plt.title(f"Original Image")
plt.axis(False)
plt.figure()
plt.imshow(augmented_images[random_number])
plt.title(f"Augmented Image")
plt.axis(False)

"""New model with augmented data"""

#Create a model (Same as Model5)

model6 = Sequential([
                     Conv2D(10, 3, activation="relu"),
                     MaxPool2D(pool_size=2),
                     Conv2D(10, 3, activation="relu"),
                     MaxPool2D(),
                     Conv2D(10, 3, activation="relu"),
                     MaxPool2D(),
                     Flatten(),
                     Dense(1, activation = "sigmoid")
])

#Compile Model
model6.compile(loss="binary_crossentropy",
               optimizer = Adam(),
               metrics = ["accuracy"])

#Fit the model
history6 = model6.fit(train_data_augmented,
                      epochs = 5,
                      steps_per_epoch = len(train_data_augmented),
                      validation_data = test_data,
                      validation_steps = len(test_data))

#check model training curve
 plot_loss_curve(history6)

"""#### The power of Shuffle"""

#train augmented and shuffled
#import data and augmented it
train_data_augmented_shuffled = train_datagen_augmented.flow_from_directory(train_dir,
                                                                         target_size=(224,224),
                                                                         class_mode="binary",
                                                                         batch_size = 32,
                                                                         shuffle=True)

#model 7 (same as model 5 and 6)

#set seed
tf.random.set_seed(42)

#create model
model7 = Sequential([
    Conv2D(10,3,activation="relu"),
    MaxPool2D(),
    Conv2D(10,3,activation="relu"),
    MaxPool2D(),
    Conv2D(10,3,activation="relu"),
    MaxPool2D(),
    Flatten(),
    Dense(1, activation="sigmoid")
])

#compile the model
model7.compile(loss="binary_crossentropy",
               optimizer = Adam(),
               metrics = ["accuracy"])

#fitting on augmented and shuffled data
history7 = model7.fit(train_data_augmented_shuffled,
                      epochs = 5,
                      steps_per_epoch = len(train_data_augmented_shuffled),
                      validation_data = test_data,
                      validation_steps = len(test_data))

#plot model 7 curves
plot_loss_curve(history7)

"""When shuffling data, model gets exposed to all different kinds of data to learn features across a wide array of images

### Repeat until satisfied

As we have beaten our baseline model, there are few things we could try to continue to improve

* Increase number of model layers (eg: add more 'Conv2D'/'MaxPool2D')

* Increase number of filters on each Conv2D layer (eg from 10 to 32 or to 64)

* Train for Longer (more epochs)

* Find Ideal Learning Rate

* Get more data (give more opportunities to learn)

* Use **Transfer Learning** to leverage, what another model has learnt and adjust it's use case
"""
