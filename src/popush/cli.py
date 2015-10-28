import os
import click
import polib
from . import ignore_msg
from .po import rewrite_po
from .pt import rewrite_pt
from .python import rewrite_python


REWRITERS = {
    '.po': rewrite_po,
    '.pt': rewrite_pt,
    '.py': rewrite_python,
}


@click.command()
@click.argument('po-file', type=click.Path(exists=True))
@click.argument('sources', type=click.Path(exists=True), nargs=-1)
@click.option('--indent-only', is_flag=True)
@click.option('--sources-from-po', is_flag=True)
def main(po_file, sources, indent_only, sources_from_po):
    """Merge translations into source files.
    """
    catalog = polib.pofile(po_file)

    files = set(sources)
    if sources_from_po or not sources:
        for msg in catalog:
            if ignore_msg(msg):
                continue
            for oc in msg.occurrences:
                files.add(oc[0])

    warned = set()
    for fn in files:
        ext = os.path.splitext(fn)[1]
        rewriter = REWRITERS.get(ext)
        if rewriter:
            rewriter(fn, catalog, indent_only)
        elif ext not in warned:
            click.echo('Do not know how to update %s files' % ext, err=True)
            warned.add(ext)
