""" Clase base para plugins de lectura """


class PluginReader(object):
    def set_config(self):
        pass

    def open(self):
        pass

    def read(self):
        pass

    def close(self):
        pass


""" Clase base para plugins de escritura """


class PluginWriter(object):
    def set_config(self):
        pass

    def open(self):
        pass

    def process_row(self):
        pass

    def close(self):
        pass
