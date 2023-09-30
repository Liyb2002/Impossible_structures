import pyglet
pyglet.options['shadow_window'] = False
import os
import numpy as np
import trimesh
import math

import perspective

from pyrender import OrthographicCamera,\
                     Primitive, Mesh, Node, Scene,\
                     Viewer, OffscreenRenderer, RenderFlags


cam = OrthographicCamera(xmag=800, ymag=800, znear=0.05, zfar=100.0)
cam_pose = perspective.get_m_view()


def get_graph(procedural_obj_list):
    scene = Scene(ambient_light=np.array([0.02, 0.02, 0.02, 1.0]))
    cam_node = scene.add(cam, pose=cam_pose)

    for i in procedural_obj_list:
        boxf_trimesh = trimesh.creation.box(np.array([i.length[0], i.length[1], i.length[2]]))
        boxf_mesh = Mesh.from_trimesh(boxf_trimesh, smooth=False)
        boxf_node = Node(mesh=boxf_mesh, translation=np.array([i.position[0], i.position[1], i.position[2]]))
        
        scene.add_node(boxf_node)
    
    r = OffscreenRenderer(viewport_width=800, viewport_height=800)
    _, depth = r.render(scene)
    r.delete()
    return depth

