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
    get_mapping_folder,
    add_bone,
    copy_animation_curves,
    select_only_one_object
)
import os
from mathutils import Matrix
from .properties import MoveSDKPropertiesMapping
import json
import string
from pathlib import Path


class MOVE_SDK_OT_run(Operator):
    """Call move.ai SDK"""

    bl_label = "Run"
    bl_idname = "move_sdk.run"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    _timer = None
    _job = None
    _move = None
    _attempts = 0
    _outputs = None
    _input_video_path = None
    _output_dir = None
    _max_attempts = 1200

    def modal(self, context, event):
        if event.type == 'TIMER':
            self._attempts += 1
            job = self._move.get_job(self._job.id)
            update_str = f"Move.ai is {job.state}. Attempt {self._attempts}. Job id: {job.id} is {job.state}"
            print(update_str)
            # context.workspace.status_text_set(update_str)  # Update status bar directly
            self.report({"INFO"}, update_str)  # Update Info panel
            context.window_manager.progress_update(self._attempts)
            context.area.tag_redraw()  # Redraw the UI to reflect updates

            if job.state == "FINISHED":
                input_video_filename = os.path.basename(self._input_video_path)
                self._outputs = self._move.download_outputs(
                    job.id,
                    self._output_dir,
                    input_video_filename.split(".")[0],
                )
                print(self._outputs)
                context.window_manager.progress_end()
                if context.scene.move_sdk.general.import_fbx:
                    bpy.ops.import_scene.fbx(filepath=self._outputs[4])
                context.window_manager.event_timer_remove(self._timer)
                context.workspace.status_text_set(None)  # Clear status bar
                self.report({"INFO"}, "Job completed successfully")
                context.area.tag_redraw()
                return {'FINISHED'}
            elif job.state == "FAILED" or self._attempts >= self._max_attempts:
                self.report({"ERROR"}, "Job failed or maximum attempts reached")
                context.window_manager.progress_end()
                context.window_manager.event_timer_remove(self._timer)
                context.workspace.status_text_set(None)  # Clear status bar
                context.area.tag_redraw()
                return {'CANCELLED'}
            
        elif event.type == 'ESC':
            self.report({"INFO"}, "Job cancelled by user")
            context.window_manager.event_timer_remove(self._timer)
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def execute(self, context):
        self._move = MoveAPI(context.scene.move_sdk.general.move_api_key)
        self._input_video_path = context.scene.move_sdk.general.input_video_path
        self._output_dir = context.scene.move_sdk.general.output_dir

        video_file_id = self._move.create_files(self._input_video_path)
        take = self._move.create_take(video_file_id)
        self._job = self._move.create_job(take.id)
        self._attempts = 0

        context.window_manager.progress_begin(0, 100)
        self._timer = context.window_manager.event_timer_add(1.0, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


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

        source_armature = scene.move_sdk.retargeting.source.rig
        source_obj = get_object_of_armature(source_armature.name)

        retargeted_previosly = False

        for bone in target_obj.pose.bones:
            for constraint in bone.constraints:
                if constraint.name.startswith("Move.ai retargeting:"):
                    retargeted_previosly = True
                    bone.constraints.remove(constraint)

        # Reset hips
        target_bone = target_obj.pose.bones.get(
            scene.move_sdk.retargeting.target.mapping.hips
        )

        # if self.save_original_transforms:
        if retargeted_previosly:
            target_bone.matrix = (
                scene.move_sdk.retargeting.target.hips_original_transforms
            )

        # TODO
        # current_selection = bpy.context.selected_objects
        # current_active_obj = bpy.context.view_layer.objects.active
        # select_only_one_object(source_obj)
        # original_mode = bpy.context.object.mode
        # bpy.ops.object.mode_set(mode='EDIT')
        # for edit_bone in source_obj.data.edit_bones:
        #     if edit_bone.name.startswith('Move.ai retargeting:'):
        #         source_obj.data.edit_bones.remove(edit_bone)

        # for fcurve in source_obj.animation_data.action.fcurves:
        #     if fcurve.data_path.startswith('pose.bones["Move.ai retargeting:'):
        #         source_obj.animation_data.action.fcurves.remove(fcurve)

        # bpy.ops.object.mode_set(mode=original_mode)
        # # deselect everything
        # for selected_obj in bpy.context.selected_objects:
        #     selected_obj.select_set(False)
        # # get original selection back
        # for obj in current_selection:
        #     obj.select_set(True)
        # bpy.context.view_layer.objects.active = current_active_obj

        

        return {"FINISHED"}


class MOVE_SDK_OT_retarget(Operator):
    """Retarget animation"""

    bl_label = "Retarget"
    bl_idname = "move_sdk.retarget"
    bl_options = {"REGISTER", "UNDO", "PRESET"}

    def execute(self, context: bpy.types.Context):
        print("Move.ai: Retargeting...")
        scene = context.scene

        source_armature = scene.move_sdk.retargeting.source.rig
        target_armature = scene.move_sdk.retargeting.target.rig

        if not source_armature and not target_armature:
            self.report({"ERROR"}, "Source and target rigs not selected")
            return {"CANCELLED"}
        elif not source_armature:
            self.report({"ERROR"}, "Source rig not selected")
            return {"CANCELLED"}
        elif not target_armature:
            self.report({"ERROR"}, "Target rig not selected")
            return {"CANCELLED"}

        scene.frame_set(0)

        bpy.ops.move_sdk.retargeting_clear(save_original_transforms=False)

        source_obj = get_object_of_armature(source_armature.name)
        target_obj = get_object_of_armature(target_armature.name)

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
        copy_rotation = add_constraint(
            target_bone,
            "Move.ai retargeting: Copy Rotation",
            "COPY_ROTATION",
            target=source_obj,
            subtarget=source_bone.name,
        )

        copy_rotation.target_space = "POSE"
        copy_rotation.owner_space = "POSE"

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
        # TODO
        # # Create temp hips bone, we're going to offset the hips movement on it for better retargeting
        # current_selection = bpy.context.selected_objects
        # current_active_obj = bpy.context.view_layer.objects.active
        # select_only_one_object(source_obj)
        # original_mode = bpy.context.object.mode
        # bpy.ops.object.mode_set(mode='EDIT')
        # bpy.context.view_layer.update()
        # head = source_obj.data.edit_bones[source_bone.name].head.copy()
        # tail = source_obj.data.edit_bones[source_bone.name].tail.copy()
        # bpy.ops.object.mode_set(mode=original_mode)

        # parent = source_obj.data.bones[source_bone.name].parent.name
        # if not source_obj.data.bones.get('Move.ai retargeting: Temp Hips'):
        #     temp_hips_bone = add_bone(source_obj, 'Move.ai retargeting: Temp Hips', parent_bone=parent, head=head, tail=tail)
        # else:
        #     temp_hips_bone = source_obj.pose.bones['Move.ai retargeting: Temp Hips']

        # copy_animation_curves(source_obj, source_bone.name, source_obj, temp_hips_bone.name)

        # source_bone = temp_hips_bone

        # # deselect everything
        # for selected_obj in bpy.context.selected_objects:
        #     selected_obj.select_set(False)
        # # get original selection back
        # for obj in current_selection:
        #     obj.select_set(True)
        # bpy.context.view_layer.objects.active = current_active_obj

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


class MOVE_SDK_OT_retargeting_create_preset(Operator):
    """Retarget animation"""

    bl_label = "New"
    bl_idname = "move_sdk.create_preset"
    bl_options = {"REGISTER", "UNDO"}  # , "PRESET"}

    preset_name: bpy.props.StringProperty(
        name="Preset Name", description="Name of the new preset", default=""
    )  # type: ignore

    rig_type: bpy.props.StringProperty(
        name="Rig Type",
        description="Specify whether this is for 'source' or 'target'",
        default="source",
        options={"HIDDEN"},
    )  # type: ignore

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        preset_name = self.preset_name

        if not preset_name:
            self.report({"ERROR"}, "Preset name cannot be empty")
            return {"CANCELLED"}

        # Define allowed ASCII printable characters
        allowed_chars = set(string.printable)

        # Check if the preset name contains only allowed ASCII printable characters
        if not all(char in allowed_chars for char in preset_name):
            self.report(
                {"ERROR"},
                "Preset name can only contain ASCII (English) printable characters",
            )
            return {"CANCELLED"}

        folder_path = get_mapping_folder(self.rig_type)
        folder_path.mkdir(parents=True, exist_ok=True)
        file_path = folder_path / f"{preset_name}.json"

        if file_path.exists():
            self.report({"ERROR"}, "File already exists")
            return {"CANCELLED"}

        # Create a blank .json file
        file_path.write_text("{}")

        # switch to the new preset
        getattr(context.scene.move_sdk.retargeting, self.rig_type).presets = preset_name

        self.report({"INFO"}, f"Preset '{preset_name}' created at {file_path}")
        return {"FINISHED"}


class MOVE_SDK_OT_retargeting_save_preset(Operator):
    """Save retargeting preset"""

    bl_label = "Save Preset"
    bl_idname = "move_sdk.save_preset"
    bl_options = {"REGISTER", "UNDO"}

    rig_type: bpy.props.StringProperty(
        name="Rig Type",
        description="Specify whether this is for 'source' or 'target'",
        default="source",
        options={"HIDDEN"},
    )  # type: ignore

    def execute(self, context: bpy.types.Context):
        rig_type = self.rig_type
        preset_name = getattr(context.scene.move_sdk.retargeting, rig_type).presets
        if not preset_name:
            self.report({"ERROR"}, "No preset selected")
            return {"CANCELLED"}

        mapping = getattr(context.scene.move_sdk.retargeting, rig_type).mapping
        folder_path = get_mapping_folder(rig_type)
        folder_path.mkdir(parents=True, exist_ok=True)
        file_path = folder_path / f"{preset_name}.json"

        mapping_data = {
            prop.identifier: getattr(mapping, prop.identifier)
            for prop in MoveSDKPropertiesMapping.bl_rna.properties
            if prop.identifier not in ["rna_type", "name"]
        }

        with file_path.open("w") as f:
            json.dump(mapping_data, f, indent=4)

        self.report({"INFO"}, f"Preset '{preset_name}' saved at {file_path}")
        return {"FINISHED"}


class MOVE_SDK_OT_retargeting_load_preset(Operator):
    """Load retargeting preset"""

    bl_label = "Load Preset"
    bl_idname = "move_sdk.load_preset"
    bl_options = {"REGISTER", "UNDO"}

    rig_type: bpy.props.StringProperty(
        name="Rig Type",
        description="Specify whether this is for 'source' or 'target'",
        default="source",
        options={"HIDDEN"},
    )  # type: ignore

    def execute(self, context: bpy.types.Context):
        rig_type = self.rig_type
        preset_name = getattr(context.scene.move_sdk.retargeting, rig_type).presets
        if not preset_name:
            self.report({"ERROR"}, "No preset selected")
            return {"CANCELLED"}

        mapping = getattr(context.scene.move_sdk.retargeting, rig_type).mapping
        folder_path = get_mapping_folder(rig_type)
        file_path = folder_path / f"{preset_name}.json"

        if not file_path.exists():
            self.report({"ERROR"}, "Preset file does not exist")
            return {"CANCELLED"}

        with file_path.open("r") as f:
            mapping_data = json.load(f)

        for prop, value in mapping_data.items():
            if hasattr(mapping, prop):
                setattr(mapping, prop, value)

        self.report({"INFO"}, f"Preset '{preset_name}' loaded from {file_path}")
        return {"FINISHED"}


class MOVE_SDK_OT_retargeting_delete_preset(Operator):
    """Delete retargeting preset"""

    bl_label = "Delete"
    bl_idname = "move_sdk.delete_preset"
    bl_options = {"REGISTER", "UNDO"}

    preset_name: bpy.props.StringProperty(
        name="Preset Name", description="Name of the preset to delete", default=""
    )  # type: ignore

    rig_type: bpy.props.StringProperty(
        name="Rig Type",
        description="Specify whether this is for 'source' or 'target'",
        default="source",
        options={"HIDDEN"},
    )  # type: ignore

    def invoke(self, context, event):
        self.preset_name = getattr(
            context.scene.move_sdk.retargeting, self.rig_type
        ).presets
        if not self.preset_name:
            self.report({"ERROR"}, "No preset selected")
            return {"CANCELLED"}
        wm = context.window_manager
        return wm.invoke_confirm(self, event)

    def execute(self, context):
        preset_name = self.preset_name
        if not preset_name:
            self.report({"ERROR"}, "Preset name cannot be empty")
            return {"CANCELLED"}

        folder_path = get_mapping_folder(self.rig_type)
        file_path = folder_path / f"{preset_name}.json"

        if not file_path.exists():
            self.report({"ERROR"}, "Preset file does not exist")
            return {"CANCELLED"}

        # Delete the .json file
        file_path.unlink()

        # Clear the preset selection if it was the deleted one
        retargeting = getattr(context.scene.move_sdk.retargeting, self.rig_type)
        if retargeting.presets == preset_name:
            retargeting.presets = ""

        self.report({"INFO"}, f"Preset '{preset_name}' deleted from {file_path}")
        return {"FINISHED"}


class MOVE_SDK_OT_retargeting_rename_preset(Operator):
    """Rename retargeting preset"""

    bl_label = "Rename Preset"
    bl_idname = "move_sdk.rename_preset"
    bl_options = {"REGISTER", "UNDO"}

    new_preset_name: bpy.props.StringProperty(
        name="New Preset Name",
        description="Enter the new name for the preset",
        default="",
    )  # type: ignore

    rig_type: bpy.props.StringProperty(
        name="Rig Type",
        description="Specify whether this is for 'source' or 'target'",
        default="source",
        options={"HIDDEN"},
    )  # type: ignore

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        rig_type = self.rig_type
        current_preset_name = getattr(
            context.scene.move_sdk.retargeting, rig_type
        ).presets
        new_preset_name = self.new_preset_name

        if not current_preset_name:
            self.report({"ERROR"}, "No preset selected")
            return {"CANCELLED"}

        if not new_preset_name:
            self.report({"ERROR"}, "New preset name cannot be empty")
            return {"CANCELLED"}

        folder_path = get_mapping_folder(rig_type)
        current_file_path = folder_path / f"{current_preset_name}.json"
        new_file_path = folder_path / f"{new_preset_name}.json"

        if not current_file_path.exists():
            self.report({"ERROR"}, "Current preset file does not exist")
            return {"CANCELLED"}

        if new_file_path.exists():
            self.report({"ERROR"}, "A preset with the new name already exists")
            return {"CANCELLED"}

        current_file_path.rename(new_file_path)

        # Update the preset name in the context
        getattr(context.scene.move_sdk.retargeting, rig_type).presets = new_preset_name

        self.report(
            {"INFO"}, f"Preset '{current_preset_name}' renamed to '{new_preset_name}'"
        )
        return {"FINISHED"}


class MOVE_SDK_OT_append_file(Operator):
    bl_idname = "move_sdk.append_file"
    bl_label = "Append File"
    bl_description = "Append data from another .blend file"

    def execute(self, context):
        filepath = bpy.path.abspath(context.scene.move_sdk.append.filepath)
        try:
            # Load collections, worlds, and scenes
            with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
                data_to.collections = data_from.collections
                data_to.worlds = data_from.worlds
                data_to.scenes = data_from.scenes

            for collection in data_to.collections:
                bpy.context.scene.collection.children.link(collection)

            # Set the appended world as the current scene world
            if data_to.worlds and context.scene.move_sdk.append.import_world:
                bpy.context.scene.world = data_to.worlds[0]

            # Overwrite current scene settings with those from the imported scene
            if data_to.scenes and context.scene.move_sdk.append.import_scene:
                imported_scene = data_to.scenes[0]
                current_scene = bpy.context.scene

                # Copy all properties dynamically
                for prop in dir(imported_scene):
                    if prop.startswith("__") or prop in {
                        "name",
                        "users",
                        "use_fake_user",
                        "tag",
                        "is_library_indirect",
                        "asset_data",
                        "asset_mark",
                    }:
                        continue
                    try:
                        setattr(current_scene, prop, getattr(imported_scene, prop))
                    except (AttributeError, TypeError, ValueError):
                        pass  # Skip properties that can't be set or are read-only

            self.report(
                {"INFO"}, "Collections, world, and scene settings appended successfully"
            )
            return {"FINISHED"}
        except Exception as e:
            self.report(
                {"ERROR"}, f"Failed to append collections, world, or scene: {e}"
            )
            return {"CANCELLED"}
