from collections import OrderedDict
from enum import Enum, auto
from re import A
from unicodedata import name
from webbrowser import UnixBrowser
from .states import DefaultState
from lewis.devices import StateMachineDevice


NUM_OUTPUTS = 4
INPUTS = ['A', 'B', 'C', 'D']


class Ramp(object):
    """
    Class representing an output ramp's rate and status.
    """
    def __init__(self) -> None:
        self.rate = 0.0
        self.status = 0

class PID(object):
    """
    Class representing a PID.
    """
    def __init__(self):
        self.p = 0
        self.i = 0
        self.d = 0

class OutMode(object):
    """
    Class holding the output mode, control input, and powerup.
    """
    def __init__(self):
        self.mode = 0
        self.control_input = 0
        self.powerup = 0

class AlarmStatus(object):
    """
    Class representing an alarm status.
    """
    def __init__(self):
        self.high = 0
        self.low = 0

class Alarm(object):
    """
    Class representing an alarm.
    """
    def __init__(self):
        self.enabled = 0
        self.high_setpoint = 0
        self.low_setpoint = 0
        self.deadband = 0
        self.latching = 0
        self.audible = 0
        self.visible = 0

class CurveHeader(object):
    """
    Class representing the header information of a curve.
    """
    def __init__(self):
        # Needs to be 15 characters.
        self.name = "".rjust(15, "#")
        # Needs to be 10 characters.
        self.serial_number = "".rjust(10, "#")
        self.data_format = 0
        self.temperature_limit = 0.0
        self.temperature_coefficient = 0

class InputType(object):
    """
    Class representing the input type parameters.
    """
    def __init__(self) -> None:
        self.sensor_type = 0
        self.auto_range_setting = 0
        self.range = 0
        self.compensation = 0
        self.units = 0


