# coding: utf-8
import re
from itertools import groupby
from operator import itemgetter

import requests

URL = "https://raw.githubusercontent.com/mix86/test_task_1/master/CHANGELOG"
VERSIONS = [
  u"0.10-0",
  u"0.9-4",
  u"0.9-3",
  u"0.9-2",
]
VERSION_RE = r"^thepackage \(([\d\S-]+)\).+$"
AUTHOR_RE = r"^\s\s\s\[(.+)\]$"

contributions = []

def get():
  resp = requests.get(URL)
  if not resp.ok:
    raise RuntimeError("Github says {}".format(resp.status_code))
  return resp.text

def process(text):
  skip = True
  for line in text.split(u"\n"):

    if not line:
      continue

    m = re.match(VERSION_RE, line)
    if m:
      version = m.groups()[0]
      if version in VERSIONS:
        skip = False
      else:
        skip = True
      continue

    if not skip:
      m = re.match(AUTHOR_RE, line)
      if m:
        author = m.groups()[0]
        continue

      if not (author, line) in contributions:
        contributions.append((author, line))

  return contributions

def pprint(contributions):
  keyfunc = itemgetter(0)

  for author, items in groupby(sorted(contributions, key=keyfunc), keyfunc):
    print u" [{}]".format(author)
    print u"\n".join(sorted(map(itemgetter(1), items)))

pprint(process(get()))
