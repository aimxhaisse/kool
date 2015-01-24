# Confz


WORKING_DIR = tmp
KERNELS = $(WORKING_DIR)/kernel-3.17
JSONS = $(WORKING_DIR)/kernel-3.17.json


# Rulz


all:	$(WORKING_DIR)/kconfiglib konfz


$(WORKING_DIR)/kconfiglib:
	git clone git://github.com/ulfalizer/Kconfiglib.git $@
	cd $@ && python setup.py install


run:	$(JSONS) konfz
	cd konfz && python koolz.py


konfz: $(JSONS)
	rm -rf konfz/data/
	mkdir -p konfz/data/
	cp $(JSONS) konfz/data/


$(WORKING_DIR)/kernel-3.17:
	mkdir -p $@
	wget https://www.kernel.org/pub/linux/kernel/v3.x/linux-3.17.8.tar.gz -O - | tar zxf - -C $@ --strip 1


fclean:
	rm -rf $(KERNELS) $(JSONS) $(WORKING_DIR)


%.json: %
	touch $@
