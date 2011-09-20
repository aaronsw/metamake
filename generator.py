from Cheetah.Template import Template
from markdown import markdown
import sanitize
import sys, os, datetime, re, cPickle as pickle

class Storage:
    def __init__(self, x=None): 
        if x: self.__dict__ = x

def striphtml(a): return re.sub('<.*?>', '', a)
def cleandate(d): return datetime.datetime.fromtimestamp(int(d)).date().strftime('%B %e, %Y')
def isodate(d): return datetime.datetime.fromtimestamp(int(d)).isoformat()
def file2dict(fn, comments=True, body=True):
    s = Storage()
    s.file = fn
    fh = open('_'+fn+'.txt')
    s.title = markdown(fh.readline()[2:].strip()).strip().replace('<p>', '').replace('</p>', '')
    fh.readline()
    if body:
        s.body = markdown(fh.read())
        s.shortbody = striphtml(s.body)[:150]
    if not os.path.exists('.'+fn+'.ctime'):
        open('.'+fn+'.ctime', 'w').write(str(os.stat('_'+fn+'.txt')[-1]))
    s.date = cleandate(open('.'+fn+'.ctime').read())
    s.isodate = isodate(open('.'+fn+'.ctime').read())
    if comments:
        s.comments = []; i = 1
        while os.path.exists('_'+fn+'.comments.'+str(i)+'.txt'):
            furl = '_'+fn+'.comments.'+str(i)+'.txt'
            if not open(furl).read(): i+=1; continue
            s.comments.append(Storage(pickle.load(open(furl))))
            if s.comments[-1].__dict__.get('moderate'):
                s.comments.pop(); i+=1; continue
            s.comments[-1].date = cleandate(s.comments[-1].date)
            s.comments[-1].id = i
            s.comments[-1].content = sanitize.HTML(markdown(s.comments[-1].content), addnofollow=True)
            i+=1
    return s

def handle(fn, out=None):
    if out is None: out = fn
    t = str(Template(open('singlepage.tmpl').read(), [file2dict(fn)]))
    open(out+'.html.tmp', 'w').write(t)
    os.rename(out+'.html.tmp', out+'.html')
    
if __name__ == "__main__":
    fn = sys.argv[1]
    if fn == "all":
        entries = []
        ents = open('list').readlines()
        ents.reverse()
        ents = ents[:12]
        for line in ents:
            entries.append(file2dict(line.strip().split()[-1], comments=False))
        for line in open('conf/indexes'):
            template, filename = line.split()
            open(filename, 'w').write(str(Template(open(template).read(), [{'entries':entries[:12]}])))
            print filename
        
        # fullarchive
        entries = []
        ents = open('list').readlines()
        ents.reverse()
        for line in ents:
            entries.append(file2dict(line.strip().split()[-1], comments=False, body=False))
        open('fullarchive.html', 'w').write(str(Template(open('fullarchive.tmpl').read(), [{'entries':entries}])))
        print "fullarchive.html"
    else:
        out = None
        if len(sys.argv) > 2: out = sys.argv[2]
        handle(fn, out)