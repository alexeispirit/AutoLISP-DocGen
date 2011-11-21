## automatic AutoLISP documentation generator
##
## ;;; <LISPDOC>
## ;;; <SUBR>subroutine-name</SUBR>
## ;;; <ARG>argument1 </ARG>
## ;;; <ARG>argument2 </ARG>
## ;;; ...
## ;;; <RET>return \
## ;;; value
## ;;; </RET>
## ;;; <DESC>description of \
## ;;;  prograrm
## ;;;;</DESC>
## ;;; </LISPDOC>

import sys
import re

# Parent class for documentation
class Docs:
    # Prepare string to tag regexp
    def make_tag_regexp(self, tag):
        return "<" + tag + ">(.+?)</" + tag + ">"

    # Get tag entry from string    
    def get_tag_entry(self, str, tag):
        return re.findall(self.make_tag_regexp(tag), str)

    # Remove garbage from string ("\n" and ";")    
    def string_remove_garbage(self, str):
        newstr = str.replace("\n","").replace(";","")
        newstr = re.sub('\s{2,}', ' ', newstr)
        newstr = newstr.strip()
        return self.string_break(newstr)

    def string_break(self, str):
        return str.replace("\\", "<br/>")

# Lispfile reader
class LispDoc(Docs):
    # Class constructor
    def __init__(self, filename):
        self.lspfile = filename
        try:
            lsp = open(self.lspfile, 'r')
            self.lsp = self.string_remove_garbage("".join(lsp.readlines()))
            lsp.close()
        except IOError:
            print "There's no file found"

    def docstrings(self):
        return self.get_tag_entry(self.lsp,"LISPDOC")

# DocStrings class
class DocStrings(Docs):
    def __init__(self, str):
        self.docstring = str
        self.subr = self.get_tag_entry(self.docstring, "SUBR")
        self.args = self.get_tag_entry(self.docstring, "ARG")
        self.desc = self.get_tag_entry(self.docstring, "DESC")
        self.ret = self.get_tag_entry(self.docstring, "RET")

# HTML Generator class
class HTMLDoc:
    def __init__(self,filename):
        self.lspname = filename
        self.htmlfile = self.lspname.replace("lsp","html")
        try:
            self.html = open(self.htmlfile, 'w')
        except IOError:
            print "Cannot open file"

    def header(self):
        self.html.write("""
            <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
            <html>
            <head>
            <title>{0}</title>
            <style type='text/css'>
            body {{font-family: Arial, Helvetica; font-size: 10pt; padding-left: 10pt}}
            h1 {{font-size: 14pt; font-weight: bold; padding-left: 50pt}}
            h2 {{font-size: 10pt; font-weight: bold; padding-left: 15pt; background-color: #CCCC99}}
            .arg {{font-weight: bold; margin-left: 20pt}}
	    .ret {{font-weight: bold; margin-left: -5pt}}
            .text {{margin-left: 25pt}}
            div {{width: 500px}}
            </style>
            </head>
            <body>
            <div>
            <h1>{0}</h1>""".format(self.lspname))

    def subroutine(self,str):
        self.html.write("""
            <h2>{0}</h2>""".format(str))

    def description(self,str):
        self.html.write("""
            <p class=text>{0}</p>""".format(str))

    def arg(self, str):
        strings = str.split(" - ")
        if len(strings) > 1:
            return """
                <span class=arg>{0}</span><br/>
                <span class=text>{1}</span><br/>""".format(strings[0],strings[1])
        else:
            return """<span class=arg>No arguments</span><br/>"""

    def arg_list(self, strlist):
        for arg in strlist:
            self.html.write(self.arg(arg))

    def ret(self, str):
        self.html.write("""
            <p class=text><span class=ret>returns:</span><br/>
	    {0}</p>""".format(str))

    def footer(self):
        self.html.write("""
            </div>
            </body>
            </html>""")

# Main script
lsd = LispDoc(sys.argv[1])
html = HTMLDoc(sys.argv[1])
html.header()

for doc in lsd.docstrings():
    docstrings = DocStrings(doc)
    html.subroutine(docstrings.subr[0])
    if docstrings.desc:
        html.description(docstrings.desc[0])
    else:
        html.desc("No description")
    if docstrings.args:
        html.arg_list(docstrings.args)
    else:
        html.arg_list(["No arguments"])
    if docstrings.ret:
	html.ret(docstrings.ret[0])
    html.footer
