from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.popup import Popup
from kivy.uix.image import Image
import RPi.GPIO as GPIO

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import time


class StartPage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.master_layout = MasterLayout()
        self.add_widget(self.master_layout)

        self.label_main = Label(text="WELCOME",
                                pos_hint={'center_x': 0.5, 'center_y': 0.6},
                                font_size=40,
                                color=(0, 0, 0, 1))
        self.add_widget(self.label_main)

        self.button_HOME = Button(text="EXIT",
                                  size_hint=(0.2, 0.1),
                                  pos_hint={'top': 0.17, 'right': 0.93},
                                  background_color=(0, 0, 0, 1),
                                  color=(0.8, 1, 1, 1),
                                  font_size=30)
        self.button_HOME.bind(on_press=self.home_button)
        self.add_widget(self.button_HOME)

        self.button_PAYMENT = Button(text="PAYMENT",
                                     size_hint=(0.2, 0.1),
                                     pos_hint={'top': 0.17, 'right': 0.72},
                                     background_color=(0, 0, 0, 1),
                                     color=(0.8, 1, 1, 1),
                                     font_size=30)
        self.button_PAYMENT.bind(on_press=self.start_button)
        self.add_widget(self.button_PAYMENT)

        self.setup_monitoring()

    def home_button(self, *args):
        main_app.stop()

    def start_button(self, *args):
        main_app.screenmanager.current = 'SelectionPage'

    def monitor_button(self, *args):
        if time.time() > (SharedValues.last_push + 2):
            self.pins.set_button1_pressed()
            self.pins.set_button2_pressed()
            if SharedValues.button1_pressed:
                self.button_event.cancel()
                main_app.screenmanager.current = 'SelectionPage'
                SharedValues.button1_pressed = False
                main_app.selectionscreen.setup_monitoring()
                SharedValues.last_push = time.time()
            elif SharedValues.button2_pressed:
                self.button_event.cancel()
                SharedValues.button2_pressed = False
                main_app.stop()

    def setup_monitoring(self, *args):
        SharedValues.last_push = time.time()
        self.pins = PinsNeu()
        self.button_event = Clock.schedule_interval(self.monitor_button, 0.2)


class SelectionPage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.master_layout = MasterLayout()
        self.add_widget(self.master_layout)

        self.label_main = Label(text="SELECTION PAGE",
                                pos_hint={'center_x': 0.5, 'center_y': 0.6},
                                font_size=40,
                                color=(0, 0, 0, 1))
        self.add_widget(self.label_main)

        self.button_HOME = Button(text="HOME",
                                  size_hint=(0.2, 0.1),
                                  pos_hint={'top': 0.17, 'right': 0.93},
                                  background_color=(0, 0, 0, 1),
                                  color=(0.8, 1, 1, 1),
                                  font_size=30)
        self.button_HOME.bind(on_press=self.home_button)
        self.add_widget(self.button_HOME)

        self.button_LND = Button(text="LND",
                                 size_hint=(0.2, 0.1),
                                 pos_hint={'top': 0.17, 'right': 0.72},
                                 background_color=(0, 0, 0, 1),
                                 color=(0.8, 1, 1, 1),
                                 font_size=30)
        self.button_LND.bind(on_press=self.lnd_button)
        self.add_widget(self.button_LND)

    def home_button(self, *args):
        main_app.screenmanager.current = 'StartPage'

    def lnd_button(self, *args):
        main_app.screenmanager.current = 'PaymentPage'

    def monitor_button(self, *args):
        if time.time() > (SharedValues.last_push + 2):
            self.pins.set_button1_pressed()
            self.pins.set_button2_pressed()

            if SharedValues.button1_pressed:
                self.button_event.cancel()
                main_app.screenmanager.current = 'PaymentPage'
                main_app.lndpaymentscreen.setup_monitoring()
                SharedValues.last_push = time.time()
                SharedValues.button1_pressed = False

            elif SharedValues.button2_pressed:
                self.button_event.cancel()
                main_app.screenmanager.current = 'StartPage'
                main_app.startscreen.setup_monitoring()
                SharedValues.last_push = time.time()
                SharedValues.button2_pressed = False

    def setup_monitoring(self, *args):
        self.pins = PinsNeu()
        self.button_event = Clock.schedule_interval(self.monitor_button, 0.2)


