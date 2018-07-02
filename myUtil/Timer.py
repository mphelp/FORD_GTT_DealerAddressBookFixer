import time
class Timer:
    """Simple Timer class to record execution time of program processes"""
    # Create timer
    def __init__(self):
        self.section = ''
        pass
    # Start timer
    def start(self):
        self.counter = time.clock()
        self.section = ''
    def start(self, section):
        self.counter = time.clock()
        self.section = section
    # End timer and print to display
    def end(self):
        print('{0} took {1:0.5f} seconds'.format(self.section, time.clock() - self.counter))
