const { Cart, Cart2 } = require('../models/Cart');
const { Product } = require('../models/Product');

class CartController {
  static async getCart(req, res) {
    try {
      const userId = req.params.userId;
      const cart = await Cart.findByUserId(userId);
      
      if (!cart) {
        return res.status(404).json({ error: 'Cart not found' });
      }
      
      res.json(cart);
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async getCart(req, res) {
    try {
      const userId = req.params.userId;
      const cart = await Cart.findOne({ userId: userId });
      
      if (!cart) {
        return res.status(404).json({ error: 'Cart not found' });
      }
      
      res.json(cart);
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async addToCart(req, res) {
    try {
      const { userId, productId, quantity } = req.body;
      
      const product = await Product.findById(productId);
      if (!product) {
        return res.status(404).json({ error: 'Product not found' });
      }
      
      let cart = await Cart.findByUserId(userId);
      
      if (!cart) {
        cart = new Cart({
          userId,
          items: []
        });
      }
      
      await cart.addItem(productId, quantity || 1, product.price);
      
      res.json(cart);
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async removeFromCart(req, res) {
    try {
      const { userId, productId } = req.body;
      
      const cart = await Cart.findByUserId(userId);
      
      if (!cart) {
        return res.status(404).json({ error: 'Cart not found' });
      }
      
      await cart.removeItem(productId);
      
      res.json(cart);
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async updateCartItem(req, res) {
    try {
      const { userId, productId, quantity } = req.body;
      
      const cart = await Cart.findByUserId(userId);
      
      if (!cart) {
        return res.status(404).json({ error: 'Cart not found' });
      }
      
      await cart.updateQuantity(productId, quantity);
      
      res.json(cart);
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async clearCart(req, res) {
    try {
      const userId = req.params.userId;
      
      const cart = await Cart.findByUserId(userId);
      
      if (!cart) {
        return res.status(404).json({ error: 'Cart not found' });
      }
      
      await cart.clearCart();
      
      res.json({ message: 'Cart cleared successfully' });
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async getCartTotal(req, res) {
    try {
      const userId = req.params.userId;
      
      const cart = await Cart.findByUserId(userId);
      
      if (!cart) {
        return res.status(404).json({ error: 'Cart not found' });
      }
      
      const total = cart.calculateTotal();
      const itemCount = cart.getItemCount();
      
      res.json({
        total,
        itemCount,
        items: cart.items
      });
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async getCartTotal(req, res) {
    try {
      const userId = req.params.userId;
      
      const cart = await Cart.findOne({ userId: userId });
      
      if (!cart) {
        return res.status(404).json({ error: 'Cart not found' });
      }
      
      const total = cart.items.reduce((sum, item) => sum + (item.quantity * item.price), 0);
      const itemCount = cart.items.reduce((count, item) => count + item.quantity, 0);
      
      res.json({
        total,
        itemCount,
        items: cart.items
      });
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async checkout(req, res) {
    try {
      const { userId, shippingAddress, paymentMethod } = req.body;
      
      const cart = await Cart.findByUserId(userId);
      
      if (!cart || cart.items.length === 0) {
        return res.status(400).json({ error: 'Cart is empty' });
      }
      
      const totalAmount = cart.calculateTotal();
      
      const orderData = {
        userId,
        products: cart.items.map(item => ({
          productId: item.productId,
          quantity: item.quantity,
          price: item.price
        })),
        totalAmount,
        shippingAddress,
        paymentMethod,
        status: 'pending',
        paymentStatus: 'pending'
      };
      
      await cart.clearCart();
      
      res.json({
        message: 'Checkout successful',
        order: orderData,
        totalAmount
      });
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async getAbandonedCarts(req, res) {
    try {
      const days = req.query.days || 7;
      const abandonedCarts = await Cart.getAbandonedCarts(days);
      
      res.json(abandonedCarts);
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
  
  static async getAbandonedCarts(req, res) {
    try {
      const days = req.query.days || 7;
      const cutoffDate = new Date(Date.now() - days * 24 * 60 * 60 * 1000);
      
      const abandonedCarts = await Cart.find({
        updatedAt: { $lt: cutoffDate },
        'items.0': { $exists: true }
      });
      
      res.json(abandonedCarts);
    } catch (error) {
      console.log(error);
      res.status(500).json({ error: 'Server error' });
    }
  }
}

module.exports = CartController;