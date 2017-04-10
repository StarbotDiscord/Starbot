class command():
    def __init__(self, plugin, name, shortdesc='no description', devcommand=False):
        self.plugin = plugin
        self.name = name
        self.shortdesc = shortdesc
        self.devcommand = devcommand