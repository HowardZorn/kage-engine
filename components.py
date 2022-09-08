
class Components:
    '''
        class `Component` refers to Buhin(部品) in the original implementation.
    '''
    def __init__(self, ignore_version = False) -> None:
        self.hash = dict()
        self.ignore_version = ignore_version

    def search(self, name: str) -> str:
        if name in self.hash:
            return self.hash[name]
        elif self.ignore_version:
            if '@' in name:
                name = name[0:name.find('@')]
                if name in self.hash:
                    return self.hash[name]
                else:
                    return ""
        else:
            return ""

    def push(self, name: str, data: str):
        self.hash[name] = data
    
    set = push
