from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color, Line
import RPi.GPIO as GPIO
from picamera import PiCamera
import zbarlight
import app
import page_start
import page_lnd_payment
import page_lnurl_payment


class SelectionPage(FloatLayout):
    """Creates a page, which inherits from FloatLayout. FloatLayout is one of several classes for pages. Here
    the position on each widget or thing can be freely chosen, which makes everything very flexible. This
    class handles the variety of payment methods, which is at the moment BOLT11 invoice and lnurl, where
    lnurl is under construction"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """The method initiates the whole layout and some basic variables. If this method doesn't end nothing
        is shown"""

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
        self.label_main = Label(text="Invoice oder LNURL",
                                pos_hint={'center_x': 0.5, 'center_y': 0.53},
                                font_size=30)
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
        # changes the page to the payment page, where the payment process uses an invoice
        self.button_invoice = Button(text="Invoice",
                                     size_hint=(0.2, 0.1),
                                     size_hint_min_x=150,
                                     size_hint_min_y=60,
                                     size_hint_max_x=150,
                                     size_hint_max_y=60,
                                     pos_hint={'center_x': 0.4, 'center_y': 0.2},
                                     font_size=33)
        self.button_invoice.bind(on_press=self.invoice_button)
        self.add_widget(self.button_invoice)

        # same as above
        # changes the page to the lnurl payment page which doesn't exist at the moment
        # therefore this button has no function
        self.button_lnurl = Button(text="LNURL",
                                   size_hint=(0.2, 0.1),
                                   size_hint_min_x=150,
                                   size_hint_min_y=60,
                                   size_hint_max_x=150,
                                   size_hint_max_y=60,
                                   pos_hint={'center_x': 0.6, 'center_y': 0.2},
                                   font_size=33)
        self.button_lnurl.bind(on_press=self.lnurl_button)
        self.add_widget(self.button_lnurl)

    def home_button(self, *args):
        # changes page to main page
        App.get_running_app().screenmanager.current = 'MainPage'

    def back_button(self, *args):
        # changes page to main page
        App.get_running_app().screenmanager.current = 'MainPage'

    def invoice_button(self, *args):
        # changes page to lnd payment page
        App.get_running_app().screenmanager.current = 'PaymentPage'

    def lnurl_button(self, *args):
        # will change the page to the lnurl payment page in the future
        # currently under construction --> nothing happens
        pass