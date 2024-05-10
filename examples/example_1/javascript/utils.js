async function runQuery(query) {
  //HTTP posts GraphQL queries and mutations and returns the result
  //relies on MOVE_URL and MOVE_API_KEY being valid in the .env file
  //See graphql/index.js for queries and mutations
  console.log("Running query: ", query)
  const response = await fetch(process.env.MOVE_URL, {
    body: JSON.stringify({ query }),
    method: 'POST',
    headers: {
      Authorization: process.env.MOVE_API_KEY
    }
  })
  if (!response.ok) throw new Error('runQuery: Network response was not ok.')

  const result = await response.json()
  console.log("Query complete")
  return result

}

//Uses the presigned URL returned by the createFile mutation to upload a video file
async function uploadVideo(url, file) {
  //Take a url and file and upload them via PUT method
  //Used to push a video file to Move via the pre-signed URL returned by the createFile mutation.
  console.log("Beginning file upload...")
  const response = await fetch(url, {
    body: file,
    method: 'PUT'
  })
  if (!response.ok) throw new Error('uploadVideo: Network response was not ok.')
  console.log("File upload complete")
  return response.status === 200
}

//Use the getJob query to poll the job every 30 seconds to check if it completes
async function pollForJobResult(query, count) {
  try {
    const response = await runQuery(query)
    const data = await response.data
    console.log("Job state:", data.job.state)
    if (count === 20) {
      //timeout after 20 minutes
      console.log("Processing took too long, exiting. If it's a very large file, change the timeout in utils.js.")
      return true
    }
    if (data.job.state === "FINISHED") {
      console.log("JOB COMPLETE!", data.job.outputs)
      console.log("Time", (count * 30) + " seconds")
      return true
    }
    else if (data.job.state === "FAILED") {
      console.log("JOB FAILURE", data.job)
      return true
    }

    else {
      // If it doesn't match, wait 30 seconds and poll again
      console.log("Checking again in 30 seconds..." + ".".repeat(count))

      await new Promise(resolve => setTimeout(resolve, 30000))
      return pollForJobResult(query, count + 1)
    }
  } catch (error) {
    console.error('Failed to fetch:', error)
    return false
  }
}

module.exports = {
  runQuery,
  uploadVideo,
  pollForJobResult
}