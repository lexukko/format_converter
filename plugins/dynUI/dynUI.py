from os.path import expanduser

from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QCheckBox, \
    QGroupBox, QRadioButton, \
    QComboBox, QTableWidget, QFileDialog


class DynDialog(QDialog):
    FILE_DIALOG_SAVE = 0
    FILE_DIALOG_OPEN = 1

    def __init__(self, parent=None):
        super(DynDialog, self).__init__(parent)
        self.init_ui()
        self.resize(500, 400)

    def set_tittle(self, tittle):
        self.setWindowTitle(tittle)

    def init_ui(self):

        # data
        self.data_dict = {}

        # layout
        self.GeneralLayout = QHBoxLayout(self)
        self.VerticalLayout = QVBoxLayout()
        self.FieldsLayout = QFormLayout()
        self.VerticalLayout.addLayout(self.FieldsLayout)
        self.GeneralLayout.addLayout(self.VerticalLayout)

        # add buttons

        self.okButton = QPushButton("OK")
        self.cancelButton = QPushButton("Cancel")

        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.okButton)
        self.hbox.addWidget(self.cancelButton)

        self.VerticalLayout.addLayout(self.hbox)

        # connect events
        self.okButton.clicked.connect(self.ok)
        self.cancelButton.clicked.connect(self.cancel)

    def add_line_edit(self, widget_name, caption, exampleText, data):
        self.txt = QLineEdit(self)
        self.txt.setObjectName(widget_name)
        self.txt.setPlaceholderText(exampleText)
        if exampleText:
            self.txt.setPlaceholderText(exampleText)
        if data:
            self.txt.setText(data)
        self.FieldsLayout.addRow(caption, self.txt)

    def add_combo_box(self, widget_name, caption, items, default_item):
        self.cmb = QComboBox(self)
        self.cmb.setObjectName(widget_name)
        for k, v in items.items():
            self.cmb.addItem(k, v)
        self.cmb.setCurrentIndex(self.cmb.findData(default_item))
        self.FieldsLayout.addRow(caption, self.cmb)

    def add_check_box(self, widget_name, caption, data):
        self.chk = QCheckBox(self)
        self.chk.setObjectName(widget_name)
        self.chk.setText(caption)
        if data:
            self.chk.setChecked(data)
        self.FieldsLayout.addWidget(self.chk)

    def add_radio_group(self, widget_name, caption, items):
        self.grp = QGroupBox(caption)
        self.grp.setObjectName(widget_name)
        self.vl = QVBoxLayout()
        self.grp.setLayout(self.vl)
        selected = True
        for item in items:
            self.opt = QRadioButton()
            self.opt.setObjectName(item)
            self.opt.setText(item)
            if selected:
                self.opt.setChecked(selected)
                selected = False
            self.vl.addWidget(self.opt)
        self.FieldsLayout.addWidget(self.grp)

    def add_check_group(self, widget_name, caption, items):
        self.grp = QGroupBox(caption)
        self.grp.setObjectName(widget_name)
        self.vl = QVBoxLayout()
        self.grp.setLayout(self.vl)
        selected = True
        for item in items:
            self.opt = QCheckBox()
            self.opt.setObjectName(item)
            self.opt.setText(item)
            if selected:
                self.opt.setChecked(selected)
                selected = False
            self.vl.addWidget(self.opt)
        self.FieldsLayout.addWidget(self.grp)

    def add_file(self, widget_name, caption, file_patterns, dialog_type, data):
        self.txt_file = QLineEdit(self)
        self.txt_file.setObjectName(widget_name)
        self.txt_file.setText(data)
        self.btn_file = QPushButton("...")
        self.btn_file.setMaximumWidth(50)
        self.FieldsLayout.addRow(caption, self.txt_file)
        self.FieldsLayout.addWidget(self.btn_file)
        self.btn_file.clicked.connect(lambda: self.file_dialog(widget_name, file_patterns, dialog_type))

    def add_table(self, widget_name, caption, headers, row_types):

        # setup layout
        self.grp = QGroupBox(caption)
        self.vl = QVBoxLayout()
        self.grp.setLayout(self.vl)
        self.tbl = QTableWidget(self)
        self.tbl.setObjectName(widget_name)
        self.tbl.setSortingEnabled(True)
        self.vl.addWidget(self.tbl)
        self.hl = QHBoxLayout()
        self.hl.addStretch(1)

        self.btn_add = QPushButton("+")
        self.btn_del = QPushButton("-")

        self.hl.insertWidget(0, self.btn_add, 0)
        self.hl.insertWidget(1, self.btn_del, 0)

        self.vl.addLayout(self.hl)
        self.FieldsLayout.addWidget(self.grp)

        # setup widgets
        self.tbl.setColumnCount(len(headers))
        self.tbl.setRowCount(0)
        self.tbl.setHorizontalHeaderLabels(headers)

        self.btn_add.clicked.connect(lambda: self.table_add(widget_name, row_types))
        self.btn_del.clicked.connect(lambda: self.table_del(widget_name))

    def ok(self):
        widgets = (self.FieldsLayout.itemAt(i).widget() for i in range(self.FieldsLayout.count()))
        for w in widgets:
            if isinstance(w, QLineEdit):
                self.data_dict[w.objectName()] = w.text()
            if isinstance(w, QComboBox):
                self.data_dict[w.objectName()] = w.currentData()
            if isinstance(w, QCheckBox):
                self.data_dict[w.objectName()] = w.isChecked()
            if isinstance(w, QGroupBox):
                grp = {}
                widgets = (w.layout().itemAt(i).widget() for i in range(w.layout().count()))
                for w2 in widgets:
                    if isinstance(w2, QRadioButton) or isinstance(w2, QCheckBox):
                        grp[w2.objectName()] = w2.isChecked()
                        self.data_dict[w.objectName()] = grp
                    if isinstance(w2, QTableWidget):
                        self.data_dict[w2.objectName()] = self.get_table_data(w2.objectName())

        self.accept()

    def file_dialog(self, widget_name, file_patterns, dialog_type):
        edit_obj = self.findChild(QLineEdit, widget_name)
        if edit_obj is not None:
            if dialog_type == DynDialog.FILE_DIALOG_OPEN:
                filename = QFileDialog.getOpenFileName(self, "Open File", expanduser('~'), file_patterns)
            elif dialog_type == DynDialog.FILE_DIALOG_SAVE:
                filename = QFileDialog.getSaveFileName(self, "Save File", expanduser('~'), file_patterns)
            edit_obj.setText(filename[0])

    def table_add(self, widget_name, col_types):
        table_obj = self.findChild(QTableWidget, widget_name)
        if table_obj is not None:
            curCol = 0
            curRow = table_obj.rowCount()
            if table_obj.currentRow() != -1:
                curRow = table_obj.currentRow()
            table_obj.insertRow(curRow)
            for col_type in col_types:
                if isinstance(col_type, dict):
                    self.w = QComboBox(self)
                    for k, v in col_type.items():
                        self.w.addItem(k, v)
                    table_obj.setCellWidget(curRow, curCol, self.w)
                elif isinstance(col_type, bool):
                    self.w = QCheckBox(self)
                    self.w.setStyleSheet("margin-left:40%; margin-right:60%;")
                    self.w.setChecked(col_type)
                    table_obj.setCellWidget(curRow, curCol, self.w)
                else:
                    self.w = QLineEdit(self)
                    table_obj.setCellWidget(curRow, curCol, self.w)
                curCol += 1

    def table_del(self, widget_name):
        table_obj = self.findChild(QTableWidget, widget_name)
        if table_obj is not None:
            curRow = table_obj.currentRow()
            if curRow != -1:
                table_obj.removeRow(curRow)
            elif table_obj.rowCount() > 0:
                table_obj.removeRow(table_obj.rowCount() - 1)

    def get_table_data(self, widget_name):
        table_obj = self.findChild(QTableWidget, widget_name)
        data = []
        if table_obj is not None:
            for col in range(table_obj.columnCount()):
                cols = []
                for row in range(table_obj.rowCount()):
                    if isinstance(table_obj.cellWidget(row, col), QLineEdit):
                        cols.append(table_obj.cellWidget(row, col).text())
                    elif isinstance(table_obj.cellWidget(row, col), QComboBox):
                        cols.append(table_obj.cellWidget(row, col).currentData())
                    elif isinstance(table_obj.cellWidget(row, col), QCheckBox):
                        cols.append(table_obj.cellWidget(row, col).isChecked())

                data.append(cols)
        return data

    def cancel(self):
        self.reject()
