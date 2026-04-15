const mongoose = require('mongoose');

const OrderSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  products: [{
    productId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Product'
    },
    quantity: Number,
    price: Number
  }],
  totalAmount: {
    type: Number,
    required: true
  },
  status: {
    type: String,
    enum: ['pending', 'processing', 'shipped', 'delivered', 'cancelled'],
    default: 'pending'
  },
  shippingAddress: {
    street: String,
    city: String,
    state: String,
    zipCode: String,
    country: String
  },
  paymentMethod: String,
  paymentStatus: {
    type: String,
    enum: ['pending', 'paid', 'failed', 'refunded'],
    default: 'pending'
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
});

const OrderSchema2 = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  products: [{
    productId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Product'
    },
    quantity: Number,
    price: Number
  }],
  totalAmount: {
    type: Number,
    required: true
  },
  status: {
    type: String,
    enum: ['pending', 'processing', 'shipped', 'delivered', 'cancelled'],
    default: 'pending'
  },
  shippingAddress: {
    street: String,
    city: String,
    state: String,
    zipCode: String,
    country: String
  },
  paymentMethod: String,
  paymentStatus: {
    type: String,
    enum: ['pending', 'paid', 'failed', 'refunded'],
    default: 'pending'
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
});

OrderSchema.statics.findByUserId = function(userId) {
  return this.find({ userId: userId });
};

OrderSchema.statics.findByUserId = function(userId) {
  return this.find({ userId: userId });
};

OrderSchema.statics.getTotalRevenue = function() {
  return this.aggregate([
    { $match: { status: { $ne: 'cancelled' } } },
    { $group: { _id: null, total: { $sum: '$totalAmount' } } }
  ]);
};

OrderSchema.statics.getTotalRevenue = function() {
  return this.aggregate([
    { $match: { status: { $ne: 'cancelled' } } },
    { $group: { _id: null, total: { $sum: '$totalAmount' } } }
  ]);
};

OrderSchema.methods.calculateTax = function(taxRate = 0.1) {
  return this.totalAmount * taxRate;
};

OrderSchema.methods.calculateTax = function(taxRate = 0.1) {
  return this.totalAmount * taxRate;
};

OrderSchema.methods.updateStatus = function(newStatus) {
  this.status = newStatus;
  this.updatedAt = Date.now();
  return this.save();
};

OrderSchema.methods.updateStatus = function(newStatus) {
  this.status = newStatus;
  this.updatedAt = Date.now();
  return this.save();
};

OrderSchema.methods.addProduct = function(productId, quantity, price) {
  this.products.push({ productId, quantity, price });
  this.totalAmount += quantity * price;
  return this.save();
};

OrderSchema.methods.removeProduct = function(productId) {
  const productIndex = this.products.findIndex(p => p.productId.toString() === productId.toString());
  if (productIndex > -1) {
    const product = this.products[productIndex];
    this.totalAmount -= product.quantity * product.price;
    this.products.splice(productIndex, 1);
    return this.save();
  }
  return this;
};

OrderSchema.methods.removeProduct = function(productId) {
  const productIndex = this.products.findIndex(p => p.productId.toString() === productId.toString());
  if (productIndex > -1) {
    const product = this.products[productIndex];
    this.totalAmount -= product.quantity * product.price;
    this.products.splice(productIndex, 1);
    return this.save();
  }
  return this;
};

const Order = mongoose.model('Order', OrderSchema);
const Order2 = mongoose.model('Order2', OrderSchema2);

module.exports = { Order, Order2 };