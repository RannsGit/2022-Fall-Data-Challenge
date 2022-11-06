'''
Kyle Tennison
November 4, 2022

Searcher Object: Computers variable matches and searches for continuous
    and categorical correlation. Returns significant r-values for continuous
    in out.txt. Returns series of csv-format heatmap (and their expected 
    values) in WRITEDIR (defined in constants.py) directory. 

'''

from collections import defaultdict
import copy
import subprocess
import scipy.stats
from constants import *
from Student import Student
from tools import *

class Match:
    '''Store the names and basic info on two matching variables.'''

    def __init__(self, f1, f2, sig, isCont) -> None:
        self.f1 = f1 
        self.f2 = f2 
        self.sig = sig
        self.isCont = isCont
        self.sortIndex = sig + 100 if isCont else -100

    def __str__(self) -> str:
        if self.isCont:
            rounded = round((self.sig/0.5), 5)
            return (f"r={rounded} for "
                    f"{self.f1} and {self.f2} regression line.")
        else:
            rounded = round(self.sig * 100, 0)
            return (f"{rounded}% change between "
                    f"{self.f1} and {self.f2} estimated & expected.")


class Searcher:

    ALPHA = 0.1

    def __init__(self) -> None:

        # Run tools setup for misc environment setup
        setup()

        log("Searcher init")
        self.students = []

        # Read Students from CSV lines
        invalidCount = 0
        with open(DATAFILE, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                try:
                    self.students.append(Student(line))
                except ValueError as e:
                    # Catch invalid students
                    print("Invalid student:", e)
                    invalidCount += 1

        color = red if invalidCount > 0 else green
        log(color("Student objects created with "
                 f"{invalidCount} invalid student(s)."))

        self.matches = []

    @classmethod
    def linearCorrelation(cls, _x: list, _y: list):
        '''
        Checks for linear correlation between two fields
        Pre:
          x (iter)  - X axis points
          y (inter) - Y axis points
        '''

        r, p = scipy.stats.pearsonr(_x, _y)
        return r

    @staticmethod
    def _match_fields(isCont) -> list:
        '''
        Get pairs of matching fields to search for correlation
        Pre:
          isCont (bool) - Use continuous headers? False = categorical headers
        Post:
          list of tuples. Each tuple has two matching codes (str).
        '''
        out = []

        # Copy header contents
        headerCopy = [] 
        if isCont: 
            # Get continuous headers
            headerCopy = copy.deepcopy(CONTINUOUS_HEADERS)
        else:
            # Get categorical headers
            headerCopy = copy.deepcopy(FIELD_HEADERS)
            [headerCopy.remove(i) for i in CONTINUOUS_HEADERS]

        # Remove conflicting headers
        [headerCopy.remove(i) for i in IGNORE_HEADERS if i in headerCopy]

        # Match different header pairs
        for header in copy.deepcopy(headerCopy):
            del headerCopy[0]
            for headerAdd in headerCopy:
                out.append((header, headerAdd))

        log(f"There are {bold(str(len(out)))} values to be searched")
        return out

    def searchCorrelation(self) -> None:
        '''
        Search every pair of fields for some correlation.
        Pre: 
            Expected file format
        Post: 
            Prints to console current log. Saves matches in self.matches
        '''
        # self.students reference; easier to read
        s = self.students

        # ~~ Search Continuous Data ~~

        # Get matching continuous Fields
        cpairs = self._match_fields(isCont=True)
        log("Got matching fields.\n")

        log('', end='')  # Add header for input
        input("Press enter to search continuous data > ")
        log("Searching Continuous Fields... ")
        for f1, f2 in cpairs:
            # Get Fields 
            x = [i.get_field(f1, d=0) for i in s]
            y = [i.get_field(f2, d=0) for i in s]

            # Search columns
            self._continuous_search(f1, f2, x, y)
        
        log(green( "Done searching continuous data. "
                  f"{len(self.matches)} matches"))

        # ~~ Search Binary Data ~~
        log("\n" + (20 * "~") + "\n", hasHeader=False)
        bpairs = self._match_fields(isCont=False)
        log("Got matching fields.\n")

        log('', end='')  # Add header for input
        input("Press enter to search binary > ")
        log("Searching Binary Fields... ")

        for f1, f2 in bpairs:
            # Get Fields 
            x = [i.get_field(f1, d=0) for i in s]
            y = [i.get_field(f2, d=0) for i in s]

            # Create container dict from lists
            containerDict = defaultdict(list)
            for i in range(len(x)):
                containerDict[x[i]].append(y[i])

            # Search columns
            self._categorical_search(f1, f2, x, y, containerDict)

        cmatches = len([i for i in self.matches if not i.isCont])
        log(green( "Done searching categorical data. "
                  f"{cmatches} matches\n"))

        log("Search complete.")        

        # Sort matches once done
        self._sort_matched()

        


    def _continuous_search(self, fx, fy, x, y):
        '''
        Create regression line and check r^2 for correlation significance
        Pre:
          fx (str)      - Code for x list
          fy (str)      - Code for y list
          x (list)      - Contains values for fx header (pairs to y)
          y (list)      - Contains values for fy header (pairs to x) 
        '''
        # Check for correlation
        r = self.linearCorrelation(x, y)

        # Add correlated pairs to list
        isCorrelation = False
        if abs(r) > 0.1: 
            self.matches.append(
                Match(fx, fy, r, True)
                )
            isCorrelation = True

        if DEBUG:
            log(
                f"Searching {(fx + ' &' + fy + ':'):<20}\t"\
                + (green("FOUND CORRELATION  ") if isCorrelation \
                    else red("No Correlation     "))+ \
                f"R-Value is: {r}"
                    )
    
    def _categorical_search(self, fx, fy, x, y, rawDict) -> None:
        '''
        Create table which contains relationships between codes.
        Pre:
          fx (str)      - Code for x list
          fy (str)      - Code for y list
          x (list)      - Contains values for fx header (pairs to y)
          y (list)      - Contains values for fy header (pairs to x)
          rawDict (dict)- Dictionary containing {CODE : [MATCHING]}
          
        Post:
          Write matching csv files to 
          '''

        SIG_THRESHOLD = 0.40  # Percent threshold 
        MIN_RESPONSE = 10  # Minimum response count before ignoring (X-Axis)

        # -- Sort rawDict --
        rawDict = dict(sorted(rawDict.items()))


        # -- Find Sums of Answers -- 

        sumDict = {}
        ''' sumDict format:
        {
            X-Value : {
                Y-Value : Count, ...
            }, ...
        }
        '''

        xIgnore = [-1]

        for ix in rawDict:
            
            # Ignore -1 rows
            if ix in xIgnore:
                continue

            # Get sums
            ycounter = defaultdict(int)
            for iy in rawDict[ix]:

                if iy == -1:
                    continue
                
                ycounter[iy] += 1

            # Calculate X size
            total = 0
            for value in ycounter.values():
                total += value

            # Only add if larger than minimum
            if total > MIN_RESPONSE:
                sumDict[ix] = dict(ycounter)
            else:
                xIgnore.append(ix)
        
        # -- Get proportions from sums --

        proportions = {}
        '''
        proportions format:
        {
            X-Value : {
                Y-Value : Proportion (percent), ...
            }, ...
        }
        '''
        ly = len(y)
        for ix in sumDict:

            # Store each X-Value's dict temporarily
            tmpPropDict = defaultdict(int)

            # Get sum for each Y-Value
            for key in sumDict[ix]:
                value = sumDict[ix][key] / \
                        len([i for i in rawDict[ix] if i != -1])
                tmpPropDict[key] = value 

            # Add to proportion dict
            proportions[ix] = dict(tmpPropDict)

        # -- Get expected values --

        expected = {} 
        '''
        expected format:
        {
            Y-Value : Expected, ...
        }'''

        # Count instances of each value
        ycounter = defaultdict(int)
   
        for i in [i for i in y if i != -1]:
            if y != -1:
                ycounter[i] += 1

        # Convert to expected proportions
        for key, value in ycounter.items():
            expected[key] = value/ly        

        # Cleanup ycounter dict
        del ycounter

        # -- Validate Table --
        isValid = False 
        significance = 0
        mostSignificant = 0

        # Loop through proportion sub-dictionaries
        for ix in proportions:

            ydict = proportions[ix]

            # Loop though y proportions
            for key in ydict:
                # Compare actual to expected
                actual  = ydict[key]
                projected = expected[key]
                significance = abs(actual - projected)

                if significance > SIG_THRESHOLD:
                    isValid = True
                    if significance > mostSignificant:
                        mostSignificant = significance
        
        if DEBUG: log(
            f"Searching {(fx + ' & ' + fy) :<30}" + 
            (green("FOUND CORRELATION   ") if isValid else \
             red("No Correlation      ")) + \
            (warn(str(xIgnore)))
            
             )

        # -- Make a table if valid -- 
        if isValid:

            # Add to matches
            self.matches.append(Match(fx, fy, sig=mostSignificant, isCont=False))
            
            # Make spreadsheet
            sigString = str(round(mostSignificant * 100, 2))
            filename = f"{WRITEDIR}/{sigString} - {fx} vs {fy}.csv"
            subprocess.Popen(["touch", filename])
            with open(filename, 'w') as f:
                # Write Descriptions
                f.write(
                    f"{fx}, A: {HEADER_DESCRIPTIONS[fx]}\n"
                    f"{fy}, B: {HEADER_DESCRIPTIONS[fy]}\n\n"
                    )

                # Write headers
                header = "  ,"
                expected = dict(sorted(expected.items()))
                for i in expected: header += f"B{i},"
                for i in expected: header += f"B{i}e,"
                header += "n,"  # Sample size header
                header = header[:-1] + "\n"
                f.write(header)

                # Write values
                for x in proportions:
                    line = ""  # Store current line
                    line += f"A{x},"

                    # Add values to tables
                    for iy in expected:
                        try:
                            line+=f"{round(proportions[x][iy] * 100, 1)}%,"
                        except KeyError:
                            line+="0.0%,"
        
                    # Write expected:
                    for e in expected.values():
                        line += f"{round(e * 100, 1)}%,"
                    
                    # Write sample size
                    n = 0
                    for value in sumDict[x].values():
                        n += value
                        
                    line += f"{n},"

                    line = line[:-1] + "\n"
                    f.write(line)


    def _sort_matched(self) -> None:
        '''
        Sort matched values by r-value.
        Pre:
          searchCorrelation has been run, and matches are stored
          self.matches only includes Match objects
        Post:
          modifies self.matches list
        '''

        self.matches.sort(key=lambda i: i.sortIndex)
        log("Sorted matched results")

    def displayResults(self) -> None:
        '''
        Print search results. Log search results to OUTFILE
        Pre:
          searchCorrelation has been run, and matches are stored
          self.matches only includes Match objects
        Post:
          prints to console
        '''

        out = "Found the following matches: \n"

        for match in self.matches:
            out += (f"\t{match}\n")

        print(out)

        with open(OUTFILE, 'w') as f:
            f.write(out)
