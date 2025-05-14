import requests
from requests.exceptions import HTTPError

API_KEY = "ATcgVTDlU5PGgRmqxDCcvYD6qPF4nnWBQZWvvmJDqNdg0hBsXe"
BASE_URL = "http://localhost:9283"

headers = {"GROCY-API-KEY":API_KEY,
            "Accept": "application/json",
            "Content-Type":"application/json"
           }



def is_product_exists(product:str) -> int:

    """
    Sends a GET request to the Grocy API to check if a product exists in the database.

    Returns the ID of the product if it exists, otherwise returns -1.

    Args:
       product_name (str): The name of the product to check.

    Returns:
       int: The ID of the product if it exists, otherwise -1.

    The function loops through the products in the database and checks if the given product exists.
    If found, it returns the product's ID.
    """

    try:
        response = requests.get(f"{BASE_URL}/api/objects/products",headers= headers)
        response.raise_for_status()
        response_json = response.json()
        for data in response_json:
            id = data["id"]
            name = data["name"]
            if name == product:
                return id
        return -1
    except HTTPError as http_err :
            print(f"HTTP error occurred: {http_err}")
            return -1
    except Exception as err:
            print(f"Ann error occurred: {err}")
            return -1    


#quantity_id 2->piece, 3->pack
#location_id 2->fridge, 3->pantry
def creating_product(name:str, location_id:int,quantity_id:int )-> int:
     '''
     Creates a new product in the Grocy Database.
        Args:
            name (str): The name of the product.
            location_id (int): The ID of the location where the product is stored.
            quantity_id (int): The ID of the quantity type for the product.

        Returns:
            int: The status code of the response from the API.
        The function checks if the product already exists in the database.
        If it does, it returns -1.
        If it doesn't, it creates a new product with the given name, location ID, and quantity ID.
        If the product is created successfully, it returns the status code of the response.
     '''    
     try:
          product = {
                        "name": name,
                        "location_id":location_id,
                        "qu_id_purchase": quantity_id,
                        "qu_id_stock":quantity_id
                    }
          
          response = requests.post(f"{BASE_URL}/api/objects/products",headers=headers,json= product)
          response.raise_for_status()        
          return response.status_code

     except HTTPError as http_err :
          print(f"HTTP error occurred: {http_err}")
          return -1
     
     except Exception as err:
          print(f"Ann error occurred: {err}")
          return -1


def get_product_id_of_existing_product(product:str)->int:
     """
     Retrieves the product ID for an existing product from the Grocy database.

     Args:
          product (str): The name of the product to search for.

     Returns:
          int: The product ID if found.
               -1 if the product is not found.
          str: An error message if an HTTP or other exception occurs.

     The function sends a GET request to the Grocy API to fetch all products.
     It then searches the list for a product with a matching name.
     If a match is found, it returns the corresponding product ID.
     If no match is found, it returns -1.
     If an error occurs during the request, it returns a descriptive error message.
     """


     try:
        response = requests.get(f"{BASE_URL}/api/objects/products",headers= headers)
        response.raise_for_status()
        response_json = response.json()
        product_id = None
        for data in response_json:
            id = data["id"]
            name = data["name"]
            if name == product:
               product_id = id
               return product_id
                
        if product_id is None:
             return -1
     except HTTPError as http_err :
        return f"HTTP error occurred: {http_err}"
     
     except Exception as err:
          return f"An error occured f{err}"
            

def adding_product_to_stock(product:str, amount:int) ->str:
     '''
     Adding declared product into stock.
     
     Args:
          product (str): The name of the product to be added.
          amount (int): The amount of the product to be added.    

     Returns:
          str: A message indicating the result of the operation.

     The function first checks if the product exists in the database.
     If it does, it retrieves the product ID.        
     If the product ID is found, it creates a dictionary with the amount.
     Then, it sends a POST request to the Grocy API to add the product to stock.
     If the request is successful, it returns a success message.    
     '''
    
     try:
        product_id = get_product_id_of_existing_product(product)
        product_to_write = {
                "amount": amount,
                "transaction_type":"purchase"
        }

        response = requests.post(f"{BASE_URL}/api/stock/products/{product_id}/add"
                                 ,headers=headers,json= product_to_write)
        
        response.raise_for_status()    
        return f"Added {product} to stock succesfully"
                       
     except HTTPError as http_err :
        return f"HTTP error occurred: {http_err}"
     
     except Exception as err:
          return f"An error occured f{err}"

def previous_stock_amount(product:str)-> int:
     """
     Gets the previous stock amount of a product.

     Args:
          product (str): The name of the product.

     Returns:
          int: The stock amount if the product is found.
          str: An error message if something goes wrong.
     
     The function retrieves the product ID and fetches the stock amount from the API.
     """


     try:
         product_id = get_product_id_of_existing_product(product)
         response = requests.get(f"{BASE_URL}/api/stock/products/{product_id}",headers= headers)
         response.raise_for_status()
         response_json = response.json()
         amount = response_json["stock_amount"]
         return amount
    
     except HTTPError as http_err :
        return f"HTTP error occurred: {http_err}"
     
     except Exception as err:
          return f"An error occured f{err}"

def consuming_product(product:str, amount:int)->str:
     '''
     Works as a stock amount updater.
     if product amount is less than previous amount, it will consume the product.
     Args:
          product (str): The name of the product to be consumed.
          amount (int): The amount of the product to be consumed.
     Returns:
          str: A message indicating the result of the operation.
     The function first checks if the product exists in the database.
     If it does, it retrieves the product ID.
     If the product ID is found, it creates a dictionary with the amount and transaction type.
     Then, it sends a POST request to the Grocy API to consume the product.
     If the request is successful, it returns a success message.

     
     '''
     try:
        product_id = get_product_id_of_existing_product(product)
        product_to_consume = {
                "amount": amount,
                "transaction_type":"purchase"
        }

        response = requests.post(f"{BASE_URL}/api/stock/products/{product_id}/consume"
                                 ,headers=headers,json= product_to_consume)
        
        response.raise_for_status()    
        return f"Consumed {product} from stock succesfully"
                       
     except HTTPError as http_err :
        return f"HTTP error occurred: {http_err}"
     
     except Exception as err:
          return f"An error occured f{err}"

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
