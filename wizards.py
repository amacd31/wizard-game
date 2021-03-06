import json
import os
import random
import time

class Wizards(object):
    def __init__(self):
        self.__state__ = {}

        self.__levels = {
                1: {'HP': 10, 'XP': 10, 'spells': ['fireball', 'lightning']},
                2: {'HP': 20, 'XP': 20, 'spells': ['fire blast', 'bolt lightning']},
                3: {'HP': 30, 'XP': 80, 'spells': []},
                4: {'HP': 40, 'XP': 200, 'spells': []},
                5: {'HP': 50, 'XP': 1000, 'spells': []}
            }

        self.__spells = json.load(open('spells.json','r'))

        self.__enemies = json.load(open('enemies.json','r'))

        self.options = {
                1: "New game",
                2: "Load game",
                3: "Save game",
                4: "Quit"
                }

    def welcome(self):
        self.clear()
        print("""
W        W       W   IIIIIII  ZZZZZ      AA      RRRRR  DDD    SSS
 W      W W     W       I        Z      A  A     R   R  D   D  S
  W    W   W   W        I       Z      AAAAAA    RRRR   D   D   S
   W  W     W W         I      Z      A      A   R   R  D   D    S
    W        W       IIIIIII  ZZZZZ  A        A  R   R  DDDD   SSS
""")

    def main_menu(self):
        for number, option in self.options.iteritems():
            print ("{0}: {1}".format(number, option))

        print("Enter your selection:")
        command = raw_input()

        while (not command.isdigit()):
            print("Please choose one of the options from 1 to 4:")
            command = raw_input()

        return int(command)

    def new_game(self):
        self.__state__['HP'] = 10
        self.__state__['XP'] = 0
        self.__state__['level'] = 1
        self.__state__['spells'] = [ 'pew', 'fire' ]

    def select_enemy(self):
        enemy = random.choice(self.__enemies.keys())
        while (self.__enemies[enemy]['level'] > self.__state__['level']):
            enemy = random.choice(self.__enemies.keys())
        return enemy

    def run(self):
        outcome = 'win'
        while (outcome == 'win'):
            enemy = self.select_enemy()
            outcome = self.fight(enemy)

            if outcome == "win":
                self.__state__['gained_xp'] = self.__enemies[enemy]['XP']
                self.__state__['XP'] += self.__state__['gained_xp']
                self.render()
                time.sleep(3)
                if self.__state__['XP'] >= self.__levels[self.__state__['level']]['XP']:
                    for spell in self.__levels[self.__state__['level']]['spells']:
                        self.__state__['spells'].append(spell)
                    self.__state__['level'] += 1
                    self.__state__['HP'] = self.__levels[self.__state__['level']]['HP']
                    self.__state__['mode'] = "level_up"
                    self.render()
                    time.sleep(3)

            elif outcome == "loss":
                self.render()
                self.main_menu()

    def fight(self, enemy):
        self.__state__['mode'] = "fight"
        self.__state__['enemy'] = self.__enemies[enemy]['name']
        self.__state__['enemy_hp'] = self.__enemies[enemy]['HP']
        self.render()
        command = ""
        self.__state__['last_cast'] = time.time()
        self.__state__['damage_received'] = 0
        while (command.lower() != 'quit'):
            command = raw_input()
            damage_done = self.cast(command)
            damage_received = self.enemy_attacked(enemy)
            if damage_done >= 0:
                self.__state__['enemy_hp'] -= damage_done
            else:
                damage_received -= damage_done

            self.__state__['damage_received'] = max(0, damage_received)
            self.__state__['HP'] -= damage_received

            if self.__state__['enemy_hp'] <= 0 or self.__state__['HP'] <= 0:
                if self.__state__['HP'] <= 0:
                    self.__state__['mode'] = 'loss'
                    return "loss"
                if self.__state__['enemy_hp'] <= 0:
                    self.__state__['mode'] = 'win'
                    return "win"

            self.render()

    def cast(self, command):
        self.__state__['current_cast'] = time.time()
        if command in self.__state__['spells']:
            return self.__spells[command]
        else:
            return self.__state__['level'] * -1

    def enemy_attacked(self, enemy):
        self.__state__['dm'] = int((time.time() - self.__state__['last_cast']) * self.__enemies[enemy]['damage'])
        damage = int(self.__state__['dm'])

        self.__state__['last_cast'] = self.__state__['current_cast']

        return damage

    def render(self):
        self.clear()

        if self.__state__['mode'] == 'fight':
            self.clear()
            enemy = self.__state__['enemy']
            print("You have encountered a {0}.\n".format(enemy))
            print("Hit points: {0}".format(self.__state__['HP']))
            print("{0} hit points: {1}".format(enemy,
                self.__state__['enemy_hp']))
            print("Level: {0}\t \t Experience points: {1}".format(self.__state__['level'], self.__state__['XP']))
            print("Cast:> ")

        elif self.__state__['mode'] == 'win':
            self.clear()
            enemy = self.__state__['enemy']
            print("You have killed a {0}!").format(enemy)
            print("You gained {0} XP!").format(self.__state__['gained_xp'])

        elif self.__state__['mode'] == 'loss':
            self.clear()
            enemy = self.__state__['enemy']
            print("You were killed by a {0}!!").format(enemy)
            print("You died a level {0} wizard with {1} experience.").format(self.__state__['level'], self.__state__['XP'])
            print("")

        elif self.__state__['mode'] == 'level_up':
            print("You leveled up!!")
            print("You are now level {0}!").format(self.__state__['level'])
            print("You now {0} hit points.").format(self.__state__['HP'])
            print("You can now cast the following spells:")
            for spell in  self.__levels[self.__state__['level'] - 1]['spells']:
                print("\t{0}".format(spell))


    def clear(self):
        os.system('clear')

if __name__ == "__main__":

    w = Wizards()
    w.welcome()
    time.sleep(3)
    w.clear()
    command = w.main_menu()

    if command == 1:
        w.new_game()
        w.run()
    elif command == 2 or command == 3:
        print("Feature yet to be implemented.")
        w.main_menu()
    elif command == 4:
        print("Exiting...")
        exit()
    else:
        print("Invalid option.")
        w.main_menu()


