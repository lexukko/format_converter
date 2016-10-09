from plugins.categorias.categorias import PluginReader, PluginWriter
from livetribe.plugins import collect_plugin_classes


class PluginManager:
    def __init__(self):
        self.plugins_classes = {}
        self.plugins_info = {}

    def load_plugins(self, namespace, subclasses, recurse):
        self.plugins_classes = {}
        self.plugins_info = {}
        for plug_class in collect_plugin_classes(namespace=namespace, subclasses_of=subclasses, recurse=recurse):
            # dummy instance
            obj = plug_class()
            # save plug class
            self.plugins_classes[obj.name] = plug_class
            # save plug info
            self.plugins_info[obj.name] = {"version": obj.version, "description": obj.description}

    def getNamesByClass(self, plug_class):
        plug_names = []
        for k, v in self.plugins_classes.items():
            if isinstance(v(), plug_class):
                plug_names.append(k)
        return plug_names

    def getClassByName(self, plugin_name):
        return self.plugins_classes[plugin_name]
