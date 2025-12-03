 #!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author: Kris Hernandez

:synopsis:
Module for any ik utils. 

:description:
This module contains utils for making with ik utils, such as creating ik rigs for legs and arms.

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

def create_ik_controls(limb_type="arm", selection=True):
    """
    Creates an IK handle for a selected limb (arm or leg).
    """
    # Get selected joints
    if selection:
        sel = cmds.ls(sl=True)
        if len(sel) < 3:
            cmds.warning("Select at least 3 joints (shoulder/hip, elbow/knee, wrist/ankle).")
            return
        joints = sel[:3]
    else:
        cmds.warning("No joints selected.")
        return

    start_joint = joints[0]
    mid_joint = joints[1]
    end_joint = joints[2]

    # Name the IK handle
    ik_name = "{}_IK".format(limb_type)

    # Create the IK handle
    ik_handle = cmds.ikHandle(
        name=ik_name,
        startJoint=start_joint,
        endEffector=end_joint,
        solver="ikRPsolver"
    )[0]

    # Create a control at the IK handle position
    ctrl_name = "{}_CTRL".format(limb_type)
    ctrl = cmds.circle(name=ctrl_name, normal=[1,0,0], radius=2)[0]
    cmds.delete(cmds.pointConstraint(ik_handle, ctrl))
    cmds.parent(ik_handle, ctrl)

    cmds.select(clear=True)
    cmds.inViewMessage(
        amg=f"✅ IK setup created for <hl>{limb_type}</hl> limb",
        pos="topCenter",
        fade=True
    )
    print("Created IK handle '{}' with control '{}'.".format(ik_handle, ctrl))
    return ik_handle