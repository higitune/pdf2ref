import urllib.request
import urllib.parse
import sys
import os
import re
from bs4 import BeautifulSoup
from http.cookiejar import MozillaCookieJar
from urllib.request import HTTPCookieProcessor, Request, build_opener
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

def pdf2ref(inputpath,outputpath):
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
          r = (author,title,conf)
          RefList.append(r)
          tmp = ""
        tmp += line.rstrip().translate(mpa)
  return RefList
  #for i in RefList:
  #  print(i)

def search_scholar(title):
  requrl="http://scholar.google.co.jp/scholar?q="
  USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'
  requrl+=urllib.parse.quote_plus(title.strip())
  print(requrl)
#  with urllib.request.urlopen(requrl) as response:
#    print(response.read())
  try:
    req = Request(url=requrl, headers={'User-Agent': USER_AGENT})
    hdl = build_opener(HTTPCookieProcessor(MozillaCookieJar())).open(req)
    html = hdl.read()
    print(html[:50])
    soup = BeautifulSoup(html)
    soup0 = soup.find_all("div",class_="gs_r")[0]
    # pdf link
    # paper title
    soup_t = soup0.find("h3",class_="gs_rt")
    # paper author
    soup_ac = soup0.find("div",class_="gs_a")
    a_c_list = soup_ac.get_text().split("-",1)
    return (soup_t.find("a").get_text(),\
      a_c_list[0],\
      a_c_list[1],\
      soup0.find("a",class_=re.compile("yC[0-9]")).get('href'))

#    for div in soup.find_all("div",class_="gs_r"):
#      print(div)
  except Exception as err:
    print(err)
#    ScholarUtils.log('info', err_msg + ': %s' % err)

def main(inputpath,outputpath):
  reflist = pdf2ref(inputpath,outputpath)
  for i in reflist:
    article = search_scholar(i[1])
    print(article)

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print('Usage: ./pdf2text pdf_path outfile_path')
    sys.exit()
  inputpath = sys.argv[1]
  outputpath = sys.argv[2]
  main(inputpath,outputpath)
