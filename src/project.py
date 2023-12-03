import maya.cmds as cmds
import math


'''------------------
CHANGEABLE ATTRIBUTES
------------------'''
#numbers_padding = 2 #not implimented

selection_sort = True

control_number = 3
#chain_name = "chainControl"
#control_padding = 2 #not implimented
control_radius = 1
control_height = 3
control_color = 22 #maya color index
control_settings_color = 18 #maya color index

chain_links = 20 #only applies if selection is empty
chain_name = "chain" 


'''---------------'''

#TODO make a pop-up window with options to customize rig

def read_selected():
    """Reads selected Maya objects.

    :returns: List of Maya objects in order they were selected.
    :rtype: list
    """
    selected_objects = cmds.ls(sl=True)
    return selected_objects

def create_chain_model(name, units):
    """Creates a chain model.

    Creates chain links and offsets them into a chain.
    This function also creates a group for each chain link model 
    for easy access to modify or swap out the model.
    
    :param name: string to use when naming objects
    :type name: str
    
    :param units: amount of chain links to create
    :type units: int

    :returns: List of the groups that hold the chain link models.
    :rtype: list
    """
    chain = []
    for x in range(units):
        link = cmds.polyTorus(n=f"{name}{x}", r=0.9, sr=0.15, sa=10, sh=10, ch=False)[0]
        geo_group = cmds.group(link, n=f"{name}{x}_GRP")
        chain.append(geo_group)
    offset_chain(chain, (1,0,0), (90,0,0))
    return chain

def offset_chain(chain, offsetT, offsetR): #try to add toples together instead of individual indexes of tople
    """Offsets chain link models to form a chain.
    
    :param chain: list of chain links or objects to offset
    :type chain: list
    
    :param offsetT: tople of translate offset
    :type offsetT: tople #TODO check if this is correct
    
    :param offsetR: tople of rotate offset
    :type offsetR: tople #TODO check if this is correct
    """
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

#TODO calculate curve points and joints amount
def calculate_chain_ends(chain): #TODO write function
    """Calculates the position of the first and last chain links.
    
    :param chain: list of chain links
    :type chain: list

    :returns: tople of X position of first and last chain links
    :rtype: tople #TODO check if correct
    """
    #get location of first and last chain
    x1 = cmds.xform(chain[0], q=True, t=True, ws=True)[0]
    x2 = cmds.xform(chain[-1], q=True, t=True, ws=True)[0]
    print(f"start and end points: {x1} : {x2}")
    return (x1, x2)


def calculate_point_offset(points, x1, x2): #TODO add variable instead of world variable
    """Calculates the offset between a specified number of points.

    Calculates the offset between a specified 
    number of points in a signle dimintion
    
    :param points: number of points to calculate distance between
    :type points: int

    :param x1: first point
    :type x1: int
    
    :param x2: second point
    :type x2: int

    :returns: Absolute distance between both points.
    :rtype: int
    """
    distance = abs(x2-x1)
    print(f"distance: {distance}")
    #calculate amount of curve points to accompany joints
    curve_point_num = points #calculate_point_num(points) #TODO clean up useless varable
    print(f"curve point num: {curve_point_num}")
    curve_point_distance = distance/(curve_point_num-1)
    print(f"curve point distance: {curve_point_distance}")
    return(curve_point_distance)

def calculate_point_num(points): #TODO add variable instead of using world variable
    """Calculate number of curve points to make.

    :param points: number of points to calculate distance between
    :type points: int

    :returns: Number of points needed.
    :rtype: int
    """
    curve_point_num = (points*4) - 3
    return curve_point_num

#TODO create curve
def create_curve(name, points):
    """Creates a curve.

    Creates chain links and offsets them into a chain.
    This function also creates a group for each chain link model 
    for easy access to modify or swap out the model.
    
    :param name: string to use when naming curve
    :type name: str
    
    :param points: list of toples containing the pos of each curve point
    :type points: list of toples #TODO check if called tople

    :returns: name of curve object
    :rtype: str #TODO check if this is actually a string?
    """
    curve = cmds.curve(n=f"{name}RigCurve", d=3, p=(points[0])) #first curve point
    print(f"received points: {points}")
    for x in range(1,len(points)):
        print(f"points: {points[x]}")
        cmds.curve(curve, a=True, p=(points[x]))
        print(f"what are these?: {points[x]}")
    return curve

