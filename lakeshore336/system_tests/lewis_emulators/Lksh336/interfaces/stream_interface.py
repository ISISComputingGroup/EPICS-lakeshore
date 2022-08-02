from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply


@has_log
class Lksh336StreamInterface(StreamInterface):
    
    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def __init__(self):
        super(Lksh336StreamInterface, self).__init__()
        self.commands = {
            CmdBuilder(self.get_id).escape("*IDN?").eos().build(),
            CmdBuilder(self.get_htr).escape("HTR? ").int().eos().build(),
            CmdBuilder(self.get_aout).escape("AOUT? ").int().eos().build(),
            CmdBuilder(self.get_setp).escape("SETP? ").int().eos().build(),
            CmdBuilder(self.get_krdg).escape("KRDG? ").string().eos().build(),
            CmdBuilder(self.get_srdg).escape("SRDG? ").string().eos().build(),
            CmdBuilder(self.get_range).escape("RANGE? ").int().eos().build(),
            CmdBuilder(self.get_ramp).escape("RAMP? ").int().eos().build(),
            CmdBuilder(self.get_mout).escape("MOUT? ").int().eos().build(),
            CmdBuilder(self.get_pid).escape("PID? ").int().eos().build(),
            CmdBuilder(self.get_om).escape("OUTMODE? ").int().eos().build(),
            CmdBuilder(self.get_zone).escape("ZONE? ").int().int().eos().build(),
            CmdBuilder(self.get_inname).escape("INNAME? ").string().eos().build(),
            CmdBuilder(self.get_alarmst).escape("ALARMST? ").string().eos().build(),
            CmdBuilder(self.get_alarm).escape("ALARM? ").string().eos().build(),
            CmdBuilder(self.get_rdgst).escape("RDGST? ").string().eos().build(),
            CmdBuilder(self.get_htrst).escape("HTRST? ").int().eos().build(),
            CmdBuilder(self.get_incrv).escape("INCRV? ").string().eos().build(),
            CmdBuilder(self.get_crvhdr).escape("CRVHDR? ").int().eos().build(),
            CmdBuilder(self.get_intype).escape("INTYPE? ").string().eos().build(),

            CmdBuilder(self.set_setp).escape("SETP ").int().escape(",").float().eos().build(),
            CmdBuilder(self.set_range).escape("RANGE ").int().escape(",").int().eos().build(),
            CmdBuilder(self.set_ramp).escape("RAMP ").int().escape(",").int().escape(",").float().eos().build(),
            CmdBuilder(self.set_mout).escape("MOUT ").int().escape(",").float().eos().build(),
            CmdBuilder(self.set_pid).escape("PID ").int().escape(",").float().escape(",").float().escape(",").float().eos().build(),
            CmdBuilder(self.set_outmode).escape("OUTMODE ").int().escape(",").int().escape(",").int().escape(",").int().eos().build(),
            CmdBuilder(self.set_inname).escape("INNAME ").string().escape(",").escape('"').string().escape('"').eos().build()
        }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def get_id(self):
        return "LSCI,{}".format(self.device.id)

    def get_htr(self, output):
        return f"{self.device.output_heater_statuses[output - 1]}"

    def get_aout(self, output):
        return f"{self.device.output_analog_outputs[output - 1]}"

    def get_setp(self, output):
        return f"{self.device.output_setpoints[output - 1]}"

    def get_krdg(self, input):
        return f"{self.device.input_kelvin_temperatures[input]}"

    def get_srdg(self, input):
        return f"{self.device.input_voltage_inputs[input]}"

    def get_range(self, output):
        return f"{self.device.output_ranges[output - 1]}"

    def get_ramp(self, output):
        return f"{self.device.output_ramp_statuses[output - 1]},{self.device.output_ramp_values[output - 1]}"

    def get_mout(self, output):
        return f"{self.device.output_manual_values[output - 1]}"

    def get_pid(self, output):
        return f"{self.device.p[output - 1]},{self.device.i[output - 1]},{self.device.d[output - 1]}"

    def get_om(self, output):
        return f"{self.device.output_mode_values[output - 1]},{self.device.output_input_modes[output - 1]},{self.device.output_powerup_modes[output - 1]}"

    def get_zone(self, output, zone):
        return self.device.zone_parameters[output - 1][zone - 1]

    def get_inname(self, input):
        return self.device.input_sensor_names[input]
    
    def get_alarmst(self, input):
        return f"{self.device.input_alarm_statuses[input]},{self.device.input_low_alarm_statuses[input]}"

    def get_alarm(self, input):
        return "{},{},{},{},{},{},{}".format(
            self.device.input_alarm_enabled_settings[input],
            self.device.input_alarm_high_setpoints[input],
            self.device.input_alarm_low_setpoints[input],
            self.device.input_alarm_deadband_settings[input],
            self.device.input_alarm_latching_settings[input],
            self.device.input_alarm_audible_settings[input],
            self.device.input_alarm_visible_settings[input]
        )

    def get_rdgst(self, input):
        return f"{self.device.input_reading_statuses[input]}"

    def get_htrst(self, output):
        return f"{self.device.output_heater_statuses_st[output - 1]}"

    def get_incrv(self, input):
        return f"{self.device.input_curve_numbers[input]}"

    def get_crvhdr(self, _):
        return "{},{},{},{},{}".format(
            self.device.input_curve_names,
            self.device.input_curve_serial_numbers,
            self.device.input_curve_data_formats,
            self.device.input_curve_temperature_limits,
            self.device.input_curve_temperature_coefficients
        )

    def get_intype(self, input):
        return "{},{},{},{},{}".format(
            self.device.input_sensor_types[input],
            self.device.input_auto_range_settings[input],
            self.device.input_ranges[input],
            self.device.input_compensations[input],
            self.device.input_units[input]
        )

    def set_setp(self, output, value):
        self.device.output_setpoints[output - 1] = value

    def set_range(self, output, value):
        self.device.output_ranges[output - 1] = value

    def set_ramp(self, output, status, value):
        self.device.output_ramp_statuses[output - 1] = status
        self.device.output_ramp_values[output - 1] = value

    def set_mout(self, output, value):
        self.device.output_manual_values[output - 1] = value

    def set_pid(self, output, p, i, d):
        self.device.p[output - 1] = p
        self.device.i[output - 1] = i
        self.device.d[output - 1] = d

    def set_outmode(self, output, mode, input, powerup):
        self.device.output_mode_values[output - 1] = mode
        self.device.output_input_modes[output - 1] = input
        self.device.output_powerup_modes[output - 1] = powerup

    def set_inname(self, input, value):
        self.device.input_sensor_names[input] = value
