#!/usr/bin/python3 

import json, textwrap, cmd

SCREEN_WIDTH = 80

rooms = { }
player = None


# =========================================================================
class Base():

    # ---------------------------------------------------------------------
    def __init__(self, name):
        self.name = name

    # ---------------------------------------------------------------------
    def __str__(self):
        return self.name

    # ---------------------------------------------------------------------
    def __repr__(self):
        return f"{type(self).__name__}({self.name})"


# =========================================================================
class Room(Base):

    # ---------------------------------------------------------------------
    def __init__(self, name, desc):
        super().__init__(name)
        self.desc = desc
        self.exits = { }

    # ---------------------------------------------------------------------
    def description(self):
        room_str = "\n" + self.name.upper() + "\n"
        room_str += ("-" * len(self.name)) + "\n"
        room_str += self.desc
        for d, r in self.exits.items():
            room_str += f"\n{d.capitalize()}: {r}"

        return room_str


# =========================================================================
class Item(Base):

    # ---------------------------------------------------------------------
    def __init__(self, name):
        self.name = name


# =========================================================================
class Prop(Base):
    pass


# =========================================================================
class Container(Prop, set):
    searchable = False
    openable = False

    def do_search(self):
        pass

    def do_open(self):
        pass

    def do_unlock(self):
        pass


# =========================================================================
class Barrier(Prop):
    """
    Assign this to 2 rooms that share an exit.
    Maintains the state to prevent or allow passage.
    """
    state = None  # locked | closed | open
    unlocked_with = None


# =========================================================================
class Player():
    location = None
    inventory = Container("inventory")



# =========================================================================
class MainGameCmd(cmd.Cmd):
    prompt = '\n> '

    # -------------------------------------------------------
    def default(self, arg):
        print('I do not understand that command. Type "help" for a list of commands.')

    # -------------------------------------------------------
    def do_quit(self, arg):
        """Quit the game."""
        return True

    # -------------------------------------------------------
    def do_look(self, arg):
        """Look around your current location and get a description of what you see, visible exits, etc."""
        global player
        if player.location:
            print(player.location.description())
        else:
            print("Unknown location.")  # this is an error if it happens

    # -------------------------------------------------------
    def do_go(self, arg):
        global player
        # check to see if the direction is even allowed
        if not arg in ['north', 'east', 'south', 'west']:
            print("That's not a valid direction.")
        # check if the direction is an option in the current room
        elif not arg in player.location.exits.keys():
            print("Moving in that direction isn't possible right now.")
        else:
            dest = player.location.exits[arg]
            player.location = dest
            print(f"You move {arg}.")
            self.do_look(None)

    # -------------------------------------------------------
    def do_n(self, arg):
        self.do_go("north")

    def do_e(self, arg):
        self.do_go("east")

    def do_s(self, arg):
        self.do_go("south")

    def do_w(self, arg):
        self.do_go("west")




# **** init() *************************************************************
def init():
    global player, room
    player = Player()

    with open('space.json') as json_file:
        data = json.load(json_file)

        # create all of the rooms so they can be referenced
        for name, values in data['ROOMS'].items():
            rooms[name] = Room(name, values['desc'])

        # loop through again to create all of the exits
        for name, values in data['ROOMS'].items():
            for direction, dest_name in values['exits'].items():
                rooms[name].exits[direction] = rooms[dest_name]

    player.location = rooms['Sick Bay']


# **** main ***************************************************************
if __name__ == '__main__':
    init()

    print('Incident on Station 57')
    print('======================')
    print()
    print('Type "help" for commands.')

    MainGameCmd().do_look(None)
    MainGameCmd().cmdloop()

