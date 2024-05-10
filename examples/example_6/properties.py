import bpy


class MoveSDKPropertiesGeneral(bpy.types.PropertyGroup):
    move_api_key: bpy.props.StringProperty(
        name="API key", description="API key", default="", subtype="PASSWORD"
    )  # type: ignore

    input_video_path: bpy.props.StringProperty(
        name="Input video path",
        description="Input video path",
        default="",
        subtype="FILE_PATH",
    )  # type: ignore

    output_dir: bpy.props.StringProperty(
        name="Output directory",
        description="Output directory",
        default="",
        subtype="DIR_PATH",
    )  # type: ignore

    import_fbx: bpy.props.BoolProperty(
        name="Import FBX", description="Import FBX", default=True
    )  # type: ignore


class MoveSDKProperties(bpy.types.PropertyGroup):
    general: bpy.props.PointerProperty(type=MoveSDKPropertiesGeneral)  # type: ignore

    def register():
        bpy.types.Scene.move_sdk = bpy.props.PointerProperty(type=MoveSDKProperties)
