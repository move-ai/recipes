import bpy
import os
import requests
from move_ugc import MoveUgc
import subprocess
import sys
import bpy_types
from mathutils import Matrix
import numpy as np


class MoveAPI:
    def __init__(self, api_key, endpoint_url=None):
        self.api_key = api_key
        if endpoint_url is None:
            endpoint_url = "https://api.move.ai/ugc/graphql"
        self.endpoint_url = endpoint_url
        self.client = MoveUgc(api_key=api_key, endpoint_url=endpoint_url)

    def create_files(self, video_path):
        video_file = self.client.files.create(file_type="mp4")

        with open(video_path, "rb") as f:
            requests.put(video_file.presigned_url, data=f.read())

        return video_file.id

    def create_take(self, video_file_id, metadata=None):
        if metadata is None:
            metadata = {"test": "test"}
        take = self.client.takes.create(
            video_file_id=video_file_id,
            metadata=metadata,
        )
        return take

    def get_take(self, take_id):
        take = self.client.takes.retrieve(id=take_id)
        return take

    def create_job(self, take_id):
        job = self.client.jobs.create(take_id=take_id, metadata={"test": "test_job"})
        return job

    def get_job(self, job_id, expand=False):
        # Get a job using the Move One Public API
        # Implement job retrieval logic using move_ugc_python SDK
        if expand is False:
            job = self.client.jobs.retrieve(id=job_id)
        else:
            job = self.client.jobs.retrieve(
                id=job_id, expand=["take", "outputs", "client"]
            )
        return job

    def download_outputs(self, job_id, output_dir, output_name):
        # make output dir if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # get job
        job = self.get_job(job_id, expand=True)
        # for each output download the file in the output_dir
        output_paths = []
        for output in job.outputs:
            output_file_name = f"{output_name}{output.file.type}"
            output_path = os.path.join(output_dir, output_file_name)
            with open(output_path, "wb") as f:
                response = requests.get(output.file.presigned_url)
                f.write(response.content)
            output_paths.append(output_path)
        return output_paths


def add_constraint(
    bone, name, constraint_type, target=None, subtarget=None, influence=1
):
    constraint = bone.constraints.new(constraint_type)
    constraint.name = name
    if target is not None:
        constraint.target = target
    if subtarget is not None:
        constraint.subtarget = subtarget
    constraint.influence = influence
    return constraint


def get_object_of_armature(armature_name):
    armature = bpy.data.armatures.get(armature_name)
    for obj in bpy.data.objects:
        if obj.type == "ARMATURE":
            if obj.data == armature:
                return obj


def get_matrix(bone_or_obj):
    if isinstance(bone_or_obj, bpy_types.PoseBone):
        # Convert matrix to world space
        arm = bone_or_obj.id_data
        mat = arm.matrix_world @ bone_or_obj.matrix
    elif isinstance(bone_or_obj, Matrix):
        mat = bone_or_obj
    else:
        mat = bone_or_obj.matrix_world

    return mat


def set_matrix(context: bpy_types.Context, mat: Matrix, bone_or_obj) -> None:
    if isinstance(bone_or_obj, bpy_types.PoseBone):
        # Convert matrix to local space
        arm_eval = context.active_object.evaluated_get(context.view_layer.depsgraph)
        bone_or_obj.matrix = arm_eval.matrix_world.inverted() @ mat
    else:
        context.active_object.matrix_world = mat


def get_offsets_rot(source, target, rot_mode):
    source_world = get_matrix(source)
    target_world = get_matrix(target)

    source_quat = source_world.to_quaternion()
    target_quat = target_world.to_quaternion()
    dif_quat = target_quat.rotation_difference(source_quat)
    dif_euler = dif_quat.to_euler()

    if rot_mode == "quaternion":
        return dif_quat
    if rot_mode == "euler":
        return dif_euler


def get_distance(start, end):
    start_world = get_matrix(start)
    end_world = get_matrix(end)
    distance = np.linalg.norm(start_world.to_translation() - end_world.to_translation())
    return distance


def get_matrix_height(matrix_world: Matrix):
    start_world = Matrix().to_translation()
    translation = matrix_world.to_translation()
    translation.x = 0
    translation.y = 0
    distance = np.linalg.norm(start_world - translation)
    return distance


def flatten_matrix(mat):
    dim = len(mat)
    return [mat[j][i] for i in range(dim) for j in range(dim)]
