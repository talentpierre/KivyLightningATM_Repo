from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color, Line
import RPi.GPIO as GPIO
from picamera import PiCamera
import zbarlight
import app
import page_start
import page_lnd_payment
import page_lnurl_payment
import shared_values
import acceptor
import master_layout
import time
from kivy.clock import Clock


class SelectionPage(FloatLayout):
    """Creates a page, which inherits from FloatLayout. FloatLayout is one of several classes for pages. Here
    the position on each widget or thing can be freely chosen, which makes everything very flexible. This
    class handles the variety of payment methods, which is at the moment BOLT11 invoice and lnurl, where
    lnurl is under construction"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """The method initiates the whole layout and some basic variables. If this method doesn't end nothing
        is shown"""

        # this creates a layout from the master_layout file, including background and lines
        self.master_layout2 = master_layout.MasterLayout()
        # the layout has to be added to the main widget
        self.add_widget(self.master_layout2)

        # creates a label and puts it in instance variable
        # pos_hint = is a relative position --> 0 is 0% , 1 is 100% --> 0,0 is bottom left !!!
        # color is set by red, green, blue, opacity --> 0 means 0 and 1 means 255
        self.label_main = Label(text="SELECTION PAGE",
                                pos_hint={'center_x': 0.5, 'center_y': 0.6},
                                font_size=40,
                                color=(0, 0, 0, 1))
        # the label has to be added to main widget, which is the page actually
        self.add_widget(self.label_main)

        # button is created nearly the same as the label
        # size_hint = is the size relatively to the parent widget, which is the page actually
        # pos_hint is the same as above
        # HOME button is for changing to the home screen, but has no real function here because no touchscreen is used
        # it's used because of an easy way to implement a rectangle with a label in it
        self.button_HOME = Button(text="HOME",
                                  size_hint=(0.2, 0.1),
                                  pos_hint={'top': 0.17, 'right': 0.93},
                                  background_color=(0, 0, 0, 1),
                                  color=(0.8, 1, 1, 1),
                                  font_size=30)
        self.button_HOME.bind(on_press=self.home_button)
        self.add_widget(self.button_HOME)

        # same as above
        # would change the page to the lndpayment page
        self.button_LND = Button(text="LND",
                                 size_hint=(0.2, 0.1),
                                 pos_hint={'top': 0.17, 'right': 0.72},
                                 background_color=(0, 0, 0, 1),
                                 color=(0.8, 1, 1, 1),
                                 font_size=30)
        self.button_LND.bind(on_press=self.lnd_button)
        self.add_widget(self.button_LND)

    def home_button(self, *args):
        # would change to the home screen
        # not in use because there is no touchscreen
        App.get_running_app().screenmanager.current = 'MainPage'

    def lnd_button(self, *args):
        # would change to the lndpayment screen
        # not in use because there is no touchscreen
        App.get_running_app().screenmanager.current = 'PaymentPage'

    def setup_monitoring(self, *args):
        '''starts a process of calling the monitor button method every 0.2 seconds'''

        # because the status of the buttons has to be checked constantly, an event is initialized
        # the monitor button function will be called every 0.2 seconds to check if a button was pressed
        self.button_event = Clock.schedule_interval(self.monitor_button, 0.2)

    def monitor_button(self, *args):
        '''checks if and what button was pressed'''
        print('\t2')
        # to avoid double clicking it will only check if a button was pressed after 2 seconds since the last
        # button push
        # time.time() returns the current time in seconds since unix time
        # this value is compared with the time of the last push plus 2 seconds
        if time.time() > (shared_values.SharedValues.last_push + 2):
            # checks if button1 was pressed and calls the method from the acceptor file
            acceptor.CoinAcceptor.set_button1_pressed()

            # checks if button2 was pressed and calls the method from the acceptor file
            acceptor.CoinAcceptor.set_button2_pressed()

            # if button1 was pressed this value equals true and the if condition is entered
            if shared_values.SharedValues.button1_pressed:
                # cancels the calling of the monitor button method
                self.button_event.cancel()

                # sets the control value to false for the next usage of the button
                shared_values.SharedValues.button1_pressed = False

                # changes the page to the lndpayment screen
                App.get_running_app().screenmanager.current = 'PaymentPage'

                # calls the monitoring method of the next page, which checks the button status again
                App.get_running_app().paymentpage.setup_monitoring()

                # sets the time for the last button push, which will be checked during the next button press
                shared_values.SharedValues.last_push = time.time()

            # if button1 wasn't pressed it checks button 2
            elif shared_values.SharedValues.button2_pressed:
                # same as above
                self.button_event.cancel()

                # same as above
                shared_values.SharedValues.button2_pressed = False

                # changes the page to the lndpayment screen
                App.get_running_app().screenmanager.current = 'MainPage'

                # calls the monitoring method of the next page, which checks the button status again
                App.get_running_app().startpage.setup_monitoring()

                # sets the time for the last button push, which will be checked during the next button press
                shared_values.SharedValues.last_push = time.time()



