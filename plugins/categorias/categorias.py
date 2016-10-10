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

""" Clase de procesamiento de informacion """


class PluginProcess(object):
    def set_config(self):
        pass

    def process(self):
        pass

    def show_results(self):
        pass

""" Clase base para plugins de escritura """


class PluginWriter(object):
    def set_config(self):
        pass

    def open(self):
        pass

    def write(self):
        pass

    def close(self):
        pass
