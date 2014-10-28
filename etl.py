import json
import sys
from datetime import datetime

def process_file(filename, type):

    f = open(filename, "r") 

    for line in f:
        data = json.loads(line)

        if type == 'product':
            output_row = product_json_to_flat(data)
        elif type == 'sku':
            for sku_data in data['variants']:
                output_row = sku_json_to_flat(sku_data, data)
        elif type == 'order':
            output_row = order_json_to_flat(data)
        elif type == 'order_line':
            for line_item in data['line_items']:
                output_row = order_line_json_to_flat(data, line_item)

        print output_row

def product_json_to_flat(data):

    """ 
    STEP 1: Define the columns you want in the exact order.
    """
    fields = ['product_id',
              'created_date_key', 
              'updated_date_key',
              'published_date_key',
              'created_on',
              'updated_on',
              'published_on',
              'handle',
              'name',
              'vendor']


    """ 
    STEP 2: Extract fields from JSON into python dictionary.
    """
    d = {}
    
    d['product_id'] = data.get('id', None)

    # Created
    if data['created_at']:
        created_dt = get_python_datetime_from_str(data['created_at'])
        d['created_date_key'] = get_datekey_from_datetime(created_dt)
        d['created_on'] = created_dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        d['created_on'] = None

    # Updated
    if data['updated_at']:
        updated_dt = get_python_datetime_from_str(data['updated_at'])
        d['updated_date_key'] = get_datekey_from_datetime(updated_dt)
        d['updated_on'] = updated_dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        d['updated_on'] = None

    # Published
    if data['published_at']:
        published_dt = get_python_datetime_from_str(data['published_at'])
        d['published_date_key'] = get_datekey_from_datetime(published_dt)
        d['published_on'] = published_dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        d['published_on'] = None 

    d['handle'] = data.get('handle', None)
    d['name'] = data.get('title', None)
    d['vendor'] = data.get('vendor', None)


    """
    STEP 3: Convert python dictionary into a tab-delimited string.
    """
    flat = '\t'.join([prepare_value(d.get(f, None)) for f in fields])
    
    return flat

def sku_json_to_flat(data, product_data):
    
    """ 
    STEP 1: Define the columns you want in the exact order.
    """
    fields = ['sku_code',
              'sku_id',
              'sku_name',
              'created_date_key',
              'updated_date_key',
              'created_on',
              'updated_on',
              'color',
              'size',
              'shopify_inventory_quantity',
              'shopify_inventory_management',
              'shopify_inventory_policy',
              'price',
              'compare_at_price',
              'taxable',
              'weight_in_grams',
              'weight_in_lbs',
              'product_id',
              'product_name',
              'vendor']


    """ 
    STEP 2: Extract fields from JSON into python dictionary.
    """
    d = {}

    # Record color and size variant positions
    color_variant_position = None
    size_variant_position = None
    for option in product_data['options']:
        if option['name'] == 'Color':
            color_variant_position = option['position']
        elif option['name'] == 'Size':
            size_variant_position = option['position']

    d['sku_key'] = "0"

    d['sku_id'] = data['id']

    d['product_id'] = product_data['id']

    d['product_name'] = product_data['title']

    d['vendor'] = product_data['vendor']

    if data['created_at']:
        created_dt = get_python_datetime_from_str(data['created_at'])
        d['created_date_key'] = get_datekey_from_datetime(created_dt)
        d['created_on'] = created_dt.strftime('%Y-%m-%d %H:%M:%S')

    else:
        d['created_date_key'] = "0"
        d['created_on'] = None

    if data['updated_at']:
        updated_dt = get_python_datetime_from_str(data['updated_at'])
        d['updated_date_key'] = get_datekey_from_datetime(updated_dt)
        d['updated_on'] = updated_dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        d['updated_date_key'] = "0"
        d['updated_on'] = None

    d['sku_name'] = data['title']

    d['sku_code'] = data['sku']

    if color_variant_position:
        color_variant_field = 'option%s' % color_variant_position
        d['color'] = data[color_variant_field]
    else:
        d['color'] = "N/A"
        
    if size_variant_position:
        size_variant_field = 'option%s' % size_variant_position
        d['size'] = data[size_variant_field]
    else:
        d['size'] = "N/A"

    d['shopify_inventory_quantity'] = float(data['inventory_quantity'])
    d['shopify_inventory_management'] = data['inventory_management']
    d['shopify_inventory_policy'] = data['inventory_policy']
    d['price'] = float(data['price'])
    d['compare_at_price'] = data.get('compare_at_price') or None
    d['taxable'] = data['taxable']

    d['weight_in_grams'] = 0 if data['grams'] is None else float(data['grams'])

    d['weight_in_lbs'] = round(d['weight_in_grams']/453.592,2)


    """
    STEP 3: Convert python dictionary into a tab-delimited string.
    """
    flat = '\t'.join([prepare_value(d.get(f, None)) for f in fields])
    
    return flat

