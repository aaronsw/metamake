import time
def parse(fn, sep):
    x = []
    for line in open(fn):
        x.append(line.strip().split()[0])
    return sep.join(x) + sep

print "all: " + parse('conf/indexes', ' ') + parse('list', '.html ') + 'Makefile'
print '\tpython code/generator.py all'
print
donesofar = set()
for line in open('list'):
    line = line.strip()
    assert line not in donesofar
    donesofar.add(line)
    if ' ' in line:
        out, fn = line.split()
    else:
        fn = out = line
    print out+'.html: _'+fn+'.txt singlepage.tmpl'
    print '\tcp _%s.txt _%s.txt.bak.%s' % (fn, fn, time.time()) 
    print '\tpython code/generator.py '+fn + (' '+out if out != fn else '')
    print '\tsudo chgrp www-data '+out+'.html'
    print '\tchmod g+w '+out+'.html'
    print
print 'Makefile: list code/metamake.py conf/indexes'
print '\tpython code/metamake.py > Makefile'
print '\tmake'
print
