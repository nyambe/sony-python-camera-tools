import os
import shutil
from datetime import datetime
import time
import argparse
import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    parser = argparse.ArgumentParser(description="Insta360 video file organizer")
    parser.add_argument("--source", default="/Volumes/Insta360GO3/DCIM/Camera01", help="Source directory")
    return parser.parse_args()

def get_connected_volumes():
    ignore_volumes = ["Insta360GO3", "Macintosh HD", ".timemachine", "Untitled"]
    volumes = [
        d for d in os.listdir('/Volumes') 
        if os.path.isdir(os.path.join('/Volumes', d)) and d not in ignore_volumes
    ]
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
                insta360_dir = os.path.join(selected_volume, 'insta360')
                
                if not os.path.exists(insta360_dir):
                    create = input(f"The 'insta360' directory doesn't exist on {volumes[choice]}. Create it? (y/n): ")
                    if create.lower() == 'y':
                        os.makedirs(insta360_dir)
                        logging.info(f"Created 'insta360' directory on {volumes[choice]}")
                    else:
                        logging.info("Operation cancelled. Please select a different volume or create the 'insta360' directory manually.")
                        return select_destination_volume()  # Recursively call the function to prompt again
                
                return insta360_dir
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def get_insta360_files(source_dir):
    files = os.listdir(source_dir)
    video_files = [
        file for file in files
        if (file.lower().startswith(("vid_", "pro_vid_", "lrv_", "pro_lrv_"))) 
        and (file.lower().endswith(".mp4") or file.lower().endswith(".lrv"))
    ]
    return video_files

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
    elif time_taken > 2:
        logging.info(f"Copied: {file}")
        logging.info(f"Time taken to copy: {time_taken:.2f} seconds")
    else:
        logging.info(f"Copied: {file}")
        logging.info(f"Time taken to copy: {time_taken * 1000:.0f} milliseconds")

def main():
    setup_logging()
    args = parse_arguments()
    
    dest_dir = select_destination_volume()
    if not dest_dir:
        logging.error("No valid destination directory selected. Exiting.")
        return
    
    logging.info(f"Selected destination directory: {dest_dir}")
    
    start_time = time.time()
    video_files = get_insta360_files(args.source)
    logging.info(f"Found {len(video_files)} Insta360 video files to process")

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

    total_time = time.time() - start_time
    logging.info(f"Total time taken: {int(total_time // 60)} minutes {total_time % 60:.2f} seconds")

if __name__ == "__main__":
    main()