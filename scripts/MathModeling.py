'''
Programmed by: Kyle Tennison
November 4, 2022

Main Program.
Searches for correlations between two columns of data. Because the data are made 
of both continuous and categorical data, multiple techniques are used. 
Information regarding algorithms can be found in the report.
'''

DEBUG = False

def main() -> None:
    ''' Search for correlations in DATAFILE '''

    from Searcher import Searcher 

    searcher = Searcher()  # Instantiate searcher

    searcher.searchCorrelation()  # Run searches

    # Display Results 
    input("Press enter to display results\n")
    searcher.displayResults()


if __name__ == "__main__": main()