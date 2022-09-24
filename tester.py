
class Person:
    def __init__(self, *args, **kwargs):
        print("." * 20)
        print(kwargs)
        print(args)


p = Person("Paul", kwargs={"name": "Paul"})