def calculate_curve_points(start_point, end_point, total_points):
    """Calculate the points needed in a curve.

    Takes the desired start and end point and calculates the location
    of each point needed to evenly distance out all the points.
    
    :param start_point: x position of start point
    :type start_point: int
    
    :param end_point: x position of end point
    :type end_point: int

    :param total_points: desired number of points
    :type total_points: int

    :returns: list of toples holding position of each curve point.
    :rtype: list of toples #TODO spellcheck tople
    """
    points = []
    offset = start_point
    point_offset = calculate_point_offset(total_points, start_point, end_point)  
    for x in range(total_points):
        #cmds.curve(curve, a=True, p=(offset,0,0))
        points.append((offset,0,0)) #creates an offset in x-axis
        offset = offset + point_offset
    print(f"calculated points: {points}")
    return points


def create_control(name, radius, length, color): #consider breaking shape creation out into it's own functions? or at least the square/rectangle part
    """Creates control for chain rig.

    Creates 2 circles and 2 rectangles and combines them 
    into a nice looking control to animate the rig with.
    
    :param name: string to use when naming objects
    :type name: str
    
    :param radius: desired radius of control
    :type radius: int

    :param length: desired length of control
    :type length: int

    :param color: maya index color of control
    :type color: int  

    :returns: name of the new control created.
    :rtype: string
    """
    end_shapes = []
    side_shapes=[]
    #create ends of control
    for x in range(1,3):
        shape=(cmds.circle(n=f"{name}_end0{x}", c=(0,0,0), d=3, r=radius, nr=(0,1,0), ch=False))[0] #TODO add padding
        change_shape_color(shape, color)
        end_shapes.append(shape)
    cmds.move(0, radius, 0, end_shapes[0])
    cmds.move(0, -radius, 0, end_shapes[1])
    #create sides of control
    side_radius = math.sqrt(2*(radius*radius))
    for y in range(1,3):
        shape=(cmds.circle(n=f"{name}_side0{y}", c=(0,0,0), d=1, r=side_radius, nr=(0,1,0), ch=False, s=4))[0] #TODO add padding
        cmds.rotate(0, 45, 0, shape)
        freeze_transformations(shape)
        #calculate what to scale the shapes by
        #scale_length = length/(radius*2)
        #print(f"side radius: {side_radius}")
        #print(f"scale length: {scale_length}")
        #cmds.scale(scale_length, 1, 1, shape)
        freeze_transformations(shape)
        change_shape_color(shape, color)
        side_shapes.append(shape)
    #stands objects up
    #TODO fix sides shape
    cmds.rotate(90, 0, 0, side_shapes[0], dph=True)
    cmds.rotate(0, 0, 90, side_shapes[1], dph=True)
    for each in (end_shapes + side_shapes):
        freeze_transformations(each)
    new_control = combine_shapes(name, (end_shapes + side_shapes))
    scale_length = length/(radius*2)
    cmds.scale(1, scale_length, 1, new_control)
    freeze_transformations(new_control)
    return new_control

def create_settings_control(name, position, radius, color):
    """Creates control to adjust settings of rig.

    Creates a square control and adds desired attributes to it
    
    :param name: string to use when naming objects
    :type name: str

    :param radius: location to create control
    :type radius: tople of 3 floats
    
    :param radius: desired radius of control
    :type radius: int

    :param color: maya index color of control
    :type color: int    

    :returns: name of the new control created.
    :rtype: str
    """
    control = (cmds.circle(n=f"{name}Settings_CTRL", c=(position), d=1, r=(radius*1.5), nr=(1,0,0), ch=False, s=4))[0]
    cmds.addAttr(ln="stretchy", at="bool", k=True)
    change_shape_color(control, color)
    #TODO lock MSR attrs
    return control

