from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color, Line
from kivy.clock import Clock
from functools import partial
import RPi.GPIO as GPIO
from picamera import PiCamera
import zbarlight

import math
import time
import page_start
import page_selection
import shared_values
import popup
import qr
import lnd_rest
import acceptor


class PaymentPage(FloatLayout):
    """Creates a page, which inherits from FloatLayout. FloatLayout is one of several classes for pages. Here
    the position on each widget or thing can be freely chosen, which makes everything very flexible. This
    class handles most of the payment process with lnd and presents page which different widgets, labels and so on."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """The method initiates the whole layout and some basic variables. If this method doesn't end nothing
        is shown"""

        # sets instance values for safety reasons
        self.fiat = 0
        self.btcprice = 0
        self.btcprice_fee = 0
        self.satprice = 0
        self.satprice_fee = 0

        # necessary to differentiate, how the popup is closed later
        # if the value is True a payment will be initiated, if it's False no payment or qr scanning will occur
        self.payment_value = False

        # creates the three rounded rectangles
        with self.canvas:
            # RGB value
            Color(1, 1, 1)
            # creates a rounded rectangle by drawing a line
            # rounded_rectangle = x, y, width, height, corner radius, resolution
            # width = width of the line
            Line(rounded_rectangle=(250, 150, 300, 200, 30, 50),
                 width=2)

        with self.canvas:
            Color(1, 1, 1)
            Line(rounded_rectangle=(20, 20, 760, 370, 30, 50),
                 width=2)

        with self.canvas:
            Color(1, 1, 1)
            Line(rounded_rectangle=(198, 405, 420, 60, 20, 50),
                 width=2)

        # creates a label and puts it in instance variable
        # pos_hint = is a relative position --> 0 is 0% , 1 is 100% --> 0,0 is bottom left !!!
        self.label_top = Label(text="LIGHTING ATM",
                               pos_hint={'center_x': 0.5, 'center_y': 0.9},
                               font_size=45)
        # the label has to be added to main widget, which is the page actually
        self.add_widget(self.label_top)

        # same as above
        self.label_main = Label(text="Start",
                                pos_hint={'center_x': 0.5, 'center_y': 0.53},
                                font_size=25)
        self.add_widget(self.label_main)

        # button is created nearly the same as the label
        # size_hint = is the size relatively to the parent widget, which is the page actually
        # the size is fixed in here, so even if you resize the screen, the buttons should be the same size
        # if min and max are not set, the size will change, if the parent size changes
        # home button is mostly for changing the page to the start page
        self.button_home = Button(text="Home",
                                  size_hint=(0.2, 0.1),
                                  size_hint_min_x=150,
                                  size_hint_min_y=60,
                                  size_hint_max_x=150,
                                  size_hint_max_y=60,
                                  pos_hint={'top': 0.98, 'right': 0.2},
                                  font_size=33)
        # binds the button to a method, so every time the button is clicked, the method is called
        self.button_home.bind(on_press=self.home_button)
        # the button has to be added to the main widget
        self.add_widget(self.button_home)

        # same as above
        # back button is mostly for going one page back
        self.button_back = Button(text="Back",
                                  size_hint=(0.2, 0.1),
                                  size_hint_min_x=150,
                                  size_hint_min_y=60,
                                  size_hint_max_x=150,
                                  size_hint_max_y=60,
                                  pos_hint={'top': 0.98, 'right': 0.99},
                                  font_size=33)
        self.button_back.bind(on_press=self.back_button)
        self.add_widget(self.button_back)

        # same as above
        # starts the process of money input
        self.button_start = Button(text="Start",
                                   size_hint=(0.2, 0.1),
                                   size_hint_min_x=150,
                                   size_hint_min_y=60,
                                   size_hint_max_x=150,
                                   size_hint_max_y=60,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.2},
                                   font_size=33)
        self.button_start.bind(on_press=self.start_button)
        self.add_widget(self.button_start)

        # starts a scheduled process, which calls the method before the next frame (-1)
        Clock.schedule_once(self.show_btc_price, -1)

    def home_button(self, *args):
        # clears everything for next user
        self.soft_reset()

        # changes page to main page
        App.get_running_app().screenmanager.current = 'MainPage'

    def back_button(self, *args):
        # clears everything for next user
        self.soft_reset()

        # changes page to selection page
        App.get_running_app().screenmanager.current = 'SelectionPage'

    def show_btc_price(self, *args):
        """Showing the price in the middle of the screen"""
        print('start btc price method')
        # if setting values take to long this is shown in the middle of the screen
        # never saw this happened
        self.label_main.text = "Processing..."

        # takes the values from the shared_values file
        self.btcprice = shared_values.SharedValues.get_BTCPRICE()
        self.btcprice_fee = shared_values.SharedValues.BTCPRICE_FEE
        self.satprice = shared_values.SharedValues.SATPRICE
        self.satprice_fee = shared_values.SharedValues.SATPRICE_FEE

        # changes the main label to present the rate
        # .2f --> float variable with two decimal places
#        self.label_main.text = f"Rate:\n" \
#                               f"{self.btcprice: .2f} Euro/BTC\n  -  " \
#                               f"{self.satprice: .3f} Cent/Sat\n\n" \
#                               f"Our Rate:\n" \
#                               f"{self.btcprice_fee: .2f} Euro/BTC\n  -  " \
#                               f"{self.satprice_fee: .3f} Cent/Sat"

        self.label_main.text = f"\nRate:\n" \
                               f"{self.btcprice_fee: .2f} Euro/BTC\n" \
                               f"{self.satprice_fee: .3f} Cent/Sat\n\n"


    #    def set_payment_value(self, value):
    #        self.payment_value = value

    def start_button(self, *args):
        """Starts the process of coin input by creating a popup and schedule some events. It also saves the current
        btcprice to the shared_values file, so there is no difference during coin input"""
        print('start start method')

        # set initial value
        self.payment_value = False

        print('creates popup')
        # create a popup from the class P
        # auto_dismiss prevents closing the popup by clicking beside the window
        self.popups = popup.P(title='Put your coins in', size_hint=(None, None), size=(300, 400), auto_dismiss=False)

        # to open the popup
        self.popups.open()
        print('popup created and opened')

        print('create label update schedule')
        # creates a scheduled event, which updates the label of the popup every second
        # therefore every second the method update_label from the popup is called
        self.popup_event = Clock.schedule_interval(self.popups.update_label, 1)

        print('create monitor coins schedule')
        # creates a scheduled event, which monitors pulses from the coin acceptor
        # therefore every second the method monitor_coins from the acceptor file is called
        self.event2 = Clock.schedule_interval(acceptor.CoinAcceptor.monitor_coins, 1)

        # sets the current btcprice
        shared_values.SharedValues.set_current_BTCPRICE(self.btcprice_fee)
        print(shared_values.SharedValues.get_current_BTCPRICE())

        # if the popup closes, the method clean_popup will be called
        self.popups.bind(on_dismiss=self.clean_popup)

    def clean_popup(self, *args):
        """Cancels the scheduled events and starts a new method"""
        print('clean_popup method started')

        # cancels the label update event and the monitoring event of the coin acceptor
        self.popup_event.cancel()
        self.event2.cancel()
        print('events canceled')

        # calls method for decision
        self.pay_or_not()

    def pay_or_not(self, *args):
        """Is responsible for whether a payment take place or not. This is because the popup has two buttons, one for
        canceling the process and one for getting payed. To decide which one was pressed, this procedure is
        necessary"""
        print('pay_or_not method called')

        # request the payment canceled value from the shared_value file
        self.payment_canceled = shared_values.SharedValues.get_payment_canceled()

        # if the payment_canceled value is False, the payment will be initiated
        if self.payment_canceled == False and shared_values.SharedValues.get_current_SATS() > 0:
            self.prepare_payment()
        else:
            print('Cancel payment')

    def prepare_payment(self, *args):
        """Just for winning some time and maybe for future use"""
        print('prepare payment method is called')

        # schedules an event once
        # the do_payment method is called after 2 seconds
        Clock.schedule_once(self.do_payment, 2)

        # updates the main_label with the current number of the satoshis
        self.label_main.text = f"Show me Invoice with\n\n" \
                               f"{math.floor(shared_values.SharedValues.get_current_SATS())} Sat\n\n"

    def do_payment(self, *args):
        """Handles the whole payment process, including scanning qr-code, evaluating the qr-code and handle
        the invoice"""
        print('do_payment function called')

        # scans a qr-code and returns either the qr-code or False
        qrcode = qr.QrCode.scan()

        # takes the qr-code and checks if a lightning invoice is in it
        # if this is the case the invoice variable from shared_values is set
        shared_values.SharedValues.INVOICE = lnd_rest.LndRest.evaluate_scan(qrcode)

        # creates a counter for the while loop
        self.counter = 0

        # if no invoice was presented do it again
        while shared_values.SharedValues.INVOICE is False:
            print(f'Round: {self.counter + 1}')

            # same as above
            qrcode = qr.QrCode.scan()

            # same as above
            shared_values.SharedValues.INVOICE = lnd_rest.LndRest.evaluate_scan(qrcode)

            # increases the counter
            self.counter += 1

            # if the counter reaches the number 3 (the process was called 3 times), the while loop ends
            if self.counter == 3:
                self.label_main.text = f"Maybe next time"

                # stops all processes for 2 seconds
                time.sleep(2)
                break

        # if a valid qr-code was presented and a invoice was detected the handling invoice method is called
        if self.counter < 3:

            # if the handling invoice method was successful the value True is presented and the process ends
            if lnd_rest.LndRest.handle_invoice():

                # updates main label
                self.label_main.text = "Thank you!"

            # the handling invoice method presented the False value
            else:
                # updates main label
                self.label_main.text = "Error during decoding"

            # initiates clean up of all important parameters
            Clock.schedule_once(self.soft_reset, 10)

        # if no qr-code was presented and scanning fails go back to MainPage
        else:
            self.soft_reset()

    def soft_reset(self, *args):
        """If the payment process ends, successful or not, all important values were reset and the start
        screen will be shown"""
        print('soft_reset method called')

        # reset screen
        self.show_btc_price()

        # clears fiat value, so the next person can insert coins again
        shared_values.SharedValues.set_FIAT(0)
        print('FIAT: ' + str(shared_values.SharedValues.get_FIAT()))

        # reset payment_canceled value in the shared_values file
        shared_values.SharedValues.set_payment_canceled(True)

        # changes screen to the main_screen
        App.get_running_app().screenmanager.current = 'MainPage'
        # cleanup needed
