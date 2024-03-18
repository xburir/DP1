// app.js
const express = require('express');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const mysql = require('mysql');
const path = require("path")
const session = require('express-session');
const app = express();
const multer = require('multer');
const fileHandler = require('./upload');
const socketIo = require('socket.io');
const http = require('http');
const fs = require('fs');
const { exec } = require('child_process');

app.use(express.static(path.resolve("")))

const server = http.createServer(app);
const io = socketIo(server);
const PORT = process.env.PORT || 8090;

// Set the views directory to 'public'
app.set('views', path.join(__dirname, 'public'));

// Set the view engine to use EJS
app.set('view engine', 'ejs');

app.use('/socket.io', express.static(path.join(__dirname, 'node_modules/socket.io/client-dist')));

// Parse URL-encoded bodies (as sent by HTML forms)
app.use(express.urlencoded({ extended: true }));

// Sessions settings
app.use(session({
  secret: 'secret-key',
  resave: false,
  saveUninitialized: false,
}));

// Middleware to parse JSON bodies
app.use(bodyParser.json());

connectionOptions = {
  host: 'localhost',
  user: 'root',
  password: 'root',
  database: 'dp_webserver'
};

// Create a MySQL connection
let connection;

function connectToDatabase() {
  connection = mysql.createConnection(connectionOptions);

  // Connect to MySQL
  connection.connect((err) => {
    if (err) {
      if (err.code == 'ECONNREFUSED') {
        console.error('Error connecting to MySQL database: Connection refused.');
      } else {
        console.error('Error connecting to MySQL database: ', err.code);
      }
      setTimeout(connectToDatabase, 5000);
    } else {
      console.log('Connected to MySQL database');
    }
  });

  connection.on('error', (err) => {
    if (err.code === 'PROTOCOL_CONNECTION_LOST') {
      console.error('Database connection lost');
      connectToDatabase(); // Reconnect if connection is lost
    } else {
      console.error('Database error: ', err);
      throw err;
    }
  })
}

connectToDatabase();

// Route to handle user registration
app.post('/register', async (req, res) => {
  const { username, password } = req.body;
  try {
    const hashedPassword = bcrypt.hashSync(password, 10);
    const sql = 'INSERT INTO users (username, password) VALUES (?, ?)';
    connection.query(sql, [username, hashedPassword], (err, result) => {
      if (err) {
        console.error('Error registering user:', err.code);
        res.status(200).send(err.code);
        return;
      }
      res.status(200).send("SUCCESS")
    });
  } catch (err) {
    console.error('Error registering user:', err.code);
    res.status(400).send(err.code);
  }
});

app.post('/logout', (req, res) => {
  req.session.username = null
  res.redirect('/login');
});

// Route to handle login
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  const sql = 'SELECT * FROM users WHERE username = ?';
  connection.query(sql, [username], async (err, results) => {
    if (err) {
      console.error('Error fetching user:', err.code);
      res.status(500).send(err.code);
      return;
    }
    if (results.length === 0) {
      res.status(401).send('Invalid username or password');
      return;
    }
    const user = results[0];
    if (await bcrypt.compareSync(password, user.password)) {
      req.session.username = username
      res.status(200).send('SUCCESS');
    } else {
      res.status(401).send('Invalid username or password');

    }
  });
});

app.get('/login', (req, res) => {
  if (req.session.username != null) {
    res.redirect("/")
    return
  }
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.get('/register', (req, res) => {
  if (req.session.username != null) {
    res.redirect("/")
    return
  }
  res.sendFile(path.join(__dirname, 'public', 'register.html'));
});


app.get('/about', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'about.html'));
});



app.get('/', (req, res) => {
  if (req.session.username == null) {
    res.redirect("/login")
    return
  }

  res.render('index.ejs', { username: req.session.username });
});

app.get('/list-routes', (req, res) => {
  if (req.session.username == null) {
    res.redirect("/login")
    return
  }

  if (!fs.existsSync(path.join(__dirname, "/routes/", req.session.username))) {
    fs.mkdirSync(path.join(__dirname, "/routes/", req.session.username), { recursive: true });
  }

  fs.readdir(path.join(__dirname, "/routes/", req.session.username), { withFileTypes: true }, (err, files) => {
    if (err) {
      console.error('Error reading directory:', err);
      res.status(500).json({ error: 'Internal server error' });
      return;
    }
    const fileDetails = files.map(file => {
      const filePath = path.join(__dirname, "/routes/", req.session.username, file.name);
      const stats = fs.statSync(filePath); // Get file stats synchronously
      return {
        name: file.name,
        path: path.join(__dirname, "/routes/", req.session.username, file.name),
        lastModified: stats.mtime
      }
    }
    );
    res.json({ files: fileDetails });
  });
});


const upload = multer({ dest: 'uploads/' });

// Route for handling file upload
app.post('/upload', upload.single('file'), async (req, res) => {
  if (req.session.username == null) {
    res.redirect("/login")
    return
  }
  try {
    if (!req.file) {
      return res.status(400).send('No files were uploaded.');
    }
    res.redirect('/');

    const message = await fileHandler.handleUploadAndUnzip(req.file, __dirname, req.session.username);
    console.log(message)

    io.to(req.session.username).emit('processing_complete', message);

  } catch (error) {
    console.error('Error handling upload and unzip:', error);
    io.to(req.session.username).emit('processing_complete', "ERROR; Error in upload or in zip: " + error);
  }
});

