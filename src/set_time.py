# ---------------------------------------------------------------------------------------------------------------------
from pferdinand.constants import (
    PFERDINAND_DIGITAL_OUTPUT_PIN_NUMBER,
    PFERDINAND_ACTIVE_TIME_MS,
    PFERDINAND_ACTIVATE_AT,
    PFERDINAND_I2C_RTC_SDA_PIN,
    PFERDINAND_I2C_RTC_SCL_PIN,
    PFERDINAND_I2C_RTC_DEVICE_ADDRESS,
)
# ---------------------------------------------------------------------------------------------------------------------

led: OnBoardLed = OnBoardLed()
rtc: IRealTimeClock = I2CReadTimeClock(
    sda_pin_number=PFERDINAND_I2C_RTC_SDA_PIN,
    scl_pin_number=PFERDINAND_I2C_RTC_SCL_PIN,
    i2c_address=PFERDINAND_I2C_RTC_DEVICE_ADDRESS,
)
rtc.set_time(
    Timestamp().from_tuple(
        # (Jahr, 	Monat, 	Tag, 	Stunde, Minute, Sekunde, 	Wochentag)
        (25, 		11, 	22, 	23, 	50, 	30, 		7)
    )
)

# spin...
while 1:
    print(a.now())
    sleep(1)
    led.on()
    sleep(1)
    led.off()

# ---------------------------------------------------------------------------------------------------------------------