from PyQt5 import *
from PyQt5 import uic,QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
import sys

from PyQt5.QtWidgets import QWidget

class listloginform(QDialog):
    def __init__(self):
        super(listloginform,self).__init__()
        uic.loadUi('login.ui',self)
        self.loginbtn.clicked.connect(self.loginfunction)
        

    def loginfunction(self):
        username=self.usertxt.toPlainText().strip()
        password=self.passtxt.text()
        self.DBfunction()
        mycursor=self.mydb.cursor()
        mycursor.execute('select * from loginform_tb')
        rows=mycursor.fetchall()
        found=0
        for x in rows:
            user=x[1].strip()
            passw=x[2]
            if user==username and password==passw:
                self.setVisible(False)
                from listform import listformclass
                lib=listformclass()
                lib.show()
                lib.exec_()
                found=1
        if found==0:
            self.setVisible(False)
            msg=QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText("Invalid!\n something is wrong!")
            msg.exec_()

    def DBfunction(self):
        import mysql.connector as sql
        try:
            self.mydb=sql.connect(
                host='localhost',
                user='root',
                password='root',
                database='librarylogin_db'
            )
        except sql.errors as err:
            print('DB error')

if __name__=='__main__':
    app=QApplication([])
    win=listloginform()
    win.show()
    sys.exit(app.exec())