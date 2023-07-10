import tkinter as tk
import json
import requests
from tkinter import messagebox
from enum import Enum

class ChannelId(Enum):
    ACQ_CHANNEL_1 = 1
    ACQ_CHANNEL_2 = 1 << 1
    ACQ_CHANNEL_3 = 1 << 2
    ACQ_CHANNEL_4 = 1 << 3
    ACQ_CHANNEL_5 = 1 << 4
    ACQ_CHANNEL_6 = 1 << 5
    ACQ_CHANNEL_7 = 1 << 6
    ACQ_CHANNEL_8 = 1 << 7

channels = [
    ChannelId.ACQ_CHANNEL_1,
    ChannelId.ACQ_CHANNEL_2,
    ChannelId.ACQ_CHANNEL_3,
    ChannelId.ACQ_CHANNEL_4,
    ChannelId.ACQ_CHANNEL_5,
    ChannelId.ACQ_CHANNEL_6
]

class ChannelIdEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ChannelId):
            print(obj.name)
            print(obj.value)
            return obj.name
        return super().default(obj)

def configure():
    if not device_entry.get():  # Check if the field is empty
        tk.messagebox.showwarning("Field Empty", "Please fill in the Local Server URL")
        return
    data = {}
    for i in range(len(labels)):
        label_text = requestLabels[i]
        entry_text = entries[i].get()
        if not entry_text:  # Check if the field is empty
            errorMessage = "Please fill in the " + labels[i]
            tk.messagebox.showwarning("Field Empty",errorMessage[:len(errorMessage) - 1])
            return
        data[label_text.lower()] = entry_text
    
    json_data = {
        "messageType": "LSL_OUTLET_CONFIG",
        "messageSource": "Server Interface",
        "data": data
    }
    
    # Convert the JSON data to a string
    json_str = json.dumps(json_data, indent=4)
    print(json_str)
    
    # Make a POST request to the desired IP address
    url = device_entry.get() + "/update"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_str, headers=headers)
    
    # Handle the response
    print(response.text)


def start():
    if not entries[3].get():  # Check if the field is empty
        tk.messagebox.showwarning("Field Empty", "Please fill in the Sampling Rate.")
        return
    if not device_entry.get():  # Check if the field is empty
        tk.messagebox.showwarning("Field Empty", "Please fill in the Local Server URL")
        return
    data = {}
    data["samplingRateHz"] = entries[3].get()
    data["sessionToken"] = 1
    data["samplesPerEpoch"] = 64
    data["enabledChannels"] = [channel.name for channel in channels]
    data["measureImpedance"] = False
    
    json_data = {
        "messageType": "START_TELEMETRY_MESSAGE",
        "messageSource": "Server Interface",
        "data": data
    }
    
    # Convert the JSON data to a string
    json_str = json.dumps(json_data, indent=4, cls=ChannelIdEncoder)
    print(json_str)
    
    # Make a POST request to the desired IP address
    url = device_entry.get() + "/update"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_str, headers=headers)
    
    # Handle the response
    print(response.text)

def stop():
    if not device_entry.get():  # Check if the field is empty
        tk.messagebox.showwarning("Field Empty", "Please fill in the Local Server URL")
        return
    data = {}
    data["sessionToken"] = 1
    
    json_data = {
        "messageType": "STOP_TELEMETRY_MESSAGE",
        "messageSource": "Server Interface",
        "data": data
    }
    
    # Convert the JSON data to a string
    json_str = json.dumps(json_data, indent=4)
    print(json_str)
    
    # Make a POST request to the desired IP address
    url = device_entry.get() + "/update"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_str, headers=headers)
    
    # Handle the response
    print(response.text)

# Create the main window
window = tk.Tk()
window.title("LSL Server Interface")
window.geometry("300x420")  # Set the window size to be square

# Create the device IP address field and label
device_label = tk.Label(window, text="Local Server URL:")
device_label.pack()

device_entry = tk.Entry(window)
device_entry.pack()

# Create the input fields and labels
labels = ['Name:', 'Type:', 'Channel Count:', 'Nominal SRate:', 'Source ID:']
requestLabels = ['name', 'type', 'channel_count', 'nominal_srate', 'source_id']
defaultValues = ['boneshaker', 'EEG', 6, 250, 'CXN_UID']
entries = []

for i, label_text in enumerate(labels):
    label = tk.Label(window, text=label_text)
    label.pack()

    entry_text = defaultValues[i]
    entry = tk.Entry(window)
    entry.insert(0, entry_text)
    entry.pack()

    entries.append(entry)

# Create the channel format dropdown menu
channel_format_label = tk.Label(window, text='Channel Format:')
channel_format_label.pack()

channel_format_var = tk.StringVar(window)
channel_format_var.set("1")  # Default value is set to 1
channel_format_dropdown = tk.OptionMenu(window, channel_format_var, *range(1, 8))
channel_format_dropdown.pack()

def get_channel_format():
    channel_format = int(channel_format_var.get())
    print(channel_format)

# Create the configure button
configure_button = tk.Button(window, text="Configure", bg="yellow", command=configure)
configure_button.pack()

# Create the start and stop buttons
button_frame = tk.Frame(window)

start_button = tk.Button(button_frame, text="Start", bg="green", command=start)
start_button.pack(side="left")

stop_button = tk.Button(button_frame, text="Stop", bg="red", command=stop)
stop_button.pack(side="left")

button_frame.pack()

# Start the GUI event loop
window.mainloop()
