#!/usr/bin/env python3

from collections import namedtuple

####
# Here are all important constants defined
####

# RS232 terminator
RS232_TERM = b'\x0D\x0A'

#### main dataset ####

BOOL_TYPE = "BOOL"
FLOAT_TYPE = "FLOAT"
INT_TYPE = "INTEGER"
SHORT_ENUM_TYPE = "INTEGER_SHORT"


# description values
_datapoint = namedtuple("Datapoint", "id name", rename=False)


SMART_BOOST_ALLOWED = _datapoint(1126, "SMART_BOOST_ALLOWED")
BATTERY_CHARGE_CURR = _datapoint(1138, "BATTERY_CHARGE_CURR")
SMART_BOOST_LIMIT = _datapoint(1607, "SMART_BOOST_LIMIT")

AC_OUTPUT_VOLTAGE = _datapoint(1286, "AC_OUTPUT_VOLTAGE")

PARAMS_SAVED_IN_FLASH = _datapoint(1550, "PARAMS_SAVED_IN_FLASH")

AC_IN_POWER = _datapoint(3081, "AC_IN_POWER")
ENERGY_USAGE = _datapoint(3083, "ENERGY_USAGE")

POWER_IN = _datapoint(3136, "POWER_IN")
POWER_OUT = _datapoint(3137, "POWER_OUT")

USER_LEVEL = _datapoint(5012, "USER_LEVEL")

BATT_VOLTAGE = _datapoint(7000, "BATT_VOLTAGE")
BATT_CURRENT = _datapoint(7001, "BATT_CURRENT")
STATE_OF_CHARGE = _datapoint(7002, "STATE_OF_CHARGE")

FORCE_NEW_CYCLE = _datapoint(10029, "FORCE_NEW_CYCLE")
PV_POWER = _datapoint(11004, "PV_POWER")
PROD_ENERGY_CURR_DAY = _datapoint(11007, "PROD_ENERGY_CURR_DAY")
PROD_ENERGY_PREV_DAY = _datapoint(11011, "PROD_ENERGY_PREV_DAY")
OPERATION_MODE = _datapoint(11016, "OPERATION_MODE")
NUM_MAX_POWER_CURR_DAY = _datapoint(11019, "NUM_MAX_POWER_CURR_DAY")
NUM_SUN_HOURS_CURR_DAY = _datapoint(11025, "NUM_SUN_HORS_CURR_DAY")
BAT_CYCLE_PHASE = _datapoint(11038, "BAT_CYCLE_PHASE")

# data type values
DATASET = {
    SMART_BOOST_ALLOWED.id: BOOL_TYPE,
    BATTERY_CHARGE_CURR.id: FLOAT_TYPE,
    SMART_BOOST_LIMIT.id: FLOAT_TYPE,
    AC_OUTPUT_VOLTAGE.id: FLOAT_TYPE,
    PARAMS_SAVED_IN_FLASH.id: BOOL_TYPE,
    AC_IN_POWER.id: FLOAT_TYPE,
    ENERGY_USAGE.id: FLOAT_TYPE,
    POWER_IN.id: FLOAT_TYPE,
    POWER_OUT.id: FLOAT_TYPE,
    USER_LEVEL.id: INT_TYPE,
    BATT_VOLTAGE.id: FLOAT_TYPE,
    BATT_CURRENT.id: FLOAT_TYPE,
    STATE_OF_CHARGE.id: FLOAT_TYPE,
    FORCE_NEW_CYCLE.id: INT_TYPE,
    PV_POWER.id: FLOAT_TYPE,
    PROD_ENERGY_CURR_DAY.id: FLOAT_TYPE,
    PROD_ENERGY_PREV_DAY.id: FLOAT_TYPE,
    NUM_MAX_POWER_CURR_DAY.id: FLOAT_TYPE,
    NUM_SUN_HOURS_CURR_DAY.id: FLOAT_TYPE,
    OPERATION_MODE.id: SHORT_ENUM_TYPE,
    BAT_CYCLE_PHASE.id: SHORT_ENUM_TYPE,
}

####


### service_id
READ_PROPERTY = b'\x01'
WRITE_PROPERTY = b'\x02'

### object_type
TYPE_INFO = b'\x01\x00'
TYPE_PARAMETER = b'\x02\x00'
TYPE_MESSAGE = b'\x03\x00'
TYPE_DATALOG = b'\x05\x00'

### property_id
VALUE_QSP = b'\x05\x00'
MIN_QSP = b'\x06\x00'
MAX_QSP = b'\x07\x00'
LEVEL_QSP = b'\x08\x00'
UNSAVED_VALUE_QSP = b'\x0D\x00'

# values for LEVEL_QSP
VIEW_ONLY = b'\x00\x00'
BASIC = b'\x10\x00'
EXPERT = b'\x20\x00'
INSTALLER = b'\x30\x00'
QSP = b'\x40\x00'

# values for Operating mode (11016)
MODE_NIGHT = 0
MODE_STARTUP = 1
MODE_CHARGER = 3
MODE_SECURITY = 5
MODE_OFF = 6
MODE_CHARGE = 8
MODE_CHARGE_V = 9
MODE_CHARGE_I = 10
MODE_CHARGE_T = 11

# values for Battery cycle phase (11038)
PHASE_BULK = 0
PHASE_ABSORPT = 1
PHASE_EQUALIZE = 2
PHASE_FLOATING = 3
PHASE_R_FLOAT = 6
PHASE_PER_ABS = 7

### error codes
ERROR_CODES = {
    b'\x01\x00': "INVALID_FRAME",
    b'\x02\x00': "DEVICE_NOT_FOUND",
    b'\x03\x00': "RESPONSE_TIMEOUT",
    b'\x11\x00': "SERVICE_NOT_SUPPORTED",
    b'\x12\x00': "INVALID_SERVICE_ARGUMENT",
    b'\x13\x00': "SCOM_ERROR_GATEWAY_BUSY",
    b'\x21\x00': "TYPE_NOT_SUPPORTED",
    b'\x22\x00': "OBJECT_ID_NOT_FOUND",
    b'\x23\x00': "PROPERTY_NOT_SUPPORTED",
    b'\x24\x00': "INVALID_DATA_LENGTH",
    b'\x25\x00': "PROPERTY_IS_READ_ONLY",
    b'\x26\x00': "INVALID_DATA",
    b'\x27\x00': "DATA_TOO_SMALL",
    b'\x28\x00': "DATA_TOO_BIG",
    b'\x29\x00': "WRITE_PROPERTY_FAILED",
    b'\x2A\x00': "READ_PROPERTY_FAILED",
    b'\x2B\x00': "ACCESS_DENIED",
    b'\x2C\x00': "SCOM_ERROR_OBJECT_NOT_SUPPORTED",
    b'\x2D\x00': "SCOM_ERROR_MULTICAST_READ_NOT_SUPPORTED",
    b'\x2E\x00': "OBJECT_PROPERTY_INVALID",
    b'\x2F\x00': "FILE_OR_DIR_NOT_PRESENT",
    b'\x30\x00': "FILE_CORRUPTED",
    b'\x81\x00': "INVALID_SHELL_ARG",
}
