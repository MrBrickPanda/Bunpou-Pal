import sqlite3
import codecs
import re
from timeit import default_timer as timer
from Project_Files_Asher_Perkins.jpstemmer import stemming

class Search:
    def __init__(self):
        # The Key of each item in tags is the name for a table in the jmd database. The value is a more human-readable 
        # word relating to the key
        self.tags = {'Misc': 'Miscellaneous', 'Xref': 'Similar Word', 'Gloss': 'Meaning', 'Pos': 'Parts of Speech', 'Field': 'Field', 'S_inf': 'Special Info', 'Dial': 'Dialect'}
        self.keb = False
        self.rebs = ''
        # Connections to the dictionary database
        self.conn = sqlite3.connect('jmd3.db')
        self.c = self.conn.cursor()

    def getSense(self, word):
        wordParts = []
        tags = ['sense_id', 'xref', 'Meaning', 'Parts of Speech', 'miscellaneous', 'field', 's_inf', 'Dialect']
        if re.search(u'[\u4e00-\u9fff]', word):
            self.c.execute(f"SELECT ent_seq FROM Kanji_element WHERE keb = '{word}'")
        else:
            self.c.execute(f"SELECT ent_seq FROM Reading_element WHERE reb = '{word}'")
        result = self.c.fetchone()
        if result != None:
            self.c.execute(f"SELECT sense_id FROM Sense WHERE ent_seq = '{result[0]}'")
            for i in self.c.fetchall():
                self.c.execute(f"SELECT * FROM Info WHERE sense_id = {i[0]}")
                for i in self.c.fetchall():
                    wordStuff = []
                    num = 0
                    for x in i:
                        # 食べる
                        wordD = tags[num] +': ' + str(x)
                        if wordD[-6:] != ': None':
                            if 'sense_id' not in wordD:
                                wordStuff.append(wordD)
                        num += 1
                    wordStuff[-1] = wordStuff[-1].rstrip(",")+'. '
                    wordParts.append(wordStuff)
# 事
        return wordParts
        self.conn.commit()
        self.c.close()
        self.conn.close()

    def getEnglish(self, word):
        wordParts = []
        tags = ['sense_id', 'xref', 'Meaning', 'Parts of Speech', 'miscellaneous', 'field', 's_inf', 'Dialect']
        self.c.execute(f"SELECT * FROM Info WHERE gloss LIKE '% {word}%'")
        for i in self.c.fetchall():
            wordStuff = []
            num = 0
            for x in i:
                wordD = tags[num] +': ' + str(x)
                if wordD[-6:] != ': None':
                    if 'sense_id' in wordD:
                        self.c.execute(f"SELECT ent_seq FROM Sense WHERE Sense.sense_id = {wordD[10:]}")
                        ent_seq = self.c.fetchone()
                        self.c.execute(f"SELECT reb FROM Reading_element WHERE Reading_element.ent_seq = {ent_seq[0]}")
                        hira = self.c.fetchone()
                        self.c.execute(f"SELECT keb FROM Kanji_element WHERE Kanji_element.ent_seq = {ent_seq[0]}")
                        kanji = self.c.fetchone()
                        wordStuff.append(hira)
                        wordStuff.append(kanji)
                    else:
                        wordStuff.append(wordD)
                num += 1
            wordStuff[-1] = wordStuff[-1].rstrip(",")+'. '
            wordParts.append(wordStuff)
        return wordParts       
        self.conn.commit()
        self.c.close()
        self.conn.close()

# Returns all relevent information of a word.
def wordResults(word):
    finder = Search()
    if re.search(u'[\u0041-\u007a]', word):
        return finder.getEnglish(word)
    else:
        wData = finder.getSense(word)
        if wData == []:
            wData = finder.getSense(stemming(word))
        return wData

def getKanji():
    rads = []
    conn = sqlite3.connect('rads.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Strokes")
    results = c.fetchall()
    for i in results:
        rads.append(i)
    conn.commit()
    c.close()
    conn.close()
    return rads

def getRads(kanji):
    radSet = set()
    conn = sqlite3.connect('rads.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM {kanji}")
    for i in c.fetchall():
        for x in i[1]:
            radSet.add(x)
    return radSet
