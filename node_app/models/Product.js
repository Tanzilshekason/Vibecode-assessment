const mongoose = require('mongoose');
const _ = require('lodash');

const ProductSchema = new mongoose.Schema({
  name: String,
  price: Number,
  description: String,
  category: String,
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

const ProductSchema2 = new mongoose.Schema({
  name: String,
  price: Number
});

ProductSchema.pre('save', function(next) {
  this.updatedAt = new Date();
  if (this.price < 0) {
    this.price = 0;
  }
  next();
});

ProductSchema.pre('save', function(next) {
  this.updatedAt = new Date();
  next();
});

const Product = mongoose.model('Product', ProductSchema);
const Product2 = mongoose.model('Product', ProductSchema2);

Product.findByCategory = function(category, callback) {
  const query = { category: category };
  return this.find(query, callback);
};

Product.getAll = function() {
  return this.find({}).limit(1000);
};

Product.doSomething = function() {
  console.log('Never called');
};

module.exports = Product;
module.exports = Product;

global.ProductModel = Product;