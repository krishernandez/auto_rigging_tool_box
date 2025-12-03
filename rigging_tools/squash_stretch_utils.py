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

def create_squash_stretch_limb():
    """
    Creates squash & stretch setup for a 3-joint limb.
    Select the control FIRST, then the 3 joints in order.
    Example selection: ctrl, upperJnt, lowerJnt, endJnt
    """

    sel = cmds.ls(sl=True)

    if len(sel) != 4:
        cmds.error("Select the CONTROL first, then UPPER → LOWER → END joints.")

    ctrl, upper, lower, end = sel


    # Measure original length of the limb
    upper_pos = cmds.xform(upper, q=True, ws=True, t=True)
    lower_pos = cmds.xform(lower, q=True, ws=True, t=True)
    end_pos   = cmds.xform(end, q=True, ws=True, t=True)

    upper_len = cmds.getAttr(upper + ".translateX")
    lower_len = cmds.getAttr(lower + ".translateX")
    original_length = abs(upper_len) + abs(lower_len)

    # Create distance measuring setup
    start_loc = cmds.spaceLocator(name=upper + "_distStart_LOC")[0]
    end_loc = cmds.spaceLocator(name=end + "_distEnd_LOC")[0]

    cmds.delete(cmds.pointConstraint(upper, start_loc))
    cmds.delete(cmds.pointConstraint(end, end_loc))

    dist = cmds.createNode("distanceBetween", name=upper + "_distanceBetween")

    cmds.connectAttr(start_loc + ".worldPosition[0]", dist + ".point1")
    cmds.connectAttr(end_loc + ".worldPosition[0]", dist + ".point2")

    # Create a stretch ratio
    md = cmds.createNode("multiplyDivide", name=upper + "_stretch_MD")
    cmds.setAttr(md + ".operation", 2)  # Divide

    cmds.connectAttr(dist + ".distance", md + ".input1X")
    cmds.setAttr(md + ".input2X", original_length)

    # Add attributes to control
    if not cmds.attributeQuery("stretch", node=ctrl, exists=True):
        cmds.addAttr(ctrl, ln="stretch", min=0, max=1, dv=1, k=True)
    if not cmds.attributeQuery("squash", node=ctrl, exists=True):
        cmds.addAttr(ctrl, ln="squash", min=0, max=1, dv=1, k=True)

    # Multiply stretch factor
    stretch_md = cmds.createNode("multiplyDivide", name=upper + "_stretchSwitch_MD")
    cmds.connectAttr(md + ".outputX", stretch_md + ".input1X")
    cmds.connectAttr(ctrl + ".stretch", stretch_md + ".input2X")

    # Drive joint scaling
    cmds.connectAttr(stretch_md + ".outputX", upper + ".scaleX")
    cmds.connectAttr(stretch_md + ".outputX", lower + ".scaleX")

    # 7. Squash on Y/Z axes
    sqrt_md = cmds.createNode("multiplyDivide", name=upper + "_sqrt_MD")
    cmds.setAttr(sqrt_md + ".operation", 3)  # Power
    cmds.connectAttr(stretch_md + ".outputX", sqrt_md + ".input1X")
    cmds.setAttr(sqrt_md + ".input2X", 0.5)  # Square root

    inv_md = cmds.createNode("multiplyDivide", name=upper + "_invSquash_MD")
    cmds.setAttr(inv_md + ".operation", 2)  # Divide (1 / sqrt(stretch))
    cmds.setAttr(inv_md + ".input1X", 1)
    cmds.connectAttr(sqrt_md + ".outputX", inv_md + ".input2X")

    # Add squash switch
    squash_md = cmds.createNode("multiplyDivide", name=upper + "_squashSwitch_MD")
    cmds.connectAttr(inv_md + ".outputX", squash_md + ".input1X")
    cmds.connectAttr(ctrl + ".squash",    squash_md + ".input2X")

    # Drive joint scales
    for jnt in (upper, lower):
        cmds.connectAttr(squash_md + ".outputX", jnt + ".scaleY")
        cmds.connectAttr(squash_md + ".outputX", jnt + ".scaleZ")

    cmds.select(clear=True)
    cmds.inViewMessage(
        amg=f"✅ Squash & Stretch created for <hl>{upper}</hl>, <hl>{lower}</hl>, <hl>{end}</hl>",
        pos="topCenter",
        fade=True
    )

    print("Squash & Stretch created for:", upper, lower, end)
