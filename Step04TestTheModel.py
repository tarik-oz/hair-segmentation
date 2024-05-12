import numpy as np
import tensorflow as tf
import cv2

# load the model
best_model_file = "C:/Users/Tarik/Desktop/unetv3.2/data/Hair-Unet.h5"

model = tf.keras.models.load_model(best_model_file)
# print(model.summary())

Height = 256
Width = 256

# show one image

imgPath = "C:/Users/Tarik/Desktop/unetv3.2/test.jpg"

img = cv2.imread(imgPath, cv2.IMREAD_COLOR)
# cv2.imshow("imread", img)
# cv2.waitKey(0)

img2 = cv2.resize(img, (Width, Height))
# cv2.imshow("resize", img2)
# cv2.waitKey(0)
img2 = img2 / 255.0
# cv2.imshow("255", img2)
# cv2.waitKey(0)
imgForModel = np.expand_dims(img2, axis=0)
print(imgForModel.shape)


p = model.predict(imgForModel)
resultMask = p[0]

print(resultMask.shape)
# print(resultMask)
print("=================INITIAL OUTPUT=================================")
resizedMask = cv2.resize(resultMask, (16, 16))
print(resizedMask)
print("==================================================")

# since it is a binary classification , any value above 0.5 means predict 1
# and any value under 0.5 is predicted to 0
# 0> black
# 1> white (mask)


# binary_mask = resultMask.astype(np.uint8) * 255
# resizedMask = cv2.resize(binary_mask, (16, 16))
# print(resizedMask)

# resultMask[resultMask <= 0.5] = 0
# resultMask[resultMask > 0.5] = 255
# resizedMask = cv2.resize(resultMask, (16, 16))
# print(resizedMask)

resultMask_normalized = (resultMask - resultMask.min()) / (
    resultMask.max() - resultMask.min()
)
resultMask_scaled = (resultMask_normalized * 255).astype(np.uint8)

# resultMask[resultMask_scaled <= 100] = 0
# resultMask[resultMask_scaled > 100] = 255


scale_precent = 100

w = int(img.shape[1] * scale_precent / 100)
h = int(img.shape[0] * scale_precent / 100)
dim = (w, h)


img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
mask = cv2.resize(resultMask_scaled, dim, interpolation=cv2.INTER_AREA)

cv2.imshow("image ", img)
cv2.imshow("Predicted Mask", mask)


cv2.waitKey(0)

# cv2.imwrite("C:/Users/Tarik/Desktop/unetv3.2/testMask.png", mask)
