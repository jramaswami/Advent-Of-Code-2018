"""
Advent of Code 2018
Day 24: Immune System Simulator 20XX
"""
import re
import copy


IMMUNE_SYS = 0
INFECTION = 1
FLAG_STRS = ['Immune System', 'Infection']


class BattleGroup:
    def __init__(self, line, uid, flag):
        self.alive = True
        self.uid = uid
        self.flag = flag
        self.units = int(re.search(r'(\d+) units', line).groups()[0])
        self.hitpoints = int(re.search(r'(\d+) hit points', line).groups()[0])
        self.initiative = int(re.search(r'initiative (\d+)', line).groups()[0])
        attack_damage, self.attack_type = re.search(r'attack that does (\d+) (\w+) damage', line).groups()
        self.attack_damage = int(attack_damage)
        defense = line[line.find('(')+1:line.find(')')].split(';')
        self.weaknesses = []
        self.immunities = []
        for d in defense:
            d = d.strip()
            if d.startswith('weak to'):
                tokens = d.split()
                self.weaknesses = [t.replace(',', '') for t in tokens[2:]]
            elif d.startswith('immune to'):
                tokens = d.split()
                self.immunities = [t.replace(',', '') for t in tokens[2:]]

    def effective_power(self):
        "Return effective power."
        return self.attack_damage * self.units

    def buff(self, power):
        "Give a boost."
        if self.flag == IMMUNE_SYS:
            self.attack_damage += power

    def possible_damage(self, in_attack_type, in_effective_power):
        "Return the possible amount of damage done by incoming attack."
        if in_attack_type in self.immunities:
            return 0
        elif in_attack_type in self.weaknesses:
            return in_effective_power * 2
        return in_effective_power


    def receive_attack(self, in_attack_type, in_effective_power):
        "Receive enemy attack."
        damage = self.possible_damage(in_attack_type, in_effective_power)
        dead_units = damage // self.hitpoints
        if dead_units > self.units:
            dead_units = self.units
        self.units = self.units - dead_units
        if self.units <= 0:
            self.units = 0
            self.alive = False
        return dead_units

    def select_target(self, battle_groups, selected):
        "Select the target."
        max_dmg = -1
        target = None
        for g in battle_groups:
            if g.flag == self.flag:
                continue
            if (g.flag, g.uid) in selected:
                continue
            dmg = g.possible_damage(self.attack_type, self.effective_power())
            if dmg == 0:
                continue
            if dmg > max_dmg:
                target = g
                max_dmg = dmg
            elif dmg == max_dmg:
                if target.effective_power() == g.effective_power():
                    if target.initiative < g.initiative:
                        target = g
                elif target.effective_power() < g.effective_power():
                    target = g
        return target

    def __repr__(self):
        flag = 'infection'
        if self.flag == IMMUNE_SYS:
            flag = 'immune system'

        return 'Group(uid={}, flag={}, units={}, hitpoints={}, initiative={}, attack_type={}, attack_damage={}, weaknesses={}, immunities={}'.format(
                    self.uid, flag, self.units, self.hitpoints, self.initiative, self.attack_type, self.attack_damage, self.weaknesses, self.immunities)


def target_phase(battle_groups):
    "Target phase"
    selected = set()
    targets = {}
    for g in sorted(battle_groups, key=lambda g: (g.flag, g.effective_power(), g.initiative), reverse=True):
        t = g.select_target(battle_groups, selected)
        if t:
            selected.add((t.flag, t.uid))
        targets[g] = t
    return targets

def attack_phase(battle_groups, targets):
    "Attack phase."
    casualties = 0
    for g in sorted(battle_groups, key=lambda g: g.initiative, reverse=True):
        if g.alive:
            t = targets[g]
            if t is None:
                continue
            dead_units = t.receive_attack(g.attack_type, g.effective_power())
            casualties += dead_units
    return casualties


def tick(battle_groups):
    targets = target_phase(battle_groups)
    attack_phase(battle_groups, targets)
    return [b for b in battle_groups if b.alive]

def solve_a(battle_groups):
    i = 1
    while True:
        battle_groups = tick(battle_groups)
        if len(set([b.flag for b in battle_groups])) == 1:
            break
    return sum(b.units for b in battle_groups)


def solve_b(battle_groups):
    b = 1
    while True:
        battle_groups0 = copy.deepcopy(battle_groups)
        for g in battle_groups0:
            g.buff(b)
        while True:
            targets = target_phase(battle_groups0)
            casualties = attack_phase(battle_groups0, targets)
            if casualties == 0:
                break
            battle_groups0 = [b for b in battle_groups0 if b.alive]
            remaining = set([g.flag for g in battle_groups0])
            if len(remaining) == 1:
                if set([IMMUNE_SYS]) == remaining:
                    return sum(g.units for g in battle_groups0)
                break
        b += 1

def main():
    "Main program."
    import sys
    battle_groups = []
    sys.stdin.readline()    # ignore "Immune System:"
    line = sys.stdin.readline().strip()
    uid = 1
    while line:
        battle_groups.append(BattleGroup(line, uid, IMMUNE_SYS))
        line = sys.stdin.readline().strip()
        uid += 1

    uid = 1
    sys.stdin.readline()    # ignore "Infection:"
    line = sys.stdin.readline().strip()
    while line:
        battle_groups.append(BattleGroup(line, uid, INFECTION))
        line = sys.stdin.readline().strip()
        uid += 1

    print(solve_a(copy.deepcopy(battle_groups)))
    print(solve_b(battle_groups))



if __name__ == '__main__':
    main()