class LndPaymentPage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.label_top = Label(text="LIGHTING ATM",
                               pos_hint={'center_x': 0.5, 'center_y': 0.9},
                               font_size=45)
        self.add_widget(self.label_top)

        self.label_main = Label(text="PaymentPage",
                                pos_hint={'center_x': 0.5, 'center_y': 0.6})
        self.add_widget(self.label_main)

        self.button_start = Button(text="Start",
                                   size_hint=(0.2, 0.1),
                                   size_hint_min_x=150,
                                   size_hint_min_y=60,
                                   size_hint_max_x=150,
                                   size_hint_max_y=60,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.2})
        self.button_start.bind(on_press=self.start_button)
        self.add_widget(self.button_start)

    def home_button(self, *args):
        main_app.screenmanager.current = 'StartPage'

    def back_button(self, *args):
        main_app.screenmanager.current = 'SelectionPage'

    def start_button(self, *args):
        main_app.screenmanager.current = 'PaymentPage'

    def setup_monitoring(self):
        pass


class PinsNeu:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set up GPIO:
        self.button1Pin = 22
        self.button2Pin = 26
        self.power1Pin = 25
        self.lastimpulse = 0
        self.pulses = 0

        self.setup_acceptor()

    def setup_acceptor(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.button1Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.button2Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def set_button1_pressed(self):
        if GPIO.input(self.button1Pin):
            SharedValues.button1_pressed = True

    def set_button2_pressed(self):
        if GPIO.input(self.button2Pin):
            SharedValues.button2_pressed = True


class SharedValues:
    button1_pressed = False
    button2_pressed = False

    last_push = 0


class MasterLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.s0 = StandardLayout0()
        self.s1 = StandardLayout1(size_hint=(0.9, 0.8), pos_hint={'x': 0.05, 'y': 0.05})
        self.s2 = StandardLayout2(size_hint=(0.883, 0.778), pos_hint={'x': 0.058, 'y': 0.062})
        self.s3 = StandardLayout3(size_hint=(0.565, 0.1), pos_hint={'x': 0.22, 'y': 0.88})
        self.s4 = StandardLayout4(size_hint=(0.55, 0.08), pos_hint={'x': 0.228, 'y': 0.89})
        self.s5 = StandardLayout5()

        self.add_widget(self.s0)
        self.add_widget(self.s1)
        self.add_widget(self.s2)
        self.add_widget(self.s3)
        self.add_widget(self.s4)
        self.add_widget(self.s5)

        self.button_home = Button(text="ATM",
                                  size_hint=(0.2, 0.1),
                                  pos_hint={'top': 0.98, 'right': 0.215},
                                  background_color=(0, 0, 0, 1),
                                  color=(0.8, 1, 1, 1),
                                  font_size=35)
        self.add_widget(self.button_home)

        self.button_back = Button(text="ATM",
                                  size_hint=(0.2, 0.1),
                                  pos_hint={'top': 0.98, 'right': 0.99},
                                  background_color=(0, 0, 0, 1),
                                  color=(0.8, 1, 1, 1),
                                  font_size=35)
        self.add_widget(self.button_back)


class StandardLayout0(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.8, 1, 1, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class StandardLayout1(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0, 0, 0, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class StandardLayout2(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.8, 1, 1, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class StandardLayout3(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0, 0, 0, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class StandardLayout4(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.8, 1, 1, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class StandardLayout5(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.label_top = Label(text="LIGHTING",
                               pos_hint={'center_x': 0.5, 'center_y': 0.93},
                               font_size=45,
                               color=(0, 0, 0, 1))
        self.add_widget(self.label_top)


class app(App):

    def build(self):
        self.screenmanager = ScreenManager(transition=NoTransition())

        self.startscreen = StartPage()
        screen = Screen(name='StartPage')
        screen.add_widget(self.startscreen)
        self.screenmanager.add_widget(screen)

        self.selectionscreen = SelectionPage()
        screen = Screen(name='SelectionPage')
        screen.add_widget(self.selectionscreen)
        self.screenmanager.add_widget(screen)

        self.lndpaymentscreen = LndPaymentPage()
        screen = Screen(name='PaymentPage')
        screen.add_widget(self.lndpaymentscreen)
        self.screenmanager.add_widget(screen)

        self.screenmanager.current = 'StartPage'

        return self.screenmanager


if __name__ == "__main__":
    main_app = app()
    main_app.run()
    # app().run()