app.get('/list-uploads', (req, res) => {
  if (req.session.username == null) {
    res.redirect("/login")
    return
  }

  if (!fs.existsSync(path.join(__dirname, "/uploads/", req.session.username))) {
    fs.mkdirSync(path.join(__dirname, "/uploads/", req.session.username), { recursive: true });
  }

  fs.readdir(path.join(__dirname, "/uploads/", req.session.username), { withFileTypes: true }, (err, files) => {
    if (err) {
      console.error('Error reading directory:', err);
      res.status(500).json({ error: 'Internal server error' });
      return;
    }
    const fileDetails = files.filter(file => file.isFile()).map(file => ({
      name: file.name,
      path: path.join(__dirname, "/uploads/", req.session.username, file.name)
    }));
    res.json({ files: fileDetails });
  });
});

app.get('/list-unzipped', (req, res) => {
  if (req.session.username == null) {
    res.redirect("/login")
    return
  }

  if (!fs.existsSync(path.join(__dirname, "/uploads/", req.session.username, "unzipped"))) {
    fs.mkdirSync(path.join(__dirname, "/uploads/", req.session.username, "unzipped"), { recursive: true });
  }

  fs.readdir(path.join(__dirname, "/uploads/", req.session.username, "unzipped"), { withFileTypes: true }, (err, files) => {
    if (err) {
      console.error('Error reading directory:', err);
      res.status(500).json({ error: 'Internal server error' });
      return;
    }
    const fileDetails = files.map(file => ({
      name: file.name,
      path: path.join(__dirname, "/uploads/", req.session.username, "unzipped", file.name)
    }));
    res.json({ files: fileDetails });
  });
});

app.get('/mapmatch/:user/:directory', (req, res) => {

  const directory = req.params.directory;
  const name = req.params.user
  const valhalla_container_name = 'valhalla'
  const zipName = path.parse(directory).name
  const dirPath = __dirname + "/uploads/" + name + "/unzipped/" + directory

  const pythonScript = 'map_match.py ' + dirPath + ' ' + valhalla_container_name + ' ' + name + ' ' + zipName;
  exec(`python3 ${pythonScript}`, (error, stdout, stderr) => {
    if (error) {
      console.log("Error in python script: " + error)
      io.to(req.session.username).emit('processing_complete', error);
      res.status(500).send('Error in processing ' + error);
    } else {
      io.to(req.session.username).emit('processing_complete', stdout);
      res.status(200).send('Processing complete ' + stdout);
    }
  });
});

app.get('/delete/*', (req, res) => {
  if (req.session.username == null) {
    res.redirect("/login")
    return
  }

  const filePath = req.params[0];
  reqUser = filePath.split("/")[1]

  if (reqUser != req.session.username) {
    io.to(req.session.username).emit('message', "You are not allowed to delete others files");
    res.status(400).send('Not allowed');
    return
  }

  fs.stat(filePath, (err, stats) => {
    if (err) {
      io.to(req.session.username).emit('message', 'Error accessing file stats:' + err);
      console.error('Error accessing file stats:', err);
      res.status(500).send('Error accessing file stats:', err);
      return;
    }

    if (stats.isFile()) {
      // If it's a file, remove it
      fs.unlink(filePath, (unlinkErr) => {
        if (unlinkErr) {
          io.to(req.session.username).emit('message', "Delete error.");
          res.status(500).send("Delete error. " + unlinkErr);
        } else {
          io.to(req.session.username).emit('message', "Delete successful.");
          res.status(200).send("Delete successful.");
        }
      });
    } else if (stats.isDirectory()) {
      // If it's a directory, remove it recursively
      fs.rmdir(filePath, { recursive: true }, (rmdirErr) => {
        if (rmdirErr) {
          io.to(req.session.username).emit('message', "Delete error.");
          res.status(500).send("Delete error. " + rmdirErr);
        } else {
          io.to(req.session.username).emit('message', "Delete successful.");
          res.status(200).send("Delete successful.");
        }
      });
    } else {
      console.error('Invalid path:', filePath);
      res.status(500).send("Invalid path.");
    }
  });



})


app.get('/warn/*', (req, res) => {
  if (req.session.username == null) {
    res.redirect("/login")
    return
  }
  const filePath = req.params[0];
  const user = filePath.split("/")[0]
  const file = filePath.split("/")[1]

  const sql = 'INSERT INTO bad_mapmatches (username, zipname) VALUES (?, ?)';
  connection.query(sql, [user, file], (err, result) => {
    if (err) {
      console.error('Error while logging warning for bad map-match:', err.code);
      io.to(req.session.username).emit('message', "Error while logging warning for bad map-match");
      res.status(500).send('Error while logging warning for bad map-match');
      return;
    }
    io.to(req.session.username).emit('message', "Warning logged successfully.");
    res.status(200).send('Warning logged successfully.');
  });

})

// Object to map each user to their corresponding socket ID
const userSockets = {};

// Socket.io connection
io.on('connection', (socket) => {

  // Associate each socket connection with a user
  socket.on('set_username', (username) => {
    userSockets[username] = socket.id;
    socket.join(username);
  });

  // Handle disconnection
  socket.on('disconnect', () => {
    // Remove the user's entry from the mapping when they disconnect
    Object.keys(userSockets).forEach((key) => {
      if (userSockets[key] === socket.id) {
        socket.leave(userSockets[key]);
        delete userSockets[key];
      }
    });
  });
});

// Serve static files from the public directory
app.use(express.static('public'));

// Start the server
server.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

process.on('uncaughtException', (err) => {
  if (err.code == 'PROTOCOL_CONNECTION_LOST') {
    console.error("Connection to database lost")
  } else {
    console.log("Uncaught exception: ", err);
  }
})