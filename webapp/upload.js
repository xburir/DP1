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
          .pipe(unzipper.Parse())
          .on('entry', (entry) => {
            const entryPath = path.join(unzipDir, entry.path);
            if (entry.type === 'Directory') {
              // Create directory if it doesn't exist
              if (!fs.existsSync(entryPath)) {
                fs.mkdirSync(entryPath, { recursive: true });
              }
            } else {
              entry.pipe(fs.createWriteStream(entryPath));
            }
          })
          .on('close', () => {

            const valhalla_container_name = 'valhalla'
            const pythonScript = 'map_match.py '+unzipDir+' '+valhalla_container_name+' '+user+' '+zipName;

            exec(`python3 ${pythonScript}`, (error, stdout, stderr) => {
                if (error) {
                  fs.rmdirSync(uploadDir, { recursive: true }); // remove uploaded zip file
                  fs.rmdirSync(unzipDir, {recursive: true}); // remove unzipped files
                  reject(error);
                } else {
                  console.log(stdout);

                  fs.rmdirSync(uploadDir, { recursive: true }); // remove uploaded zip file
                  fs.rmdirSync(unzipDir, {recursive: true}); // remove unzipped files

                  resolve(`File ${zipName} uploaded and map-matched succesfully, please refresh the site to see the new file.`);
                }
              });

          })
          .on('error', (err) => {
            fs.rmdirSync(uploadDir, { recursive: true }); // remove uploaded zip file
            fs.rmdirSync(unzipDir, {recursive: true}); // remove unzipped files
            reject(err);
          });
      }
    });
  });
}

module.exports = {
  handleUploadAndUnzip
};