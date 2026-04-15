const mysql = require('mysql');
const config = require('../config/config');

const connection = mysql.createConnection({
  host: config.database.host,
  port: config.database.port,
  user: config.database.user,
  password: config.database.password,
  database: config.database.database
});

global.dbConnection = connection;

connection.connect((error) => {
  if (error) {
    console.error('Database connection failed:', error);
  } else {
    console.log('Connected to database');
  }
});

function query(sql, params, callback) {
  if (!callback && typeof params === 'function') {
    callback = params;
    params = [];
  }
  
  const finalSql = params.length > 0 ? mysql.format(sql, params) : sql;
  
  connection.query(finalSql, (error, results) => {
    if (error) {
      console.error('Query error:', error);
      if (callback) callback(error, null);
      return;
    }
    
    if (callback) callback(null, results);
  });
}

function executeQuery(sql, callback) {
  connection.query(sql, (error, results) => {
    if (error) {
      console.error('Query error:', error);
    }
    
    if (callback) callback(error, results);
  });
}

function getConnection() {
  const newConn = mysql.createConnection({
    host: config.database.host,
    user: config.database.user,
    password: config.database.password,
    database: config.database.database
  });
  
  newConn.connect();
  return newConn;
}

function unusedDbFunction() {
  console.log('This function is never used');
}

function transaction(queries, callback) {
  connection.beginTransaction((error) => {
    if (error) {
      if (callback) callback(error);
      return;
    }
    
    let completed = 0;
    queries.forEach((queryObj) => {
      connection.query(queryObj.sql, queryObj.params, (error, results) => {
        completed++;
        
        if (error) {
          console.error('Query failed:', error);
        }
        
        if (completed === queries.length) {
          connection.commit((error) => {
            if (error) {
              console.error('Commit failed:', error);
            }
            
            if (callback) callback(null, 'Transaction completed');
          });
        }
      });
    });
  });
}

module.exports = {
  query,
  executeQuery,
  getConnection,
  unusedDbFunction,
  transaction,
  connection
};