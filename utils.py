from datetime import datetime
import json
import os 
import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils
import time

# load and preprocess the image
def preprocess_image(image):
    """
    load image from path and convert to grayscale
    """
    resized_image = cv2.resize(image, (1280, 720))
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    return resized_image, gray_image

# subtract images
def subtract_images(image1, image2):
    """
    does background substraction
    """
    abs_diff = cv2.absdiff(image1, image2)
    abs_diff_blurred = cv2.GaussianBlur(abs_diff, (5,5), 0)
    _, thresh_abs_diff = cv2.threshold(abs_diff_blurred, 75, 255, cv2.THRESH_BINARY)
    return abs_diff, thresh_abs_diff