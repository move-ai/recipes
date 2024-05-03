# Example 1: Generate 3D animation data of a single person from a single video from an unknown camera
## Setup
* Rename .env.example to .env and add your API key 
* Install the Dotenv module (`npm install dotenv`)
* Download the [example input video](https://move-ai-recipes.nyc3.cdn.digitaloceanspaces.com/single_1.mp4), or add your own, to 'recipes/videos/single-cam/single_1.mp4'

## Run
In the terminal inside the project folder type: `node app`

Once complete, presigned URLs will be generated
for the following files:
* .blend
* .fbx
* .mp4
* .usdc
* .usdz

## How it works
The demo carries out the following steps using the Move GraphQL API:
1. Requests a presigned URL and file ID from the Move API in order to upload a video file.
2. Uploads example.mp4 to the presigned URL.
3. Uses the file ID returned in step 1 to create a Take.
4. Uses the take ID returned in step 3 to create a Job.
5. Jobs are long running processes so the code contains a polling function that will check the state of the Job every 30
seconds and return the motion output files (including preview mp4 files) as new presigned URLs.
