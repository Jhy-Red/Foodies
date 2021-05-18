#!usr/bin/python3
#from re import TEMPLATE
secret_file=open("/media/jhy/46AE-6494/Projet/id.txt","r")
secret_data=secret_file.readlines()
secret_file.close()
import mysql.connector


try : #Docker configured
    mydb = mysql.connector.connect(
      host="127.0.0.1"
    , port = "3308"
    , user=secret_data[0].strip()
    , password= secret_data[1].strip()
    , database = secret_data[2].strip()
    )
except : #docker base
    mydb = mysql.connector.connect(
      host="127.0.0.1"
    , port = "3308"
    , user= secret_data[0].strip()
    , password= secret_data[1].strip()
    )

def create_database(database) :
    mycursor = mydb.cursor()
    request = "CREATE DATABASE {database} ".format(database= database )
    mycursor.execute(request)
    mycursor.close()

#create_database("Foodies")

def show_base():
    mycursor = mydb.cursor()
    request = "SHOW DATABASES"
    mycursor.execute(request)
    for x in mycursor:
     print(x) 
    mycursor.close()

#show_base()

def show_table():
    mycursor = mydb.cursor()
    request = "SHOW TABLES"
    mycursor.execute(request)

    for x in mycursor:
     print(x) 
    mycursor.close()

#show_table()


def create_table_users():
    mycursor = mydb.cursor()

    request_init = "CREATE TABLE USERS "

    ID_USERS = "ID_USERS INT PRIMARY KEY NOT NULL AUTO_INCREMENT"
    CREATION = "CREATION DATETIME DEFAULT (CURRENT_TIMESTAMP()) "
    E_MAIL   = "E_MAIL VARCHAR(25) UNIQUE "
    TEL      = "TEL VARCHAR(10) UNIQUE "
    USERNAME = "USERNAME VARCHAR(25) NOT NULL UNIQUE " 
    PASSWORD = "PASSWORD VARCHAR(255) NOT NULL " 
    AGE      = "AGE INT(3) DEFAULT 0 "
    POIDS    = "KG INT(3)  DEFAULT 0"
    SEXE     = "SEXE VARCHAR(1) DEFAULT 'X' "
    NOM      = "NOM VARCHAR(25) "
    
    request_SQL_LOG     = ID_USERS + "," + CREATION + "," +  E_MAIL + ","  + TEL + ","  +USERNAME + "," + PASSWORD 
    request_SQL_APP     = AGE + "," + POIDS   +  "," + SEXE 
    request_SQL_BONUS   = NOM

    request = request_init + "(" + request_SQL_LOG + "," + request_SQL_APP + "," + request_SQL_BONUS + ")"
    mycursor.execute(request)
    mycursor.close() 

#create_table_users()
    
def show_elements(Table = 'USERS'):
    """
    import mysql.connector

    mydb = mysql.connector.connect(
       host="localhost"
    , user="root"
    , password="Umbrell@2325"
    , database = "FOOD_ALPHA"
    )
    """

    mycursor = mydb.cursor()
    request = "SELECT * FROM {TABLE}".format(TABLE = Table)
    mycursor.execute(request)
    result = mycursor.fetchall()
    mycursor.close() 
    return result

#print(show_elements())


def drop_table(table):
    mycursor = mydb.cursor()
    request = "DROP TABLES {table}".format(table = table)
    mycursor.execute(request)
    mydb.commit()
    mycursor.close()
#drop_table("USERS")

