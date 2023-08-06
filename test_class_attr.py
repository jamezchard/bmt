class test_class:
    s = "s of class"

    def __init__(self) -> None:
        self.s = "s of instance"
        pass

    def change_s(self):
        self.s = "s of instance changed"

    @classmethod
    def change_cs(cls):
        cls.s = "s of class changed"


t = test_class()
t2 = test_class()
# test_class.change_cs()
t.change_s()
print(t.s)
print(t2.s)
test_class.change_cs()
print(test_class.s)
print(test_class.__dict__)
print(t.__dict__)
