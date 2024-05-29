import bpy
import os
import requests
from move_ugc import MoveUgc
import subprocess
import sys
import bpy_types
from mathutils import Matrix
import numpy as np
import addon_utils
from pathlib import Path

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

def get_mapping_folder(rig_type="source"):
    for mod in addon_utils.modules():
        if mod.bl_info['name'] == "Move SDK":
            filepath = Path(mod.__file__)

    mapping_folder = filepath.parent / "data/mapping_templates" / rig_type

    return mapping_folder

def select_only_one_object(obj):
    for selected_obj in bpy.context.selected_objects:
        selected_obj.select_set(False)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

def add_bone(rig_obj, bone_name, parent_bone=None, head=(0, 0, 0), tail=(0, 1, 0)):
    original_mode = bpy.context.object.mode
    armature = rig_obj.data
    select_only_one_object(rig_obj)
    bpy.ops.object.mode_set(mode='EDIT')
    new_bone = armature.edit_bones.new(bone_name)
    if parent_bone:
        new_bone.parent = armature.edit_bones[parent_bone]
    new_bone.head = head
    new_bone.tail = tail
    bpy.ops.object.mode_set(mode=original_mode)
    return rig_obj.pose.bones[bone_name]

def copy_animation_curves(source_obj, source_bone, target_obj, target_bone):
    if source_obj.animation_data and source_obj.animation_data.action:
        action = source_obj.animation_data.action
        for fcurve in action.fcurves:
            if fcurve.data_path.startswith(f'pose.bones["{source_bone}"]'):
                target_data_path = f'pose.bones["{target_bone}"].' + fcurve.data_path.split('.')[-1]
                
                # Check if the fcurve already exists
                target_fcurve = None
                for tfcurve in action.fcurves:
                    if tfcurve.data_path == target_data_path and tfcurve.array_index == fcurve.array_index:
                        target_fcurve = tfcurve
                        break

                # If it doesn't exist, create a new one
                if not target_fcurve:
                    target_fcurve = action.fcurves.new(
                        data_path=target_data_path,
                        index=fcurve.array_index
                    )
                    target_fcurve.keyframe_points.add(len(fcurve.keyframe_points))
                
                # Update the keyframe points
                for i, keyframe in enumerate(fcurve.keyframe_points):
                    if i < len(target_fcurve.keyframe_points):
                        target_keyframe = target_fcurve.keyframe_points[i]
                    else:
                        target_keyframe = target_fcurve.keyframe_points.insert(
                            keyframe.co[0], keyframe.co[1], {'NEEDED'}
                        )
                    target_keyframe.co = keyframe.co
                    target_keyframe.interpolation = keyframe.interpolation
