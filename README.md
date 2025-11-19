# PROJECT TITLE: Rigging Automation Tool Box 

# DESCRIPTION
This tool helps speed up the process of a rigger's workflow. With a simple layout followed by tips and 
instructions, the goal of this tool is to be as user-friendly as possible. 
 
# FEATURES
- General utils such as freezing transformations, deleting history and centering pivots 
- Streamline transformation tools 
- Streamline joint manipulation such as mirroring and orientating joints 
- Custom curve util options. Set override colors and custom curve shapes in one tool box 
- Automatic FK and IK limb set up as well as use for auto FK finger controls set up 
- Automative Squash and stretch functions with the option to add pole vectors 

# BUG LOG
- Squash and stretch functions currently not functional. 
- Pole vector selection currently not functional 
- IK finger set up to only work when joints are renamed to the right prefix
- Currently, the only way to bring in this rigging tool box is to call it within the maya script.


# TODO 
- Add the option to rename joints and controls based on a set dictionary 
- Add an automation ribbon joint tool 
- Add a simple shortcuts to bind, mirror and delete skin binding
- Add a general constrain options when using custom curve utils 
- Add the custom designed IK handle to the IK limbs automation tool
- When dragging in the final toolbox, make it show up in one of the maya menus 
- Clean up notification systems such as the success of the operation and warning commands 
- Add text box for tips, tricks and instructions on how to use each tool 
- Clean up and rename certain tabs on tool box 
- Clean up documentation