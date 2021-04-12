#!/usr/bin/env python3.7

# Author: Phillip Lakaschus

import sys, os
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
from anki.hooks import addHook
import json
from anki.storage import Collection
#import subprocess

ADDON_HOME = os.path.dirname(os.path.abspath(__file__))
PROFILE_HOME = os.path.dirname(os.path.dirname(ADDON_HOME))
JSON_FILE_LOC = os.path.join(ADDON_HOME,'config.json')

sys.path.append(ADDON_HOME)

import styleRandomizer

with open(JSON_FILE_LOC, 'r') as json_file:
    json_data = json.load(json_file)

user = json_data["user"]
decks = json_data["decks"]
field_numbers = json_data["field_no"]
interpolation_bool = int(json_data["interpolate"])
random_color_bool = int(json_data["random_color"])
ai_generated_bool = int(json_data["AI_generated"])
non_ai_generated_bool = int(json_data["non_AI_generated"])
full_deck_bool = int(json_data["full_deck"])
options = [interpolation_bool, random_color_bool, ai_generated_bool, non_ai_generated_bool, full_deck_bool]

GAN_OUTPUT_PATH = os.path.join(ADDON_HOME,'zi2ziGAN', 'output_dir')
GAN_HANZI_PATH = os.path.join(ADDON_HOME,'zi2ziGAN', 'hanzi_dir')
MEDIA_SRC = os.path.join(PROFILE_HOME, user, 'collection.media')
JSON_DIR = os.path.join(ADDON_HOME, 'zi2ziGAN','charset','cjk.json')
GAN_DIR = os.path.join(ADDON_HOME, 'zi2ziGAN')
FNAME_END = "gan_generated.png"
FONT_DIR = os.path.join(ADDON_HOME, 'fonts')
_, _, fonts = next(os.walk(FONT_DIR ))
PATHS = [GAN_DIR, GAN_HANZI_PATH, GAN_OUTPUT_PATH, JSON_DIR, FONT_DIR, MEDIA_SRC]

cpath = os.path.join(PROFILE_HOME, user,"collection.anki2")
col = Collection(cpath, log=True) # Entry point to the API

for d in range(len(decks)):
    field_no = int(field_numbers[d])
    print(field_no)
    did = col.decks.id(decks[d])
    col.decks.select(did)
    styleRandomizer.main(col, field_no, fonts, decks[d], PATHS, options)