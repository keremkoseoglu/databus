from passenger.abstract_passenger import AbstractPassenger


class DemoPassenger(AbstractPassenger):
    def __init__(self):
        pass

    def hello_world(self):
        print("Demo passenger says hello world!")
