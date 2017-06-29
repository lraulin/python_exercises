# Similutes a fight between characters using rules largely derived from
# the tabletop RPG GURPS.

from random import randint
import dice

class Character():

    def __init__(self, name, st=10, dx=10, iq=10, ht=10):
        self.name = name
        self.st = st
        self.dx = dx
        self.iq = iq
        self.ht = ht
        self.hp = self.ht
        self.will = self.iq
        self.per = self.iq
        self.speed = (ht + dx) / 4
        self.dodge = int(self.speed + 3)
        self.move = int(self.speed)

        # calculate damage
        # formula derived from line of best fit for average damage
        # in GURPS strength/damage table
        self.swing_dmg = 0.7254 * self.st - 2.51
        self.thrust_dmg = 0.335 * self.st - 0.355

    def roll_damage_swing(self):
        return self.swing_dmg + randint(-2, 2)

    def roll_damage_thrust(self):
        return self.thrust_dmg + randint(-2, 2)

    def melee_attack(self, target):
        attack = dice.roll_gurps(self.dx)
        target_dodge = target.dodge_attack()
        print('{} attacks {}'.format(self.name, target.name))
        if attack[3] and not target_dodge[3]:
            # apply damage
            print('{} scored a hit!'.format(self.name))
        elif attack[3] and target_dodge[3]:
            print(target.name, 'narrowly dodged the strike!')
        elif not attack[3]:
            print(self.name, 'missed!')

    def dodge_attack(self):
        return dice.roll_gurps(self.dodge)

olaf = Character('Olaf', dx=12)
brutus = Character('Brutus')

for i in range(6):
    olaf.melee_attack(brutus)
    brutus.melee_attack(olaf)