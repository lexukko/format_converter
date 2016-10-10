import locale
from plugins.categorias.categorias import PluginReader, PluginWriter
from plugins.dynUI.dynUI import DynDialog


class FixedReaderChunks(PluginReader):
    def __init__(self):
        self.name = "FixedReaderChunks"
        self.version = "1.0"
        self.description = "Plugin de lectura de archivos de ancho fijo por porciones de caracteres"

        self.file_path = None
        self.tamanios = None
        self.encoding = None

        self.line_size = 0
        self.current_row = 0

    def set_config(self):
        # dynamic DynDialog
        dialog = DynDialog()
        dialog.set_tittle("{0} - Setup".format(self.name))
        dialog.add_file("file_path", "Select File:", "Text Files (*.txt *.csv *.dat);;All Files(*.*)",
                        DynDialog.FILE_DIALOG_OPEN)
        dialog.add_line_edit("encoding", "Encoding:", "", "")
        dialog.add_table("tbl",
                        "Field Size",
                         ["Size"],
                         [None]
                         )
        dialog.exec_()
        config = dialog.data_dict
        # set config
        self.file_path = config["file_path"]
        self.tamanios = config["tbl"][0]
        self.line_size = sum(int(field_size) for field_size in self.tamanios)
        if config["encoding"]:
            self.encoding = config["encoding"]
        else:
            self.encoding = locale.getpreferredencoding(False)

    def open(self):
        self.fixed_file = open(file=self.file_path, mode="rt", newline=None, encoding=self.encoding)

    def read(self):
        while True:
            chunk = self.fixed_file.read(self.line_size)
            if not chunk:
                break;

            # -- transform into array
            line_array = []
            init_pos = 0
            for j in range(0, len(self.tamanios)):
                if j == 0:
                    init_pos = 0;
                    end_pos = int(self.tamanios[j])
                else:
                    init_pos = end_pos
                    end_pos = init_pos + int(self.tamanios[j])

                field = chunk[init_pos:end_pos]
                line_array.append(field.strip())

            self.current_row += 1
            yield (line_array)

    def close(self):
        self.fixed_file.close()


class FixedWriterChunks(PluginWriter):
    def __init__(self):
        self.name = "FixedWriterChunks"
        self.version = "1.0"
        self.description = "Plugin de escritura de archivos de ancho fijo por porciones de caracteres"

        self.file_path = None
        self.tamanios = None
        self.orientations = None
        self.encoding = None

        self.current_row = 0

    def set_config(self):
        # dynamic DynDialog
        dialog = DynDialog()
        dialog.set_tittle("{0} - Setup".format(self.name))
        dialog.add_file("file_path", "Select File:", "Text Files (*.txt *.csv *.dat);;All Files(*.*)",
                        DynDialog.FILE_DIALOG_SAVE)
        dialog.add_line_edit("encoding", "Encoding:", "", "")
        dialog.add_table("tbl",
                        "Field Size & Orientations",
                         ["Size", "Orientation"],
                         [
                            None,
                            {"Rigth": "r", "Left": "l"}
                        ]
                         )
        dialog.exec_()
        config = dialog.data_dict
        # set config
        self.file_path = config["file_path"]
        self.tamanios = config["tbl"][0]
        self.orientations = config["tbl"][1]
        if config["encoding"]:
            self.encoding = config["encoding"]
        else:
            self.encoding = locale.getpreferredencoding(False)

    def open(self):
        self.fixed_file = open(file=self.file_path, mode="wt", newline=None, encoding=self.encoding)

    def write(self, line):
        line_fixed = ""
        for j in range(0, len(self.tamanios)):
            if self.orientations[j] == "l":
                line_fixed = line_fixed + line[j].ljust(int(self.tamanios[j]), " ")
            else:
                line_fixed = line_fixed + line[j].rjust(int(self.tamanios[j]), " ")

        self.fixed_file.write(line_fixed)
        self.current_row += 1

    def close(self):
        self.fixed_file.close()
