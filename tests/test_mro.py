class FooBaseline:
    def __init__(self):
        print("FooBaseline ctor")
        
    def foo(self):
        return "BASE_FOO"
    
    def bar(self):
        return "BASE_BAR"
    

class FooMixin:
    def __init__(self):
        print("FooMixin ctor")
        
    def bar(self):
        return "MIXIN_BAR"

class FooThing(FooMixin, FooBaseline):
    ""
    def __init__(self):
        FooMixin.__init__(self)
        FooBaseline.__init__(self)

    # def bar(self):
    #     return "THING_BAR"

def test_1():
    foo = FooThing()
    assert foo.foo() == "BASE_FOO"
    assert foo.bar() == "MIXIN_BAR"