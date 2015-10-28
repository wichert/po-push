import click
import polib
from . import ignore_msg
from .pt import rewrite_pt


@click.command()
@click.argument('po-file', type=click.Path(exists=True))
@click.option('--indent-only', is_flag=True)
def main(po_file, indent_only):
    """Merge translations into source files.
    """
    catalog = polib.pofile(po_file)

    files = set()
    for msg in catalog:
        if ignore_msg(msg):
            continue
        for oc in msg.occurrences:
            files.add(oc[0])

    for fn in files:
        if fn.endswith('.pt'):
            modified = rewrite_pt(fn, catalog, indent_only)
