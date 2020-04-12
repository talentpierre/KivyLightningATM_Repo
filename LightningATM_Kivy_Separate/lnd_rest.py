import json
import requests
import math
import shared_values



class LndRest:
    class InvoiceDecodeError(BaseException):
        """This is currently under construction and not used. It will handle future exceptions"""
        def __init__(self, **kwargs):
            super().__init__()
            pass

    @staticmethod
    def payout(amt, payment_request):
        """This method attempts to pay the BOLT11 invoice using BTCPAY-Server at this time.
        Therefore the Rest-Api of BTCPAY-Server and the admin-macaroon is used"""

        print('payout method')
        # creates the rest-api-url using the basic BTCPAY_URL from the shared_value file and an additional string
        # which contains the correct position
        url = shared_values.SharedValues.get_BTCPAY_URL() + "/channels/transactions"

        # data over the wire is mostly sent in json format. Therefore a dictionary is created first,
        # to paste it later into the request. The values/parameters are given by the method call.
        data = {
            "payment_request": payment_request,
            "amt": math.floor(amt),
        }
        print('data dictionary created')

        # sends a post request to BTCPAY-Server using the url defined above, a header which contains
        # the admin-macaroon in Hex format from your BTCPAY-Server Node and the data defined above.
        # the direct response from the server is stored in the variable 'response'
        print('send request for payout')
        response = requests.post(
            url,
            headers={"Grpc-Metadata-macaroon": shared_values.SharedValues.get_LND_MACAROON()},
            data=json.dumps(data),
        )
        print('got response for payout')
        # the response is sent in a different format, therefore it is converted into json object i guess
        res_json = response.json()

        # checks if the response contains a error message and prints it
        if res_json.get("payment_error"):
            errormessage = res_json.get("payment_error")
            print("Error: " + str(errormessage))

    @staticmethod
    def last_payment(payment_request):
        """Returns whether the last payment attempt succeeded or failed and takes payment_request as
        an argument."""

        print('last payment method')
        # same procedure as in payout_method above
        url = shared_values.SharedValues.get_BTCPAY_URL() + "/payments"

        # same procedure as in payout_method above
        data = {
            "include_incomplete": True,
        }
        print('data dictionary created')

        print('send request for last_payment')
        # same procedure as in payout_method above
        response = requests.get(
            url,
            headers={"Grpc-Metadata-macaroon": shared_values.SharedValues.get_LND_MACAROON()},
            data=json.dumps(data),
        )
        print('got response for last_payment')

        # same procedure as in payout_method above
        json_data = response.json()

        # because their are a lot of values inside the response, we only take the part payments of it
        payment_data = json_data["payments"]

        # this means from all the payments data we only take the last entry. therefore -1
        _last_payment = payment_data[-1]

        # checks if the last payment request matches our payment request and if the status of this payment request
        # is succeeded. if both conditions are true the payment has succeeded and the user got their satoshis.
        # the caller gets a true or false value
        if (_last_payment["payment_request"] == payment_request) and (
                _last_payment["status"] == "SUCCEEDED"
        ):
            print("Payment succeeded")
            return True
        else:
            print("Payment failed")
            return False

    @staticmethod
    def decode_request(payment_request):
        """The method takes the BOLT11 Invoice from the shared_values file and decodes it, by sending it to
        the BTCPAY-Server and getting the details from inside through the response. The method returns 0 for
        invoices below 20000 satoshis or the number of satoshis given by the invoice"""

        print('start decoding')

        #if an invoice exists
        if payment_request:
            print('if_payment_request')

            # same procedure as in payout_method above, but this time the invoice as a string is added
            url = shared_values.SharedValues.get_BTCPAY_URL() + "/payreq/" + str(payment_request)

            print('send request for payment_request')
            # same procedure as in payout_method above
            response = requests.get(
                url,
                headers={"Grpc-Metadata-macaroon": shared_values.SharedValues.get_LND_MACAROON()}
            )
            print('got response for payment_request')

            # status_code 200 refers to a successful response, therefore if it's not 200 the exception handler
            # raises an exeption. this is actually not implemented. Only a status code error will be printed
            if response.status_code != 200:
                # raise InvoiceDecodeError(
                # "Invoice {} got bad decode response {}".format(
                #   payment_request, response.text
                # )
                # )
                print('status code error')

            # same procedure as in payout_method above
            json_data = response.json()

            # this is a little bit tricky because a zero sat invoice starts with lnbc1 and every invoice below
            # 20000 sat do as well. this is a little tradeoff, we have to deal with at the moment
            if "lnbc1" in payment_request:
                print("invoice below 20000")
                return 0
            else:
                # if the invoice is above 20000 satoshi the number of satoshis is taken from the data received earlier
                print(int(json_data["num_satoshis"]))
                return int(json_data["num_satoshis"])
        else:
            pass

    @staticmethod
    def handle_invoice():
        """Decodes a BOLT11 invoice. Ensures that amount is correct or 0, then attempt to
        make the payment. The method returns True or False in dependence of the payment attempt was successful
        or not"""

        print('start handle invoice')
        print(shared_values.SharedValues.INVOICE)
        # decode_req contains the number of satoshis for the payment and takes the invoice from the shared_values
        # file
        decode_req = LndRest.decode_request(shared_values.SharedValues.INVOICE)
        # if the amount is inside the current_sats value in the shared_value file, the payout is initiated
        if decode_req in (math.floor(shared_values.SharedValues.get_current_SATS()), 0):
            print('in payout')
            # initiates payout
            LndRest.payout(shared_values.SharedValues.get_current_SATS(), shared_values.SharedValues.INVOICE)
            # calls the last_payment method and gets a true or false value in dependence of the status of the payment
            result = LndRest.last_payment(shared_values.SharedValues.INVOICE)

            #checks the result
            if result is True:
                return True
            else:
                print('Error during decode')
                return False
        else:
            print("Please show correct invoice")

    @staticmethod
    def evaluate_scan(qrcode):
        """Gets a qr-code as a parameter and checks it for a lightning invoices. The key value for the search is
        lnbc, which indicates a lightning invoice exists. The method returns either False if no lightning
        invoice is found or the invoice if it is found"""

        print('start evaluating qrcode')
        # if qr-code has no value the method returns false
        if not qrcode:
            print('scanning failed')
            return False
        # check for a lightning invoice
        else:
            # looks for 'lnbc' in the qr-code, where all characters are lower case after the conversion
            if "lnbc" in qrcode.lower():
                print('Invoice detected')
                invoice = qrcode.lower()

                # because the qr-code format differs, it's possible that the decoded qr-code contains 'lightning'
                # in front of the string
                # if invoice preceded with "lightning:" then chop it off so that we can
                # handle it correctly
                if "lightning:" in invoice:
                    invoice = invoice[10:]
                return invoice
            else:
                print('Error during evaluating - no lightning included')
                return False

