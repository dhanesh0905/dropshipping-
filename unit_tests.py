import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from dropshipping import BackendService

class TestBackendService(unittest.TestCase):
    def setUp(self):
        self.backend = BackendService()
        self.sample_cart = [
            {"id": 101, "name": "Naruto Hoodie", "price": 49.99, "quantity": 2},
            {"id": 102, "name": "One Piece T-Shirt", "price": 29.99, "quantity": 1}
        ]
    
    def test_create_order_with_empty_cart(self):
        """Test creating order with empty cart returns correct error"""
        with self.assertRaises(ValueError):
            self.backend.create_order([])
    
    def test_create_order_has_correct_order_id_format(self):
        """Test order ID follows the correct format"""
        order = self.backend.create_order(self.sample_cart)
        self.assertTrue(order["order_id"].startswith("ORD-"))
        self.assertEqual(len(order["order_id"]), 10)  # ORD- + 6 chars
    
    def test_create_order_contains_all_cart_items(self):
        """Test all cart items are included in the order"""
        order = self.backend.create_order(self.sample_cart)
        self.assertEqual(len(order["items"]), 2)
        self.assertEqual(order["items"][0]["id"], 101)
        self.assertEqual(order["items"][1]["id"], 102)
    
    def test_create_order_has_correct_total(self):
        """Test order total is calculated correctly"""
        order = self.backend.create_order(self.sample_cart)
        expected_total = (49.99 * 2) + 29.99
        self.assertAlmostEqual(order["total"], expected_total, places=2)
    
    def test_create_order_has_processing_status(self):
        """Test new orders have 'Processing' status"""
        order = self.backend.create_order(self.sample_cart)
        self.assertEqual(order["status"], "Processing")
    
    def test_create_order_has_timestamp(self):
        """Test order has a valid timestamp"""
        with patch('datetime.datetime') as mock_datetime:
            test_time = datetime(2023, 1, 1, 12, 0, 0)
            mock_datetime.utcnow.return_value = test_time
            order = self.backend.create_order(self.sample_cart)
            self.assertEqual(order["timestamp"], test_time.isoformat())
    
    def test_create_order_adds_to_orders_list(self):
        """Test order is added to the orders list"""
        initial_count = len(self.backend.orders)
        order = self.backend.create_order(self.sample_cart)
        self.assertEqual(len(self.backend.orders), initial_count + 1)
        self.assertEqual(self.backend.orders[-1]["order_id"], order["order_id"])
    
    def test_create_order_with_single_item(self):
        """Test order creation with single item"""
        single_item_cart = [{"id": 101, "name": "Naruto Hoodie", "price": 49.99, "quantity": 1}]
        order = self.backend.create_order(single_item_cart)
        self.assertEqual(len(order["items"]), 1)
        self.assertEqual(order["total"], 49.99)
    
    def test_create_order_with_large_quantities(self):
        """Test order creation with large quantities"""
        large_cart = [{"id": 101, "name": "Naruto Hoodie", "price": 49.99, "quantity": 100}]
        order = self.backend.create_order(large_cart)
        self.assertEqual(order["total"], 49.99 * 100)
    
    def test_create_order_preserves_item_details(self):
        """Test order preserves all item details"""
        order = self.backend.create_order(self.sample_cart)
        for item in order["items"]:
            self.assertIn("name", item)
            self.assertIn("price", item)
            self.assertIn("quantity", item)
            self.assertIn("id", item)
    
    def test_create_order_with_zero_quantity_fails(self):
        """Test order creation fails with zero quantity"""
        invalid_cart = [{"id": 101, "name": "Naruto Hoodie", "price": 49.99, "quantity": 0}]
        with self.assertRaises(ValueError):
            self.backend.create_order(invalid_cart)

if __name__ == '__main__':
    unittest.main()