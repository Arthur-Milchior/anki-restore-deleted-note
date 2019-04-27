# Restore deleted notes
## Rationale
Sometime, you realize that you have missing notes. Personnally, I lost
5000 notes, and I took months to realize that there was this
error. Those notes can be found in the file deleted.txt in anki's
folder.

This add-on allow you to import again the notes from deleted.txt. More
precisely, you should first copy paste the lines corresponding to the
note you want to get back, into another file, and then import this
other file.

Note that it won't import card back. There is currently no way known
to me to do that. It means that all cards will be new. Note also that
those notes will have lost their tags.

This is really a bad add-on, and you should first try to figure out
whether you have the missing note in some backup somewhere. This is a
last recourse add-on.

To find the notes created by this add-on easily, it adds the tag
```NoteBackFromDeleted``` to cards imported.

The creation date of notes is kept (but not the creation date of card)

## Usage
First, use the add-on manager to edit the configuration of this
add-on. In front of "file", put the adress of the file you want to
import. By default, it's called deleted.txt and is assumed to be in
your home directory. But you'll probably have to change this, in
particular if you're not on a unix system (linux, mac os x, bsd)

Then in the main window, do "Tools>add back". You'll have a message
telling you how many notes were imported and whether there were notes
which were not imported.

## Warning
### Tab
deleted.txt is a very bag log. For example, it separates every fields
with tab (\t). But you can have tab in your field. Which means that it
is literally impossible for the add-on to know whether a tab separates
fields, or belong to a field. So as soon as a field will contains a
tab, the importation is going to be wrongly done and you'll have to
correct it by hand.

### Modified note type
If you have modified the note type after the deletion occured, and
before you use this add-on, then the import will give a wrong
result. Indeed, it will import what was the first field in what is
currently the first field, and similarly for every other field.

Luckily, however, you can correct this later by selecting all imported
card, and changing their note type, which allow you to move fields
from one position to another one.

### Note generating no card
Sometime, a note generate no card. When it occurs in the «add card»
window, you get a warning. Here, I force the generation of the first
card, and I add the tag "NoteWithNoCard". You then get a warning
telling you that you should find those note and edit them
quickly. Otherwise, those notes will be deleted as soon as you press
«Empty cards...»

### Note already present
Sometime a note is in deleted.tx, but in fact was not deleted. May be
you did cancel the deletion, or you imported the note again from
somewhere. Anyway, if a note from your file has the same id than a
card in your collection, then this card is not added, and an error
message is written.

This mean in particular that if you import twice the same file, you'll
still have a single copy.

### Missing note type
If you have deleted the note type, the note can't be
imported. Instead, you'll get an error message telling you the list of
id of note type (known as mid) which are missing.

It's hard to tell you what to do in this case, because it's quite
complicated. May be you should change the mid of those cards to the id
of note type which already exists. You'll have the data in anki, even
if it is in bad place. You'll have then to manually decide what to do
with those cards.

### Medias
Sorry, but deleted media are not saved anywhere. So if your card add
media, it won't be back.

## Technical details
A line is supposed to encode a note type if it starts by two numbers
with at least 6 digits, each numbere followed by a tab. Otherwise, it
is assumed that the line represents the end of the preceding line, and
that a field of the preceding line contained a new line symbol.

## Version 2.0
None



## Links, licence and credits

Key         |Value
------------|-------------------------------------------------------------------
Copyright   | Arthur Milchior <arthur@milchior.fr>
Based on    | Anki code by Damien Elmes <anki@ichi2.net>
License     | GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Source in   | https://github.com/Arthur-Milchior/anki-restore-deleted-note
Addon number| [912930620](https://ankiweb.net/shared/info/912930620)
