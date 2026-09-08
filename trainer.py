import cv2
import numpy as np
from PIL import Image
import os

# create recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

dataset_path = "dataset"

face_samples = []
ids = []

# read dataset images
for image_name in os.listdir(dataset_path):

    image_path = os.path.join(dataset_path, image_name)

    gray_image = Image.open(image_path).convert('L')

    image_numpy = np.array(gray_image, 'uint8')

    # extract ID from filename
    user_id = int(image_name.split(".")[1])

    face_samples.append(image_numpy)
    ids.append(user_id)

# train recognizer
recognizer.train(face_samples, np.array(ids))

# save trained model
recognizer.save("trainer.yml")

print("✅ Training Complete")