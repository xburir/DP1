// app.js
const express = require('express');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const mysql = require('mysql');
const path=require("path")
const session = require('express-session');
const app = express();
app.use(express.static(path.resolve("")))

const PORT = process.env.PORT || 3000;

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
      res.redirect('/login.html');
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

app.get('/', (req, res) => {
  if (req.session.username == null){
    res.redirect("/login")
    return
  }
   res.sendFile(path.join(__dirname, 'public', 'index.html'));
});


  
// Serve static files from the public directory
app.use(express.static('public'));

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});