class SimulatedLksh336(StateMachineDevice):

    def _initialize_data(self):
        self.connected = True

        self.id = ""
        self.output_heater_values = [0] * NUM_OUTPUTS
        self.output_analog_outputs = [0] * NUM_OUTPUTS
        self.output_setpoints = [0.0] * NUM_OUTPUTS
        self.input_kelvin_temperatures = { k:v for k,v in zip(INPUTS, [0] * len(INPUTS)) }
        self.input_voltage_inputs = { k:v for k,v in zip(INPUTS, [0] * len(INPUTS)) }
        self.output_ranges = [0] * NUM_OUTPUTS
        self.output_ramps = [Ramp()] * NUM_OUTPUTS
        self.output_manual_values = [0.0] * NUM_OUTPUTS
        self.pids = [PID()] * NUM_OUTPUTS
        self.output_modes = [OutMode()] * NUM_OUTPUTS
        self.input_sensor_names = { k:v for k,v in zip(INPUTS, [""] * len(INPUTS)) }
        self.input_alarm_statuses = { k:v for k,v in zip(INPUTS, [AlarmStatus()] * len(INPUTS)) }
        self.input_alarms = { k:v for k,v in zip(INPUTS, [Alarm()] * len(INPUTS)) }
        self.input_reading_statuses = { k:v for k,v in zip(INPUTS, [0] * len(INPUTS)) }
        self.output_heater_statuses = [0] * NUM_OUTPUTS
        self.input_curve_numbers = { k:v for k,v in zip(INPUTS, [0] * len(INPUTS)) }
        self.input_curve_header = CurveHeader()
        self.input_types = { k:v for k,v in zip(INPUTS, [InputType()] * len(INPUTS)) }
        
    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])


    def get_output_heater_value(self, output):
        return self.output_heater_values[output - 1]

    def get_output_analog_output(self, output):
        return self.output_analog_outputs[output - 1]

    def get_output_setpoint(self, output):
        return self.output_setpoints[output - 1]

    def get_input_kelvin_temperature(self, input):
        return self.input_kelvin_temperatures[input]

    def get_input_voltage_input(self, input):
        return self.input_voltage_inputs[input]

    def get_output_range(self, output):
        return self.output_ranges[output - 1]

    def get_output_ramp(self, output):
        ramp = self.output_ramps[output - 1]
        return f"{ramp.status},{ramp.rate}"

    def get_output_manual_value(self, output):
        return self.output_manual_values[output - 1]

    def get_pid(self, output):
        pid = self.pids[output - 1]
        return f"{pid.p},{pid.i},{pid.d}"

    def get_output_mode(self, output):
        output_mode = self.output_modes[output - 1]
        return f"{output_mode.mode},{output_mode.control_input},{output_mode.powerup}"

    def get_input_sensor_name(self, input):
        return self.input_sensor_names[input]

    def get_input_alarm_status(self, input):
        alarm = self.input_alarm_statuses[input]
        return f"{alarm.high},{alarm.low}"

    def get_input_alarm(self, input):
        alarm = self.input_alarms[input]
        return f"{alarm.enabled},{alarm.high_setpoint},{alarm.low_setpoint},{alarm.deadband},{alarm.latching},{alarm.audible},{alarm.visible}"

    def get_input_reading_status(self, input):
        return self.input_reading_statuses[input]

    def get_output_heater_status(self, output):
        return self.output_heater_statuses[output - 1]

    def get_input_curve_number(self, input):
        return self.input_curve_numbers[input]

    def get_input_curve_header(self):
        return f"{self.input_curve_header.name},{self.input_curve_header.serial_number},{self.input_curve_header.data_format},{self.input_curve_header.temperature_limit},{self.input_curve_header.temperature_coefficient}"

    def get_input_type(self, input):
        type = self.input_types[input]
        return f"{type.sensor_type},{type.auto_range_setting},{type.range},{type.compensation},{type.units}"


    def set_output_heater_value(self, output, value):
        self.output_heater_values[output - 1] = value

    def set_output_analog_output(self, output, value):
        self.output_analog_outputs[output - 1] = value

    def set_output_setpoint(self, output, value):
        self.output_setpoints[output - 1] = value

    def set_input_kelvin_temperature(self, input, value):
        self.input_kelvin_temperatures[input] = value

    def set_input_voltage_input(self, input, value):
        self.input_voltage_inputs[input] = value

    def set_output_range(self, output, value):
        self.output_ranges[output - 1] = value

    def set_output_ramp(self, output, status, rate):
        ramp = self.output_ramps[output - 1]
        ramp.status = status
        ramp.rate = rate

    def set_output_manual_value(self, output, value):
        self.output_manual_values[output - 1] = value

    def set_pid(self, output, p, i, d):
        pid = self.pids[output - 1]
        pid.p = p
        pid.i = i
        pid.d = d

    def set_output_mode(self, output, mode, control_input, powerup):
        output_mode = self.output_modes[output - 1]
        output_mode.mode = mode
        output_mode.control_input = control_input
        output_mode.powerup = powerup

    def set_input_sensor_name(self, input, value):
        self.input_sensor_names[input] = value

    def set_input_alarm_status(self, input, high, low):
        alarm = self.input_alarm_statuses[input]
        alarm.high = high
        alarm.low = low

    def set_input_alarm(self, input, enabled, high_setpoint, low_setpoint, deadband, latching, audible, visible):
        alarm = self.input_alarms[input]
        alarm.enabled = enabled
        alarm.high_setpoint = high_setpoint
        alarm.low_setpoint = low_setpoint
        alarm.deadband = deadband
        alarm.latching = latching
        alarm.audible = audible
        alarm.visible = visible

    def set_input_reading_status(self, input, value):
        self.input_reading_statuses[input] = value

    def set_output_heater_status(self, output, value):
        self.output_heater_statuses[output - 1] = value

    def set_input_curve_number(self, input, value):
        self.input_curve_numbers[input] = value

    def set_input_curve_header(self, num, name, serial_number, data_format, temperature_limit, temperature_coefficient):
        self.input_curve_header.name = name
        self.input_curve_header.serial_number = serial_number
        self.input_curve_header.data_format = data_format
        self.input_curve_header.temperature_limit = temperature_limit
        self.input_curve_header.temperature_coefficient = temperature_coefficient

    def set_input_type(self, input, sensor_type, auto_range_setting, range, compensation, units):
        type = self.input_types[input]
        type.sensor_type = sensor_type
        type.auto_range_setting = auto_range_setting
        type.range = range
        type.compensation = compensation
        type.units = units
