# ----------------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------ HEADER --#

"""
:author:
    Kris Hernandez

:synopsis:


:description:


:applications:
    Maya.

:see_also:
"""

# ----------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------- IMPORTS --#

# Default Python Imports
import maya.cmds as cmds


# ----------------------------------------------------------------------------------------#
# --------------------------------------------------------------------------- FUNCTIONS --#

def rename_objects_by_type():
    # Get selected objects
    selected_objects = cmds.ls(selection=True)

    # Create dictionaries for object type prefixes
    type_prefix = {
        'mesh': 'geo',
        'joint': 'jnt',
        'nurbsCurve': 'crv',
    }

    # Loop through each selected object
    for obj in selected_objects:
        # Get object type
        obj_type = cmds.objectType(obj)

        # Find out the prefix based on object type
        prefix = type_prefix.get(obj_type, 'obj')

        # Create a new name with a prefix and a number
        new_name = f"{prefix}_{obj}_01"

        # Rename the object
        cmds.rename(obj, new_name)
        print(f"Renamed {obj} to {new_name}")


# Run the function
rename_objects_by_type()