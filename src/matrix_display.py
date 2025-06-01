"""Matrix display module."""

import os
import sys
import time
import argparse
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions

class MatrixDisplay:
    """Matrix display class to handle rendering on a single or multiple matrices."""

    def __init__(self):
        self.matrix = None
        self.offscreen_canvas = None

        # Display rows. 16 for 16x32, 32 for 32x32. Default: 16
        self.rows = 32

        # Panel columns. Typically 32 or 64. (Default: 32)
        self.cols = 64

        # Daisy-chained boards. Default: 1.
        self.chain = 1

        # For Plus-models or RPi2: parallel chains. 1..3. Default: 1
        self.parallel = 1

        # Bits used for PWM. Something between 1..11. Default: 11
        self.pwm_bits = 11

        # Sets brightness level. Default: 100. Range: 1..100
        self.brightness = 50

        # Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm
        self.gpio_mapping = "regular"

        # Progressive or interlaced scan. 0 Progressive, 1 Interlaced (default)
        self.scan_mode = 1

        # Base time-unit for the on-time in the lowest significant bit in nanoseconds. Default: 130
        self.pwm_lsb_nanoseconds = 130

        # Shows the current refresh rate of the LED panel
        self.show_refresh = False

        # Slow down writing to GPIO. Range: 0..4. Default: 1
        self.slowdown_gpio = 1

        # Don't use hardware pin-pulse generation
        self.no_hardware_pulse = True

        # Switch if your matrix has led colors swapped. Default: RGB
        self.rgb_sequence = "RGB"

        # Apply pixel mappers. e.g "Rotate:90"
        self.pixel_mapper = ""

        # 0 = default 1=AB-addressed panels 2=row direct 3=ABC-addressed panels 4 = ABC Shift + DE direct
        self.row_addr_type = 0

        # Multiplexing type: 0=direct 1=strip 2=checker 3=spiral 4=ZStripe 5=ZnMirrorZStripe 6=coreman 7=Kaler2Scan 8=ZStripeUneven... (Default: 0)
        self.led_multiplexing = 0

        # Needed to initialize special panels. Supported: 'FM6126A'
        self.panel_type = ""

        # Don't drop privileges from 'root' after initializing the hardware.
        self.drop_privileges = False

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-a", "--animation", action="store",
                                 help="Which animation to show", default="sample", type=str)

        self.args = self.parser.parse_args()

    def usleep(self, value):
        """Sleep for a given number of microseconds."""
        time.sleep(value / 1000000.0)

    def run(self):
        """Run the matrix display."""
        print("Running")

        self.display_images('./animations/' + self.args.animation)

    def setup(self):
        """Setup matrix display."""

        options = RGBMatrixOptions()

        if self.gpio_mapping is not None:
            options.hardware_mapping = self.gpio_mapping

        options.rows = self.rows
        options.cols = self.cols
        options.chain_length = self.chain
        options.parallel = self.parallel
        options.row_address_type = self.row_addr_type
        options.multiplexing = self.led_multiplexing
        options.pwm_bits = self.pwm_bits
        options.brightness = self.brightness
        options.pwm_lsb_nanoseconds = self.pwm_lsb_nanoseconds
        options.led_rgb_sequence = self.rgb_sequence
        options.pixel_mapper_config = self.pixel_mapper
        options.panel_type = self.panel_type

        if self.show_refresh:
            options.show_refresh_rate = 1

        if self.slowdown_gpio is not None:
            options.gpio_slowdown = self.slowdown_gpio

        if self.no_hardware_pulse:
            options.disable_hardware_pulsing = True

        if not self.drop_privileges:
            options.drop_privileges = False

        self.matrix = RGBMatrix(options=options)

        try:
            # Start loop
            print("Press CTRL-C to stop sample")
            self.run()
            while True:
                time.sleep(100)
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

        return True

    def display_images(self, folder_path):
        """Display a folder of images"""

        if not os.path.exists(folder_path) and os.path.isdir(folder_path):
            print('Unable to find image folder\n')
            return

        files = os.listdir(folder_path).sort()

        for file in files:
            self.display_image(file)
            self.usleep(10)

    def display_image(self, image_path):
        """Display an image on the matrix display."""

        if not os.path.exists(image_path):
            print('Unable to find image\n')
            return

        self.offscreen_canvas = self.matrix.CreateFrameCanvas()

        image = Image.open(image_path)
        image = image.convert("RGB")

        self.offscreen_canvas.SetImage(image)
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

# Main function
if __name__ == "__main__":
    matrix_display = MatrixDisplay()
    if not matrix_display.setup():
        print("Failed to process the matrix display options.")
        sys.exit(1)
