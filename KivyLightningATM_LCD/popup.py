from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
import RPi.GPIO as GPIO

from PIL import Image
from io import BytesIO
from picamera import PiCamera
import zbarlight

import math
import time
import os
import os.path
import sys

import app
import page_start
import page_selection
import shared_values
import acceptor


class P(Popup):
    """Creates a kind of window, which inherits from Popup. The window is some different attributes like poping up
    in front of an existing page. This class handles most of the coin input process"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """The method initiates the whole layout and some basic variables. If this method doesn't end nothing
        is shown"""
        print('create popup')

        # because of p inherits from popup, it has fixed number of widgets, which can be added. therefore we create
        # a kind of page inside it which inherits from floatlayout, which is way more flexible
        layout = FloatLayout()

        # creates a label and puts it in instance variable
        # pos_hint = is a relative position --> 0 is 0% , 1 is 100% --> 0,0 is bottom left !!!
        self.top_label = Label(text=f"Deposit:",
                               size_hint=(0.28, 0.4),
                               pos_hint={'x': 0.01, 'y': 0.7},
                               font_size=30,
                               underline=True)

        # same as above
        self.value_label = Label(text="",
                                 size_hint=(0.4, 0.4),
                                 pos_hint={'x': 0.05, 'center_y': 0.5},
                                 font_size=30)

        # button is created nearly the same as the label
        # size_hint = is the size relatively to the parent widget, which is the 'layout' actually
        # the pay button is for initiating the payment process and for closing the popup
        self.pay_button = Button(text="GET PAYED",
                                 size_hint=(0.60, 0.1),
                                 pos_hint={'x': 0.01, 'y': 0.05},
                                 font_size=25)
        # binds the button to a method, so every time the button is clicked, the method is called
        # which is exactly one time because the after clicking the popup closes
        self.pay_button.bind(on_press=self.button_pay)

        # same as above
        # the button cancels the payment process
        self.close_button = Button(text="X",
                                   size_hint=(0.34, 0.1),
                                   pos_hint={'x': 0.65, 'y': 0.05},
                                   font_size=25)
        self.close_button.bind(on_press=self.button_close)

        # because only one widget can be added to the popup, all widget will be added to a layout widget
        layout.add_widget(self.top_label)
        layout.add_widget(self.close_button)
        layout.add_widget(self.pay_button)
        layout.add_widget(self.value_label)

        # here the one widget is added to the popup
        self.add_widget(layout)

    def setup_monitoring(self, *args):
        '''starts a process of calling the monitor button method every 0.2 seconds'''

        # because the status of the buttons has to be checked constantly, an event is initialized
        # the monitor button function will be called every 0.2 seconds to check if a button was pressed
        self.button_event = Clock.schedule_interval(self.monitor_button, 0.2)

    def monitor_button(self, *args):
        '''checks if and what button was pressed'''

        # to avoid double clicking it will only check if a button was pressed after 2 seconds since the last
        # button push
        # time.time() returns the current time in seconds since unix time
        # this value is compared with the time of the last push plus 2 seconds
        if time.time() > (shared_values.SharedValues.last_push + 2):
            # checks if button1 was pressed and calls the method from the acceptor file
            acceptor.CoinAcceptor.set_button1_pressed()

            # checks if button1 was pressed and calls the method from the acceptor file
            acceptor.CoinAcceptor.set_button2_pressed()

            # if button1 was pressed this value equals true and the if condition is entered
            if shared_values.SharedValues.button1_pressed:
                # cancels the calling of the monitor button method
                self.button_event.cancel()

                # sets the control value to false for the next usage of the button
                shared_values.SharedValues.button1_pressed = False

                # sets the time for the last button push, which will be checked during the next button press
                shared_values.SharedValues.last_push = time.time()

                # calls the pay method to continue with payment process
                self.button_pay()

            # if button1 wasn't pressed it checks button 2
            elif shared_values.SharedValues.button2_pressed:
                # same as above
                self.button_event.cancel()

                # same as above
                shared_values.SharedValues.button2_pressed = False

                # same as above
                shared_values.SharedValues.last_push = time.time()

                # calls the closing method to cancel the payment process
                self.button_close()

    def button_close(self, *args):
        print('button close method')

        # sets the payment_canceled value in the shared_value file to True
        # so it's known that the payment was canceled
        shared_values.SharedValues.set_payment_canceled(True)

        # closes the popup
        self.dismiss()

    def button_pay(self, *args):
        print('button pay method')

        # sets the payment_canceled value in the shared_value file to False
        # so it's known that the payment can be initiated
        shared_values.SharedValues.set_payment_canceled(False)

        # closes the popup
        self.dismiss()

    def update_label(self, *args):
        """This method updates the main label, which shows the current amount inserted into the coin acceptor
        Also it sets the number of satoshis which have to be paid later"""
        print('update label called')

        # gets the fiat value from the shared_value file
        # the amount will be regularly updated and set by the coin acceptor
        self.fiat = shared_values.SharedValues.get_FIAT()

        # sets the current number of satoshis in the shared_value file
        # this is an important value because the payment refers to it
        shared_values.SharedValues.set_current_SATS(
            math.floor((self.fiat * 100000000) / shared_values.SharedValues.get_current_BTCPRICE()))

        # updates the label
        # .2f --> presented as a float number with 2 decimal places
        self.value_label.text = f"FIAT: {self.fiat:.2f} Eur\n\n" \
                                f"SATOSHIS: {math.floor(shared_values.SharedValues.get_current_SATS())} Sat"

        print('update popup ' + str(math.floor(shared_values.SharedValues.get_current_SATS())))
