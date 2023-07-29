class test_class(test_attr="lava"):
    s = "s of class"

    def __init__(self) -> None:
        # self.s = "s of instance"
        print(self.test_attr)
        pass

    def change_s(self):
        self.s = "s of instance changed"

    @classmethod
    def change_cs(cls):
        cls.s = "s of class changed"


t = test_class()
# test_class.change_cs()
# t.change_s()
print(t.s)
print(test_class.s)
