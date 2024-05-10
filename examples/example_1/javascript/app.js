// Load environment variables from the .env file.
require('dotenv').config()

// Import required modules
const fs = require('fs') // File system for reading files
const { createFileMutation, createTakeMutation, createJobMutation, getJobQuery } = require('./graphql') // Move API GraphQL mutations and queries
const { runQuery, uploadVideo, pollForJobResult } = require('./utils') // Utility functions for interacting with APIs

// Main function to upload a video file to the Move API and receive back links to Motion data
async function run() {
    
    // Create a new file reference using the file creation GraphQL mutation
    const fileReference = await runQuery(createFileMutation)

    // Read the video file from the filesystem
    const videoFile = fs.readFileSync("../../../videos/single-cam/single_1.mp4")

    // Upload the video file using the presigned URL obtained from the file creation mutation
    const videoFileUpload = await uploadVideo(fileReference.data.createFile.presignedUrl, videoFile)

    // Create a new 'take' using the take creation GraphQL mutation and the file ID
    const take = await runQuery(createTakeMutation(fileReference.data.createFile.id))

    // Create a new job using the job creation GraphQL mutation and the take ID
    const job = await runQuery(createJobMutation(take.data.take.id))

    // Query for the job status using the job's ID
    const getJob = await runQuery(getJobQuery(job.data.job.id))

    // Poll the job status until completion or failure
    const pollJob = await pollForJobResult(getJobQuery(getJob.data.job.id), 0)
}

// Execute the main function
run()
