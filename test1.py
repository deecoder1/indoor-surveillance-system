import os 
import cv2
import matplotlib.pyplot as plt
import imutils

# load and preprocess the image
def load_and_preprocess(image_path):
    """
    load image from path and convert to grayscale
    """
    image = cv2.imread(image_path)
    image = cv2.resize(image, (1280, 720))
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image, gray_image

# subtract images
def subtract_images(image1, image2):
    """
    does background substraction
    """
    diff = cv2.absdiff(image1, image2)
    _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
    return diff, thresh


def main():
    image_path1 = 'data/static.png' # original image
    image_path2 = 'data/test.png' # ss of original image at next frame (has static image of moving bus and car in the background)
    assert os.path.exists(image_path1)
    assert os.path.exists(image_path2)

    image1, gray_image1 = load_and_preprocess(image_path1)
    image2, gray_image2 = load_and_preprocess(image_path2)

    # subtract the images
    diff, thresh = subtract_images(gray_image1, gray_image2)

    # plot the images
    plt.figure(figsize=(15, 7))

    plt.subplot(2, 2, 1)
    plt.title('Static Image')
    plt.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.title('Test Image')
    plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.title('Difference')
    plt.imshow(diff, cmap='gray')
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.title('Threshold Difference')
    plt.imshow(thresh, cmap='gray')
    plt.axis('off')

    plt.show()
    dilated_image = cv2.dilate(thresh, None, iterations=2)
    plt.imshow(dilated_image, cmap='gray')
    plt.axis('off')
    plt.show()

    # movements of trees
    cnts = cv2.findContours(dilated_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # cnts
    cnts # pixel coordinates
    # iterate the contours
    for c in cnts:
        if cv2.contourArea(c) < 700:
            continue

        # get the bounding box coordinates
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(image2, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow('test', image2)
    cv2.waitKey(5000)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()