import re, datetime

regex = re.compile(r"""
    ^((0?[13578]|10|12)
    (-|\/)
    (([1-9])|(0[1-9])|([12])([0-9]?)|(3[01]?))
    (-|\/)
    ((19)([2-9])(\d{1}) | (20)([01])(\d{1}) | (\d{2})) | (0?[2469]|11)
    (-|\/)
    (([1-9]) | (0[1-9])|([12])([0-9]?)|(3[0]?))
    (-|\/)
    ((19)
    ([2-9])
    (\d{1}) | (20)
    ([01])
    (\d{1}) | (\d{2})
    ))$
""", re.VERBOSE)

base = datetime.date(1920, 1, 1)
numdays = 36500
date_list = [base + datetime.timedelta(days=x) for x in range(0, numdays)]

for i in date_list:
    #mydate = i.strftime("%m/%d/%y")
    mydate = i.strftime("%M/%D/%Y")
    if re.match(regex, mydate):
        print(mydate)
print(base.strftime("%M/%D/%Y"))
