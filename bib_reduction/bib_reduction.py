# author: Matteo Bianchetti
# date: November 26 2022
# python3 version: 3.10.0
# description: 
# (1) take a tex file and a bib file
# (2) from the bib file, remove all the entries that the tex file does not use.

import os
import re

# read tex file
with open(os.path.join("input", "main.tex")) as texFile:
    texLines:list = texFile.readlines()

# remove lines that are commented out in the tex file
texLines_noComments:list = [line for line in texLines if not line.startswith("%")]

# retain only lines with a \cite{} command
texLines_cite:list = [line for line in texLines_noComments if "cite{" in line]

# extract exactly all citations
citations:list = []
for line in texLines_cite:
    while "cite{" in line:
        citation:str = re.findall(".*cite{(.*?)}.*", line)[0]
        citations.append(citation)
        line:str = line.replace(f"cite{{{citation}}}", "")

# read the bib file
with open(os.path.join("input", "mybibliography.bib")) as bibFile:
    bibLines:list = bibFile.readlines()

# remove lines that are commented out in the tex file
bibLines_noComments:list = [line for line in bibLines if not line.startswith("%")]

# add two empty items at the end to protect the code below
bibLines_noComments.append("")
bibLines_noComments.append("")

# create list of entries
entries:list = []
for index, line in enumerate(bibLines_noComments):
    if line.startswith("@"):
        entrylines:list = [line]
        k = 1
        while ( not ( bibLines_noComments[index+k].startswith("@") or bibLines_noComments[index+k].strip()=="")
             and k<len(bibLines_noComments) ) :
            entrylines.append(bibLines_noComments[index+k])
            k += 1
        entry:str = "".join(entrylines)
        entries.append(entry)

# retain only entries with a \cite{} command
usedEntries:list = [f"{entry}\n" for entry in entries if re.findall(".*{(.*?),", entry)[0] in citations]

with open(os.path.join("output", "restrictedBibliography.bib"), "w") as restrictedBibliography:
    restrictedBibliography.writelines(usedEntries)