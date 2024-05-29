import bpy
from .operators import (
    MOVE_SDK_OT_run,
    MOVE_SDK_OT_retarget,
    MOVE_SDK_OT_retargeting_clear,
    MOVE_SDK_OT_retargeting_create_preset,
    MOVE_SDK_OT_retargeting_save_preset,
    MOVE_SDK_OT_retargeting_load_preset,
    MOVE_SDK_OT_retargeting_delete_preset,
    MOVE_SDK_OT_retargeting_rename_preset,
    MOVE_SDK_OT_append_file,
)

from bl_ui.utils import PresetPanel


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


# class MOVE_SDK_PT_main_panel(bpy.types.Panel):
#     bl_label = "Move.ai SDK"
#     bl_idname = "MOVE_SDK_PT_main_panel"
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_category = "Move.ai SDK"

#     def draw(self, context):
#         pass


class MOVE_SDK_PT_general_panel(bpy.types.Panel):
    bl_label = "API"
    bl_idname = "MOVE_SDK_PT_general_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move.ai SDK"
    # bl_parent_id = "MOVE_SDK_PT_main_panel"

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
    bl_options = {"DEFAULT_CLOSED"}
    # bl_parent_id = "MOVE_SDK_PT_main_panel"

    def draw(self, context):
        layout = self.layout

        layout.operator(MOVE_SDK_OT_retarget.bl_idname)
        layout.separator()

        layout.operator(MOVE_SDK_OT_retargeting_clear.bl_idname)


class MOVE_SDK_PT_scene_panel(bpy.types.Panel):
    bl_label = "Import Scene"
    bl_idname = "MOVE_SDK_PT_scene_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move.ai SDK"
    bl_options = {"DEFAULT_CLOSED"}
    # bl_parent_id = "MOVE_SDK_PT_main_panel"

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene.move_sdk.append, "filepath")
        layout.prop(context.scene.move_sdk.append, "import_scene")
        layout.prop(context.scene.move_sdk.append, "import_world")
        layout.operator(MOVE_SDK_OT_append_file.bl_idname)


class MOVE_SDK_PT_test_files_panel(bpy.types.Panel):
    bl_label = "Test Files"
    bl_idname = "MOVE_SDK_PT_test_files_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move.ai SDK"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "MOVE_SDK_PT_scene_panel"

    def draw(self, context):
        layout = self.layout

        layout.prop(context.scene.move_sdk.append, "test_rig_path")
        layout.prop(context.scene.move_sdk.append, "test_scene_path")


class MOVE_SDK_PT_retargeting_mapping_panel(bpy.types.Panel):
    def draw_retargeting_panel(self, context, rig_type):
        layout = self.layout
        scene = context.scene

        layout.separator()

        populate_panel_with_bones(layout, scene, rig_type, ids=[0, 1, 2, 3])

        layout.separator()

        split = layout.split(factor=0.5)
        column_left = split.column()
        column_right = split.column()

        populate_panel_with_bones(column_left, scene, rig_type, ids=[4, 5, 6, 7])
        populate_panel_with_bones(column_right, scene, rig_type, ids=[8, 9, 10, 11])

        layout.separator()

        split = layout.split(factor=0.5)
        column_left = split.column()
        column_right = split.column()

        populate_panel_with_bones(column_left, scene, rig_type, ids=[12, 13, 14, 15])
        populate_panel_with_bones(column_right, scene, rig_type, ids=[16, 17, 18, 19])

        if getattr(scene.move_sdk.retargeting, rig_type).rig:
            layout.separator()

            split = layout.split(factor=0.5)
            column_left = split.column()
            column_right = split.column()

            row = column_left.row()
            row.label(text="Right Thumb")
            populate_panel_with_bones(
                row, scene, rig_type, ids=[20, 21, 22], add_label=False
            )

            row = column_left.row()
            row.label(text="Right Index")
            populate_panel_with_bones(
                row, scene, rig_type, ids=[23, 24, 25], add_label=False
            )

            row = column_left.row()
            row.label(text="Right Middle")
            populate_panel_with_bones(
                row, scene, rig_type, ids=[26, 27, 28], add_label=False
            )

            row = column_left.row()
            row.label(text="Right Ring")
            populate_panel_with_bones(
                row, scene, rig_type, ids=[29, 30, 31], add_label=False
            )

            row = column_left.row()
            row.label(text="Right Pinky")
            populate_panel_with_bones(
                row, scene, rig_type, ids=[32, 33, 34], add_label=False
            )

            row = column_right.row()
            row.label(text="Left Thumb")
            populate_panel_with_bones(
                row, scene, rig_type, ids=[35, 36, 37], add_label=False
            )

            row = column_right.row()
            row.label(text="Left Index")
            populate_panel_with_bones(
                row, scene, rig_type, ids=[38, 39, 40], add_label=False
            )

            row = column_right.row()
            row.label(text="Left Middle")
            populate_panel_with_bones(
                row, scene, rig_type, ids=[41, 42, 43], add_label=False
            )

            row = column_right.row()
            row.label(text="Left Ring")
            populate_panel_with_bones(
                row, scene, rig_type, ids=[44, 45, 46], add_label=False
            )

            row = column_right.row()
            row.label(text="Left Pinky")
            populate_panel_with_bones(
                row, scene, rig_type, ids=[47, 48, 49], add_label=False
            )
        else:
            layout.label(text="No armature selected or invalid selection")


