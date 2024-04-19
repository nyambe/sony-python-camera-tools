import cv2
import os

# Set the directory containing the video files
directory = "/Users/samiebuka/Downloads/auto"

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".mp4"):  # Check if the file is an MP4 video
        video_path = os.path.join(directory, filename)

        # Open the video file
        cap = cv2.VideoCapture(video_path)

        # Check if the video was opened successfully
        if not cap.isOpened():
            print(f"Unable to open video file: {filename}")
            continue

        # Get the total number of frames in the video
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Set the current frame position to the last frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count - 1)

        # Read the last frame
        ret, frame = cap.read()

        # Save the frame as an image
        if ret:
            # Save the image in the same directory with a different name
            output_image_path = os.path.join(directory, f"last_frame_of_{filename}.png")
            cv2.imwrite(output_image_path, frame)
            print(f"Last frame of {filename} saved as {output_image_path}")

        # Release the video capture object
        cap.release()
    else:
        continue
