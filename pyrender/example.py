"""Examples of using pyrender for viewing and offscreen rendering.
"""
import pyglet
pyglet.options['shadow_window'] = False
import os
import numpy as np
import trimesh

from pyrender import PerspectiveCamera,\
                     DirectionalLight, SpotLight, PointLight,\
                     MetallicRoughnessMaterial,\
                     Primitive, Mesh, Node, Scene,\
                     Viewer, OffscreenRenderer, RenderFlags


#------------------------------------------------------------------------------
# Creating meshes with per-face colors
#------------------------------------------------------------------------------
boxf_trimesh = trimesh.creation.box(extents=0.1*np.ones(3))
boxf_face_colors = np.random.uniform(size=boxf_trimesh.faces.shape)
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
cam_pose = np.array([
    [0.0,  -np.sqrt(2)/2, np.sqrt(2)/2, 0.5],
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
boxf_node = Node(mesh=boxf_mesh, translation=np.array([-0.1, -0.10, 0.05]))
boxf_node2 = Node(mesh=boxf_mesh, translation=np.array([-0.2, -0.20, 0.5]))

scene.add_node(boxf_node)
scene.add_node(boxf_node2)

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
