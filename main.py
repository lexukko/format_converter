import sys
import json
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow
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

        # conversion manager
        self.pm = PluginManager()
        self.pm.load_plugins('plugins', [PluginReader, PluginWriter], False)

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

    def transform(self, plugin_reader, plugin_writter):
        try:
            start_time = datetime.now()
            plugin_reader.open()
            plugin_writter.open()
            for line in plugin_reader.read():
                plugin_writter.process_row(line)
            plugin_reader.close()
            plugin_writter.close()
            stop_time = datetime.now()
            elapsed_time = stop_time - start_time
            statistics = {
                "lines_read": plugin_reader.current_row,
                "written_lines": plugin_writter.current_row,
                "time_elapsed": str(elapsed_time)
            }
        except Exception as e:
            statistics = {
                "lines_read": plugin_reader.current_row,
                "written_lines": plugin_writter.current_row,
                "error": str(e)
            }
        finally:
            plugin_reader.close()
            plugin_writter.close()
        return json.dumps(statistics, indent=4, separators=(',', ':'))

    def refresh(self):
        self.ui.lstreaders.clear()
        for reader in self.pm.getNamesByClass(PluginReader):
            self.ui.lstreaders.addItem(reader)
        self.ui.lstwritters.clear()
        for writer in self.pm.getNamesByClass(PluginWriter):
            self.ui.lstwritters.addItem(writer)
        self.ui.txtlog.append("[Done] - Refresh")
        self.ui.statusBar.showMessage("[Done]")

    def run(self):
        iplug_name = self.ui.lstreaders.currentItem()
        oplug_name = self.ui.lstwritters.currentItem()
        if iplug_name is None or oplug_name is None:
            self.ui.txtlog.append("[Error] - Select plugins")
            return
        plugin_reader = self.pm.getClassByName(iplug_name.text())()
        plugin_writter = self.pm.getClassByName(oplug_name.text())()
        plugin_reader.set_config()
        plugin_writter.set_config()
        self.ui.txtlog.append("[Working] Transforming Inputs.")
        data = self.transform(plugin_reader, plugin_writter)
        self.ui.txtlog.append(data)
        self.ui.txtlog.append("[Done] Transformed.")


app = QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
