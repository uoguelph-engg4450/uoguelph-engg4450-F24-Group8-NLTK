import os
import unittest.mock

from nltk import download


def test_downloader_using_existing_parent_download_dir(tmp_path):
    """Test that download works properly when the parent folder of the download_dir exists"""

    download_dir = str(tmp_path.joinpath("another_dir"))
    download_status = download("mwa_ppdb", download_dir)
    assert download_status is True


def test_downloader_using_non_existing_parent_download_dir(tmp_path):
    """Test that download works properly when the parent folder of the download_dir does not exist"""

    download_dir = str(
        tmp_path.joinpath("non-existing-parent-folder", "another-non-existing-folder")
    )
    download_status = download("mwa_ppdb", download_dir)
    assert download_status is True


def test_downloader_redownload(tmp_path):
    """Test that a second download correctly triggers the 'already up-to-date' message"""

    download_dir = str(tmp_path.joinpath("test_repeat_download"))
    for i in range(0, 2):
        # capsys doesn't capture functools.partial stdout, which nltk.download.show uses, so just mock print
        with unittest.mock.patch("builtins.print") as print_mock:
            download_status = download("stopwords", download_dir)
            assert download_status is True
            if i == 0:
                expected_second_call = unittest.mock.call(
                    "[nltk_data]   Unzipping %s."
                    % os.path.join("corpora", "stopwords.zip")
                )
                assert print_mock.call_args_list[1].args == expected_second_call.args
            elif i == 1:
                expected_second_call = unittest.mock.call(
                    "[nltk_data]   Package stopwords is already up-to-date!"
                )
                assert print_mock.call_args_list[1].args == expected_second_call.args
