#!/usr/bin/env python3

# Similutes a fight between characters using rules largely derived from
# the tabletop RPG GURPS.
# Experimenting with inheritance and composition.

from random import randint, gauss
import dice
import math


class Character:

    def __init__(self, name, st=10, dx=10, iq=10, ht=10):
        self.name = name
        self.st = st         # strength
        self.dx = dx         # dexterity
        self.iq = iq         # intelligence
        self.ht = ht         # health
        self.max_hp = self.ht    # hit points
        self.hp = self.max_hp
        self.will = self.iq  # willpower
        self.per = self.iq   # perception
        self.speed = (ht + dx) / 4
        self.dodge = int(self.speed + 3)
        self.move = int(self.speed)
        self.dr = 0    # damage resistance (armor)
        self.weapon = None

        # states the character may be in
        self._reeling = False
        self.conscious = True
        self._alive = True
        self._neg_hp_mult = -1
        self._neg_hp = self.max_hp * self._neg_hp_mult
        
        # skills
        self.melee_skill = MeleeSkill(self.dx, 1)


        # calculate damage
        # formula derived from line of best fit for average damage
        # in GURPS strength/damage table
        self.swing_dmg = round((0.94 * self.st - 6.3), 1)
        self.thrust_dmg = round((0.335 * self.st - 0.355), 1)

    def __str__(self):
        return self.name

    def roll_damage_swing(self):
        return int(self.swing_dmg * gauss(1, .3) + self.weapon.damage[1])

    def roll_damage_thrust(self):
        return self.thrust_dmg * gauss(1, .3)

    def melee_attack(self, target):
        attack = dice.roll_gurps(self.melee_skill.skill)
        target_dodge = target.parry_attack()
        print('{}({}hp) attacks {}...{}'.format(self.name, self.hp, target.name, attack[1]))

        # determine outcome of attack
        if attack[1] == "Critical Success":
            print('Critical hit!')
            basic_damage = self.roll_damage_swing()
            half_dr = False

            crit_table = dice.roll3d6()
            if crit_table in (3, 18):
                basic_damage *= 3
                print('Triple damage!')
            elif crit_table in (4, 17):
                penetrating_damage = basic_damage - (target.dr / 2)
                half_dr = True
                print('Armor penetration!')
            elif crit_table in (5, 16):
                basic_damage *= 2
                print('Double damage!')
            elif crit_table in (6, 15):
                basic_damage = int(self.swing_dmg * 1.9 + self.weapon.damage[1])
                print('Max damage!')

            if not half_dr:
                penetrating_damage = basic_damage - target.dr

            # determine amount of damage
            if penetrating_damage > 0:
                if self.weapon.type == 'cut' or self.weapon.type == 'pi+':
                    injury = int(penetrating_damage * 1.5)
                    target.hp -= injury
                print('{} scored a hit with his {}! {} takes {} damage'.format(
                    self.name, self.weapon.name, target.name, injury))
            else:
                print("{}'s {} failed to penetrate {}'s armor.".format(
                    self.name, self.weapon, target.name))
        elif attack[3] and not target_dodge[3]:   # the attack hit
            basic_damage = self.roll_damage_swing()
            penetrating_damage = basic_damage - target.dr

            # determine amount of damage
            if penetrating_damage > 0:
                if self.weapon.type == 'cut' or self.weapon.type == 'pi+':
                    injury = int(penetrating_damage * 1.5)
                    target.hp -= injury
                print('{} scored a hit with his {}! {} takes {} damage'.format(
                    self.name, self.weapon.name, target.name, injury))
            else:
                print("{}'s {} failed to penetrate {}'s armor.".format(
                    self.name, self.weapon, target.name))
        elif attack[3] and target_dodge[3]:
            print(target.name, 'narrowly dodged the strike!')
        elif not attack[3]:
            print(self.name, 'missed!')

    def dodge_attack(self):
        return dice.roll_gurps(self.dodge)

    def parry_attack(self):
        return dice.roll_gurps(self.melee_skill.parry)

    def turn(self):
        if self.hp < (self.max_hp / 3) and not self._reeling:
            self.dodge = math.ceil(self.dodge / 2)
            self.move = math.ceil(self.move / 2)
            self._reeling = True
            print("{} is reeling from his wounds!".format(self.name))
        if self.hp <= 0:
            if dice.roll_gurps(self.ht)[3]:
                print("{} holds on to consciousness.".format(self.name))
            else:
                self.conscious = False
                print("{} loses consciousness!".format(self.name))

        if self.hp <= self.max_hp * -5:
            self.conscious = False
            self._alive = False
            print("{} IS DEAD!".format(self.name))
        elif self.hp <= self._neg_hp:
            self._neg_hp_mult -= 1
            self._neg_hp = self.max_hp * self._neg_hp_mult
            if dice.roll_gurps(self.ht)[3]:
                print("{} is critically wounded, but clings to life through sheer willpower.".format(self.name))
            else:
                self.conscious = False
                self._alive = False
                print("{} IS DEAD!".format(self.name))


