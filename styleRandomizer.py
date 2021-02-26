import sys, os
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
import random
import re
import time
import functions
import subprocess
from shutil import copyfile
import glob
import shutil
import codecs
from PIL import Image
import numpy

#sys.path.append("../anki")
from anki.storage import Collection # OK

User = "Benutzer 1"
PROFILE_HOME = "/Users/Phillip/AppData/Roaming/Anki2/"+User
GAN_OUTPUT_PATH = "/Users/Phillip/Google Drive/python/Projects/AnkiAddons/randomFonts/zi2zi/output_dir/"
GAN_HANZI_PATH = "/Users/Phillip/Google Drive/python/Projects/AnkiAddons/randomFonts/zi2zi/hanzi_dir/"
DECK_NAME = "HSK1to6+"  #"HSK1to6+" #"HSK1to6::deck""Radicals"
DECK = "deck:"+DECK_NAME 
MEDIA_SRC = "/Users/Phillip/AppData/Roaming/Anki2/"+User+"/collection.media"
MEDIA_SRC = "/Users/Phillip/Downloads/test"
DIRNAME = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(DIRNAME, 'zi2zi','charset','cjk.json')
GAN_DIR = os.path.join(DIRNAME, 'zi2zi')
FNAME_END = "gan_generated.png"
FIELD_NO = 0
FONT_DIR = DIRNAME+"/fonts"
_, _, fonts = next(os.walk(FONT_DIR ))
#print(fonts)

font_list = [1,2,3,4,5,6,7,8,9,11,12,13,14,17,18,19,21,22,23,24,25,26,27]
good_fonts = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 22, 26]
font_list = good_fonts
#average_fonts = [5, 10, 14, 19, 23, 24, 25, 28]
#bad_fonts = [15, 16, 17, 18, 20, 27]

template = "<img src='{{Front}}"+"_"+DECK_NAME+"_"+FNAME_END+"'>"

cpath = os.path.join(PROFILE_HOME, "collection.anki2")
col = Collection(cpath, log=True) # Entry point to the API
did = col.decks.id(DECK_NAME)
col.decks.select(did)
#deck = col.decks.byName(DECK_NAME)

def get_cards(col, n = 20):
    cards = []
    counter = 0
    
    while True:
        card = col.sched.getCard()
        if card == None or counter > n: break
        cards.append(card)
        counter += 1
        #cards.append(col.getCard(cid))
        #print(col.getCard(cid))
    return cards #sorted(cards, key=lambda k: k.due)

def get_characters(col, stack, field_no):
    char_ids = [] # format: [([id], [1,2]), (id, 3), (id, 4, 5, 6)] 
    counter = 0

    for card in stack:
        note = col.getNote(card.nid)
        char = note.fields[field_no]
        print(char)        
        char_list = list(char)
        no_chars = len(char)
        char_tpl = (char_list,[counter+n for n in range(len(char_list))])
        char_ids.append(char_tpl)
        counter += no_chars
    
    return char_ids

def chars_to_json(char_arr):
    char_list_flattened = [char for sublist in char_arr for char in sublist[0]]
    ucode_list = [functions.char_to_unicode(ch) for ch in char_list_flattened]
    print(ucode_list)
    functions.char_to_json(ucode_list, JSON_DIR)  
    
    return ucode_list

def get_concat_h(im1, im2):
    """ Credit: https://note.nkmk.me/en/python-pillow-concat-images/ """
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def save_to_db(char_arr, no_chars, r_str, interp_bool, gan_path, gan_output_path):
    # Clear all files in Hanzi dir
    files = glob.glob(GAN_DIR+'/hanzi_dir/*')
    for f in files:
        os.remove(f)
    subprocess.call(["python", "-W", "ignore", "run.py", "--font_ids", r_str, \
                        "--sample_count", str(no_chars), "--interpolate", str(interp_bool)], cwd=GAN_DIR)

    for char in char_arr:
        print(char)
        chars, ids = char
        full_char = ""
        images = []
        #get_concat_h(im1, im1)
        for i in range(len(chars)):
            ch = chars[i]
            char_no = str(ids[i]).zfill(4)
            full_char += ch
            images.append(Image.open(gan_output_path+"inferred_"+char_no +".png"))
        print(full_char)
        if len(chars) >= 2:
            img = get_concat_h(images[0], images[1])
            for im in images[2:]:
                img = get_concat_h(img, im)
        else: img = images[0]
        DB_PATH = MEDIA_SRC+"/"+full_char+"_"+DECK_NAME+"_"+FNAME_END
        print(DB_PATH)
        img.save(DB_PATH)

