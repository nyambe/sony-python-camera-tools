import os
import shutil
from datetime import datetime
import xml.etree.ElementTree as ET

print('Start')
# Define the source directory (SD card) and base destination directory
source_dir = '/Volumes/Untitled/PRIVATE/M4ROOT/CLIP'
base_dest_dir = '/Volumes/Dominos/Originales/SD/'

# Get list of all files in source directory
files = os.listdir(source_dir)
print(f'Found {len(files)} files')

# Filter video files
video_files =  [file for file in files if file.lower().endswith('.mp4') or file.lower().endswith('.xml')]
print(f'Found {len(video_files)} video and xml files')

# Sort files by date
video_files.sort(key=lambda x: os.path.getmtime(os.path.join(source_dir, x)))

# Copy sorted files to destination directory
for file in video_files:
    # Get the modification time and format it as yearmonthday
    mod_time = os.path.getmtime(os.path.join(source_dir, file))
    date_subdir = datetime.fromtimestamp(mod_time).strftime('%Y%m%d')

    # Create a new destination directory with the formatted date
    dest_dir = os.path.join(base_dest_dir, date_subdir)

    # Create the directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f'Created directory: {date_subdir}')

    # Copy the file
    shutil.copy(os.path.join(source_dir, file), dest_dir)
    print(f'Copied: {file} to {date_subdir}')

    # If the file is an XML file, create a human-readable text file
    if file.lower().endswith('.xml'):
        # Parse the XML file
        tree = ET.parse(os.path.join(dest_dir, file))
        root = tree.getroot()

        # Open a new text file and write the XML data in a human-readable way
        with open(os.path.join(dest_dir, f'{os.path.splitext(file)[0]}.txt'), 'w') as f:
            for elem in root.iter():
                # Write the tag and text of the element (or "None" if there's no text)
                f.write(f'{elem.tag}: {elem.text.strip() if elem.text else "None"}\n')

print('Finished')
