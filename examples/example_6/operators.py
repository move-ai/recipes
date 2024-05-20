import bpy
import time
from datetime import datetime
from bpy.types import Operator
from .utils import (
    MoveAPI,
    add_constraint,
    get_object_of_armature,
    get_offsets_rot,
    get_distance,
    get_matrix,
    set_matrix,
    get_matrix_height,
    flatten_matrix,
)
import os
from mathutils import Matrix


class MOVE_SDK_OT_run(Operator):
    """Call move.ai SDK"""

    bl_label = "Run"
    bl_idname = "move_sdk.run"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    def execute(self, context: bpy.types.Context):
        context.window_manager.progress_begin(0, 100)

        move = MoveAPI(context.scene.move_sdk.general.move_api_key)
        input_video_path = context.scene.move_sdk.general.input_video_path
        video_file_id = move.create_files(input_video_path)
        take = move.create_take(video_file_id)
        job = move.create_job(take.id)
        attempts = 0
        while job.state != "FAILED" and attempts < 100:
            job = move.get_job(job.id)
            update_str = f"[{datetime.now().isoformat()} | {attempts}] Job {job.id} is {job.state}"
            print(update_str)
            context.window_manager.progress_update(attempts)
            if job.state == "FINISHED":
                input_video_filename = os.path.basename(input_video_path)
                outputs = move.download_outputs(
                    job.id,
                    context.scene.move_sdk.general.output_dir,
                    input_video_filename.split(".")[0],
                )
                print(outputs)
                break
            else:
                time.sleep(30)
                attempts += 1

        if context.scene.move_sdk.general.import_fbx:
            bpy.ops.import_scene.fbx(filepath=outputs[4])

        context.window_manager.progress_end()

        return {"FINISHED"}


class MOVE_SDK_OT_retargeting_clear(Operator):
    """Clear constraints"""

    bl_label = "Clear Constraints"
    bl_idname = "move_sdk.retargeting_clear"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    save_original_transforms: bpy.props.BoolProperty(
        default=True, name="Save original transforms"
    )  # type: ignore

    def execute(self, context: bpy.types.Context):
        scene = context.scene
        target_armature = scene.move_sdk.retargeting.target.rig
        target_obj = get_object_of_armature(target_armature.name)

        retargeted_previosly = False

        for bone in target_obj.pose.bones:
            for constraint in bone.constraints:
                if constraint.name.startswith("Move.ai retargeting:"):
                    retargeted_previosly = True
                    bone.constraints.remove(constraint)

        # Reset hips
        target_bone = target_obj.pose.bones.get(scene.move_sdk.retargeting.target.mapping.hips)

        # if self.save_original_transforms:
        if retargeted_previosly:
            target_bone.matrix = (
                scene.move_sdk.retargeting.target.hips_original_transforms
            )

        return {"FINISHED"}


class MOVE_SDK_OT_retarget(Operator):
    """Retarget animation"""

    bl_label = "Retarget"
    bl_idname = "move_sdk.retarget"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    def execute(self, context: bpy.types.Context):
        print("Retargeting...")

        bpy.context.scene.frame_set(0)

        bpy.ops.move_sdk.retargeting_clear(save_original_transforms=False)

        scene = context.scene

        source_armature = scene.move_sdk.retargeting.source.rig
        target_armature = scene.move_sdk.retargeting.target.rig

        source_obj = get_object_of_armature(source_armature.name)
        target_obj = get_object_of_armature(target_armature.name)

        if not source_armature and not target_armature:
            self.report({"ERROR"}, "Source and target rigs not selected")
            return {"CANCELLED"}
        elif not source_armature:
            self.report({"ERROR"}, "Source rig not selected")
            return {"CANCELLED"}
        elif not target_armature:
            self.report({"ERROR"}, "Target rig not selected")
            return {"CANCELLED"}

        target_bone_properties_names = list(
            scene.move_sdk.retargeting.target.mapping.__annotations__.keys()
        )

        for bone_prop_name in target_bone_properties_names:
            target_bone_name = getattr(
                scene.move_sdk.retargeting.target.mapping, bone_prop_name
            )
            source_bone_name = getattr(
                scene.move_sdk.retargeting.source.mapping, bone_prop_name
            )
            target_bone = target_obj.pose.bones.get(target_bone_name)
            source_bone = source_obj.pose.bones.get(source_bone_name)
            if target_bone:
                if bone_prop_name == "hips":
                    self.retarget_location(
                        context, source_obj, target_bone, source_bone
                    )

                self.retarget_rotation(source_obj, target_bone, source_bone)

        return {"FINISHED"}

    def retarget_rotation(self, source_obj, target_bone, source_bone):
        add_constraint(
            target_bone,
            "Move.ai retargeting: Copy Rotation",
            "COPY_ROTATION",
            target=source_obj,
            subtarget=source_bone.name,
        )

        offset_rot = get_offsets_rot(
            target_bone,
            source_bone,
            "euler",
        )

        offset_constraint = add_constraint(
            target_bone,
            "Move.ai retargeting: Offset",
            "TRANSFORM",
            source_obj,
            source_obj.pose.bones[0].name,
        )
        offset_constraint.target_space = "LOCAL"
        offset_constraint.owner_space = "LOCAL"
        offset_constraint.map_to = "ROTATION"
        offset_constraint.mix_mode_rot = "AFTER"

        offset_constraint.to_min_x_rot = offset_rot[0]
        offset_constraint.to_min_y_rot = offset_rot[1]
        offset_constraint.to_min_z_rot = offset_rot[2]

    def retarget_location(self, context, source_obj, target_bone, source_bone):
        target_bone_matrix = get_matrix(target_bone)
        source_bone_matrix = get_matrix(source_bone)

        context.scene.move_sdk.retargeting.target.hips_original_transforms = (
            flatten_matrix(target_bone.matrix.copy())
        )

        target_hips_height = get_matrix_height(target_bone_matrix.copy())
        source_hips_height = get_matrix_height(source_bone_matrix.copy())

        leg_ratio = target_hips_height / source_hips_height
        # original_hips_matrix = get_matrix(target_bone).copy()
        # original_hips_loc = target_bone_matrix.copy().to_translation()

        # if target_bone.rotation_mode == "QUATERNION":
        #     original_hips_rot = target_bone_matrix.copy().to_quaternion()
        # elif target_bone.rotation_mode in [
        #     "XYZ",
        #     "XZY",
        #     "YXZ",
        #     "YZX",
        #     "ZXY",
        #     "ZYX",
        # ]:
        #     original_hips_rot = target_bone_matrix.copy().to_euler(
        #         target_bone.rotation_mode
        #     )

        # original_hips_scale = target_bone_matrix.copy().to_scale()

        copy_loc_constraint = add_constraint(
            target_bone,
            "Move.ai retargeting: Copy Location",
            "COPY_LOCATION",
            target=source_obj,
            subtarget=source_bone.name,
            influence=leg_ratio,
        )
        copy_loc_constraint.use_offset = True

        hips_offset = source_bone_matrix.translation * leg_ratio

        target_bone_matrix.translation -= hips_offset
        set_matrix(context, target_bone_matrix, target_bone)

        # target_bone.scale = original_hips_scale
        # if target_bone.rotation_mode == "QUATERNION":
        #     target_bone.rotation_quaternion = original_hips_rot
        # elif target_bone.rotation_mode in [
        #     "XYZ",
        #     "XZY",
        #     "YXZ",
        #     "YZX",
        #     "ZXY",
        #     "ZYX",
        # ]:
        #     target_bone.rotation_euler = original_hips_rot
