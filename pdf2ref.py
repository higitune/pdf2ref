import urllib.request
import sys
import os
import re
from collections import namedtuple

# おおまかにhttp://blog.mwsoft.jp/article/93796981.htmlを参照している

def rereplace(src):
  src = src.replace('\\','\\\\')
  src = src.replace('.','\.')
  src = src.replace('^','\^')
  src = src.replace('$','\$')
  src = src.replace('*','\*')
  src = src.replace('+','\+')
  src = src.replace('?','\?')
  src = src.replace('{','\{')
  src = src.replace('}','\}')
  src = src.replace('[','\[')
  src = src.replace(']','\]')
  src = src.replace('|','\|')
  src = src.replace('(','\(')
  src = src.replace(')','\)')
  
  return src


if len(sys.argv) < 3:
  print('Usage: ./pdf2text pdf_path outfile_path')
  sys.exit()

inputpath = sys.argv[1]
outputpath = sys.argv[2]
tmp_pdfpath = 'tmppdf.pdf'

# download pdf file if path is url
if re.match('^https?\:\/\/', inputpath):
  with urllib.request.urlopen(inputpath) as response, open(tmp_pdfpath,'wb') as output:
    output.write(response.read())
  inputpath = tmp_pdfpath

# convert pdf to text
status = os.system('pdftotext {0} {1}'.format(inputpath, inputpath + '.txt'))
if status != 0:
  print('Error: pdftotext return illegal status code ${0}'.format())
  sys.exit()

# remove pdf if download file
if os.path.exists(tmp_pdfpath):
  os.remove(tmp_pdfpath)

# remove ctrl char settings
# see http://stackoverflow.com/questions/4324790/removing-control-characters-from-a-string-in-python
mpa = dict.fromkeys(range(32))
RefTuple = namedtuple('RefTuple', 'author title conf')
RefList = []
# fix line break, remove ctrl char
flag = flagref= False
tmp = ""
with open(inputpath + '.txt') as input, open(outputpath, 'wt') as output:
  for line in input:
    if line.strip() == "":
      continue
    if flagref:
      m = re.search('[10]',line.strip()) 
      if m != None:
        flag = True
        prefix = rereplace(line.strip()[:m.start()])
        refnum = 2
      else:
        flagref = False
    if re.search('[Rr](EFERENCE)|(eference)',line.strip()) != None:
      flagref = True
    if flag:
      # Author
      if re.search('^'+prefix+str(refnum),line.strip()) != None:
        refnum += 1
        m = re.search('^.*?and.*?[a-zAZ]{2,}?\.',tmp)
        if m != None:
          author = m.group()
        else:
          m = re.search('^.*?[a-zAZ]{2,}?\.',tmp)
          author = m.group()
        tmp = tmp[m.end():]
      # Conf
        m = re.search('In .*?$',tmp)
        if m!= None:
          conf = m.group()
          title = tmp[:m.start()]
        else:
          m = re.search('Proc.*?$',tmp)
          if m!= None:
            conf = m.group()
            title = tmp[:m.start()]
          else:
            m = re.search('\..*?$',tmp)
            conf = m.group()[2::]
            title = tmp[:m.start()+1]
        r = RefTuple(author,title,conf)
        RefList.append(r)
        tmp = ""
      tmp += line.rstrip().translate(mpa)
for i in RefList:
  print(i)

