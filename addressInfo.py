class addressInfo:
    """A simple class detailing stats on the addresses read ===
        Keeps track of address info AND writes to the results
        file specified, no parsing in this class"""

    # Constructor
    def __init__(self,resultsFile='results.txt', hasOffset=True):
        self.hasOffset = hasOffset
        self.resultsFile = resultsFile
        self.badAddress = 0
        self.goodAddress = 0
        if hasOffset:
            self.currentAddrIndex = 4
        else:
            self.currentAddrIndex = 0
        self.resultsStream = open(resultsFile, 'w')


    # Write no city to results file
    def writeNoCity(self):
        self.badAddress = self.badAddress + 1
        self.resultsStream.write('\n')

    # Write city to results file
    def writeCity(self, city):
        self.goodAddress = self.goodAddress + 1
        self.resultsStream.write(city + '\n')

    # increment addr index
    def incrCurrentIndex(self):
        self.currentAddrIndex = self.currentAddrIndex + 1

    # display resulting good and bad address counts
    def dispCityResults(self):
        print('\nTotal: {}'.format(self.goodAddress + self.badAddress))
        print('Good:  {}'.format(self.goodAddress))
        print('Bad:   {}'.format(self.badAddress))
        print('Ratio: {}\n\n'.format(self.goodAddress / (self.goodAddress + self.badAddress)))
        print('All cities identified have been written to results.txt')
        print('All invalid addresses have a blank line instead')
