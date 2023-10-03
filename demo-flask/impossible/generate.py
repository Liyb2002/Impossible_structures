from . import parseTree
from . import particle
from . import resample
from . import decorations
from . import perspective
from . import constraints_loader
from . import global_execution
from . import bounding_box
from . import write2JSON

from copy import deepcopy
import numpy as np


class generate_helper:
    def __init__(
        self,
        generic_object_list,
        global__object_list,
        extra_system_list,
        visual_bridge_info,
        decorate_path,
    ):
        # find impossible intersection positions

        self.generic_object_list = generic_object_list
        self.global__object_list = global__object_list
        self.extra_system_list = extra_system_list

        self.particle_list = []
        self.score_list = []
        self.result_particle = None
        self.sampled_points = constraints_loader.load_constraints()
        self.visual_bridge_info = visual_bridge_info
        self.decorate_path = decorate_path

        box_pos = np.array([0, 0, 0])
        box_scope = np.array([5, 5, 5])
        self.bounding_box = bounding_box.box(box_pos, box_scope)

    def extra_system_init(self):
        for i in range(len(self.particle_list)):
            tempt_particle = self.particle_list[i]
            for extra_system in self.extra_system_list:
                tempt_particle.arbitrary_add_extra_system(extra_system)

    def smc_process(
        self,
        foreground_intersection=np.array([-100, 0, 0]),
        background_intersection=np.array([-100, 0, 0]),
    ):
        num_particles = 3000
        for i in range(num_particles):
            tempt_particle = particle.Particle(
                self.generic_object_list, self.sampled_points, self.bounding_box
            )
            self.particle_list.append(tempt_particle)

        self.extra_system_init()

        foreground_index = self.visual_bridge_info["foreground_index"]
        background_index = self.visual_bridge_info["background_index"]
        startPos = np.array(
            [
                self.visual_bridge_info["startPos"][0],
                self.visual_bridge_info["startPos"][1],
            ]
        )

        camera = perspective.ortho_camera()

        if foreground_intersection[0] == -100 and background_intersection[0] == -100:
            foreground_intersection, background_intersection = camera.get_intersections(
                startPos, foreground_index, background_index
            )

        foreground_type = self.visual_bridge_info["foreground_type"][0]
        foreground_connect = self.visual_bridge_info["foreground_connect"]
        background_type = self.visual_bridge_info["background_type"]
        background_connect = self.visual_bridge_info["background_connect"]

        steps = self.visual_bridge_info["steps"]
        # print(
        #     "foreground_intersection",
        #     foreground_intersection,
        #     "background_intersection",
        #     background_intersection,
        # )

        self.small_cubes = constraints_loader.guide_visualizer(
            self.sampled_points, foreground_index
        )

        if self.visual_bridge_info["num_visual_bridge"] == 1:
            self.procedural_generate(
                foreground_type,
                foreground_connect,
                foreground_intersection,
                steps,
                True,
            )
            if background_type != 0:
                self.procedural_generate(
                    background_type,
                    background_connect,
                    background_intersection,
                    steps,
                    False,
                )

        branching = False
        if branching:
            self.branching(
                foreground_type, foreground_connect, foreground_intersection, steps
            )

        if self.visual_bridge_info["num_visual_bridge"] == 2:
            startPos2 = np.array([600, 800])
            (
                foreground_intersection2,
                background_intersection2,
            ) = camera.get_intersections(
                startPos2, foreground_index - 2, background_index + 8
            )

            start_type_list = [foreground_type, foreground_type]
            connect_direction_list = [foreground_connect, foreground_connect]
            intersection_pos_list = [foreground_intersection, foreground_intersection2]
            self.multiple_intersections(
                start_type_list, connect_direction_list, intersection_pos_list
            )
            self.procedural_generate(
                background_type,
                background_connect,
                background_intersection,
                steps,
                True,
            )
            if background_type != 0:
                self.procedural_generate(
                    background_type,
                    background_connect,
                    background_intersection2,
                    steps,
                    False,
                )

        if self.visual_bridge_info["num_visual_bridge"] == 3:
            startPos2 = np.array([600, 800])
            (
                foreground_intersection2,
                background_intersection2,
            ) = camera.get_intersections(
                startPos2, foreground_index - 2, background_index + 8
            )

            startPos3 = np.array([400, 600])
            (
                foreground_intersection3,
                background_intersection3,
            ) = camera.get_intersections(
                startPos3, foreground_index - 4, background_index + 2
            )

            start_type_list = [
                foreground_type,
                foreground_type,
                foreground_type,
                background_type,
            ]
            connect_direction_list = [
                foreground_connect,
                foreground_connect,
                foreground_connect,
                background_connect,
            ]
            intersection_pos_list = [
                foreground_intersection,
                foreground_intersection2,
                foreground_intersection3,
                background_intersection3,
            ]
            self.multiple_intersections(
                start_type_list, connect_direction_list, intersection_pos_list
            )
            self.procedural_generate(
                background_type,
                background_connect,
                background_intersection,
                steps,
                True,
            )
            if background_type != 0:
                self.procedural_generate(
                    background_type,
                    background_connect,
                    background_intersection2,
                    steps,
                    False,
                )

        if self.visual_bridge_info["num_visual_bridge"] == 4:
            startPos2 = np.array([600, 800])
            (
                foreground_intersection2,
                background_intersection2,
            ) = camera.get_intersections(
                startPos2, foreground_index - 2, background_index + 9
            )

            startPos3 = np.array([400, 600])
            (
                foreground_intersection3,
                background_intersection3,
            ) = camera.get_intersections(
                startPos3, foreground_index - 4, background_index + 2
            )

            startPos4 = np.array([300, 500])
            (
                foreground_intersection4,
                background_intersection4,
            ) = camera.get_intersections(
                startPos4, foreground_index + 3, background_index + 5
            )

            start_type_list = [
                foreground_type,
                foreground_type,
                foreground_type,
                foreground_type,
                background_type,
                background_type,
            ]
            connect_direction_list = [
                foreground_connect,
                foreground_connect,
                foreground_connect,
                foreground_connect,
                background_connect,
                background_connect,
            ]
            intersection_pos_list = [
                foreground_intersection,
                foreground_intersection2,
                foreground_intersection3,
                foreground_intersection4,
                background_intersection3,
                background_intersection4,
            ]
            self.multiple_intersections(
                start_type_list, connect_direction_list, intersection_pos_list
            )
            self.procedural_generate(
                background_type,
                background_connect,
                background_intersection,
                steps,
                True,
            )
            if background_type != 0:
                self.procedural_generate(
                    background_type,
                    background_connect,
                    background_intersection2,
                    steps,
                    False,
                )

        tempt_list = []
        for temple_particle in self.particle_list:
            if temple_particle.success and hasattr(temple_particle, "start_connect"):
                tempt_list.append(temple_particle)
        self.particle_list = tempt_list

        # self.reproduce_particle_list(num_particles)
        # startPos = np.array([100,800])
        # foreground_intersection, background_intersection = camera.get_intersections(startPos, foreground_index, background_index)
        # self.procedural_generate(foreground_type, foreground_connect, foreground_intersection+np.array([0.05,0.075,0.05]), steps, True)
        # self.procedural_generate(background_type, background_connect, background_intersection-np.array([0.05,0.15,0.05]), steps, False)
        self.connect()

        self.select_result_particle()

        return self.finish(), [foreground_intersection, background_intersection]

    def procedural_generate(
        self, start_type, connect_direction, intersection_pos, steps, isFront
    ):
        parsedProb = parseTree.parseProb(
            self.generic_object_list, self.generic_object_list[start_type]
        )

        score_list = []

        for i in range(len(self.particle_list)):
            tempt_particle = self.particle_list[i]
            tempt_particle.prepare_particle(
                intersection_pos, start_type, connect_direction, parsedProb
            )

        for s in range(steps):
            cur_step = steps - s - 1
            print("cur_step", cur_step)

            score_list = []
            for i in range(len(self.particle_list)):
                tempt_particle = self.particle_list[i]
                tempt_particle.run_step(cur_step, isFront)
                score_list.append(tempt_particle.get_score())

            self.particle_list = resample.resample_particles(
                self.particle_list, score_list
            )

        if not isFront:
            success_connect_list = []
            for i in range(len(self.particle_list)):
                self.particle_list[i].connect_extra_system()
                if self.particle_list[i].success:
                    success_connect_list.append(self.particle_list[i])

            self.particle_list = success_connect_list
        print("generation complete")

    def multiple_intersections(self, start_types, connect_directions, intersection_pos):
        success_connect_list = []

        for i in range(len(self.particle_list)):
            tempt_particle = self.particle_list[i]
            for j in range(len(start_types)):
                tempt_particle.arbitrary_add_object(
                    intersection_pos[j], start_types[j], connect_directions[j]
                )

            tempt_particle.arbitrary_connect(0, 1)
            tempt_particle.run_connect()

            if len(connect_directions) == 4:
                tempt_particle.arbitrary_connect(0, 3)
                tempt_particle.run_connect()
                tempt_particle.arbitrary_connect(1, 2)
                tempt_particle.run_connect()

            if len(connect_directions) == 6:
                tempt_particle.arbitrary_connect(2, 3)
                tempt_particle.run_connect()
                tempt_particle.arbitrary_connect(3, 4)
                tempt_particle.run_connect()
                # tempt_particle.arbitrary_connect(5,6)
                # tempt_particle.run_connect()
                # tempt_particle.arbitrary_connect(3,4)
                # tempt_particle.run_connect()

            if self.particle_list[i].success:
                success_connect_list.append(tempt_particle)

        self.particle_list = success_connect_list

    def connect(self):
        success_connect_list = []
        print("len(self.particle_list)", len(self.particle_list))
        for i in range(len(self.particle_list)):
            self.particle_list[i].run_connect()
            if self.particle_list[i].success and self.particle_list[i].score > 0:
                success_connect_list.append(self.particle_list[i])

        self.particle_list = success_connect_list
        success_connect_list = []

        print("successful connected particle list", len(self.particle_list))

    def select_result_particle(self):
        highest_score = self.particle_list[0].score
        self.result_particle = self.particle_list[0]
        for particle in self.particle_list:
            if particle.score > highest_score:
                self.result_particle = particle
                highest_score = particle.score

    def reproduce_particle_list(self, num_particles):
        new_particle_list = []
        multipler = int(num_particles / len(self.particle_list)) + 1

        for particle in self.particle_list:
            for i in range(0, multipler):
                copied_particle = deepcopy(particle)
                new_particle_list.append(copied_particle)

        self.particle_list = new_particle_list

    def finish(self):
        # write the process
        # output_writer = write2JSON.output()
        # output_writer.write_proceudral_objects(
        #     self.result_particle.procedural_objects, "three/process_demo.json"
        # )

        # self.result_particle.procedural_objects[0].type = self.visual_bridge_info['foreground_type'][1]
        procedural_objects = global_execution.global_assign(
            self.result_particle.procedural_objects, self.global__object_list
        )
        decorator = decorations.decoration_operator(self.decorate_path)
        decoration_list = decorator.decorate(procedural_objects)

        print("len procedural_objects", len(procedural_objects))
        print("len decoration_list", len(decoration_list))

        return decoration_list

    def recursive_process(self):
        # phrase: 1->random walk, 2->connect, 3-> decorations
        # find impossible intersection positions
        startPos = np.array([400, 400])
        foreground_index = 8
        background_index = 16

        camera = perspective.ortho_camera()
        foreground_intersection, background_intersection = camera.get_intersections(
            startPos, foreground_index, background_index
        )

        # parse probability tree
        # start produce
        foreground_type = 1
        foreground_connect = "-y"
        foreground_parsedProb = parseTree.parseProb(
            self.generic_object_list, self.generic_object_list[foreground_type]
        )

        background_type = 3
        background_connect = "+y"
        background_parsedProb = parseTree.parseProb(
            self.generic_object_list, self.generic_object_list[background_type]
        )

        steps = 2
        success = False

        phase1 = []
        phase2 = []
        phase3 = []

        decorator = decorations.decoration_operator()
        while success != True:
            print("-----------------")
            cur_particle = particle.Particle(self.generic_object_list)
            cur_particle.prepare_particle(
                foreground_intersection,
                foreground_type,
                foreground_connect,
                foreground_parsedProb,
            )

            for s in range(steps):
                cur_step = steps - s - 1
                cur_particle.run_step(cur_step, True)
            if cur_particle.score == 0:
                continue

            cur_particle.prepare_particle(
                background_intersection,
                background_type,
                background_connect,
                background_parsedProb,
            )
            for s in range(steps):
                cur_step = steps - s - 1
                print("cur_step", cur_step)

                cur_particle.run_step(cur_step, False)
            if cur_particle.score == 0:
                continue

            phase1 = cur_particle.procedural_objects

            cur_particle.run_connect()
            cur_particle.overlapping_check()
            success = cur_particle.success
            if cur_particle.score == 0:
                continue

            phase2 = cur_particle.procedural_objects

        # procedural_objects = assign_type.assign(cur_particle.procedural_objects)

        decoration_list = decorator.decorate(cur_particle.procedural_objects)

        phase3 = decoration_list
        return (phase1, phase2, phase3)

    def branching(
        self, foreground_type, foreground_connect, foreground_intersection, steps
    ):
        for s in range(steps):
            cur_step = steps - s - 1
            print("cur_step", cur_step)

            score_list = []
            for i in range(len(self.particle_list)):
                tempt_particle = self.particle_list[i]
                tempt_particle.branching_run_step(cur_step)
                score_list.append(tempt_particle.get_score())
            self.particle_list = resample.resample_particles(
                self.particle_list, score_list
            )

        success_connect_list = []
        for i in range(len(self.particle_list)):
            self.particle_list[i].branching_connect()
            if self.particle_list[i].success and self.particle_list[i].score > 0:
                success_connect_list.append(self.particle_list[i])
        self.particle_list = success_connect_list
        success_connect_list = []
