import os
import shutil
from datetime import datetime
import xml.etree.ElementTree as ET

print("Start")
# Define the source directory (SD card) and base destination directory
source_dir = "/Volumes/Untitled/PRIVATE/M4ROOT/CLIP"
base_dest_dir = "/Volumes/Dominos/Originales/SD/"

# Get list of all files in source directory
files = os.listdir(source_dir)
print(f"Found {len(files)} files")

# Filter video files
video_files = [
    file
    for file in files
    if file.lower().endswith(".mp4") or file.lower().endswith(".xml")
]
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
        shutil.copy(os.path.join(source_dir, file), dest_dir)
        print(f"Copied: {file} to {date_subdir}")
        print(f"")
    else:
        print(f"Skipped: {file} (already exists at destination)")
        print(f"")

    # If the file is an XML file, create a human-readable text file
    if file.lower().endswith(".xml"):
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


print("Finished")
