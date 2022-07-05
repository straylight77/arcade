#!/usr/bin/python3 

import json, textwrap, cmd

SCREEN_WIDTH = 80

rooms = { }
props = { }
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
        self.barriers = { }

    # ---------------------------------------------------------------------
    def add_barrier(self, direction, b):
        self.barriers[direction] = b

    # ---------------------------------------------------------------------
    def find_object(self, keyword):
        for b in self.barriers.values():
            if keyword == b.name:
                return b
            if keyword in b.aliases:
                return b
        return None


    # ---------------------------------------------------------------------
    def describe(self):
        room_str = "\n" + self.name.upper() + "\n"
        room_str += ("-" * len(self.name)) + "\n"
        room_str += self.desc + "\n"

        if len(self.barriers) > 0:
            room_str += "You see:\n"

        # describe all of the barriers and their state
        for direction, b in self.barriers.items():
            room_str += f"  a {b.name} to the {direction} which is {b.state}.\n"

        # list all of the exits
        if len(self.exits) > 0:
            room_str += "Visible exits:\n"

        for d, name in self.exits.items():
            if d in self.barriers.keys():
                #TODO: move this check to Barrier class
                if self.barriers[d].state == "open":
                    room_str += f"  {d.capitalize()}: {name}\n"
            else:
                room_str += f"  {d.capitalize()}: {name}\n"

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
class Barrier(Prop):
    """
    Assign this to 2 rooms that share an exit.
    Maintains the state to prevent or allow passage.
      state = locked | closed | open
    """

    def __init__(self, name, args):
        super().__init__(name)
        try:
            self.aliases = args['aliases']
        except KeyError:
            self.aliases = []

        try:
            self.state = args['state']
        except KeyError:
            self.state = None

        try:
            self.locked_with = args['locked_with']
        except KeyError:
            self.locked_with = None


    def __str__(self):
        return f"{self.name} ({self.state})"

    def do_open(self):
        if self.state == 'locked':
            msg = f"It's locked. You'll need a {self.locked_with} to unlock it."
        elif self.state == 'open':
            msg = "It's already open."
        else:
            self.state = 'open'
            msg = f"You open the {self.name}."
        return msg



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
            print(player.location.describe(), end="")
        else:
            print("Unknown location.")  # this is an error if it happens

    # -------------------------------------------------------
    def do_go(self, arg):
        """Move to a new location in the given direction."""
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
        """Shortcut to 'go north'"""
        self.do_go("north")

    def do_e(self, arg):
        """Shortcut to 'go east'"""
        self.do_go("east")

    def do_s(self, arg):
        """Shortcut to 'go south'"""
        self.do_go("south")

    def do_w(self, arg):
        """Shortcut to 'go west'"""
        self.do_go("west")


    # -------------------------------------------------------
    def do_open(self, arg):
        obj = player.location.find_object(arg)
        if not obj:
            print(f"You don't see a {arg} here.")
        else:
            print(obj.do_open())



# **** init() *************************************************************
def init():
    global player, rooms
    player = Player()

    with open('space.json') as json_file:
        data = json.load(json_file)

        for name, values in data['PROPS'].items():
            if values['type'] == 'barrier':
                props[name] = Barrier(name, values)

        # create all of the rooms so they can be referenced
        for name, values in data['ROOMS'].items():
            new_room = Room(name, values['desc'])

            try:
                for d, b_name in values['barriers'].items():
                    new_room.add_barrier(d, props[b_name])
            except KeyError:
                pass

            rooms[name] = new_room

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

