import bpy
from mathutils import Matrix
from .utils import flatten_matrix, get_mapping_folder
import addon_utils
from pathlib import Path
import os


def my_settings_callback(scene, context, rig_type):
    # get to mapping_templates folder or create if there isn't one
    mapping_folder = get_mapping_folder(rig_type)

    json_presets = []
    files = os.listdir(mapping_folder)
    # get only json files
    for file in files:
        _, file_extension = os.path.splitext(file)
        if file_extension == ".json":
            json_presets.append(os.path.splitext(file)[0])

    items = []
    for i in json_presets:
        s = (i, i, "")
        items.append(s)

    return items


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


class MoveSDKPropertiesMapping(bpy.types.PropertyGroup):
    hips: bpy.props.StringProperty(name="Hips")  # type: ignore
    spine: bpy.props.StringProperty(name="Spine")  # type: ignore
    spine1: bpy.props.StringProperty(name="Spine1")  # type: ignore
    head: bpy.props.StringProperty(name="Head")  # type: ignore

    right_shoulder: bpy.props.StringProperty(name="RightShoulder")  # type: ignore
    right_arm: bpy.props.StringProperty(name="RightArm")  # type: ignore
    right_fore_arm: bpy.props.StringProperty(name="RightForeArm")  # type: ignore
    right_hand: bpy.props.StringProperty(name="RightHand")  # type: ignore

    left_shoulder: bpy.props.StringProperty(name="LeftShoulder")  # type: ignore
    left_arm: bpy.props.StringProperty(name="LeftArm")  # type: ignore
    left_fore_arm: bpy.props.StringProperty(name="LeftForeArm")  # type: ignore
    left_hand: bpy.props.StringProperty(name="LeftHand")  # type: ignore

    right_up_leg: bpy.props.StringProperty(name="RightUpLeg")  # type: ignore
    right_leg: bpy.props.StringProperty(name="RightLeg")  # type: ignore
    right_foot: bpy.props.StringProperty(name="RightFoot")  # type: ignore
    right_toe_base: bpy.props.StringProperty(name="RightToeBase")  # type: ignore

    left_up_leg: bpy.props.StringProperty(name="LeftUpLeg")  # type: ignore
    left_leg: bpy.props.StringProperty(name="LeftLeg")  # type: ignore
    left_foot: bpy.props.StringProperty(name="LeftFoot")  # type: ignore
    left_toe_base: bpy.props.StringProperty(name="LeftToeBase")  # type: ignore

    right_thumb_01: bpy.props.StringProperty(name="RightThumb1")  # type: ignore
    right_thumb_02: bpy.props.StringProperty(name="RightThumb2")  # type: ignore
    right_thumb_03: bpy.props.StringProperty(name="RightThumb3")  # type: ignore

    right_index_01: bpy.props.StringProperty(name="RightIndex1")  # type: ignore
    right_index_02: bpy.props.StringProperty(name="RightIndex2")  # type: ignore
    right_index_03: bpy.props.StringProperty(name="RightIndex3")  # type: ignore

    right_middle_01: bpy.props.StringProperty(name="RightMiddle1")  # type: ignore
    right_middle_02: bpy.props.StringProperty(name="RightMiddle2")  # type: ignore
    right_middle_03: bpy.props.StringProperty(name="RightMiddle3")  # type: ignore

    right_ring_01: bpy.props.StringProperty(name="RightRing1")  # type: ignore
    right_ring_02: bpy.props.StringProperty(name="RightRing2")  # type: ignore
    right_ring_03: bpy.props.StringProperty(name="RightRing3")  # type: ignore

    right_pinky_01: bpy.props.StringProperty(name="RightPinky1")  # type: ignore
    right_pinky_02: bpy.props.StringProperty(name="RightPinky2")  # type: ignore
    right_pinky_03: bpy.props.StringProperty(name="RightPinky3")  # type: ignore

    left_thumb_01: bpy.props.StringProperty(name="LeftThumb1")  # type: ignore
    left_thumb_02: bpy.props.StringProperty(name="LeftThumb2")  # type: ignore
    left_thumb_03: bpy.props.StringProperty(name="LeftThumb3")  # type: ignore

    left_index_01: bpy.props.StringProperty(name="LeftIndex1")  # type: ignore
    left_index_02: bpy.props.StringProperty(name="LeftIndex2")  # type: ignore
    left_index_03: bpy.props.StringProperty(name="LeftIndex3")  # type: ignore

    left_middle_01: bpy.props.StringProperty(name="LeftMiddle1")  # type: ignore
    left_middle_02: bpy.props.StringProperty(name="LeftMiddle2")  # type: ignore
    left_middle_03: bpy.props.StringProperty(name="LeftMiddle3")  # type: ignore

    left_ring_01: bpy.props.StringProperty(name="LeftRing1")  # type: ignore
    left_ring_02: bpy.props.StringProperty(name="LeftRing2")  # type: ignore
    left_ring_03: bpy.props.StringProperty(name="LeftRing3")  # type: ignore

    left_pinky_01: bpy.props.StringProperty(name="LeftPinky1")  # type: ignore
    left_pinky_02: bpy.props.StringProperty(name="LeftPinky2")  # type: ignore
    left_pinky_03: bpy.props.StringProperty(name="LeftPinky3")  # type: ignore


