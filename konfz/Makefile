# Confz

KERNEL_BASE_URL	?= "https://www.kernel.org/pub/linux/kernel/v3.x/"
WORKING_DIR 	?= tmp
KERNEL		?= linux-3.17
TARBALL		?= $(KERNEL).tar.gz
JSON 		?= $(KERNEL)
RESULT		?= data/
VENV		?= .venv

# Rulz

all:	$(VENV) $(RESULT)/$(JSON)


$(VENV):
	virtualenv $@
	pip install -r requirements.txt


$(RESULT)/$(JSON): $(RESULT) $(WORKING_DIR)/kconfiglib $(WORKING_DIR)/$(KERNEL)
	. $(VENV)/bin/activate && ./scripts/scan-kconfigs.sh $(WORKING_DIR)/$(KERNEL) $(RESULT)/$(JSON)


$(WORKING_DIR)/$(KERNEL):
	mkdir -p $@
	wget $(KERNEL_BASE_URL)/$(KERNEL).tar.gz -O - | tar zxf - -C $@ --strip 1


$(RESULT):
	mkdir -p $@


$(WORKING_DIR)/kconfiglib:
	git clone git://github.com/ulfalizer/Kconfiglib.git $@
	. $(VENV)/bin/activate && cd $@ && python setup.py install
