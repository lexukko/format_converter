import sys
import json
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow
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

        # conversion manager
        self.pm = PluginManager()
        self.pm.load_plugins('plugins', [PluginReader, PluginProcess, PluginWriter], False)

        # globals plugins
        self.plugin_reader = None
        self.plugin_process = None
        self.plugin_writer = None


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

    def transform(self, plugin_reader, plugin_process, plugin_writter):
        try:
            start_time = datetime.now()
            # transform
            plugin_reader.open()
            if plugin_writter is not None:
                plugin_writter.open()
            # loop
            for line in plugin_reader.read():
                if plugin_process is None:
                    if plugin_writter is not None:
                        plugin_writter.write(line)
                else:
                    if plugin_writter is not None:
                        plugin_writter.write(plugin_process.process(line))
                    else:
                        plugin_process.process(line)
            if plugin_writter is not None:
                plugin_writter.close()
            plugin_reader.close()
            # Time & stadisticts
            stop_time = datetime.now()
            elapsed_time = stop_time - start_time
            statistics = {
                "time_elapsed": str(elapsed_time)
            }
        except Exception as e:
            statistics = {
                "error": str(e)
            }
        finally:
            plugin_reader.close()
            if plugin_writter is not None:
                plugin_writter.close()
        return json.dumps(statistics, indent=4, separators=(',', ':'))

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
            self.plugin_reader = self.pm.getClassByName(pplug_name.text())()
            self.plugin_reader.set_config()
        else:
            self.ui.txtlog.append("[Error] - Select Plugin")

    def lstwriters_config(self):
        oplug_name = self.ui.lstwriters.currentItem()
        if oplug_name is not None:
            self.plugin_reader = self.pm.getClassByName(oplug_name.text())()
            self.plugin_reader.set_config()
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
        self.ui.txtlog.append("[Working] Transforming Inputs.")
        data = self.transform(self.plugin_reader, self.plugin_process, self.plugin_writter)
        self.ui.txtlog.append(data)
        self.ui.txtlog.append("[Done] Transformed.")


app = QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
