from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition
import RPi.GPIO as GPIO
import page_start
import page_selection
import page_lnd_payment
import acceptor

from kivy.core.window import Window


class MainApp(App):
    def build(self):
        """This is the main-application. The build method follows the __init__
        method and has to be completed unless nothing is shown on screen.
        3 screens will be created. A screen manager coordinates the transition
        and holds the screens. Screens will be called by their name for switching"""

        Window.show_cursor = False

        print('create Screenmanager and Screens')
        self.screenmanager = ScreenManager(transition=NoTransition())

        # creates the welcome page and adds it to the screen manager
        self.startpage = page_start.StartPage()
        screen = Screen(name='MainPage')
        screen.add_widget(self.startpage)
        self.screenmanager.add_widget(screen)

        # creates a page where you can choose between lnurl and lnd
        # it is also added to the screen manager
        self.selectionpage = page_selection.SelectionPage()
        screen = Screen(name='SelectionPage')
        screen.add_widget(self.selectionpage)
        self.screenmanager.add_widget(screen)

        # creates a page for the lnurl payment process
        # it is also added to the screen manager
        self.paymentpage = page_lnd_payment.PaymentPage()
        screen = Screen(name='PaymentPage')
        screen.add_widget(self.paymentpage)
        self.screenmanager.add_widget(screen)

        print('Screens created')
        print('Initialize CoinAcceptor, including Pins')
        # sets all important basics for the raspberry pi and the coinacceptor
        # espacially pins and countingsystem of the pins
        acceptor.CoinAcceptor.setup_acceptor()

        return self.screenmanager

    # exit the app
    def close(self):
        # reset all the GPIOs to close securely
        GPIO.cleanup()

        # stops the app
        App.get_running_app().stop()


if __name__ == "__main__":
    # not really necessary to use an instance
    # instance cannot be called from outside the file
    # only through App.get_running_app()
    main_app = MainApp()
    main_app.run()
