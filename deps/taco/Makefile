TOP = $(realpath $(dir $(realpath $(firstword $(MAKEFILE_LIST))))../..)
TACO=$(TOP)/deps/taco
ARCH = $(shell uname)
ifeq ($(wildcard $(TACO)/Makefile.$(ARCH)),)
	MYARCH = Default
else
	MYARCH = $(ARCH)
endif

.PHONY: all clean

all: stamp

include $(TACO)/Makefile.$(MYARCH)

clean:
	rm -f $(TACO)/stamp
	rm -rf $(TACO)/build
	rm -rf $(TACO)/install
	rm -rf $(TACO)/tmp
