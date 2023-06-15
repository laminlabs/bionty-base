from pathlib import Path

from bionty.dev._io import url_download


def test_url_download():
    url = "https://bionty-assets.s3.amazonaws.com/bfxpipelines.json"
    localpath = Path(f"./{url.split('/')[-1]}")
    assert not localpath.exists()

    localpath_default = url_download(url=url)
    assert Path(localpath_default) == localpath
    assert localpath.exists()
