build-linux:
	cp src/bss.py build/linux/usr/bin/bssenglish
	cp src/bss.py src/init.py src/install_requires.py src/lib*.py build/linux/usr/lib/bssenglish
	cp res/bss.png build/linux/usr/share/pixmaps
	cp changelog.txt LICENSE build/linux/usr/share/bssenglish
	chmod 755 build/linux/usr/bin/bssenglish
	dpkg -b build/linux bssenglish_linux.deb
build-deepin:
	patch -p0 src/bss.py <patch/deepin.patch
	cp src/bss.py src/init.py src/install_requires.py src/lib*.py changelog.txt LICENSE build/deepin/opt/apps/com.Bail.bssenglish/files
	cp res/bss.png build/deepin/opt/apps/com.Bail.bssenglish/files/
	chmod 755 build/deepin/opt/apps/com.Bail.bssenglish/files/bss.py
	dpkg -b build/deepin bssenglish_deepin.deb
build-termux:
	patch -0 src/bss.py <patch/termux.patch
	cp src/bss.py build/termux/data/data/com.termux/files/usr/bin/bssenglish
	cp src/bss.py src/init.py src/install_requires.py src/lib*.py build/termux/data/data/com.termux/files/usr/lib/bssenglish
	cp res/bss.png build/termux/data/data/com.termux/files/usr/share/pixmaps
	cp changelog.txt LICENSE build/termux/data/data/com.termux/files/usr/share/bssenglish
	chmod 755 build/termux/data/data/com.termux/files/usr/bin/bssenglish
	dpkg -b build/termux bssenglish_termux.deb
clear:
	git checkout -- .
