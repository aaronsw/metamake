Welcome to metamake, a weblog system based on make. This probably isn't 
usable by anyone but extreme geeks, but here it is if you're interested.

## Install

    cd /path/to/weblog
    git clone git@github.com:aaronsw/metamake.git code

## Configure

* singlepage.tmpl is the template for the entry page
* conf/indexes lets you list index templates (RSS, index.html, etc.), e.g.:
      rss.tmpl rss.xml
      index.tmpl index.html

Templates are standard Cheetah templates with variables file (filename),
title, body (converted using Markdown), and date (creation date). The 
multi-entry templates have these inside a list named entries.

## Post

    $ cat > _postname.txt
    # The Truth About Purple
    
    Through copious research I have discovered that purple is not really a color.
    Call Dan Rather!
    
    ^D
    $ echo postname >> list
    $ make

The first time the Makefile won't exist yet, so you'll have to run:

    python code/metamake.py > Makefile

-- 
Aaron Swartz: http://www.aaronsw.com/  
email: me@aaronsw.com
