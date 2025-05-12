import requests
from requests.exceptions import HTTPError

API_KEY = "ATcgVTDlU5PGgRmqxDCcvYD6qPF4nnWBQZWvvmJDqNdg0hBsXe"
BASE_URL = "http://localhost:9283"

headers = {
    "GROCY-API-KEY": API_KEY,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def is_product_exists(product: str) -> int:
    """
    Sends a GET request to the Grocy API to check if a product exists in the database.
    Returns the ID of the product if it exists, otherwise returns -1.
    """
    try:
        response = requests.get(f"{BASE_URL}/api/objects/products", headers=headers)
        response.raise_for_status()
        response_json = response.json()
        for data in response_json:
            if data["name"] == product:
                return data["id"]
        return -1
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return -1
    except Exception as err:
        print(f"Ann error occurred: {err}")
        return -1

def creating_product(name: str, location_id: int, quantity_id: int) -> int:
    """
    Creates a new product in the Grocy Database.
    """
    try:
        product = {
            "name": name,
            "location_id": location_id,
            "qu_id_purchase": quantity_id,
            "qu_id_stock": quantity_id
        }
        response = requests.post(f"{BASE_URL}/api/objects/products", headers=headers, json=product)
        response.raise_for_status()
        return response.status_code
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return -1
    except Exception as err:
        print(f"Ann error occurred: {err}")
        return -1

def adding_product_to_stock(product: str, amount: int, best_before_date: str) -> str:
    """
    Adds a product to stock with a best before date.
    """
    try:
        response = requests.get(f"{BASE_URL}/api/objects/products", headers=headers)
        response.raise_for_status()
        response_json = response.json()

        product_id = None
        for data in response_json:
            if data["name"] == product:
                product_id = data["id"]
                break

        if product_id is None:
            return f"Product '{product}' not found."

        product_to_write = {
            "amount": amount,
            "best_before_date": best_before_date,
            "transaction_type": "purchase"
        }

        response = requests.post(
            f"{BASE_URL}/api/stock/products/{product_id}/add",
            headers=headers,
            json=product_to_write
        )
        response.raise_for_status()
        return f"Added {product} to stock successfully"
    except HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except Exception as err:
        return f"An error occurred: {err}"

# --------------------- TESTS ---------------------
if __name__ == "__main__":
    import unittest
    from unittest.mock import patch, MagicMock

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
            result = adding_product_to_stock("orange", 3, "2025-05-30")
            self.assertIn("success", result.lower())

        @patch("product_management.requests.get")
        def test_adding_product_to_stock_product_not_found(self, mock_get):
            mock_get.return_value = MagicMock(status_code=200)
            mock_get.return_value.json.return_value = [{"id": 10, "name": "banana"}]
            result = adding_product_to_stock("notexist", 3, "2025-05-30")
            self.assertEqual(result, "Product 'notexist' not found.")

    unittest.main()
