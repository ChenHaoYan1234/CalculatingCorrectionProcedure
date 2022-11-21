# -*- coding: utf-8 -*-
from enum import Enum
# Program info
author = "ChenHaoYan"
version = "1.2.6"
# Baidu AI keys
client_id = "MrM4zO5cStpSxD3TBi5qPzZt"
client_secret = "cFEAj5yCrxxck22fqAitegNYFDOnVCtV"
# Upgrade
update_url = "http://localhost:8080/"


class STATUS(Enum):
    """
    Status values:
    1.ok;
    2.error;
    3.cancel;
    """
    OK = 0
    ERROR = 1
    CANCEL = 2
    NOTFOUND = 3
