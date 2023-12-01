import maya.cmds as cmds
import math


'''------------------
CHANGEABLE ATTRIBUTES
------------------'''
numbers_padding = 2 #not implimented

selection_sort = True

control_number = 3
#chain_name = "chainControl"
control_padding = 2 
control_radius = 1
control_height = 1

chain_links = 20 #only applies if selection is empty
chain_name = "chain" #only applies if selection is empty


'''---------------'''

#TODO make a pop-up window with options to customize rig

def read_selected():
    selected_objects = cmds.ls(sl=True)
    return selected_objects

def create_chain_model(name, units):
    chain = []
    for x in range(units):
        link = cmds.polyTorus(n=f"{name}{x}", r=0.9, sr=0.15, sa=10, sh=10, ch=False)[0]
        geo_group = cmds.group(link, n=f"{name}{x}_GRP")
        chain.append(geo_group)
    offset_chain(chain, (1,0,0), (90,0,0))
    return chain

def offset_chain(chain, offsetT, offsetR): #try to add toples together instead of individual indexes of tople
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
        print(f"chain link: {link}")
        #freeze_transformations(link) #why does this line break maya?!!
        #cmds.makeIdentity(link, a=True, t=True, r=True, s=True)



#TODO calculate curve points and joints amount
def calculate_chain_ends(chain):
    #get location of first and last chain
    x1 = 0
    x2 = 20
    return (x1, x2)


def calculate_point_offset(x1, x2):
    distance = abs(x2-x1)
    print(distance)
    #calculate amount of curve points to accompany joints
    curve_point_num = calculate_point_num()
    print(curve_point_num)
    curve_point_distance = distance/curve_point_num
    print(curve_point_distance)
    return(curve_point_distance)

def calculate_point_num():
    curve_point_num = (control_number*4) - 3
    return curve_point_num

#TODO create curve
def create_curve(name, points):
    #point_offset = calculate_point_offset(start_point, end_point)
    #offset = 0
    curve = cmds.curve(n=name, d=3, p=(0,0,0)) #first curve point
    #points = calculate_point_num() #gets list of tuple positions (theoretically)
    print(f"received points: {points}")
    for x in range(1,len(points)):
        print(f"points: {points[x]}")
        cmds.curve(curve, a=True, p=(points[x]))
        #offset = offset + point_offset
    return curve


def calculate_curve_points(start_point, end_point, total_points):
    points = []
    offset = 0
    point_offset = calculate_point_offset(start_point, end_point)
    
    #curve = cmds.curve(n=name, d=3, p=(0,0,0))
    
    for x in range(total_points):
        #cmds.curve(curve, a=True, p=(offset,0,0))
        points.append((offset,0,0)) #creates an offset in x-axis
        offset = offset + point_offset
    print(f"calculated points: {points}")
    return points


def create_rig_control(name, radius, length): #consider breaking shape creation out into it's own functions? or at least the square/rectangle part
    end_shapes = []
    side_shapes=[]
    #create ends of control
    for x in range(1,3):
        shape=(cmds.circle(n=f"{name}_end0{x}", c=(0,0,0), d=3, r=radius, nr=(0,1,0), ch=False))[0]
        end_shapes.append(shape)
    cmds.move(0, radius, 0, end_shapes[0])
    cmds.move(0, -radius, 0, end_shapes[1])
    #create sides of control
    side_radius = math.sqrt(2*(radius*radius))
    for y in range(1,3):
        shape=(cmds.circle(n=f"{name}_side0{y}", c=(0,0,0), d=1, r=side_radius, nr=(0,1,0), ch=False, s=4))[0]
        cmds.rotate(0, 45, 0, shape)
        freeze_transformations(shape)
        #calculate what to scale the shapes by
        scale_length = length/(radius*2)
        print(f"scale length: {scale_length}")
        cmds.scale(scale_length, 1, 1, shape)
        side_shapes.append(shape)
    #stands objects up
    cmds.rotate(90, 0, 0, side_shapes[0], dph=True)
    cmds.rotate(0, 0, -90, side_shapes[1], dph=True)
    for each in (end_shapes + side_shapes):
        freeze_transformations(each)
    new_control = combine_shapes(name, (end_shapes + side_shapes))
    return new_control

