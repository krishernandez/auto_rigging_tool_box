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

    #General Logic
    def freeze_transforms():
        """Freezes transforms on selected objects."""
        sel = cmds.ls(selection=True)
        if not sel:
            cmds.warning("No objects selected.")
            return
        cmds.makeIdentity(sel, apply=True, translate=True, rotate=True, scale=True, normal=False)
        cmds.inViewMessage(amg="✅ Transforms frozen!", pos="topCenter", fade=True)


    def delete_history():
        """Deletes history on selected objects."""
        sel = cmds.ls(selection=True)
        if not sel:
            cmds.warning("No objects selected.")
            return

        cmds.delete(sel, constructionHistory=True)
        cmds.inViewMessage(amg="✅ History deleted!", pos="topCenter", fade=True)


    def center_pivot():
        """Centers pivot on selected objects."""
        sel = cmds.ls(selection=True)
        if not sel:
            cmds.warning("No objects selected.")
            return
        cmds.xform(sel, centerPivots=True)
        cmds.inViewMessage(amg="✅ Pivot centered!", pos="topCenter", fade=True)


    def mirror_joints():
        """Mirrors selected joints."""
        sel = cmds.ls(selection=True, type="joint")
        if not sel:
            cmds.warning("Select at least one joint to mirror.")
            return
        for joint in sel:
            cmds.mirrorJoint(joint, mirrorYZ=True, mirrorBehavior=True, searchReplace=("L_", "R_"))
        cmds.inViewMessage(amg="✅ Joints mirrored!", pos="topCenter", fade=True)


    def orient_joints():
        """Orients selected joints."""
        sel = cmds.ls(selection=True, type="joint")
        if not sel:
            cmds.warning("Select joints to orient.")
            return
        for jnt in sel:
            cmds.joint(jnt, edit=True, orientJoint="xyz", secondaryAxisOrient="yup", zeroScaleOrient=True)
        cmds.inViewMessage(amg="✅ Joints oriented!", pos="topCenter", fade=True)

    #Transformation Logic
    def reset_translation():
        """
        Resets the translation of selected objects to (0, 0, 0).
        """
        sel = cmds.ls(selection=True) or []
        if not sel:
            cmds.warning("No object was selected.")
            return

        for obj in sel:
            cmds.setAttr(f"{obj}.translateX", 0)
            cmds.setAttr(f"{obj}.translateY", 0)
            cmds.setAttr(f"{obj}.translateZ", 0)
        cmds.inViewMessage(amg="✅ Translation Reset!", pos="topCenter", fade=True)


    def reset_rotation():
        """
        Resets the rotation of selected objects to (0, 0, 0).
        """
        sel = cmds.ls(selection=True) or []
        sel = cmds.ls(selection=True) or []
        if not sel:
            cmds.warning("No object was selected.")
            return

        for obj in sel:
            cmds.setAttr(f"{obj}.rotateX", 0)
            cmds.setAttr(f"{obj}.rotateY", 0)
            cmds.setAttr(f"{obj}.rotateZ", 0)
        cmds.inViewMessage(amg="✅ Rotation Reset!", pos="topCenter", fade=True)


    def reset_translation_rotation():
        """
        Resets both translation and rotation of selected objects.

        :return: Success of the reset translation and rotation function.
        :type: bool
        """
        sel = cmds.ls(selection=True) or []
        if not sel:
            cmds.warning("No object was selected.")
            return

        for obj in sel:
            cmds.setAttr(f"{obj}.translateX", 0)
            cmds.setAttr(f"{obj}.translateY", 0)
            cmds.setAttr(f"{obj}.translateZ", 0)
            cmds.setAttr(f"{obj}.rotateX", 0)
            cmds.setAttr(f"{obj}.rotateY", 0)
            cmds.setAttr(f"{obj}.rotateZ", 0)
        cmds.inViewMessage(amg="✅ Translation and Rotation Reset!", pos="topCenter", fade=True)


    def reset_scale():
        """
        Resets the scale of selected objects to (1, 1, 1).

        :return: Success of the reset scale function.
        :type: bool
        """
        sel = cmds.ls(selection=True) or []
        if not sel:
            cmds.warning("No object was selected.")
            return

        for obj in sel:
            cmds.setAttr(f"{obj}.scaleX", 1)
            cmds.setAttr(f"{obj}.scaleY", 1)
            cmds.setAttr(f"{obj}.scaleZ", 1)
        cmds.inViewMessage(amg="✅ Scale Reset!", pos="topCenter", fade=True)

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#