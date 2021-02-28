#!/usr/bin/env python3.7

# Author: Phillip Lakaschus

import sys, os
import subprocess
ADDON_HOME = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ADDON_HOME)

#subprocess.call([os.path.join(ADDON_HOME, 'packages', 'python-3.7.9-h60c2a47_0', 'python.exe')\
#                , "main.py"], cwd=ADDON_HOME)

import main