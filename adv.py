from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk

def projected_path(starting_room, prev_visited=set()):
    #get lst orderad for visited
    visited = set()
    #Add rooms that have been visited to visited
    for room in prev_visited: 
        visited.add(room)
    #start path list
    path = []
    #make a dic for oppsite directions
    opposite = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
    #make def to add a step to the path
    def add_step(room, back=None):
        #add the room player in to visited
        visited.add(room)
        #get room exits
        exits = room.get_exits()
        #for each possable exit
        for direction in exits:
            #if room in dir not visited:
            if room.get_room_in_direction(direction) not in visited:
                #add step to path
                path.append(direction)
                #and then exlore that room
                add_step(room.get_room_in_direction(direction), opposite[direction])
        #then go back
        if back: 
            path.append(back)
    add_step(starting_room)
    return path

#Make path for player
def make_path(starting_room, visited=set()):
    #make a list to hold the path
    player_path = []
    #make a dic for oppsite directions
    opposite_dir = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
    #make def to add a step to the path
    def add_step(room, back=None):
        #make lst with current room 
        visited.add(room)
        #get room exits
        exits = room.get_exits()
        #make path lengths tuple
        path_lengths = {}
        #for each possable exit
        for direction in exits:
            #How long will the path be in specific directions
            path_lengths[direction] = len(projected_path(room.get_room_in_direction(direction), visited))
        #start treversal order
        traverse_order = []
        for key, _ in sorted(path_lengths.items(), key=lambda x: x[1]): traverse_order.append(key)
        #for each dir in path order
        for direction in traverse_order:
        #for each dir find a path order
            #if there is a direction from room not visited
            if room.get_room_in_direction(direction) not in visited:
                #add that dir to the main path
                player_path.append(direction)
                #and then exlore that room
                add_step(room.get_room_in_direction(direction), opposite_dir[direction])
        #if player has explored everything in the world end
        if len(visited) == len(world.rooms): return
        #if not: go back
        elif back: 
            player_path.append(back)
    #take the next step
    add_step(starting_room)
    return player_path


#try the code
traversal_path = make_path(world.starting_room)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
