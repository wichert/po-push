import os
import polib
from . import ignore_msg


def replace(fn, catalog):
    tmpfn = fn + '~'
    catalog.save(tmpfn)
    os.rename(tmpfn, fn)


def rewrite_po(fn, catalog, indent_only, path_strip):
    c = polib.pofile(fn)
    changed = False
    for msg in c:
        new_msg = catalog.find(msg.msgid, msgctxt=msg.msgctxt)
        if new_msg is not None and not ignore_msg(new_msg):
            if msg.comment.startswith('Defaut: '):
                # We would broke Zope-style message ids
                continue
            msg.msgid = new_msg.msgstr
            changed = True

    if indent_only or changed:
        replace(fn, c)
