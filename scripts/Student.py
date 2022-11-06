'''
Kyle Tennison
November 1, 2022

Student Object: Stores data attributes for each student
'''

from constants import *
from tools import *

class Student:
    def __init__(self, raw):
        self.raw = raw
        self.fields = self._create_fields(raw)
        self.dict = self._create_dict(self.fields)

    @staticmethod
    def _create_dict(fields):
        '''
        Map field headers to values
        Pre:
          fields (list) - List containing student fields (ordered)
        Post:
          (dict)        - Dict containing str keys to field values.
        '''

        d = {} 
        for i in range(len(FIELD_HEADERS)): 
            d[FIELD_HEADERS[i]] = fields[i]

        return d

    def get_field(self, field, d=None):
        '''
        Get a field from the student dictionary.
        Pre:
          field (str)   - Key name to search for
          d (any)       - Return value if key not found
          '''
        try:
            return self.dict[field]
        except:
            log(f"No field {field} in student {self.fields[0]}")
            log(self.dict)
        return d
        

    @staticmethod
    def _create_fields(raw):
        '''
        Get student fields as list. Validate that raw data is valid.
        Pre:
          raw (str) - String format of CSV row
        Post:
          (list)    - List containing fields (any)
        '''
        # Get list
        fields = raw.split(",")
        
        # Validate Fields
        if len(fields) != len(FIELD_HEADERS):
            raise ValueError("Student data invalid")
        for index in fields:
          if not index.replace('-','').isnumeric():
            sid = fields[0]
            raise ValueError(f"Student {sid} contains nonnumeric data: {index}")


        # Convert numeric to numeric
        return [int(i) for i in fields]