def create_settings_control(con_name, radius, length):
    control = (cmds.circle(n=f"{con_name}Settings_CTRL", c=(0,0,0), d=1, r=(radius*1.5), nr=(1,0,0), ch=False, s=4))[0]
    print(f"new control: {control}")
    cmds.addAttr(ln="stretchy", at="bool", k=True)
    return control



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

def create_control_joint(name, position):
    joint = cmds.joint(n=name, p=position)
    return joint

def create_control_rig(name, curve_points):
    point_index = 0
    controls = []
    joints = []
    for x in range(control_number):
        print(x)
        print(control_number)
        new_control = create_rig_control(f"{name}{x}_CTRL", control_radius, control_height)#TODO pad number
        cmds.rotate(0, 0, 90, new_control)
        cmds.move(curve_points[point_index][0], 
                  curve_points[point_index][1], 
                  curve_points[point_index][2],
                  new_control)
        freeze_transformations(new_control)
        new_joint = create_control_joint(f"{name}Rig{x}_JNT", curve_points[point_index])
        point_index += 4
        controls.append(new_control)
        joints.append(new_joint)
        print(new_joint)
        cmds.parentConstraint(str(new_control), str(new_joint), w=1)
        cmds.scaleConstraint(str(new_control), str(new_joint), w=1)


    return (controls, joints)


        
        
#TODO get length of curve 
def get_curve_length(curve): #actually might not be needed if percentage works
    length = cmds.getAttr(f"{curve}.minMaxValue.maxValue")
    print(f"curve length: {length}")
    return length

#TODO calculate distance between chain links
def calculate_object_offset(curve, object_number):
    print(f"object num: {object_number}")
    #curve_length = get_curve_length(curve)
    offset = 1.0 / (object_number - 1) # -1 from object_number to acount for object at 0
    print (f"curve offset: {offset}")
    return offset

#TODO constrain chains to curve
def get_object_shape(object):
    cmds.select(object, r=True)
    cmds.pickWalk(d="down")
    shape = read_selected()[0]
    return shape

def constrain_to_curve(curve, object, offset): #come back to this... maybe give up and use joints... specifically an ik spline
    '''shape = get_object_shape(curve)
    point_on_curve_info = cmds.createNode("pointOnCurveInfo")
    cmds.setAttr(f"{point_on_curve_info}.turnOnPercentage", 1)
    cmds.connectAttr(f"{shape}.local", f"{point_on_curve_info}.inputCurve")
    cmds.connectAttr(f"{point_on_curve_info}.result.position", f"{object}.translate")
    cmds.setAttr(f"{point_on_curve_info}.parameter", offset)'''
    pass



def create_chain_joints(name, geometry):
    joints = []
    cmds.select(cl=True)
    for x in range(len(geometry)):
        #get location of chain link
        location = cmds.getAttr(f"{geometry[x]}.translate")[0]
        #create link joint
        joint = cmds.joint(n=f"{name}Geo{x}_JNT", p=location)
        joints.append(joint)
        print(f"new joint: {joint}")
    print(f"all joints: {joints}")
    return joints

def create_ik_spline(curve, joints):
    #create spline with current curve
    #ikHandle -sol ikSplineSolver;
    print(f"curve in ik spline should be: {curve}")
    spline = cmds.ikHandle(c=curve, sol="ikSplineSolver", sj=joints[0], ee=joints[-1], fj=True)
    return spline[0]

