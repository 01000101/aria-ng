
from .validation import ValidationContext
from .implementation import ImplementationContext
from .style import Style
import sys

class ConsumptionContext(object):
    def __init__(self):
        self.presentation = None
        self.out = sys.stdout
        self.style = Style()
        self.args = []
        self.validation = ValidationContext()
        self.implementation = ImplementationContext()