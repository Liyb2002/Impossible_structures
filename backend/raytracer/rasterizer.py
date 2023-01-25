import numpy as np

import trimesh

import raytracer.perspective

from pyrender import (
    PerspectiveCamera,
    Mesh,
    Node,
    Scene,
    OffscreenRenderer,
)


cam = PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.0)
cam_pose = raytracer.perspective.get_m_view()


def get_graph(rects):
    scene = Scene(ambient_light=np.array([0.02, 0.02, 0.02, 1.0]))
    cam_node = scene.add(cam, pose=cam_pose)

    for i in rects:
        boxf_trimesh = trimesh.creation.box(np.array([i.scale_x, i.scale_y, i.scale_z]))
        boxf_mesh = Mesh.from_trimesh(boxf_trimesh, smooth=False)
        boxf_node = Node(
            mesh=boxf_mesh, translation=np.array([i.start_x, i.start_y, i.start_z])
        )

        scene.add_node(boxf_node)

    r = OffscreenRenderer(viewport_width=640 * 2, viewport_height=480 * 2)
    _, depth = r.render(scene)
    r.delete()
    return depth
