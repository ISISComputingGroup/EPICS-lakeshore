import contextlib
import unittest

from parameterized import parameterized

from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc, parameterized_list


DEVICE_PREFIX = "LKSH336_01"

IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("LKSH336"),
        "macros": {},
        "emulator": "Lksh336",
    },
]

TEST_MODES = [TestModes.DEVSIM]


OUTPUTS = [ 1, 2, 3, 4 ]
INPUTS = ['A', 'B', 'C', 'D']

class Lksh336Tests(unittest.TestCase):
    """
    Tests for the Lksh336 IOC.
    """
    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("Lksh336", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX, default_wait_time=0)

    def test_GIVEN_default_id_THEN_id_set_correctly(self):
        self.ca.assert_that_pv_is("ID", "test")
    
    @parameterized.expand(parameterized_list(OUTPUTS))
    def test_GIVEN_default_output_header_status_THEN_output_header_set_correctly(self, _, output):
        self.ca.assert_that_pv_is(f"HEATER{output}:OUTPUT", 2)

    @parameterized.expand(parameterized_list(OUTPUTS))
    def test_GIVEN_default_analog_output_THEN_analog_output_set_correctly(self, _, output):
        self.ca.assert_that_pv_is(f"AOUT{output}", 2)

    @parameterized.expand(parameterized_list(OUTPUTS))
    def test_GIVEN_default_output_setpoints_THEN_output_setpoints_set_correctly(self, _, output):
        self.ca.assert_that_pv_exists(f"TEMP{output}:SP")
        self.ca.assert_that_pv_is(f"TEMP{output}:SP:RBV", 2.0)

    @parameterized.expand(parameterized_list(INPUTS))
    def test_GIVEN_default_input_kelvin_temperatures_THEN_input_kelvin_temperatures_set_correctly(self, _, input):
        self.ca.assert_that_pv_is(f"TEMP_{input}", 2)

    @parameterized.expand(parameterized_list(INPUTS))
    def test_GIVEN_default_input_voltage_inputs_THEN_input_voltage_inputs_set_correctly(self, _, input):
        self.ca.assert_that_pv_is(f"RAW_VOLT_{input}", 2)

    @parameterized.expand(parameterized_list(OUTPUTS))
    def test_GIVEN_default_output_ranges_THEN_output_ranges_set_correctly(self, _, output):
        self.ca.assert_that_pv_exists(f"HEATER{output}:RANGE:SP")
        self.ca.assert_that_pv_is(f"HEATER{output}:RANGE", "Medium")

    @parameterized.expand(parameterized_list(OUTPUTS))
    def test_GIVEN_default_output_ramp_values_THEN_output_ramp_values_set_correctly(self, _, output):
        self.ca.assert_that_pv_exists(f"RAMP_RATE{output}:SP")
        self.ca.assert_that_pv_exists(f"RAMP_ON{output}:SP")
        self.ca.assert_that_pv_is(f"RAMP_RATE{output}", 2)
        self.ca.assert_that_pv_is(f"RAMP_ON{output}", "On")

    @parameterized.expand(parameterized_list(OUTPUTS))
    def test_GIVEN_default_output_manual_values_THEN_output_manual_values_set_correctly(self, _, output):
        self.ca.assert_that_pv_exists(f"MANUAL_OUT{output}:SP")
        self.ca.assert_that_pv_is(f"MANUAL_OUT{output}", 2)

    @parameterized.expand(parameterized_list(OUTPUTS))
    def test_GIVEN_default_pid_values_THEN_pid_values_set_correctly(self, _, output):
        self.ca.assert_that_pv_exists(f"P{output}:SP")
        self.ca.assert_that_pv_exists(f"I{output}:SP")
        self.ca.assert_that_pv_exists(f"D{output}:SP")
        self.ca.assert_that_pv_is(f"P{output}", 2)
        self.ca.assert_that_pv_is(f"I{output}", 2)
        self.ca.assert_that_pv_is(f"D{output}", 2)

    @parameterized.expand(parameterized_list(OUTPUTS))
    def test_GIVEN_default_output_mode_THEN_output_mode_set_correctly(self, _, output):
        self.ca.assert_that_pv_exists(f"OUT_MODE{output}:SP")
        self.ca.assert_that_pv_exists(f"CTRL_IN{output}:SP")
        self.ca.assert_that_pv_exists(f"POWERUP{output}:SP")
        self.ca.assert_that_pv_is(f"OUT_MODE{output}", "Zone")
        self.ca.assert_that_pv_is(f"CTRL_IN{output}", "Measurement B")
        self.ca.assert_that_pv_is(f"POWERUP{output}", "On")

    # TODO: No sim?
    # @parameterized.expand(parameterized_list(OUTPUTS))
    # def test_GIVEN_default_zone_parameters_THEN_zone_parameters_set_correctly(self, _, output):
    #     self.ca.assert_that_pv_is(f"Z0:ALL{output}", [2] * 8)

    @parameterized.expand(parameterized_list(INPUTS))
    def test_GIVEN_default_input_sensor_names_THEN_input_sensor_names_set_correctly(self, _, input):
        self.ca.assert_that_pv_exists(f"NAME_{input}:SP")
        self.ca.assert_that_pv_is(f"NAME_{input}", "test")

    @parameterized.expand(parameterized_list(INPUTS))
    def test_GIVEN_default_input_alarm_statuses_THEN_input_alarm_statuses_set_correctly(self, _, input):
        self.ca.assert_that_pv_is(f"ALARM_{input}:HIGH", "On")
        self.ca.assert_that_pv_is(f"ALARM_{input}:LOW", "On")

    @parameterized.expand(parameterized_list(INPUTS))
    def test_GIVEN_default_input_alarm_parameters_THEN_input_alarm_parameters_set_correctly(self, _, input):
        self.ca.assert_that_pv_is(f"ALARM_{input}:ON", "Enabled")
        self.ca.assert_that_pv_is(f"ALARM_{input}:HIVAL", 2)
        self.ca.assert_that_pv_is(f"ALARM_{input}:LOVAL", 2)
        self.ca.assert_that_pv_is(f"ALARM_{input}:DEADBAND", 2)
        self.ca.assert_that_pv_is(f"ALARM_{input}:LATCHED", "Latching")
        self.ca.assert_that_pv_is(f"ALARM_{input}:AUDIBLE", "Audible")
        self.ca.assert_that_pv_is(f"ALARM_{input}:VISIBLE", "Visible")

    @parameterized.expand(parameterized_list(INPUTS))
    def test_GIVEN_default_input_reading_status_THEN_input_reading_status_set_correctly(self, _, input):
        self.ca.assert_that_pv_is(f"READING_{input}:STAT", 2)

    @parameterized.expand(parameterized_list(OUTPUTS))
    def test_GIVEN_default_output_heater_status_st_THEN_output_heater_status_st_set_correctly(self, _, output):
        self.ca.assert_that_pv_is(f"HEATER{output}:RAW_STAT", 2)

    @parameterized.expand(parameterized_list(INPUTS))
    def test_GIVEN_default_input_curve_number_THEN_input_curve_number_set_correctly(self, _, input):
        self.ca.assert_that_pv_is(f"CURVE_{input}:NUM", 2)

    @parameterized.expand(parameterized_list(INPUTS))
    def test_GIVEN_default_input_curve_header_THEN_input_curve_header_set_correctly(self, _, input):
        self.ca.assert_that_pv_is(f"CURVE_{input}:NAME", "111111111111111")
        self.ca.assert_that_pv_is(f"CURVE_{input}:SERIAL_N", "2222222222")
        self.ca.assert_that_pv_is(f"CURVE_{input}:FORMAT", "V/K")
        self.ca.assert_that_pv_is(f"CURVE_{input}:LIM", 2.0)
        self.ca.assert_that_pv_is(f"CURVE_{input}:COEFF", "Positive")

    @parameterized.expand(parameterized_list(INPUTS))
    def test_GIVEN_default_input_type_parameters_THEN_input_type_parameters_set_correctly(self, _, input):
        self.ca.assert_that_pv_is(f"IN_{input}:SENS_TYPE", "Platinum RTD")
        self.ca.assert_that_pv_is(f"IN_{input}:AUTORANGE", "On")
        self.ca.assert_that_pv_is(f"IN_{input}:RANGE", "100 Ohm")
        self.ca.assert_that_pv_is(f"IN_{input}:COMPENSATION", "On")
        self.ca.assert_that_pv_is(f"IN_{input}:UNITS", "Celcius")

    @parameterized.expand(parameterized_list(OUTPUTS))
    def test_autotune_pv_exists(self, _, output):
        self.ca.assert_that_pv_exists(f"AUTOTUNE_START{output}")
        