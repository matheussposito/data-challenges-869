import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """
        # Hint: Within this instance method, you have access to the instance of the
        # class Order in the variable self, as well as all its attributes
        orders = self.data['orders'].copy()
        orders = orders[orders['order_status'] == 'delivered'][[
            'order_id', 'order_status', 'order_purchase_timestamp',
            'order_delivered_customer_date', 'order_estimated_delivery_date'
        ]]

        # deal with datetime
        orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
        orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
        orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

        # compute wait time
        orders['wait_time'] = (
            orders['order_delivered_customer_date'] -
            orders['order_purchase_timestamp']) / np.timedelta64(24, 'h')

        # compute expected wait time
        orders['expected_wait_time'] = (orders['order_estimated_delivery_date']\
            - orders['order_purchase_timestamp']) / np.timedelta64(24, 'h')

        # compute delay vs expected
        orders['delay_vs_expected'] = ((orders['order_delivered_customer_date']\
            - orders['order_estimated_delivery_date'])\
            /np.timedelta64(24, 'h')) \
            .apply(lambda x: x if x > 0 else 0)

        return orders[['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']]

    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        reviews = self.data['order_reviews'][['order_id',
                                              'review_score']].copy()

        reviews['dim_is_five_star'] = reviews['review_score']\
            .apply(lambda x: 1 if x == 5 else 0)
        reviews['dim_is_one_star'] = reviews['review_score']\
            .apply(lambda x: 1 if x == 1 else 0)

        return reviews


    def get_number_products(self):
        """
        Returns a DataFrame with:
        order_id, number_of_products
        """
        products = self.data['order_items'][['order_id', 'product_id']].copy()
        products = products.groupby('order_id', as_index=False).count().rename(
            {
                'product_id': 'number_of_products'
            }, axis=1)
        return products

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        sellers = self.data['order_items'][['order_id', 'seller_id']].copy()
        sellers = sellers.groupby('order_id', as_index=False).nunique().rename(
            {
                'seller_id': 'number_of_sellers'
            }, axis=1)
        return sellers

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        prices = self.data['order_items'][[
            'order_id', 'price', 'freight_value'
        ]].copy()
        prices = prices.groupby('order_id', as_index=False).sum()
        return prices

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        # geo data
        geo = self.data['geolocation'][['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng']].copy().rename({'geolocation_zip_code_prefix': 'zipcode'}, axis=1)
        geo = geo.groupby('zipcode', as_index=False).first()

        # get order_id and customer_id
        orders_customers = self.data['orders'][['order_id', 'customer_id']].copy()

        # get order_id and seller_id
        orders_sellers = self.data['order_items'][['order_id', 'seller_id']].copy()

        # merge a df that contains order_id, customer_id and seller_id
        orders_merged = orders_customers.merge(orders_sellers, on='order_id')

        # get seller location info
        sellers_loc = self.data['sellers'][['seller_id', 'seller_zip_code_prefix']].copy().rename({'seller_zip_code_prefix': 'zipcode'}, axis=1)\
            .merge(geo, on='zipcode').drop(columns='zipcode').rename({'geolocation_lat': 'seller_lat', 'geolocation_lng': 'seller_lng'}, axis=1)

        # get customer location info
        customers_loc = self.data['customers'][['customer_id', 'customer_zip_code_prefix']].copy().rename({'customer_zip_code_prefix': 'zipcode'}, axis=1)\
            .merge(geo, on='zipcode').drop(columns='zipcode').rename({'geolocation_lat': 'customer_lat', 'geolocation_lng': 'customer_lng'}, axis=1)

        # merge the df with the ids to the dfs with the location info
        orders_seller_customer = orders_merged.merge(
            sellers_loc, on='seller_id').merge(
                customers_loc,
                on='customer_id').drop(columns=['customer_id', 'seller_id'])

        # apply the harversine distance function
        orders_seller_customer.loc[:,'distance_seller_customer'] = orders_seller_customer.apply(\
            lambda x: haversine_distance(x['seller_lng'], x['seller_lat'], x['customer_lng'], x['customer_lat']), axis=1)

        # groupby and take the mean for order_id (one order may have more than one seller)
        orders_seller_customer = orders_seller_customer[[
            'order_id', 'distance_seller_customer']].groupby('order_id', as_index=False).mean()

        return orders_seller_customer

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_products', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        wait_df = self.get_wait_time()
        review_df = self.get_review_score()
        product_df = self.get_number_products()
        seller_df = self.get_number_sellers()
        price_df = self.get_price_and_freight()
        distance_df = self.get_distance_seller_customer()

        if with_distance_seller_customer:
            df = wait_df.merge(review_df).merge(product_df).merge(seller_df)\
                .merge(price_df).merge(distance_df)
            return df.dropna()

        df = wait_df.merge(review_df).merge(product_df).merge(seller_df).merge(price_df)
        return df.dropna()
