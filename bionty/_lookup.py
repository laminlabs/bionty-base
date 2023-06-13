# Modified from: https://stackoverflow.com/a/32107024
class Lookup(dict):
    """Lookup object with dot and [] access."""

    def __init__(self, *args, **kwargs):
        super(Lookup, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Lookup, self).__setitem__(key, value)
        self.__dict__.update({key: value})
