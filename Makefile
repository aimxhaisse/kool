# Confz

KERNEL_BASE_URL	?= "https://www.kernel.org/pub/linux/kernel/v3.x/"
WORKING_DIR 	?= tmp
KERNEL		?= linux-3.17
TARBALL		?= $(KERNEL).tar.gz
JSON 		?= $(KERNEL)
RESULT		?= konfz/data

# Rulz

all:	$(RESULT)/$(JSON)


$(RESULT)/$(JSON): $(RESULT) $(WORKING_DIR)/kconfiglib $(WORKING_DIR)/$(KERNEL)
	./konfz/scripts/scan-kconfigs.sh $(WORKING_DIR)/$(KERNEL) $(RESULT)/$(JSON)


$(WORKING_DIR)/$(KERNEL):
	mkdir -p $@
	wget $(KERNEL_BASE_URL)/$(KERNEL).tar.gz -O - | tar zxf - -C $@ --strip 1


$(RESULT):
	mkdir -p $@


$(WORKING_DIR)/kconfiglib:
	git clone git://github.com/ulfalizer/Kconfiglib.git $@
	cd $@ && python setup.py install
