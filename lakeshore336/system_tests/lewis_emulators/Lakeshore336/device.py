from collections import OrderedDict
from enum import Enum
from .states import DefaultState
from lewis.devices import StateMachineDevice


class SimulatedLksh336(StateMachineDevice):

    def _initialize_data(self):
        self.connected = True
        
    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])
