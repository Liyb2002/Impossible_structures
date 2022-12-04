import math 

camera_pos = np.array([5,5,5])
lookAt = np.array([0,0,0])
up = np.array([0,1,0])
look_vec = lookAt - camera_pos

w = 800
h = 800
near = 0.1
far = 100

theta_w = 45
theta_w = math.radians(theta_w)

theta_h = 45
theta_h = math.radians(theta_h)

c = - near / far


def get_m_view():
    w = look_vec / np.linalg.norm(look_vec)
    u = np.cross(up, w)
    u = u / np.linalg.norm(u)
    v = np.cross(w, u)
    m_view = np.array([u,v,w])
    return m_view

def get_m_proj():
    m_proj = np.array([[1 / (math.tan(theta_w / 2)), 0, 0, 0],
                       [0, 1 / (math.tan(theta_h / 2)), 0, 0],
                       [0, 0, c, -1],
                       [0, 0, c * near, 0]])
    return m_proj


