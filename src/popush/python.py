import os
import tokenize
from . import ignore_msg

def my_messages(fn, catalog):
    msgs = {}
    for msg in catalog:
        for o in msg.occurrences:
            if fn == o[0]:
                msgs.setdefault(msg.msgid, []).append((int(o[1]), msg.msgstr))
    return msgs


def replace(fn, tokens):
    tmpfn = fn + '~'
    with open(tmpfn, 'wb') as output:
        output.write(tokenize.untokenize(tokens))
    os.rename(tmpfn, fn)


def semi_safe_eval(s):
    return eval(s, {'__builtins__':{}}, {})


def rewrite_python(fn, catalog, indent_only):
    msgs = my_messages(fn, catalog)
    output = []
    changed = True
    with open(fn, 'rb') as input:
        pending = []
        for token in tokenize.tokenize(input.readline):
            if indent_only or token.type == tokenize.STRING:
                pending.append(token)
            else:
                if pending:
                    msgid = ''.join(semi_safe_eval(t.string) for t in pending)
                    for (lineno, msgstr) in msgs.get(msgid, []):
                        if pending[0].start[0] - 2 <= lineno <= pending[-1].end[0] + 2:
                            changed = True
                            output.append((tokenize.STRING, 'u' + repr(msgstr)) + pending[0][2:])
                            break
                    else:
                        output.extend(pending)
                    pending = []
                output.append(token)
        # Any string bits remaining here can not be i18n messages, since those
        # always appear inside a function call, and thus must be followed by
        # a ')' operator token.
        output.extend(pending)

    if indent_only or changed:
        replace(fn, output)
