import tkinter as tk

def configure():
    # Add code to handle the configuration here
    pass

def start():
    # Add code to handle the start button click here
    pass

def stop():
    # Add code to handle the stop button click here
    pass

# Create the main window
window = tk.Tk()
window.title("LSL Server Interface")
window.geometry("300x420")  # Set the window size to be square

# Create the device IP address field and label
device_label = tk.Label(window, text="Device IP Address:")
device_label.pack()

device_entry = tk.Entry(window)
device_entry.pack()

# Create the input fields and labels
labels = ['Name:', 'Type:', 'Channel Count:', 'Nominal SRate:', 'Channel Format:', 'Source ID:']
entries = []

for label_text in labels:
    label = tk.Label(window, text=label_text)
    label.pack()

    entry = tk.Entry(window)
    entry.pack()

    entries.append(entry)

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
