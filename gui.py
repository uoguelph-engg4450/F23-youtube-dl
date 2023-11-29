import tkinter as tk
import youtube_dl
from tkinter import ttk
from tkinter import filedialog, font
import os
import re
import threading

VALID_FORMATS = {"mp4", "mp3", "avi", "mkv", "flv", "wav"}


def download_link(index, link, output_path, output_name, num_links):
    status_label.config(text=f"Downloading {index}/{num_links}...")
    # Construct the output file name
    parts = output_name.split(".")
    if len(parts) > 1 and parts[-1] in VALID_FORMATS:
        filename = f"{parts[0]}_{index}.{parts[1]}"
    else:
        filename = (
            f"{output_name}_{index}.mp4"  # Default to .mp4 if no format is provided
        )

    # Define youtube-dl options
    ydl_opts = {"format": "best", "outtmpl": os.path.join(output_path, filename)}

    # Download using youtube-dl
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        status_label.config(text=f"Download {index + 1}/{num_links} Complete")
    except Exception as e:
        status_label.config(text=f"Download {index + 1}/{num_links} Failed: {e}")


def is_valid_url(url):
    if not isinstance(url, str):
        return False
    # Simple URL validation
    regex = re.compile(
        r"^(?:http|ftp)s?://",
        re.IGNORECASE,
    )
    return re.match(regex, url) is not None


def is_valid_filename(filename):
    if len(filename) < 1:
        return False
    # Check for illegal characters in filename
    illegal_chars = set('<>:"/\\|?*')
    if any((c in illegal_chars) for c in filename):
        return False
    # Check if file format is valid
    parts = filename.split(".")
    if len(parts) > 1 and parts[-1] in VALID_FORMATS:
        return True
    # No file extension or just one part
    return len(parts) == 1


def start_download():
    links = listbox.get(0, tk.END)
    output_path = path_entry.get()
    output_name = name_entry.get()  # Assuming you've added this

    # reset colors of all links
    for i in range(len(links)):
        listbox.itemconfig(i, {"fg": "black"})

    # Validate output path
    if not os.path.exists(output_path):
        status_label.config(text="Invalid output path")
        path_entry.config(highlightthickness=2)
        return
    else:
        path_entry.config(highlightthickness=0)

    # Validate output file name
    if not is_valid_filename(output_name):
        status_label.config(text="Invalid output file name")
        name_entry.config(highlightthickness=2)
        return
    else:
        name_entry.config(highlightthickness=0)

    # Validate links and highlight invalid ones
    if len(links) < 1:
        status_label.config(text="No Link(s) Found")
        return
    else:
        all_links_valid = True
        for index, link in enumerate(links):
            if link and not is_valid_url(link):
                listbox.itemconfig(index, {"fg": "red"})  # Change color to red
                all_links_valid = False

        if not all_links_valid:
            status_label.config(text="Invalid link(s) found")
            return

    for index, link in enumerate(links):
        threading.Thread(
            target=download_link,
            args=(index, link, output_path, output_name, len(links)),
        ).start()


def add_link():
    link = link_entry.get()
    if link:
        listbox.insert(tk.END, link)
        link_entry.delete(0, tk.END)


def remove_link():
    selected_indices = listbox.curselection()
    for i in selected_indices[::-1]:
        listbox.delete(i)


def browse_output_path():
    path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, path)


# Create the main window
root = tk.Tk()
root.title("YouTube-dl GUI")
root.geometry("450x450")
root.resizable(False, False)

# Custom font
custom_font = font.Font(family="Consolas", size=10)


# Label for the listbox
listbox_label = tk.Label(root, text="Links to Download", font=custom_font)
listbox_label.pack()

# Listbox for links
listbox = tk.Listbox(root, height=10, width=50, font=custom_font)
listbox.pack()

# Frame for link management buttons
link_management_frame0 = tk.Frame(root)
link_management_frame0.pack(pady=5)

# Label for the new links
links_label = tk.Label(link_management_frame0, text="New Link:", font=custom_font)
links_label.grid(row=0, column=0, padx=(0, 5))

# Entry widget for adding new links
link_entry = tk.Entry(link_management_frame0, width=40, font=custom_font)
link_entry.grid(row=0, column=1)

# Frame for link management buttons
link_management_frame = tk.Frame(root)
link_management_frame.pack(pady=5)

# Button to add the link to the Listbox
add_link_button = tk.Button(
    link_management_frame, text="Add Link", command=add_link, font=custom_font
)
add_link_button.grid(row=0, column=1)

# Button to remove the selected link from the Listbox
remove_link_button = tk.Button(
    link_management_frame,
    text="Remove Selected Link",
    command=remove_link,
    font=custom_font,
)
remove_link_button.grid(row=0, column=2, padx=5)

# Create a horizontal separator
separator = ttk.Separator(root, orient="horizontal")

# Place the separator below the listbox
separator.pack(fill="x", pady=10)

# Frame for output name entry
output_name_frame = tk.Frame(root)
output_name_frame.pack(pady=5, padx=[0, 62])

# Label and entry for the output name
name_label = tk.Label(output_name_frame, text="Output Name:", font=custom_font)
name_label.grid(row=0, column=0, padx=(0, 5))
name_entry = tk.Entry(
    output_name_frame, width=40, font=custom_font, highlightbackground="red"
)
name_entry.grid(row=0, column=1)

# Frame for output path entry and browse button
output_path_frame = tk.Frame(root)
output_path_frame.pack(pady=5)

# Label and entry for the output path
path_label = tk.Label(output_path_frame, text="Output Path:", font=custom_font)
path_label.grid(row=0, column=0, padx=(0, 5))
path_entry = tk.Entry(
    output_path_frame, width=40, font=custom_font, highlightbackground="red"
)
path_entry.grid(row=0, column=1)

# Button to browse for output path
browse_button = tk.Button(
    output_path_frame, text="Browse", command=browse_output_path, font=custom_font
)
browse_button.grid(row=0, column=2, padx=5)

# Create a horizontal separator
separator = ttk.Separator(root, orient="horizontal")

# Place the separator below the listbox
separator.pack(fill="x", pady=10)

# Start Button
start_button = tk.Button(
    root, text="Start Download", command=start_download, font=custom_font
)
start_button.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="Status: Ready", font=custom_font)
status_label.pack()

# Start the GUI loop
root.mainloop()