def save_to_db_noGAN(char_arr, no_chars, font_str, gan_path, gan_output_path):
    # Clear all files in Hanzi dir
    files = glob.glob(GAN_DIR+'/hanzi_dir/*')
    for f in files:
        os.remove(f)
    subprocess.call(["python", "font2img.py", "--src_font=SIMSUN.ttf", "--dst_font="+FONT_DIR+"/"+font_str, "--charset=CN",\
                        "--sample_count", str(no_chars), "--sample_dir=hanzi_dir", "--label=0", "--filter=0 ",\
                            "--shuffle=0"], cwd=GAN_DIR)

    for char in char_arr:
        print(char)
        chars, ids = char
        full_char = ""
        images = []
        #get_concat_h(im1, im1)
        for i in range(len(chars)):
            ch = chars[i]
            char_no = str(ids[i]).zfill(4)
            full_char += ch
            image = Image.open(gan_output_path+"0_"+char_no +".jpg")
            # crop second image half
            width, height = image.size 
            print(image.size)
            print(width)
            image = image.crop((0, 0, width//2, height))
            images.append(image)
        print(full_char)
        if len(chars) >= 2:
            img = get_concat_h(images[0], images[1])
            for im in images[2:]:
                img = get_concat_h(img, im)
        else: img = images[0]
        DB_PATH = MEDIA_SRC+"/"+full_char+"_"+DECK_NAME+"_"+FNAME_END
        print(DB_PATH)
        img.save(DB_PATH)

def randomize_deck():
    char_arr = get_characters(col, DECK, FIELD_NO)
    ucode_arr = chars_to_json(char_arr)
    r_str = "1,2,3,4,5,6,7,8,9,11,12,13,14,17,18,19,21,22,23,24,25,26,27"#str(random.choice(font_list))+","+str(random.choice(font_list))+","+str(random.choice(font_list))#
    no_chars = len(ucode_arr)
    print("no_chars: ", no_chars)
    save_to_db(char_arr, no_chars, r_str, GAN_DIR, GAN_OUTPUT_PATH)

    files = glob.glob(GAN_DIR+'/hanzi_dir/*')
    for f in files:
        os.remove(f)

    files = glob.glob(GAN_DIR+'/output_dir/*')
    for f in files:
        os.remove(f)

def randomize_next_cards(n, interp_bool):
    while True:
        cards_sorted = get_cards(col, n)
        char_arr = get_characters(col, cards_sorted, FIELD_NO)
        ucode_arr = chars_to_json(char_arr)
        if interp_bool == 1: r_str = str(random.choice(font_list))+","+str(random.choice(font_list))+","+str(random.choice(font_list))
        else: r_str = str(random.choice(font_list))
        print("font id: ", r_str)
        no_chars = len(ucode_arr)
        print("no_chars: ", no_chars)
        save_to_db(char_arr, no_chars, r_str, interp_bool, GAN_DIR, GAN_OUTPUT_PATH)

        files = glob.glob(GAN_DIR+'/hanzi_dir/*')
        for f in files:
            os.remove(f)

        files = glob.glob(GAN_DIR+'/output_dir/*')
        for f in files:
            os.remove(f)
        
        if not col.sched.getCard(): break

def randomize_next_cards_noGAN(n):
    while True:
        cards_sorted = get_cards(col, n)
        char_arr = get_characters(col, cards_sorted, FIELD_NO)
        ucode_arr = chars_to_json(char_arr)
        no_chars = len(ucode_arr)
        print("no_chars: ", no_chars)
        font_str = str(random.choice(fonts))
        input(font_str)
        save_to_db_noGAN(char_arr, no_chars, font_str, GAN_DIR, GAN_HANZI_PATH)

        files = glob.glob(GAN_DIR+'/hanzi_dir/*')
        for f in files:
            os.remove(f)

        files = glob.glob(GAN_DIR+'/output_dir/*')
        for f in files:
            os.remove(f)
        
        if not col.sched.getCard(): break

if __name__ == "__main__":
    #main()
    #randomize_next_cards(10, 1)
    randomize_next_cards_noGAN(100)
    #print(get_cards(col))
    #print(did)
    #print(col.sched.getCard())
   