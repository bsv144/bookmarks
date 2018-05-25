'''
Script convert bookmarks from places.sqlite to html file with Netscape bookmarks format

v. 0.1
e-mail: bsv_144@mail.ru
'''

import sqlite3

DB_PATH = 'D:\Tmp\places_.sqlite'
OUTPUT_FILE = 'd:\TMP\bookmarks.html'

'''
SQL_TMP = """ select moz_bookmarks.id, moz_bookmarks.type, moz_bookmarks.parent, 
             moz_bookmarks.title, moz_places.url, moz_bookmarks.dateAdded
             from moz_bookmarks left join moz_places where (moz_bookmarks.fk = moz_places.id) and
             (moz_bookmarks.parent=? and (moz_bookmarks.type=1 or moz_bookmarks.type=2))
             """
'''
SQL_ROOT = "SELECT id, type, parent, title, fk, dateAdded FROM moz_bookmarks WHERE parent=? and (type=1 or type=2)"

SQL_NODE = """ select moz_bookmarks.title, moz_places.url, moz_bookmarks.dateAdded
             from moz_bookmarks left join moz_places where (moz_bookmarks.fk = moz_places.id) and
             (moz_bookmarks.parent = ? and moz_bookmarks.fk = ? and moz_bookmarks.type = 1)
             """

HEADER  = '''<!DOCTYPE NETSCAPE-Bookmark-file-1>
<Title>Bookmarks</Title>
<H1>Bookmarks</H1>'''

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

def DFS(id=1, level=1):
    t = (id,)
    c.execute(SQL_ROOT, t)
    f =  c.fetchall()
    for node in  f:
        if node[1] == 1:
            #print(node)
            #print(id)
            n = (id, node[4])
            #print(n)
            c.execute(SQL_NODE, n)
            fn = c.fetchone()
            #print(fn)
            lbm = level + 2
            print(' ' * lbm, end=" ")
            print('<DT> <A HREF = "%s" ADD_DATE = "%s"> %s </A>' % (fn[1], fn[2], fn[0]))
            #print(node[3])
        elif node[1] == 2:
            print(' ' * level, end=" ")
            print('<DT><H3 FOLDED  ADD_DATE = "%s" > %s </H3>' % (node[5], node[3]))
            print(' ' * level, end=" ")
            print('<DL><p>')
            #print(node[3])
            DFS(node[0], level+1)
    #Понижаем уровень для </DL><p>
    lc = level - 1
    print(' ' * lc, end=" ")
    print('</DL><p>')
    level += 1

#Выводим в файл
#with open(OUTPUT_FILE, 'w') as f:
print(HEADER)
print('<DL>')
DFS()
print('</DL>')

#conn.close()
