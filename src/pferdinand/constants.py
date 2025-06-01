"""Hier werden Konstanten abgelegt."""
# ---------------------------------------------------------------------------------------------------------------------
PFERDINAND_DIGITAL_OUTPUT_0_PIN_NUMBER: int = 2
PFERDINAND_DIGITAL_OUTPUT_1_PIN_NUMBER: int = 3
PFERDINAND_ACTIVE_TIME_MS: int = 20000
# (Jahr, Monat, Tag, Stunde, Minute, Sekunde, Wochentag, daylight-saving (always 0...))
PFERDINAND_ACTIVATE_AT: tuple = (25, 0, 0, 3, 0, 0, 0, 0)

# RTC related...
PFERDINAND_I2C_RTC_SDA_PIN: int = 20
PFERDINAND_I2C_RTC_SCL_PIN: int = 21
PFERDINAND_I2C_RTC_DEVICE_ADDRESS: int = 0x68

# Digial Input for Switch
PFERDINAND_SWITCH_INPUT_0: int = 14
PFERDINAND_SWITCH_INPUT_1: int = 15
PFERDINAND_INPUT_BUFFER_SIZE: int = 32
# ---------------------------------------------------------------------------------------------------------------------
