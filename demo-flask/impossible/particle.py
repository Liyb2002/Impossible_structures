from . import produce
from . import cycle_connect
import random
from . import procedural_objects
import numpy as np
import math
from . import perspective


class Particle:
    def __init__(self, generic_object_list, guided_pts, bounding_box):
        self.generic_object_list = generic_object_list
        self.success = True
        self.procedural_objects = []
        self.extra_system = []

        self.targetProb = {}
        self.eye = np.array([5.0, 5.0, 5.0])
        self.score = 1

        self.constraints_pts = guided_pts
        self.camera = perspective.ortho_camera()
        self.hit_constraints = 0
        self.bounding_box = bounding_box

    def prepare_particle(self, intersection, start_type, connected_dir, targetProb):
        self.cur_obj = start_obj(
            intersection, self.generic_object_list, start_type, connected_dir
        )
        self.intersection_obj = self.cur_obj
        self.procedural_objects.append(self.cur_obj)
        self.targetProb = targetProb

    def run_step(self, step, isFront):
        results = produce.execute_model(self.generic_object_list, self.cur_obj, 1)
        if len(results) == 0:
            self.score = 0
            return False
        self.cur_obj = results[-1]
        self.procedural_objects += results
        self.calculate_score(self.intersection_obj, results)

        if step == 0 and isFront:
            self.start_connect = self.procedural_objects[-1]
            self.end_connect = self.procedural_objects[0]

        if step == 0 and not isFront:
            self.end_connect = self.procedural_objects[-1]

    def branching_run_step(self, step):
        results = produce.execute_model(self.generic_object_list, self.cur_obj, 1)
        if len(results) == 0:
            self.score = 0
            return False
        self.cur_obj = results[-1]
        self.procedural_objects += results
        self.calculate_score(self.intersection_obj, results)

        if step == 0:
            self.branching_start = self.procedural_objects[-1]

    def branching_connect(self):
        self.run_connect(targetStart=self.branching_start, targetEnd=self.start_connect)

    def arbitrary_add_object(self, intersection, start_type, connected_dir):
        obj = start_obj(
            intersection, self.generic_object_list, start_type, connected_dir
        )
        self.procedural_objects.append(obj)

    def arbitrary_connect(self, id1, id2):
        self.start_connect = self.procedural_objects[id1]
        self.end_connect = self.procedural_objects[id2]

    def arbitrary_add_extra_system(self, extra_system):
        scope_x = extra_system["scope_x"]
        scope_y = extra_system["scope_y"]
        scope_z = extra_system["scope_z"]
        scope = np.array([scope_x, scope_y, scope_z])
        gen_hash = extra_system["object_id"] + random.uniform(0, 1)
        position = np.array(
            [
                extra_system["position"][0],
                extra_system["position"][1],
                extra_system["position"][2],
            ]
        )

        obj = procedural_objects.Procedural_object(
            extra_system["object_id"],
            position,
            scope,
            gen_hash,
            np.array([[0], [0], [0]]),
            np.array([0, 0, 0]),
        )
        self.procedural_objects.append(obj)
        self.extra_system.append(obj)

    def connect_extra_system(self):
        for e_sys in self.extra_system:
            prev_start = self.start_connect
            self.start_connect = e_sys
            self.run_connect()
            self.start_connect = prev_start

    def run_connect(self, targetStart=None, targetEnd=None):
        if targetStart == None:
            targetStart = self.start_connect
        if targetEnd == None:
            targetEnd = self.end_connect
        startPos = targetStart.position
        endPos = targetEnd.position

        delta = endPos - startPos
        production_list = []
        production_list.append(targetStart)
        abs_delta = np.array([abs(delta[0]), abs(delta[1]), abs(delta[2])])
        abs_delta -= np.array([0, 0, targetEnd.length[2]])

        directions = cycle_connect.get_dirs(delta)
        # directions = cycle_connect.update_order(self.start_connect, directions)
        orders = cycle_connect.random_order()
        # print("------------------------")
        # print("orders:", directions[orders[0]],directions[orders[1]],directions[orders[2]])
        for i in range(0, 3):
            index = orders[i]
            if abs_delta[index] != 0:
                if i < 2:
                    target_dir_index = orders[i + 1]
                    available_endings = cycle_connect.Available_Ending_With_Direction(
                        self.generic_object_list, directions[target_dir_index]
                    )
                    # print("i:", i, "available_endings", available_endings)
                if i == 2:
                    available_endings = cycle_connect.Available_Ending_With_Object(
                        self.generic_object_list, targetEnd
                    )
                    # print("i:", i, "available_endings", available_endings)

                connect_particle = produce.connect_execution(
                    production_list[-1],
                    self.generic_object_list,
                    abs_delta,
                    directions[index],
                    available_endings,
                    self.end_connect,
                )
                ok = 1

                while ok == 1:
                    ok = connect_particle.execute_model_withDirection()

                if ok == 0 or self.score < 0:
                    self.success = False
                    return

                if ok == 2:
                    tempt_result = connect_particle.set_scope()
                    production_list += tempt_result
                    for obj in tempt_result:
                        if not self.overlapping_check_obj(obj):
                            self.success = False
                            return

            # print("rotation", i, "succes")

        # self.success = True
        self.procedural_objects += production_list

    def run_particle2(self, steps):
        rd1, rd2 = self.random_object()
        objStart = self.procedural_objects[rd1]
        objStart2 = self.procedural_objects[rd2]

        self.procedural_objects += produce.execute_model(
            self.generic_object_list, objStart, steps
        )
        self.start_connect = self.procedural_objects[-1]
        self.procedural_objects += produce.execute_model(
            self.generic_object_list, objStart2, steps
        )
        self.end_connect = self.procedural_objects[-1]

    def overlapping_check(self):
        for obj_A in self.procedural_objects:
            if (
                obj_A.rotation[0] != 0
                or obj_A.rotation[1] != 0
                or obj_A.rotation[2] != 0
            ):
                continue

            for obj_B in self.procedural_objects:
                if (
                    obj_B.rotation[0] != 0
                    or obj_B.rotation[1] != 0
                    or obj_B.rotation[2] != 0
                ):
                    continue

                if obj_A.hash != obj_B.hash:
                    overlapping = obj_A.collision_check(obj_B)
                    if overlapping:
                        # print("final overlapping check failed")
                        self.success = False

    def overlapping_check_obj(self, obj_A):
        if obj_A.rotation[0] != 0 or obj_A.rotation[1] != 0 or obj_A.rotation[2] != 0:
            return True

        for obj_B in self.procedural_objects:
            if obj_A.hash != obj_B.hash:
                overlapping = obj_A.collision_check(obj_B)
                if overlapping:
                    # print("step by step overlapping check failed")
                    self.success = False
                    return False

        return True

    def find_connect_ending(self):
        for obj in self.back_list:
            if obj.type == 1:
                return obj

    def random_object(self):
        rd1 = 0
        rd2 = 0

        while True:
            rd1 = random.randint(0, len(self.procedural_objects) - 1)
            obj1 = self.procedural_objects[rd1]
            # need to work on rules
            if obj1.type == 1:
                break

        while True:
            rd2 = random.randint(0, len(self.procedural_objects) - 1)
            obj2 = self.procedural_objects[rd2]
            # need to work on rules
            if obj2.type == 1 and rd1 != rd2:
                break

        return (rd1, rd2)

    def calculate_score(self, intersection_obj, results):
        density_score = self.density_score()
        probability_score = self.probability_score()
        occulusion_score = self.occulusion_score(intersection_obj, results)
        constraints_score = self.constraints_score(results)
        constraints_score = 0
        bounding_box_score = 1

        overlapping_score = 1
        for obj in results:
            if not self.overlapping_check_obj(obj):
                overlapping_score = 0

            if not self.bounding_box.check_within(obj):
                bounding_box_score = 0

        self.score = (
            (density_score + probability_score + occulusion_score + constraints_score)
            * overlapping_score
            * bounding_box_score
        )

        if len(results) == 0:
            self.score = 0

    def get_score(self):
        return self.score

    def density_score(self):
        added_object = self.procedural_objects[-1]
        k = 1.0
        alpha, beta, alpha_dash, beta_dash = 0.5, 0.5, 0.5, 0.5
        D = 0.0
        S_de = 0.0

        expanded_cube_length = added_object.length + np.array([k, k, k])
        expanded_cube_size = (
            expanded_cube_length[0]
            * expanded_cube_length[1]
            * expanded_cube_length[2]
            * 8
        )
        # sum_overlapping_size = added_object.length[0] * added_object.length[1] * added_object.length[2] * 8

        for obj in self.procedural_objects[:-1]:
            D = alpha * distance(
                added_object, obj
            ) + beta * procedural_objects.getOverlap3D(
                added_object.position, expanded_cube_length, obj.position, obj.length
            )
            S_de += math.exp(-alpha_dash * D - beta_dash)

        return S_de

    def probability_score(self):
        current_Prob = {}
        KL = 0
        for generic_obj in self.generic_object_list:
            current_Prob[generic_obj.id] = 0

        for obj in self.procedural_objects:
            current_Prob[obj.type] += 1 / len(self.procedural_objects)

        for key in current_Prob:
            if not self.targetProb[key]:
                continue
            term = self.targetProb[key]

            if current_Prob[key] != 0:
                term = self.targetProb[key] * math.log(
                    self.targetProb[key] / current_Prob[key]
                )
            KL += term

        return 1 - KL

    def occulusion_score(self, intersection_obj, new_Obj_list):
        occulusion_score = 0
        # vb = []
        # vb.append(new_Obj_list[0])
        # rasterized_vb = rasterizer.get_graph(vb)
        for obj in new_Obj_list:
            occulusion_score += 5
            occulusion_score += check_occlusion(obj, intersection_obj, self.eye)

        return occulusion_score

    def constraints_score(self, new_Obj_list):
        constraints_score = 0
        for obj in new_Obj_list:
            obj_center = obj.position
            u, v = self.camera.get_uv(obj_center)

            for constraints in self.constraints_pts:
                if abs(u - constraints[0]) < 20 and abs(v - constraints[1]) < 20:
                    constraints_score += 20
                    self.hit_constraints += 1

        return constraints_score


