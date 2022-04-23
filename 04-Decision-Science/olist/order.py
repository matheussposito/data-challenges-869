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
        pass  # YOUR CODE HERE

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        pass  # YOUR CODE HERE

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        pass  # YOUR CODE HERE

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        pass  # YOUR CODE HERE

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
        pass  # YOUR CODE HERE
