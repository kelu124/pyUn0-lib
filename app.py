import streamlit as st

from spi_connector import SpiConnector
import pyUn0 as us
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

## Creating the Connector
UN0RICK = SpiConnector()

## Creating the object

UN0RICK.set_period_between_acqs(int(2500000))  # Setting 2.5ms between shots
UN0RICK.JSON["N"] = 1  # Experiment ID of the day
UN0RICK.set_multi_lines(False)  # Single acquisition
UN0RICK.set_acquisition_number_lines(1)  # Setting the number of lines (1)
UN0RICK.set_msps(0)  # Sampling speed setting


# Variables to test


Pon = st.sidebar.number_input(label='Pulse on (ns)',min_value=10,max_value=500,value=200)
PDamp = st.sidebar.number_input(label='Damping on (ns)',min_value=500,max_value=5000,value=2000)
#PInter = st.sidebar.number_input(label='Pause in between (ns)',min_value=10,max_value=300,value=10)
PInter = 10
fPiezo = st.sidebar.number_input(label='F piezo (MHz)',min_value=1,max_value=10,value=5)


#st.write(Pon,PDamp,PInter)

A = UN0RICK.set_timings(
    Pon, PInter, PDamp, 5000, 190000
)  # Settings the series of pulses

TGC_start = st.sidebar.number_input(label='TGC Start',min_value=10,max_value=1000,value=500)
TGC_stop = st.sidebar.number_input(label='TGC Stop',min_value=10,max_value=1000,value=800)

TGCC = UN0RICK.create_tgc_curve(TGC_start, TGC_stop, True)[0]  # Gain: linear, 10mV to 980mV
UN0RICK.set_tgc_curve(TGCC)  # We then apply the curve
UN0RICK.set_tgc_constant(0)  # Sets in mV from 0 to 1000


## Doing the acq and saving it.
UN0RICK.JSON["data"] = UN0RICK.do_acquisition()  # Doing the acquisition and saves

name_json = (UN0RICK.JSON["experiment"]["id"] + "-" + str(UN0RICK.JSON["N"]) + ".json")

# Loading the data
y = us.DataToJson()
y.fPiezo = fPiezo
y.json_proccess(name_json)


fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(x=y.t, y=y.tmp,mode='lines', name='signal'),secondary_y=False)
fig.add_trace(go.Scatter(x=y.t, y=y.tdac,mode='lines', name='TGC'),secondary_y=True)

# Add figure title
fig.update_layout(
    title_text="Acquisition stored in "+name_json
)

# Set x-axis title
fig.update_xaxes(title_text="Time in us")

# Set y-axes titles
fig.update_yaxes(title_text="<b>Signal</b> in V", secondary_y=False)
fig.update_yaxes(title_text="<b>TGC</b> gain (0 to 1024)", secondary_y=True)
st.write("# Acquisition")
st.write(fig)


y.create_fft()

middle = int(y.LengthT / 2)-1
plot_time = y.FFT_x[50:middle]
plot_abs_fft = np.abs(y.FFT_y[50:middle])
plot_filtered_fft = np.abs(y.filtered_fft[50:middle])

fig = go.Figure()
fig.add_trace(go.Scatter(x=plot_time, y=plot_abs_fft,mode='lines', name='FFT'))
fig.add_trace(go.Scatter(x=plot_time, y=plot_filtered_fft,mode='lines', name='Filtered'))
fig.update_xaxes(title_text="Freq in MHz ")
st.write("# Exploring the spectrum")
st.write("Central frequency can be set with the FPIezo on the left hand")
st.write(fig)
#filtered_signal.FFT_x
#.FFT_x

st.write("# Cleaner signal")
fig = go.Figure()
fig.add_trace(go.Scatter(x=y.t, y=y.tmp,mode='lines', name='Raw signal'))
fig.add_trace(go.Scatter(x=y.t, y=y.filtered_signal,mode='lines', name='Filtered signal'))
fig.update_xaxes(title_text="Time in us")
st.write(fig)
