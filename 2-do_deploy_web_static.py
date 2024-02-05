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
    local(f"tar -czvf web_static_{datestr}.tar.gz web_static/")
