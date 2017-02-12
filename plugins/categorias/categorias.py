""" Clase base para plugins de lectura """


class PluginReader(object):
    def set_config(self):
        pass

    def get_header(self):
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

    def set_header(self):
        pass

    def open(self):
        pass

    def write(self, line):
        pass

    def close(self):
        pass
