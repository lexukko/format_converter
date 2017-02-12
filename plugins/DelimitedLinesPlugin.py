import csv
from plugins.categorias.categorias import PluginReader, PluginWriter
from plugins.dynUI.dynUI import DynDialog
from plugins.utils import python_encodings


class DelimitedReaderLines(PluginReader):
    def __init__(self):
        self.name = "DelimitedReaderLines"
        self.version = "1.0"
        self.description = "Plugin de lectura de archivos delimitados"

        self.file_path = None
        self.skip = None
        self.delimiter = None
        self.quotechar = None
        self.encoding = None

        self.current_row = 0

    def set_config(self):
        # dynamic DynDialog
        dialog = DynDialog()
        dialog.set_tittle("{0} - Setup".format(self.name))
        dialog.add_file("file_path", "Select File:", "Text Files (*.txt *.csv *.dat);;All Files(*.*)",
                        DynDialog.FILE_DIALOG_OPEN, self.file_path)
        dialog.add_line_edit("skip", "Skip lines:", "", self.skip)                
        dialog.add_line_edit("delimiter", "Delimiter:", "", self.delimiter)
        dialog.add_line_edit("quotechar", "Quote Char:", "", self.quotechar)
        dialog.add_combo_box("encoding", "Encoding:", python_encodings, "utf_8" if self.encoding is None else self.encoding )
        res = dialog.exec_()
        # set config
        if res == DynDialog.Accepted:
            config = dialog.data_dict
            self.file_path = config["file_path"]
            self.skip = config["skip"]
            self.delimiter = config["delimiter"]
            self.quotechar = config["quotechar"]
            self.encoding = config["encoding"]

    def open(self):
        self.csv_file = open(file=self.file_path, mode="rt", newline="", encoding=self.encoding)
        if self.quotechar:
            self.csv_reader = csv.reader(self.csv_file, delimiter=self.delimiter, quotechar=self.quotechar)
        else:
            self.csv_reader = csv.reader(self.csv_file, delimiter=self.delimiter)
        self.current_row = 0

    def read(self):
        for row in self.csv_reader:
            self.current_row += 1
            if self.current_row > int(self.skip):
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
        dialog.add_combo_box("encoding", "Encoding:", python_encodings, "utf_8")
        res = dialog.exec_()
        # set config
        if res == DynDialog.Accepted:
            config = dialog.data_dict
            self.file_path = config["file_path"]
            self.delimiter = config["delimiter"]
            self.quotechar = config["quotechar"]
            self.encoding = config["encoding"]

    def open(self):
        self.csv_file = open(file=self.file_path, mode="wt", newline="", encoding=self.encoding)
        self.csv_writer = csv.writer(self.csv_file, delimiter=self.delimiter, quotechar=self.quotechar,
                                     quoting=csv.QUOTE_MINIMAL)

    def write(self, line):
        self.csv_writer.writerow(line)
        self.current_row += 1

    def close(self):
        self.csv_file.close()