def make_ik_spline_stretchy(curve, joints, control, number):
    #get_curve_length(curve) #don't think I need this...
    #do stuff to make spline stretchy
    print(f"the settings control: {control}")
    curve_info = cmds.createNode("curveInfo")
    shape = get_object_shape(curve)
    cmds.connectAttr(f"{shape}.local", f"{curve_info}.inputCurve")
    divide_node = cmds.createNode("multiplyDivide")
    cmds.connectAttr(f"{curve_info}.arcLength", f"{divide_node}.input1X")
    #cmds.setAttr() #TODO set up settings for divide node
    cmds.setAttr(f"{divide_node}.operation", 2)
    cmds.setAttr(f"{divide_node}.input2X", (number-1))
    condition = cmds.createNode("floatCondition")
    cmds.connectAttr(f"{divide_node}.outputX", f"{condition}.floatA")
    cmds.connectAttr(f"{control}.stretchy", f"{condition}.condition")
    for joint in joints:
        cmds.connectAttr(f"{condition}.outFloat", f"{joint}.scaleX")

    pass



def constrain_geo(geometry, constraint):
    #constrain transform
    #constrain rotation
    print(f"I should constrain {geometry} to {constraint} eventually")
    pass





#TODO make a control to limit each chain's distance from each other link
#TODO write docstrings? 
#TODO write function to change colors of controls
#TODO clean up

#useful functions
#freeze transformations


def main():
    #get selected geometry 
    geometry = read_selected()
    if geometry == []:
        geometry = create_chain_model(chain_name, chain_links)
    elif selection_sort == True:
        geometry.sort()
    curve_ends = calculate_chain_ends(geometry)
    total_points = calculate_point_num()
    curve_points = calculate_curve_points(curve_ends[0], curve_ends[1], total_points)
    print(curve_points)
    rig_curve = create_curve("chainCurve", curve_points)
    print(f"returned curve{rig_curve}")
    print(rig_curve)

    #create control rig
    controls, joints = create_control_rig(chain_name, curve_points)
    print(controls)
    print(joints)
    print(rig_curve)
    cmds.select(joints, r=True)
    cmds.select(rig_curve, add=True)
    bindable_objects = joints.copy().append(rig_curve)
    print(bindable_objects)
    #cmds.bindSkin(tsb=True)
    #tsb=True
    curve_dropoff_rate = 4 #range of 0.1-10.0
    cmds.skinCluster(tsb=True, bm=0, sm=1, nw=1, wd=1, mi=2, omi=True, dr=curve_dropoff_rate, rui=True,)
    #newSkinCluster "-toSelectedBones -bindMethod 0 -skinMethod 1 -normalizeWeights 1 
    # -weightDistribution 1 -mi 5 -omi true -dr 4 -rui true  , multipleBindPose, 1";
    settings_control = create_settings_control(chain_name, control_radius, control_height)
    cmds.parent(settings_control, controls[0])

    #connecting links to curve
    print(f"geo: {geometry}")
    chain_joints = create_chain_joints(chain_name, geometry)
    ik_handle = create_ik_spline(rig_curve, chain_joints)
    for x in range(len(chain_joints)):
        cmds.parentConstraint(str(chain_joints[x]), str(geometry[x]), w=1, mo=True)
        #cmds.scaleConstraint(str(constraint), str(object), w=1, mo=True)
    make_ik_spline_stretchy(rig_curve, chain_joints, settings_control, chain_links)
    '''offset = calculate_object_offset(rig_curve, len(geometry))
    temp_object = cmds.polyTorus(n="tempObject", r=0.8, sr=0.25, sa=10, sh=10, ch=False)[0]
    percentage = 0
    for obj in geometry:
        constrain_to_curve(rig_curve, obj, percentage)
        print(percentage)
        percentage += offset'''
    



    #group stuff in final hiearchy
    control_grp = cmds.group(controls, n="controls")
    control_joint_grp = cmds.group(joints, n="control_joints")
    chain_joint_grp = cmds.group(chain_joints[0], n="chain_joints")
    joint_grp = cmds.group([chain_joint_grp, control_joint_grp, rig_curve, ik_handle], n="joints")
    geo_grp = cmds.group(geometry, n="geometry")
    final_rig_grp = cmds.group([control_grp, joint_grp, geo_grp], n=f"{chain_name}_rig")
    #put curve and ikhandle under joint grp
    cmds.setAttr(f"{joint_grp}.visibility", 0)
    

    

if __name__ == "__main__":
    main()