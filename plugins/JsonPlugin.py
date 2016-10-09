import json
import locale
from plugins.categorias.categorias import PluginReader, PluginWriter
from plugins.dynUI.dynUI import DynDialog


class JSONReaderLines(PluginReader):
    def __init__(self):
        self.name = "JSONReaderLines"
        self.version = "1.0"
        self.description = "Plugin de lectura de archivos JSON por lineas"

        self.file_path = None
        self.encoding = None

        self.current_row = 0

    def set_config(self):
        # dynamic DynDialog
        dialog = DynDialog()
        dialog.set_tittle("{0} - Setup".format(self.name))
        dialog.add_file("file_path", "Select File:", "Text Files (*.txt *.csv *.dat);;All Files(*.*)",
                        DynDialog.FILE_DIALOG_OPEN)
        dialog.add_line_edit("encoding", "Encoding:", "", "")
        dialog.exec_()
        config = dialog.data_dict
        # set config
        self.file_path = config["file_path"]
        if config["encoding"]:
            self.encoding = config["encoding"]
        else:
            self.encoding = locale.getpreferredencoding(False)

    def open(self):
        self.json_file = open(file=self.file_path, mode="rt", newline=None, encoding=self.encoding)

    def read(self):
        for line in self.json_file:
            json_line = json.loads(line)
            self.current_row += 1
            yield (json_line)

    def close(self):
        self.json_file.close()


class JSONWriterLines(PluginWriter):
    def __init__(self):
        self.name = "JSONWriterLines"
        self.version = "1.0"
        self.description = "Plugin de escritura de archivos JSON por lineas"

        self.file_path = None
        self.encoding = None

        self.current_row = 0

    def set_config(self):
        # dynamic DynDialog
        dialog = DynDialog()
        dialog.set_tittle("{0} - Setup".format(self.name))
        dialog.add_file("file_path", "Select File:", "Text Files (*.txt *.csv *.dat);;All Files(*.*)",
                        DynDialog.FILE_DIALOG_SAVE)
        dialog.add_line_edit("encoding", "Encoding:", "", "")
        dialog.exec_()
        config = dialog.data_dict
        # set config
        self.file_path = config["file_path"]
        if config["encoding"]:
            self.encoding = config["encoding"]
        else:
            self.encoding = locale.getpreferredencoding(False)

    def open(self):
        self.json_file = open(file=self.file_path, mode="wt", newline=None, encoding=self.encoding)

    def process_row(self, line):
        json_line = json.dumps(line)
        self.json_file.write(json_line + "\n")
        self.current_row += 1

    def close(self):
        self.json_file.close()
