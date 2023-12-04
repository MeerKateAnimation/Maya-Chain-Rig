# Maya-Chain-Rig

## Demo
Demo Video: <URL>

## GitHub Repository
GitHub Repo: https://github.com/MeerKateAnimation/Maya-Chain-Rig

## Description
This tool will be able to create a custom chain rig in Maya.

This script automatically creates a rig for a chain in Maya. 
All you have to do is select your chain geometry and run the script.

To break down how the rig works:
You have a certain number of controls that each have a joint constrained to them.
These joints have a curve skinned to them.
Scaling the control in the X-axis controls how sharp or soft the curve can be.

This script also creates a series of joints and creates an IK spline to connect it to the previous curve.

Each chain link is constrained to a joint with a parent constraint.

There is also a settings control parented to the first chain control with an option to turn "stretchy" on.
This makes the ends of the chain match both ends of the curve and evenly distributes each joint by using the scale attribute.
No matter how long or what shape the curve takes, the chain will take up the entire length of the curve.
Note that this can go too far, and you have to be careful when animating not to "break" the rig.

Changeable Attributes:
Before running the script, you can change attributes to adjust how the rig will be made.

selection_sort - bool 
When this is True, it will sort the selected geometry alphabetically. 
When this is False, the order the geometry was selected will determine the order of the chain links.

chain_name - string
This will let you insert a different name that the rig will use when naming nodes.

chain_links - int
This will let you control how many links you want to be created when no geometry is selected.
Note that the script ignores this if you have selected geometry.

control_number - int
This lets you choose how many controls you would like in your rig.

control_radius - int or float
This will control the radius of the control shape.

control_height - int or float
This will control the height or length of the control shape.

control_color - int
This will change the color of the main controls.
The value refers to an int from Maya's Color Index.

control_settings_color - int
This will change the color of the settings control.
The value refers to an int from Maya's Color Index.

curve_dropoff_rate - int or float (The range is 0.1-10.0)
This affects the skinning of the curve and requires a knowledge of skinning in Maya.
