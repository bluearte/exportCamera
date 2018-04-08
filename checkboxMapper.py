#! python2
from Qt import QtWidgets
from Qt import QtGui
from Qt import QtCore

import sys
import os

def GetData():
    data = dict()
    data["Unnamed1"] = {"class": ["Hero","Animals","Mystic"], "version":[1,2,3,4,5,6,7,8]}
    data["Unnamed2"] = {"class": ["Hero","Animals","Mystic"], "version":[1,2,3,4,5,6,7,8]}
    data["Unnamed3"] = {"class": ["Hero","Animals","Mystic"], "version":[1,2,3,4,5,6,7,8]}

    return data


class TestTable(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(TestTable, self).__init__(parent)

        self.chkMapper = QtCore.QSignalMapper()

        self.colChk = 0
        self.colName = 1
        self.colClass = 2
        self.colVersion = 3
        self.colButton = 4

        self.setHeaderName()
        self.setInitialData()
        self.setTableBehaviour()

    def setTableBehaviour(self):
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
    
    def setHeaderName(self):
        headerName = ["Check", "Name", "Class", "Version", "Button"]
        self.setColumnCount(len(headerName))
        self.setHorizontalHeaderItem(self.colChk, QtWidgets.QTableWidgetItem(headerName[self.colChk]))
        self.setHorizontalHeaderItem(self.colName, QtWidgets.QTableWidgetItem(headerName[self.colName]))
        self.setHorizontalHeaderItem(self.colClass, QtWidgets.QTableWidgetItem(headerName[self.colClass]))
        self.setHorizontalHeaderItem(self.colVersion, QtWidgets.QTableWidgetItem(headerName[self.colVersion]))
        self.setHorizontalHeaderItem(self.colButton, QtWidgets.QTableWidgetItem(headerName[self.colButton]))

    def setInitialData(self):
        data = GetData()
        self.setRowCount(len(data))

        for rowIndex, each in enumerate(data):
            chk = QtWidgets.QCheckBox()
            wdg = QtWidgets.QWidget()
            lyt = QtWidgets.QHBoxLayout()
            lyt.addWidget(chk)
            lyt.setAlignment(QtCore.Qt.AlignCenter)
            wdg.setLayout(lyt)

            self.setCellWidget(rowIndex, self.colChk, wdg)

            self.setItem(rowIndex, self.colName, QtWidgets.QTableWidgetItem(each))

            comboClass = QtWidgets.QComboBox()
            # comboClass.addItems(data.keys())
            self.setCellWidget(rowIndex, self.colClass, comboClass)

            comboVersion = QtWidgets.QComboBox()
            # comboVersion.addItems(map(lambda x: "v%02d" % x, data[each].values()[0]))
            self.setCellWidget(rowIndex, self.colVersion, comboVersion)

            btn = QtWidgets.QPushButton("Button", self)
            self.setCellWidget(rowIndex, self.colButton, btn)
            
            item = self.cellWidget(rowIndex, self.colChk)

            # item.stateChanged.connect(self.chkMapper.map)
            # self.chkMapper.setMapping(item, rowIndex)
            # self.chkMapper.mapped.connect(self.checkState)

            self.chkCb = item.layout().itemAt(0).widget()
            self.chkCb.stateChanged.connect(self.checkState)
            # item.stateChanged.connect(self.checkState)
            self.cellWidget(rowIndex, self.colClass).currentIndexChanged[str].connect(self.classOut)
            self.cellWidget(rowIndex, self.colVersion).currentIndexChanged[str].connect(self.verOut)
            self.cellWidget(rowIndex, self.colButton).clicked.connect(self.buttonClicked)

    def classOut(self, name):
        print(name)

    def verOut(self, name):
        print(name)

    def buttonClicked(self):
        sender = self.sender()
        print(sender.pos())

    def checkState(self, state):
        if state == QtCore.Qt.Checked:
            print(True)
        else:
            print(False)
        # print(self.chkCb.checkState())
        

class TestWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TestWidget, self).__init__(parent)

        self.setInitUi()
        self.resize(500,200)

    def setInitUi(self):
        tableWidget = TestTable()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tableWidget)

        self.setLayout(layout)

def main():
    main.testWidget = TestWidget()
    main.testWidget.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main()
    app.exec_()
