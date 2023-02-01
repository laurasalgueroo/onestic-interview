# -*- coding: utf-8 -*-
import pandas as pd
products = pd.read_csv('products.csv', header=0)
orders = pd.read_csv('orders.csv', header=0)
customers = pd.read_csv('customers.csv', header=0)


#report1
dic_order_prices = {}
ids = []
totals = []
for i in range(len(orders)):
    quanti = {}
    for pr in orders.iloc[i,:].products.split():
        if int(pr) not in quanti:
            quanti[int(pr)] = 1
        else:
            quanti[int(pr)] += 1
    total = 0
    for k, v in quanti.items():
        for j in range(len(products)):
            if k == products.iloc[j].id:
                calcul = products.iloc[j]['cost']*v
                total += calcul
    ids.append(orders.iloc[i,:].id)
    totals.append(total)
dic_order_prices['id'] = ids
dic_order_prices['total'] = totals

order_prices = pd.DataFrame(dic_order_prices)
order_prices.to_csv('order_prices.csv', index = False)

#report2
dic_product_customers = {pr:[] for pr in list(products.id)}
for k, v in dic_product_customers.items():
    for i in range(len(orders)):
        for elem in set(orders.iloc[i,:].products.split()):   #usamos un set para obtener solamente un id de cada producto, no nos interesa la cantidad del mismo
            if k == int(elem):
                v.append(orders.iloc[i,:].customer)

ids = []
for k in dic_product_customers.keys():
    ids+=[k]*len(dic_product_customers[k])
    
customer_ids = []
for v in dic_product_customers.values():
    customer_ids+=v
    
dic_product_customers2 = {'id': ids, 'customer_id': customer_ids}
product_customers = pd.DataFrame(dic_product_customers2)
product_customers.to_csv('product_customers.csv', index = False)

#report3
orders_with_prices = pd.merge(orders, order_prices, on='id')
orders_with_prices = orders_with_prices.drop(['products', 'id'], axis = 1)
orders_with_prices = orders_with_prices.groupby(by = 'customer').sum().reset_index()
orders_with_customers = pd.merge(orders_with_prices, customers, left_on='customer', right_on='id')
orders_with_customers = orders_with_customers.drop(['id'], axis = 1)  
customer_ranking = orders_with_customers.sort_values('total', ascending=False)
customer_ranking.to_csv('customer_ranking.csv', index = False)
