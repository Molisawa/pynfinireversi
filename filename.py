# Singleton class to store the filename and the text in the file
class Filename():
    def __init__(self):
        self._filename = None
        self.text = ""
        self.num_of_chars = 0



    def get_instance(self):
        if self._filename is None:
            self._filename = Filename()
        return self._filename

