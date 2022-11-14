# -*- coding: utf-8 -*-

import os
try:
    secret = os.environ['secret']
except:
    secret = "305e8bc2f3bd56bd8a02fae8caf6d56021c35a6049d51946"  # default key
