#code03.py
#주소록 입력, 사진등록, 리스트에 보이기, 저장, 불러오기 
#수정, 삭제 
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QMenu, QInputDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel
from myAddDB import * #이것은 내가 만든 myAddDB에서 모든 객체 및 함수를 사용하겠다.

class EditContactDialog(QDialog):
    def __init__(self, parent=None, name='', phone='', image_path=''):
        super().__init__(parent)
        # UI 파일 로드
        loadUi('./res/edit.ui', self)

        # 메인 윈도우 설정
        self.setWindowTitle('주소록수정')
        self.name_edit.setText(name)
        self.phone_edit.setText(phone)
        self.lblPicturePath.setText(image_path)
        
        pixmap = QPixmap(image_path)
        
        self.lblPicture.setPixmap(pixmap)
        self.lblPicture.setScaledContents(True)

        # 시그널 연결
        self.select_image_button.clicked.connect(self.select_image)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def select_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, '이미지 파일 선택', '.', '이미지 파일 (*.png *.jpg *.bmp *.gif)')
        if filename:
            self.lblPicturePath.setText(filename)  # 수정된 부분
            pixmap = QPixmap(filename)
            self.lblPicture.setPixmap(pixmap)


class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        # UI 파일 로드
        loadUi('./res/myWin01.ui', self)

        # 메인 윈도우 설정
        self.setWindowTitle('DB로 만드는 주소록 ver 0.2')
        
        # print (f'self.db객체는 {self.db}') #터미널에 확인

        # 나중에 할것 
        # 처음 실행시 self.db에서 주소록 데이터 가져와서 보여주기 

        
        # 버튼에 연결할 이벤트 핸들러
        self.btnPicture.clicked.connect(self.getimage)
        self.btnAdd.clicked.connect(self.add_contact)
        self.btnSave.clicked.connect(self.save_contacts)
        self.btnLoad.clicked.connect(self.load_contacts)

        # 연락처 정보를 저장할 리스트
        self.contacts = []

        # 리스트 위젯에 컨텍스트 메뉴 이벤트 설정
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.openMenu)

        # DB 객체를 생성한다. 
        self.db = mysqlDB()
        # self.load_contacts() 이것 대신 DB에서 가져 오는 함수를 아래 만듬
        self.load_contacts_from_DB()

    def openMenu(self, position):
        # 컨텍스트 메뉴 생성
        menu = QMenu()

        # 액션 추가
        editAction = menu.addAction("수정")
        deleteAction = menu.addAction("삭제")

        # 메뉴 실행 및 액션에 따른 함수 호출
        action = menu.exec_(self.listWidget.mapToGlobal(position))
        if action == editAction:
            self.edit_contact()
        elif action == deleteAction:
            self.delete_contact()

    def edit_contact(self):
        current_row = self.listWidget.currentRow()
        selected_items = self.listWidget.selectedItems()
        for item in selected_items:
            name, phone, image_path = item.text().split(',')
            
            dialog = EditContactDialog(self, name, phone, image_path)

            if dialog.exec_() == QDialog.Accepted:
                # 사용자가 다이얼로그에서 '확인'을 누른 경우, 정보 업데이트
                new_name = dialog.name_edit.text()
                new_phone = dialog.phone_edit.text()
                new_image_path = dialog.lblPicturePath.text()

                # 연락처 정보 업데이트
                self.contacts[current_row] = (new_name, new_phone, new_image_path)
                current_item = self.listWidget.item(current_row)
                current_item.setText(f'{new_name} , {new_phone}')
                current_item.setIcon(QIcon(new_image_path))

                # DB에 업데이트 하기 
                result = self.db.update(name,new_phone,new_image_path)
    

    def delete_contact(self):
        # 현재 선택된 아이템을 삭제하는 코드 작성
        current_row = self.listWidget.currentRow()
        if current_row != -1:
            # 리스트와 연락처 목록에서 아이템 삭제
            del self.contacts[current_row]
            self.listWidget.takeItem(current_row)
            item = self.listWidget.item(current_row)
            name,phone = item.text().split(',')

            # DB에서 삭제 하기 
            result = self.db.delete(name)
    def getimage(self):
        # 파일 다이얼로그 열기
        filename, _ = QFileDialog.getOpenFileName(self, '이미지 파일 선택', '.', '이미지 파일 (*.png *.jpg *.bmp *.gif)')

        if filename:
            # 파일이 선택되었을 때만 처리
            pixmap = QPixmap(filename)            
        else:
            filename = './res/unknown.jpg'
        
        self.lblPicture.setPixmap(pixmap)
        self.lblPicture.setScaledContents(True)
        # 이미지 파일의 경로 저장
        self.image_path = filename

    def add_contact(self):
        name = self.lineEditName.text()
        phone = self.lineEditPhone.text()

        # 이름과 전화번호가 입력되어 있는지 확인
        if name and phone:
            # 아이템 생성
            item = QListWidgetItem()
            item.setText(f'{name} , {phone}')
            
            # 사진이 선택되었는지 확인하고, 선택된 경우 아이콘 설정 및 이미지 파일의 경로 저장            
            if not hasattr(self, 'image_path'):
                self.image_path = './res/unknown.jpg'  # 기본 이미지 경로 설정                            
            
            icon = QIcon(self.image_path)
            item.setIcon(icon)

            # 연락처 정보를 리스트에 추가
            self.contacts.append((name, phone, self.image_path))
            # 리스트 위젯에 아이템 추가
            self.listWidget.addItem(item)

            #다 입력을 하고 나서 DB에 쓰는 작업만 추가 
            result = self.db.insert(name, phone, self.image_path)
            #print (result)
        else:
            print("이름과 전화번호를 입력하세요.")

    def save_contacts(self):
        # 연락처 정보를 텍스트 파일로 저장
        # filename, _ = QFileDialog.getSaveFileName(self, '연락처 저장', '.', '텍스트 파일 (*.txt)')
        filename = 'addBook2.txt'

        if filename:
            with open(filename, 'w', encoding='ansi') as file:
                for contact in self.contacts:
                    file.write(','.join(contact) + '\n')

    def load_contacts_from_DB(self):
        # 연락처 정보를 DB에서 불러오기
        results = self.db.getAllData()
        for row in results:
            name = row['name']
            phone = row['phone']
            image_path = row['filename']
        
            item = QListWidgetItem()
            item.setText(f'{name} , {phone} , {image_path}')

            # 이미지 아이콘 설정
            icon = QIcon(image_path)
            item.setIcon(icon)

            self.listWidget.addItem(item)
    def load_contacts(self):
        # 연락처 정보를 텍스트 파일에서 불러오기
        # filename, _ = QFileDialog.getOpenFileName(self, '연락처 불러오기', '.', '텍스트 파일 (*.txt)')
        filename = 'addBook2.txt'

        if filename:
            with open(filename, 'r', encoding='ansi') as file:
                self.contacts = [line.strip().split(',') for line in file.readlines()]
            
            # 불러온 연락처 정보를 리스트 위젯에 추가
            self.listWidget.clear()
            for contact in self.contacts:
                name, phone, image_path = contact
                item = QListWidgetItem()
                item.setText(f'{name} , {phone} , {image_path}')

                # 이미지 아이콘 설정
                icon = QIcon(image_path)
                item.setIcon(icon)

                self.listWidget.addItem(item)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
