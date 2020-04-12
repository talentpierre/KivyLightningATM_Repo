import requests
import math
import time
import os
import os.path
import logging
import sys


class SharedValues:
    """This class is mostly for shared values between classes or general values. Most of the are changed or
    requested by getter and setter methods. If you run your own atm you have to provide some credentials like
    BTCPAY-Server-rest-api path and your admin macaroon in hex format"""

    # PLACE YOUR CREDENTIALS HERE
    # this path is placed at BTCPAY-Server --> maintenance --> services --> rest-service --> click here
    # if 'v1' is not at the end, you have to add it manually
    BTCPAY_URL = ''

    # admin macaroon in hex format
    LND_MACAROON = ''

    # important for the coin acceptor
    # if a coin is inserted this value changes
    FIAT = 0

    #CURRENT_FIAT = 0

    # if a payment process starts, this price will be set so no changes in price will occur during coin input
    # value is set to 1 because the CURRENT_SATS value executes a divide by zero
    CURRENT_BTCPRICE = 1

    # calculates the number of satoshis, which will be payed
    CURRENT_SATS = math.floor((FIAT * 100000000) / CURRENT_BTCPRICE)

    # requests see btcprice rate from opennode
    # because opennode provides a lot of data, it is specified which is needed
    BTCPRICE = requests.get('https://api.opennode.co/v1/rates').json()['data']['BTCEUR']['EUR']

    # calculates the btcprice with some fee --> e.g. transaction fee, fee for buying
    BTCPRICE_FEE = BTCPRICE * 1.01

    # calculates satprice
    SATPRICE = (BTCPRICE * 100) / 100000000

    # calculates sats with fee
    SATPRICE_FEE = SATPRICE * 1.05

    # the invoice, which provided by the qr-code is placed here
    # it is mainly used by lnd_rest file
    INVOICE = ''

    payment_canceled = True

    ATM_data_dir = ''

    @staticmethod
    def create_directory():
        home = os.path.expanduser("~")
        SharedValues.ATM_data_dir = home + "/.lightningATM/"
        if not os.path.exists(SharedValues.ATM_data_dir):
            os.makedirs(SharedValues.ATM_data_dir)

    @staticmethod
    def get_FIAT():
        return SharedValues.FIAT

    @staticmethod
    def get_BTCPRICE():
        return SharedValues.BTCPRICE

    @staticmethod
    def get_BTCPRIC_FEE():
        return SharedValues.BTCPRICE_FEE

    @staticmethod
    def get_SATPRICE():
        return SharedValues.SATPRICE

    @staticmethod
    def get_current_FIAT():
        return SharedValues.CURRENT_FIAT

    @staticmethod
    def get_current_BTCPRICE():
        return SharedValues.CURRENT_BTCPRICE

    @staticmethod
    def get_INVOICE():
        return SharedValues.INVOICE

    @staticmethod
    def get_BTCPAY_URL():
        return SharedValues.BTCPAY_URL

    @staticmethod
    def get_LND_MACAROON():
        return SharedValues.LND_MACAROON

    @staticmethod
    def get_current_SATS():
        return SharedValues.CURRENT_SATS

    @staticmethod
    def get_payment_canceled():
        return SharedValues.payment_canceled

    @staticmethod
    def set_FIAT(value):
        SharedValues.FIAT = value

    @staticmethod
    def set_BTCPRICE(value):
        SharedValues.BTCPRICE = value

    @staticmethod
    def set_BTCPRIC_FEE(value):
        SharedValues.BTCPRICE_FEE = value

    @staticmethod
    def set_SATPRICE(value):
        SharedValues.SATPRICE = value

    @staticmethod
    def get_SATPRICE_FEE(value):
        SharedValues.SATPRICE_FEE = value

    @staticmethod
    def set_current_FIAT(value):
        SharedValues.CURRENT_FIAT = value

    @staticmethod
    def set_current_BTCPRICE(value):
        SharedValues.CURRENT_BTCPRICE = value

    @staticmethod
    def set_INVOICE(value):
        SharedValues.INVOICE = value

    @staticmethod
    def set_BTCPAY_URL(value):
        SharedValues.BTCPAY_URL = value

    @staticmethod
    def set_LND_MACAROON(value):
        SharedValues.LND_MACAROON = value

    @staticmethod
    def set_current_SATS(value):
        SharedValues.CURRENT_SATS = value

    @staticmethod
    def set_payment_canceled(value):
        SharedValues.payment_canceled = value
