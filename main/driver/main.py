"""
APPLICATION DRIVER
"""

# Global set def: application state
# Possible app states => IDLE, MANAGE, REPORT, CONNECTING
ALLOWED_APP_STATES = {'REPORT', 'MANAGE', 'IDLE', 'CONNECTING'}
CURRENT_STATE = 'IDLE'