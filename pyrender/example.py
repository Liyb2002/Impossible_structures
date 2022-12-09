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



def render(coordinates):
        
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

    cam = PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.0)

    s = np.sqrt(2)/2

    cam_pose = np.array([
        [0.0, -s,   s,   0.3],
        [1.0,  0.0, 0.0, 0.0],
        [0.0,  s,   s,   0.35],
        [0.0,  0.0, 0.0, 1.0],
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
    
    for coordinate in coordinates:
        node = Node(mesh=boxf_mesh, translation=coordinate)
        scene.add_node(node)

    #------------------------------------------------------------------------------
    # By using the add() utility function
    #------------------------------------------------------------------------------
    direc_l_node = scene.add(direc_l, pose=cam_pose)

    #==============================================================================
    # Using the viewer with a default camera
    #==============================================================================
    boxf_node = Node(mesh=boxf_mesh)

    #==============================================================================
    # Using the viewer with a pre-specified camera
    #==============================================================================
    v = Viewer(scene, central_node=boxf_node)

    #==============================================================================
    # Rendering offscreen from that camera
    #==============================================================================

    r = OffscreenRenderer(viewport_width=640*2, viewport_height=480*2)
    color, depth = r.render(scene)


coordinates = np.array([[0, 0, 0],  [-0.1,2,0.04]])
render(coordinates)

r = pyrender.OffscreenRenderer(viewport_width=640,viewport_height=480,point_size=1.0) 
color, depth = r.render(scene)
