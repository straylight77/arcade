#!/usr/bin/env python 

from adventurelib import *
import json

Room.items = Bag()

class Prop(Item):
    getable = False
    state = None


#-------------------------------------------------------------
@when('north', direction='north')
@when('south', direction='south')
@when('east', direction='east')
@when('west', direction='west')
@when('n', direction='north')
@when('s', direction='south')
@when('e', direction='east')
@when('w', direction='west')
def go(direction):
    global current_room
    room = current_room.exit(direction)
    if room:
        current_room = room
        print(f'You go {direction}.')
        look()


#-------------------------------------------------------------
@when('look')
def look():
    global current_room
    print()
    print(current_room.name)
    say(current_room)
    #say(f"Visible exits: {current_room.exits()}")
    for item in current_room.items:
        say(f"You see {item} here.")
    for x in current_room.exits():
        print(f"{x.capitalize()}: {current_room.exit(x).name}")
    print()


@when('examine ITEM')
@when('look at ITEM')
def examine(item):
    obj = current_room.items.find(item)
    msg = ""
    if not obj:
        msg += f"You don't see that here."
    else:
        msg += obj.desc
        if obj.state:
            msg += f" It's {obj.state}."
    say(msg)


#-------------------------------------------------------------
@when('get ITEM')
@when('take ITEM')
def take(item):
    obj = current_room.items.find(item)
    if not obj:
        print(f"There is no {item} here.")
    elif not obj.getable:
        print(f"You aren't able to pick up the {obj}.")
    else:
        obj = current_room.items.take(item)
        inventory.add(obj)
        print(f"You take the {obj}.")


#-------------------------------------------------------------
@when('i')
def show_inventory():
    print("You have:")
    if not inventory:
        print (" - nothing!")
    else:
        for item in inventory:
            print(f" - {item}")

#-------------------------------------------------------------
def init():
    global rooms, items, props, current_room, inventory
    rooms = { }
    items = { }
    props = { }

    with open('space.json') as json_file:
        data = json.load(json_file)

        #create all of the items first so they can be referenced
        #for k in data['items']:
        #    items[k] = Item(k, data['items'][k])

        #create all of the props
        for k in data['props']:
            props[k] = Prop(k)
            props[k].aliases = data['props'][k]['aliases']
            props[k].desc = data['props'][k]['desc']
            try:
                props[k].state = data['props'][k]['state']
            except KeyError:
                pass

        #create all of the rooms
        for r in data['rooms']:
            new_room = Room(data['rooms'][r]['desc'])
            new_room.name = r
            rooms[r] = new_room

        #set up all of the exits for each room
        for r in data['rooms']:
            for d in data['rooms'][r]['exits']:
                room_name = data['rooms'][r]['exits'][d]
                s = f"rooms[r].{d} = rooms[room_name]"
                #print(s)
                exec(s)

    inventory = Bag()
    current_room = rooms['Sick Bay']

    #door = Prop("security door", "door")
    rooms['Sick Bay'].items.add(props['security door'])


#-------------------------------------------------------------
if __name__ == "__main__":
    init()
    print('Incident on Station 57')
    print('======================')
    print()
    print('Type "help" for commands.')
    look()
    start()

