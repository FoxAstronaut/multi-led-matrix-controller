#!/usr/bin/env python
import sys

class MatrixDisplay():
    def __init__(self, *args, **kwargs):
        super(MatrixDisplay, self).__init__(*args, **kwargs)

    def run(self):
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
            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

# Main function
if __name__ == "__main__":
    matrix_display = MatrixDisplay()

    try:
      # Start loop
      print("Press CTRL-C to stop sample")
    except KeyboardInterrupt:
      print("Exiting\n")
      sys.exit(0)