class MOVE_SDK_PT_retargeting_target_panel(MOVE_SDK_PT_retargeting_mapping_panel):
    bl_label = "Target rig"
    bl_idname = "MOVE_SDK_PT_retargeting_target_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move.ai SDK"
    bl_parent_id = "MOVE_SDK_PT_retargeting_panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        layout.prop(scene.move_sdk.retargeting.target, "rig")


class MOVE_SDK_PT_retargeting_source_panel(MOVE_SDK_PT_retargeting_mapping_panel):
    bl_label = "Source rig"
    bl_idname = "MOVE_SDK_PT_retargeting_source_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move.ai SDK"
    bl_parent_id = "MOVE_SDK_PT_retargeting_panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        layout.prop(scene.move_sdk.retargeting.source, "rig")


class MOVE_SDK_PT_retargeting_target_mapping_panel(
    MOVE_SDK_PT_retargeting_mapping_panel
):
    bl_label = "Bone Mapping"
    bl_idname = "MOVE_SDK_PT_retargeting_target_mapping_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move.ai SDK"
    bl_parent_id = "MOVE_SDK_PT_retargeting_target_panel"

    def draw(self, context):
        self.draw_retargeting_panel(context, "target")


class MOVE_SDK_PT_retargeting_source_mapping_panel(
    MOVE_SDK_PT_retargeting_mapping_panel
):
    bl_label = "Bone Mapping"
    bl_idname = "MOVE_SDK_PT_retargeting_source_mapping_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move.ai SDK"
    bl_parent_id = "MOVE_SDK_PT_retargeting_source_panel"

    def draw(self, context):
        self.draw_retargeting_panel(context, "source")


class MOVE_SDK_PT_retargeting_target_presets_panel(
    MOVE_SDK_PT_retargeting_mapping_panel
):
    bl_label = "Presets"
    bl_idname = "MOVE_SDK_PT_retargeting_target_presets_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move.ai SDK"
    bl_parent_id = "MOVE_SDK_PT_retargeting_target_panel"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        row = layout.row()

        cols = row.split(factor=0.80)

        cols.prop(scene.move_sdk.retargeting.target, "presets")
        create_preset = cols.operator(
            MOVE_SDK_OT_retargeting_create_preset.bl_idname, icon="ADD"
        )
        create_preset.rig_type = "target"

        delete_preset = cols.operator(
            MOVE_SDK_OT_retargeting_delete_preset.bl_idname, icon="REMOVE"
        )
        delete_preset.rig_type = "target"

        row = layout.row()

        cols = row.split(factor=0.33)
        save_preset = cols.operator(
            MOVE_SDK_OT_retargeting_save_preset.bl_idname, icon="FILE_TICK"
        )
        save_preset.rig_type = "target"

        load_preset = cols.operator(
            MOVE_SDK_OT_retargeting_load_preset.bl_idname, icon="FILEBROWSER"
        )
        load_preset.rig_type = "target"

        rename_preset = cols.operator(
            MOVE_SDK_OT_retargeting_rename_preset.bl_idname, icon="OUTLINER_OB_FONT"
        )
        rename_preset.rig_type = "target"


