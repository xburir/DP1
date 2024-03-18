const fs = require('fs');
const unzipper = require('unzipper');
const path = require('path');
const { exec } = require('child_process');
const { log } = require('console');
const { unzip } = require('zlib');

function handleUploadAndUnzip(file, baseFolder, username) {
  return new Promise((resolve, reject) => {
    // Create a directory for unzipping files if it doesn't exist
    
    const zipName = path.parse(file.originalname).name
    const uploadDir = path.join(baseFolder,"uploads",username)
    const unzipDir = path.join(baseFolder,"uploads",username,"unzipped",zipName) 

    if (!fs.existsSync(unzipDir)) {
      fs.mkdirSync(unzipDir, { recursive: true });
    }

    // Ensure upload directory exists
    if (!fs.existsSync(uploadDir)) {
        fs.mkdirSync(uploadDir, { recursive: true });
      }

    // Move the uploaded file to the upload directory
    const filePath = path.join(uploadDir, file.originalname);
    fs.rename(path.join(baseFolder,file.path),filePath, (err) => {
      if (err) {
        reject(err);
      } else {
        // Unzip the uploaded file
        fs.createReadStream(filePath)
        .pipe(unzipper.Extract({path: unzipDir}))
          .on('close', () => {
            const valhalla_container_name = 'valhalla'
            const pythonScript = 'map_match.py '+unzipDir+' '+valhalla_container_name+' '+username+' '+zipName;

            exec(`python3 ${pythonScript}`, (error, stdout, stderr) => {
                if (error) {
                  console.log("Error in python script: "+error)
                  reject(error);
                } else {
                  let json  = JSON.parse(stdout)
                  if (json.failed == 0){
                    fs.rmdirSync(path.join(uploadDir,file.originalname), { recursive: true }); // remove uploaded zip file
                    fs.rmdirSync(unzipDir, {recursive: true}); // remove unzipped files
                  }
                  resolve(stdout);
                }
              });

          })
          .on('error', (err) => {
            console.log("Error in unzipping zip: "+err)
            reject(err);
          });
      }
    });
  });
}

module.exports = {
  handleUploadAndUnzip
};