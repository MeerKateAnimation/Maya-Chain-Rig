import maya.cmds as cmds #look up if it's maya, maya.cmds, or something else
import math


'''------------------
CHANGEABLE ATTRIBUTES
------------------'''

#TODO read selected meshes and create some if none are selected
def read_selected():
    pass

def create_chain_model(units):
    pass

#TODO make a pop-up window with options to customize rig
#TODO calculate curve points and joints amount
#TODO create curve
#TODO skin curve to joints
#TODO create animation controls
def create_rig_control(con_name, radius, length): #consider breaking shape creation out into it's own functions? or at least the square/rectangle part
    end_shapes = []
    side_shapes=[]
    #create ends of control
    for x in range(1,3):
        shape=(cmds.circle(n=f"{con_name}_end0{x}", c=(0,0,0), d=3, r=radius, nr=(0,1,0), ch=False))[0]
        end_shapes.append(shape)
    cmds.move(0, radius, 0, end_shapes[0])
    cmds.move(0, -radius, 0, end_shapes[1])
    #create sides of control
    side_radius = math.sqrt(2*(radius*radius))
    for y in range(1,3):
        shape=(cmds.circle(n=f"{con_name}_side0{y}", c=(0,0,0), d=1, r=side_radius, nr=(0,1,0), ch=False, s=4))[0]
        cmds.rotate(0, 45, 0, shape)
        #freeze transformations
        cmds.makeIdentity(shape, a=True, t=True, r=True, s=True) #make own function
        #scale shapes to length
        cmds.scale()
        side_shapes.append(shape)
        
    cmds.rotate(90, 0, 0, side_shapes[0], dph=True)
    cmds.rotate(0, 0, 90, side_shapes[1], dph=True)

    for each in (end_shapes + side_shapes):
        cmds.makeIdentity(each, a=True, t=True, r=True, s=True)
    print()
    '''print(shapes)
    for each in shapes:
        print(each)
        
    return shapes'''

def combine_shapes(): #TODO find better name for function
    pass

def freeze_transformations(object, t=True, r=True, s=True):
    pass

#TODO constrain joints to controls
#TODO calculate distance between chain links
#TODO constrain chains to curve
#TODO make a control to limit each chain's distance from each other link
#TODO write docstrings? 

#useful functions
#freeze transformations


def main():
    create_rig_control("con", 2, 3)

if __name__ == "__main__":
    main()