 #!/usr/bin/env python
#SETMODE 777

#----------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------ HEADER --#

"""
:author: Kris Hernandez

:synopsis:
This is the basic GUI for the rigging tool box.

:description:
This is the GUI for the Rigging Tool Box. This tool box features several functions that 
can be used by riggers to automate workflow. In this tool box, users can reset 
transformations as needed, override set colors on curves and bring in preset custom curves
into the scene. More to be added in future weeks. 

:applications:
    Maya

:see_also:

"""

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- IMPORTS --#

# Built-in
import os

# Third party
from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial

# Internal
from auto_rigging_tool_box.rigging_tools.gen_utils import (freeze_transforms, delete_history, center_pivot,
                                     mirror_joints, orient_joints, reset_translation,
                                     reset_rotation, reset_scale, reset_translation_rotation)
from auto_rigging_tool_box.rigging_tools.curve_utils import (set_override_color, create_curve_circle,
                                                         create_curve_cube, create_ik_curve, create_e_curve,
                                                         create_k_curve,create_arrow_curve, create_diamond_curve,
                                                         create_arrow_four_curve, create_arrow_double_curve)
from auto_rigging_tool_box.rigging_tools.finger_fk_utils import (create_middle_fk, create_ring_fk, create_pinky_fk,
                                                             create_thumb_fk,create_index_fk)
from auto_rigging_tool_box.rigging_tools.limb_ik_utils import create_limb_ik


 # External


#----------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------- FUNCTIONS --#

def get_maya_window():
    """
    Return Maya's main window as a QWidget, so we can parent custom UIs to it.
    """
    import maya.OpenMayaUI as omui
    try:
        from shiboken2 import wrapInstance  # for PySide2
    except ImportError:
        from shiboken6 import wrapInstance  # for newer PySide versions

    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

#----------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------- CLASSES --#

class RiggingToolsGUI(QtWidgets.QDialog):
    """
    Rigging Tool Box GUI - buttons are visible and clickable.
    Logic can be connected later via external functions.
    """

    def __init__(self, parent=None):
        super(RiggingToolsGUI, self).__init__(parent or get_maya_window())
        self.setWindowTitle("Rigging Tool Box")
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowCloseButtonHint |
                            QtCore.Qt.WindowMinimizeButtonHint)
        self.setMinimumSize(400, 400)
        self.init_gui()

    def init_gui(self):
        """Initialize the GUI layout and buttons."""
        main_layout = QtWidgets.QVBoxLayout(self)

        # Tab widget
        tab_widget = QtWidgets.QTabWidget()
        main_layout.addWidget(tab_widget)

#--------------------------------------------------------------------------------------------------------------

        # General Utils Tab
        general_tab = QtWidgets.QWidget()
        general_tab_layout = QtWidgets.QVBoxLayout(general_tab)

        # -------------------------------

        # General Utils Group
        gen_group = QtWidgets.QGroupBox("General Utils")
        gen_layout = QtWidgets.QVBoxLayout(gen_group)
        self.freeze_transforms_btn = QtWidgets.QPushButton("Freeze Transformations")
        self.delete_history_btn = QtWidgets.QPushButton("Delete History")
        self.center_pivot_btn = QtWidgets.QPushButton("Center Pivot")
        gen_layout.addWidget(self.freeze_transforms_btn)
        gen_layout.addWidget(self.delete_history_btn)
        gen_layout.addWidget(self.center_pivot_btn)

        # Connect buttons
        self.freeze_transforms_btn.clicked.connect(freeze_transforms)
        self.delete_history_btn.clicked.connect(delete_history)
        self.center_pivot_btn.clicked.connect(center_pivot)

        # Add widgets
        gen_layout.addWidget(self.freeze_transforms_btn)
        gen_layout.addWidget(self.delete_history_btn)
        gen_layout.addWidget(self.center_pivot_btn)
        general_tab_layout.addWidget(gen_group)

        # -------------------------------

        # Joint Utils Group
        joint_group = QtWidgets.QGroupBox("Joint Utils")
        joint_layout = QtWidgets.QVBoxLayout(joint_group)
        self.mirror_joints_btn = QtWidgets.QPushButton("Mirror Joints")
        self.orient_joints_btn = QtWidgets.QPushButton("Orient Joints")
        joint_layout.addWidget(self.mirror_joints_btn)
        joint_layout.addWidget(self.orient_joints_btn)
        general_tab_layout.addWidget(joint_group)

        # Connect buttons
        self.mirror_joints_btn.clicked.connect(mirror_joints)
        self.orient_joints_btn.clicked.connect(orient_joints)

        # Add widgets
        joint_layout.addWidget(self.mirror_joints_btn)
        joint_layout.addWidget(self.orient_joints_btn)
        general_tab_layout.addWidget(gen_group)

        # -------------------------------

        # Transform Utils Group
        trans_group = QtWidgets.QGroupBox("Transformation Utils")
        trans_layout = QtWidgets.QVBoxLayout(trans_group)
        self.reset_translation_btn = QtWidgets.QPushButton("Reset Translation")
        self.reset_rotation_btn = QtWidgets.QPushButton("Reset Rotation")
        self.reset_trans_rot_btn = QtWidgets.QPushButton("Reset Translation and Rotation")
        self.reset_scale_btn = QtWidgets.QPushButton("Reset Scale")

        # Connect buttons
        self.reset_translation_btn.clicked.connect(reset_translation)
        self.reset_rotation_btn.clicked.connect(reset_rotation)
        self.reset_trans_rot_btn.clicked.connect(reset_translation_rotation)
        self.reset_scale_btn.clicked.connect(reset_scale)

        # Add widgets
        trans_layout.addWidget(self.reset_translation_btn)
        trans_layout.addWidget(self.reset_rotation_btn)
        trans_layout.addWidget(self.reset_trans_rot_btn)
        trans_layout.addWidget(self.reset_scale_btn)
        general_tab_layout.addWidget(trans_group)

        # -------------------------------

        # Add this tab to the window
        tab_widget.addTab(general_tab, "General Tools")

