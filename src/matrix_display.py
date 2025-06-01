"""Matrix display module."""

import os
import sys
import time
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))


class MatrixDisplay:
    """Matrix display class to handle rendering on a single or multiple matrices."""

    def __init__(self):
        self.matrix = None
        self.offscreen_canvas = None

        # Display rows. 16 for 16x32, 32 for 32x32. Default: 16
        self.rows = 16

        # Panel columns. Typically 32 or 64. (Default: 32)
        self.cols = 64

        # Daisy-chained boards. Default: 1.
        self.chain = 1

        # For Plus-models or RPi2: parallel chains. 1..3. Default: 1
        self.parallel = 1

        # Bits used for PWM. Something between 1..11. Default: 11
        self.pwm_bits = 11

        # Sets brightness level. Default: 100. Range: 1..100
        self.brightness = 100

        # Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm
        self.gpio_mapping = None

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
        self.drop_privileges = True

    def usleep(self, value):
        """Sleep for a given number of microseconds."""
        time.sleep(value / 1000000.0)

    def run(self):
        """Run the matrix display."""
        print("Running")
        self.display_image('./animations/sample/1.jph')

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
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

        return True
    
    def display_image(self, image_path):
        """Display an image on the matrix display."""

        if not os.path.exists(image_path):
            return

        self.offscreen_canvas = self.matrix.CreateFrameCanvas()

        image = Image.open(image_path)
        image = image.convert("RGB")
        image.thumbnail((self.cols, self.rows), Image.ANTIALIAS)

        self.offscreen_canvas.SetImage(image)
        self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

    def pulse_colour(self):
        """Pulse a range of colours onto the matrix display."""

        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        continuum = 0

        while True:
            self.usleep(5 * 1000)
            continuum += 1
            continuum %= 3 * 255

            red = 0
            green = 0
            blue = 0

            if continuum <= 255:
                c = continuum
                blue = 255 - c
                red = c
            elif continuum > 255 and continuum <= 511:
                c = continuum - 256
                red = 255 - c
                green = c
            else:
                c = continuum - 512
                green = 255 - c
                blue = c

            self.offscreen_canvas.Fill(red, green, blue)
            self.offscreen_canvas = self.matrix.SwapOnVSync(
                self.offscreen_canvas)


# Main function
if __name__ == "__main__":
    matrix_display = MatrixDisplay()
    if not matrix_display.setup():
        print("Failed to process the matrix display options.")
        sys.exit(1)
