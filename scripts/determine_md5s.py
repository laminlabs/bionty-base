import tempfile

from rich import print

from bionty.dev._handle_sources import parse_sources_yaml
from bionty.dev._io import url_download
from bionty.dev._md5 import calculate_md5

df = parse_sources_yaml()

for index, row in df.iterrows():
    url = row["url"]
    md5 = row["md5"]
    if not md5:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            tmp_file_path = temp_file.name
            if not url.startswith("s3"):
                url_download(url, tmp_file_path)
                md5 = calculate_md5(tmp_file_path)
                print(f"[bold blue]URL: [green]{url} [blue]has md5: [green]{md5}")
            elif url.startswith("s3"):
                pass
                # s3_bionty_assets
            else:
                raise ValueError(f"URL type for: {url} not recognized")
