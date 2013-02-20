from lispdoc import *
import os
import sys

basedir = sys.argv[1]

for root, dirs, files in os.walk(basedir):
    for name in files:
	print name
        fname, fext = os.path.splitext(name)
        if 'lsp' in fext:
            doc = MarkdownDoc(os.path.join(root,name))
            doc.generate()
