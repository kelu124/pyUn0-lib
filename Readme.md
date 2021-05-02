![GitHub repo size](https://img.shields.io/github/repo-size/kelu124/pyUn0-lib?style=plastic)
![GitHub language count](https://img.shields.io/github/languages/count/kelu124/pyUn0-lib?style=plastic)
![GitHub top language](https://img.shields.io/github/languages/top/kelu124/pyUn0-lib?style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/kelu124/pyUn0-lib?color=red&style=plastic)

[![Patreon](https://img.shields.io/badge/patreon-donate-orange.svg)](https://www.patreon.com/kelu124) 
[![Kofi](https://badgen.net/badge/icon/kofi?icon=kofi&label)](https://ko-fi.com/G2G81MT0G)

[![Slack](https://badgen.net/badge/icon/slack?icon=slack&label)](https://join.slack.com/t/usdevkit/shared_invite/zt-2g501obl-z53YHyGOOMZjeCXuXzjZow)
[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)

# un0rick companion - pyUn0 module

The aim of this module is to provide a Python API to the [un0rick board](http://un0rick.cc/un0rick), a Lattice FPGA-powered ultrasound pulse-echo board.

In this setup, the [board has been flashed](http://un0rick.cc/un0rick/rpi-setup) with a dedicated [binary](v1.1.bin) using iceprog, and connected to the RPi using a 40-pin ribbon.

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

## Setup of the "single" parameter acquisition


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

## Example of a piezo with a reflector a few cm away

![](/images/20201009a-1.png)

![](/images/20201009a-1-fft)



