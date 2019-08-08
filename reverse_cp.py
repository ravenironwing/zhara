#from settings import *
# Used to reverse animations for left and right body sides
def reverse_symetry(position):
    #switches left and right body placements
    new_position = []
    new_position = [position[1], position[0], position[2], position[4], position[3], position[6], position[5], position[7], position[8], position[10], position[9], position[11]]
    #switches the body part angles and y positions
    switched_positions = []
    for part in new_position:
        try:
            switched_positions.append([part[0], -part[1], -part[2]])
        except:
            switched_positions.append([-part[1], -part[0]])
    return switched_positions

def reverse_animation_symetry(animation):
    new_animation = []
    for pos in animation:
        new_animation.append(reverse_symetry(pos))
    return new_animation

#print(reverse_symetry(CP_PUNCH1))



