MCS_start_time = 0 #seconds
MCS_stop_time = 2.1 #seconds
MCS_bin_size = 0.1 #millisecond
plot_averages = 1 #1 is single shot

# DO NOT MODIFY THE FORMATTING ABOVE: "start_timeSPACE=SPACE3SPACEcomments" ETC.
# DO NOT ENTER BIN SIZE WITH 2 DECIMAL PRECISION (2.3 IS OKAY 2.35 IS NOT

from labscript import *
from labscript_devices.PulseBlaster_No_DDS import PulseBlaster_No_DDS
from labscript_devices.NI_DAQmx.labscript_devices import NI_PCIe_6363
from labscript_devices.NI_DAQmx.labscript_devices import NI_PCIe_6738
from labscript_devices.DummyIntermediateDevice import DummyIntermediateDevice

from labscript_devices.NI_DAQmx.models.NI_PCIe_6363 import (
    CAPABILITIES as NI_PCIe_6363_CAPABILITIES
    )

modified_ports = NI_PCIe_6363_CAPABILITIES['ports'].copy()
del modified_ports['port1']
del modified_ports['port2']


PulseBlaster_No_DDS('pulseblaster_0')
ClockLine(name='clkline_1', pseudoclock=pulseblaster_0.pseudoclock, connection='flag 0') 
ClockLine(name='clkline_2', pseudoclock=pulseblaster_0.pseudoclock, connection='flag 1') 
ClockLine(name='mcs_clockline', pseudoclock=pulseblaster_0.pseudoclock, connection='flag 2') 
NI_PCIe_6363(name='ni_6363', parent_device=clkline_1, clock_terminal='/ni_6363/PFI8', MAX_name='ni_6363', acquisition_rate=100e3, ports=modified_ports)
NI_PCIe_6738(name='ni_6738', parent_device=clkline_2, clock_terminal='/ni_6738/PFI5', MAX_name='ni_6738')
DummyIntermediateDevice(name='dummy', parent_device=mcs_clockline)

DigitalOut('Imaging_Camera',        ni_6363, 'port0/line0')
DigitalOut('Collim_AOM_TTL',        ni_6363, 'port0/line1')
DigitalOut('Imaging_AOM_TTL',       ni_6363, 'port0/line2')
Shutter   ('Push_Shutter',          ni_6363, 'port0/line3', (0,0), 0)
Shutter   ('MOT2_Shutter',          ni_6363, 'port0/line4', (0,0), 0)
DigitalOut('MOT2_Coil_Switch',      ni_6363, 'port0/line5')
DigitalOut('PD_Trigger',            ni_6363, 'port0/line7')
DigitalOut('V_Dipole_ARB_Trigger',  ni_6363, 'port0/line8')
Shutter   ('MOT1_Shutter',          ni_6363, 'port0/line9', (0,0))
DigitalOut('Load_Beam_AOMs',        ni_6363, 'port0/line10')
Shutter   ('Collim_Shutter',        ni_6363, 'port0/line11', (0,0), 0)
DigitalOut('MOT2_AOM_TTL',          ni_6363, 'port0/line12')
Shutter   ('Push_Focus_Shutter',    ni_6363, 'port0/line15', (0,0))
DigitalOut('LVIS_ZS_Coil_Switch',   ni_6363, 'port0/line16')
DigitalOut('Focus_AOM_TTL',         ni_6363, 'port0/line17')
DigitalOut('Flipper_Mirror',        ni_6363, 'port0/line18')
DigitalOut('RS_Trigger',            ni_6363, 'port0/line20')
DigitalOut('RF_Amp_TTL',            ni_6363, 'port0/line21')
Shutter   ('Imaging_Shutter',       ni_6363, 'port0/line22', (0,0))
DigitalOut('Horiz_Dipole_AOM',      ni_6363, 'port0/line23')
AnalogOut ('MOT2_frequency',        ni_6738, 'ao0')
AnalogOut ('MOT2_Coil_V',           ni_6738, 'ao2')
AnalogOut ('ChTron_HV',             ni_6738, 'ao4')
AnalogOut ('MOT2_Power',            ni_6738, 'ao6')
AnalogOut ('Imaging_frequency',     ni_6738, 'ao8')
AnalogOut ('ZUP_Current',           ni_6738, 'ao11')
AnalogOut ('H_Dipole_Power',        ni_6738, 'ao12')
AnalogOut ('AOref',                 ni_6738, 'ao7')
DigitalOut('mcs_clock',             dummy,   '   ')
DigitalOut('mcs_trigger',           pulseblaster_0.direct_outputs, 'flag 3')

#Changing anything above requires Blacs to be re-compiled

if __name__ == '__main__':

    start()

    t=0
    # t=0.001
    Push_Shutter.close(t)
    MOT2_Shutter.close(t)
    MOT2_Coil_Switch.go_high(t)
    Load_Beam_AOMs.go_high(t)
    Collim_Shutter.close(t)
    LVIS_ZS_Coil_Switch.go_high(t)
    RF_Amp_TTL.go_high(t)
    MOT2_frequency.constant(t,0.2)
    Imaging_frequency.constant(t,2)
    ZUP_Current.ramp(t, duration=0.099, initial=0, final=0.92, samplerate= 1e4)
    MOT2_Power.constant(t,10)

    t=1.2
    LVIS_ZS_Coil_Switch.go_low(t)

    t=1.149
    MOT2_Coil_Switch.go_low(t)

    t=1.15
    Collim_AOM_TTL.go_high(t)
    Push_Shutter.open(t)
    PD_Trigger.go_high(t)
    Load_Beam_AOMs.go_low(t)
    Collim_Shutter.open(t)
    Push_Focus_Shutter.go_high(t)

    t=1.149
    ZUP_Current.constant(t,0)

    t=1.1501
    MOT2_frequency.constant(t,5.4)

    t=1.18
    MOT1_Shutter.open(t)

    t=1.185
    MOT2_Shutter.open(t)
    MOT2_AOM_TTL.go_high(t)

    t=1.5512
    MOT2_frequency.ramp(t, duration=0.004, initial=5.4, final=0.2, samplerate= 1e4)

    t=1.7
    PD_Trigger.go_low(t)
    MOT1_Shutter.close(t)

    t=1.8
    MOT2_AOM_TTL.go_low(t)

    t=2.1
    Collim_AOM_TTL.go_low(t)
    Push_Shutter.close(t)
    MOT2_Shutter.close(t)
    MOT2_Coil_Switch.go_high(t)
    Load_Beam_AOMs.go_high(t)
    Collim_Shutter.close(t)
    Push_Focus_Shutter.go_low(t)


    


    #MCS stop time must not be greater than the above time. Add free time if necessary
    #The code below handles MCS readings. Do not modify unless intended
    if(MCS_stop_time>t):
        exit("MCS stop time is greater than experiment duration")

    t+=0.2
    mcs_trigger.go_high(0.1)
    mcs_clock.repeat_pulse_sequence(10e-5,t,[(0,1),(5e-5,0)],10e-5,1e4) #fix this
    stop(t+0.1)


    
