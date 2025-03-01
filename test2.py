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
    _, thresh_abs_diff = cv2.threshold(abs_diff_blurred, 100, 255, cv2.THRESH_BINARY)
    return abs_diff, thresh_abs_diff


def main():
    # video_path = 'data/test.mp4'
    # video_cap = cv2.VideoCapture(video_path)

    video_cap = cv2.VideoCapture(0) # capture from webcam
    reference_frame = None

    while True:
        try: 
            # try reading from camera/video feed
            status, input_rgb_frame = video_cap.read()
        except Exception as e:
            print(e)
            print('Unable to show webcam - you need to enable permissions on your machine')
            break

        # preprocess input image
        resized_input_rgb_frame, resized_input_gray_frame = preprocess_image(input_rgb_frame)

        # initialise first previous frame, this code is only run at the start
        if reference_frame is None:
            reference_frame = resized_input_gray_frame

        # get the subtract frames and threshold to make diff more obvious
        abs_diff, thresh_abs_diff = subtract_images(reference_frame, resized_input_gray_frame)
        dilated_image = cv2.dilate(thresh_abs_diff, None, iterations=10)

        # get contours
        cnts = cv2.findContours(dilated_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts) # each array is a coordinate with a contour in the image

        # iterate the contours - draw bounding box of the large contour areas
        # can also draw contours instead of bbox - cv2.drawContours(frame1, contours, -1, (0, 0, 255), 2)
        for c in cnts:
            if cv2.contourArea(c) > 7500: # only want to take the large contours to avoid noise
                (x, y, w, h) = cv2.boundingRect(c) # generate the bounding box coordinates
                cv2.rectangle(
                    img=resized_input_rgb_frame, 
                    pt1=(x, y), 
                    pt2=(x+w, y+h), 
                    color=(0, 0, 255), 
                    thickness=3
                ) # draws the bbox on the src image

        # cv2.imshow("Motion Detection", resized_input_rgb_frame)
        cv2.imshow("Motion Detection", resized_input_rgb_frame)
        # cv2.imshow("Motion Detection", resized_input_rgb_frame[200:,150:-150] )

        # # exit if any key is pressed
        if cv2.waitKey(1) & 0xFF != 255:
            break
        # time.sleep(0.1)
        # reference_frame = resized_input_gray_frame # can set the the last -20 image as well


    video_cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()