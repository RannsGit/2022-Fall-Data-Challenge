'''
Kyle Tennison
November 6, 2022

Match Class:
Store the names and basic info on two matching fields.
'''

class Match:

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
                    f"{self.f1} and {self.f2} regression.")
        else:
            rounded = round(self.sig * 100, 0)
            return (f"{rounded}% change between "
                    f"{self.f1} and {self.f2}")