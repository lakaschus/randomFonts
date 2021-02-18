import sys, os
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
import random
import re
import functions
import subprocess
from shutil import copyfile
import glob
import shutil

#sys.path.append("../anki")
from anki.storage import Collection # OK

User = "Benutzer 1"
PROFILE_HOME = "/Users/Phillip/AppData/Roaming/Anki2/"+User
GAN_OUTPUT_PATH = "/Users/Phillip/Google Drive/python/Projects/AnkiAddons/randomFonts/zi2zi/output_dir/"
DECK_NAME = "HSK1to6+" #"HSK1to6::deck"
DECK = "deck:"+DECK_NAME 
MEDIA_SRC = "/Users/Phillip/AppData/Roaming/Anki2/"+User+"/collection.media"
DIRNAME = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(DIRNAME, 'zi2zi','charset','cjk.json')
GAN_DIR = os.path.join(DIRNAME, 'zi2zi')
FNAME_END = "gan_generated.png"

font_list = [1,2,3,4,5,6,7,8,9,11,12,13,14,17,18,19,21,22,23,24,25,26,27]

template = "<img src='{{Front}}"+"_"+DECK_NAME+"_"+FNAME_END+"'>"

cpath = os.path.join(PROFILE_HOME, "collection.anki2")
col = Collection(cpath, log=True) # Entry point to the API

for cid in col.findCards(DECK):
    card = col.getCard(cid)
    note = col.getNote(card.nid)
    #print(note)
    #input()
    char = note.fields[1]
    char_list = list(char)
    print(char_list)
    no_chars = len(char)
    print("no_chars", no_chars)
    ucode_list = [functions.char_to_unicode(ch) for ch in char_list]
    print(ucode_list)
    functions.char_to_json(ucode_list, JSON_DIR)
    
    r_str = str(random.choice(font_list))
    print("random font: ", r_str)
    subprocess.call(["python", "-W", "ignore", "run.py", "--font_ids", r_str, \
                    "--sample_count", str(no_chars)], cwd=GAN_DIR)
    copyfile(GAN_OUTPUT_PATH+"inferred_000"+str(no_chars)+".png", MEDIA_SRC+"/"+char+"_"+DECK_NAME+"_"+FNAME_END)
    # Clear all files in Hanzi dir
    files = glob.glob(GAN_DIR+'/hanzi_dir/*')
    for f in files:
        os.remove(f)
    print("###############")

    # TODO: ADD Image to field

#col.save()