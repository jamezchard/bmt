def foo(pos, *, forcenamed):
    print(pos, forcenamed)

foo(10, 20, 30, forcenamed=30)
