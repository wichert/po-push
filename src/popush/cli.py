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
@click.option('-p', '--strip', type=int, default=0)
def main(po_file, sources, indent_only, sources_from_po, strip):
    """Merge translations into source files.
    """
    catalog = polib.pofile(po_file)

    files = set(sources)
    if sources_from_po or not sources:
        for msg in catalog:
            if ignore_msg(msg):
                continue
            for oc in msg.occurrences:
                path = oc[0]
                if strip:
                    path = os.path.sep.join(path.split(os.path.sep)[strip:])
                files.add(path)

    warned = set()
    with click.progressbar(files, label='Updating files') as bar:
        for fn in bar:
            if not os.path.exists(fn):
                click.echo('Can not find file %s' % fn, err=True)
                continue
            ext = os.path.splitext(fn)[1]
            rewriter = REWRITERS.get(ext)
            if rewriter:
                rewriter(fn, catalog, indent_only, strip)
            elif ext not in warned:
                click.echo('Do not know how to update %s files' % ext, err=True)
                warned.add(ext)
