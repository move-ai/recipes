import bpy
import time
from datetime import datetime
from bpy.types import Operator
from .utils import MoveAPI
import os


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
