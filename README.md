<p align="center">
  <a href="https://move.ai">
    <img src="/images/logo.jpeg" width="200px" alt="Move AI logo" />
  </a>
</p>

# Move AI Recipes
This repo provides examples, guides and tools for using the [Move AI API](https://developers.move.ai/docs/welcome) to 
access models developed by [Move AI](https://move.ai). To run these models, you will need a Move AI API key which you 
can request [here](https://www.move.ai/api).

The models generate spatial motion data related to humans (e.g. human motion and camera positions in different file 
formats) from 2D video input by using physics and AI based estimation techniques.

Most of the code examples are written in Python, although the concepts can be applied in any language.

<p align="center">
  <a href="https://move.ai">
    <img src="/images/breakdance.gif" width="300px" alt="Move AI logo" />
  </a>
</p>

## User examples
[Video game development by Electronic Arts](https://www.youtube.com/watch?v=z0aNKvZR8Tk&t=139s).
<p align="left">
  <a href="https://www.youtube.com/watch?v=z0aNKvZR8Tk&t=139s">
    <img src="/images/ea.png" width="400px" alt="Move AI logo" />
  </a>
</p>

[Music video for MGMT's “Mother Nature” by Eye Garden](https://www.youtube.com/watch?v=sDzIO5ahGE8).
<p align="left">
  <a href="https://www.youtube.com/watch?v=sDzIO5ahGE8">
    <img src="/images/mgmt.png" width="400px" alt="MGMT music video" />
  </a>
</p>

## Models
### Overview
| Model                                                                                                                | Description                                                                                   |
|----------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| single-cam                                                                                                           | Generates spatial motion data using a single video as input, optimised for quality.           |
| single-cam-fast <br/>(coming soon)                                                                                   | Generates spatial motion data using a single video as input, optimised for speed and quality. |
| multi-cam <br/>(coming soon)                                                                                         | Generates spatial motion data using multiple videos as input, optimised for quality.          |
| multi-cam-rt <br/>([available now, request access here](https://share-eu1.hsforms.com/1J1WzWmHUT_aXIlmv7-b3xwfk5ge)) | Generates spatial motion data using multiple videos as input, optimised for real-time speed.  |

### Single-Camera
Features:
* Full body tracking
* Hand and finger tracking
* FBX, USD output formats
* Track up to 3 people (coming soon)
* Supports video from any camera but video from known cameras give the best results

[FAQs](./FAQs.md)

### Multi-Camera (coming soon)
Features:
* Full body tracking
* Hand and finger tracking
* Track up to TK people
* Track volumes of 100m x 50m
* FBX, USD output formats
* Supports up to TK cameras
* Tracks large spherical objects (e.g. basketballs, volleyballs)
* Supports video from any camera but video from known cameras give the best results

## Code examples
### Python
#### Example 1: Generate a 3D animation file of a single person from a single camera from an unknown camera
#### Example 2: Generate a 3D animation file of a single person from a single camera from an iPhone 13
#### Example 3: Convert a 3D animation file to CSV
#### Example 4: Visualise foot step detection and ground reaction forces from a 3D animation file
#### Example 5: Estimate bone lengths from a 3D animation file
#### Example 6: Retarget animation to a character and render the result in a different environment

### JavaScript
#### Example 1: Generate a 3D animation file of a single person from a single camera from an unknown camera
