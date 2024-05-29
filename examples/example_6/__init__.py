# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Move SDK",
    "author": "Denis Cera",
    "description": "Move.ai SDK",
    "blender": (4, 1, 0),
    "version": (1, 0, 0),
    "location": "",
    "warning": "",
    "category": "Generic",
}

import sys
import subprocess
import site
from pathlib import Path


def check_pip_dependencies(dependencies_to_check: list):
    sitepackages = Path(site.getsitepackages()[0])
    sitepackages_names = [package.stem for package in sitepackages.glob("*")]
    uninstalled_dependencies = [
        dependency_to_check[1]
        for dependency_to_check in dependencies_to_check
        if dependency_to_check[0] not in sitepackages_names
    ]
    return uninstalled_dependencies


def install_pip_dependencies(dependencies_to_install: list):
    if not dependencies_to_install:
        return
    print("Installing dependencies:", dependencies_to_install)
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", *dependencies_to_install],
        capture_output=True,
    )
    return result.returncode == 0


dependencies = [("move_ugc", "move-ugc-python")]
uninstalled_dependencies = check_pip_dependencies(dependencies)
install_pip_dependencies(uninstalled_dependencies)

import bpy  # noqa: E402
from .ui import (  # noqa: E402
    MOVE_SDK_PT_general_panel,
    MOVE_SDK_PT_retargeting_panel,
    MOVE_SDK_PT_retargeting_source_panel,
    MOVE_SDK_PT_retargeting_target_panel,
    MOVE_SDK_PT_retargeting_source_mapping_panel,
    MOVE_SDK_PT_retargeting_target_mapping_panel,
    MOVE_SDK_PT_retargeting_source_presets_panel,
    MOVE_SDK_PT_retargeting_target_presets_panel,
    MOVE_SDK_PT_scene_panel,
    MOVE_SDK_PT_test_files_panel,
    MOVE_SDK_PT_ffmpeg_presets,
    MOVE_SDK_PT_output,
    MOVE_SDK_PT_output_views,
    MOVE_SDK_PT_output_color_management,
    MOVE_SDK_PT_encoding,
    MOVE_SDK_PT_encoding_video,
    MOVE_SDK_PT_encoding_audio,
    MOVE_SDK_UL_renderviews,

)  # noqa: E402
from .operators import (  # noqa: E402
    MOVE_SDK_OT_run,
    MOVE_SDK_OT_retarget,
    MOVE_SDK_OT_retargeting_clear,
    MOVE_SDK_OT_retargeting_create_preset,
    MOVE_SDK_OT_retargeting_save_preset,
    MOVE_SDK_OT_retargeting_load_preset,
    MOVE_SDK_OT_retargeting_delete_preset,
    MOVE_SDK_OT_retargeting_rename_preset,
    MOVE_SDK_OT_append_file
)  # noqa: E402
from .properties import (  # noqa: E402
    MoveSDKPropertiesGeneral,
    MoveSDKPropertiesMapping,
    MoveSDKPropertiesRetargetingEntity,
    MoveSDKPropertiesRetargeting,
    MoveSDKPropertiesAppend,
    MoveSDKProperties,
)  # noqa: E402


classes = (
    MOVE_SDK_PT_general_panel,
    MOVE_SDK_PT_retargeting_panel,
    MOVE_SDK_PT_retargeting_source_panel,
    MOVE_SDK_PT_retargeting_target_panel,
    MOVE_SDK_PT_retargeting_source_mapping_panel,
    MOVE_SDK_PT_retargeting_target_mapping_panel,
    MOVE_SDK_PT_retargeting_source_presets_panel,
    MOVE_SDK_PT_retargeting_target_presets_panel,
    MOVE_SDK_PT_scene_panel,
    MOVE_SDK_PT_test_files_panel,
    MOVE_SDK_PT_ffmpeg_presets,
    MOVE_SDK_PT_output,
    MOVE_SDK_PT_output_views,
    MOVE_SDK_PT_output_color_management,
    MOVE_SDK_PT_encoding,
    MOVE_SDK_PT_encoding_video,
    MOVE_SDK_PT_encoding_audio,
    MOVE_SDK_UL_renderviews,
    MOVE_SDK_OT_run,
    MOVE_SDK_OT_retarget,
    MOVE_SDK_OT_retargeting_clear,
    MOVE_SDK_OT_retargeting_create_preset,
    MOVE_SDK_OT_retargeting_save_preset,
    MOVE_SDK_OT_retargeting_load_preset,
    MOVE_SDK_OT_retargeting_delete_preset,
    MOVE_SDK_OT_retargeting_rename_preset,
    MOVE_SDK_OT_append_file,
    MoveSDKPropertiesGeneral,
    MoveSDKPropertiesMapping,
    MoveSDKPropertiesRetargetingEntity,
    MoveSDKPropertiesRetargeting,
    MoveSDKPropertiesAppend,
    MoveSDKProperties,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
