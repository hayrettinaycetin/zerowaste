import product_management as pm


#Read from blob 
#Process Image 

#We need these 
product = "Egg"
amount = 10
best_before_date ="2025-05-05"



























if pm.is_product_exists(product) == -1:
     pm.creating_product(product, 2, 2)
     pm.adding_product_to_stock(product, amount, best_before_date )
     print("Hello")

else:
     pm.adding_product_to_stock(product, amount, best_before_date )
     print("Sa")