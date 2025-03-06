# indoor-surveillance-system
consolidates code for indoor-surveillance system - web app

## Pre-requisites

### Install requirements
- create a new python venv

```pip install -r requirements.txt```

### Email setup
- create a .env file
- set your gmail username
- assuming your gmail has 2FA, you need to create an app password. This will be the password you set as password in the .env file.
  - Refer to https://support.google.com/mail/answer/185833?hl=en
- in the .env file, add the following
  - SENDER_EMAIL = '-your gmail address-'
  - SENDER_PASSWORD = '-your app password created above-'
 
### App variables - change these according to your needs
- set recipient_email = '-your own gmail address or another address you want to send notifications to-'
- final_width = 1280
- final_height = 720
- binary_threshold = 100 # change this according to different lighting conditions
- min_contour_area_to_trigger_detection = 10000 # change this to change the minimum bounding box area required to trigger detection (detection is triggered whenever you see a red bounding box on the screen)
- max_small_object_area = 2500 # this is a threshold btwn considering if an object is considered small or big object

## To run the app, do
```streamlit run Home.py```

## Notes
- App works best with current variables in darker room conditions, then use something bright as a 'moving object'. Example dim lights in your room and switch on your phone flashlight and move the phone across your screen. If its too sensitive, increase binary_threshold parameter.
