const fs = require('fs');
const unzipper = require('unzipper');
const path = require('path');
const { exec } = require('child_process');

function handleUploadAndUnzip(file, uploadDir, unzipDir, user, zipName) {
  return new Promise((resolve, reject) => {
    // Create a directory for unzipping files if it doesn't exist
    if (!fs.existsSync(unzipDir)) {
      fs.mkdirSync(unzipDir, { recursive: true });
    }

    // Ensure upload directory exists
    if (!fs.existsSync(uploadDir)) {
        fs.mkdirSync(uploadDir, { recursive: true });
      }

    // Move the uploaded file to the upload directory
    const filePath = path.join(uploadDir, file.originalname);
    fs.rename("/DP1/webapp/"+file.path,filePath, (err) => {
      if (err) {
        reject(err);
      } else {
        // Unzip the uploaded file
        fs.createReadStream(filePath)
          .pipe(unzipper.Extract({ path: unzipDir }))
          .on('close', () => {

            fs.rmdirSync(uploadDir, { recursive: true });

            const valhalla_container_name = 'valhalla'
            const pythonScript = 'map_match.py '+unzipDir+' '+valhalla_container_name+' '+'csv'+' '+user+' '+zipName;

            exec(`python3 ${pythonScript}`, (error, stdout, stderr) => {
                if (error) {
                  reject(error);
                } else {
                  console.log(stdout);
                  resolve(stdout);
                }
              });

          })
          .on('error', (err) => {
            reject(err);
          });
      }
    });
  });
}

module.exports = {
  handleUploadAndUnzip
};