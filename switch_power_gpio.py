# To modify the code to work with an on-board switch power button, you'll need to use the `GPIO` module in Python, which is commonly used for interacting with hardware components on single-board computers like Raspberry Pi;

# Here's an example of how you can modify the code to work with an on-board switch power button;

import RPi.GPIO as GPIO
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty

Set up GPIO mode
GPIO.setmode(GPIO.BCM)

Define the GPIO pin for the power button
POWER_BUTTON_PIN = 17

class PowerApp(BoxLayout):
    progress_value = NumericProperty(0)
    progress_message = StringProperty("Welcome Matrepers")
    show_progress = False
    progress_max = 20
    establishing_energy_shield = False

    def __init__(self, **kwargs):
        super(PowerApp, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.progress_bar = ProgressBar(max=self.progress_max)
        self.progress_label = Label(text=self.progress_message)
        self.add_widget(self.progress_bar)
        self.add_widget(self.progress_label)
        self.progress_bar.opacity = 0
        self.progress_label.opacity = 0

        # Set up GPIO pin as input
        GPIO.setup(POWER_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(POWER_BUTTON_PIN, GPIO.FALLING, callback=self.power_on, bouncetime=300)

    def power_on(self, channel):
        if not self.show_progress:
            self.show_progress = True
            self.progress_bar.opacity = 1
            self.progress_label.opacity = 1
            Clock.schedule_interval(self.update_progress, 0.1)

    def update_progress(self, dt):
        if self.progress_value < self.progress_max:
            self.progress_value += 1
            self.progress_bar.value = self.progress_value
            if self.progress_value == self.progress_max // 2 and not self.establishing_energy_shield:
                self.establishing_energy_shield = True
                self.progress_message = "Establishing energy shield power"
                self.progress_label.text = self.progress_message
                self.progress_bar.value = 0
                self.progress_max = 100
                self.progress_bar.max = self.progress_max
        else:
            self.progress_value = 0
            self.show_progress = False
            self.progress_bar.opacity = 0
            self.progress_label.opacity = 0
            # Add code to start your program here

class MatrepersApp(App):
    def build(self):
        return PowerApp()

if __name__ == '__main__':
    try:
        MatrepersApp().run()
    finally:
        GPIO.cleanup()
# In this example, the `power_on` function is triggered when the power button is pressed. The `GPIO.FALLING` event is used to detect the falling edge of the button press, and the `bouncetime` parameter is used to debounce the button press;

# Note: Make sure to replace `POWER_BUTTON_PIN` with the actual GPIO pin number of your on-board switch power button.

Also, this code should be run on a Raspberry Pi or other single-board computer with GPIO capabilities. 😊