def insert_table_USERS(MAIL,USERNAME ,PASSWORD, table = 'USERS',hash = True ):
    try :
        mycursor = mydb.cursor()
        request_init = "INSERT INTO {TABLE}".format(TABLE = table)
        request_table = "(E_MAIL, USERNAME,PASSWORD)"
        
        if hash is True :
            request_value =  "('{MAIL}','{USERNAME}', MD5('{PASSWORD}'))".format(MAIL = MAIL,USERNAME = USERNAME, PASSWORD = PASSWORD)
        elif hash is False :
            request_value =  "('{MAIL}','{USERNAME}','{PASSWORD}')".format(MAIL = MAIL,USERNAME = USERNAME, PASSWORD = PASSWORD)
        
        request = request_init + request_table + "VALUES" + request_value +";"
        mycursor.execute(request)
        mydb.commit()
        mycursor.close()
        print ("Inscription reussis ! Bienvenu")
    except : 
        print ("Nom d'utilisateurs déja existant, veuillez en choisir un autre")


#show_base()
#create_table_users()
#show_table()
#insert_table_USERS(USERNAME = 'Jhyeon', PASSWORD = 2325, AGE = 28, KG = 94)
#print(show_elements(Table = "USERS"))
#drop_table(table = "USERS")


def creation_user(MAIL,USERNAME ,PASSWORD, table = 'USERS', hash = True):
    mycursor = mydb.cursor()
    request_init = "INSERT INTO {TABLE}".format(TABLE = table)
    request_table = "(E_MAIL, USERNAME,PASSWORD)"
    if hash is True :
        request_value =  "('{MAIL}','{USERNAME}',MD5('{PASSWORD}'))".format(MAIL = MAIL,USERNAME = USERNAME, PASSWORD = PASSWORD)
    elif hash is False :
        request_value =  "('{MAIL}','{USERNAME}','{PASSWORD}')".format(MAIL = MAIL,USERNAME = USERNAME, PASSWORD = PASSWORD)
    
    request = request_init + request_table + "VALUES" + request_value +";"
    mycursor.execute(request)
    mycursor.close()
    mydb.commit()


def connection_user(MAIL,PASSWORD, table = 'USERS'):
    """
    Request Token users
    """
    mycursor = mydb.cursor()
    request = "SELECT ID_USERS,E_MAIL, PASSWORD,USERNAME FROM {TABLE} WHERE E_MAIL = '{EMAIL}' AND PASSWORD =MD5('{PASSWORD}')".format(TABLE = table, EMAIL =MAIL, PASSWORD = PASSWORD)
    mycursor.execute(request)
    result = mycursor.fetchall()
    mycursor.close()
    ID = result[0][0]
    email = result[0][1]
    password = result[0][2]
    pseudo = result[0][3] 
    mycursor.close()
    return ID,email,password,pseudo

"""
A,B,C,D = connection_user(MAIL = "jhyeon@hotmail.fr", PASSWORD = "Elsa")
print(A)
print(B)
print(C)
print(D)
"""

def information_user(ID,userdata, table = 'USERS'):
    """
    Request ID users for flask login
    """
    mycursor = mydb.cursor()
    request = "SELECT * FROM {TABLE} WHERE ID_USERS = '{ID}' ".format(TABLE = table, ID=ID)
    mycursor.execute(request)
    result = mycursor.fetchall()

    userdata.ID = result[0][0]
    userdata.Date_creation = result[0][1]
    userdata.Adresse_mail = result[0][2]
    userdata.TEL = result[0][3]
    userdata.Pseudo = result[0][4]
    #userdata.Mot_de_passe = result[0][5]	
    userdata.Age = result[0][6] 
    userdata.Poids = result[0][7]
    userdata.Sexe = result[0][8]
    
    mycursor.close()
    return userdata

def information_user2(ID,table='USERS'):
    """
    Request ID users for flask login
    """
    mycursor = mydb.cursor()
    request = "SELECT * FROM {TABLE} WHERE ID_USERS = '{ID}' ".format(TABLE = table, ID=ID)
    mycursor.execute(request)
    result = mycursor.fetchall()

    return result

#from userdata import User
#userdata = User()
#userdata.get_data(1)
#data = information_user(1,userdata)
#print(data.Adresse_mail)
#print(userdata.Adresse_mail)
