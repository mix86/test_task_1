# coding: utf-8
import re
from itertools import groupby
from operator import itemgetter

text = open("CHANGELOG", "rb").read().decode("utf-8")

contributions = []

for line in text.split(u"\n"):
  version_re = r"^thepackage \(([\d\S-]+)\).+$"
  author_re = r"^\s\s\s\[(.+)\]$"
  if not line:
    continue

  m = re.match(version_re, line)
  if m:
    version = m.groups()[0]
    continue

  m = re.match(author_re, line)
  if m:
    author = m.groups()[0]
    continue

  contributions.append((author, line))

keyfunc = itemgetter(0)

for author, items in groupby(sorted(contributions, key=keyfunc), keyfunc):
  print u" [{}]".format(author)
  print u"\n".join(map(itemgetter(1), items))
