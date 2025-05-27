# ---------------------------------------------------------------------------------------------------------------------
from time import sleep
from hal.impl.led import OnBoardLed
from hal.impl.stdout import UartOut
from hal.impl.real_time_clock import I2CReadTimeClock, RealTimeClock, Timestamp
from pferdinand.constants import (
    PFERDINAND_ACTIVE_TIME_MS,
    PFERDINAND_ACTIVATE_AT,
    PFERDINAND_I2C_RTC_SDA_PIN,
    PFERDINAND_I2C_RTC_SCL_PIN,
    PFERDINAND_I2C_RTC_DEVICE_ADDRESS,
)
# ---------------------------------------------------------------------------------------------------------------------

led: OnBoardLed = OnBoardLed()
stdout: IStdOut = UartOut()
rtc: IRealTimeClock = I2CReadTimeClock(
    sda_pin_number=PFERDINAND_I2C_RTC_SDA_PIN,
    scl_pin_number=PFERDINAND_I2C_RTC_SCL_PIN,
    i2c_address=PFERDINAND_I2C_RTC_DEVICE_ADDRESS,
)
rtc.set_time(
    Timestamp().from_tuple(
        # (Jahr, 	Monat, 	Tag, 	Stunde, Minute, Sekunde, 	Wochentag)
        (25, 		5, 		27, 	21, 	39, 	0, 			2, 0)
    )
)

# spin...
while 1:
    #stdout.write(f'{rtc.now()}\n')
    print(f'{rtc.now()}\n')
    sleep(1)
    led.on()
    sleep(1)
    led.off()

# ---------------------------------------------------------------------------------------------------------------------