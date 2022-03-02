from aqt import mw
from aqt.qt import QAction
from aqt.utils import showInfo
from anki.notes import Note
from anki.hooks import addHook
import re
from .config import getUserOption
import os

def addBackNote(line, wrongMids, presentNids):
    elements=line.split("\t")
    #print(f"Considering line «{elements}»")
    nid = elements[0]
    #print(f"nid is {nid}")
    mid = elements[1]
    if mw.col.db.list("""select id from notes where id = ?""", nid):
        print(f"Note {nid} was already present")
        presentNids.add(nid)
        return "nid present"
    #print(f"mid is {mid}")
    fields = elements[2:]
    model = mw.col.models.get(mid)
    if model is None:
        wrongMids.add(mid)
        return "no mid"
    nbFieldEntry = len(fields)
    nbFieldModel = len(model["flds"])
    if nbFieldModel < nbFieldEntry:
        end = fields[nbFieldModel-1:]
        last_field = "EXTRAFIELD".join(end)
        fields = fields[:nbFieldModel-1]
        fields.append(last_field)
    elif nbFieldModel > nbFieldEntry:
        fields += [""]*(nbFieldModel - nbFieldEntry)
    note = Note(mw.col, model)
    note.id = nid
    note.fields = fields
    note.addTag("NoteBackFromDeleted")
    nbCard = mw.col.addNote(note)
    if nbCard == 0:
        note.addTag("NoteWithNoCard")
        note.flush()
        template0 = model["tmpls"][0]
        mw.col._newCard(note,template0,mw.col.nextID("pos"))
        return "no card"
    return True

def testLine(line):
      return re.search(r"^\d{6,}\t\d{6,}\t", line) is not None

def addBack():
    lines = []
    message = []
    wrongMids = set()
    presentNids = set()
    firstLine = True
    deletedPath = os.path.join(mw.col.path.replace("collection.anki2", ""), getUserOption("file","r"))
    with open(deletedPath, encoding = "UTF-8") as f:
        for line in f:
            if testLine(line):
                lines.append(line)
            else:
                if not (firstLine and line == "nid\tmid\tfields"):
                    lines[-1]+="\n"+line
            firstLine = False
    print(f"We must consider {len(lines)} lines")
    cnt = 1
    imp = 0
    noCard = 0
    for line in lines:
        ret = addBackNote(line, wrongMids, presentNids)
        if ret is True or ret == "no card":
              imp+=1
        if ret == "no card":
            noCard+=1
        cnt += 1
        if (cnt % 100)==0:
            print(f"Saving the {cnt} first elements")
    if wrongMids:
        message .append( f"The wrong mids are {wrongMids}")
    if presentNids:
        message .append( f"Already contains note with nids {presentNids}")
    if imp:
        message .append( f"Succesfully imported back {imp} notes")
    else:
        message .append( f"No note imported")
    if noCard:
        message .append( f"{noCard} notes have generated 0 card. We added card 1 to them, and the tag NoteWithNoCard. You should edit them quickly, or «empty cards» will make them disappear.")
    showInfo("\n".join(message))


action = QAction(mw)
action.setText("add back")
mw.form.menuTools.addAction(action)
action.triggered.connect(addBack)
