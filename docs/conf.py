import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path[:0] = [str(HERE)]
from lamin_sphinx import *  # noqa
import bionty  # noqa

project = "Bionty"
html_title = f"{project} | Lamin Labs"
release = bionty.__version__
html_context["github_repo"] = "bionty"  # noqa

nb_execution_mode = "force"

ogp_site_url = "https://lamin.ai/bionty"
