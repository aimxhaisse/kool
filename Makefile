KERNELS = kernel-3.17

all:	kool-configs


kool-configs: $(KERNELS)


kernel-3.17:
	mkdir $@
	wget https://www.kernel.org/pub/linux/kernel/v3.x/linux-3.17.8.tar.xz -O - | tar zxf - -C $@ --strip 1


fclean:
	rm -rf $(KERNELS)