def order_json_to_flat(data):

    """ 
    STEP 1: Define the columns you want in the exact order.
    """
    fields = ['order_id',
              'order_number',
              'customer_id',
              'email',
              'created_date_key',
              'updated_date_key',
              'ordered_date_key',
              'closed_date_key',
              'cancelled_date_key',
              'created_on',
              'updated_on',
              'ordered_on',
              'closed_on',
              'cancelled_on',
              'total_price',
              'total_line_items_price',
              'subtotal_price',
              'total_tax',
              'total_discounts',
              'total_shipping',
              'total_weight_in_grams',
              'total_weight_in_lbs',
              'currency',
              'credit_card_company',
              'payment_gateway',
              'financial_status',
              'fulfillment_status',
              'is_revenue',
              'used_discount_code,',
              'shipping_method',
              'shipping_first_name',
              'shipping_last_name',
              'shipping_phone_number',
              'shipping_address1',
              'shipping_address2',
              'shipping_city',
              'shipping_zip',
              'shipping_province',
              'shipping_province_code',
              'shipping_country',
              'shipping_country_code',
              'shipping_latitude',
              'shipping_longitude',
              'shipping_company',
              'billing_first_name',
              'billing_last_name',
              'billing_phone_number',
              'billing_address1',
              'billing_address2',
              'billing_city',
              'billing_zip',
              'billing_province',
              'billing_province_code',
              'billing_country',
              'billing_country_code',
              'billing_latitude',
              'billing_longitude',
              'billing_company',
              'shopify_landing_site',
              'shopify_landing_site_ref',
              'shopify_referring_site',
              'token']

    """ 
    STEP 2: Extract fields from JSON into python dictionary.
    """
    d = {}

    d['order_id'] = data['id']
    d['order_number'] = data['order_number']
    d['customer_id'] = data['customer']['id']

    dates = {
            'created': 'created_at',
            'updated': 'updated_at', 
            'ordered': 'created_at',
            'closed': 'closed_at', 
            'cancelled': 'cancelled_at'
            }

    d = assign_date_attributes(data, d, dates)

    d['total_price'] = data['total_price']
    d['total_line_items_price'] = data['total_line_items_price']
    d['subtotal_price'] = data['subtotal_price']
    d['total_tax'] = data['total_tax']
    d['total_discounts'] = data['total_discounts']
    d['total_shipping'] = data['shipping_lines'][0]['price']
    d['total_weight_in_grams'] = float(data['total_weight'])
    d['total_weight_in_lbs'] = round(data['total_weight']/453.592,2)
    d['currency'] = data['currency']
    d['financial_status'] = data['financial_status']
    if data['fulfillment_status'] != None:
        d['fulfillment_status'] = data['fulfillment_status']
    else:
        d['fulfillment_status'] = 'unfulfilled'
    d['shipping_method'] = data['shipping_lines'][0]['code']
    if data['fulfillment_status'] == 'fulfilled':
        d['is_revenue'] = 1
    else:
        d['is_revenue'] = 0

    s = data['shipping_address']
    d['shipping_first_name'] = s['first_name']
    d['shipping_last_name'] = s['last_name']
    d['shipping_phone_number'] = s['phone']
    d['shipping_address1'] = s['address1']
    d['shipping_address2'] = s['address2']
    d['shipping_city'] = s['city']
    d['shipping_zip'] = s['zip']
    d['shipping_province'] = s['province']
    d['shipping_province_code'] = s['province_code']
    d['shipping_country'] = s['country']
    d['shipping_country_code'] = s['country_code']
    d['shipping_latitude'] = float(s['latitude'])
    d['shipping_longitude'] = float(s['longitude'])
    d['shipping_company'] = s['company']

    b = data['billing_address']
    d['billing_first_name'] = b['first_name']
    d['billing_last_name'] = b['last_name']
    d['billing_phone_number'] = b['phone']
    d['billing_address1'] = b['address1']
    d['billing_address2'] = b['address2']
    d['billing_city'] = b['city']
    d['billing_zip'] = b['zip']
    d['billing_province'] = b['province']
    d['billing_province_code'] = b['province_code']
    d['billing_country'] = b['country']
    d['billing_country_code'] = b['country_code']
    d['billing_latitude'] = float(b['latitude'])
    d['billing_longitude'] = float(b['longitude'])
    d['billing_company'] = b['company']

    d['shopify_landing_site'] = data['landing_site']
    if data['landing_site_ref'] != None:
        d['shopify_landing_site_ref'] = data['landing_site_ref']
    else:
        d['shopify_landing_site_ref'] = 'N/A'
    if data['referring_site'] != '':
        d['shopify_referring_site'] = data['referring_site']
    else:
        d['shopify_referring_site'] = 'N/A'

    d['token'] = data['token']
    d['email'] = data['email']
    d['credit_card_company'] = data['payment_details']['credit_card_company']
    d['payment_gateway'] = data['gateway']
    
    if len(data['discount_codes']) > 0:
        d['used_discount_code'] = 1
    else:
        d['used_discount_code'] = 0

    """
    STEP 3: Convert python dictionary into a tab-delimited string.
    """
    flat = '\t'.join([prepare_value(d.get(f, None)) for f in fields])
    
    return flat