class MOVE_SDK_PT_retargeting_source_presets_panel(
    MOVE_SDK_PT_retargeting_mapping_panel
):
    bl_label = "Presets"
    bl_idname = "MOVE_SDK_PT_retargeting_source_presets_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move.ai SDK"
    bl_parent_id = "MOVE_SDK_PT_retargeting_source_panel"

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        row = layout.row()

        cols = row.split(factor=0.80)

        cols.prop(scene.move_sdk.retargeting.source, "presets")
        create_preset = cols.operator(
            MOVE_SDK_OT_retargeting_create_preset.bl_idname, icon="ADD"
        )
        create_preset.rig_type = "source"

        delete_preset = cols.operator(
            MOVE_SDK_OT_retargeting_delete_preset.bl_idname, icon="REMOVE"
        )
        delete_preset.rig_type = "source"

        row = layout.row()

        cols = row.split(factor=0.33)
        save_preset = cols.operator(
            MOVE_SDK_OT_retargeting_save_preset.bl_idname, icon="FILE_TICK"
        )
        save_preset.rig_type = "source"

        load_preset = cols.operator(
            MOVE_SDK_OT_retargeting_load_preset.bl_idname, icon="FILEBROWSER"
        )
        load_preset.rig_type = "source"

        rename_preset = cols.operator(
            MOVE_SDK_OT_retargeting_rename_preset.bl_idname, icon="OUTLINER_OB_FONT"
        )
        rename_preset.rig_type = "source"


class MOVE_SDK_PT_ffmpeg_presets(PresetPanel, bpy.types.Panel):
    bl_label = "FFmpeg Presets"
    preset_subdir = "ffmpeg"
    preset_operator = "script.python_file_run"


class RenderOutputButtonsPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Move.ai SDK"
    #    bl_context = "output"
    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES


class MOVE_SDK_PT_output(RenderOutputButtonsPanel, bpy.types.Panel):
    bl_label = "Render"
    bl_options = {"DEFAULT_CLOSED"}
    COMPAT_ENGINES = {
        "BLENDER_RENDER",
        "BLENDER_EEVEE",
        "BLENDER_EEVEE_NEXT",
        "BLENDER_WORKBENCH",
    }

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False  # No animation.

        rd = context.scene.render
        image_settings = rd.image_settings

        layout.prop(rd, "filepath", text="")

        layout.use_property_split = True

        col = layout.column(heading="Saving")
        col.prop(rd, "use_file_extension")
        col.prop(rd, "use_render_cache")

        layout.template_image_settings(image_settings, color_management=False)

        if not rd.is_movie_format:
            col = layout.column(heading="Image Sequence")
            col.prop(rd, "use_overwrite")
            col.prop(rd, "use_placeholder")

        render = layout.operator("render.render", text="Render Animation")
        render.animation = True


class MOVE_SDK_PT_output_views(RenderOutputButtonsPanel, bpy.types.Panel):
    bl_label = "Views"
    bl_parent_id = "MOVE_SDK_PT_output"
    COMPAT_ENGINES = {
        "BLENDER_RENDER",
        "BLENDER_EEVEE",
        "BLENDER_EEVEE_NEXT",
        "BLENDER_WORKBENCH",
    }

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.use_multiview

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False  # No animation.

        rd = context.scene.render
        layout.template_image_views(rd.image_settings)


class MOVE_SDK_PT_output_color_management(RenderOutputButtonsPanel, bpy.types.Panel):
    bl_label = "Color Management"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = "MOVE_SDK_PT_output"
    COMPAT_ENGINES = {
        "BLENDER_RENDER",
        "BLENDER_EEVEE",
        "BLENDER_EEVEE_NEXT",
        "BLENDER_WORKBENCH",
    }

    def draw(self, context):
        scene = context.scene
        image_settings = scene.render.image_settings

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        layout.row().prop(image_settings, "color_management", text=" ", expand=True)

        flow = layout.grid_flow(
            row_major=True, columns=0, even_columns=False, even_rows=False, align=True
        )

        if image_settings.color_management == "OVERRIDE":
            owner = image_settings
        else:
            owner = scene
            flow.enabled = False

        col = flow.column()

        if image_settings.has_linear_colorspace:
            if hasattr(owner, "linear_colorspace_settings"):
                col.prop(owner.linear_colorspace_settings, "name", text="Color Space")
        else:
            col.prop(owner.display_settings, "display_device")
            col.separator()
            col.template_colormanaged_view_settings(owner, "view_settings")


class MOVE_SDK_PT_encoding(RenderOutputButtonsPanel, bpy.types.Panel):
    bl_label = "Encoding"
    bl_parent_id = "MOVE_SDK_PT_output"
    bl_options = {"DEFAULT_CLOSED"}
    COMPAT_ENGINES = {
        "BLENDER_RENDER",
        "BLENDER_EEVEE",
        "BLENDER_EEVEE_NEXT",
        "BLENDER_WORKBENCH",
    }

    def draw_header_preset(self, _context):
        MOVE_SDK_PT_ffmpeg_presets.draw_panel_header(self.layout)

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.image_settings.file_format in {"FFMPEG", "XVID", "H264", "THEORA"}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        rd = context.scene.render
        ffmpeg = rd.ffmpeg

        layout.prop(rd.ffmpeg, "format")
        layout.prop(ffmpeg, "use_autosplit")


