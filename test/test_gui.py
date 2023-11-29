import unittest
import pytest

import sys
sys.path.append('..')
from gui import is_valid_filename, is_valid_url, add_link, remove_link, start_download



# Parameterized tests for is_valid_url
@pytest.mark.parametrize("url, expected", [
    ("http://www.example.com", True),
    ("https://www.example.com", True),
    ("ftp://www.example.com", True),
    ("www.example.com", False),
    ("", False),
    (None, False),
    (123, False)
])
def test_is_valid_url(url, expected):
    assert is_valid_url(url) == expected

# Parameterized tests for is_valid_filename
@pytest.mark.parametrize("filename, expected", [
    ("", False),
    ("video.mp4", True),
    ("invalid<name.mp4", False),
    ("image.jpg", False),
    ("my.video.file.mp3", True),
    # more cases can be added here
])
def test_is_valid_filename(filename, expected):
    assert is_valid_filename(filename) == expected

# Integration test example
def test_download_workflow():
    # Assuming your application has these functions
    valid_url = "https://www.youtube.com/watch?v=v6HBZC9pZHQ&ab_channel=BabyKeemVEVO"
    invalid_url = "just_some_string"
    valid_filename = "video.mp4"
    invalid_filename = "<invalid>.mp4"

    # Test with valid inputs
    # Here, replace 'add_link' and 'start_download' with the actual functions from your GUI application
    # and adjust the assertions according to their expected behavior.
    assert add_link(valid_url, valid_filename) == True
    assert start_download() == True

    # Test with invalid URL
    assert add_link(invalid_url, valid_filename) == False

    # Test with invalid filename
    assert add_link(valid_url, invalid_filename) == False

    # More comprehensive tests can be added to simulate different scenarios
        

if __name__ == "__main__":
    unittest.main()




