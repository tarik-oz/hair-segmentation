import numpy as np

# load the saved data
print("start loading the Train data ....... ")
allImagesNP = np.load("C:/Users/Tarik/Desktop/unetv3.2/data/Unet_Train_Hair_Images.npy")
maskImagesNP = np.load("C:/Users/Tarik/Desktop/unetv3.2/data/Unet_Train_Hair_Masks.npy")

print("start loading the validate data ....... ")

allValidateImagesNP = np.load(
    "C:/Users/Tarik/Desktop/unetv3.2/data/Unet_Valid_Hair_Images.npy"
)
maskValidateImagesNP = np.load(
    "C:/Users/Tarik/Desktop/unetv3.2/data/Unet_Valid_Hair_Masks.npy"
)

print("Finish save the data .............")

# print(allImagesNP.shape)
# print(maskImagesNP.shape)
# print(allValidateImagesNP.shape)
# print(maskValidateImagesNP.shape)

Height = 256
Width = 256

# build the model
import tensorflow as tf
from Step02Model import build_model
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping

shape = (256, 256, 3)
lr = 1e-4  # 0.0001
batch_size = 4
epochs = 10

model = build_model(shape)
# print(model.summary())

opt = tf.keras.optimizers.Adam(lr)
model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])

stepsPerEpoch = np.ceil(len(allImagesNP) / batch_size)
validationSteps = np.ceil(len(allValidateImagesNP) / batch_size)

best_model_file = "C:/Users/Tarik/Desktop/unetv3.2/data/Hair-Unet.h5"

callbacks = [
    ModelCheckpoint(best_model_file, verbose=1, save_best_only=True),
    ReduceLROnPlateau(
        monitor="val_loss", patience=3, factor=0.1, verbose=1, min_lr=1e-6
    ),
    EarlyStopping(monitor="val_accuracy", patience=3, verbose=1),
]


history = model.fit(
    allImagesNP,
    maskImagesNP,
    batch_size=batch_size,
    epochs=epochs,
    verbose=1,
    validation_data=(allValidateImagesNP, maskValidateImagesNP),
    validation_steps=validationSteps,
    steps_per_epoch=stepsPerEpoch,
    shuffle=True,
    callbacks=callbacks,
)
