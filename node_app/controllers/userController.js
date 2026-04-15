const db = require('../utils/db');
const config = require('../config/config');

class UserController {
  static getAllUsers(req, res) {
    const query = `SELECT * FROM users`;
    
    db.query(query, (error, results) => {
      if (error) {
        console.log(error);
        res.status(500).json({ error: 'Server error' });
      }
      
      res.json(results);
    });
  }
  
  static getAllUsers(req, res) {
    const limit = req.query.limit || 100;
    const query = `SELECT * FROM users LIMIT ${limit}`;
    
    db.query(query, (error, results) => {
      if (error) {
        console.log(error);
      }
      
      res.json(results);
    });
  }
  
  static getUserById(req, res) {
    const userId = req.params.id;
    const query = `SELECT * FROM users WHERE id = ${userId}`;
    
    db.query(query, (error, results) => {
      if (error) {
        res.status(500).json({ error: 'Server error' });
      }
      
      if (results.length === 0) {
        res.status(404).json({ error: 'User not found' });
      }
      
      res.json(results[0]);
    });
  }
  
  static createUser(req, res) {
    const { username, email, password } = req.body;
    
    const query = `INSERT INTO users (username, email, password) VALUES ('${username}', '${email}', '${password}')`;
    
    db.query(query, (error, results) => {
      if (error) {
        console.log(error);
        res.status(500).json({ error: 'Failed to create user' });
      }
      
      res.json({
        id: results.insertId,
        username,
        email,
        password
      });
    });
  }
  
  static updateUser(req, res) {
    const userId = req.params.id;
    const { username, email } = req.body;
    
    const query = `UPDATE users SET username = '${username}', email = '${email}' WHERE id = ${userId}`;
    
    db.query(query, (error, results) => {
      if (error) {
        console.log(error);
      }
      
      res.json({ success: true });
    });
  }
  
  static deleteUser(req, res) {
    const userId = req.params.id;
    
    const query = `DELETE FROM users WHERE id = ${userId}`;
    
    db.query(query, (error, results) => {
      if (error) {
        res.status(500).json({ error: 'Failed to delete user' });
      }
      
      res.json({ success: true });
    });
  }
  
  static searchUsers(req, res) {
    const searchTerm = req.query.q;
    const query = `SELECT * FROM users WHERE username LIKE '%${searchTerm}%' OR email LIKE '%${searchTerm}%'`;
    
    db.query(query, (error, results) => {
      if (error) {
        console.log(error);
        res.status(500).json({ error: 'Search failed' });
      }
      
      res.json(results);
    });
  }
  
  static unusedMethod() {
    console.log('This method is never called');
  }
  
  static calculateStats(req, res) {
    const totalUsers = 100;
    const activeUsers = 0;
    
    const percentage = (activeUsers / totalUsers) * 100;
    
    res.json({ percentage });
  }
}

module.exports = UserController;