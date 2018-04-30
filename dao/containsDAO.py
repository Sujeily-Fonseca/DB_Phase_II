#contains table: containsID, msgID, hashtagID

import psycopg2

class HashtagInMessageDAO:
    def __init__(self):
        self.conn = psycopg2.connect(database='postgres', user='liss',
                                     password='LiSSMsgApp', host='35.193.157.126')

    def getAllHashtags(self):
        cursor = self.conn.cursor()
        query = "SELECT hashtagID, hashString FROM hashtags;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getHashIn(self, msgID):
        cursor = self.conn.cursor()
        query = "SELECT hashString FROM hashtags NATURAL INNER JOIN contains WHERE msgID=%s;"
        cursor.execute(query, (msgID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getMsgsWith(self, hashtagID):
        cursor = self.conn.cursor()
        query = "SELECT message FROM messages NATURAL INNER JOIN contains WHERE hashtagID=%s;"
        cursor.execute(query, (hashtagID,))
        result = []
        for row in cursor:
            result.append(row)
        return result
