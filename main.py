import os
import multiprocessing as mp
from functools import partial
from skimage.io import imread
from skimage.transform import resize
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pickle

# Preparing data
input_dir = r'C:\Users\Usuario\Desktop\Python\Image_classification\data\Bottle Images\Bottle Images'
categories = ['Beer Bottles', 'Plastic Bottles', 'Soda Bottle', 'Water Bottle', 'Wine Bottle']

def load_and_preprocess_image(image_path, size=(50, 50)):
    try:
        img = imread(image_path)
        img = resize(img, size)
        return img.flatten()
    except Exception as e:
        print(f"Error loading image '{image_path}': {e}")
        return None

def load_images_from_category(category_dir, size=(50, 50)):
    images = []
    for file in os.listdir(category_dir):
        image_path = os.path.join(category_dir, file)
        img = load_and_preprocess_image(image_path, size)
        if img is not None:
            images.append(img)
    return images

def load_data(input_dir, categories, size=(50, 50)):
    data = []
    labels = []

    for category_idx, category in enumerate(categories):
        category_dir = os.path.join(input_dir, category)
        if not os.path.exists(category_dir):
            print(f"Directory '{category_dir}' does not exist.")
            continue

        images = load_images_from_category(category_dir, size)
        data.extend(images)
        labels.extend([category_idx] * len(images))

    return np.asarray(data), np.asarray(labels)

data, labels = load_data(input_dir, categories)

print("Data shape:", data.shape)
print("Labels shape:", labels.shape)

# Time to train/test split
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# Train the classifier
classifier = SVC()
parameters = [{'gamma': [0.01, 0.001, 0.0001], 'C': [1, 10, 100, 1000]}]

grid_search = GridSearchCV(classifier, parameters)
grid_search.fit(x_train, y_train)

best_estimator = grid_search.best_estimator_
y_predict = best_estimator.predict(x_test)
score = accuracy_score(y_predict, y_test)

print('{}% of samples were correctly classified'.format(str(score * 100)))
pickle.dump(best_estimator, open('/model.p', 'wb'))
