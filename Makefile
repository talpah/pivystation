
prepare:
	# Install necessary system packages
	sudo apt-get install -y \
		python-pip \
		build-essential \
		git \
		python \
		python-dev \
		ffmpeg \
		libsdl2-dev \
		libsdl2-image-dev \
		libsdl2-mixer-dev \
		libsdl2-ttf-dev \
		libportmidi-dev \
		libswscale-dev \
		libavformat-dev \
		libavcodec-dev \
		zlib1g-dev \
		libgstreamer1.0-dev


virtualenv: prepare
	test ! -d "env"
	sudo -H pip install --upgrade pip virtualenv setuptools
	virtualenv --no-site-packages env

setup:
	sudo -H pip install Cython==0.23
	sudo -H pip install kivy
	sudo -H pip install -r requirements.txt
	
setup-in-venv: virtualenv
	. env/bin/activate && pip install Cython==0.23
	. env/bin/activate && pip install kivy
	. env/bin/activate && pip install -r requirements.txt
	
clean:
	rm -rf env

.PHONY: setup requirements prepare virtualenv enable-venv clean
