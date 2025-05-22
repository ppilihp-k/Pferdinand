# ---------------------------------------------------------------------------------------------------------------------
import machine
from time import time, gmtime, mktime
from hal.interfaces.types import Timestamp
from hal.interfaces.ireal_time_clock import IRealTimeClock
from machine import Pin, I2C
# ---------------------------------------------------------------------------------------------------------------------

class I2CReadTimeClock(IRealTimeClock):
    """External RTC connected via i2c.

    Device used: https://www.az-delivery.de/products/ds3231-real-time-clock?variant=27476099401&utm_source=google&utm_medium=cpc&utm_campaign=16964979024&utm_content=166733588295&utm_term=&gad_source=1&gad_campaignid=16964979024&gbraid=0AAAAADBFYGUJ0vUbnnnE4KXz5xGjdidOc&gclid=EAIaIQobChMIqMDCgb-3jQMV06WDBx2ynSMPEAQYASABEgKsFfD_BwE
    See Device Docs: https://www.analog.com/media/en/technical-documentation/data-sheets/ds3231.pdf

    MicroPython:
        i2c: https://docs.micropython.org/en/latest/library/machine.I2C.html
    """
    def __init__(self, sda_pin_number: int, scl_pin_number: int, i2c_address: int):
        self.__i2c: I2C = I2C(0, sda=Pin(sda_pin_number), scl=Pin(scl_pin_number), freq=100000)
        self.__i2c_address: int = i2c_address
        print(
            self.__i2c.writeto(
                self.__i2c_address,
                bytes(
                    [0x0f],
                ),
            )
        )
        print(
            self.__i2c.readfrom(
                 self.__i2c_address,
                 1,
            )
        )
        pass

    def double_dabble(self, bin_value: int) -> int:
        """Algorithm from: https://blog.smittytone.net/2020/12/03/clock-design-explore-bcd/"""
        for i in range(0, 8):
            # Multiply by 2
            bin_value = bin_value << 1

            # Final op is always a shift, so break out when done
            if i == 7: break

            # If the BCD units value (bits 8-11)  is 5 or more, add 3
            if (bin_value & 0xF00) > 0x4FF: bin_value += 0x300

            # If the BCD tens value (bits 12-15) is 5 or more, add 3
            if (bin_value & 0xF000) > 0x4FFF: bin_value += 0x3000
        return (bin_value >> 8) & 0xFF

    def set_time(self, timestamp: Timestamp) -> 'Self':
        # (Jahr, Monat, Tag, Stunde, Minute, Sekunde, Wochentag)
        ts = timestamp.to_tuple()
        print(f'Convert {ts} to BCD')
        year: int = self.double_dabble(ts[0])
        month: int = self.double_dabble(ts[1])
        day: int = self.double_dabble(ts[2])
        hours: int = self.double_dabble(ts[3])
        minutes: int = self.double_dabble(ts[4])
        seconds: int = self.double_dabble(ts[5])
        weekday: int = self.double_dabble(ts[6])

        print(f'Year: {year}, M:{month}, d:{day}, h:{hours}, m:{minutes}, s:{seconds}, wd:{weekday}')

        data: bytes = self.__read_timekeeping_registers()
        self.__i2c.writeto(
            self.__i2c_address,
            bytes(
                [
                    0x00, # Register Address Byte
                    seconds & 0x7f, # Data Seconds
                    minutes & 0x7f, # Minutes
                    data[2] & 0x40 | hours, # Hours
                    weekday & 0x7, # Day 0-7
                    day & 0x3f, # Date 0 - 31
                    month & 0x1f, # Month
                    year & 0xff, # Year
                ],
            ),
        )
        return self

    def __read_timekeeping_registers(self) -> bytes:
        self.__i2c.writeto(
            self.__i2c_address,
            bytes(
                [0x00],
            ),
        )
        return self.__i2c.readfrom(
             self.__i2c_address,
             0x07,
        )

    def now(self) -> Timestamp:
        data: bytes = self.__read_timekeeping_registers()
        # (Jahr, Monat, Tag, Stunde, Minute, Sekunde, Wochentag)
        return Timestamp().from_tuple(
            (
                (data[6] & 0xf) + (data[6] >> 4) * 10,
                (data[5] & 0xf) + ((data[5] >> 4) & 0x1) * 10,
                (data[4] & 0xf) + (data[4] >> 4) * 10,
                (data[2] & 0xf) + (data[2] >> 4) * 10,
                (data[1] & 0xf) + (data[1] >> 4) * 10,
                (data[0] & 0xf) + (data[0] >> 4) * 10,
                (data[3] & 0x7),
                0 # daylight saving time...
            )
        )

    pass

# ---------------------------------------------------------------------------------------------------------------------

class RealTimeClock(IRealTimeClock):

    def __init__(self):
        self.__rtc = machine.RTC()
        pass

    def set_time(self, timestamp: Timestamp) -> 'Self':
        return self

    def now(self) -> Timestamp:
        return Timestamp().from_tuple(
            self.__rtc.datetime()
        )

    def start_of_day(self) -> Timestamp:
        return self.now().set_time(0, 0, 0)

    pass
# ---------------------------------------------------------------------------------------------------------------------
