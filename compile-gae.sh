# modified from https://github.com/fjakobs/cloud9-gae-template/blob/master/compile-gae.sh

function install_python27 {
    wget http://www.python.org/ftp/python/2.7.3/Python-2.7.3.tgz
    tar xvfz Python-2.7.3.tgz
    cd Python-2.7.3 
    ./configure --prefix=$HOME
    make
    make install
    cd ..
    rm -rf Python-2.7.3*
}

function install_appengine {
    wget http://googleappengine.googlecode.com/files/google_appengine_1.8.2.zip
    unzip google_appengine_1.8.2.zip
    rm google_appengine_1.8.2.zip
    mv google_appengine ../lib/
    cd ../bin/
    ln -s ../lib/google_appengine/*.py .
}

function install_pil {
    wget http://effbot.org/downloads/Imaging-1.1.7.tar.gz
    tar xvfz Imaging-1.1.7.tar.gz
    cd Imaging-1.1.7
    python setup.py install
    cd ..
    rm -rf rm Imaging-1.1.7*
}

install_appengine
install_pil