import os
import json
import streamlit as st

# Set Page Configuration
st.set_page_config(layout="wide")

# Title
st.markdown("<h1 style='text-align: center; color: white;'>View video recordings of Intruders</h1>", unsafe_allow_html=True)

recordings_folder_path = "data/recordings"

# Fetch and display recordings
if not os.path.exists(recordings_folder_path) or not os.listdir(recordings_folder_path):
    st.info("No recordings available.")
else:
    for folder in sorted(os.listdir(recordings_folder_path), reverse=True):  # Show latest first
        if folder.startswith("."):
            continue

        video_file_path = os.path.join(recordings_folder_path, folder, "motion.mp4")
        json_file_path = os.path.join(recordings_folder_path, folder, "metadata.json")

        # Skip if required files are missing
        if not os.path.exists(json_file_path) or not os.path.exists(video_file_path):
            continue

        # Load metadata
        with open(json_file_path, "r") as f:
            json_data = json.load(f)

        output_video_filename = json_data.get("video_file", "Unknown")
        timestamp = json_data.get("timestamp", "Unknown Time")
        intruder_position = json_data.get("intruder_position", "Unknown Position")
        intruder_type = json_data.get("intruder_type", "Unknown Intruder")

        # Display each recording in a card-style layout
        with st.container():
            st.markdown(
                f"""
                <div class="recording-card">
                    <h3>🚨 {intruder_type.capitalize()} Detected</h3>
                    <p class="metadata">📍 Intruder spotted leaving the <b>{intruder_position}</b> part of the room.</p>
                    <p class="metadata">⏰ Time of occurrence: <b>{timestamp}</b></p>
                    <p class="metadata">📁 Video stored at: <b>{output_video_filename}</b></p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.video(video_file_path, format="video/mp4")


# ORIGINAL CODE ARCHIVED
# import os
# import json
# import streamlit as st

# recordings_folder_path = 'data/recordings'

# st.markdown("<h1 style='text-align: center; color: white;'>View video recordings of Intruders</h1>", unsafe_allow_html=True)


# for folder in os.listdir(recordings_folder_path):
#     if folder.startswith('.'):
#         continue
#     video_file_path = os.path.join(recordings_folder_path, folder, 'motion.mp4')
#     json_file_path = os.path.join(recordings_folder_path, folder, 'metadata.json')
#     with open(json_file_path, 'r') as f:
#         json_data = json.load(f)


#     output_video_filename = json_data["video_file"]
#     timestamp = json_data["timestamp"]
#     intruder_position = json_data["intruder_position"]
#     intruder_type = json_data["intruder_type"]

#     st.write(f'### {intruder_type} detected.')
#     st.write(f'{intruder_type} spotted leaving the scene at the {intruder_position} part of the room.')
#     st.write(f'Time of occurence: {timestamp}')
#     st.write(f'Video filename stored at: {output_video_filename}')

#     st.write(str(json_data))
#     st.video(
#         data=video_file_path,
#         format='video/mp4'
#     )


# # TO DO: 
# # save video and metadata in separate folders (metadata info from chatgpt > save in json)
# # View_Recordings.py > display video and the metadata info above it (use markdown ## for heading 2 
# # Push notifcation message > put in utils function
# # clean code and scripts, abstract code into functions where possible
# # beautify UI > add info for ChatGPT like the context of this project then chatgpt can clean more

# # still need jump on a zoom call to explain how it works > send tele bb of how it works and then 
# ## message Erika and ask for 250, then dont go under 230 > say the detection algo was tricky and web dashboard was a big ask
