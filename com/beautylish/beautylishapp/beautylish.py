"""
Author: Dominik Suwala <dxs9411@rit.edu>


Query this API that returns a randomized list of products in JSON format:
https://www.beautylish.com/rest/interview-product/list
    ● Display a list of products including only the brand name, product name, and price.
        ○ Filter out any products that are hidden or deleted.
        ○ Sort by lowest to highest price. If two items have the same price, sort by name.
        ○ If the same product is included twice, only display it once.
    ● Display a summary that includes:
        ○ The total number of unique products
        ○ The total number of unique brands
        ○ The average price

"""
import pandas as pd
import urllib3
import json

class Beautylish:
    __slots__ = ('raw_json', 'json_s', 'df')

    def __init__(self):
        pass

    def clean_price_remove_symbols(self):
        self.df['price'] = self.df['price'].str.replace(',', '')
        self.df['price'] = self.df['price'].str.replace("$", '')
        self.df['price'] = self.df['price'].astype(float)

    def filter_items_marked_deleted(self):
        self.df = self.df.drop(self.df[self.df.deleted == True].index)
    def filter_items_marked_hidden(self):
        self.df = self.df.drop(self.df[self.df.hidden == True].index)
    
    def get_unique_brand_names(self):
        return self.df['brand_name'].unique()
    def get_unique_brand_names_ct(self):
        return len(self.get_unique_brand_names())
    
    def get_unique_product_names(self):
        return self.df['product_name'].unique()
    def get_unique_product_names_ct(self):
        return len(self.get_unique_brand_names())
    
    def call_api_list_products(self):
        url = 'https://www.beautylish.com/rest/interview-product/list'

        http = urllib3.PoolManager()
        resp = http.request("GET", url)

        return resp.data

    def set_obj(self, raw_json):
        self.raw_json = raw_json
        self.json_s = json.loads(self.raw_json)
        self.df = pd.json_normalize(self.json_s['products'])

def main():

    catalog = Beautylish()
    raw_json = '{"products": [{"deleted": false, "price": "$10.00", "brand_name": "Wonderful Widgets", "id": 1001, "hidden": false, "product_name": "Most Wonderful Widget"}, {"deleted": false, "price": "$10.00", "brand_name": "Hooli", "id": 2003, "hidden": false, "product_name": "Nucleus"}, {"deleted": false, "price": "$123.45", "brand_name": "Wonderful Widgets", "id": 1002, "hidden": false, "product_name": "Another Widget"}, {"deleted": false, "price": "$10.00", "brand_name": "Acme", "id": 2002, "hidden": false, "product_name": "Mini Anvil"}, {"deleted": true, "price": "$10.00", "brand_name": "Acme", "id": 2003, "hidden": false, "product_name": "Anvil - Two Pack"}, {"deleted": false, "price": "$99.99", "brand_name": "Acme", "id": 2001, "hidden": true, "product_name": "Giant Anvil"}, {"deleted": false, "price": "$10.00", "brand_name": "Acme", "id": 2002, "hidden": false, "product_name": "Mini Anvil"}, {"deleted": false, "price": "$123.45", "brand_name": "Acme", "id": 2000, "hidden": false, "product_name": "Anvil"}, {"deleted": false, "price": "$99.99", "brand_name": "Wonderful Widgets", "id": 1000, "hidden": false, "product_name": "Widget 3000"}]}'# catalog.call_api_list_products()

    catalog.set_obj(raw_json)
    
    # Remove dollars and comma symbols, modify df column to be of type float
    catalog.clean_price_remove_symbols()

    # Filter out any products that are hidden or deleted.
    catalog.filter_items_marked_deleted()
    catalog.filter_items_marked_hidden()
 
    # Sort by lowest to highest price. If two items have the same price, sort by name.
    df = catalog.df
    df = df.sort_values(by=['price','product_name'], ascending=(True, True))

    # If the same product is included twice, only display it once.
    df = df.drop_duplicates(subset=['product_name','brand_name'], keep='first')
    
    unique_products_ct = len(df['product_name'].unique())
    unique_products_ct = catalog.get_unique_product_names_ct()

    unique_brands_ct = len(df['brand_name'].unique())
    unique_brands_ct = catalog.get_unique_brand_names_ct()
    
    average_price = df['price'].sum() / df['price'].count()

    # Print out the data with these columns
    print_columns = ['brand_name', 'product_name', 'price']
    print(df.loc[:, df.columns.isin(print_columns)])

    # Print out a summary
    print('The total number of unique products: %s' % unique_products_ct)
    print('The total number of unique brands: %s' % unique_brands_ct)
    print('Average price: ${:,.2f}'.format(average_price))


if __name__ == "__main__":
    main()