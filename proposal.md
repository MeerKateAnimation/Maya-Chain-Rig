# Maya Chain Rig

## Repository
[GitHub Repository](https://github.com/MeerKateAnimation/Maya-Chain-Rig)

## Description
This tool will be able to create a custom chain rig in Maya. Everything about the rig creation will be automated with python with a few customizable attributes.

## Features
- Creates a curve with controls to animate
	- Using Python, I can skin points of the curve to seperate joints that are constrained to the controls.
- Constrains chain links to curve 
	- Using Python, I will align all the chain links and set up nodes to calculate the distance each chain link needs to be from each other.
- Pop-up window 
	- I would like to make a pop-up window for users to easily change attributes without understanding and changing the code.

## Challenges
- I will be looking a lot at [Maya's PyMEL Documentaion](https://help.autodesk.com/cloudhelp/2018/CHS/Maya-Tech-Docs/CommandsPython/)
- I will need to look into how to create a pop-up window in Maya
- Short sentence of any skill or topic that needs to be learnt or researched.

## Outcomes
Ideal Outcome:
- A chain rig that can be costomizable based on the animator's needs. Includes custom number of controls upon creation, a pop-up window to input variables to customize,

Minimal Viable Outcome:
- To make a chain rig that is not customizable.

## Milestones

- Week 1
  1. Make system to create animation controls
  2. Make system to create a curve and skin it to joints

- Week 2
  1. Make system to read selected chain link models and align them with the control curve
  2. Make system to space each chain link evenly on the control curve

- Week N (Final)
  1. Make pop-up window with options to customize rig
  2. Make a way to limit how far each chain link can get from it's neighboring links (to avoid the chain links clipping into each other)
