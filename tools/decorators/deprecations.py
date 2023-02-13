"""modules imports
"""

class deprecated_param:
    def __init__(self, deprecated_args, deprecated_args_positions, version, reason):
        self.deprecated_args = set(deprecated_args.split())
        self.deprecated_args_positions = set(deprecated_args_positions.split())
        self.version = version
        self.reason = reason

    def __call__(self, callable):
        # print("call deprecation")
        def wrapper(*args, **kwargs):
            # print("wrapp deprecation")
            # print("deprecated args", self.deprecated_args)
            # print("args", args)
            # print("kwargs", kwargs)
            found = self.deprecated_args.intersection(kwargs)
            if found:
                raise TypeError(f"Parameter(s) {found} deprecated since version\
                                 {self.version}; {self.reason}")
            for pos in self.deprecated_args_positions:
                if int(pos) < len(args):
                    found = pos
                    raise TypeError(
                        f"Parameter(s) in position {found} deprecated since version\
                              {self.version}; {self.reason}"
                    )
            return callable(*args, **kwargs)
        return wrapper
