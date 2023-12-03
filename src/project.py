import maya.cmds as cmds
import math


'''------------------------
   CHANGEABLE ATTRIBUTES
------------------------'''
selection_sort = True

chain_name = "chain" 
chain_links = 20 #only applies if selection is empty

control_number = 3
control_radius = 1
control_height = 3
control_color = 22 #maya color index
control_settings_color = 18 #maya color index

curve_dropoff_rate = 4 #range of 0.1-10.0 (affects skinning of rig curve)
'''---------------------'''

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
    :rtype: lists
    """
    chain = []
    for x in range(units):
        link = cmds.polyTorus(n=f"{name}{x}_GEO", r=0.9, sr=0.15, 
                              sa=10, sh=10, ch=False)[0]
        chain.append(link)
    offset_chain(chain, (1,0,0), (90,0,0))
    return chain

def offset_chain(chain, offsetT, offsetR):
    """Offsets chain link models to form a chain.
    
    :param chain: list of chain links or objects to offset
    :type chain: list
    
    :param offsetT: tuple of translate offset
    :type offsetT: tuple
    
    :param offsetR: tuple of rotate offset
    :type offsetR: tuple
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

def calculate_chain_ends(chain):
    """Calculates the position of the first and last chain links.
    
    :param chain: list of chain links
    :type chain: list

    :returns: tuple of X position of first and last chain links
    :rtype: tuple
    """
    print(f"chain[0]: {chain[0]}")
    x1 = cmds.xform(chain[0], q=True, t=True, ws=True)[0]
    x2 = cmds.xform(chain[-1], q=True, t=True, ws=True)[0]
    return (x1, x2)

def calculate_point_offset(points, x1, x2):
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
    curve_point_distance = distance/(points-1)
    return(curve_point_distance)

def calculate_point_num(points):
    """Calculate number of curve points to make.

    :param points: number of points to calculate distance between
    :type points: int

    :returns: Number of points needed.
    :rtype: int
    """
    curve_point_num = (points*4) - 3
    return curve_point_num

def create_curve(name, points):
    """Creates a curve.

    Creates chain links and offsets them into a chain.
    This function also creates a group for each chain link model 
    for easy access to modify or swap out the model.
    
    :param name: string to use when naming curve
    :type name: str
    
    :param points: list of tuples containing the pos of each curve point
    :type points: list of tuples 

    :returns: name of curve object
    :rtype: str 
    """
    #creates first curve point
    curve = cmds.curve(n=f"{name}RigCurve", d=3, p=(points[0])) 
    for x in range(1,len(points)):
        cmds.curve(curve, a=True, p=(points[x]))
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

    :returns: list of tuples holding position of each curve point.
    :rtype: list of tuples
    """
    points = []
    offset = start_point
    point_offset = calculate_point_offset(total_points, start_point, end_point)  
    for x in range(total_points):
        points.append((offset,0,0)) #creates an offset in x-axis
        offset = offset + point_offset
    return points

def create_control(name, radius, length, color): 
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
        shape=(cmds.circle(n=f"{name}_end0{x}", c=(0,0,0), d=3, 
                           r=radius, nr=(0,1,0), ch=False))[0]
        change_shape_color(shape, color)
        end_shapes.append(shape)
    cmds.move(0, radius, 0, end_shapes[0])
    cmds.move(0, -radius, 0, end_shapes[1])
    #create sides of control
    side_radius = math.sqrt(2*(radius*radius))
    for y in range(1,3):
        shape=(cmds.circle(n=f"{name}_side0{y}", c=(0,0,0), d=1, 
                           r=side_radius, nr=(0,1,0), ch=False, s=4))[0]
        cmds.rotate(0, 45, 0, shape)
        freeze_transformations(shape)
        change_shape_color(shape, color)
        side_shapes.append(shape)
    #orient side objects
    cmds.rotate(90, 0, 0, side_shapes[0], dph=True)
    cmds.rotate(0, 0, 90, side_shapes[1], dph=True)
    for each in (end_shapes + side_shapes):
        freeze_transformations(each)
    new_control = combine_shapes(name, (end_shapes + side_shapes))
    scale_length = length/(radius*2)
    cmds.scale(1, scale_length, 1, new_control)
    freeze_transformations(new_control)
    return new_control

def create_settings_control(name, radius, color):
    """Creates control to adjust settings of rig.

    Creates a square control and adds desired attributes to it
    
    :param name: string to use when naming objects
    :type name: str
    
    :param radius: desired radius of control
    :type radius: int

    :param color: maya index color of control
    :type color: int    

    :returns: name of the new control created.
    :rtype: str
    """
    control = (cmds.circle(n=f"{name}Settings_CTRL", c=(0,0,0), d=1, 
                           r=(radius*1.5), nr=(1,0,0), ch=False, s=4))[0]
    cmds.addAttr(ln="stretchy", at="bool", k=True)
    change_shape_color(control, color)
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

def combine_shapes(name, shapes):
    """Combines shapes into one object.

    :param name: string to use when naming objects
    :type name: str
    
    :param shapes: lists of shapes to combinde into new object
    :type shapes: list

    :returns: name of the object created.
    :rtype: string
    """
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

def freeze_transformations(object, absolute=True, translate=True, 
                           rotate=True, scale=True):
    """freezes transformations of given object.

    Provides a simpler way to freeze transformations of an object

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

