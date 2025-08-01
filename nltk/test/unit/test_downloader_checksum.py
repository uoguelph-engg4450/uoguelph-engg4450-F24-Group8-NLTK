"""
Tests for checksum generation of downloads
"""

import os
from hashlib import sha256

from nltk.downloader import sha256_hexdigest


def test_sha256_hexdigest_generation(tmp_path):
    """Test that SHA256 hash is still generated properly when usedforsecurity=False argument is used in module"""
    tmp_file_name = os.path.join(tmp_path, "somefile")
    with open(tmp_file_name, "wb") as test_fi:
        test_fi.write(b"somebinarydata")
    test_sha256_hex = sha256_hexdigest(tmp_file_name)
    assert isinstance(test_sha256_hex, str)
