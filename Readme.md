# un0rick companion - pyUn0 module

The aim of this module is to provide a Python API to the [un0rick board][http://un0rick.cc/un0rick)], a Lattice FPGA-powered ultrasound pulse-echo board.

In this setup, the [board has been flashed](http://un0rick.cc/un0rick/rpi-setup) with a dedicated [binary](https://github.com/kelu124/un0rick/raw/master/bins/v1.1.bin) using iceprog, and connected to the RPi using a 40-pin ribbon.

## Setup

In short, it looks like this:

![](https://raw.githubusercontent.com/kelu124/echomods/master/matty/images/P_20191123_161358.jpg)

## Testing for un0rick

Been testing it on un0rick v1.1 (with double SMA connectors) on a RPi4, with python2 and python3.

To get a blinky, one can use the following

```
python3 pyUn0.py single
```

For a single line,

```
python3 pyUn0.py single
python3 pyUn0.py process
```

## Setup of the "single" parameter acquisition


```python
UN0RICK = us_spi()
UN0RICK.init()
UN0RICK.test_spi(3)
TGCC = UN0RICK.create_tgc_curve(10, 980, True)[0]    # Gain: linear, 10mV to 980mV 
#                                                    # (1% to 98% gain over 200us)
UN0RICK.set_tgc_curve(TGCC)                          # We then apply the curve
UN0RICK.set_period_between_acqs(int(2500000))        # Setting 2.5ms between shots
UN0RICK.JSON["N"] = 1 				     # Experiment ID of the day
UN0RICK.set_multi_lines(False)                       # Single acquisition
UN0RICK.set_acquisition_number_lines(1)              # Setting the number of lines (1)
UN0RICK.set_msps(0)                                  # Sampling speed setting (64Msps)
A = UN0RICK.set_timings(200, 100, 2000, 5000, 200000)# Settings the series of pulses, 200ns pulse.
UN0RICK.JSON["data"] = UN0RICK.do_acquisition()      # Doing the acquisition and saves
```

## Seems to be working 

![](/images/20201009a-1.png)

![](/images/20201009a-1-fft)
