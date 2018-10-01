import sqlite3
import codecs
import re
from Project_Files_Asher_Perkins.jpstemmer import stemming

class Search:
    def __init__(self):
        # The Key of each item in tags is the name for a table in the jmd database. The value is a more human-readable 
        # word relating to the key
        self.tags = {'Misc': 'Miscellaneous', 'Xref': 'Similar Word', 'Gloss': 'Meaning', 'Pos': 'Parts of Speech', 'Field': 'Field', 'S_inf': 'Special Info', 'Dial': 'Dialect'}
        self.wordParts = []
        self.keb = False
        self.rebs = ''
        # Connections to the dictionary database
        self.conn = sqlite3.connect('jmd.db')
        self.c = self.conn.cursor()

    # Function for initially finding if a word exists in the JMdict database.
    def findWord(self, word):
        # Japanese words can be spelled with both Hiragana and Kanji scripts. To accommodate for both, the JMdict database 
        # is searched differently if a Kanji character is included in the word. 
        if re.search(u'[\u4e00-\u9fff]', word):
            self.keb = True
            # If a word match is found, the various 'sense' primary keys associated with the word are returned.
            # The sense keys relate to an intermediary table, which leads to tables containing information on the
            # searched word.
            self.c.execute(f"SELECT sense_id FROM Kanji_element CROSS JOIN Sense WHERE keb = '{word}' AND Kanji_element.ent_seq = Sense.ent_seq")
            senses = self.c.fetchall()
            # Returns the Hiragana reading(s) for the Kanji characters
            self.c.execute(f"SELECT reb FROM Reading_element CROSS JOIN Kanji_element WHERE keb = '{word}' AND Reading_element.ent_seq = Kanji_element.ent_seq")
            self.rebs = self.c.fetchall()
        else:
            # Same as above, but for words that only have Hiragana characters.
            self.c.execute(f"SELECT sense_id FROM Reading_element CROSS JOIN Sense WHERE reb = '{word}' AND Reading_element.ent_seq = Sense.ent_seq")
            senses = self.c.fetchall()
        # If the searches did not find anything, the senses list will not be updated with anything and 'False' wil be 
        # Returned. If the searches did find a match, the 'senses' list will be returned.
        if senses != []:
            return senses
        else:
            return False
    # Returns all of the information associated with the word. As gathering a word's information has some overhead and 
    # searching if the word exists in JMdict is almost instantaneous, I split this into two functions for when I need 
    # to find a word quick.
    def getSense(self, word):
        getResult = self.findWord(word)
        # To accomodate for JMdict's lack of support for conjugations, the search function is run up to two times; 
        # if a match is not found on the first search, the stemming algorithm is applied to the word and is searched again.
        goAgain = True
        if not getResult:
            getResult = self.findWord(stemming(word))
            if not getResult:
                goAgain = False
        if goAgain:
            # Every table specified in the tags dictionary is searched for the data it contains for each sense key 
            # returned by getResult. If a table does not have data for a sense, it returns as null
            # If a table is sucsessful in returning data, it is added as a value to the tag_results dictionary with the
            # appropriate table name as the key. After all relevent data is added to tag_results, tag_results is added to
            # the wordParts list.
            for sense in getResult:
                tag_results = {}
                for tag in self.tags:
                    if sense[0] != None:
                        self.c.execute(f"SELECT {tag.lower()} FROM {tag} WHERE sense_id = '{sense[0]}'")
                        for result in self.c.fetchall():
                            if result != None:
                                for item in result:
                                    if tag not in tag_results:
                                        tag_results[tag] = [item]
                                    else:
                                        tag_results[tag].append(item)
                self.wordParts.append(tag_results)
        else:
            self.wordParts = False

        # If a word contains Kanji, this adds the word's Hiragana reading to wordParts.
        if self.keb:
            if type(self.wordParts) != bool:
                self.wordParts.append('Hiragana:' + self.rebs[0][0])
        return self.wordParts
        self.conn.commit()
        self.c.close()
        self.conn.close()

# Function to see if a word exists in the JMdict database.
def isWord(word):
    findW = Search()
    return findW.findWord(word)

# Returns all relevent information of a word.
def wordResults(word):
    finder = Search()
    return finder.getSense(word)