def get_object_shape(object):
    """gets the shape of an object.

    gets the shape of an object by selecting 
    the object and pickwalking down.

    :param object: name of object to get shape of.
    :type object: str

    :returns: name of the shape.
    :rtype: str
    """
    cmds.select(object, r=True)
    cmds.pickWalk(d="down")
    shape = read_selected()[0]
    return shape

def change_shape_color(object, color):
    """changes the color of the given object.

    :param shape: name of object to change color
    :type shape: str

    :param color: maya index color to change color of control
    :type color: int    
    """
    shape = get_object_shape(object)
    cmds.setAttr(f"{shape}.overrideEnabled", 1)
    cmds.setAttr(f"{shape}.overrideColor", color)

def combine_shapes(name, shapes): #TODO find better name for function
    """Combines shapes into one object.

    :param name: string to use when naming objects
    :type name: str
    
    :param shapes: lists of shapes to combinde into new object
    :type shapes: list

    :returns: name of the object created.
    :rtype: string
    """
    cmds.select(d=True)
    new_object = cmds.group(n=name, em=True) #TODO add padding
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
    """freezes transformations of given object.

    provides a simpler way to freeze transformations of an object

    :param object: name of object to freeze transformations
    :type object: str
    
    :param absolute: determines if absolute tag is used.
    :type absolute: bool

    :param translate: determines if translate values are frozen.
    :type translate: bool

    :param rotate: determines if rotate values are frozen.
    :type rotate: bool

    :param scale: determines if scale values are frozen.
    :type scale: bool
    """
    cmds.makeIdentity(object, a=absolute, t=translate, r=rotate, s=scale)

def create_control_rig(name, curve_points, color):
    """Creates rig to control curve.

    Creates controls and joints for the rig. 
    This function also contrains the joints to the controls.

    :param name: string to use when naming objects
    :type name: str
    
    :param curve_points: lists of toples containing desired positions
    :type curve_points: list of toples

    :param color: maya index color to change color of control
    :type color: int

    :returns: tople containing lists of controls and joints.
    :rtype: tople of lists
    """
    point_index = 0
    controls = []
    joints = []
    for x in range(control_number):
        new_control = create_control(f"ik_{name}{x}_CTRL", 
                                         control_radius, 
                                         control_height, 
                                         color)#TODO pad number
        cmds.rotate(0, 0, 90, new_control)
        pos_x = curve_points[point_index][0]
        pos_y = curve_points[point_index][1]
        pos_z = curve_points[point_index][2]
        cmds.move(pos_x, pos_y, pos_z, new_control)
        freeze_transformations(new_control)
        new_joint = cmds.joint(n=f"ik_{name}Rig{x}_JNT", p=curve_points[point_index])#TODO add padding number
        point_index += 4
        controls.append(new_control)
        joints.append(new_joint)
        cmds.parentConstraint(str(new_control), str(new_joint), w=1)
        cmds.scaleConstraint(str(new_control), str(new_joint), w=1)
    return (controls, joints)

def create_chain_joints(name, geometry):
    """create joints for the chain geometry.

    :param name: string to use when naming objects
    :type name: str
    
    :param geometry: list of geometry to create joints for
    :type geometry: list

    :returns: list of joints created
    :rtype: list
    """
    joints = []
    cmds.select(cl=True)
    for x in range(len(geometry)):
        #get location of chain link
        location = cmds.getAttr(f"{geometry[x]}.translate")[0]
        #create link joint
        joint = cmds.joint(n=f"{name}Geo{x}_JNT", p=location) #TODO add padding
        joints.append(joint)
    return joints

def create_ik_spline(name, curve, joints):
    """Creates an ik spline.

    :param name: string to use when naming objects
    :type name: str
    
    :param joints: lists of joints
    :type joints: list

    :returns: name of the object created.
    :rtype: string
    """
    spline = cmds.ikHandle(n=f"{name}_ikHandle", c=curve, sol="ikSplineSolver", sj=joints[0], ee=joints[-1], fj=True)
    return spline[0]

