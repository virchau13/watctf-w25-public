import sqlite3, os
try:
    os.remove('haystack')
except:
    pass
con = sqlite3.connect('haystack')

words = {}

with open('AIW.txt', 'r') as f:
    for line in f:
        for word in line.split():
            if word in words:
                words[word] += 1
            else:
                words[word] = 1

con.execute("CREATE TABLE aiw_words (word, count)")
con.commit()
con.executemany("INSERT INTO aiw_words VALUES (?, ?)", words.items())
con.commit()
con.close()
