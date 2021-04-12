import json
import codecs
import random
import os, sys

from PIL import Image

import numpy as np

def char_to_unicode(char):
    text = char.encode('unicode-escape')
    ucode = text.decode("utf-8")
    return ucode

def char_to_json(ucode_list, path):
    json_list = [codecs.decode(ucode, 'unicode-escape') for ucode in ucode_list]
    json_entry = {"CN":json_list} # First entry is just a placeholder
    print(json_entry)
    with open(path, 'w') as json_file:
        json.dump(json_entry, json_file)
    return json_entry

def read_json(path):
    with open(path, 'r') as json_file:
        text = json.load(json_file)
        print(text['CN'][1])
    return 

def random_color():
    r1 = random.randint(0, 255)
    r2 = random.randint(0, 200)
    r3 = random.randint(0, 200)
    return (r1, r2, r3)

def change_color(image, random_colors):
    image = image.convert("RGBA")
    im_data = np.array(image)
    red, green, blue, alpha = im_data.T
    max_val = 200
    black = (red < max_val) & (blue < max_val) & (green < max_val)
    im_data[..., :-1][black.T] = random_colors
    image = Image.fromarray(im_data)
    return image


if __name__ == "__main__":
    ucode = char_to_unicode("我我")
    print(str(ucode))
    char_to_json(ucode, "charset/cjk.json")
    read_json("charset/cjk.json")
