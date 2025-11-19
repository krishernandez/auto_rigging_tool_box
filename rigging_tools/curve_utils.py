#!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author: Kris Hernandez

:synopsis:
Module for custom curve utils. 


:description:
This module contains custom curve utils including: creating custom curves, overwriting curve
colors and setting default colors for a basic rigging workflow. 


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

def set_override_color(color_index):
    """
    This function s the override color of an object in Maya when selected.
    """
    sel = cmds.ls(selection=True) or []
    sel = cmds.ls(selection=True) or []
    if not sel:
        cmds.warning("No object was selected.")
        return

    for obj in sel:
        shapes = cmds.listRelatives(obj, shapes=True) or []
        for shape in shapes:
            cmds.setAttr(f"{shape}.overrideEnabled", 1)
            cmds.setAttr(f"{shape}.overrideColor", color_index)

def create_curve_circle():
    """
    Creates a NURBS circle in the scene.

    :return: Name of the created curve object.
    :rtype: str
    """

    curve_circle = cmds.circle(
        c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, s=8, ch=1)[0]

    return curve_circle


def create_curve_cube():
    """
    Creates a custom cube in the scene.

    :return: Name of the created curve object.
    :rtype: str
    """
    cube = cmds.curve(d=1, p=[(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1), (0, 0, 0),
                              (0, 1, 0), (1, 1, 0), (1, 0, 0), (1, 1, 0),
                              (1, 1, 1), (1, 0, 1), (1, 1, 1),
                              (0, 1, 1), (0, 0, 1), (0, 1, 1), (0, 1, 0)])
    cmds.CenterPivot()
    return cube

def create_diamond_curve():
    """
    Creates a diamond in the scene.

    :return: Name of the created curve object.
    :rtype: str
    """

    diamond = cmds.curve(d=1, p=[(-0.0102, 0, -2.9423),
        (-2.9729, 0, 0),
        (-0.0306, 0, 3.0444),
        (3.0138, 0, 0.0204),
        (0.0102, 0, -2.9014)])

    cmds.CenterPivot()
    return diamond

def create_ik_curve():
    """"
    Creates a star-like shape that can be used as an IK handle in the scene.

    :return: Name of the created curve object.
    :rtype: str
    """
    cmds.select(clear=True)
    ik_curve = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, s=8, ch=1)[0]

    cv_indices = [0, 2, 4, 6]
    cv_selection = [f"{ik_curve}.cv[{i}]" for i in cv_indices]

    cmds.select(cv_selection)
    cmds.scale(0.179, 0.179, 0.179, r=True, pivot=(0, 0, 0))

    cmds.select(clear=True)
    cmds.select(ik_curve)
    cmds.CenterPivot()

    return ik_curve

def create_e_curve():
    """"
    Creates the letter E using curves in the scene.

    :return: Name of the created curve object.
    :rtype: str
    """

    e_curve = cmds.curve(d=1, p=[(1.923, 2.779, 0), (0.371, 2.779, 0),
        (0.371, -0.035, 0), (2.003, -0.035, 0),
        (2.003, 0.295, 0), (0.771, 0.295, 0),
        (0.771, 1.297, 0), (1.733, 1.297, 0),
        (1.733, 1.577, 0), (0.771, 1.577, 0),
        (0.771, 2.489, 0), (1.923, 2.489, 0),
        (1.923, 2.779, 0)])

    cmds.CenterPivot()
    return e_curve

def create_k_curve():
    """"
    Creates the letter K  using curves in the scene.

    :return: Name of the created curve object.
    :rtype: str
    """
    k_curve = cmds.curve(d=1, p=[ (2.256, 2.794, 0), (1.878, 2.794, 0),
        (0.742, 1.431, 0), (0.734, 2.777, 0),
        (0.372, 2.785, 0), (0.355, -0.016, 0),
        (0.734, -0.016, 0), (0.742, 1.397, 0),
        (1.962, -0.007, 0), (2.45, -0.007, 0),
        (1.188, 1.448, 0), (2.256, 2.777, 0)])

    cmds.CenterPivot()
    return k_curve


def create_arrow_curve():
    """"
    Creates an arrow using curves in the scene.

    :return: Name of the created curve object.
    :rtype: str
    """
    arrow = cmds.curve(d=1, p=[ (0.022, 0, -7.982), (-3.042, 0, -4.962),
        (-0.928, 0, -4.962), (-0.928, 0, 1.036),
        (1.057, 0, 1.036), (1.057, 0, -4.962),
        (3.042, 0, -4.962), (-0.022, 0, -7.853)])

    cmds.CenterPivot()
    return arrow

def create_arrow_double_curve():
    """"
    Creates a double-sided arrow using curves in the scene.

    :return: Name of the created curve object.
    :rtype: str
    """
    double_arrow = cmds.curve(d=1, p=[ (0.057, 0, -4.971), (-3.002, 0, -2.027),
        (-0.937, 0, -2.027), (-0.937, 0, 4.015),
        (-2.963, 0, 4.015), (0.057, 0, 7.036),
        (3.040, 0, 4.053), (0.975, 0, 4.053),
        (0.975, 0, -1.988), (2.963, 0, -1.988),
        (0.057, 0, -4.933)])

    cmds.CenterPivot()
    return double_arrow

def create_arrow_four_curve():
    """"
    Creates a four-sided arrow using curves in the scene.

    :return: Name of the created curve object.
    :rtype: str
    """
    four_arrow = cmds.curve(d=1, p=[
        (0.022, 0, -7.896), (-3.042, 0, -4.962),
        (-0.971, 0, -4.962), (-0.971, 0, -1.942),
        (-3.991, 0, -1.942), (-3.991, 0, -3.883),
        (-6.968, 0, -0.949), (-3.948, 0, 2.071),
        (-3.948, 0, 0.086), (-1.014, 0, 0.086),
        (-1.014, 0, 3.063), (-3.085, 0, 3.063),
        (0.022, 0, 5.997), (2.999, 0, 3.020),
        (1.057, 0, 3.020), (1.057, 0, 0.129),
        (4.077, 0, 0.129), (4.034, 0, 2.071),
        (6.968, 0, -0.992), (4.077, 0, -3.970),
        (4.077, 0, -1.985), (1.057, 0, -1.985),
        (1.057, 0, -5.048), (3.042, 0, -5.005),
        (0.022, 0, -7.810)])

    cmds.CenterPivot()
    return four_arrow