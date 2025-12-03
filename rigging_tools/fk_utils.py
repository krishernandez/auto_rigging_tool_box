#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author: Kris Hernandez

:synopsis:
Module for any fk utils.

:description:
This module contains utils for making with fk utils, such as creating finger, limb and
neck controls.

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
import maya.cmds as cmds


def create_fk_controls_from_selection():
    """
    Creates FK controls for for nay selected joint chain
    """

    joints = cmds.ls(sl=True, type="joint")

    if len(joints) == 0:
        cmds.warning("No joints selected! Select a joint chain and try again.")
        return
    if len(joints) < 2:
        cmds.warning("Select at least TWO joints in order to create FK controls.")
        return

    # Create a master control group
    top_grp = cmds.group(empty=True, name="GRP_FK_controls")

    parent_ctrl = None

    # Iterate through selected joints
    for i, jnt in enumerate(joints):
        ctrl_name = f"{jnt}_FK_CTRL"

        ctrl = cmds.circle(name=ctrl_name, normal=[1, 0, 0], radius=0.5)[0]

        cmds.matchTransform(ctrl, jnt)

        if parent_ctrl:
            cmds.parent(ctrl, parent_ctrl)
        else:
            cmds.parent(ctrl, top_grp)

        # Constrain joint to control
        cmds.parentConstraint(ctrl, jnt, mo=True)

        parent_ctrl = ctrl

    cmds.select(clear=True)
    cmds.inViewMessage(
        amg=f"✅ FK controls created for <hl>{len(joints)}</hl> joints",
        pos="topCenter",
        fade=True
    )



