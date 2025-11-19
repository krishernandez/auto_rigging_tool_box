#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author: Kris Hernandez

:synopsis:


:description:


:applications:
    Maya

:see_also:

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in
import os

# Third party
import maya.cmds as cmds
try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except ImportError:
    from PySide2 import QtGui, QtCore, QtWidgets

# Internal

# External


#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

def create_fk_controls(finger_prefix, num_joints=3):
    """
    Creates FK controls for a given finger prefix
    """
    finger_joints = []
    for i in range(1, num_joints + 1):
        joint_name = f"{finger_prefix}{i:02d}_bind_JNT"
        if cmds.objExists(joint_name):
            finger_joints.append(joint_name)
        else:
            cmds.warning(f"Joint not found: {joint_name}. Skipping.")
            return

    if not finger_joints:
        cmds.warning(f"No joints found for {finger_prefix}. Aborting.")
        return

    # Create FK controls
    parent_control = None
    for i, joint in enumerate(finger_joints, start=1):
        control_name = f"CTRL_{finger_prefix}{i:02d}"
        control = cmds.circle(name=control_name, normal=[1, 0, 0], radius=0.5)[0]
        cmds.matchTransform(control, joint)

        # Parent structure
        if parent_control:
            cmds.parent(control, parent_control)
        else:
            grp_name = f"GRP_{finger_prefix}_controls"
            if not cmds.objExists(grp_name):
                cmds.group(empty=True, name=grp_name)
            cmds.parent(control, grp_name)

        # Constraint
        cmds.parentConstraint(control, joint, maintainOffset=True)

        parent_control = control

    cmds.select(clear=True)
    cmds.inViewMessage(amg="✅ FK rig created for {finger_prefix} finger.", pos="topCenter", fade=True)


# --------------

#Finger Fumctions

def create_index_fk():
    create_fk_controls("L_index", 3)

def create_middle_fk():
    create_fk_controls("L_middle", 3)

def create_ring_fk():
    create_fk_controls("L_ring", 3)

def create_pinky_fk():
    create_fk_controls("L_pinky", 3)

def create_thumb_fk():
    create_fk_controls("L_thumb", 3)
