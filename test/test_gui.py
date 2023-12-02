import time
import tkinter as tk
import unittest
from unittest.mock import MagicMock, patch
import pytest
import threading
import pyautogui
import sys
from multiprocessing import Process

sys.path.append("..")
from gui import (
    is_valid_filename,
    is_valid_url,
    add_link,
    remove_link,
    start_download,
    download_link,
    browse_output_path,
)
import gui


def run_gui_app():
    gui.root.mainloop()


@pytest.fixture(scope="module")
def app_process():
    # Start the GUI in a separate process
    process = Process(target=run_gui_app)
    process.start()
    time.sleep(5)  # Give enough time for the GUI to fully initialize
    yield
    process.terminate()  # Terminate the GUI process when tests are done


# Adjust the helper functions to work as independent functions rather than methods
# Add the correct x and y coordinates for your system where indicated


# Helper function to add a link using pyautogui
def add_link(url, add_link_entry_x, add_link_entry_y):
    pyautogui.click(
        x=add_link_entry_x, y=add_link_entry_y
    )  # Click on the link entry field
    pyautogui.write(url)  # Type the link
    pyautogui.press("tab")  # Navigate to the "Add Link" button
    pyautogui.press("enter")  # Press the "Add Link" button
    time.sleep(0.5)  # Wait for the GUI to update


# Helper function to remove a link using pyautogui
def remove_link(link_index, listbox_x, listbox_y):
    pyautogui.click(
        x=listbox_x, y=listbox_y + 20 * link_index
    )  # Click on the link at the given index
    pyautogui.press(
        "tab", presses=3, interval=0.25
    )  # Navigate to the "Remove Selected Link" button
    pyautogui.press("enter")  # Press the "Remove Selected Link" button
    time.sleep(0.5)  # Wait for the GUI to update


# Integration test to add and remove links
@pytest.mark.integration
def test_add_and_remove_links(app_process):
    # Add three links
    add_link("http://www.example1.com", add_link_entry_x=315, add_link_entry_y=335)
    add_link("http://www.example2.com", add_link_entry_x=315, add_link_entry_y=335)
    add_link("http://www.example3.com", add_link_entry_x=315, add_link_entry_y=335)

    # Now remove the second link
    remove_link(link_index=1, listbox_x=355, listbox_y=215)


# Parameterized tests for is_valid_url
@pytest.mark.parametrize(
    "url, expected",
    [
        ("http://www.example.com", True),
        ("https://www.example.com", True),
        ("ftp://www.example.com", True),
        ("www.example.com", False),
        ("", False),
        (None, False),
        (123, False),
    ],
)
def test_is_valid_url(url, expected):
    assert is_valid_url(url) == expected


# Parameterized tests for is_valid_filename
@pytest.mark.parametrize(
    "filename, expected",
    [
        ("", False),
        ("video.mp4", True),
        ("invalid<name.mp4", False),
        ("image.jpg", False),
        ("my.video.file.mp3", True),
        # more cases can be added here
    ],
)
def test_is_valid_filename(filename, expected):
    assert is_valid_filename(filename) == expected


# Parameterized tests for start_download
@pytest.mark.parametrize(
    "output_path, output_name, links, path_exists, expected_result",
    [
        ("/valid/path", "valid_name.mp4", ["http://www.example.com"], True, True),
        ("/invalid/path", "valid_name.mp4", ["http://www.example.com"], False, False),
        ("/valid/path", "invalid<name.mp4", ["http://www.example.com"], True, False),
        ("/valid/path", "valid_name.mp4", [], True, False),
        ("/valid/path", "valid_name.mp4", ["invalid_url"], True, False),
    ],
)
def test_start_download(output_path, output_name, links, path_exists, expected_result):
    with patch("gui.path_entry.get", return_value=output_path), patch(
        "gui.name_entry.get", return_value=output_name
    ), patch("gui.listbox.get", return_value=links), patch(
        "gui.os.path.exists", return_value=path_exists
    ), patch(
        "gui.threading.Thread"
    ) as mock_thread, patch(
        "gui.listbox.itemconfig"
    ) as mock_itemconfig, patch(
        "gui.path_entry.config"
    ) as mock_path_config, patch(
        "gui.name_entry.config"
    ) as mock_name_config, patch(
        "gui.status_label.config"
    ) as mock_status_label_config:
        start_download()

        if expected_result:
            mock_thread.assert_called()
        else:
            mock_thread.assert_not_called()


@pytest.fixture
def mock_youtube_dl():
    with patch("gui.youtube_dl.YoutubeDL") as mock_ydl:
        yield mock_ydl


# Parameterized tests for start_download
@pytest.mark.parametrize(
    "index, link, output_path, output_name, num_links, parts, filename, ydl_opts, expected_result",
    [
        (
            "1",
            "https://www.youtube.com/watch?v=G-tRyR1kJNc",
            "C:/Users/talha/Downloads/",
            "test_file_MARVELS",
            1,
            ["test_file_MARVELS", "mp4"],
            "test_file_MARVELS_0.mp4",
            {
                "format": "best",
                "outtmpl": "C:/Users/talha/Downloads/test_file_MARVELS_0.mp4",
            },
            False,
        ),
    ],
)
def test_download_link(
    index, link, output_path, output_name, num_links, parts, filename, ydl_opts
):
    # Mocking os.path.join
    with patch(
        "gui.os.path.join",
        return_value="C:/Users/talha/Downloads/test_file_MARVELS.mp4",
    ):
        download_link(
            index, link, output_path, output_name, num_links
        )  # , mock_status_label)

    # Check if youtube_dl.YoutubeDL is called with the correct options
    mock_youtube_dl.assert_called_with(
        {"format": "best", "outtmpl": "C:/Users/talha/Downloads/test_file_MARVELS.mp4"}
    )
    mock_youtube_dl.return_value.download.assert_called_with(
        ["https://www.youtube.com/watch?v=G-tRyR1kJNc"]
    )
