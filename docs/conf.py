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
html_sidebars = {
    "*": ["sidebar-nav-bs"],
    "**/*": ["sidebar-nav-bs"],
}

nb_execution_mode = "force"