class MoveSDKPropertiesRetargetingEntity(bpy.types.PropertyGroup):
    rig: bpy.props.PointerProperty(type=bpy.types.Armature)  # type: ignore
    mapping: bpy.props.PointerProperty(type=MoveSDKPropertiesMapping)  # type: ignore

    hips_original_transforms: bpy.props.FloatVectorProperty(
        subtype="MATRIX", size=16, default=flatten_matrix(Matrix())
    )  # , default=Matrix())  # type: ignore

    def get_presets_items(self, context):
        if self == context.scene.move_sdk.retargeting.source:
            return my_settings_callback(self, context, "source")
        elif self == context.scene.move_sdk.retargeting.target:
            return my_settings_callback(self, context, "target")
        else:
            return []

    presets: bpy.props.EnumProperty(name="Presets", items=get_presets_items)  # type: ignore


class MoveSDKPropertiesRetargeting(bpy.types.PropertyGroup):
    source: bpy.props.PointerProperty(type=MoveSDKPropertiesRetargetingEntity)  # type: ignore
    target: bpy.props.PointerProperty(type=MoveSDKPropertiesRetargetingEntity)  # type: ignore


class MoveSDKPropertiesAppend(bpy.types.PropertyGroup):
    test_rig_path: bpy.props.StringProperty(
        name="Test rig path",
        description="Test rig path",
        default="",
        get=lambda self: str(Path(__file__).parent / "data" / "rigs" / "wingit_cat.blend"),
    )  # type: ignore

    test_scene_path: bpy.props.StringProperty(
        name="Test scene path",
        description="Test scene path",
        default="",
        get=lambda self: str(Path(__file__).parent / "data" / "scenes" / "wing_it_barn.blend"),
    )  # type: ignore

    filepath: bpy.props.StringProperty(
        name=".blend path",
        description=".blend path",
        default="",
        subtype="FILE_PATH",
    )  # type: ignore
    import_scene: bpy.props.BoolProperty(
        name="Import scene", description="Import scene settings", default=True
    )  # type: ignore
    import_world: bpy.props.BoolProperty(
        name="Import world", description="Import world settings", default=True
    )  # type: ignore


class MoveSDKProperties(bpy.types.PropertyGroup):
    general: bpy.props.PointerProperty(type=MoveSDKPropertiesGeneral)  # type: ignore
    retargeting: bpy.props.PointerProperty(type=MoveSDKPropertiesRetargeting)  # type: ignore
    append: bpy.props.PointerProperty(type=MoveSDKPropertiesAppend)  # type: ignore

    def register():
        bpy.types.Scene.move_sdk = bpy.props.PointerProperty(type=MoveSDKProperties)
