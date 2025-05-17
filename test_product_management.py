import unittest
from unittest.mock import patch, MagicMock
from requests.exceptions import HTTPError
from product_management import (
    is_product_exists,
    creating_product,
    get_product_id_of_existing_product,
    adding_product_to_stock,
    previous_stock_amount,
    consuming_product
)

class TestProductManagement(unittest.TestCase):

    @patch("product_management.requests.get")
    def test_is_product_exists_found(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = [
            {"id": 1, "name": "tomato"},
            {"id": 2, "name": "cucumber"}
        ]
        result = is_product_exists("cucumber")
        self.assertEqual(result, 2)

    @patch("product_management.requests.get")
    def test_is_product_exists_not_found(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = [
            {"id": 1, "name": "tomato"}
        ]
        result = is_product_exists("apple")
        self.assertEqual(result, -1)

    @patch("product_management.requests.post")
    def test_creating_product_success(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200)
        result = creating_product("apple", 2, 2)
        self.assertEqual(result, 200)

    @patch("product_management.requests.post")
    def test_creating_product_failure(self, mock_post):
        mock_post.side_effect = Exception("Connection error")
        result = creating_product("banana", 2, 2)
        self.assertEqual(result, -1)

    @patch("product_management.requests.get")
    @patch("product_management.requests.post")
    def test_adding_product_to_stock_success(self, mock_post, mock_get):
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = [{"id": 10, "name": "orange"}]
        mock_post.return_value = MagicMock(status_code=200)
        result = adding_product_to_stock("orange", 3)
        self.assertIn("successfully", result.lower())

    @patch("product_management.get_product_id_of_existing_product")
    def test_adding_product_to_stock_product_not_found(self, mock_get_id):
        mock_get_id.return_value = -1
        result = adding_product_to_stock("notexist", 3)
        self.assertIn("not found", result.lower())

    @patch("product_management.requests.get")
    def test_get_product_id_found(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = [
            {"id": 3, "name": "apple"},
            {"id": 4, "name": "banana"}
        ]
        result = get_product_id_of_existing_product("banana")
        self.assertEqual(result, 4)

    @patch("product_management.requests.get")
    def test_get_product_id_not_found(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = [
            {"id": 1, "name": "milk"}
        ]
        result = get_product_id_of_existing_product("bread")
        self.assertEqual(result, -1)

    @patch("product_management.requests.get")
    def test_previous_stock_amount_success(self, mock_get):
        def side_effect(url, headers):
            mock_resp = MagicMock(status_code=200)
            if url.endswith("/products"):
                mock_resp.json.return_value = [{"id": 7, "name": "cheese"}]
            else:
                mock_resp.json.return_value = {"stock_amount": 15}
            return mock_resp

        mock_get.side_effect = side_effect
        result = previous_stock_amount("cheese")
        self.assertEqual(result, 15)

    @patch("product_management.requests.get")
    @patch("product_management.requests.post")
    def test_consuming_product_success(self, mock_post, mock_get):
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = [{"id": 6, "name": "yogurt"}]
        mock_post.return_value = MagicMock(status_code=200)
        result = consuming_product("yogurt", 2)
        self.assertIn("successfully", result.lower())

    @patch("product_management.requests.get")
    @patch("product_management.requests.post")
    def test_consuming_product_http_error(self, mock_post, mock_get):
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = [{"id": 9, "name": "juice"}]
        mock_post.side_effect = HTTPError("API error")
        result = consuming_product("juice", 1)
        self.assertIn("http error", result.lower())

if __name__ == "__main__":
    unittest.main()
