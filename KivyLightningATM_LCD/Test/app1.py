from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock


class MainScreenPage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.master_layout = MasterLayout()
        self.add_widget(self.master_layout)

        # creates an image from the current directory
        self.wimg = Image(source='YourImageHere2.png', size=(200, 200), pos_hint={'x': 0.37, 'y': 0.35},
                          size_hint=(None, None))
        # the image has to be added to the main widget
        self.add_widget(self.wimg)

#        self.label_main = Label(text="Start",
#                                pos_hint={'center_x': 0.5, 'center_y': 0.6},
#                                font_size=40,
#                                color=(0, 0, 0, 1))
#        self.add_widget(self.label_main)

        self.button_HOME = Button(text="HOME",
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

    def home_button(self, *args):
        main_app.screenmanager.current = 'MainPage'

    def start_button(self, *args):
        main_app.screenmanager.current = 'StandardPage'



class StandardPage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 1)
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

        self.label_top = Label(text="LIGHTING ATM",
                               pos_hint={'center_x': 0.5, 'center_y': 0.9},
                               font_size=45)
        self.add_widget(self.label_top)

        self.label_main = Label(text="Invoice oder LNURL",
                                pos_hint={'center_x': 0.5, 'center_y': 0.53})
        self.add_widget(self.label_main)

        self.button_home = Button(text="Home",
                                  size_hint=(0.2, 0.1),
                                  size_hint_min_x=150,
                                  size_hint_min_y=60,
                                  size_hint_max_x=150,
                                  size_hint_max_y=60,
                                  pos_hint={'top': 0.98, 'right': 0.2})
        self.button_home.bind(on_press=self.home_button)
        self.add_widget(self.button_home)

        self.button_back = Button(text="Back",
                                  size_hint=(0.2, 0.1),
                                  size_hint_min_x=150,
                                  size_hint_min_y=60,
                                  size_hint_max_x=150,
                                  size_hint_max_y=60,
                                  pos_hint={'top': 0.98, 'right': 0.99})
        self.button_back.bind(on_press=self.back_button)
        self.add_widget(self.button_back)

        self.button_invoice = Button(text="Invoice",
                                     size_hint=(0.2, 0.1),
                                     size_hint_min_x=150,
                                     size_hint_min_y=60,
                                     size_hint_max_x=150,
                                     size_hint_max_y=60,
                                     pos_hint={'center_x': 0.4, 'center_y': 0.2})
        self.button_invoice.bind(on_press=self.invoice_button)
        self.add_widget(self.button_invoice)

        self.button_lnurl = Button(text="LNURL",
                                   size_hint=(0.2, 0.1),
                                   size_hint_min_x=150,
                                   size_hint_min_y=60,
                                   size_hint_max_x=150,
                                   size_hint_max_y=60,
                                   pos_hint={'center_x': 0.6, 'center_y': 0.2})
        self.button_lnurl.bind(on_press=self.lnurl_button)
        self.add_widget(self.button_lnurl)

    def home_button(self, *args):
        main_app.screenmanager.current = 'MainPage'

    def back_button(self, *args):
        main_app.screenmanager.current = 'MainPage'

    def invoice_button(self, *args):
        main_app.screenmanager.current = 'PaymentPage'

    def lnurl_button(self, *args):
        # main_app.screenmanager.current = 'PaymentPage'
        pass


class PaymentPage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.fiat = 0
        self.btcprice = 0
        self.btcprice_fee = 0
        self.satprice = 0
        self.satprice_fee = 0

        with self.canvas:
            Color(1, 1, 1)
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

        self.label_top = Label(text="LIGHTING ATM",
                               pos_hint={'center_x': 0.5, 'center_y': 0.9},
                               font_size=45)
        self.add_widget(self.label_top)

        self.label_main = Label(text="Start",
                                pos_hint={'center_x': 0.5, 'center_y': 0.53})
        self.add_widget(self.label_main)

        self.button_home = Button(text="Home",
                                  size_hint=(0.2, 0.1),
                                  size_hint_min_x=150,
                                  size_hint_min_y=60,
                                  size_hint_max_x=150,
                                  size_hint_max_y=60,
                                  pos_hint={'top': 0.98, 'right': 0.2})
        self.button_home.bind(on_press=self.home_button)
        self.add_widget(self.button_home)

        self.button_back = Button(text="Back",
                                  size_hint=(0.2, 0.1),
                                  size_hint_min_x=150,
                                  size_hint_min_y=60,
                                  size_hint_max_x=150,
                                  size_hint_max_y=60,
                                  pos_hint={'top': 0.98, 'right': 0.99})
        self.button_back.bind(on_press=self.back_button)
        self.add_widget(self.button_back)

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
        main_app.screenmanager.current = 'MainPage'

    def back_button(self, *args):
        main_app.screenmanager.current = 'StandardPage'

    def start_button(self, *args):
        pass


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


class MainApp(App):


    def build(self):

        self.screenmanager = ScreenManager(transition=NoTransition())

        self.mainscreenpage = MainScreenPage()
        screen = Screen(name='MainPage')
        screen.add_widget(self.mainscreenpage)
        self.screenmanager.add_widget(screen)

        self.standardscreenpage = StandardPage()
        screen = Screen(name='StandardPage')
        screen.add_widget(self.standardscreenpage)
        self.screenmanager.add_widget(screen)

        self.paymentscreen = PaymentPage()
        screen = Screen(name='PaymentPage')
        screen.add_widget(self.paymentscreen)
        self.screenmanager.add_widget(screen)

        return self.screenmanager



    def return_self(self):
        return self

if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()
