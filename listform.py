from PyQt5 import *
from PyQt5 import uic,QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox
import sys
import mysql.connector as sql
from PyQt5.QtWidgets import QWidget

class listformclass(QDialog):
    def __init__(self):
        super(listformclass,self).__init__()
        uic.loadUi('libraryform.ui',self)
        self.searchbut.clicked.connect(self.searchfun)
        self.tableView.clicked.connect(self.selectfound)
        self.selectbut.clicked.connect(self.selectfunction)

    def selectfound(self):
        self.selectbut.setEnabled(True)

    def selectfunction(self):
        index=self.tableView.selectionModel().currentIndex()
        values=index.sibling(index.row(),index.column()).data()
        self.setVisible(False)
        from Add import Addclassfun
        adf=Addclassfun(values)
        adf.show()
        adf.exec_()

    def searchfun(self):
        checkpoint=None
        inputpoint=None
        if self.authorbut.isChecked():
            checkpoint='Author'
        elif self.Titlebut.isChecked():
            checkpoint='Title'
        elif self.departbut.isChecked():
            checkpoint='Department_No'
        else:
            checkpoint='library_No'
        inputpoint=self.inputtxt.toPlainText().strip()
        self.inputtxt.clear()
        self.DBconnect()
        mycursor=self.mydb.cursor()
        sql_search="select * from office_library where "+checkpoint+"='"+inputpoint+"'"
        mycursor.execute(sql_search)
        row=mycursor.fetchall()
        if len(row)==0:
            from PyQt5.QtWidgets import QMessageBox
            msg=QMessageBox() 
            msg.setText('Your information is wrong,try again!')
            msg.setWindowTitle("No Data")
            msg.exec_()
        else:
            import pandas as pd
            sq_quary=pd.read_sql(sql_search,self.mydb)
            df=pd.DataFrame(sq_quary,columns=['Id','Author','Title','Department_No','library_No','copies_No'])
            from TableModel import pandasModel
            model=pandasModel(df)
            self.tableView.setModel(model)

    def DBconnect(self):
        try:
            self.mydb=sql.connect(
                host='localhost',
                user='root',
                password='root',
                database='libreay_db'
            )
        except sql.errors as err:
            print('DB error')
