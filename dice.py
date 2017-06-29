from random import randrange, randint

def roll(number, sides, modifier=0):
    result = 0
    for i in range(number):
        result += randrange(sides) + 1
    return result + modifier

def roll3d6():
    return roll(3, 6)

def rolld20():
    return roll(1, 20)

def roll4dF():
    result = 0
    for i in range(4):
        result += randrange(3) - 1
    return result

def roll_fudge():
    descriptors = ['Terrible', 'Poor', 'Mediocre', 'Fair', 'Good', 'Great']
    roll = roll4dF()
    return descriptors[roll + 3]

def roll_percentile():
    roll(1, 100)

# 4d6, drop lowest
# can also take other types of dice, number of dice, and number of high rolls to keep
def roll_best(sides=6, dice=4, keep=3):
    rolls = []
    for i in range(dice):
        rolls.append(randint(1, sides))
    #print(rolls)
    while len(rolls) > keep:
        rolls.remove(min(rolls))
    return sum(rolls)

# Set of D&D scores using 4d6b3 method
def gen_attributes():
    attributes = []
    for i in range(6):
        attributes.append(roll_best())
    return attributes

def roll_owod(pool, difficulty, successes=0, reroll=False):
    # Roll using rules from Old World of Darkness
    no_successes = True
    any_ones = False

    for i in range(pool):
        roll = randint(1, 10)
        if roll == 1 and reroll == False:
            successes -= 1
            any_ones = True
        elif roll == 10:
            roll_owod(pool, difficulty, successes, True)
        elif randint(1, 10) > difficulty:
            successes += 1
            no_successes = False

    if no_successes and any_ones:
        return "Botch!"

    return successes

def roll_nwod(pool, successes=0):
    # Roll using rules from New World of Darkness
    for i in range(pool):
        roll = randint(1, 10)
        if roll == 1:
            successes -= 1
        elif roll == 10:
            roll_owod(pool, successes)
        elif randint(1, 10) >= 8:
            successes += 1

    return successes

def roll_gurps(skill, *args):
    # Skill the player's effective skill.
    # Returns result of die roll and degree and margin of success or failure.
    mod = sum(args)    # Take arbitrary number of modifiers to the roll
    success = ""
    roll = randint(1, 6) + randint(1, 6) + randint(1, 6) + mod
    margin = skill - roll    # Margin of success or failure
    if roll <= 4:
        success = "Critical Success"
    elif roll == 5 and skill >= 15:
        success = "Critical Success"
    elif roll == 6 and skill >= 16:
        success = "Critical Success"
    elif roll >= 18:
        success = "Critical Failure"
    elif roll >= 17 and skill <= 15:
        success = "Critical Failure"
    elif margin <= -10:
        success = "Critical Failure"
    elif roll <= skill:
        success = "Success"
    else:
        success = "Failure"
    if "Success" in success:
        passfail = True
    else:
        passfail = False

    return roll, success, margin, passfail

def gurps_quick_contest(skill1, skill2, mod1=0, mod2=0):
    # Returns margin of success for first actor
    # If negative, the absolute value is the margin of success for second actor.
    roll1 = roll_gurps(skill1 + mod1)[0]
    roll2 = roll_gurps(skill2 + mod2)[0]
    return roll1 - roll2

def gurps_regular_contest(skill1, skill2):
    turns = 0
    winner = ''
    # If both skills are low, make the lower one 10, and
    # increase the other one by the same amount.
    if skill1 <= 6 and skill2 <= 6:
        if skill1 > skill2:
            skill2 = 10
            skill1 += 10 - skill2
        else:
            skill1 = 10
            skill2 += 10 - skill1
    while winner == '':
        pass

def gurps_long_task(hours, *args):
    """
    :param hours:   Total man-hours required to complete task.
    :param args:    Each arg is the skill of a worker.
    :return:
    """
    skills = list(args)
    day = 0
    total_work = 0
    success = False
    while success == False:
        day += 1
        days_work = 0
        for worker in skills:
            work = 0
            result = roll_gurps(worker)[1]
            if result == 'Critical Success':
                work = 12
            if result == 'Failure':
                work = 4
            if result == 'Critical Failure':
                hours -= randint(1, 6) + randint(1, 6)
            if result == 'Success':
                work = 8
            days_work += work
        print('Day {}: {} man-hours of work completed'.format(day, days_work))
        total_work += days_work
        if total_work >= hours:
            success = True

    return print('Task completed in {} days.'.format(day))


#--------------------------------
# Test

if __name__ == "__main__":
    for i in range(10):
        #print(roll_gurps_contested(11, 15))
        #print(roll_gurps(10))
        #print(roll_best())
        print(gen_attributes())

    gurps_long_task(100, 10, 10, 10)

#--------------------------------

# OOP version

class Die():
    def __init__(self, sides):
        self.sides = sides

    def roll(self, number):
        result = 0
        for i in range(number):
            result += randrange(self.sides) + 1
        return result

class D6(Die):
    def __init__(self):
        self.sides = 6

class GURPSRoll():

    def __init__(self, skill, *args):
        self.skill = skill
        self.mod = sum(args)  # Take arbitrary number of modifiers to the roll
        self.success = None
        self.roll = randint(1, 6) + randint(1, 6) + randint(1, 6) + mod
        self.margin = skill - roll  # Margin of success or failure
        if roll <= 4:
            self.success = True
        elif roll >= 17:
            self.success = False

    def get_margin(self):
        return self.margin

    def get_success(self):
        return self.success

class GurpsLongTask():

    def __init__(self, hours, *args):
        skills = args
