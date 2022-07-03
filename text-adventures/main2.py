#!/usr/bin/python3 

import json, textwrap, cmd

SCREEN_WIDTH = 80

rooms = { }


# =========================================================================
class Base():

    name = ""

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
    exits = { }
    items = { }
    props = { }

    # ---------------------------------------------------------------------
    def __init__(self, name, desc):
        super().__init__(name)
        self.desc = desc


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



# **** main() *************************************************************
if __name__ == '__main__':
    name = "Test Room"
    r = Room(name, "This is a long description of the test room.")
    rooms[name] = r
    print(rooms)

    i = Item("hydrospanner")
    print(i)

    print( {"one":i, "two":i} )

    p = Player()
    p.inventory.add(i)
    print(p.inventory)

