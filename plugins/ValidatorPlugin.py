import datetime
import re
from plugins.categorias.categorias import PluginWriter
from plugins.dynUI.dynUI import DynDialog


class PlugValidatorError(Exception):
    def __init__(self, message):
        self.message = message


class ValidateWriter(PluginWriter):
    def __init__(self):
        self.name = "ValidateWriter"
        self.version = "1.0"
        self.description = "Plugin verificador de tipos de dato"

        self.formats = []  # # decimal, #.# flotante, DDMMYYY or DD-MM-YYYY etc..,
        self.allow_nulls = []  # para cada campo True para no evaluar campos nulos o False para evaluarlos [True, True, False]
        self.skip_no = 0

        self.msgErrorLine = None
        self.current_row = 0
        self.current_col = 0

    def set_config(self):
        # dynamic DynDialog
        dialog = DynDialog()
        dialog.set_tittle("{0} - Setup".format(self.name))
        dialog.add_line_edit("skip", "rows skip:", "header rows to skip", "1")
        dialog.add_table("tbl",
                        "Types & Nulls",
                         ["formats", "allow_nulls"],
                         [{
                            'Text': 'NA',
                            'Integer': '#',
                            'Float': '#.#',
                            'Date: DD-MM-YYYY ': 'DD-MM-YYYY',
                            'Date: DD/MM/YYYY ': 'DD/MM/YYYY',
                            'Date: DD MM YYYY': 'DD MM YYYY',
                            'Date: YYYY-MM-DD': 'YYYY-MM-DD',
                            'Date: YYYY/MM/DD': 'YYYY/MM/DD',
                            'Date: YYYY MM DD': 'YYYY MM DD',
                            'Date: DDMMYYYY': 'DDMMYYYY',
                            'Date: YYYYMMDD': 'YYYYMMDD'
                        },
                            True
                        ]
                         )
        dialog.exec_()
        config = dialog.data_dict
        # set config
        self.formats = config["tbl"][0]
        self.allow_nulls = config["tbl"][1]
        self.skip_no = int(config["skip"])

    def open(self):
        pass

    def write(self, line):
        self.current_row += 1
        if self.current_row > self.skip_no:
            if not self.is_valid_row(line):
                raise PlugValidatorError(
                    "ERROR: Linea {0}, Columna {1}, Msg: {2}".format(self.current_row, self.current_col,
                                                                     self.msgErrorLine))
        return line

    def close(self):
        pass

    # ---------------------------------------------------------------------------------------------------------------------------
    # -- funciones auxiliares
    # ---------------------------------------------------------------------------------------------------------------------------

    def is_int(self, int_str):
        int_regex = re.compile("^[-]?\d+$")
        return int_regex.match(int_str) is not None

    def is_dec(self, dec_str):
        dec_regex = re.compile("(^[-]?[0-9]{1,}[.]{1}[0-9]{1,}$)|(^[-]?[.]{1}[0-9]{1,}$)")
        return dec_regex.match(dec_str) is not None

    def is_date(self, date_str, date_format):
        try:
            if date_format == 'DD-MM-YYYY' or date_format == 'DD/MM/YYYY' or date_format == 'DD MM YYYY':
                return datetime.date(day=int(date_str[0:2]), month=int(date_str[3:3 + 2]),
                                     year=int(date_str[6:6 + 4])) is not None
            elif date_format == 'YYYY-MM-DD' or date_format == 'YYYY/MM/DD' or date_format == 'YYYY MM DD':
                return datetime.date(year=int(date_str[0:4]), month=int(date_str[5:5 + 2]),
                                     day=int(date_str[8:8 + 2])) is not None
            elif date_format == 'DDMMYYYY':
                return datetime.date(day=int(date_str[0:2]), month=int(date_str[2:2 + 2]),
                                     year=int(date_str[4:4 + 4])) is not None
            elif date_format == 'YYYYMMDD':
                return datetime.date(year=int(date_str[0:4]), month=int(date_str[4:4 + 2]),
                                     day=int(date_str[6:6 + 2])) is not None
        except ValueError:
            return False
        return False

    def is_valid_row(self, row):

        self.current_col = 0
        self.msgErrorLine = None

        if not len(row) == len(self.formats) and len(self.formats) == len(self.allow_nulls):
            self.msgErrorLine = "Longitudes de campos, formatos y nulos no coincide."
            return False

        for field, format, allow_nulls in zip(row, self.formats, self.allow_nulls):

            self.current_col += 1

            if field == '' and not allow_nulls:
                self.msgErrorLine = "no acepta nulos."
                return False

            if format == "#":
                if not self.is_int(field):
                    self.msgErrorLine = "entero invalido."
                    return False
            elif format == "#.#":
                if not self.is_dec(field):
                    self.msgErrorLine = "decimal invalido."
                    return False
            elif format == "NA":
                pass
            else:
                if not self.is_date(field, format):
                    self.msgErrorLine = "fecha invalida."
                    return False
        return True
