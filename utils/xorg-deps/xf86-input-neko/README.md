# xf86-input-glass-fence
[X.org](https://x.org/) [glass-fence](http://arxndev/glass-fence) input driver

### how to use
xf86-input-glass-fence assumes you have only one virtual touchscreen device available, see
`80-glass-fence.conf`. If there are multiple in your system, please specify one config
section for each.
xf86-input-glass-fence aims to make [glass-fence](http://arxndev/glass-fence) easy to use and doesn't
offer special configuration options.

* `./configure --prefix=/usr`
* `make`
* `sudo make install`

Done.

To _uninstall_, again go inside the extracted directory, and do

    sudo make uninstall
