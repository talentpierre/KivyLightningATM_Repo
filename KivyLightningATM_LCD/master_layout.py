from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color


class MasterLayout(FloatLayout):
    '''It's a little bit tricky to create a colored background or some graphics. If the screen size changes the
     size of the colored background has to be resized too. Also the relation has to be the same as before.
     This class sums all layouts up, created before and gives them a structure. Every time an empty colored page
     in a different size and position is added, so it looks like boarders'''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """The method initiates the whole layout. If this method doesn't end nothing
        is shown"""

        # sets variables for the different colored pages with different sizes and positions
        self.s0 = StandardLayout0()
        self.s1 = StandardLayout1(size_hint=(0.9, 0.8), pos_hint={'x': 0.05, 'y': 0.05})
        self.s2 = StandardLayout2(size_hint=(0.883, 0.778), pos_hint={'x': 0.058, 'y': 0.062})
        self.s3 = StandardLayout3(size_hint=(0.565, 0.1), pos_hint={'x': 0.22, 'y': 0.88})
        self.s4 = StandardLayout4(size_hint=(0.55, 0.08), pos_hint={'x': 0.228, 'y': 0.89})
        self.s5 = StandardLayout5()

        # adds the pages to the main page
        self.add_widget(self.s0)
        self.add_widget(self.s1)
        self.add_widget(self.s2)
        self.add_widget(self.s3)
        self.add_widget(self.s4)
        self.add_widget(self.s5)

        # button is created nearly the same as the label
        # size_hint = is the size relatively to the parent widget, which is the page actually
        # pos_hint is the same as above
        # this button has no function here because no touchscreen is used
        # it's used because of an easy way to implement a rectangle with a label in it
        self.button_home = Button(text="ATM",
                                  size_hint=(0.2, 0.1),
                                  pos_hint={'top': 0.98, 'right': 0.215},
                                  background_color=(0, 0, 0, 1),
                                  color=(0.8, 1, 1, 1),
                                  font_size=35)
        self.add_widget(self.button_home)

        # same as above
        self.button_back = Button(text="ATM",
                                  size_hint=(0.2, 0.1),
                                  pos_hint={'top': 0.98, 'right': 0.99},
                                  background_color=(0, 0, 0, 1),
                                  color=(0.8, 1, 1, 1),
                                  font_size=35)
        self.add_widget(self.button_back)


class StandardLayout0(FloatLayout):
    '''main background'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # creates a colored canvas
        with self.canvas.before:
            # color is set by red, green, blue, opacity --> 0 means 0 and 1 means 255
            Color(0.8, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # binds the size of the canvas to a method
        # if the size changes the update rect method is called
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        '''necessary to resize and relocate the colored canvas, if the main screen changed'''

        # updates the position of the canvas
        self.rect.pos = instance.pos

        # updates the size of the canvas
        self.rect.size = instance.size


# same as above
class StandardLayout1(FloatLayout):
    '''outside boarder'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


# same as above
class StandardLayout2(FloatLayout):
    '''inside edge of the outside boarder'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.8, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


# same as above
class StandardLayout3(FloatLayout):
    '''Lighting boarder'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


# same as above
class StandardLayout4(FloatLayout):
    '''inside of the Lightning boarder'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.8, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class StandardLayout5(FloatLayout):
    '''creates a Lightning Label'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # creates a label and puts it in instance variable
        # pos_hint = is a relative position --> 0 is 0% , 1 is 100% --> 0,0 is bottom left !!!
        # color is set by red, green, blue, opacity --> 0 means 0 and 1 means 255
        self.label_top = Label(text="LIGHTING",
                               pos_hint={'center_x': 0.5, 'center_y': 0.93},
                               font_size=45,
                               color=(0, 0, 0, 1))
        self.add_widget(self.label_top)
