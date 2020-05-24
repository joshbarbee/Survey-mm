import mysql.connector
import mysql_creds as sql_d
import re

def aggregate(formatted_dict,matrix):
    database = mysql.connector.connect(host = sql_d.host, user = sql_d.user, passwd = sql_d.password, database = sql_d.database)

    cursor = database.cursor()
    sql = "INSERT INTO matched (name, username, matched_with) VALUES (%s, %s, %s)"
    for k, v in formatted_dict.items():
        username = str(k)
        matches = re.sub('[\[\]]', '', str(v))
        matrix_user = matrix["Username"][k]
        cursor.execute(sql,(k,matrix_user,matches))
    database.commit()
    return None

