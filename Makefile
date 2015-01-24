# Confz


WORKING_DIR = tmp
KERNELS = $(WORKING_DIR)/kernel-3.17
LKDDBS = $(WORKING_DIR)/kernel-3.17.lkddb


# Rulz


all:	kool-configs


kool-configs: $(WORKING_DIR)/lkddb $(LKDDBS)


$(WORKING_DIR)/kernel-3.17:
	mkdir -p $@
	wget https://www.kernel.org/pub/linux/kernel/v3.x/linux-3.17.8.tar.gz -O - | tar zxf - -C $@ --strip 1


$(WORKING_DIR)/lkddb:
	mkdir -p $@
	wget http://cateee.net/sources/lkddb-sources/lkddb-sources-2015-01-07.tar.gz -O - | tar zxf - -C $@ --strip 1


fclean:
	rm -rf $(KERNELS) $(LKDDBS) $(WORKING_DIR)/lkddb


%.lkddb: %
	cd $(WORKING_DIR)/lkddb && ./build-lkddb.py ../../$< && mv lkddb.data.db ../../$@
