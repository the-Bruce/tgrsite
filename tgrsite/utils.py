class PermsError:
    val = False

    @classmethod
    def suppress(cls):
        cls.val = True

    def __bool__(self):
        return self.val
