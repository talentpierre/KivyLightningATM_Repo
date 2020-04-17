from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.image import Image
import time
from kivy.clock import Clock
import shared_values
import acceptor
import master_layout
import os
import os.path
import sys



class StartPage(FloatLayout):
    """Creates a page, which inherits from FloatLayout. FloatLayout is one of several classes for pages. Here
    the position on each widget or thing can be freely chosen, which makes everything very flexible. This
    class handles most of the payment process with lnd and presents page which different widgets, labels and so on."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """The method initiates the whole layout and some basic variables. If this method doesn't end nothing
        is shown"""

        # this creates a layout from the master_layout file, including background and lines
        self.master_layout1 = master_layout.MasterLayout()
        # the layout has to be added to the main widget
        self.add_widget(self.master_layout1)

        # creates an image from the current directory
        self.wimg = Image(source='YourImageHere2.png', size=(200, 200), pos_hint={'x': 0.45, 'y': 0.35},
                          size_hint=(None, None))
        # the image has to be added to the main widget
        self.add_widget(self.wimg)

#        # creates a label and puts it in instance variable
#        # pos_hint = is a relative position --> 0 is 0% , 1 is 100% --> 0,0 is bottom left !!!
#        # color is set by red, green, blue, opacity --> 0 means 0 and 1 means 255
#        self.label_main = Label(text="WELCOME",
#                                pos_hint={'center_x': 0.5, 'center_y': 0.6},
#                                font_size=40,
#                                color=(0, 0, 0, 1))
#        # the label has to be added to main widget, which is the page actually
#        self.add_widget(self.label_main)

        # button is created nearly the same as the label
        # size_hint = is the size relatively to the parent widget, which is the page actually
        # pos_hint is the same as above
        # HOME button is for exiting the app, but has no real function here because no touchscreen is used
        # it's used because of an easy way to implement a rectangle with a label in it
        self.button_HOME = Button(text="EXIT",
                                  size_hint=(0.2, 0.1),
                                  pos_hint={'top': 0.17, 'right': 0.93},
                                  background_color=(0, 0, 0, 1),
                                  color=(0.8, 1, 1, 1),
                                  font_size=30)
        self.button_HOME.bind(on_press=self.home_button)
        self.add_widget(self.button_HOME)

        # same as above
        # would change the page to the selection page
        self.button_PAYMENT = Button(text="PAYMENT",
                                     size_hint=(0.2, 0.1),
                                     pos_hint={'top': 0.17, 'right': 0.72},
                                     background_color=(0, 0, 0, 1),
                                     color=(0.8, 1, 1, 1),
                                     font_size=30)
        self.button_PAYMENT.bind(on_press=self.start_button)
        self.add_widget(self.button_PAYMENT)

        # due to the use of buttons this method is called
        self.setup_monitoring()

        # due to the beginning of the program, the time for the last button push will be initialized here
        # just for security reasons
        shared_values.SharedValues.last_push = time.time()

    def home_button(self, *args):
        # would close the app
        # not in use because there is no touchscreen
        App.get_running_app().stop()

    def start_button(self, *args):
        # would change the page to the selection page
        # not in use because there is no touchscreen
        App.get_running_app().screenmanager.current = 'SelectionPage'

    def setup_monitoring(self, *args):
        '''starts a process of calling the monitor button method every 0.2 seconds'''

        # because the status of the buttons has to be checked constantly, an event is initialized
        # the monitor button function will be called every 0.2 seconds to check if a button was pressed
        self.button_event = Clock.schedule_interval(self.monitor_button, 0.2)

    def monitor_button(self, *args):
        '''checks if and what button was pressed'''
        print('1')
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

                # changes the page to the selection page
                App.get_running_app().screenmanager.current = 'SelectionPage'

                # sets the control value to false for the next usage of the button
                shared_values.SharedValues.button1_pressed = False

                # calls the monitoring method of the next page, which checks the button status again
                App.get_running_app().selectionpage.setup_monitoring()

                # sets the time for the last button push, which will be checked during the next button press
                shared_values.SharedValues.last_push = time.time()

            # if button1 wasn't pressed it checks button 2
            elif shared_values.SharedValues.button2_pressed:
                # same as above
                self.button_event.cancel()

                # same as above
                shared_values.SharedValues.button2_pressed = False

                # exits the app
                App.get_running_app().stop()