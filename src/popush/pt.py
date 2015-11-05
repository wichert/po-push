import itertools
import os
import re
import bs4
import click
from . import ignore_msg


I18N_FILTER = {'i18n:translate': True}
STR_RX = r'\${[^}]+}'

try:
    zip_longest = itertools.zip_longest
except AttributeError:  # For Python 2
    zip_longest = itertools.izip_longest

def find_domain_and_context(tag):
    domain = context = None
    for p in itertools.chain([tag], tag.parents):
        if not domain:
            domain = p.attrs.get('i18n:domain')
        if not context:
            context = p.attrs.get('i18n:context')
        if domain and context:
            break
    return (domain, context)


def get_message(tag):
    msgstr = []
    for el in tag.children:
        if isinstance(el, bs4.NavigableString):
            msgstr.append(unicode(el))
        elif isinstance(el, bs4.Tag):
            msgstr.append(u'${%s}' % el.attrs.get('i18n:name', 'dynamic'))
    msgstr = ''.join(msgstr)
    msgid = tag.attrs['i18n:translate'] or msgstr
    (domain, msgctxt) = find_domain_and_context(tag)
    return (domain, msgctxt, msgid, msgstr)


def replace_message(tag, msg, fn):
    texts = re.split(STR_RX, msg.msgstr)
    variables = re.findall(STR_RX, msg.msgstr)
    msg_parts = itertools.chain(*zip_longest(variables, texts, fillvalue=''))

    dynamic_children = {}
    for el in tag.children:
        if isinstance(el, bs4.Tag):
            dynamic_children[el.attrs.get('i18n:name', 'dynamic')] = el

    tag.clear()
    for part in msg_parts:
        if part:
            if re.match(STR_RX, part):
                try:
                    child_name = part[2:-1]
                    if child_name is 'dynamic' and 'dynamic' not in dynamic_children:
                        child_name = ''
                    tag.append(dynamic_children[child_name])
                except KeyError:
                    click.echo('%s: translation references non-existing %s' % (fn, part), err=True)
                    tag.append(bs4.NavigableString(part))
            else:
                tag.append(bs4.NavigableString(part))


def replace(fn, soup):
    tmpfn = fn + '~'
    with open(tmpfn, 'w') as output:
        output.write(str(soup))
    os.rename(tmpfn, fn)


def rewrite_pt(fn, catalog, indent_only, path_strip):
    soup = bs4.BeautifulSoup(open(fn), 'html5lib')
    changed = False
    for tag in soup.find_all(**I18N_FILTER):
        (domain, msgctxt, msgid, msgstr) = get_message(tag)
        new_msg = catalog.find(msgid, msgctxt=msgctxt)
        if new_msg is not None and not ignore_msg(new_msg):
            if not indent_only:
                replace_message(tag, new_msg, fn)
            changed = True
    if changed:
        replace(fn, soup)
