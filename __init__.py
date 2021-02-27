# Author: Phillip Lakaschus

import sys, os
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
from anki.hooks import addHook
import json

from anki.storage import Collection # OK

with open('config.json', 'r') as json_file:
    json_data = json.load(json_file)

PROFILE_HOME = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(PROFILE_HOME)
print(json_data["user"])