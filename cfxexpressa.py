import os
import shutil
from datetime import datetime
import xml.etree.ElementTree as ET
import time
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "--no-xml",
    action="store_true",
    help="set this flag to skip processing of XML files",
)
args = parser.parse_args()

# Get the current date and time
now = datetime.now()

# Format the date and time
formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

total_time = time.time()  # Start timer

# Define the source directory (SD card) and base destination directory
source_dir = "/Volumes/Untitled/M4ROOT/CLIP"
base_dest_dir = "/Volumes/Crucial2/original"
# base_dest_dir = "/Volumes/Dominos/Originales/actual"
# base_dest_dir = "/Volumes/Crucial X8/original"
# Get list of all files in source directory
files = os.listdir(source_dir)
print(f"Found {len(files)} files")

# Filter video files
if args.no_xml:
    video_files = [file for file in files if file.lower().endswith(".mp4")]
else:
    video_files = [file for file in files if file.lower().endswith((".mp4", ".xml"))]

print(f"Found {len(video_files)} video and xml files")

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

    # If the file is an XML file, create a human-readable text file
    if not args.no_xml and file.lower().endswith(".xml"):
        # Parse the XML file
        tree = ET.parse(os.path.join(dest_dir, file))
        root = tree.getroot()

        # The XML uses namespaces, so we need to define them
        namespaces = {"ns": "urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.20"}

        # Extract key values
        duration = root.find("ns:Duration", namespaces).get("value")
        creation_date = root.find("ns:CreationDate", namespaces).get("value")
        video_format = root.find("ns:VideoFormat/ns:VideoFrame", namespaces).get(
            "videoCodec"
        )
        audio_format = root.find("ns:AudioFormat", namespaces).get("numOfChannel")
        tc_fps = root.find("ns:LtcChangeTable", namespaces).get("tcFps")
        capture_fps = root.find("ns:VideoFormat/ns:VideoFrame", namespaces).get(
            "captureFps"
        )
        pixel = root.find("ns:VideoFormat/ns:VideoLayout", namespaces).get("pixel")
        vertical_line = root.find("ns:VideoFormat/ns:VideoLayout", namespaces).get(
            "numOfVerticalLine"
        )
        aspect_ratio = root.find("ns:VideoFormat/ns:VideoLayout", namespaces).get(
            "aspectRatio"
        )
        model_name = root.find("ns:Device", namespaces).get("modelName")
        capture_gamma_equation = root.find(
            'ns:AcquisitionRecord/ns:Group/ns:Item[@name="CaptureGammaEquation"]',
            namespaces,
        ).get("value")
        sub_stream = root.find("ns:SubStream", namespaces)
        sub_stream = sub_stream.get("codec") if sub_stream is not None else "Not Found"

        # Check if elements exist and status is "start"
        imager_control_info = root.find(
            'ns:AcquisitionRecord/ns:ChangeTable[@name="ImagerControlInformation"]/ns:Event',
            namespaces,
        )
        lens_control_info = root.find(
            'ns:AcquisitionRecord/ns:ChangeTable[@name="LensControlInformation"]/ns:Event',
            namespaces,
        )
        distortion_correction = root.find(
            'ns:AcquisitionRecord/ns:ChangeTable[@name="DistortionCorrection"]/ns:Event',
            namespaces,
        )
        gyroscope = root.find(
            'ns:AcquisitionRecord/ns:ChangeTable[@name="Gyroscope"]/ns:Event',
            namespaces,
        )
        accelerometer = root.find(
            'ns:AcquisitionRecord/ns:ChangeTable[@name="Accelerometor"]/ns:Event',
            namespaces,
        )

        imager_control_info = (
            imager_control_info is not None
            and imager_control_info.get("status") == "start"
        )
        lens_control_info = (
            lens_control_info is not None and lens_control_info.get("status") == "start"
        )
        distortion_correction = (
            distortion_correction is not None
            and distortion_correction.get("status") == "start"
        )
        gyroscope = gyroscope is not None and gyroscope.get("status") == "start"
        accelerometer = (
            accelerometer is not None and accelerometer.get("status") == "start"
        )

        # Define the destination text file path
        dest_txt_file_path = os.path.join(dest_dir, f"{os.path.splitext(file)[0]}.txt")

        # If the text file doesn't already exist at the destination, create it
        if not os.path.exists(dest_txt_file_path):
            # Create a new text file and write the extracted values
            print(f"")
            print(f"Creating text file: {dest_txt_file_path}")
            with open(dest_txt_file_path, "w") as f:
                f.write(f"File Name: {file}\n")
                f.write(f"Duration: {duration}\n")
                f.write(f"Creation Date: {creation_date}\n")
                f.write(f"Video Format: {video_format}\n")
                f.write(f"Audio Format: {audio_format}\n")
                f.write(f"TC FPS: {tc_fps}\n")
                f.write(f"Capture FPS: {capture_fps}\n")
                f.write(f"Pixel: {pixel}\n")
                f.write(f"Vertical Line: {vertical_line}\n")
                f.write(f"Aspect Ratio: {aspect_ratio}\n")
                f.write(f"Model Name: {model_name}\n")
                f.write(f"Capture Gamma Equation: {capture_gamma_equation}\n")
                f.write(f"Sub Stream: {sub_stream}\n")
                f.write(f"Imager Control Info: {imager_control_info}\n")
                f.write(f"Lens Control Info: {lens_control_info}\n")
                f.write(f"Distortion Correction: {distortion_correction}\n")
                f.write(f"Gyroscope: {gyroscope}\n")
                f.write(f"Accelerometer: {accelerometer}\n")
            print(f"Created text file: {dest_txt_file_path}")
        else:
            print(f"Skipped creating text file: {dest_txt_file_path} (already exists)")

total_time_end = time.time()  # Stop timer
total_time_taken = total_time_end - total_time
total_minutes, total_seconds = divmod(total_time_taken, 60)
formatted_seconds = "{:.2f}".format(total_seconds)


endnow = datetime.now()
formatted_endnow = endnow.strftime("%H:%M:%S")
print(f"Start {formatted_now} ")
print(f"Finished {formatted_endnow}")
print(f"Total time taken: {int(total_minutes)} minutes {formatted_seconds} seconds")