def create_control_rig(name, curve_points, control_num, radius, height, 
                       color, settings_color):
    """Creates rig to control curve.

    Creates controls and joints for the rig. 
    This function also contrains the joints to the controls.

    :param name: string to use when naming objects
    :type name: str
    
    :param curve_points: lists of tuples containing desired positions
    :type curve_points: list of tuples

    :param control_num: number of controls to make
    :type control num: int

    :param radius: desired radius of controls
    :type radius: int

    :param height: desired height of controls
    :type heigt: int

    :param color: maya index color to change color of control
    :type color: int

    :param settings_color: maya index color to change color of 
    settings control
    :type settings_colir: int

    :returns: tuple containing lists of controls, list of joints,
    & setting control name. 
    :rtype: tuple of 2 lists and 1 string
    """
    point_index = 0
    controls = []
    joints = []
    for x in range(control_num):
        new_control = create_control(f"ik_{name}{x}_CTRL", radius, 
                                     height, color)
        cmds.rotate(0, 0, 90, new_control)
        if x == 0:
            settings_control = create_settings_control(name,
                                                       control_radius, 
                                                       settings_color)
            cmds.parent(settings_control, new_control)
        pos_x = curve_points[point_index][0]
        pos_y = curve_points[point_index][1]
        pos_z = curve_points[point_index][2]
        cmds.move(pos_x, pos_y, pos_z, new_control)
        freeze_transformations(new_control)
        new_joint = cmds.joint(n=f"ik_{name}Rig{x}_JNT", 
                               p=curve_points[point_index])
        point_index += 4
        controls.append(new_control)
        joints.append(new_joint)
        cmds.parentConstraint(str(new_control), str(new_joint), w=1)
        cmds.scaleConstraint(str(new_control), str(new_joint), w=1)
    lock_attrs(settings_control)
    return (controls, joints, settings_control)

def lock_attrs(object, attrs=["tx", "ty", "tz", 
                              "rx", "ry", "rz", 
                              "sx", "sy", "sz"]):
    """Locks given attributes.

    Locks attributes on given object. 
    Defaults to locking all MSR attributes

    :param object: name of object to lock attributes
    :type object: str
    
    :param attrs: list of attrs to lock
    :type attrs: list of str
    """
    for attr in attrs:
        cmds.setAttr(f"{object}.{attr}", l=True)
    
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
        location = cmds.getAttr(f"{geometry[x]}.translate")[0]
        joint = cmds.joint(n=f"{name}Geo{x}_JNT", p=location)
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
    spline = cmds.ikHandle(n=f"{name}_ikHandle", c=curve, sol="ikSplineSolver", 
                           sj=joints[0], ee=joints[-1], fj=True)
    return spline[0]

def make_ik_spline_stretchy(curve, joints, control):
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
    """
    curve_info = cmds.createNode("curveInfo")
    shape = get_object_shape(curve)
    cmds.connectAttr(f"{shape}.local", f"{curve_info}.inputCurve")

    multiply_node = cmds.createNode("multiplyDivide", n="multiplyNode")
    multiplier = 1/(cmds.getAttr(f"{curve_info}.arcLength"))
    cmds.setAttr(f"{multiply_node}.input2X", multiplier)
    cmds.setAttr(f"{multiply_node}.operation", 1)
    cmds.connectAttr(f"{curve_info}.arcLength", f"{multiply_node}.input1X")

    condition = cmds.createNode("floatCondition", n="stretchyToggle")
    cmds.connectAttr(f"{multiply_node}.outputX", f"{condition}.floatA")
    cmds.connectAttr(f"{control}.stretchy", f"{condition}.condition")
    for joint in joints:
        cmds.connectAttr(f"{condition}.outFloat", f"{joint}.scaleX")

def main():
    #reads selected geometry or creates geometry if none is selected
    geometry = read_selected()
    if geometry == []:
        geometry = create_chain_model(chain_name, chain_links)
        print(f"geometry: {geometry}")
    else:
        if selection_sort == True:
            geometry.sort()
    geometry_grps = []
    for x in range(len(geometry)): 
        geo_group = cmds.group(geometry[x], n=f"{chain_name}{x}_GRP")
        geometry_grps.append(geo_group)
    curve_ends = calculate_chain_ends(geometry)
    total_points = calculate_point_num(control_number)
    curve_points = calculate_curve_points(curve_ends[0], 
                                          curve_ends[1], 
                                          total_points)
    rig_curve = create_curve(chain_name, curve_points)

    #create control rig
    control_rig = create_control_rig(chain_name, curve_points, control_number, 
                       control_radius, control_height,
                       control_color, control_settings_color)
    controls, joints, settings_control = control_rig
    cmds.select(joints, r=True)
    cmds.select(rig_curve, add=True)
    cmds.skinCluster(tsb=True, bm=0, sm=1, nw=1, wd=1, mi=2, 
                     omi=True, dr=curve_dropoff_rate, rui=True,)

    #connecting links to curve
    chain_joints = create_chain_joints(chain_name, geometry) 
    ik_handle = create_ik_spline(chain_name, rig_curve, chain_joints)
    for x in range(len(chain_joints)):
        cmds.parentConstraint(str(chain_joints[x]), geometry_grps[x], 
                              w=1, mo=True)
    make_ik_spline_stretchy(rig_curve, chain_joints, settings_control)

    #group objects into final hiearchy
    control_grp = cmds.group(controls, n="controls")
    control_joint_grp = cmds.group(joints, n="control_joints")
    chain_joint_grp = cmds.group(chain_joints[0], n="chain_joints")
    joint_grp = cmds.group([chain_joint_grp, control_joint_grp, rig_curve, 
                            ik_handle], n="joints")
    cmds.setAttr(f"{joint_grp}.visibility", 0)
    geo_grp = cmds.group(geometry_grps, n="geometry")
    cmds.group([control_grp, joint_grp, geo_grp], n=f"{chain_name}_rig")
    

if __name__ == "__main__":
    main()