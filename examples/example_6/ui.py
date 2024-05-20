import bpy
from .operators import (
    MOVE_SDK_OT_run,
    MOVE_SDK_OT_retarget,
    MOVE_SDK_OT_retargeting_clear,
)


def populate_panel_with_bones(
    layout: bpy.types.UILayout,
    scene: bpy.types.Scene,
    rig_type: str,
    ids: list = [],
    add_label: bool = True,
):
    rig = getattr(scene.move_sdk.retargeting, rig_type).rig

    if rig:
        annotations_keys = list(
            getattr(scene.move_sdk.retargeting, rig_type).mapping.__annotations__.keys()
        )

        for index, bone_prop_name in enumerate(annotations_keys):
            if ids and index not in ids:
                continue
            layout.prop_search(
                getattr(scene.move_sdk.retargeting, rig_type).mapping,
                bone_prop_name,
                rig,
                "bones",
                text=[bone_prop_name if add_label else ""][0],
            )

            # Check if the selected bone is valid
            selected_bone = getattr(
                getattr(scene.move_sdk.retargeting, rig_type).mapping, bone_prop_name
            )
            if selected_bone and selected_bone not in rig.bones:
                row = layout.row()
                row.alert = True
                row.label(
                    text=f"Bone {bone_prop_name} '{selected_bone}' not found!",
                    icon="ERROR",
                )
    # else:
    #     layout.label(text="No armature selected or invalid selection")


class MOVE_SDK_PT_main_panel(bpy.types.Panel):
    bl_label = "Move.ai SDK"
    bl_idname = "MOVE_SDK_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move.ai SDK"

    def draw(self, context):
        pass

class MOVE_SDK_PT_general_panel(bpy.types.Panel):
    bl_label = "API"
    bl_idname = "MOVE_SDK_PT_general_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move.ai SDK"
    bl_parent_id = "MOVE_SDK_PT_main_panel"

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene.move_sdk.general, "move_api_key")
        layout.prop(context.scene.move_sdk.general, "input_video_path")
        layout.prop(context.scene.move_sdk.general, "output_dir")
        layout.prop(context.scene.move_sdk.general, "import_fbx")
        layout.operator(MOVE_SDK_OT_run.bl_idname)


class MOVE_SDK_PT_retargeting_panel(bpy.types.Panel):
    bl_label = "Retargeting"
    bl_idname = "MOVE_SDK_PT_retargeting_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move.ai SDK"
    bl_parent_id = "MOVE_SDK_PT_main_panel"

    def draw(self, context):
        layout = self.layout

        layout.operator(MOVE_SDK_OT_retarget.bl_idname)
        layout.separator()

        layout.operator(MOVE_SDK_OT_retargeting_clear.bl_idname)


class MOVE_SDK_PT_retargeting_mapping_panel(bpy.types.Panel):
    def draw_retargeting_panel(self, context, type):
        layout = self.layout
        scene = context.scene

        layout.prop(getattr(scene.move_sdk.retargeting, type), "rig")

        layout.separator()

        populate_panel_with_bones(layout, scene, type, ids=[0, 1, 2, 3])

        layout.separator()

        split = layout.split(factor=0.5)
        column_left = split.column()
        column_right = split.column()

        populate_panel_with_bones(column_left, scene, type, ids=[4, 5, 6, 7])
        populate_panel_with_bones(column_right, scene, type, ids=[8, 9, 10, 11])

        layout.separator()

        split = layout.split(factor=0.5)
        column_left = split.column()
        column_right = split.column()

        populate_panel_with_bones(column_left, scene, type, ids=[12, 13, 14, 15])
        populate_panel_with_bones(column_right, scene, type, ids=[16, 17, 18, 19])

        if getattr(scene.move_sdk.retargeting, type).rig:
            layout.separator()

            split = layout.split(factor=0.5)
            column_left = split.column()
            column_right = split.column()

            row = column_left.row()
            row.label(text="Right Thumb")
            populate_panel_with_bones(row, scene, type, ids=[20, 21, 22], add_label=False)

            row = column_left.row()
            row.label(text="Right Index")
            populate_panel_with_bones(row, scene, type, ids=[23, 24, 25], add_label=False)

            row = column_left.row()
            row.label(text="Right Middle")
            populate_panel_with_bones(row, scene, type, ids=[26, 27, 28], add_label=False)

            row = column_left.row()
            row.label(text="Right Ring")
            populate_panel_with_bones(row, scene, type, ids=[29, 30, 31], add_label=False)

            row = column_left.row()
            row.label(text="Right Pinky")
            populate_panel_with_bones(row, scene, type, ids=[32, 33, 34], add_label=False)

            row = column_right.row()
            row.label(text="Left Thumb")
            populate_panel_with_bones(row, scene, type, ids=[35, 36, 37], add_label=False)

            row = column_right.row()
            row.label(text="Left Index")
            populate_panel_with_bones(row, scene, type, ids=[38, 39, 40], add_label=False)

            row = column_right.row()
            row.label(text="Left Middle")
            populate_panel_with_bones(row, scene, type, ids=[41, 42, 43], add_label=False)

            row = column_right.row()
            row.label(text="Left Ring")
            populate_panel_with_bones(row, scene, type, ids=[44, 45, 46], add_label=False)

            row = column_right.row()
            row.label(text="Left Pinky")
            populate_panel_with_bones(row, scene, type, ids=[47, 48, 49], add_label=False)

class MOVE_SDK_PT_retargeting_target_panel(MOVE_SDK_PT_retargeting_mapping_panel):
    bl_label = "Target rig"
    bl_idname = "MOVE_SDK_PT_retargeting_target_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move.ai SDK"
    bl_parent_id = "MOVE_SDK_PT_retargeting_panel"

    def draw(self, context):
        self.draw_retargeting_panel(context, "target")

class MOVE_SDK_PT_retargeting_source_panel(MOVE_SDK_PT_retargeting_mapping_panel):
    bl_label = "Source rig"
    bl_idname = "MOVE_SDK_PT_retargeting_source_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move.ai SDK"
    bl_parent_id = "MOVE_SDK_PT_retargeting_panel"

    def draw(self, context):
        self.draw_retargeting_panel(context, "source")
