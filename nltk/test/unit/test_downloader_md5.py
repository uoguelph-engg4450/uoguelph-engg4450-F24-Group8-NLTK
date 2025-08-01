"""
Tests for md5 checksum generation
"""

import os
from hashlib import md5

from nltk.downloader import md5_hexdigest


def test_md5_hexdigest_generation(tmp_path):
    """Test that MD5 hash is still generated properly when usedforsecurity=False argument is used in module"""
    tmp_file_name = os.path.join(tmp_path, "somefile")
    with open(tmp_file_name, "wb") as test_fi:
        test_fi.write(b"somebinarydata")
    test_md5_hex = md5_hexdigest(tmp_file_name)
    assert isinstance(test_md5_hex, str)
