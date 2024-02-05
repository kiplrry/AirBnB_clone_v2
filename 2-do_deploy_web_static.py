#!/usr/bin/python3
"""
fabric file to pack
"""

from fabric.api import *
from datetime import datetime


def do_pack():
    """gzips a file"""
    time = datetime.now()

    datestr = time.strftime("%Y%m%d%H%M%S")
    local("mkdir -p versions")
    local(f"tar -cz -v --totals -f \
          versions/web_static_{datestr}.tgz web_static/")
