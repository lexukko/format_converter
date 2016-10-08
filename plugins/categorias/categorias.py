""" Clase base para plugins de lectura """


class IPlugin_Reader(object):
    def set_config(self):
        pass

    def open(self):
        pass

    def read(self):
        pass

    def close(self):
        pass


""" Clase base para plugins de escritura """


class IPlugin_Writer(object):
    def set_config(self):
        pass

    def open(self):
        pass

    def process_row(self):
        pass

    def close(self):
        pass