def start_obj(start_pos, generic_object_list, start_type, connected_dir):
    cur_type = start_type
    start_scope = generic_object_list[cur_type].scope
    gen_hash = generic_object_list[cur_type].generate_hash()
    next_rotation = generic_object_list[cur_type].rotation
    cur_obj = procedural_objects.Procedural_object(
        cur_type, start_pos, start_scope, gen_hash, next_rotation, np.array([0, 0, 0])
    )
    cur_obj_x = cur_obj.length[0]
    cur_obj_y = cur_obj.length[1]
    cur_obj_z = cur_obj.length[2]
    update_pos = np.array([cur_obj_x, cur_obj_y, cur_obj_z])
    cur_obj.arbitrary_set_position(start_pos - update_pos)
    cur_obj.add_connected(connected_dir)

    return cur_obj


def check_occlusion(front_obj, back_obj, eye):
    score = 0

    pt0 = back_obj.position
    pt1 = front_obj.position
    alpha = 0.5
    val = math.exp(-alpha * ((pt0[0] - pt1[0]) ** 2 + (pt0[1] - pt1[1])))

    return val


def ray_intersecting_Obj(front_obj, ro, rd):
    minX = front_obj.position[0] - front_obj.length[0]
    maxX = front_obj.position[0] + front_obj.length[0]
    minY = front_obj.position[1] - front_obj.length[1]
    maxY = front_obj.position[1] + front_obj.length[1]
    minZ = front_obj.position[2] - front_obj.length[2]
    maxZ = front_obj.position[2] + front_obj.length[2]

    tMin = (minX - ro[0]) / rd[0]
    tMax = (maxX - ro[0]) / rd[0]

    if tMin > tMax:
        swap(tMin, tMax)

    tMinY = (minY - ro[1]) / rd[1]
    tMaxY = (maxY - ro[1]) / rd[1]
    if tMinY > tMaxY:
        swap(tMinY, tMaxY)

    if (tMin > tMaxY) or (tMinY > tMax):
        return False

    if tMinY > tMin:
        tMin = tMinY

    if tMaxY < tMax:
        tMax = tMaxY

    tMinZ = (minZ - ro[2]) / rd[2]
    tMaxZ = (maxZ - ro[2]) / rd[2]

    if tMinZ > tMaxZ:
        swap(tMinZ, tMaxZ)

    if (tMin > tMaxZ) or (tMinZ > tMax):
        return False

    return True


def distance(obj1, obj2):
    return math.sqrt(
        (obj1.length[0] - obj2.length[0]) ** 2
        + (obj1.length[1] - obj2.length[1]) ** 2
        + (obj1.length[2] - obj2.length[2]) ** 2
    )
