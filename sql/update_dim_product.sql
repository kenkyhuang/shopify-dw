INSERT INTO dim_product
(
product_id,
created_date_key,
updated_date_key,
published_date_key,
created_on,
updated_on,
published_on,
handle,
name,
vendor
)
SELECT
product_id,
created_date_key,
updated_date_key,
published_date_key,
created_on,
updated_on,
published_on,
handle,
name,
vendor
FROM load_dim_product evt
ON DUPLICATE KEY UPDATE
created_date_key = evt.created_date_key,
updated_date_key = evt.updated_date_key,
published_date_key = evt.published_date_key,
created_on = evt.created_on,
updated_on = evt.updated_on,
published_on = evt.published_on,
handle = evt.handle,
name = evt.name,
vendor = evt.vendor;