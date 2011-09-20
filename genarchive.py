for item in file('list'):
    item = item.strip()
    print '<li><a href="%s">%s</a></li>' % (item, open('_%s.txt' % item).readline()[2:].strip())