class Weapon:

    def __init__(self, name, type, damage, cost, weight, min_st):
        self.name = name
        self.type = type
        self.damage = damage
        self.cost = cost
        self.weight = weight
        self.min_st = min_st

    def __str__(self):
        return self.name


class MeleeWeapon:

    def __init__(self, weapon):
        self.name = weapon['name']
        self.type = weapon['type']
        self.damage = weapon['damage']
        self.cost = weapon['cost']
        self.weight = weapon['weight']
        self.min_str = weapon['min_str']
        self.reach = weapon['reach']

    def __str__(self):
        return self.name


class Firearm(Weapon):

    def __init__(self, name, type, damage, cost, weight, min_st, ss, acc, rof, shots):
        super().__init__(name, type, damage, cost, weight, min_st)
        self.ss = ss
        self.accuracy = acc
        self.rof = rof
        self.shots = shots

class Skill:

    def __init__(self):
        self.cont_att = None    # controlling attribute
        self.mod = 0
        self.rank = 0
        self.skill = self.cont_att + self.mod + self.rank

    def set_skill(self, att, rank):
        self.cont_att = att
        self.rank = rank
        self.skill = self.cont_att + self.mod + self.rank

class MeleeSkill(Skill):

    def __init__(self, att, rank):
        self.cont_att = att  # controlling attribute
        self.mod = -1
        self.rank = rank
        self.skill = self.cont_att + self.mod + self.rank
        self.parry = int(self.skill / 2 + 3)

    def set_skill(self, att, rank):
        self.cont_att = att
        self.rank = rank
        self.skill = self.cont_att + self.mod + self.rank
        self.parry = int(self.skill / 2 + 3)

class Battle:

    def __init__(self):
        self.round = 1

    def battle(self):
        while lee.conscious and goblin.conscious:
            print()
            print('----- Round', self.round, '-----')
            lee.melee_attack(goblin)
            print()
            goblin.melee_attack(lee)
            goblin.turn()
            lee.turn()
            self.round += 1
            input('Press any key to continue.')
        if lee.conscious and not goblin.conscious:
            print('{} is victorious!'.format(lee.name))
        else:
            print('Lee fought bravely, but was defeated.')

weapons = {'broadsword': {'name': 'Broadsword', 'type': 'cut', 'damage': ['sw', 2],
                          'cost': 500, 'weight': 3, 'min_str': 10, 'reach': 1}}

lee = Character('Lee', st=12, iq=13, dx=12, ht=11)
lee.weapon = MeleeWeapon(weapons['broadsword'])
lee.melee_skill.set_skill(lee.dx, 2)
lee.dr = 4 # give chainmail
goblin = Character('Goblin', ht=13)
goblin.weapon = MeleeWeapon(weapons['broadsword'])
goblin.dr = 4

new_battle = Battle()
new_battle.battle()


print(lee.swing_dmg)