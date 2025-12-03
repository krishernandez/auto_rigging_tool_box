#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author: Kris Hernandez

:synopsis:
Module for skin utils.

:description:
This module contains utils for basic skin utils for rigging such as binding, deleting
and mirroring.

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

def bind_skin(max_influences=4, dropoff=4.0):
    """
    Binds selected joints to the selected mesh.
    """
    sel = cmds.ls(sl=True)

    if len(sel) < 2:
        cmds.warning("Select at least one joint and a mesh.")
        return

    mesh = sel[-1]
    joints = sel[:-1]

    try:
        cmds.skinCluster(
            joints,
            mesh,
            toSelectedBones=True,
            maximumInfluences=max_influences,
            dropoffRate=dropoff,
            normalizeWeights=1,
            name=f"{mesh}_skinCluster"
        )
        cmds.inViewMessage(amg="✅ Skin bound.", pos="topCenter", fade=True)
    except:
        cmds.warning("Failed to bind skin. Check your selection.")

def mirror_skin_weights(direction="leftToRight"):
    """
    Mirrors skin weights on the selected mesh.
    direction options: 'leftToRight' or 'rightToLeft'
    """

    sel = cmds.ls(sl=True)

    if not sel:
        cmds.warning("Select a skinned mesh.")
        return

    mesh = sel[0]

    skin = cmds.ls(cmds.listHistory(mesh), type="skinCluster")
    if not skin:
        cmds.warning("No skinCluster found on selected mesh.")
        return

    # Maya uses these conventions
    if direction == "leftToRight":
        dir_flag = "YZ"
    else:
        dir_flag = "YZ"

    try:
        cmds.copySkinWeights(
            surfaceAssociation="closestPoint",
            influenceAssociation="closestJoint",
            mirrorMode=dir_flag,
            noMirroring=False
        )
        cmds.inViewMessage(amg="✅ Skin weights mirrored.", pos="topCenter", fade=True)
    except:
        cmds.warning("Skin weight mirroring failed.")

def delete_skin():
    """
    Deletes the skinCluster on the selected mesh (if any).
    """
    sel = cmds.ls(sl=True)
    if not sel:
        cmds.warning("Select a mesh with a skinCluster.")
        return

    mesh = sel[0]
    skin = cmds.ls(cmds.listHistory(mesh), type="skinCluster")

    if not skin:
        cmds.warning("No skinCluster found.")
        return

    try:
        cmds.delete(skin)
        cmds.inViewMessage(amg="✅️ Skin binding removed.", pos="topCenter", fade=True)
    except:
        cmds.warning("Could not delete skinCluster.")
