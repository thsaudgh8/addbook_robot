import sys
import pymysql
from PyQt5.QtWidgets import QApplication
class mysqlDB():
    def __init__(self) -> None:
        pymysql.version_info=(1,4,2,"final",0)
        pymysql.install_as_MySQLdb()
        super().__init__()

        #이것이 무엇인가 하면 데이터베이스를 다루는 객체임.
        self.connection = pymysql.connect(
            host='localhost',
            user='thsaudgh8',      #데이터베이스의 사용자 이름
            passwd='son!@!@1212',
            db='thsaudgh8',
            charset='utf8',
            port=3306,          #일반적으로 사용하는 포트임
            cursorclass=pymysql.cursors.DictCursor
        )
    def insert(self, new_name, new_phone, new_filename):
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO addbook (name, phone, filename) VALUES (%s, %s, %s)"
            result = cursor.execute(sql, (new_name, new_phone, new_filename))            
            self.connection.commit()    # 메모리 내용을 DB로 전송
            return result
    
    def update(self, key_name, new_phone, new_filename):
        with self.connection.cursor() as cursor:
            sql = "UPDATE `addbook` SET phone= %s, filename = %s WHERE name=%s"
            result = cursor.execute(sql, (new_phone, new_filename, key_name))            
            self.connection.commit()    # 메모리 내용을 DB로 전송
            return result
    
    def search(self, key_any):
        with self.connection.cursor() as cursor:            
            #이름이나 전화번호가 비슷할때 즉 '황' '1' 처럼 key_any를 포함할때
            sql2 = "SELECT * FROM `addbook` WHERE name LIKE %s OR phone LIKE %s OR filename LIKE %s"
            key = '%' + key_any + '%' # 반드시 전처리를 해줘야 합니다. 
            cursor.execute(sql2, (key, key, key))            
            # result = cursor.fetchone() # 이것은 execute한 결과값중 1개를 
            result = cursor.fetchall() # 이것은 execute한 결과값중 전부를
            return result
    
    def delete(self, key_name):
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM addbook WHERE name = %s"
            result = cursor.execute(sql, key_name)
            self.connection.commit()
            return result
    
    def getAllData(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM addbook"
            cursor.execute(sql)
            results = cursor.fetchall() # 이것은 execute한 결과값중 전부를
            return results

if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = mysqlDB()
    # 데이터 추가 하기 테스트 
    result = db.insert("황동하0326-11","110-2512-6818","")
    print (result)
    input("앤터를 누르세요")
    
    # 업데이트 
    result = db.update("황동하0326-11","110-0326-2024","")
    print (result)
    input("앤터를 누르세요")

    #찾기 
    result = db.search('황')
    print (result)
    input("앤터를 누르세요")

    #삭제 
    result = db.delete('황0326-11')
    print (result)
    input("앤터를 누르세요")

    #전체리스트 불러오기 
    results = db.getAllData()
    for row in results:
        name = row['name']
        phone = row['phone']
        filename = row['filename']
        print (f'name : {name}, phone : {phone}, filename : {filename}')
    
    
