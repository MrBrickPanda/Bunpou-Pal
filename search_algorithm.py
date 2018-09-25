import sqlite3
import codecs
import re
from jpstemmer import stemming

class Search:
    def __init__(self):
        self.tags = {'Misc': 'Miscellaneous', 'Xref': 'Similar Word', 'Gloss': 'Meaning', 'Pos': 'Parts of Speech', 'Field': 'Field', 'S_inf': 'Special Info', 'Dial': 'Dialect'}
        self.word_parts = []
        self.keb = False
        self.rebs = ''
        self.conn = sqlite3.connect('betterjm2.db')
        self.c = self.conn.cursor()


    def findWord(self, word):
        if re.search(u'[\u4e00-\u9fff]', word):
            self.keb = True
            self.c.execute(f"SELECT sense_id FROM Kanji_element CROSS JOIN Sense WHERE keb = '{word}' AND Kanji_element.ent_seq = Sense.ent_seq")
            senses = self.c.fetchall()
            self.c.execute(f"SELECT reb FROM Reading_element CROSS JOIN Kanji_element WHERE keb = '{word}' AND Reading_element.ent_seq = Kanji_element.ent_seq")
            self.rebs = self.c.fetchall()
        else:
            self.c.execute(f"SELECT sense_id FROM Reading_element CROSS JOIN Sense WHERE reb = '{word}' AND Reading_element.ent_seq = Sense.ent_seq")
            senses = self.c.fetchall()
        if senses != []:
            return senses
        else:
            return False

    def getSense(self, word):
        getResult = self.findWord(word)
        goAgain = True
        if not getResult:
            getResult = self.findWord(stemming(word))
            if not getResult:
                goAgain = False
        if goAgain:
            for j in getResult:
                tag_results = {}
                for i in self.tags:
                    if j[0] != None:
                        self.c.execute(f"SELECT {i.lower()} FROM {i} WHERE sense_id = '{j[0]}'")
                        for k in self.c.fetchall():
                            if k != None:
                                for eh in k:
                                    if i not in tag_results:
                                        tag_results[i] = [eh]
                                    else:
                                        tag_results[i].append(eh)
                self.word_parts.append(tag_results)
        else:
            self.word_parts = False

        if self.keb:
            if type(self.word_parts) != bool:
                self.word_parts.append('Hiragana:' + self.rebs[0][0])
        return self.word_parts
        self.conn.commit()
        self.c.close()
        self.conn.close()

def isWord(word):
    findW = Search()
    return findW.findWord(word)

def wordResults(word):
    finder = Search()
    return finder.getSense(word)

# 食べる
