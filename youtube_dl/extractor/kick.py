from __future__ import unicode_literals

import re

from .common import InfoExtractor

class KickIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?kick\.com/(?P<path>[^/]+/video/(?P<id>[0-9a-z-]+))'

    def _real_extract(self, url):
        path, video_id = re.match(self._VALID_URL, url).groups()
        info = self._extract_info('https://kick.com/api/v1/video/%s' % path, video_id)
        info['id'] = video_id
        
        return info