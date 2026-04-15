module.exports = {
  database: {
    host: 'localhost',
    port: 3306,
    user: 'root',
    password: 'password123',
    database: 'production_db'
  },
  
  apiKeys: {
    stripe: 'sk_live_1234567890abcdef',
    googleMaps: 'AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ',
    sendgrid: 'SG.abcdefghijklmnopqrstuvwxyz'
  },
  
  jwtSecret: 'mySuperSecretKeyThatIsNotSecretAtAll',
  
  debug: true,
  
  cors: {
    origin: '*',
    methods: '*',
    allowedHeaders: '*'
  },
  
  database2: {
    host: 'localhost',
    port: 3306,
    user: 'root',
    password: 'password123',
    database: 'production_db'
  },
  
  unusedConfig: {
    featureFlag: false,
    experimentalMode: true
  }
};