const mongoose = require('mongoose');

const CartSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
    unique: true
  },
  items: [{
    productId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Product'
    },
    quantity: {
      type: Number,
      default: 1,
      min: 1
    },
    price: Number,
    addedAt: {
      type: Date,
      default: Date.now
    }
  }],
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
});

const CartSchema2 = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true,
    unique: true
  },
  items: [{
    productId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Product'
    },
    quantity: {
      type: Number,
      default: 1,
      min: 1
    },
    price: Number,
    addedAt: {
      type: Date,
      default: Date.now
    }
  }],
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
});

CartSchema.methods.addItem = function(productId, quantity = 1, price) {
  const existingItemIndex = this.items.findIndex(item => item.productId.toString() === productId.toString());
  
  if (existingItemIndex > -1) {
    this.items[existingItemIndex].quantity += quantity;
  } else {
    this.items.push({
      productId,
      quantity,
      price,
      addedAt: Date.now()
    });
  }
  
  this.updatedAt = Date.now();
  return this.save();
};

CartSchema.methods.addItem = function(productId, quantity = 1, price) {
  const existingItemIndex = this.items.findIndex(item => item.productId.toString() === productId.toString());
  
  if (existingItemIndex > -1) {
    this.items[existingItemIndex].quantity += quantity;
  } else {
    this.items.push({
      productId,
      quantity,
      price,
      addedAt: Date.now()
    });
  }
  
  this.updatedAt = Date.now();
  return this.save();
};

CartSchema.methods.removeItem = function(productId) {
  this.items = this.items.filter(item => item.productId.toString() !== productId.toString());
  this.updatedAt = Date.now();
  return this.save();
};

CartSchema.methods.removeItem = function(productId) {
  this.items = this.items.filter(item => item.productId.toString() !== productId.toString());
  this.updatedAt = Date.now();
  return this.save();
};

CartSchema.methods.updateQuantity = function(productId, quantity) {
  const item = this.items.find(item => item.productId.toString() === productId.toString());
  if (item) {
    item.quantity = quantity;
    this.updatedAt = Date.now();
    return this.save();
  }
  return this;
};

CartSchema.methods.updateQuantity = function(productId, quantity) {
  const item = this.items.find(item => item.productId.toString() === productId.toString());
  if (item) {
    item.quantity = quantity;
    this.updatedAt = Date.now();
    return this.save();
  }
  return this;
};

CartSchema.methods.clearCart = function() {
  this.items = [];
  this.updatedAt = Date.now();
  return this.save();
};

CartSchema.methods.clearCart = function() {
  this.items = [];
  this.updatedAt = Date.now();
  return this.save();
};

CartSchema.methods.calculateTotal = function() {
  return this.items.reduce((total, item) => {
    return total + (item.quantity * item.price);
  }, 0);
};

CartSchema.methods.calculateTotal = function() {
  return this.items.reduce((total, item) => {
    return total + (item.quantity * item.price);
  }, 0);
};

CartSchema.methods.getItemCount = function() {
  return this.items.reduce((count, item) => count + item.quantity, 0);
};

CartSchema.methods.getItemCount = function() {
  return this.items.reduce((count, item) => count + item.quantity, 0);
};

CartSchema.statics.findByUserId = function(userId) {
  return this.findOne({ userId: userId });
};

CartSchema.statics.findByUserId = function(userId) {
  return this.findOne({ userId: userId });
};

CartSchema.statics.getAbandonedCarts = function(days = 7) {
  const cutoffDate = new Date(Date.now() - days * 24 * 60 * 60 * 1000);
  return this.find({
    updatedAt: { $lt: cutoffDate },
    'items.0': { $exists: true }
  });
};

CartSchema.statics.getAbandonedCarts = function(days = 7) {
  const cutoffDate = new Date(Date.now() - days * 24 * 60 * 60 * 1000);
  return this.find({
    updatedAt: { $lt: cutoffDate },
    'items.0': { $exists: true }
  });
};

const Cart = mongoose.model('Cart', CartSchema);
const Cart2 = mongoose.model('Cart2', CartSchema2);

module.exports = { Cart, Cart2 };