class MOVE_SDK_PT_encoding_video(RenderOutputButtonsPanel, bpy.types.Panel):
    bl_label = "Video"
    bl_parent_id = "MOVE_SDK_PT_encoding"
    COMPAT_ENGINES = {
        "BLENDER_RENDER",
        "BLENDER_EEVEE",
        "BLENDER_EEVEE_NEXT",
        "BLENDER_WORKBENCH",
    }

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.image_settings.file_format in {"FFMPEG", "XVID", "H264", "THEORA"}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        self.draw_vcodec(context)

    def draw_vcodec(self, context):
        """Video codec options."""
        layout = self.layout
        ffmpeg = context.scene.render.ffmpeg

        needs_codec = ffmpeg.format in {
            "AVI",
            "QUICKTIME",
            "MKV",
            "OGG",
            "MPEG4",
            "WEBM",
        }
        if needs_codec:
            layout.prop(ffmpeg, "codec")

        if needs_codec and ffmpeg.codec == "NONE":
            return

        if ffmpeg.codec == "DNXHD":
            layout.prop(ffmpeg, "use_lossless_output")

        # Output quality
        use_crf = needs_codec and ffmpeg.codec in {
            "H264",
            "MPEG4",
            "WEBM",
            "AV1",
        }
        if use_crf:
            layout.prop(ffmpeg, "constant_rate_factor")

        # Encoding speed
        layout.prop(ffmpeg, "ffmpeg_preset")
        # I-frames
        layout.prop(ffmpeg, "gopsize")
        # B-Frames
        row = layout.row(align=True, heading="Max B-frames")
        row.prop(ffmpeg, "use_max_b_frames", text="")
        sub = row.row(align=True)
        sub.active = ffmpeg.use_max_b_frames
        sub.prop(ffmpeg, "max_b_frames", text="")

        if not use_crf or ffmpeg.constant_rate_factor == "NONE":
            col = layout.column()

            sub = col.column(align=True)
            sub.prop(ffmpeg, "video_bitrate")
            sub.prop(ffmpeg, "minrate", text="Minimum")
            sub.prop(ffmpeg, "maxrate", text="Maximum")

            col.prop(ffmpeg, "buffersize", text="Buffer")

            col.separator()

            col.prop(ffmpeg, "muxrate", text="Mux Rate")
            col.prop(ffmpeg, "packetsize", text="Mux Packet Size")


class MOVE_SDK_PT_encoding_audio(RenderOutputButtonsPanel, bpy.types.Panel):
    bl_label = "Audio"
    bl_parent_id = "MOVE_SDK_PT_encoding"
    COMPAT_ENGINES = {
        "BLENDER_RENDER",
        "BLENDER_EEVEE",
        "BLENDER_EEVEE_NEXT",
        "BLENDER_WORKBENCH",
    }

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.image_settings.file_format in {"FFMPEG", "XVID", "H264", "THEORA"}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        rd = context.scene.render
        ffmpeg = rd.ffmpeg

        if ffmpeg.format != "MP3":
            layout.prop(ffmpeg, "audio_codec", text="Audio Codec")

        if ffmpeg.audio_codec != "NONE":
            layout.prop(ffmpeg, "audio_channels")
            layout.prop(ffmpeg, "audio_mixrate", text="Sample Rate")
            layout.prop(ffmpeg, "audio_bitrate")
            layout.prop(ffmpeg, "audio_volume", slider=True)


class MOVE_SDK_UL_renderviews(bpy.types.UIList):
    def draw_item(
        self, _context, layout, _data, item, icon, _active_data, _active_propname, index
    ):
        view = item
        if self.layout_type in {"DEFAULT", "COMPACT"}:
            if view.name in {"left", "right"}:
                layout.label(text=view.name, icon_value=icon + (not view.use))
            else:
                layout.prop(
                    view, "name", text="", index=index, icon_value=icon, emboss=False
                )
            layout.prop(view, "use", text="", index=index)

        elif self.layout_type == "GRID":
            layout.alignment = "CENTER"
            layout.label(text="", icon_value=icon + (not view.use))
