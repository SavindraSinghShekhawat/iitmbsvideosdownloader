class _Site:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    def __eq__(self, other):
        return (self.name == other.name) and (self.url == other.url)


Y2MATE = _Site("y2mate", "https://www.y2mate.com/")
Y2META = _Site("y2meta", "https://y2meta.app/")
