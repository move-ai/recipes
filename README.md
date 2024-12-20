<p align="center">
  <a href="https://move.ai">
    <img src="images/logo.jpeg" width="200px" alt="Move AI logo" />
  </a>
</p>

# Move AI Recipes
This repo provides examples, guides and tools for using the Move API to 
access models developed by [Move AI](https://move.ai). To run these models, sign up to the Team plan [here](https://platform.move.ai).

The models generate spatial motion data related to humans (e.g. human motion and camera positions in different file 
formats) from 2D video input by using physics and AI based estimation techniques.

Most of the code examples are written in Python, although the concepts can be applied in any language.

Some examples live in their own repos and are included here as submodules.

So if you want to get all the examples, make sure to clone the repo recursively (GitHub .zip download will not include the submodules):

`git clone --recurse-submodules --remote-submodules git@github.com:move-ai/recipes.git`

## User examples

| [<img src="images/ea.png" width="400px" alt="Move AI logo">](https://www.youtube.com/watch?v=z0aNKvZR8Tk&t=139s) | [<img src="images/mgmt.png" width="400px" alt="MGMT music video">](https://www.youtube.com/watch?v=sDzIO5ahGE8) |
|:--:|:--:|
| Video game development by Electronic Arts | Music video for MGMT's “Mother Nature” by Eye Garden |

## Models
### Overview
| Model                                                                                                               | Description                                                                                   | Inference time                        |
|---------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|---------------------------------------|
| singlecam                                                                                                           | Generates spatial motion data using a single video as input, optimised for quality.           | 25-30s for 10s, 60fps, HD             |
| singlecam-turbo <br/>(coming soon)                                                                                  | Generates spatial motion data using a single video as input, optimised for speed and quality. | 10s for 10s, 60fps, HD                |
| multicam                                                                                          | Generates spatial motion data using multiple videos as input, optimised for quality.          | 2.5mins for 10s, 60fps, HD, 4 cameras |
| multicam-rt <br/>([available now, request access here](https://share-eu1.hsforms.com/1J1WzWmHUT_aXIlmv7-b3xwfk5ge)) | Generates spatial motion data using multiple videos as input, optimised for real-time speed.  | <120ms latency                        |

### singlecam

* Full body tracking
* Hand and finger tracking
* FBX, USD and Blend 3D output formats
* Supports any video but best results are obtained when the camera is known

  This model powers the [Move One iPhone app](https://apps.apple.com/us/app/move-one/id6448635527)

### multicam

* Full body tracking
* Hand and finger tracking
* Camera calibration output (coming soon)
* FBX, USD and Blend 3D output formats
* Track up to 5 people

  This model currently only supports cameras listed [here](https://move-ai.github.io/move-ugc-api/getting-started/multicam/lenses/)

## Code examples

<table>
  <tr>
    <th>Link</th>
    <th>Language</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><a href="examples/Move_API_single_person_single_video_unknown_camera.ipynb">Move_API_single_person_single_video_unknown_camera.ipynb</a></td>
    <td>Python</td>
    <td>Generate 3D animation data of a single person from a single video from an unknown camera</td>
  </tr>
  <tr>
    <td><a href="examples/Move_API_single_person_multiple_video_go_pro.ipynb">Move_API_single_person_multiple_video_go_pro.ipynb</a></td>
    <td>Python</td>
    <td>Generate 3D animation data of a single person from multiple videos from a gopro</td>
  </tr>
  <tr>
    <td><a href="https://github.com/move-ai/Move_API_JavaScript_demo">Move_API_JavaScript_demo</a></td>
    <td>JavaScript</td>
    <td>Generate 3D animation data of a single person from a single video from an unknown camera</td>
  </tr>
  <tr>
    <td><a href="https://github.com/move-ai/Move_API_and_retargeting_Blender_addon">Move_API_and_retargeting_Blender_addon</a></td>
    <td>Blender Python API</td>
    <td>Move.ai API integrated into Blender via an add-on. Additional features: retargeting, scene import, rendering</td>
  </tr>
  <tr>
    <td><a href="examples/Move_API_ JSON_motion_data_sample_overview.ipynb">Move_API_JSON_motion_data_sample_overview.ipynb</a></td>
    <td>Python</td>
    <td>Explore and analyse the .JSON motion data output</td>
  </tr>
  <tr>
    <td><a href="https://github.com/move-ai/MoveSingleAPISwift">MoveSingleAPISwift</a></td>
    <td>Swift</td>
    <td>Swift SDK</td>
  </tr>
</table>
