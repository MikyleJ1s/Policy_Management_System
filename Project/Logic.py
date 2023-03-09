import pandas as pd
import mysql.connector
class DatabaseUser():
    def __init__(self,s_host,s_user,s_password,s_dbname):   #provides for individual db
        self.db = s_dbname
        self.host = s_host
        self.password = s_password
        self.user = s_user
    def isValidUser(self,password,username):  # this method will return whether a user is a valid user or not
        query = "SELECT * FROM policy_management_system.user_table;"   #selects all users
        starlink = mysql.connector.connect(host = self.host, user = self.user, password = self.password, database = self.db)
        passwords = []   #empty lists to store all users and their passwords
        usernames = []
        df = pd.read_sql(query,starlink) #stores results into a dataframe
        passwords = df.loc[:,"user_password"].to_list()   #fills the empty lists
        usernames = df.loc[:,"user_name"].to_list()

        #This nested if checks if we have a valid user
        if username in usernames: #if a user exists in our known user list then continue else return false. The logic behind this is that if a user doesnt exist in our registered list there's no need to even check their password
            if password == passwords[usernames.index(username)]: #since we have a user with an exisiting username, as username is unique, this if statement check if the provided password is the same as the password stored by index reference of their username.
                return True
            else:
                return False
        else:
            return False
        
obj = DatabaseUser("localhost", "root", "Mikyle123", "policy_management_system")
print(obj.isValidUser("Aa", "A"))