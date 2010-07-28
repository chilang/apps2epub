BOOK = re.compile(r'Payload/[^\.]+\.[^/]+/book/(.+)')

def extract(ipafile, todir):
  """Extract EPUB content from an application IPA file"""
  import os
  
  if not os.path.isdir(todir):
    os.mkdir(todir)
  os.chdir(todir)
  for d in ['META-INF', 'mimetype', 'OEBPS']:
    if not os.path.isdir(d):
      os.mkdir(d)
  
  from zipfile import ZipFile
  import re

  z = ZipFile(ipafile)
  for e in z.namelist():
    m = BOOK.match(e)
    if m:
      name = os.path.join(todir, m.group(1))
      if not os.path.isdir(name):
        open(name, 'w').write(z.read(e))
  
  parent = os.path.join(todir, os.pardir)
  epub = '%s.epub' % ipafile[:ipafile.rfind('.')]
  print "Creating %s " % epub
  t = ZipFile(os.path.join(parent, epub), 'w')
  
  for d in os.listdir(os.curdir):
    for e in os.listdir(d):
      name = os.path.join(d, e)
      item = os.path.join(os.path.realpath(os.curdir), name)
      #print "Processing %s" % item
      if os.path.isfile(item):
        print "Adding file %s as %s" % (item, name)
        t.write(item, name)
  
  t.close()
  
  os.chdir(os.path.join(os.curdir, os.pardir))
  


  