from datetime import datetime
import json
import os 
import cv2
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


def main():
    # video_path = 'data/test1.mp4'
    # video_cap = cv2.VideoCapture(video_path)

    time.sleep(1)

    video_cap = cv2.VideoCapture(0) # capture from webcam
    reference_frame = None
    movement_detected = False
    recording_frames = []  # To store 150 frames for saving
    frame_count = 0
    recordings_folder_path = "data/recordings"
    os.makedirs(recordings_folder_path, exist_ok=True)  # Ensure folder exists

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
            continue

        # get the subtract frames and threshold to make diff more obvious
        abs_diff, thresh_abs_diff = subtract_images(reference_frame, resized_input_gray_frame)
        dilated_image = cv2.dilate(thresh_abs_diff, None, iterations=5)

        # get contours
        cnts = cv2.findContours(dilated_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts) # each array is a coordinate with a contour in the image

        # iterate the contours - draw bounding box of the large contour areas
        # can also draw contours instead of bbox - cv2.drawContours(frame1, contours, -1, (0, 0, 255), 2)
        for c in cnts:            
            if cv2.contourArea(c) > 10000: # only want to take the large contours to avoid noise
                (x, y, w, h) = cv2.boundingRect(c) # generate the bounding box coordinates
                cv2.rectangle(
                    img=resized_input_rgb_frame, 
                    pt1=(x, y), 
                    pt2=(x+w, y+h), 
                    color=(0, 0, 255), 
                    thickness=3
                ) # draws the bbox on the src image
                movement_detected = True

                # Determine intruder location (left or right)
                frame_center = 1280 // 2  # Half of frame width
                if (x + w) // 2 < frame_center:
                    intruder_position = "Left"
                else:
                    intruder_position = "Right"
        intruder_type = "Small object" if max([cv2.contourArea(c) for c in cnts], default=0) < 2500 else "Big object"

        cv2.imshow("Motion Detection", resized_input_rgb_frame)
        # cv2.imshow("Motion Detection", resized_input_rgb_frame[200:,150:-150])

        # If movement detected, start recording the next 150 frames
        if movement_detected:
            recording_frames.append(resized_input_rgb_frame)
            frame_count += 1

            if frame_count == 150:  # After 150 frames (5 seconds at 30 FPS)
                # Save video
                video_index = len([f for f in os.listdir(recordings_folder_path) if not f.startswith('.')]) + 1
                output_folder = f"{recordings_folder_path}/motion_{video_index}"
                os.makedirs(output_folder, exist_ok=True)  # Ensure folder exists
                output_video_filename = f"{output_folder}/motion.mp4"
                
                # Define video writer
                fourcc = cv2.VideoWriter_fourcc(*"avc1")  # H.264 codec
                out = cv2.VideoWriter(output_video_filename, fourcc, 30, (1280, 720))

                for frame in recording_frames:
                    out.write(frame)

                out.release()
                print(f"Saved at: {output_video_filename}")

                # Get current timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                metadata_entry = {
                    "video_file": output_video_filename,
                    "timestamp": timestamp,
                    "intruder_position": intruder_position,
                    "intruder_type": intruder_type
                }

                # Save metadata to a JSON file
                metadata_filename = f"{output_folder}/metadata.json"
                with open(metadata_filename, "w") as f:
                    json.dump(metadata_entry, f)
                print(f"Saved metadata: {metadata_entry} at: {metadata_filename}")

                # Reset for next detection
                recording_frames = []
                movement_detected = False
                frame_count = 0

        # # exit if any key is pressed
        if cv2.waitKey(1) & 0xFF != 255:
            break
        # time.sleep(0.1)
        # reference_frame = resized_input_gray_frame # can set the the last -20 image as well

    video_cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()