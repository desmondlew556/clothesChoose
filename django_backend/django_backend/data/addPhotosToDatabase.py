import os
import mysql.connector
def main():
    clothesChooseDB = mysql.connector.connect(
        host='',
        user='fiiecool',
        password='admin@Fiiecool7',
        database='clothesChoose'
    )
    cursorInstance=clothesChooseDB.cursor()
    for filename in enumerate(os.listdir("images")):
        sql="INSERT INTO female_Clothes(imageURL,score,rank) VALUES(%s,%s)"
        val=(filename,0,"0")
        cursorInstance.execute(sql,val)
        
    clothesChooseDB.commit()
    print(cursorInstance.rowcount," records inserted.")

if __name__ == '__main__':
    main()
