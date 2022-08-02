from io import BytesIO, StringIO
import sys
import os
import subprocess
from typing import TextIO
import venv
import shutil
if __name__ =="__main__":
    from pathlib import Path
    
    root_dir = Path(__file__).parent.parent
    os.chdir(root_dir)
    stdout = TextIO()
    venv_dir = root_dir.joinpath(".venv")
    site_package_dir = venv_dir.joinpath("Lib").joinpath("site-packages")
    print(site_package_dir)
    shutil.rmtree(site_package_dir)
    