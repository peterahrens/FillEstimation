TOP = $(dir $(realpath $(firstword $(MAKEFILE_LIST))))

.PHONY: all deps src clean clean_deps clean_src

all: deps src

clean: clean_deps clean_src

deps:
	$(MAKE) -C $(TOP)deps all

src: deps
	$(MAKE) -C $(TOP)src all

clean_deps:
	$(MAKE) -C $(TOP)deps clean

clean_src:
	$(MAKE) -C $(TOP)src clean
