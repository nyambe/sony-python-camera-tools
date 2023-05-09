#gui_sony_xml.py
import tkinter as tk
from tkinter import filedialog
import os
import xml.etree.ElementTree as ET

def read_sony_xml(file_path, text_widget):
    # Your function here
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
    tc_fps = root.find('ns:LtcChangeTable', namespaces).get('tcFps')
    capture_fps = root.find('ns:VideoFormat/ns:VideoFrame', namespaces).get('captureFps')
    pixel = root.find('ns:VideoFormat/ns:VideoLayout', namespaces).get('pixel')
    vertical_line = root.find('ns:VideoFormat/ns:VideoLayout', namespaces).get('numOfVerticalLine')
    aspect_ratio = root.find('ns:VideoFormat/ns:VideoLayout', namespaces).get('aspectRatio')
    model_name = root.find('ns:Device', namespaces).get('modelName')
    capture_gamma_equation = root.find('ns:AcquisitionRecord/ns:Group/ns:Item[@name="CaptureGammaEquation"]', namespaces).get('value')
    sub_stream = root.find('ns:SubStream', namespaces)
    sub_stream = sub_stream.get('codec') if sub_stream is not None else 'Not Found'
    
    # Check if elements exist and status is "start"
    imager_control_info = root.find('ns:AcquisitionRecord/ns:ChangeTable[@name="ImagerControlInformation"]/ns:Event', namespaces)
    lens_control_info = root.find('ns:AcquisitionRecord/ns:ChangeTable[@name="LensControlInformation"]/ns:Event', namespaces)
    distortion_correction = root.find('ns:AcquisitionRecord/ns:ChangeTable[@name="DistortionCorrection"]/ns:Event', namespaces)
    gyroscope = root.find('ns:AcquisitionRecord/ns:ChangeTable[@name="Gyroscope"]/ns:Event', namespaces)
    accelerometer = root.find('ns:AcquisitionRecord/ns:ChangeTable[@name="Accelerometor"]/ns:Event', namespaces)

    imager_control_info = imager_control_info is not None and imager_control_info.get('status') == 'start'
    lens_control_info = lens_control_info is not None and lens_control_info.get('status') == 'start'
    distortion_correction = distortion_correction is not None and distortion_correction.get('status') == 'start'
    gyroscope = gyroscope is not None and gyroscope.get('status') == 'start'
    accelerometer = accelerometer is not None and accelerometer.get('status') == 'start'
    
    # Print the extracted values
    text_widget.insert('end', f'Duration: {duration}\n')
    text_widget.insert('end', f'Creation Date: {creation_date}\n')
    text_widget.insert('end', f'Video Format: {video_format}\n')
    text_widget.insert('end', f'Audio Format: {audio_format}\n')
    text_widget.insert('end', f'TC FPS: {tc_fps}\n')
    text_widget.insert('end', f'Capture FPS: {capture_fps}\n')
    text_widget.insert('end', f'Pixel: {pixel}\n')
    text_widget.insert('end', f'Vertical Line: {vertical_line}\n')
    text_widget.insert('end', f'Aspect Ratio: {aspect_ratio}\n')
    text_widget.insert('end', f'Model Name: {model_name}\n')
    text_widget.insert('end', f'Capture Gamma Equation: {capture_gamma_equation}\n')
    text_widget.insert('end', f'Sub Stream: {sub_stream}\n')
    text_widget.insert('end', f'Imager Control Information: {imager_control_info}\n')
    text_widget.insert('end', f'Lens Control Information: {lens_control_info}\n')
    text_widget.insert('end', f'Distortion Correction: {distortion_correction}\n')
    text_widget.insert('end', f'Gyroscope: {gyroscope}\n')
    text_widget.insert('end', f'Accelerometer: {accelerometer}\n')

pass

def browse_file(text_widget):
    file_path = filedialog.askopenfilename(filetypes = (("XML files","*.xml"),("all files","*.*")))
    if file_path:
       root.title(f"Selected File: {file_path}")
       read_sony_xml(file_path, text_widget)

root = tk.Tk()
text_widget = tk.Text(root)
text_widget.pack()
button = tk.Button(root, text="Browse", command=lambda: browse_file(text_widget))
button.pack()

root.mainloop()
