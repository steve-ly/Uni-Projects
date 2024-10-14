#!/usr/bin/env python
"""
This script sends a print-state request to the server

Use if debugging the front-end to get a print-out of the entire program state
"""

from . import call_wrappers as cw

cw.print_state()
