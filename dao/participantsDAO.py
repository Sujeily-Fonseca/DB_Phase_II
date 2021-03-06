#participants table: participantID, groupID, userID
from dao.groupDAO import GroupDAO
from dao.contactDAO import ContactDAO
from dao.userDAO import UserDAO
import psycopg2

class ParticipantsDAO:

    def __init__(self):
        self.conn = psycopg2.connect(database='postgres', user='liss',
                                     password='LiSSMsgApp', host='35.193.157.126')

    def getAllParticipants(self):
        cursor = self.conn.cursor()
        query = "SELECT fName, lName, groupName FROM users NATURAL INNER JOIN participants NATURAL INNER JOIN groups;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getParticipantsForGroup(self, groupID):
        cursor = self.conn.cursor()
        query = "SELECT userName FROM users NATURAL INNER JOIN participants where groupId=%s;"
        cursor.execute(query,(groupID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUsersIdOnGroup(self, groupID):
        cursor = self.conn.cursor()
        query = "SELECT userID FROM participants WHERE groupID=%s;"
        cursor.execute(query, (groupID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllUsersOnGroup(self, groupID):
        cursor = self.conn.cursor()
        query = "SELECT userID, fname, lname FROM users NATURAL INNER JOIN participants WHERE groupID=%s;"
        cursor.execute(query, (groupID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllGroupsForUser(self, userID):
        cursor = self.conn.cursor()
        query = "SELECT groupID, groupName FROM groups NATURAL INNER JOIN participants WHERE userID=%s;"
        cursor.execute(query, (userID,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insertUserToGroup(self, userName, groupID, ownerID):
        gdao = GroupDAO()
        cdao = ContactDAO()
        udao = UserDAO()
        userID = udao.getUserIdByUserName(userName)
        result = []
        if int(ownerID) in (gdao.getOwnerId(groupID)) and cdao.isContact(userID, ownerID) and \
                not userID in (self.getAllUsersIdOnGroup(groupID)):
            cursor =self.conn.cursor()
            query = "INSERT INTO Participants(groupid,userid) values(%s,%s) returning userid;"
            cursor.execute(query,(groupID,userID,))
            result.append(cursor.fetchone())
            self.conn.commit()
        return result