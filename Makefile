# The top level Makefile compiles the library in the lib subdirectory.
RGB_LIBDIR=./lib
RGB_LIBRARY_NAME=rgbmatrix
RGB_LIBRARY=$(RGB_LIBDIR)/lib$(RGB_LIBRARY_NAME).a

# Some language bindings.
PYTHON_LIB_DIR=./python

all : $(RGB_LIBRARY)

$(RGB_LIBRARY): FORCE
	$(MAKE) -C $(RGB_LIBDIR)

clean:
	$(MAKE) -C lib clean
	$(MAKE) -C $(PYTHON_LIB_DIR) clean

build-python: $(RGB_LIBRARY)
	$(MAKE) -C $(PYTHON_LIB_DIR) build

install-python: build-python
	$(MAKE) -C $(PYTHON_LIB_DIR) install

FORCE:
.PHONY: FORCE
