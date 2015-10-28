Sometimes you have an application which has a lot of text that is not as great
as it should be. It might have been written by non-native speakers, or use a
different tone of voice, or you need to do some quick rephrasing. In such
situations a standard trick is to add a translation from your source language
*to the same source language* and put your corrections in the translation.

This works very well, but may lead to problems later on: for example when translating to new
languages it is convenient to have updated text as the canonical text (although
some tools such as Weblate can handle this and show your same-language
translation as canonical text). At that point you can find yourself wanting
to replace the text in your Python code and HTML templates with the new text.
``po-push`` is a tool to do exactly that. It does three things:

1. It can update all texts in Python files
2. It can update all texts in HTML templates (if they use the ZPT syntax).
3. It can update other PO files so their translations are still found

Using ``po-push`` is simple: just point it to a po-file. It will look for all
sources mentioned in the file and try to process those:

.. code-block:: shell

   $ po-push src/myapp/locales/en/LC_MESSAGES/mydomain.po

If you have other translations po-push will not find those automatically, since
they are not mentioned in the po file. To handle this you can also specify files
to update manually:

.. code-block:: shell

   $ po-push src/myapp/locales/en/LC_MESSAGES/mydomain.po \
        src/myapp/locales/*/LC)MESSAGES/mydomain.po

Or you can use both all mentioned sources in the po file and specify a few extra
files by hand:

.. code-block:: shell

   $ po-push --sources-from-po \
        src/myapp/locales/en/LC_MESSAGES/mydomain.po \
        src/myapp/locales/*/LC)MESSAGES/mydomain.po

When updating HTML templates po-push can also make some other changes, such
as closing empty elements. These changes are harmless, but they will make your
diff harder to verify. To help with this you can run po-push in *indent-only*
mode: this will make it rewrite any files that will be modified, but does not
actually change any text. After you have commited those changes you can run
po-push in normal mode and get a diff with only text changes.

.. code-block:: shell

   $ po-push --indent-only src/myapp/locales/en/LC_MESSAGES/mydomain.po
   $ git add src
   $ git commit -m 'Prepare for text changes'
   $ po-push src/myapp/locales/en/LC_MESSAGES/mydomain.po
   $ git diff