def order_line_json_to_flat(order, line):

    fields = ['order_line_id',
              'order_id',
               'product_id',
               'sku_id',
               'fulfillment_id',
               'customer_id',
               'ordered_date_key',
               'sku_code',
               'quantity',
               'price',
               'gross_extended_price',
               'net_extended_price',
               'weight_in_grams',
               'weight_in_lbs',
               'fulfillment_status',
               'fulfillment_service',
               'currency',
               'oh_financial_status',
               'oh_fulfillment_status',
               'oh_created_on',
               'oh_updated_on',
               'oh_ordered_on',
               'oh_closed_on',
               'oh_cancelled_on']

    d = {}

    d['order_line_id'] = line['id']
    d['order_id'] = order['id']
    d['product_id'] = line['product_id']
    d['sku_id'] = line['variant_id'] or "N/A"
    d['customer_id'] = order['customer']['id']

    d['fulfillment_id'] = 'N/A'
    for f in order['fulfillments']:
        for li in f['line_items']:
            if li['id'] == line['id']:
                d['fulfillment_id'] = f['id']

    ordered_dt = get_python_datetime_from_str(order['created_at'])
    d['ordered_date_key'] = get_datekey_from_datetime(ordered_dt)

    d['sku_code'] = line['sku']

    # Facts
    d['quantity'] = line['quantity']
    d['price'] = line['price']
    d['gross_extended_price'] = round(float(line['quantity']) * float(line['price']),2)
    d['net_extended_price'] = d['gross_extended_price']
    d['weight_in_grams'] = line['grams']
    d['weight_in_lbs'] = round(line['grams']/453.592,2)

    # Other
    d['fulfillment_status'] = line['fulfillment_status'] or "unfulfilled"
    d['fulfillment_service'] = line['fulfillment_service']
    d['currency'] = order['currency']

    d['oh_financial_status'] = order['financial_status']
    d['oh_fulfillment_status'] = order.get('fulfillment_status', 'unfulfilled')

    dates = {
            'oh_created': 'created_at',
            'oh_updated': 'updated_at', 
            'oh_ordered': 'created_at',
            'oh_closed': 'closed_at', 
            'oh_cancelled': 'cancelled_at'
            }

    d = assign_date_attributes(order, d, dates)

    """
    STEP 3: Convert python dictionary into a tab-delimited string.
    """
    flat = '\t'.join([prepare_value(d.get(f, None)) for f in fields])
    
    return flat    

def get_python_datetime_from_str(dt):
    offset = dt[-6:]
    return datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S' + offset)

def get_datekey_from_datetime(dt):
    return str(dt.year) + two_digit(dt.month) + two_digit(dt.day)

def two_digit(integer):
    if integer < 10:
        return '0' + str(integer)
    else:
        return str(integer)

def prepare_value(x):
    if x == None:
        return '\N'
    elif type(x) == int:
        return str(x)
    elif type(x) == float:
        return str(x)
    elif type(x) == long:
        return str(x)
    elif type(x) == bool:
        return str(x)
    else:
        return x.encode('utf-8')

def assign_date_attributes(data_src, data_dict, dates):
    for date_type, src_field in dates.iteritems():

        src_key_exists = src_field in data_src.keys()

        if src_key_exists and data_src[src_field]:
            python_dt = get_python_datetime_from_str(data_src[src_field])
            data_dict['%s_date_key' % date_type] = get_datekey_from_datetime(python_dt)
            data_dict['%s_on' % date_type] = python_dt.strftime('%Y-%m-%d %H:%M:%S')
        else:
            data_dict['%s_date_key' % date_type] = "0"
            data_dict['%s_on' % date_type] = None

    return data_dict

if __name__ == '__main__':
    process_file(sys.argv[1], sys.argv[2])