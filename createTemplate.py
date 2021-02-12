import sys, os
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
import random
import re
from anki.storage import Collection # OK

DECK = "deck:HSK1to6::deck"

PROFILE_HOME = "/Users/Phillip/AppData/Roaming/Anki2/Benutzer 1"
cpath = os.path.join(PROFILE_HOME, "collection.anki2")
col = Collection(cpath, log=True) # Entry point to the API
#template = <img src="{{Front}}">

for cid in col.findCards(DECK):
    card = col.getCard(cid)
    note = col.getNote(card.nid)
    print(note.fields)
    fieldFrontName = col.models.get(note.mid)['flds'][0]['name']
    print("###############")
    frontTemplate = col.models.get(note.mid)['tmpls'][0]['qfmt']
    #print(frontTemplate)
    front = "{{"+fieldFrontName+"}}"
    col.models.get(note.mid)['tmpls'][0]['qfmt'] = front
    note.flush()
    #temp = card.template
    #print(temp)


col.save()