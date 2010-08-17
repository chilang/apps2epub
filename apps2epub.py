#!/usr/bin/python

import re
import os
import sys

from zipfile import ZipFile

BOOK = re.compile(r'Payload/[^\.]+\.[^/]+/book/(.+)')
APPS_DIR = '~/Music/iTunes/Mobile Applications'

def scan(appsdir=APPS_DIR, write=False, target=os.curdir):
  
  """Scan iTunes apps directory for o'reilly (stanza-based) ebook app"""
  abs_dir = os.path.expanduser(appsdir)
  print "Scanning for ebook apps under directory: %s" % abs_dir
  for app in os.listdir(abs_dir):
    app_file = os.path.join(abs_dir, app)
    if app_file.endswith('.ipa') and is_ebook_app(app_file):
      print "Found '%s'" % app
      if write:
        extract(app_file, target)

def is_ebook_app(app):
  """Detect if an app contains ebook"""
  z = ZipFile(app, 'r')
  for name in z.namelist():
    if BOOK.match(name):
      return True
  return False
  
def extract(ipafile, target):
  """Create an EPUB content from an O'reilly ebooks app IPA file"""
  
  parent, filename = os.path.split(os.path.realpath(ipafile))
  epub = os.path.join(target, '%s.epub' % filename[:filename.rfind('.')])
  
  z = ZipFile(ipafile)
  print "Creating %s " % epub
  t = ZipFile(epub, 'w')
  
  for e in z.namelist():
    m = BOOK.match(e)
    if m:
      name = m.group(1)
      if not os.path.isdir(name):
        t.writestr(name, z.read(e))

  t.close()



if __name__ == "__main__":
  for arg in sys.argv:
    print arg
  if len(sys.argv) == 2:
    target = os.path.realpath(sys.argv[1])
    print "Target dir: %s" % target
    scan(write=True, target=target)
  else:
    scan()
    
  