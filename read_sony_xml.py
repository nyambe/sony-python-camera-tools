import xml.etree.ElementTree as ET
import sys

def read_sony_xml(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # The XML uses namespaces, so we need to define them
    namespaces = {
        'ns': 'urn:schemas-professionalDisc:nonRealTimeMeta:ver.2.20'
    }

    # Extract key values
    duration = root.find('ns:Duration', namespaces).get('value')
    creation_date = root.find('ns:CreationDate', namespaces).get('value')
    video_format = root.find('ns:VideoFormat/ns:VideoFrame', namespaces).get('videoCodec')
    audio_format = root.find('ns:AudioFormat', namespaces).get('numOfChannel')

    # Print the extracted values
    print(f'Duration: {duration}')
    print(f'Creation Date: {creation_date}')
    print(f'Video Format: {video_format}')
    print(f'Audio Format: {audio_format}')

# Run the function on your XML file

if __name__ == "__main__":
    # Run the function on the XML file passed as a command line argument
    read_sony_xml(sys.argv[1])

#read_sony_xml('/path/to/your/xml/file.xml')
