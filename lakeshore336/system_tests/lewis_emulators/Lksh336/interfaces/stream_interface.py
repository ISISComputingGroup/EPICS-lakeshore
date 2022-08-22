from lewis.adapters.stream import StreamInterface
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

    @conditional_reply("connected")
    def get_id(self):
        return "LSCI,{}".format(self.device.id)

    @conditional_reply("connected")
    def get_htr(self, output):
        return self.device.get_output_heater_value(output)

    @conditional_reply("connected")
    def get_aout(self, output):
        return self.device.get_output_analog_output(output)

    @conditional_reply("connected")
    def get_setp(self, output):
        return self.device.get_output_setpoint(output)

    @conditional_reply("connected")
    def get_krdg(self, input):
        return self.device.get_input_kelvin_temperature(input)

    @conditional_reply("connected")
    def get_srdg(self, input):
        return self.device.get_input_voltage_input(input)

    @conditional_reply("connected")
    def get_range(self, output):
        return self.device.get_output_range(output)

    @conditional_reply("connected")
    def get_ramp(self, output):
        return self.device.get_output_ramp(output)

    @conditional_reply("connected")
    def get_mout(self, output):
        return self.device.get_output_manual_value(output)

    @conditional_reply("connected")
    def get_pid(self, output):
        return self.device.get_pid(output)

    @conditional_reply("connected")
    def get_om(self, output):
        return self.device.get_output_mode(output)

    @conditional_reply("connected")
    def get_inname(self, input):
        return self.device.get_input_sensor_name(input)

    @conditional_reply("connected")
    def get_alarmst(self, input):
        return self.device.get_input_alarm_status(input)

    @conditional_reply("connected")
    def get_alarm(self, input):
        return self.device.get_input_alarm(input)

    @conditional_reply("connected")
    def get_rdgst(self, input):
        return self.device.get_input_reading_status(input)

    @conditional_reply("connected")
    def get_htrst(self, output):
        return self.device.get_output_heater_status(output)

    @conditional_reply("connected")
    def get_incrv(self, input):
        return self.device.get_input_curve_number(input)

    @conditional_reply("connected")
    def get_crvhdr(self, _):
        return self.device.get_input_curve_header()

    @conditional_reply("connected")
    def get_intype(self, input):
        return self.device.get_input_type(input)

    @conditional_reply("connected")
    def set_setp(self, output, value):
        self.device.set_output_setpoint(output, value)

    @conditional_reply("connected")
    def set_range(self, output, value):
        self.device.set_output_range(output, value)

    @conditional_reply("connected")
    def set_ramp(self, output, status, rate):
        self.device.set_output_ramp(output, status, rate)

    @conditional_reply("connected")
    def set_mout(self, output, value):
        self.device.set_output_manual_value(output, value)

    @conditional_reply("connected")
    def set_pid(self, output, p, i, d):
        self.device.set_pid(output, p, i, d)

    @conditional_reply("connected")
    def set_outmode(self, output, mode, control_input, powerup):
        self.device.set_output_mode(output, mode, control_input, powerup)

    @conditional_reply("connected")
    def set_inname(self, input, value):
        self.device.set_input_sensor_name(input, value)
