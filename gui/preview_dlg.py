from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, \
    QLabel


class Ui_Dialog(QDialog):
    def __init__(self, tittle, parent=None):

        super(Ui_Dialog, self).__init__(parent)

        self.setWindowTitle(tittle)
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
        self.btnok.setText("ok")

    def add_data(self, headers, data):
        # setup widgets
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(headers)

        for row in data:
            y = self.tableWidget.rowCount()
            self.tableWidget.insertRow(y)
            for x in range(len(row)):
                self.tableWidget.setCellWidget(y, x, QLabel(row[x]))

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.resize(800, 600)
