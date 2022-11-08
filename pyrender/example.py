"""Examples of using pyrender for viewing and offscreen rendering.
"""
import pyglet
pyglet.options['shadow_window'] = False
import os
import numpy as np
import trimesh
import math

from pyrender import PerspectiveCamera,\
                     DirectionalLight, SpotLight, PointLight,\
                     MetallicRoughnessMaterial,\
                     Primitive, Mesh, Node, Scene,\
                     Viewer, OffscreenRenderer, RenderFlags


#------------------------------------------------------------------------------
# Creating meshes with per-face colors
#------------------------------------------------------------------------------
boxf_trimesh = trimesh.creation.box(extents=0.01*np.ones(3))
boxf_face_colors = (0.3,0.5,0.2,1)
boxf_trimesh.visual.face_colors = boxf_face_colors
boxf_mesh = Mesh.from_trimesh(boxf_trimesh, smooth=False)

#==============================================================================
# Light creation
#==============================================================================

direc_l = DirectionalLight(color=np.ones(3), intensity=1.0)

#==============================================================================
# Camera creation
#==============================================================================

cam = PerspectiveCamera(yfov=(np.pi / 3.0))
width = 500
height = 500
far = 1000.0
near = 0.1
c = -near/far

theta_w = math.radians(45)
theta_h = math.radians(45)

S_xyz = np.array([
    [1/far * np.tan(theta_w/2), 0, 0, 0],
    [0, 1/far * np.tan(theta_h/2), 0, 0],
    [0, 0, 1/far, 0],
    [0, 0, 0, 1]
])

M_pp = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0,0,1/(1+c), -c/(1+c)],
    [0,0,-1,0]
])

M_reshape = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0,0,-2,-1],
    [0,0,0,1]
])

perspective_matrix = M_reshape @ M_pp @ S_xyz

cam_pose = np.array([
    [0.0,  -np.sqrt(4)/2, np.sqrt(2)/2, 0.5],
    [1.0, 0.0,           0.0,           0.0],
    [0.0,  np.sqrt(2)/2,  np.sqrt(2)/2, 0.4],
    [0.0,  0.0,           0.0,          1.0]
])

#==============================================================================
# Scene creation
#==============================================================================

scene = Scene(ambient_light=np.array([0.02, 0.02, 0.02, 1.0]))

#==============================================================================
# Adding objects to the scene
#==============================================================================

#------------------------------------------------------------------------------
# By manually creating nodes
#------------------------------------------------------------------------------
boxf_node = Node(mesh=boxf_mesh, translation=np.array([0, 0, 0]))
boxf_node2 = Node(mesh=boxf_mesh, translation=np.array([0.1, 0, 0]))
boxf_node3 = Node(mesh=boxf_mesh, translation=np.array([0, 0.1, 0]))

scene.add_node(boxf_node)
scene.add_node(boxf_node2)
scene.add_node(boxf_node3)


#------------------------------------------------------------------------------
# By using the add() utility function
#------------------------------------------------------------------------------
direc_l_node = scene.add(direc_l, pose=cam_pose)

#==============================================================================
# Using the viewer with a default camera
#==============================================================================

v = Viewer(scene, shadows=True)

#==============================================================================
# Using the viewer with a pre-specified camera
#==============================================================================
cam_node = scene.add(cam, pose=cam_pose)
v = Viewer(scene, central_node=boxf_node)

#==============================================================================
# Rendering offscreen from that camera
#==============================================================================

r = OffscreenRenderer(viewport_width=640*2, viewport_height=480*2)
color, depth = r.render(scene)
