import sys
import json
from gui.preview_dlg import Ui_Dialog
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
from gui.ui_mainwindow import Ui_MainWindow
import gui.icons_rc
from plugins.categorias.categorias import PluginReader, PluginWriter, PluginProcess
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
        self.ui.pbprocessconfig.clicked.connect(self.lstprocess_config)
        self.ui.pbwriterconfig.clicked.connect(self.lstwriters_config)

        self.ui.pbpreview.clicked.connect(self.preview_data)

        # conversion manager
        self.pm = PluginManager()
        self.pm.load_plugins('plugins', [PluginReader, PluginProcess, PluginWriter], False)

        # globals plugins
        self.plugin_reader = None
        self.plugin_process = None
        self.plugin_writer = None

        # table headers
        self.ui.tblwidget.setColumnCount(3)
        self.ui.tblwidget.setRowCount(3)
        self.ui.tblwidget.setHorizontalHeaderLabels(["plugin", "read", "write"])

    # utils functions

    def refresh_table(self):
        self.ui.tblwidget.clear()

    def line_count(self, plugin_reader):
        line_count = 0
        try:
            plugin_reader.open()
            for line in plugin_reader.read():
                line_count += 1
            plugin_reader.close()
        except Exception as e:
            plugin_reader.close()
            return json.dumps({"error": str(e)})
        return line_count

    def transform(self):
        if self.plugin_reader is None:
            self.ui.txtlog.append("Select & config input plugin !!")
            return
        if self.plugin_process is None or self.plugin_writer is None:
            self.ui.txtlog.append("Select & config process/input plugin(s) !!")
            return
        try:
            # transform
            self.plugin_reader.open()
            if self.plugin_writer is not None:
                self.plugin_writer.open()
            # loop
            self.ui.txtlog.append("[Working] Transforming Inputs.")
            for line in self.plugin_reader.read():
                if self.plugin_process is None:
                    if self.plugin_writer is not None:
                        self.plugin_writer.write(line)
                else:
                    if self.plugin_writer is not None:
                        self.plugin_writer.write(self.plugin_process.process(line))
                    else:
                        self.plugin_process.process(line)
            self.ui.txtlog.append("[Done] Success! .")
        except Exception as e:
            self.ui.txtlog.append(str(e))
        finally:
            self.plugin_reader.close()
            if self.plugin_writer is not None:
                self.plugin_writer.close()
            self.plugin_reader = None
            self.plugin_process = None
            self.plugin_writer = None

    # SLOTS

    def preview_data(self):
        if self.plugin_reader is None:
            self.ui.txtlog.append("Select & config input plugin !!")
            return
        # read data
        preview_rows, ok = QInputDialog.getInt(self, "Input", "Select Number of rows")
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
        dlg = Ui_Dialog(self)
        dlg.add_data(headers, data)
        dlg.exec_()

    def lstreaders_config(self):
        iplug_name = self.ui.lstreaders.currentItem()
        if iplug_name is not None:
            self.plugin_reader = self.pm.getClassByName(iplug_name.text())()
            self.plugin_reader.set_config()
        else:
            self.ui.txtlog.append("[Error] - Select Plugin")

    def lstprocess_config(self):
        pplug_name = self.ui.lstprocess.currentItem()
        if pplug_name is not None:
            self.plugin_process = self.pm.getClassByName(pplug_name.text())()
            self.plugin_process.set_config()
        else:
            self.ui.txtlog.append("[Error] - Select Plugin")

    def lstwriters_config(self):
        oplug_name = self.ui.lstwriters.currentItem()
        if oplug_name is not None:
            self.plugin_writer = self.pm.getClassByName(oplug_name.text())()
            self.plugin_writer.set_config()
        else:
            self.ui.txtlog.append("[Error] - Select Plugin")

    def refresh(self):
        self.ui.lstreaders.clear()
        for reader in self.pm.getNamesByClass(PluginReader):
            self.ui.lstreaders.addItem(reader)
        self.ui.lstprocess.clear()
        for process in self.pm.getNamesByClass(PluginProcess):
            self.ui.lstprocess.addItem(process)
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
