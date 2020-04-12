from kivy.uix.image import Image
from PIL import Image
from io import BytesIO
from picamera import PiCamera
import zbarlight
import time
import os
import os.path
import sys

import app
import page_start
import page_selection
import shared_values
import acceptor


class QrCode:
    """This class is responsible for scanning a qr-code."""

    @staticmethod
    def scan():
        """This methods sets up the pi camera and scans a qr-code. The method returns either a qr-code
        or False value"""
        print('scan method called')

        # starts the process of using the camera and scanning
        # in the following procedure the pi camera is called camera
        with PiCamera() as camera:
            # because it's unclear whether the camera works as expected it's in a try except block
            # if any problem occurs the program doesn't stop
            try:
                # starts a preview of the camera but not seen because of the kivy grafic framework
                camera.start_preview()

                # program sleeps for a second
                time.sleep(1)
                print('start scanning')
            # if any problem occurs inside the try block, the exception block will execute
            except:
                print('problem with pi camera start')

            # creates a file-like object for reading and writing bytes
            stream = BytesIO()

            # variable for the qr-code later
            qr_codes = None

            # Set timeout to 10 seconds
            timeout = time.time() + 10

            # as long as there is no qr-code in qr_codes and the timeout is not reached stay in this loop
            # and try to get an qr-code
            while qr_codes is None and (time.time() < timeout):
                stream.seek(0)
                # Start camera stream (make sure RaspberryPi camera is focused correctly
                # manually adjust it, if not)
                # camera captures an image from the stream
                camera.capture(stream, "jpeg")
                stream.seek(0)
                # zbarlight scans the image stream for a specific code --> here it's a qr-code and puts it
                # into the variable
                qr_codes = zbarlight.scan_codes("qrcode", Image.open(stream))

                # program stops for 50 milli seconds
                time.sleep(0.05)

            # after the loop the preview stops
            camera.stop_preview()

            # break immediately if we didn't get a qr code scan
            if not qr_codes:
                print('no qr code within 10 seconds')
                return False

            # decode the first qr_code to get the data
            qr_code = qr_codes[0].decode()

            return qr_code