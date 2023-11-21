import maya.cmds as cmds
import math


'''------------------
CHANGEABLE ATTRIBUTES
------------------'''
selection_sort = True

control_number = 3
control_name = "chainControl"
control_padding = 2 

chain_links = 10 #only applies if selection is empty
chain_name = "chain" #only applies if selection is empty



'''---------------'''


def read_selected():
    selected_objects = cmds.ls(sl=True)
    return selected_objects

def create_chain_model(name, units):
    chain = []
    for x in range(units):
        link = cmds.polyTorus(n=f"{name}{x}", r=0.8, sr=0.25, sa=10, sh=10)
        chain.append(link)
    offset_chain(chain, (1,0,0), (30,0,0))

def offset_chain(chain, offsetT, offsetR):
    new_offsetT = (0,0,0)
    new_offsetR = (0,0,0)
    for link in chain:
        cmds.move(new_offsetT[0], new_offsetT[1], new_offsetT[2], link)
        cmds.rotate(new_offsetR[0], new_offsetR[1], new_offsetR[2], link)
        new_offsetT = (new_offsetT[0] + offsetT[0],
                       new_offsetT[1] + offsetT[1],
                       new_offsetT[2] + offsetT[2])
        new_offsetR = (new_offsetR[0] + offsetR[0],
                       new_offsetR[1] + offsetR[1],
                       new_offsetR[2] + offsetR[2])

    


#TODO make a pop-up window with options to customize rig
#TODO calculate curve points and joints amount
#TODO create curve
#TODO skin curve to joints

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
        freeze_transformations(shape)
        #calculate what to scale the shapes by
        scale_length = length/(radius*2)
        cmds.scale(scale_length, 1, 1, shape)
        side_shapes.append(shape)
    #stands objects up
    cmds.rotate(90, 0, 0, side_shapes[0], dph=True)
    cmds.rotate(0, 0, 90, side_shapes[1], dph=True)
    for each in (end_shapes + side_shapes):
        freeze_transformations(each)
    new_control = combine_shapes(con_name, (end_shapes + side_shapes))
    return new_control

def combine_shapes(name, shapes): #TODO find better name for function
    cmds.select(d=True)
    new_object = cmds.group(n=name, em=True)
    #select shapes
    cmds.select(shapes)
    cmds.pickWalk(d='down')
    #select empty group
    cmds.select(new_object, add=True)
    cmds.parent(r=True, s=True)
    #select and delete remaining empty nodes
    cmds.select(d=True)
    for each in shapes:
        cmds.select(each, add=True)
    cmds.delete()
    return new_object

def freeze_transformations(object, absolute=True, translate=True, rotate=True, scale=True):
    cmds.makeIdentity(object, a=absolute, t=translate, r=rotate, s=scale)

#TODO constrain joints to controls
#TODO calculate distance between chain links
#TODO constrain chains to curve
#TODO make a control to limit each chain's distance from each other link
#TODO write docstrings? 

#useful functions
#freeze transformations


def main():
    #get selected geometry 
    geometry = read_selected()
    if geometry == []:
        geometry = create_chain_model(chain_name, chain_links)
    elif selection_sort == True:
        geometry.sort()

    #create control
'''    for x in range(control_number):
        create_rig_control(f"{control_name}{x}", 2, 4)#TODO pad number
'''

if __name__ == "__main__":
    main()