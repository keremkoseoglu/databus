from passenger.abstract_passenger import AbstractPassenger


class DemoPassenger1(AbstractPassenger):
    dataset: str

    def __init__(self):
        self.dataset = "Demo dataset"

    def hello_world(self):
        print("Demo passenger 1 says hello world!")
        print("My dataset is: " + self.dataset)
