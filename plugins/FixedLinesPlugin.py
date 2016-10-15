from plugins.categorias.categorias import PluginReader, PluginWriter
from plugins.dynUI.dynUI import DynDialog
from plugins.utils import python_encodings


class FixedReaderLines(PluginReader):
    def __init__(self):
        self.name = "FixedReaderLines"
        self.version = "1.0"
        self.description = "Plugin de lectura de archivos de ancho fijo por lineas"

        self.file_path = None
        self.tamanios = None
        self.encoding = None

        self.current_row = 0

    def set_config(self):
        # dynamic DynDialog
        dialog = DynDialog()
        dialog.set_tittle("{0} - Setup".format(self.name))
        dialog.add_file("file_path", "Select File:", "Text Files (*.txt *.csv *.dat);;All Files(*.*)",
                        DynDialog.FILE_DIALOG_OPEN)
        dialog.add_combo_box("encoding", "Encoding:", python_encodings, "utf_8")
        dialog.add_table("tbl",
                        "Field Size",
                         ["Size"],
                         [None]
                         )
        res = dialog.exec_()
        # set config
        if res == DynDialog.Accepted:
            config = dialog.data_dict
            self.file_path = config["file_path"]
            self.tamanios = config["tbl"][0]
            self.encoding = config["encoding"]

    def open(self):
        self.fixed_file = open(file=self.file_path, mode="rt", newline=None, encoding=self.encoding)

    def read(self):
        for line in self.fixed_file:

            # -- remove enter and carriage return
            line_fix = line.replace(chr(10), "")
            line_fix = line_fix.replace(chr(13), "")

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

                field = line_fix[init_pos:end_pos]
                line_array.append(field.strip())

            self.current_row += 1
            yield (line_array)

    def close(self):
        self.fixed_file.close()


class FixedWriterLines(PluginWriter):
    def __init__(self):
        self.name = "FixedWriterLines"
        self.version = "1.0"
        self.description = "Plugin de escritura de archivos de ancho fijo por lineas"

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
        dialog.add_combo_box("encoding", "Encoding:", python_encodings, "utf_8")
        dialog.add_table("tbl",
                        "Field Size & Orientations",
                         ["Size", "Orientation"],
                         [
                            None,
                            {"Rigth": "r", "Left": "l"}
                        ]
                         )
        res = dialog.exec_()
        # set config
        if res == DynDialog.Accepted:
            config = dialog.data_dict
            self.file_path = config["file_path"]
            self.tamanios = config["tbl"][0]
            self.orientations = config["tbl"][1]
            self.encoding = config["encoding"]

    def open(self):
        self.fixed_file = open(file=self.file_path, mode="wt", newline=None, encoding=self.encoding)

    def write(self, line):
        line_fixed = ""
        for j in range(0, len(self.tamanios)):
            if self.orientations[j] == "l":
                line_fixed = line_fixed + line[j].ljust(int(self.tamanios[j]), " ")
            else:
                line_fixed = line_fixed + line[j].rjust(int(self.tamanios[j]), " ")

        self.fixed_file.write(line_fixed + "\n")
        self.current_row += 1

    def close(self):
        self.fixed_file.close()
