MCS_start_time = 0 #seconds
MCS_stop_time = 6 #seconds
MCS_bin_size = 1 #millisecond

# DO NOT MODIFY THE FORMATTING ABOVE: "start_timeSPACE=SPACE3SPACEcomments" ETC.
# DO NOT ENTER BIN SIZE WITH 2 DECIMAL PRECISION (2.3 IS OKAY 2.35 IS NOT)

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
DigitalOut('V_Dipole_RF_TTL',       ni_6363, 'port0/line6')
DigitalOut('PD_Trigger',            ni_6363, 'port0/line7')
DigitalOut('V_Dipole_ARB_Trigger',  ni_6363, 'port0/line8')
DigitalOut('Square_Coil_Switch',    ni_6363, 'port0/line9')
DigitalOut('Load_Beam_AOMs',        ni_6363, 'port0/line10')
Shutter   ('Collim_Shutter',        ni_6363, 'port0/line11', (0,0), 0)
DigitalOut('MOT2_AOM_TTL',          ni_6363, 'port0/line12')
DigitalOut('H_Dipole_AOM_TTL',      ni_6363, 'port0/line13')
DigitalOut('H_Dipole_ARB_Trigger',  ni_6363, 'port0/line14')
Shutter   ('Push_Focus_Shutter',    ni_6363, 'port0/line15', (0,0))
DigitalOut('LVIS_ZS_Coil_Switch',   ni_6363, 'port0/line16')
Shutter   ('LVIS_MOT1_Shutter',     ni_6363, 'port0/line17', (0,0))
DigitalOut('Flipper_Mirror',        ni_6363, 'port0/line18')
DigitalOut('DLD_Trigger',           ni_6363, 'port0/line19')
DigitalOut('RS_Trigger',            ni_6363, 'port0/line20')
DigitalOut('RF_Amp_TTL',            ni_6363, 'port0/line21')
Shutter   ('Imaging_Shutter',       ni_6363, 'port0/line22', (0,0))
Shutter   ('Intrap_Cooling_Shutter',ni_6363, 'port0/line23', (0,0))
AnalogOut ('MOT2_frequency',        ni_6738, 'ao0')
AnalogOut ('Bias_Coil_Current',     ni_6738, 'ao2')
AnalogOut ('ChTron_HV',             ni_6738, 'ao4')
AnalogOut ('MOT2_Power',            ni_6738, 'ao6')
AnalogOut ('Imaging_frequency',     ni_6738, 'ao8')
AnalogOut ('ZUP_Current',           ni_6738, 'ao11')
AnalogOut ('H_Dipole_Power',        ni_6738, 'ao12')
AnalogOut ('AOref',                 ni_6738, 'ao7')
DigitalOut('mcs_clock',             dummy,   '   ')

#Changing anything above requires Blacs to be re-compiled

if __name__ == '__main__':

    start()

    t=0
    t=0.001
    Push_Shutter.close(t)
    MOT2_Shutter.close(t)
    MOT2_Coil_Switch.go_high(t)
    Load_Beam_AOMs.go_high(t)
    Collim_Shutter.close(t)
    LVIS_ZS_Coil_Switch.go_high(t)
    RF_Amp_TTL.go_high(t)
    MOT2_frequency.constant(t,0.1)
    Bias_Coil_Current.constant(t,0)
    MOT2_Power.constant(t,10)
    ZUP_Current.ramp(t, duration=0.099, initial=0, final=0.92, samplerate= 1e4)
    
    t=1.15
    Push_Shutter.open(t)
    Collim_AOM_TTL.go_high(t)
    Load_Beam_AOMs.go_low(t)
    Collim_Shutter.open(t)
    Push_Focus_Shutter.open(t)
    LVIS_ZS_Coil_Switch.go_low(t)
    LVIS_MOT1_Shutter.open(t)

    t=1.1502
    MOT2_frequency.ramp(t, duration=10e-3, initial=0.1, final=5, samplerate= 1e4)
    MOT2_Power.ramp(t, duration=10e-3-0.0001, initial=10, final=4.7, samplerate= 1e4)
    ZUP_Current.ramp(t, duration=9e-3-0.0001, initial=0.92, final=0.3, samplerate= 1e4)

    t=1.16
    MOT2_Shutter.open(t)
    MOT2_AOM_TTL.go_high(t)
    DLD_Trigger.go_high(t)

    t=1.1602
    ZUP_Current.constant(t,3.5)

    t=1.1603
    MOT2_frequency.constant(t,0.1)
    MOT2_Power.constant(t,10)

    t=1.161
    DLD_Trigger.go_low(t)

    t=1.2806
    Bias_Coil_Current.ramp(t, duration=0.1-0.0001, initial=0, final=3.49, samplerate= 1e4)


    t=1.3
    RS_Trigger.go_high(t)
    

    t=1.378
    Intrap_Cooling_Shutter.open(t)

    t=1.38
    Square_Coil_Switch.go_high(t)

    t=1.3805
    MOT2_AOM_TTL.go_low(t)
    MOT2_frequency.constant(t, 6.57)
    MOT2_Power.constant(t,7.1)
    

    t=1.395
    V_Dipole_ARB_Trigger.go_high(t)
    H_Dipole_ARB_Trigger.go_high(t)

    t=1.4
    V_Dipole_RF_TTL.go_high(t)
    H_Dipole_AOM_TTL.go_high(t)

    t=1.72
    RS_Trigger.go_low(t)

    t=1.8807
    MOT2_AOM_TTL.go_high(t)
    MOT2_frequency.constant(t, 6.57)
    Bias_Coil_Current.ramp(t, duration=0.1-0.0001, initial=3.49, final=0.1, samplerate= 1e4)
    MOT2_Power.constant(t,10)
    ZUP_Current.ramp(t, duration=100e-3-0.0002, initial=3.5, final=0.1, samplerate= 1e4)

    t=1.881
    Intrap_Cooling_Shutter.close(t)
    

    t=1.9806
    MOT2_Coil_Switch.go_low(t)
    Bias_Coil_Current.constant(t,0)
    ZUP_Current.constant(t,0)

    t=1

    t=1.981
    RF_Amp_TTL.go_low(t)

    t=3.41
    RF_Amp_TTL.go_high(t)


    t=3.505
    PD_Trigger.go_high(t)
    V_Dipole_RF_TTL.go_low(t)
    V_Dipole_ARB_Trigger.go_low(t)
    H_Dipole_AOM_TTL.go_low(t)
    H_Dipole_ARB_Trigger.go_low(t)


    t=3.8
    PD_Trigger.go_low(t)

    t=4
    Load_Beam_AOMs.go_high(4)
    Push_Focus_Shutter.close(t)
    Square_Coil_Switch.go_low(t)



    t=6
    Push_Shutter.close(t)
    Collim_AOM_TTL.go_low(t)
    MOT2_Coil_Switch.go_high(t)
    MOT2_Shutter.close(t)
    Collim_Shutter.close(t)
    MOT2_AOM_TTL.go_low(t)
    LVIS_MOT1_Shutter.close(t)
    MOT2_frequency.constant(t,0)
    MOT2_Power.constant(t,0)


    #MCS stop time must not be greater than the above time. Add free time if necessary
    #The code below handles MCS readings. Do not modify unless intended
    if(MCS_stop_time>t): exit("MCS stop time is greater than experiment duration")
    mcs_clock.repeat_pulse_sequence(0.1,t+0.2,[(0,1),(5e-5,0)],10e-5,1e4)
    stop(t+0.4)
