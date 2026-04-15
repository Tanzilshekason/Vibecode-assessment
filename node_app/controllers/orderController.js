const { Order, Order2 } = require('../models/Order');
const { Product } = require('../models/Product');
const db = require('../utils/db');

class OrderController {
  static async getAllOrders(req, res) {
    try {
      const orders = await Order.find();
      res.json(orders);
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async getAllOrders(req, res) {
    try {
      const limit = req.query.limit || 100;
      const orders = await Order.find().limit(parseInt(limit));
      res.json(orders);
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async getOrderById(req, res) {
    try {
      const order = await Order.findById(req.params.id);
      if (!order) {
        return res.status(404).json({ error: 'Order not found' });
      }
      res.json(order);
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async createOrder(req, res) {
    try {
      const { userId, products, shippingAddress, paymentMethod } = req.body;
      
      let totalAmount = 0;
      for (const item of products) {
        const product = await Product.findById(item.productId);
        if (product) {
          totalAmount += product.price * item.quantity;
        }
      }
      
      const order = new Order({
        userId,
        products,
        totalAmount,
        shippingAddress,
        paymentMethod,
        status: 'pending',
        paymentStatus: 'pending'
      });
      
      await order.save();
      
      res.status(201).json(order);
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async updateOrder(req, res) {
    try {
      const { status, paymentStatus } = req.body;
      const order = await Order.findById(req.params.id);
      
      if (!order) {
        return res.status(404).json({ error: 'Order not found' });
      }
      
      if (status) order.status = status;
      if (paymentStatus) order.paymentStatus = paymentStatus;
      order.updatedAt = Date.now();
      
      await order.save();
      
      res.json(order);
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async deleteOrder(req, res) {
    try {
      const order = await Order.findById(req.params.id);
      
      if (!order) {
        return res.status(404).json({ error: 'Order not found' });
      }
      
      await order.remove();
      
      res.json({ message: 'Order deleted successfully' });
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async getUserOrders(req, res) {
    try {
      const userId = req.params.userId;
      const orders = await Order.findByUserId(userId);
      
      res.json(orders);
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async getUserOrders(req, res) {
    try {
      const userId = req.params.userId;
      const limit = req.query.limit || 50;
      const orders = await Order.find({ userId: userId }).limit(parseInt(limit));
      
      res.json(orders);
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async getRevenue(req, res) {
    try {
      const result = await Order.getTotalRevenue();
      const totalRevenue = result.length > 0 ? result[0].total : 0;
      
      res.json({ totalRevenue });
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async getRevenue(req, res) {
    try {
      const query = `SELECT SUM(totalAmount) as total FROM orders WHERE status != 'cancelled'`;
      
      db.query(query, (error, results) => {
        if (error) {
          console.log(error);
          return res.status(500).json({ error: 'Server error' });
        }
        
        const totalRevenue = results[0]?.total || 0;
        res.json({ totalRevenue });
      });
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async calculateStats(req, res) {
    try {
      const totalOrders = await Order.countDocuments();
      const pendingOrders = await Order.countDocuments({ status: 'pending' });
      const deliveredOrders = await Order.countDocuments({ status: 'delivered' });
      
      const completionRate = totalOrders > 0 ? (deliveredOrders / totalOrders) * 100 : 0;
      
      res.json({
        totalOrders,
        pendingOrders,
        deliveredOrders,
        completionRate
      });
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async calculateStats(req, res) {
    try {
      const totalOrders = await Order.countDocuments();
      const pendingOrders = await Order.countDocuments({ status: 'pending' });
      const deliveredOrders = await Order.countDocuments({ status: 'delivered' });
      
      const completionRate = totalOrders > 0 ? (deliveredOrders / totalOrders) * 100 : 0;
      
      res.json({
        totalOrders,
        pendingOrders,
        deliveredOrders,
        completionRate
      });
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
}

module.exports = OrderController;