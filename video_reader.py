import os
import shutil
from datetime import datetime
import xml.etree.ElementTree as ET
import time
import argparse
import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description="Video file organizer and metadata extractor")
    parser.add_argument("--no-xml", action="store_true", help="Skip processing of XML files")
    parser.add_argument("--source", default="/Volumes/Untitled/M4ROOT/CLIP", help="Source directory")
    return parser.parse_args()

def get_connected_volumes():
    volumes = [d for d in os.listdir('/Volumes') if os.path.isdir(os.path.join('/Volumes', d))]
    return volumes

def select_destination_volume():
    volumes = get_connected_volumes()
    print("Available volumes:")
    for i, volume in enumerate(volumes, 1):
        print(f"{i}. {volume}")
    
    while True:
        try:
            choice = int(input("Select the destination volume (enter the number): ")) - 1
            if 0 <= choice < len(volumes):
                selected_volume = os.path.join('/Volumes', volumes[choice])
                original_dir = os.path.join(selected_volume, 'original')
                
                if not os.path.exists(original_dir):
                    create = input(f"The 'original' directory doesn't exist on {volumes[choice]}. Create it? (y/n): ")
                    if create.lower() == 'y':
                        os.makedirs(original_dir)
                        logging.info(f"Created 'original' directory on {volumes[choice]}")
                    else:
                        logging.info("Operation cancelled. Please select a different volume or create the 'original' directory manually.")
                        return select_destination_volume()  # Recursively call the function to prompt again
                
                return original_dir
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def get_video_files(source_dir, include_xml):
    files = os.listdir(source_dir)
    extensions = (".mp4", ".xml") if include_xml else (".mp4",)
    return [f for f in files if f.lower().endswith(extensions)]

def create_dest_directory(base_dest_dir, date_subdir):
    dest_dir = os.path.join(base_dest_dir, date_subdir)
    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir)
            logging.info(f"Created directory: {dest_dir}")
        except PermissionError:
            logging.error(f"Permission denied: Unable to create directory {dest_dir}")
            raise
        except OSError as e:
            logging.error(f"Failed to create directory {dest_dir}: {e}")
            raise
    return dest_dir

def copy_file(source_path, dest_path):
    start_time = time.time()
    shutil.copy2(source_path, dest_path)  # Use copy2 to preserve metadata
    time_taken = time.time() - start_time
    return time_taken

def log_copy_time(file, time_taken):
    if time_taken > 120:
        logging.info(f"Copied: {file}")
        logging.info(f"Time taken to copy: {time_taken / 60:.2f} minutes")
    elif time_taken > 9:
        logging.info(f"Copied: {file}")
        logging.info(f"Time taken to copy: {time_taken:.2f} seconds")
    else:
        logging.info(f"Copied: {file}")
        logging.info(f"Time taken to copy: {time_taken * 1000:.0f} milliseconds")

def extract_xml_metadata(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    namespaces = {"ns": "urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.20"}

    metadata = {}
    for elem in root.findall(".//ns:*", namespaces):
        if 'name' in elem.attrib:
            metadata[elem.attrib['name']] = elem.get('value')
        elif 'value' in elem.attrib:
            metadata[elem.tag.split('}')[-1]] = elem.get('value')

    return metadata

def write_metadata_file(metadata, dest_file_path):
    with open(dest_file_path, 'w') as f:
        for key, value in metadata.items():
            f.write(f"{key}: {value}\n")

def main():
    setup_logging()
    args = parse_arguments()
    
    dest_dir = select_destination_volume()
    if not dest_dir:
        logging.error("No valid destination directory selected. Exiting.")
        return
    
    logging.info(f"Selected destination directory: {dest_dir}")
    
    start_time = time.time()
    video_files = get_video_files(args.source, not args.no_xml)
    logging.info(f"Found {len(video_files)} files to process")

    for file in sorted(video_files, key=lambda x: os.path.getmtime(os.path.join(args.source, x))):
        source_path = os.path.join(args.source, file)
        mod_time = os.path.getmtime(source_path)
        date_subdir = datetime.fromtimestamp(mod_time).strftime("%Y%m%d")
        full_dest_dir = create_dest_directory(dest_dir, date_subdir)
        dest_path = os.path.join(full_dest_dir, file)

        if not os.path.exists(dest_path):
            try:
                time_taken = copy_file(source_path, dest_path)
                log_copy_time(file, time_taken)
            except IOError as e:
                logging.error(f"Failed to copy {file}: {e}")
                continue

        if not args.no_xml and file.lower().endswith('.xml'):
            metadata = extract_xml_metadata(dest_path)
            txt_file_path = os.path.splitext(dest_path)[0] + '.txt'
            if not os.path.exists(txt_file_path):
                try:
                    write_metadata_file(metadata, txt_file_path)
                    logging.info(f"Created metadata file: {txt_file_path}")
                except IOError as e:
                    logging.error(f"Failed to create metadata file for {file}: {e}")

    total_time = time.time() - start_time
    logging.info(f"Total time taken: {int(total_time // 60)} minutes {total_time % 60:.2f} seconds")

if __name__ == "__main__":
    main()