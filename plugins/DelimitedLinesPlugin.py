import csv
import locale
from plugins.categorias.categorias import PluginReader, PluginWriter
from plugins.dynUI.dynUI import DynDialog


class DelimitedReaderLines(PluginReader):
    def __init__(self):
        self.name = "DelimitedReaderLines"
        self.version = "1.0"
        self.description = "Plugin de lectura de archivos delimitados"

        self.file_path = None
        self.delimiter = None
        self.quotechar = None
        self.encoding = None

        self.current_row = 0

    def set_config(self):
        # dynamic DynDialog
        dialog = DynDialog()
        dialog.set_tittle("{0} - Setup".format(self.name))
        dialog.add_file("file_path", "Select File:", "Text Files (*.txt *.csv *.dat);;All Files(*.*)",
                        DynDialog.FILE_DIALOG_OPEN)
        dialog.add_line_edit("delimiter", "Delimiter:", "", "")
        dialog.add_line_edit("quotechar", "Quote Char:", "", "")
        dialog.add_line_edit("encoding", "Encoding:", "", "")
        dialog.exec_()
        config = dialog.data_dict
        # set config
        self.file_path = config["file_path"]
        self.delimiter = config["delimiter"]
        self.quotechar = config["quotechar"]
        if config["encoding"]:
            self.encoding = config["encoding"]
        else:
            self.encoding = locale.getpreferredencoding(False)

    def open(self):
        self.csv_file = open(file=self.file_path, mode="rt", newline="", encoding=self.encoding)
        self.csv_reader = csv.reader(self.csv_file, delimiter=self.delimiter, quotechar=self.quotechar)

    def read(self):
        for row in self.csv_reader:
            self.current_row += 1
            yield (row)

    def close(self):
        self.csv_file.close()


class DelimitedWriterLines(PluginWriter):
    def __init__(self):
        self.name = "DelimitedWriterLines"
        self.version = "1.0"
        self.description = "Plugin de escritura de archivos delimitados"

        self.file_path = None
        self.delimiter = None
        self.quotechar = None
        self.encoding = None

        self.current_row = 0

    def set_config(self):
        # dynamic DynDialog
        dialog = DynDialog()
        dialog.set_tittle("{0} - Setup".format(self.name))
        dialog.add_file("file_path", "Select File:", "Text Files (*.txt *.csv *.dat);;All Files(*.*)",
                        DynDialog.FILE_DIALOG_SAVE)
        dialog.add_line_edit("delimiter", "Delimiter:", "", "")
        dialog.add_line_edit("quotechar", "Quote Char:", "", "")
        dialog.add_line_edit("encoding", "Encoding:", "", "")
        dialog.exec_()
        config = dialog.data_dict
        # set config
        self.file_path = config["file_path"]
        self.delimiter = config["delimiter"]
        self.quotechar = config["quotechar"]
        if config["encoding"]:
            self.encoding = config["encoding"]
        else:
            self.encoding = locale.getpreferredencoding(False)

    def open(self):
        self.csv_file = open(file=self.file_path, mode="wt", newline="", encoding=self.encoding)
        self.csv_writer = csv.writer(self.csv_file, delimiter=self.delimiter, quotechar=self.quotechar,
                                     quoting=csv.QUOTE_MINIMAL)

    def write(self, line):
        self.csv_writer.writerow(line)
        self.current_row += 1

    def close(self):
        self.csv_file.close()
