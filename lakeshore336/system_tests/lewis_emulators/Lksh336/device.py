from collections import OrderedDict
from enum import Enum
from .states import DefaultState
from lewis.devices import StateMachineDevice

NUM_OUTPUTS = 4
INPUTS = ['A', 'B', 'C', 'D']
NUM_ZONES = 10

class SimulatedLksh336(StateMachineDevice):

    def _initialize_data(self):
        self.connected = True

        self.id = "test"
        self.output_heater_statuses = [2] * NUM_OUTPUTS
        self.output_analog_outputs = [2] * NUM_OUTPUTS
        self.output_setpoints = [2.0] * NUM_OUTPUTS
        self.input_kelvin_temperatures = { k:v for k,v in zip(INPUTS, [2] * len(INPUTS)) }
        self.input_voltage_inputs = { k:v for k,v in zip(INPUTS, [2] * len(INPUTS)) }
        self.output_ranges = [2] * NUM_OUTPUTS
        self.output_ramp_statuses = [1] * NUM_OUTPUTS
        self.output_ramp_values = [2] * NUM_OUTPUTS
        self.output_manual_values = [2] * NUM_OUTPUTS
        self.p = [2] * NUM_OUTPUTS
        self.i = [2] * NUM_OUTPUTS
        self.d = [2] * NUM_OUTPUTS
        self.output_mode_values = [2] * NUM_OUTPUTS
        self.output_input_modes = [2] * NUM_OUTPUTS
        self.output_powerup_modes = [1] * NUM_OUTPUTS
        self.zone_parameters = [[[2] * 8] * NUM_ZONES] * NUM_OUTPUTS
        self.input_sensor_names = { k:v for k,v in zip(INPUTS, ["test"] * len(INPUTS)) }
        self.input_alarm_statuses = { k:v for k,v in zip(INPUTS, [1] * len(INPUTS)) }
        self.input_low_alarm_statuses = { k:v for k,v in zip(INPUTS, [1] * len(INPUTS)) }
        self.input_alarm_enabled_settings = { k:v for k,v in zip(INPUTS, [1] * len(INPUTS)) }
        self.input_alarm_high_setpoints = { k:v for k,v in zip(INPUTS, [2] * len(INPUTS)) }
        self.input_alarm_low_setpoints = { k:v for k,v in zip(INPUTS, [2] * len(INPUTS)) }
        self.input_alarm_deadband_settings = { k:v for k,v in zip(INPUTS, [2] * len(INPUTS)) }
        self.input_alarm_latching_settings = { k:v for k,v in zip(INPUTS, [1] * len(INPUTS)) }
        self.input_alarm_audible_settings = { k:v for k,v in zip(INPUTS, [1] * len(INPUTS)) }
        self.input_alarm_visible_settings = { k:v for k,v in zip(INPUTS, [1] * len(INPUTS)) }
        self.input_reading_statuses = { k:v for k,v in zip(INPUTS, [2] * len(INPUTS)) }
        self.output_heater_statuses_st = [2] * NUM_OUTPUTS
        self.input_curve_numbers = { k:v for k,v in zip(INPUTS, [2] * len(INPUTS)) }
        self.input_curve_names = "111111111111111"
        self.input_curve_serial_numbers = "2222222222"
        self.input_curve_data_formats = 2
        self.input_curve_temperature_limits = 2.0
        self.input_curve_temperature_coefficients = 2
        self.input_sensor_types = { k:v for k,v in zip(INPUTS, [2] * len(INPUTS)) }
        self.input_auto_range_settings = { k:v for k,v in zip(INPUTS, [1] * len(INPUTS)) }
        self.input_ranges = { k:v for k,v in zip(INPUTS, [2] * len(INPUTS)) }
        self.input_compensations = { k:v for k,v in zip(INPUTS, [1] * len(INPUTS)) }
        self.input_units = { k:v for k,v in zip(INPUTS, [2] * len(INPUTS)) }
        
    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])
