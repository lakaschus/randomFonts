import json
import codecs

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

if __name__ == "__main__":
    ucode = char_to_unicode("我我")
    print(str(ucode))
    char_to_json(ucode, "charset/cjk.json")
    read_json("charset/cjk.json")