# --------------------------------------------------------------------------------------------------------------
        # Color Override Utils Tab
        color_tab = QtWidgets.QWidget()
        color_tab_layout = QtWidgets.QVBoxLayout(color_tab)

        # -------------------------------

        # Color Picker Tab
        color_tab = QtWidgets.QWidget()
        color_tab_layout = QtWidgets.QVBoxLayout(color_tab)

        colors = {
            "Blue": 6,
            "Red": 13,
            "Green": 23,
            "Lime Green": 14,
            "Yellow": 17,
            "Light Pink": 20,
            "Magenta": 9,
            "Pinkish": 31,
            "Peach": 21,
            "Dark Brown": 11,
            "Light Blue": 18,
            "Black": 1,
            "Dark Purple": 30
        }

        for name, index in colors.items():
            btn = QtWidgets.QPushButton(name)
            # Pass the color index to the function
            btn.clicked.connect(partial(set_override_color, index))
            color_tab_layout.addWidget(btn)

        # -------------------------------

        # Add this tab to the window
        tab_widget.addTab(color_tab, "Color Curve Override Util")

# --------------------------------------------------------------------------------------------------------------
        # Custom Control Curves Tab
        curves_tab = QtWidgets.QWidget()
        curves_tab_layout = QtWidgets.QVBoxLayout(curves_tab)

        # -------------------------------

        # Shape Buttons Group
        shapes_group = QtWidgets.QGroupBox("Custom Shapes")
        shapes_layout = QtWidgets.QVBoxLayout(shapes_group)
        self.circle_btn = QtWidgets.QPushButton("Circle")
        self.cube_btn = QtWidgets.QPushButton("3D Cube")
        self.diamond_btn = QtWidgets.QPushButton("Diamond")
        self.ik_btn = QtWidgets.QPushButton("IK Star Handle")

        shapes_layout.addWidget(self.circle_btn)
        shapes_layout.addWidget(self.cube_btn)
        shapes_layout.addWidget(self.diamond_btn)
        shapes_layout.addWidget(self.ik_btn)
        curves_tab_layout.addWidget(shapes_group)

        # Connect buttons
        self.circle_btn.clicked.connect(create_curve_circle)
        self.cube_btn.clicked.connect(create_curve_cube)
        self.diamond_btn.clicked.connect(create_diamond_curve)
        self.ik_btn.clicked.connect(create_ik_curve)

        # Add widgets
        shapes_layout.addWidget(self.circle_btn)
        shapes_layout.addWidget(self.cube_btn)
        shapes_layout.addWidget(self.diamond_btn)
        shapes_layout.addWidget(self.ik_btn)
        curves_tab_layout.addWidget(shapes_group)

        # -------------------------------

        # Letter Buttons Group
        letter_group = QtWidgets.QGroupBox("Custom Letters")
        letter_layout = QtWidgets.QVBoxLayout(letter_group)
        self.e_btn = QtWidgets.QPushButton("E")
        self.k_btn = QtWidgets.QPushButton("K")

        letter_layout.addWidget(self.e_btn)
        letter_layout.addWidget(self.k_btn)
        curves_tab_layout.addWidget(letter_group)

        # Connect buttons
        self.e_btn.clicked.connect(create_e_curve)
        self.k_btn.clicked.connect(create_k_curve)

        # Add widgets
        letter_layout.addWidget(self.e_btn)
        letter_layout.addWidget(self.k_btn)
        curves_tab_layout.addWidget(letter_group)

        # -------------------------------

        # Arrow Buttons Group
        arrow_group = QtWidgets.QGroupBox("Custom Arrows")
        arrow_layout = QtWidgets.QVBoxLayout(arrow_group)
        self.arrow_btn = QtWidgets.QPushButton("One Sided Arrow")
        self.arrow_double_btn = QtWidgets.QPushButton("Double Sided Arrow")
        self.arrow_four_btn = QtWidgets.QPushButton("Four Sided Arrow")

        arrow_layout.addWidget(self.arrow_btn)
        arrow_layout.addWidget(self.arrow_double_btn)
        arrow_layout.addWidget(self.arrow_four_btn)
        curves_tab_layout.addWidget(arrow_group)

        # Connect buttons
        self.arrow_btn.clicked.connect(create_arrow_curve)
        self.arrow_double_btn.clicked.connect(create_arrow_double_curve)
        self.arrow_four_btn.clicked.connect(create_arrow_four_curve)

        # Add widgets
        arrow_layout.addWidget(self.arrow_btn)
        arrow_layout.addWidget(self.arrow_double_btn)
        arrow_layout.addWidget(self.arrow_four_btn)
        curves_tab_layout.addWidget(arrow_group)

        # -------------------------------

        # Add this tab to the window
        tab_widget.addTab(curves_tab, "Custom Curve Utils")

