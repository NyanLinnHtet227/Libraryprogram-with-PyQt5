from PyQt5 import *
from PyQt5 import uic,QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtWidgets import QWidget
import mysql.connector as sql1

class Addclassfun(QDialog):
    def __init__(self,did):
        super(Addclassfun,self).__init__()
        uic.loadUi('updateform.ui',self)
        self.LoadData(did)
        print("this is id="+str(did))
        self.updatebtn.clicked.connect(self.updatefunc)
        self.clearbtn.clicked.connect(self.cleardata)
        self.insertbtn.clicked.connect(self.insertdata)
        self.deletebtn.clicked.connect(self.deletedata)
        self.backbtn.clicked.connect(self.backbtnfun)

    def updatefunc(self):
        self.DBconnect()
        author=self.authortxt.toPlainText()
        title=self.titletxt.toPlainText()
        department=self.departxt.toPlainText()
        library=self.librarytxt.toPlainText()
        copy=self.copytxt.toPlainText()
        sql_update="update office_library set Author=%s,Title=%s,library_No=%s,copies_No=%s where Department_No='"+department+"'"
        values=(author,title,library,copy)
        cursors=self.mydb2.cursor()
        cursors.execute(sql_update,values)
        self.mydb2.commit()
        self.cleardata()
        self.messageboxes("Update successful!","message info")

    def insertdata(self):
        self.DBconnect()
        author=self.authortxt.toPlainText()
        title=self.titletxt.toPlainText()
        department=self.departxt.toPlainText()
        library=self.librarytxt.toPlainText()
        copy=self.copytxt.toPlainText()  
        sql_insert=("insert into office_library(Author,Title,Department_No,library_No,copies_No) values(%s,%s,%s,%s,%s)") 
        values=(author,title,department,library,copy)
        cursors=self.mydb2.cursor()
        cursors.execute(sql_insert,values)
        self.mydb2.commit()
        self.cleardata()
        self.messageboxes("Insert successful!","message info")

    def deletedata(self):
        department=self.departxt.toPlainText()
        if len(department)==0:
            self.messageboxes("NO Data","message info")
        else:
            self.DBconnect()
            cursor=self.mydb2.cursor()
            sql_delete="delete from office_library where Department_No='"+department+"'"
            cursor.execute(sql_delete)
            self.mydb2.commit()
            self.cleardata()
            self.messageboxes("Delete successful!","message info")   

    def LoadData(self,did):
        self.DBconnect()
        sql_st="select * from office_library where Department_No='"+did+"'"
        cursors=self.mydb2.cursor()
        cursors.execute(sql_st)
        values=cursors.fetchone()
        self.authortxt.setPlainText(values[1])
        self.titletxt.setPlainText(values[2])
        self.departxt.setPlainText(values[3])
        self.librarytxt.setPlainText(str(values[4]))
        self.copytxt.setPlainText(str(values[5]))

    def backbtnfun(self):
        self.setVisible(False)
        from listform import listformclass
        lib=listformclass()
        lib.show()
        lib.exec_()

    def DBconnect(self):
        try:
            self.mydb2=sql1.connect(
                host='localhost',
                user='root',
                password='root',
                database='libreay_db'
            )
        except sql1.errors as err:
            print('DB error')
        
    def cleardata(self):
        self.authortxt.setPlainText("")
        self.titletxt.setPlainText("")
        self.departxt.setPlainText("")
        self.librarytxt.setPlainText("")
        self.copytxt.setPlainText("")

    def messageboxes(self,body,title):
        from PyQt5.QtWidgets import QMessageBox
        msg=QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(body)
        msg.exec_()