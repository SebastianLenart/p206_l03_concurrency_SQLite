class SomethingWrong(Exception):
    def __init__(self, text):
        print(text)