# --------------------------------------------------------------------------------------------------------------

        # Custom Control Curves Tab
        auto_tab = QtWidgets.QWidget()
        auto_tab_layout = QtWidgets.QVBoxLayout(auto_tab)

        # -------------------------------

        # Finger Buttons Group
        finger_group = QtWidgets.QGroupBox("Finger Controls Utils")
        finger_layout = QtWidgets.QVBoxLayout(finger_group)
        self.index_btn = QtWidgets.QPushButton("Create Index Finger Controls")
        self.middle_btn = QtWidgets.QPushButton("Create Middle Finger Controls")
        self.ring_btn = QtWidgets.QPushButton("Create Ring Finger Controls")
        self.pinky_btn = QtWidgets.QPushButton("Create Pinky Finger Controls")
        self.thumb_btn = QtWidgets.QPushButton("Create Thumb Controls")

        finger_layout.addWidget(self.index_btn)
        finger_layout.addWidget(self.middle_btn)
        finger_layout.addWidget(self.ring_btn)
        finger_layout.addWidget(self.pinky_btn)
        finger_layout.addWidget(self.thumb_btn)
        auto_tab_layout.addWidget(finger_group)

        # Connect buttons
        self.index_btn.clicked.connect(create_index_fk)
        self.middle_btn.clicked.connect(create_middle_fk)
        self.ring_btn.clicked.connect(create_ring_fk)
        self.pinky_btn.clicked.connect(create_pinky_fk)
        self.thumb_btn.clicked.connect(create_thumb_fk)

        # Add widgets
        finger_layout.addWidget(self.index_btn)
        finger_layout.addWidget(self.middle_btn)
        finger_layout.addWidget(self.ring_btn)
        finger_layout.addWidget(self.pinky_btn)
        finger_layout.addWidget(self.thumb_btn)
        auto_tab_layout.addWidget(finger_group)

        # -------------------------------

        # Limbs Controls Buttons Group
        limbs_group = QtWidgets.QGroupBox("Automation Limbs Utils")
        limbs_layout = QtWidgets.QVBoxLayout(limbs_group)
        self.fk_btn = QtWidgets.QPushButton("Create FK Limb")
        self.ik_btn = QtWidgets.QPushButton("Create IK Limb")
        self.pole_vector_btn = QtWidgets.QPushButton("Create Pole Vector")
        self.squash_btn = QtWidgets.QPushButton("Create Squash Function")
        self.stretch_btn = QtWidgets.QPushButton("Create Stretch Function")

        limbs_layout.addWidget(self.fk_btn)
        limbs_layout.addWidget(self.ik_btn)
        limbs_layout.addWidget(self.pole_vector_btn)
        limbs_layout.addWidget(self.squash_btn)
        limbs_layout.addWidget(self.stretch_btn)
        auto_tab_layout.addWidget(limbs_group)

        # # Connect buttons
        # self.fk_btn.clicked.connect()
        self.ik_btn.clicked.connect(create_limb_ik)
        # self.pole_vector_btn.clicked.connect()
        # self.squash_btn.connect()
        # self.stretch_btn.clicked.connect()

        # Add widgets
        limbs_layout.addWidget(self.fk_btn)
        limbs_layout.addWidget(self.ik_btn)
        limbs_layout.addWidget(self.pole_vector_btn)
        limbs_layout.addWidget(self.squash_btn)
        limbs_layout.addWidget(self.stretch_btn)
        auto_tab_layout.addWidget(limbs_group)

        # -------------------------------

        # Add this tab to the window
        tab_widget.addTab(auto_tab, "Automation Utils BETA")

        # -------------------------------

        self.setLayout(main_layout)


