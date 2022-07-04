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
        print(player.location.description())


    # -------------------------------------------------------
    def do_go(self, arg):
        global player
        if not arg in ['north', 'east', 'south', 'west']:
            print("That's not a valid direction.")
        elif not arg in player.location.exits.keys():
            print("Moving in that direction isn't possible right now.")
        else:
            dest = player.location.exits[arg]
            player.location = dest
            print(f"You move {arg}.")
            self.do_look(None)


# **** init() *************************************************************
def init():
    global player, room
    player = Player()
    r1 = Room("White Room", "This is a long description of the test room.")
    r2 = Room("Blue Room", "This is a long description of the test room.")
    r1.exits['east'] = r2
    r2.exits['west'] = r1
    rooms["White Room"] = r1
    rooms["Blue Room"] = r2
    player.location = r1



# **** main ***************************************************************
if __name__ == '__main__':
    init()
    MainGameCmd().do_look(None)
    MainGameCmd().cmdloop()

