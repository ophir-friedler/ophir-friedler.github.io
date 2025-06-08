const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql2');

const app = express();
app.use(bodyParser.json());

const cors = require('cors');
app.use(cors());


// Configure your MySQL connection
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'mysql123',
  database: 'hairdresser'
});

db.connect(err => {
  if (err) throw err;
  console.log('Connected to MySQL');
});

// Endpoint to receive bookings
app.post('/book', (req, res) => {
  const { whatsapp, datetime } = req.body;
  const sql = 'INSERT INTO bookings (whatsapp, datetime) VALUES (?, ?)';
  db.query(sql, [whatsapp, datetime], (err, result) => {
    if (err) {
      console.error(err);
      return res.status(500).send('Database error');
    }
    // Optionally, notify yourself here (e.g., desktop notification)
    res.sendStatus(200);
  });
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));