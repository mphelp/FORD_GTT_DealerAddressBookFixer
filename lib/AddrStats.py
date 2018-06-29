class AddrStats:
    """A simple class detailing stats on the read addresses ...
        Keeps track of address info AND writes to the results
        file specified, no parsing in this class"""

    # Constructor
    def __init__(self, resultsFile='results.txt', hasOffset=True, debug=False, debugAll=False):
        self.hasOffset = hasOffset          # excel offset
        self.resultsFile = resultsFile      # city write file
        self.badAddress = 0                 # count of bad address strings
        self.goodAddress = 0                # count of good address strings
        if hasOffset:
            self.currentAddrIndex = 4
        else:
            self.currentAddrIndex = 0
        self.resultsStream = open(resultsFile, 'w') # write stream
        self.debug = debug
        self.debugAll = debugAll

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

    # a print function for debugging
    def debugPrint(self, addrElements, distr='NO_District', key='NoKEY',correctCity=''):
        if self.debugAll or (self.debug and key == 'noValidCity' or key == 'tooShort'):
            if isinstance(addrElements, list):
                print(self.currentAddrIndex, distr, correctCity, key + '\t: ', " ".join(addrElements))
            else:
                print(self.currentAddrIndex, distr, key + '\t: ', correctCity, addrElements)

    # display resulting good and bad address counts
    def dispCityResults(self):
        print('\nTotal: {}'.format(self.goodAddress + self.badAddress))
        print('Good:  {}'.format(self.goodAddress))
        print('Bad:   {}'.format(self.badAddress))
        print('Ratio: {}\n'.format(self.goodAddress / (self.goodAddress + self.badAddress)))
        print(f'All cities identified have been written to {self.resultsFile}')
        print('All invalid addresses have a blank line instead')
