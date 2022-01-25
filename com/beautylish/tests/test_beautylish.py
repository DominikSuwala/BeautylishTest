import numpy as np
import pandas as pd
import urllib3
import json
import sys

from com.beautylish.beautylishapp.beautylish import Beautylish

import unittest

test_data_json = '{"products": [{"deleted": false, "price": "$10.00", "brand_name": "Wonderful Widgets", "id": 1001, "hidden": false, "product_name": "Most Wonderful Widget"}, {"deleted": false, "price": "$10.00", "brand_name": "Hooli", "id": 2003, "hidden": false, "product_name": "Nucleus"}, {"deleted": false, "price": "$123.45", "brand_name": "Wonderful Widgets", "id": 1002, "hidden": false, "product_name": "Another Widget"}, {"deleted": false, "price": "$10.00", "brand_name": "Acme", "id": 2002, "hidden": false, "product_name": "Mini Anvil"}, {"deleted": true, "price": "$10.00", "brand_name": "Acme", "id": 2003, "hidden": false, "product_name": "Anvil - Two Pack"}, {"deleted": false, "price": "$99.99", "brand_name": "Acme", "id": 2001, "hidden": true, "product_name": "Giant Anvil"}, {"deleted": false, "price": "$10.00", "brand_name": "Acme", "id": 2002, "hidden": false, "product_name": "Mini Anvil"}, {"deleted": false, "price": "$123.45", "brand_name": "Acme", "id": 2000, "hidden": false, "product_name": "Anvil"}, {"deleted": false, "price": "$99.99", "brand_name": "Wonderful Widgets", "id": 1000, "hidden": false, "product_name": "Widget 3000"}]}'

class BeautylishTestCase(unittest.TestCase):

    def setUp(self):
        self.catalog = Beautylish()
        self.catalog.set_obj(test_data_json)

    def test_filter_items_marked_deleted(self):
        # Has product with deleted set to True prior to filter
        self.assertTrue(True in self.catalog.df['deleted'].values)

        # Does not have product with ID 2003 after filtering
        self.catalog.filter_items_marked_deleted()
        self.assertFalse(True in self.catalog.df['deleted'].values)

    
    def test_filter_items_marked_hidden(self):
        # Has product with hidden set to True prior to filter
        self.assertTrue(True in self.catalog.df['hidden'].values)

        # Does not have product with ID 2001 after filtering
        self.catalog.filter_items_marked_hidden()
        
        self.assertFalse(True in self.catalog.df['hidden'].values)

    def test_unique_brand_names_ct(self):
        self.assertEqual(3, self.catalog.get_unique_brand_names_ct())

    def test_unique_product_names_ct(self):
        self.assertEqual(3, self.catalog.get_unique_product_names_ct())

if __name__ == "__main__":
    print(sys.path)
    unittest.main()