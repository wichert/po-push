def ignore_msg(msg):
    return 'fuzzy' in msg.flags or \
        msg.msgstr == msg.msgid or \
        not msg.msgstr
