# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import populate_betsy_db
populate_betsy_db.populate_betsy()


# Add your code after this line
import models_betsy
import peewee

# from typing import List
# from datetime import time
M = models_betsy


M.print_all_procucts()


########################################
print('#1. ############## search(term) ################')
def search(term):
    query_search = (M.Product.select().where(M.Product.name.contains(term)))
    print('------ print(prod.name, prod.description, prod.price_per_unit, prod.stock, prod.owner)')
    for prod in query_search:
        print(prod.name, prod.description, prod.price_per_unit, prod.stock, prod.owner)

search('sweater')


########################################
print('#2.############## list_user_products(user_id) ################')
def list_user_products(user_id):
    
    query_user_products = (M.Product.select(M.Product, M.User)
                        .join(M.User)
                        .where(M.User.id == user_id))
    print('------ print( prod.owner.name, prod.name, prod.description, prod.price_per_unit, prod.stock)')
    for prod in query_user_products:
            print(prod.owner.name, prod.name, prod.description, prod.price_per_unit, prod.stock)

list_user_products(1)
list_user_products(2)


########################################
print('#3.############## list_products_per_tag(tag_id) ################')
# def list_products_per_tag(tag_id):
#     query = (M.Product.select()
#             .join(M.Tag)
#             .where(M.Tag.id==tag_id))
#     print('-----------print(prod.name, prod.tag)')
#     for prod in query:
#         print(prod.name, prod.tag)

def list_products_per_tag(tag_id):
    query = (M.ProductTag
             .select(M.ProductTag,M.Product,M.Tag)
            .join(M.Product)
            .switch(M.ProductTag)
            .join(M.Tag)
            .where(M.Tag.id==tag_id))
    print('-----------print(prodtag.product.name, prodtag.tag.name)')
    for prodtag in query:
        print(prodtag.product.name, prodtag.tag.name)

list_products_per_tag(4)

########################################
print('#4.############## add_product_to_catalog(user_id, product) ################')
def add_product_to_catalog(user_id, product):
    models_betsy.Product.create(name=product, description='Product_DescriptionX', price_per_unit=100, stock=100, owner=user_id,tag=1) 


add_product_to_catalog(5, 'Product_nameX')
print('---- Test if product was added: M.print_all_procucts()')
M.print_all_procucts()  
print("------ list_user_products('Product_name')")
list_user_products('User_name5')

########################################
print('#5.############## update_stock(product_id, new_quantity) ################')
def update_stock(product_id, new_quantity):
    product = M.Product.select().where(M.Product.id == product_id).first()
    product.stock = new_quantity
    product.save()

update_stock(1, 600)
print('---- Test if stock was updated: M.print_all_procucts()')
M.print_all_procucts()  


########################################
print('#6.############## purchase_product(product_id, buyer_id, quantity) ################')
def purchase_product(product_id, buyer_id, quantity):
    M.Transaction.create(buyer=buyer_id, product=product_id, quantity=quantity) 

purchase_product(1, 1, 5)
query_all = M.Transaction.select()
for mod in query_all:
    print(mod.buyer.name, mod.product.name, mod.quantity)
print('---------')
query_all = M.Transaction.select()
for mod in query_all:
    print(mod.buyer.name, mod.product.name, mod.quantity)

query_all = M.Transaction.select()
for mod in query_all:
    print(mod.buyer.name, mod.product.name, mod.quantity)

########################################
print('#7.############## remove_product(product_id) ################')
def remove_product(product_id):
    product = M.Product.get(M.Product.id == product_id)
    product.delete_instance()

remove_product(2)
print('---- Test if product 1 was removed: M.print_all_procucts()')
M.print_all_procucts()  

########################################
print('#8. ############## Handle a purchase between a buyer and a seller for a given product')


seller_id = 4
seller_name='User_name4'
product_name = 'Product_name5: mobile'
product_id = 1
buy_quantity = 20

product = (M.Product
           .select(M.Product, M.User)
           .join(M.User)
           .where(M.Product.id == product_id and M.User.id == seller_id)
           .first())
print(product)


if product is None:
    producttemp=M.Product.get(M.Product.name==product_name)
    print('Product (', producttemp.name, ')is not owned by seller(', producttemp.owner.name, ')')
elif product.stock < buy_quantity:
    print('Product stock is to low: ', product.stock, '(', buy_quantity , ' was requested)')
else:
    purchase_product(product.id, seller_id, buy_quantity)
    updated_stock = product.stock - buy_quantity
    update_stock(product.id, updated_stock)
    
    print('Product bought: ', product.name, buy_quantity, '(from stock:',product.stock,')')
    print('Updated Stock: ', updated_stock)
    # print(product.owner.name,product.name, product.stock)
    
    print('---- Updated Product list: M.print_all_procucts()')
    M.print_all_procucts()  

    print('---- Updated transaction list: print(mod.buyer.name, mod.product.name, mod.quantity)')
    query_all = M.Transaction.select()
    for mod in query_all:
        print(mod.buyer.name, mod.product.name, mod.quantity)

a=1
exit()