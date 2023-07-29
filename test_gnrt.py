def itertest(early_return=True):
    if early_return:
        return "hello early return"
    for i in range(10):
        yield f"{i} is running"


gnrt = itertest(False)
gnrt2 = itertest(True)
print(gnrt.__next__())
gnrt2.__next__()
