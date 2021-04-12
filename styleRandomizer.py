import sys, os
#from aqt import mw
#from aqt.utils import showInfo
#from aqt.qt import *
import random
import re
import time
import subprocess
from shutil import copyfile
import glob
import shutil
import codecs
import importlib.util

from PIL import Image
from anki.storage import Collection

import functions

font_list = [1,2,3,4,5,6,7,8,9,11,12,13,14,17,18,19,21,22,23,24,25,26,27]
good_fonts = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 22, 26]

def get_all_cards(col):
    did = col.decks.id(DECK_NAME)
    cards = []
    counter = 0
    
    for cid in col.findCards('deck:'+str(DECK_NAME)):
        cards.append(col.getCard(cid))
    return cards 

def get_cards(col, n = 20):
    global flag
    cards = []
    counter = 0
    
    while True:
        card = col.sched.getCard()
        if card == None:
            print("No more scheduled cards found!") 
            flag = False
            break
        if counter > n:
            break
        cards.append(card)
        counter += 1
    return cards 

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

def save_to_db(char_arr, no_chars, r_str, interp_bool):
    # Clear all files in Hanzi dir
    clear_folders()
    subprocess.call(["python", "-W", "ignore", "run.py", "--font_ids", r_str, \
                        "--sample_count", str(no_chars), "--interpolate", str(interp_bool)], cwd=GAN_DIR)
    
    for char in char_arr:
        random_colors = functions.random_color()
        chars, ids = char
        full_char = ""
        images = []
        for i in range(len(chars)):
            ch = chars[i]
            char_no = str(ids[i]).zfill(4)
            full_char += ch
            image = Image.open(GAN_OUTPUT_PATH+"/inferred_"+char_no +".png")
            if rand_color_b == 1:
                image = functions.change_color(image, random_colors)
            images.append(image)
        if len(chars) >= 2:
            img = get_concat_h(images[0], images[1])
            for im in images[2:]:
                img = get_concat_h(img, im)
        else: img = images[0]
        DB_PATH = os.path.join(MEDIA_SRC, full_char+"_"+DECK_NAME+"_"+"gan_generated.png")
        print(DB_PATH)
        img.save(DB_PATH)

def save_to_db_noGAN(char_arr, no_chars, font_str):
    clear_folders()
    subp = subprocess.call(["python", "font2img.py", "--src_font=SIMSUN.ttf", "--dst_font="+FONT_DIR+"/"+font_str, "--charset=CN",\
                    "--sample_count", str(no_chars), "--sample_dir=hanzi_dir", "--label=0", "--filter=0 ",\
                    "--shuffle=0"], cwd=GAN_DIR)
    #raise Exception("subprocess...")

    for char in char_arr:
        random_colors = functions.random_color()
        chars, ids = char
        full_char = ""
        images = []
        for i in range(len(chars)):
            ch = chars[i]
            char_no = str(ids[i]).zfill(4)
            full_char += ch
            image = Image.open(os.path.join(GAN_HANZI_PATH,"0_"+char_no +".jpg"))
            # crop second image half
            width, height = image.size 
            image = image.crop((0, 0, width//2, height))
            if rand_color_b == 1:
                image = functions.change_color(image, random_colors)
            images.append(image)
        if len(chars) >= 2:
            img = get_concat_h(images[0], images[1])
            for im in images[2:]:
                img = get_concat_h(img, im)
        else: img = images[0]
        DB_PATH = os.path.join(MEDIA_SRC, full_char+"_"+DECK_NAME+"_"+"gan_generated.png")
        img.save(DB_PATH)

def clear_folders():
    files = glob.glob(GAN_DIR+'/hanzi_dir/*')
    for f in files:
        os.remove(f)

    files = glob.glob(GAN_DIR+'/output_dir/*')
    for f in files:
        os.remove(f)

def randomize_deck_noGAN(field_no):
    cards_sorted = get_all_cards(col)
    char_arr = get_characters(col, cards_sorted, field_no)
    ucode_arr = chars_to_json(char_arr)
    no_chars = len(ucode_arr)
    print("no_chars: ", no_chars)
    font_str = str(random.choice(fonts))
    save_to_db_noGAN(char_arr, no_chars, font_str)

    clear_folders()

def randomize_next_cards(n, interp_bool, field_no):
    cards_sorted = get_cards(col, n)
    char_arr = get_characters(col, cards_sorted, field_no)
    ucode_arr = chars_to_json(char_arr)
    if interp_bool == 1: r_str = str(random.choice(font_list))+","+str(random.choice(font_list))+","+str(random.choice(font_list))
    else: r_str = str(random.choice(font_list))
    print("font id: ", r_str)
    no_chars = len(ucode_arr)
    print("no_chars: ", no_chars)
    save_to_db(char_arr, no_chars, r_str, interp_bool)
    clear_folders()

def randomize_next_cards_noGAN(n, field_no):
    cards_sorted = get_cards(col, n)
    char_arr = get_characters(col, cards_sorted, field_no)
    ucode_arr = chars_to_json(char_arr)
    no_chars = len(ucode_arr)
    print("no_chars: ", no_chars)
    font_str = str(random.choice(fonts))
    save_to_db_noGAN(char_arr, no_chars, font_str)

    clear_folders()

def main(collection, field_no, font_list, deck_name, paths, options):
    global flag, col, fonts, GAN_DIR, GAN_HANZI_PATH, GAN_OUTPUT_PATH, JSON_DIR, \
           FONT_DIR, MEDIA_SRC, DECK_NAME, rand_color_b
    GAN_DIR, GAN_HANZI_PATH, GAN_OUTPUT_PATH, JSON_DIR, FONT_DIR, MEDIA_SRC = paths
    DECK_NAME = deck_name
    print(f"################\nDeck: {DECK_NAME}\n################")
    fonts = font_list
    col = collection
    flag = True # True: Scheduled cards available; False: No scheduled cards available
    n = 5
    tot_n = 0
    interp_b, rand_color_b, ai_b, non_ai_b, full_deck_b = options
    if full_deck_b == 1: 
        print("Characters for the entire deck are generated! Will take some time...")
        randomize_deck_noGAN(field_no)
    while flag:
        if flag and ai_b == 1:
            randomize_next_cards(n, interp_b, field_no)
            tot_n += n
        if flag and non_ai_b == 1:
            randomize_next_cards_noGAN(n, field_no)
            tot_n += n
    print("total style transfers: ", tot_n)
   