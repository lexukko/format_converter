import sys
import json
from gui.preview_dlg import Ui_Dialog
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QLabel
from gui.ui_mainwindow import Ui_MainWindow
import gui.icons_rc
from plugins.categorias.categorias import PluginReader, PluginWriter
from plugin_manager import PluginManager


class MyWindowClass(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        # load qtcreator ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # connect actions & slots
        self.ui.actionRefresh.triggered.connect(self.refresh)
        self.ui.actionRun.triggered.connect(self.run)
        self.ui.actionExit.triggered.connect(self.close)

        self.ui.pbreaderconfig.clicked.connect(self.lstreaders_config)
        self.ui.pbwriterconfig.clicked.connect(self.lstwriters_config)

        self.ui.pbpreview.clicked.connect(self.preview_data)

        # conversion manager
        self.pm = PluginManager()
        self.pm.load_plugins('plugins', [PluginReader, PluginWriter], False)

        # globals plugins
        self.plugin_reader = None
        self.plugin_writer = None

        self.iplug_name = None
        self.oplug_name = None

        # table headers
        self.ui.tblwidget.setColumnCount(3)
        self.ui.tblwidget.setRowCount(3)
        self.ui.tblwidget.setHorizontalHeaderLabels(["plugin", "read", "write"])

        # progress labels table
        self.lbl_input_plugin = QLabel(self)
        self.lbl_process_plugin = QLabel(self)
        self.lbl_output_plugin = QLabel(self)

        self.lbl_input_read = QLabel(self)
        self.lbl_process_read = QLabel(self)
        self.lbl_output_read = QLabel(self)

        self.lbl_input_write = QLabel(self)
        self.lbl_process_write = QLabel(self)
        self.lbl_output_write = QLabel(self)

        self.ui.tblwidget.setCellWidget(0, 0, self.lbl_input_plugin)
        self.ui.tblwidget.setCellWidget(0, 1, self.lbl_process_plugin)
        self.ui.tblwidget.setCellWidget(0, 2, self.lbl_output_plugin)

        self.ui.tblwidget.setCellWidget(1, 0, self.lbl_input_read)
        self.ui.tblwidget.setCellWidget(1, 1, self.lbl_process_read)
        self.ui.tblwidget.setCellWidget(1, 2, self.lbl_output_read)

        self.ui.tblwidget.setCellWidget(2, 0, self.lbl_input_write)
        self.ui.tblwidget.setCellWidget(2, 1, self.lbl_process_write)
        self.ui.tblwidget.setCellWidget(2, 2, self.lbl_output_write)

        self.clearProgress()

    def clearProgress(self):
        self.lbl_input_plugin.setText("")
        self.lbl_process_plugin.setText("")
        self.lbl_output_plugin.setText("")

        self.lbl_input_read.setText("")
        self.lbl_process_read.setText("")
        self.lbl_output_read.setText("")

        self.lbl_input_write.setText("")
        self.lbl_process_write.setText("")
        self.lbl_output_write.setText("")

    def updateProgress(self):
        if self.plugin_reader is not None:
            self.lbl_input_plugin.setText(self.plugin_reader.name)
            self.lbl_process_plugin.setText(str(self.plugin_reader.current_row))
            self.lbl_output_plugin.setText("")

        if self.plugin_writer is not None:
            self.lbl_input_write.setText(self.plugin_writer.name)
            self.lbl_process_write.setText(str(self.plugin_writer.current_row))
            self.lbl_output_write.setText("")

        self.ui.tblwidget.resizeColumnsToContents()
        self.ui.tblwidget.resizeRowsToContents()


    # utils functions
    def refresh_table(self):
        self.ui.tblwidget.clear()

    def transform(self):
        if self.plugin_reader is None or self.plugin_writer is None:
            self.ui.txtlog.append("Select & config input/output plugin(s) !!")
            return
        try:
            # get header
            self.plugin_reader.open()
            header = self.plugin_reader.get_header()
            # set header
            self.plugin_writer.open()
            self.plugin_writer.set_header(header)
            # loop
            self.ui.txtlog.append("[Working] Transforming Inputs.")
            for line in self.plugin_reader.read():
                self.updateProgress()
                self.plugin_writer.write(line)
            self.ui.txtlog.append("[Done] Success! .")
        except Exception as e:
            self.ui.txtlog.append(str(e))
        finally:
            self.plugin_reader.close()
            self.plugin_writer.close()
            self.plugin_reader = None
            self.plugin_writer = None

    # SLOTS

    def preview_data(self):
        if self.plugin_reader is None:
            self.ui.txtlog.append("Select & config input plugin !!")
            return
        # read data
        preview_rows, ok = QInputDialog.getInt(self, "Input", "Select Number of rows", 100)
        current_row = 0
        headers = []
        data = []
        try:
            self.plugin_reader.open()
            for line in self.plugin_reader.read():
                current_row += 1
                if current_row > 1:
                    data.append(line)
                else:
                    headers = line
                if current_row > int(preview_rows):
                    break
        except Exception as e:
            self.ui.txtlog.append(str(e))
        finally:
            self.plugin_reader.close()
        # display data
        dlg = Ui_Dialog( "Preview Data - {0} Lines".format(preview_rows) , self)
        dlg.add_data(headers, data)
        dlg.exec_()

    def lstreaders_config(self):
        if self.ui.lstreaders.currentItem() is None:
            self.ui.txtlog.append("[Error] - Select Plugin")
            return
        
        if self.iplug_name != self.ui.lstreaders.currentItem():
            self.iplug_name = self.ui.lstreaders.currentItem()
            self.plugin_reader = self.pm.getClassByName(self.iplug_name.text())()
            self.plugin_reader.set_config()
        else:
            self.plugin_reader.set_config()

    def lstwriters_config(self):
        if self.ui.lstwriters.currentItem() is None:
            self.ui.txtlog.append("[Error] - Select Plugin")
            return

        if self.oplug_name != self.ui.lstwriters.currentItem():
            self.oplug_name = self.ui.lstwriters.currentItem()
            self.plugin_writer = self.pm.getClassByName(self.oplug_name.text())()
            self.plugin_writer.set_config()
        else:
            self.plugin_writer.set_config()


    def refresh(self):
        self.ui.lstreaders.clear()
        for reader in self.pm.getNamesByClass(PluginReader):
            self.ui.lstreaders.addItem(reader)

        self.ui.lstwriters.clear()
        for writer in self.pm.getNamesByClass(PluginWriter):
            self.ui.lstwriters.addItem(writer)

        self.ui.txtlog.append("[Done] - Refresh")

    def run(self):
        self.transform()

# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    app.exec_()
