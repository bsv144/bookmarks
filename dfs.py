'''
Script convert bookmarks from places.sqlite to html file with Netscape bookmarks format

v. 0.1
e-mail: bsv_144@mail.ru
'''

import sqlite3

DB_PATH = 'D:\places.sqlite'


conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

def DFS(id=1, level=1):
    t = (id,)
    c.execute("SELECT id,type,parent,title FROM moz_bookmarks WHERE parent=? and (type=1 or type=2)", t)
    f =  c.fetchall()
    for node in  f:
        if node[1] == 1:
            lbm = level + 2
            print(' ' * lbm, end=" ")
            print(node[3])
        elif node[1] == 2:
            print('->' * level, end=" ")
            print('<DT><H3 FOLDED  ADD_DATE = "{date}" > %s </H3>' % node[3])
            print('->' * level, end=" ")
            print('<DL><p>')
            #print(node[3])
            DFS(node[0], level+1)
    print('->' * level, end=" ")
    print('</DL><p>')
    level += 1

header ='''<!DOCTYPE NETSCAPE-Bookmark-file-1>
    <Title>Bookmarks</Title>
    <H1>Bookmarks</H1>
'''

print(header)
print('<DL>')
DFS()
print('</DL>')


