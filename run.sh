#!/bin/bash

echo 'Clearing JSON folder...'
rm json/*.txt

echo 'Pulling data from Shopify API...'
# Change min_updated_date parameter to (current date - N days) to have a lookback period
ruby puller/shopify_puller.rb '2010-01-01 00:00'

echo 'Clearing import folder...'
rm import/*.txt

echo 'Transforming JSON to flat files...'
python etl.py json/ShopifyAPI\:\:Product.json product > import/load_dim_product.txt
python etl.py json/ShopifyAPI\:\:Product.json sku > import/load_dim_sku.txt
python etl.py json/ShopifyAPI\:\:Order.json order > import/load_dim_order.txt
python etl.py json/ShopifyAPI\:\:Order.json order_line > import/load_fact_order_line.txt

echo 'Truncating mySQL temp tables...'
/usr/local/mysql/bin/mysql -u root shopify < sql/truncate_load_tables.sql

echo 'Importing mySQL temp tables...'
/usr/local/mysql/bin/mysqlimport -u root --local --debug --verbose shopify import/load_dim_product.txt
/usr/local/mysql/bin/mysqlimport -u root --local --debug --verbose shopify import/load_dim_sku.txt
/usr/local/mysql/bin/mysqlimport -u root --local --debug --verbose shopify import/load_dim_order.txt
/usr/local/mysql/bin/mysqlimport -u root --local --debug --verbose shopify import/load_fact_order_line.txt

echo 'Updating mySQL data warehouse tables...'
/usr/local/mysql/bin/mysql -u root shopify < sql/update_dim_product.sql
/usr/local/mysql/bin/mysql -u root shopify < sql/update_dim_sku.sql
/usr/local/mysql/bin/mysql -u root shopify < sql/update_dim_order.sql
/usr/local/mysql/bin/mysql -u root shopify < sql/update_fact_order_line.sql
