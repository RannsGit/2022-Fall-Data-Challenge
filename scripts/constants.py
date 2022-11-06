'''
Kyle Tennison
November 4, 2022

Configuration and constants for Math Modeling Program
'''

from MathModeling import DEBUG

DATAFILE = "../data.csv"
LOGFILE = "../etc/log.txt"
OUTFILE = "../outputs/correlations.txt"
WRITEDIR = "../outputs/CSV Output"
FIELD_HEADERS = [
    'BASMID','ALLGRADEX','EDCPUB','SCCHOICE','SPUBCHOIX','SCONSIDR','SCHLHRSWK',
    'EINTNET','MOSTIMPT','INTNUM','SEENJOY','SEGRADES','SEABSNT','SEGRADEQ',
    'FSSPORTX','FSVOL','FSMTNG','FSPTMTNG','FSATCNFN','FSFUNDRS','FSCOMMTE',
    'FSCOUNSLR','FSFREQ','FSNOTESX','FSMEMO','FCSCHOOL','FCTEACHR','FCSTDS',
    'FCORDER','FCSUPPRT','FHHOME','FHWKHRS','FHAMOUNT','FHCAMT','FHPLACE',
    'FHCHECKX','FHHELP','FOSTORY2X','FOCRAFTS','FOGAMES','FOBUILDX','FOSPORT'
    ,'FORESPON','FOHISTX','FODINNERX','FOLIBRAYX','FOBOOKSTX','HDHEALTH',
    'CDOBMM','CDOBYY','CSEX','CSPEAKX','HHTOTALXX','RELATION','P1REL','P1SEX'
    ,'P1MRSTA','P1EMPL','P1HRSWK','P1MTHSWRK','P1AGE','P2GUARD','TTLHHINC'
    ,'OWNRNTHB','CHLDNT','SEFUTUREX','DSBLTY','HHPARN19X','HHPARN19_BRD'
    ,'NUMSIBSX','PARGRADEX','RACEETH','INTACC','CENREG','ZIPLOCL'
]
CONTINUOUS_HEADERS = [
"ALLGRADEX", "INTNUM", "FSFREQ", "FHWKHRS", "CDOBMM", "HHTOTALXX", "P1HRSWK", "P1MTHSWRK", 
"P1AGE", "NUMSIBSX", "CDOBYY", "SEGRADES", "SEABSNT", "SCHLHRSWK"]
IGNORE_HEADERS = ["BASMID"]
HEADER_DESCRIPTIONS = {
    'Label ID': ' Description', 
    'BASMID': 'Unique child identifier', 
    'ALLGRADEX': '"What is this child’s current grade, grade equivalent, or year of school "', 
    'EDCPUB': 'Does the child attend a Public school?', 
    'SCCHOICE': 'Did you feel that you had a choice in what school this child attends?', 
    'SPUBCHOIX': 'Does your public school district let you choose which public school you want this child to attend? ', 
    'SCONSIDR': 'Did you consider other schools for this child?', 
    'SCHLHRSWK': 'About how many hours does this child attend a school each week? ', 
    'EINTNET': '"Child enrolled in online, virtual or cyber courses"', 
    'MOSTIMPT': '"Of the reasons that this child is enrolled in online, virtual, or cyber courses, which one would you say is the most important to you? "', 
    'INTNUM': '"How many online, virtual, or cyber courses does this child take?"', 
    'SEENJOY': 'How much do you agree or disagree with the following statement: “This child enjoys school.”', 
    'SEGRADES': '"Please tell us about this child’s grades during this school year. Overall, across all subjects, what grades does this child get? "', 
    'SEABSNT': '"Since the beginning of this school year, how many days has this child been absent from school?"', 
    'SEGRADEQ': 'How would you describe his or her work at school?', 
    'FSSPORTX': '"Since the beginning of this school year, has any adult in this child’s household Attended a school or class event, such as a play, dance, sports event, or science fair"', 
    'FSVOL': '"Since the beginning of this school year, has any adult in this child’s household Serve as a volunteer in this child’s classroom or elsewhere in the school"', 
    'FSMTNG': '"Since the beginning of this school year, has any adult in this child’s household Attended a general school meeting, for example, an open house, or a back-to-school night"', 
    'FSPTMTNG': '"Since the beginning of this school year, has any adult in this child’s household Attended a meeting of the parent-teacher organization or association"', 
    'FSATCNFN': '"Since the beginning of this school year, has any adult in this child’s household Gone to a regularly scheduled parent-teacher conference with this child\'s teacher"', 
    'FSFUNDRS': '"Since the beginning of this school year, has any adult in this child’s household Participated in fundraising for the school"', 
    'FSCOMMTE': '"Since the beginning of this school year, has any adult in this child’s household Served on a school committee"', 
    'FSCOUNSLR': '"Since the beginning of this school year, has any adult in this child’s household Met with a guidance counselor in person"', 
    'FSFREQ': '"During this school year, how many times has any adult in the household gone to meetings or participated in activities at this child’s school?"', 
    'FSNOTESX': '"During this school year, has your family received any Notes or emails specifically about this child from his or her teachers or school administrators?"', 
    'FSMEMO': '"During this school year, has your family received any Newsletters, memos, emails, or notices addressed to all parents?"', 
    'FCSCHOOL': 'How satisfied or dissatisfied are you with The school this child attends this year?', 
    'FCTEACHR': 'How satisfied or dissatisfied are you with The teachers this child has this year?', 
    'FCSTDS': 'How satisfied or dissatisfied are you with The academic standards of the school?', 
    'FCORDER': 'How satisfied or dissatisfied are you with The order and discipline at the school?', 
    'FCSUPPRT': 'How satisfied or dissatisfied are you with The way that school staff interacts with parents?', 
    'FHHOME': '"How often does this child do homework at home, at an after-school program, or somewhere else outside of school?"', 
    'FHWKHRS': '"In an average week, how many hours does this child spend on homework outside of school?"', 
    'FHAMOUNT': 'How do you feel about the amount of homework this child is assigned?', 
    'FHCAMT': 'How does this child feel about the amount of homework he or she is assigned?', 
    'FHPLACE': 'Is there a place in your home that is set aside for this child to do homework?', 
    'FHCHECKX': 'How often does any adult in your household check to see that this child’s homework is done?', 
    'FHHELP': '"During this school year, about how many days in an average week does anyone in your household help this child with his or her homework?"', 
    'FOSTORY2X': '"In the past week, has anyone in your family Told him or her a story (Do not include reading to this child.)"', 
    'FOCRAFTS': '"In the past week, has anyone in your family Done activities like arts and crafts, coloring, painting, pasting, or using clay"', 
    'FOGAMES': '"In the past week, has anyone in your family Played board games or did puzzles with him or her"', 
    'FOBUILDX': '"In the past week, has anyone in your family Worked on a project like building, making, or fixing something"', 
    'FOSPORT': '"In the past week, has anyone in your family Played sports, active games, or exercised together"', 
    'FORESPON': '"In the past week, has anyone in your family Discussed with him or her how to manage time"', 
    'FOHISTX': '"In the past week, has anyone in your family Talked with him or her about the family’s history or ethnic heritage"', 
    'FODINNERX': '"In the past week, how many days has your family eaten the evening meal together?"', 
    'FOLIBRAYX': '"In the past month, has anyone in your family done the following things with this child? a. Visited a library"', 
    'FOBOOKSTX': '"In the past month, has anyone in your family done the following things with this child? b. Visited a bookstore"', 
    'HDHEALTH': '"In general, how would you describe this child’s health?"', 
    'CDOBMM': 'In what year was this child born?', 
    'CSEX': 'What is this child’s sex?', 
    'CSPEAKX': 'What language does this child speak most at home?', 
    'HHTOTALXX': '"Including children, how many people live in this household?"', 
    'RELATION': 'How are you related to this child?', 
    'P1REL': 'Relation of first parent/guardian to child', 
    'P1SEX': 'First parent/guardian sex', 
    'P1MRSTA': 'First parent/guardian marital status', 
    'P1EMPL': 'First parent/guardian employment status', 
    'P1HRSWK': 'First parent/guardian hours worked per week', 
    'P1MTHSWRK': '"In the past 12 months, how many months (if any) has this parent or guardian worked for pay or income?"', 
    'P1AGE': 'First parent/guardian age', 
    'P2GUARD': 'Is there a second parent or guardian living in this household?', 
    'TTLHHINC': 'Which category best fits the total income of all persons in your household over the past 12 months?', 
    'OWNRNTHB': 'Own/rent house', 
    'CHLDNT': 'How often does this child use the Internet at home for learning activities?', 
    'SEFUTUREX': 'How far do you expect this child to go in his or her education?', 
    'DSBLTY': 'Child currently has disability', 
    'HHPARN19X': 'D - Parental structure of household', 
    'HHPARN19_BRD': 'D - Household has second parent or guardian', 
    'NUMSIBSX': 'D -Number of child’s siblings', 
    'PARGRADEX': 'D -Parent/guardian highest education', 
    'RACEETH': 'D -Race and ethnicity of child', 
    'INTACC': 'D -Household has internet access', 
    'CENREG': 'D -Census region where child lives', 
    'ZIPLOCL': 'D -Zip code classification by community type'
    }