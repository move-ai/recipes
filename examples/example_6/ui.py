import bpy
from .operators import MOVE_SDK_OT_run


class MOVE_SDK_PT_main_panel(bpy.types.Panel):
    bl_label = "Move.ai SDK"
    bl_idname = "MOVE_SDK_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move.ai SDK"

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene.move_sdk.general, "move_api_key")
        layout.prop(context.scene.move_sdk.general, "input_video_path")
        layout.prop(context.scene.move_sdk.general, "output_dir")
        layout.prop(context.scene.move_sdk.general, "import_fbx")
        layout.operator(MOVE_SDK_OT_run.bl_idname)
