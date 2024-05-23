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
    hips: bpy.props.StringProperty(name="Hips", default="_1:Hips")  # type: ignore
    spine: bpy.props.StringProperty(name="Spine", default="_1:Spine")  # type: ignore
    spine1: bpy.props.StringProperty(name="Spine1", default="_1:Spine1")  # type: ignore
    head: bpy.props.StringProperty(name="Head", default="_1:Head")  # type: ignore

    right_shoulder: bpy.props.StringProperty(
        name="RightShoulder", default="_1:RightShoulder"
    )  # type: ignore
    right_arm: bpy.props.StringProperty(name="RightArm", default="_1:RightArm")  # type: ignore
    right_fore_arm: bpy.props.StringProperty(
        name="RightForeArm", default="_1:RightForeArm"
    )  # type: ignore
    right_hand: bpy.props.StringProperty(name="RightHand", default="_1:RightHand")  # type: ignore

    left_shoulder: bpy.props.StringProperty(
        name="LeftShoulder", default="_1:LeftShoulder"
    )  # type: ignore
    left_arm: bpy.props.StringProperty(name="LeftArm", default="_1:LeftArm")  # type: ignore
    left_fore_arm: bpy.props.StringProperty(
        name="LeftForeArm", default="_1:LeftForeArm"
    )  # type: ignore
    left_hand: bpy.props.StringProperty(name="LeftHand", default="_1:LeftHand")  # type: ignore

    right_up_leg: bpy.props.StringProperty(name="RightUpLeg", default="_1:RightUpLeg")  # type: ignore
    right_leg: bpy.props.StringProperty(name="RightLeg", default="_1:RightLeg")  # type: ignore
    right_foot: bpy.props.StringProperty(name="RightFoot", default="_1:RightFoot")  # type: ignore
    right_toe_base: bpy.props.StringProperty(
        name="RightToeBase", default="_1:RightToeBase"
    )  # type: ignore

    left_up_leg: bpy.props.StringProperty(name="LeftUpLeg", default="_1:LeftUpLeg")  # type: ignore
    left_leg: bpy.props.StringProperty(name="LeftLeg", default="_1:LeftLeg")  # type: ignore
    left_foot: bpy.props.StringProperty(name="LeftFoot", default="_1:LeftFoot")  # type: ignore
    left_toe_base: bpy.props.StringProperty(
        name="LeftToeBase", default="_1:LeftToeBase"
    )  # type: ignore

    right_thumb_01: bpy.props.StringProperty(
        name="RightThumb1", default="_1:RightHandThumb1"
    )  # type: ignore
    right_thumb_02: bpy.props.StringProperty(
        name="RightThumb2", default="_1:RightHandThumb2"
    )  # type: ignore
    right_thumb_03: bpy.props.StringProperty(
        name="RightThumb3", default="_1:RightHandThumb3"
    )  # type: ignore

    right_index_01: bpy.props.StringProperty(
        name="RightIndex1", default="_1:RightHandIndex1"
    )  # type: ignore
    right_index_02: bpy.props.StringProperty(
        name="RightIndex2", default="_1:RightHandIndex2"
    )  # type: ignore
    right_index_03: bpy.props.StringProperty(
        name="RightIndex3", default="_1:RightHandIndex3"
    )  # type: ignore

    right_middle_01: bpy.props.StringProperty(
        name="RightMiddle1", default="_1:RightHandMiddle1"
    )  # type: ignore
    right_middle_02: bpy.props.StringProperty(
        name="RightMiddle2", default="_1:RightHandMiddle2"
    )  # type: ignore
    right_middle_03: bpy.props.StringProperty(
        name="RightMiddle3", default="_1:RightHandMiddle3"
    )  # type: ignore

    right_ring_01: bpy.props.StringProperty(
        name="RightRing1", default="_1:RightHandRing1"
    )  # type: ignore
    right_ring_02: bpy.props.StringProperty(
        name="RightRing2", default="_1:RightHandRing2"
    )  # type: ignore
    right_ring_03: bpy.props.StringProperty(
        name="RightRing3", default="_1:RightHandRing3"
    )  # type: ignore

    right_pinky_01: bpy.props.StringProperty(
        name="RightPinky1", default="_1:RightHandPinky1"
    )  # type: ignore
    right_pinky_02: bpy.props.StringProperty(
        name="RightPinky2", default="_1:RightHandPinky2"
    )  # type: ignore
    right_pinky_03: bpy.props.StringProperty(
        name="RightPinky3", default="_1:RightHandPinky3"
    )  # type: ignore

    left_thumb_01: bpy.props.StringProperty(
        name="LeftThumb1", default="_1:LeftHandThumb1"
    )  # type: ignore
    left_thumb_02: bpy.props.StringProperty(
        name="LeftThumb2", default="_1:LeftHandThumb2"
    )  # type: ignore
    left_thumb_03: bpy.props.StringProperty(
        name="LeftThumb3", default="_1:LeftHandThumb3"
    )  # type: ignore

    left_index_01: bpy.props.StringProperty(
        name="LeftIndex1", default="_1:LeftHandIndex1"
    )  # type: ignore
    left_index_02: bpy.props.StringProperty(
        name="LeftIndex2", default="_1:LeftHandIndex2"
    )  # type: ignore
    left_index_03: bpy.props.StringProperty(
        name="LeftIndex3", default="_1:LeftHandIndex3"
    )  # type: ignore

    left_middle_01: bpy.props.StringProperty(
        name="LeftMiddle1", default="_1:LeftHandMiddle1"
    )  # type: ignore
    left_middle_02: bpy.props.StringProperty(
        name="LeftMiddle2", default="_1:LeftHandMiddle2"
    )  # type: ignore
    left_middle_03: bpy.props.StringProperty(
        name="LeftMiddle3", default="_1:LeftHandMiddle3"
    )  # type: ignore

    left_ring_01: bpy.props.StringProperty(name="LeftRing1", default="_1:LeftHandRing1")  # type: ignore
    left_ring_02: bpy.props.StringProperty(name="LeftRing2", default="_1:LeftHandRing2")  # type: ignore
    left_ring_03: bpy.props.StringProperty(name="LeftRing3", default="_1:LeftHandRing3")  # type: ignore

    left_pinky_01: bpy.props.StringProperty(
        name="LeftPinky1", default="_1:LeftHandPinky1"
    )  # type: ignore
    left_pinky_02: bpy.props.StringProperty(
        name="LeftPinky2", default="_1:LeftHandPinky2"
    )  # type: ignore
    left_pinky_03: bpy.props.StringProperty(
        name="LeftPinky3", default="_1:LeftHandPinky3"
    )  # type: ignore

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

    presets: bpy.props.EnumProperty(
        name="Presets",
        items=get_presets_items
    )  # type: ignore




class MoveSDKPropertiesRetargeting(bpy.types.PropertyGroup):
    source: bpy.props.PointerProperty(type=MoveSDKPropertiesRetargetingEntity)  # type: ignore
    target: bpy.props.PointerProperty(type=MoveSDKPropertiesRetargetingEntity)  # type: ignore


class MoveSDKProperties(bpy.types.PropertyGroup):
    general: bpy.props.PointerProperty(type=MoveSDKPropertiesGeneral)  # type: ignore
    retargeting: bpy.props.PointerProperty(type=MoveSDKPropertiesRetargeting)  # type: ignore

    def register():
        bpy.types.Scene.move_sdk = bpy.props.PointerProperty(type=MoveSDKProperties)
