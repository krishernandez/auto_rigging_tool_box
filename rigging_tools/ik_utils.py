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
N/A

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
    if selection:
        sel = cmds.ls(sl=True)
        if len(sel) < 3:
            cmds.warning("Select at least 3 joints (shoulder/hip, elbow/knee, wrist/ankle).")
            return
        joints = sel[:3]
    else:
        cmds.warning("No joints selected.")
        return

    start_joint, mid_joint, end_joint = joints

    # Detect limb axis direction (X, Y, or Z)
    start_pos = cmds.xform(start_joint, q=True, ws=True, t=True)
    end_pos   = cmds.xform(end_joint,   q=True, ws=True, t=True)

    vec = [
        end_pos[0] - start_pos[0],
        end_pos[1] - start_pos[1],
        end_pos[2] - start_pos[2]
    ]

    # Determine dominant axis
    axis_index = max(range(3), key=lambda i: abs(vec[i]))

    # Map axis - circle normal
    axis_normals = {
        0: [1, 0, 0],   # X axis limb - face X
        1: [0, 1, 0],   # Y axis limb - face Y
        2: [0, 0, 1]    # Z axis limb - face Z
    }

    normal = axis_normals[axis_index]

    # Create IK handle
    ik_name = "{}_IK".format(limb_type)
    ik_handle = cmds.ikHandle(
        name=ik_name,
        startJoint=start_joint,
        endEffector=end_joint,
        solver="ikRPsolver"
    )[0]

    # Create a control at the IK handle position
    ctrl_name = "{}_CTRL".format(limb_type)
    ctrl = cmds.circle(name=ctrl_name, normal=normal, radius=2)[0]

    cmds.delete(cmds.pointConstraint(ik_handle, ctrl))
    cmds.parent(ik_handle, ctrl)

    cmds.inViewMessage(
        amg=f"✅ IK setup created for <hl>{limb_type}</hl> limb",
        pos="topCenter",
        fade=True
    )
    print("Created IK handle '{}' with control '{}'.".format(ik_handle, ctrl))
    return ik_handle
