import unittest
from youtube_dl.downloader.common import FileDownloader
from youtube_dl import YoutubeDL

class TestFileDownloader(unittest.TestCase):

    def test_download_speed(self):
        info = {
            'status': 'finished',
            'total_bytes': 1024,
            'elapsed': 2
        }
        params = {'simulate': True, }
        ydl = FileDownloader(YoutubeDL(),params)
        ydl.report_progress(info)
        expected_speed = info['total_bytes'] / info['elapsed']
        self.assertIn('speed', info)
        self.assertEqual(info['speed'], expected_speed)

if __name__ == '__main__':
    unittest.main()
