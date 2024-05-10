import bpy
import os
import requests
from move_ugc import MoveUgc
import subprocess
import sys


class MoveAPI:
    def __init__(self, api_key, endpoint_url=None):
        self.api_key = api_key
        if endpoint_url is None:
            endpoint_url = "https://api.move.ai/ugc/graphql"
        self.endpoint_url = endpoint_url
        self.client = MoveUgc(api_key=api_key, endpoint_url=endpoint_url)

    def create_files(self, video_path):
        video_file = self.client.files.create(file_type="mp4")

        with open(video_path, "rb") as f:
            requests.put(video_file.presigned_url, data=f.read())

        return video_file.id

    def create_take(self, video_file_id, metadata=None):
        if metadata is None:
            metadata = {"test": "test"}
        take = self.client.takes.create(
            video_file_id=video_file_id,
            metadata=metadata,
        )
        return take

    def get_take(self, take_id):
        take = self.client.takes.retrieve(id=take_id)
        return take

    def create_job(self, take_id):
        job = self.client.jobs.create(take_id=take_id, metadata={"test": "test_job"})
        return job

    def get_job(self, job_id, expand=False):
        # Get a job using the Move One Public API
        # Implement job retrieval logic using move_ugc_python SDK
        if expand is False:
            job = self.client.jobs.retrieve(id=job_id)
        else:
            job = self.client.jobs.retrieve(
                id=job_id, expand=["take", "outputs", "client"]
            )
        return job

    def download_outputs(self, job_id, output_dir, output_name):
        # make output dir if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # get job
        job = self.get_job(job_id, expand=True)
        # for each output download the file in the output_dir
        output_paths = []
        for output in job.outputs:
            output_file_name = f"{output_name}{output.file.type}"
            output_path = os.path.join(output_dir, output_file_name)
            with open(output_path, "wb") as f:
                response = requests.get(output.file.presigned_url)
                f.write(response.content)
            output_paths.append(output_path)
        return output_paths
