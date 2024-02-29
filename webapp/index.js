// app.js
const express = require('express');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const mysql = require('mysql');
const path=require("path")
const session = require('express-session');
const app = express();
const multer = require('multer');
const fileHandler = require('./upload');
const socketIo = require('socket.io');
const http = require('http');
const fs = require('fs');

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

// Create a MySQL connection
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'root',
  database: 'dp_webserver'
});

// Connect to MySQL
connection.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL database:', err);
    return;
  }
  console.log('Connected to MySQL database');
});

// Route to handle user registration
app.post('/register',async (req, res) => {
  const { username, password } = req.body;
  try {
    const hashedPassword = bcrypt.hashSync(password, 10);
    const sql = 'INSERT INTO users (username, password) VALUES (?, ?)';
    connection.query(sql, [username, hashedPassword], (err, result) => {
      if (err) {
        console.error('Error registering user:', err);
        res.status(400).send('Registration failed');
        return;
      }
      res.redirect('/login');
    });
  } catch (err) {
    console.error('Error registering user:', err);
    res.status(400).send('Registration failed');
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
      console.error('Error fetching user:', err);
      res.status(500).send('Login failed');
      return;
    }
    if (results.length === 0) {
      res.status(401).send('Invalid username or password');
      return;
    }
    const user = results[0];
    if (await bcrypt.compareSync(password, user.password)) {
      req.session.username = username
      res.redirect("/")
    } else {
      res.status(401).send('Invalid username or password');
    }
  });
});

app.get('/login', (req, res) => {
  if (req.session.username != null){
    res.redirect("/")
    return
  }
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
  });

app.get('/register', (req, res) => {
  if (req.session.username != null){
    res.redirect("/")
    return
  }
  res.sendFile(path.join(__dirname, 'public', 'register.html'));
});


app.get('/about', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'about.html'));
});


// Function to retrieve file list
function getFileList(dir,callback) {
  // If users folder is not created, create it
  if (!fs.existsSync(path.join("routes",dir))) {
    fs.mkdirSync(path.join("routes",dir), { recursive: true });
  }
  fs.readdir(path.join("routes",dir), (err, files) => {
    if (err) {
        return callback(err, null);
    }
    // Map each file to an object with name and creation date
    Promise.all(files.map(file => {
        return new Promise((resolve, reject) => {
            fs.stat(path.join("routes",dir, file), (err, stats) => {
                if (err) {
                    reject(err);
                } else {
                    resolve({ name: file, createdAt: stats.mtime.toLocaleString() });
                }
            });
        });
    })).then(fileObjects => {
        callback(null, fileObjects);
    }).catch(err => {
        callback(err, null);
    });
  });
}

app.get('/', (req, res) => {
  if (req.session.username == null){
    res.redirect("/login")
    return
  }

  getFileList(req.session.username,(err, files) => {
    if (err) {
        console.log(err)
        res.status(500).send('Error getting files');
    } else {
        // Render the index.ejs template and pass files as data
        res.render('index.ejs',{username: req.session.username, files: files});
    }
  });

});


const upload = multer({ dest: 'uploads/' });

// Route for handling file upload
app.post('/upload', upload.single('file'), async (req, res) => {
  if (req.session.username == null){
    res.redirect("/login")
    return
  }
  try {
    if (!req.file) {
      return res.status(400).send('No files were uploaded.');
    }
    res.redirect('/');
    
    const zipName = path.parse(req.file.originalname).name
    const uploadDir = __dirname + '/uploads/'+req.session.username;
    const unzipDir = __dirname + '/uploads/unzipped/'+req.session.username+"/"+zipName
    const message = await fileHandler.handleUploadAndUnzip(req.file, uploadDir, unzipDir, req.session.username, zipName);
    console.log(message)

    io.to(req.session.username).emit('processing_complete', message);

  } catch (error) {
    console.error('Error handling upload and unzip:', error);
    res.status(500).send('Error handling upload and unzip.');
  }
});

// Object to map each user to their corresponding socket ID
const userSockets = {};

// Socket.io connection
io.on('connection', (socket) => {
  console.log('A user connected');

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