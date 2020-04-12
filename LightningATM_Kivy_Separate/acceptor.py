import RPi.GPIO as GPIO
import time
import shared_values


class CoinAcceptor:

    # Set up GPIO:
    # Pin from the coinacceptor to the raspberry, which takes the inserted coin signals
    acceptorPin = 6
    # time for the last pulses to measure the difference
    lastimpulse = 0
    # takes the pulses from the coinacceptor. e.g. 3 pulses for 20 cent
    pulses = 0
    # necessary for creating an clockevent which initiates a method
    event2 = None

    @staticmethod
    def setup_acceptor():
        """prepares the acceptor to be used. this will be the case at the beginning of the program"""

        print('enter acceptor setup method')
        # disables all the warnings from the raspberry pi. e.g. pin is allready used
        GPIO.setwarnings(False)

        # GPIO.BCM defines that the pins will be called by there GPIO number. GPIO.BOARD calls the pins by their total
        # number. BCM values differ from model to model
        GPIO.setmode(GPIO.BCM)

        # defines a setup with a specific pin, how this pin is configured (input or output) and the actual
        # position. is it open or closed. here it's open, so no electric current flows
        GPIO.setup(CoinAcceptor.acceptorPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # a listener will be created who listens to a specific pin. therefore a pin is specified, if the
        # voltage is falling the event is triggered. callback mentions the method which is called
        GPIO.add_event_detect(CoinAcceptor.acceptorPin, GPIO.FALLING, callback=CoinAcceptor.coin_event)

    @staticmethod
    def coin_event(*args):
        """This method is called if the voltage is falling, which is defined in the setup method.
        So every time a coin is inserted this method is called, mostly multiple times because
        the acceptor sends more than one pulse per coin"""

        print('coin event')
        # saves the time of the last impulse
        CoinAcceptor.lastimpulse = time.time()

        # measure how many pulses where send
        CoinAcceptor.pulses = CoinAcceptor.pulses + 1

    @staticmethod
    def monitor_coins(*args):
        """Creates a condition, which checks the time between the actual time and the
        time of the last impulse and additionally the number of pulses. Therefore the different pulses from
        one coin event are counted as one input. This method is called repeatedly"""

        print('monitor coins')
        if (time.time() - CoinAcceptor.lastimpulse > 0.5) and (CoinAcceptor.pulses > 0):
            # if the condition matches, the coin_inserted method is called
            CoinAcceptor.coins_inserted()
        return True

    @staticmethod
    def coins_inserted(*args):
        """It measures the number of total pulses per coin input. Depending on the number of pulses a
        fiat value is set into the shared_value file. the fiat values add up during one payment process."""

        print('coin inserted')
        if CoinAcceptor.pulses == 3:
            print('5 Cent')
            shared_values.SharedValues.FIAT += 0.05
        if CoinAcceptor.pulses == 4:
            print('10 Cent')
            shared_values.SharedValues.FIAT += 0.10
        if CoinAcceptor.pulses == 5:
            print('20 Cent')
            shared_values.SharedValues.FIAT += 0.20
        if CoinAcceptor.pulses == 6:
            print('50 Cent')
            shared_values.SharedValues.FIAT += 0.50

        # the number of pulses has to be set to zero to match the next incoming number of pulses
        CoinAcceptor.pulses = 0




