"""modules imports
"""

class deprecated_param:
    def __init__(self, deprecated_args, version, reason):
        self.deprecated_args = set(deprecated_args.split())
        self.version = version
        self.reason = reason

    def __call__(self, callable):
        def wrapper(*args, **kwargs):
            found = self.deprecated_args.intersection(kwargs)
            if found:
                raise TypeError("Parameter(s) %s deprecated since version %s; %s" % (
                    ', '.join(map("'{}'".format, found)), self.version, self.reason))
            return callable(*args, **kwargs)
        return wrapper
