import os
import shutil
from datetime import datetime
import time
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser()
args = parser.parse_args()

# Get the current date and time
now = datetime.now()

# Format the date and time
formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

total_time = time.time()  # Start timer

# Define the source directory (SD card) and base destination directory
source_dir = "/Volumes/Insta360GO3/DCIM/Camera01"
base_dest_dir = "/Volumes/Crucial3/original"

# Get list of all files in source directory
files = os.listdir(source_dir)
print(f"Found {len(files)} files")

# Filter video files that start with 'VID_'
video_files = [
    file
    for file in files
    if (file.lower().startswith("vid_") or file.lower().startswith("pro_vid_")  or file.lower().startswith("lrv_") or file.lower().startswith("pro_lrv_")) 
    and file.lower().endswith(".mp4")
]

print(f"Found {len(video_files)} video files")

# Sort files by date
video_files.sort(key=lambda x: os.path.getmtime(os.path.join(source_dir, x)))

# Copy sorted files to destination directory
for file in video_files:
    # Get the modification time and format it as yearmonthday
    mod_time = os.path.getmtime(os.path.join(source_dir, file))
    date_subdir = datetime.fromtimestamp(mod_time).strftime("%Y%m%d")

    # Create a new destination directory with the formatted date
    dest_dir = os.path.join(base_dest_dir, date_subdir)

    # Create the directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"")
        print(f"------------------------------------------")
        print(f"Created directory: {date_subdir}")
        print(f"------------------------------------------")
        print(f"")

    # Define the destination file path
    dest_file_path = os.path.join(dest_dir, file)

    # If the file doesn't already exist at the destination, copy it
    if not os.path.exists(dest_file_path):
        print(f"Copying...: {file}")
        start_time = time.time()  # Start timer
        shutil.copy(os.path.join(source_dir, file), dest_dir)
        end_time = time.time()  # End timer
        time_taken = end_time - start_time
        # Convert to milliseconds and round to nearest whole number
        milliseconds = round(time_taken * 1000)
        seconds = time_taken
        minutes = time_taken / 60

        # If time taken is more than 9000 milliseconds but less than 120 seconds
        if milliseconds > 9000 and seconds <= 120:
            print(f"Copied: {file}")
            print(f"Time taken to copy: {round(seconds, 2)} seconds")
            print(f"")

        # If time taken is more than 120 seconds
        elif seconds > 120:
            print(f"Copied: {file}")
            print(f"Time taken to copy: {round(minutes, 2)} minutes")
            print(f"")

        # If time taken is less than or equal to 9000 milliseconds
        else:
            print(f"Copied: {file}")
            print(f"Time taken to copy: {milliseconds} milliseconds")
            print(f"")

total_time_end = time.time()  # Stop timer
total_time_taken = total_time_end - total_time
total_minutes, total_seconds = divmod(total_time_taken, 60)
formatted_seconds = "{:.2f}".format(total_seconds)

endnow = datetime.now()
formatted_endnow = endnow.strftime("%H:%M:%S")
print(f"Start {formatted_now} ")
print(f"Finished {formatted_endnow}")
print(f"Total time taken: {int(total_minutes)} minutes {formatted_seconds} seconds")
