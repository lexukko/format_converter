from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, \
    QLineEdit


class Ui_Dialog(QDialog):
    def __init__(self, parent=None):

        super(Ui_Dialog, self).__init__(parent)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnok = QPushButton(self)
        self.btnok.setObjectName("btnok")
        self.horizontalLayout.addWidget(self.btnok)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.btnok.clicked.connect(self.accept)
        self.retranslateUi(self)

    def add_data(self, headers, data):
        # setup widgets
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for row in data:
            y = self.tableWidget.rowCount()
            self.tableWidget.insertRow(y)
            for x in range(len(row)):
                self.edit = QLineEdit()
                self.edit.setText(row[x])
                self.tableWidget.setCellWidget(y, x, self.edit)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btnok.setText(_translate("Dialog", "ok"))