def make_ik_spline_stretchy(curve, joints, control, number):
    """Makes an ik spline into a stretchy rig.

    Makes joints in an ik spline scale in the x axis to make rig stretchy.
    This function also connects a control to toggle the stretchiness
    factor on and off. Control MUST have "stretchy" attr

    :param curve: string to use when naming objects
    :type curve: str
    
    :param joints: lists of joints in ik spline to scale in x value
    :type joints: list

    :param control: control to toggle stretchiness. MUST have "stretchy" attr
    :type control: str
    
    :param number: 
    :type number: int
    """
    curve_info = cmds.createNode("curveInfo")
    shape = get_object_shape(curve)
    cmds.connectAttr(f"{shape}.local", f"{curve_info}.inputCurve")
    divide_node = cmds.createNode("multiplyDivide")
    cmds.connectAttr(f"{curve_info}.arcLength", f"{divide_node}.input1X")
    cmds.setAttr(f"{divide_node}.operation", 2)
    cmds.setAttr(f"{divide_node}.input2X", (number-1))
    condition = cmds.createNode("floatCondition")
    cmds.connectAttr(f"{divide_node}.outputX", f"{condition}.floatA")
    cmds.connectAttr(f"{control}.stretchy", f"{condition}.condition")
    for joint in joints:
        cmds.connectAttr(f"{condition}.outFloat", f"{joint}.scaleX")

#TODO make a control to limit each chain's distance from each other link
#TODO write function to change colors of controls
#TODO clean up
#TODO fix selected meshes work (does not like negative)

def main():
    geometry = read_selected()
    if geometry == []:
        geometry_grps = create_chain_model(chain_name, chain_links)
    else:
        if selection_sort == True:
            geometry.sort()
        geometry_grps = []
        for x in range(len(geometry)): #TODO did something and broke maya
            geo_group = cmds.group(geometry[x], n=f"{chain_name}{x+1}_GRP")
            geometry_grps.append(geo_group)
        #get geometry positions
        #group each geo
    curve_ends = calculate_chain_ends(geometry_grps)
    total_points = calculate_point_num(control_number)
    curve_points = calculate_curve_points(curve_ends[0], curve_ends[1], total_points)
    rig_curve = create_curve(chain_name, curve_points)

    #create control rig
    controls, joints = create_control_rig(chain_name, curve_points, control_color)
    cmds.select(joints, r=True)
    cmds.select(rig_curve, add=True)
    #bindable_objects = joints.copy().append(rig_curve) #TODO unused variable

    curve_dropoff_rate = 4 #range of 0.1-10.0
    cmds.skinCluster(tsb=True, bm=0, sm=1, nw=1, wd=1, mi=2, 
                     omi=True, dr=curve_dropoff_rate, rui=True,) #TODO what is this doing again?
    first_control_position = cmds.xform(controls[0], q=True, t=True, ws=True)
    print(f"controls: {controls}")
    print(f"location of first control: {first_control_position}")
    settings_control = create_settings_control(chain_name, 
                                               first_control_position, 
                                               control_radius, 
                                               control_settings_color)
    cmds.parent(settings_control, controls[0])

    #connecting links to curve
    chain_joints = create_chain_joints(chain_name, geometry_grps)
    ik_handle = create_ik_spline(chain_name, rig_curve, chain_joints)
    for x in range(len(chain_joints)):
        cmds.parentConstraint(str(chain_joints[x]), str(geometry_grps[x]), w=1, mo=True)
    make_ik_spline_stretchy(rig_curve, chain_joints, settings_control, chain_links)

    #group stuff in final hiearchy
    control_grp = cmds.group(controls, n="controls")
    control_joint_grp = cmds.group(joints, n="control_joints")
    chain_joint_grp = cmds.group(chain_joints[0], n="chain_joints")
    joint_grp = cmds.group([chain_joint_grp, control_joint_grp, rig_curve, ik_handle], n="joints")
    cmds.setAttr(f"{joint_grp}.visibility", 0)
    geo_grp = cmds.group(geometry_grps, n="geometry")
    final_rig_grp = cmds.group([control_grp, joint_grp, geo_grp], n=f"{chain_name}_rig")
    

if __name__ == "__main__":
    main()