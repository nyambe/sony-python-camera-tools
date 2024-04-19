import pyperclip
import time
import re
import os
import subprocess
import threading


def is_valid_url(url):
    url_regex = re.compile(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    return url_regex.match(url) is not None


def download_video(url):
    try:
        result = subprocess.run(["youtube-dl", url], check=True, text=True)
        print(f"Successfully downloaded: {url}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {url}: {e}")


def main():
    last_clipboard_content = ""

    while True:
        current_clipboard_content = pyperclip.paste()

        if current_clipboard_content != last_clipboard_content:
            if is_valid_url(current_clipboard_content):
                # Create and start a new thread for each download
                download_thread = threading.Thread(
                    target=download_video, args=(current_clipboard_content,)
                )
                download_thread.start()

            last_clipboard_content = current_clipboard_content

        time.sleep(1)


if __name__ == "__main__":
    main()
