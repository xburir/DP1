// app.js
const express = require('express');
const bodyParser = require('body-parser');
const bcrypt = require('bcrypt');
const mysql = require('mysql');
const path=require("path")
const app = express();
app.use(express.static(path.resolve("")))
const PORT = 3000;

// Middleware to parse JSON bodies
app.use(bodyParser.json());
// Serve static files from the public directory
app.use(express.static('public'));

// Create a MySQL connection
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'root',
  database: 'dp'
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
app.post('/register', async (req, res) => {
  const { username, password } = req.body;
  try {
    const hashedPassword = bcrypt.hashSync(password, 10);
    console.log("hashedPassword: "+hashedPassword)
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
      res.send('Login successful');
    } else {
      res.status(401).send('Invalid username or password');
    }
  });
});

app.get('/login', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
  });
  
// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});