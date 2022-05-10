import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path[:0] = [str(HERE)]
from lamin_sphinx import *  # noqa
import bionty  # noqa

for generated in HERE.glob("bionty.*.rst"):
    generated.unlink()

project = "Bionty"
html_title = f"{nbproject} | Lamin Labs"
release = nbproject.__version__
html_context["github_repo"] = "nbproject"  # noqa
html_sidebars = {
    "*": [],
    "guides": ["sidebar-nav-bs"],
    "guides/*": ["sidebar-nav-bs"],
}
