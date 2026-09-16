import random
from copy import deepcopy
from datetime import date, datetime, timedelta

from enums import OS, Browser, Chipset, Language


def _random_date(start: datetime.date, end: datetime.date):
    """Generate a random datetime between `start` and `end`"""
    return start + timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


class _State:
    os = None
    chipset = None
    browser = None
    language = None


class RandomUserAgent:
    """
    Generates a random user agent to be used in HTTP requests as your browser.

    Defaults: completely randomized
    """

    def __init__(self):
        self._state = _State()

    ##################################################################
    # Quick access
    ##################################################################
    @property
    def os(self):
        return self._state.os

    @property
    def language(self):
        return self._state.language

    @property
    def browser(self):
        return self._state.browser

    @property
    def chipset(self):
        return self._state.chipset

    ##################################################################

    ##################################################################
    # select OS
    ##################################################################
    def linux(self):
        self._state.os = OS.Linux
        return self

    def windows(self):
        self._state.os = OS.Windows
        return self

    def macosx(self):
        self._state.os = OS.MacOSX
        return self

    def android(self):
        self._state.os = OS.Android
        return self

    def ios(self):
        self._state.os = OS.iOS
        return self

    ##################################################################

    ##################################################################
    # select chipset
    ##################################################################
    def x86(self):
        self._state.chipset = Chipset.x86
        return self

    def x64(self):
        self._state.chipset = Chipset.x64
        return self

    def intel(self):
        self._state.chipset = Chipset.Intel
        return self

    def ppc(self):
        self._state.chipset = Chipset.PPC
        return self

    def uintel(self):
        self._state.chipset = Chipset.UIntel
        return self

    def uppc(self):
        self._state.chipset = Chipset.UPPC
        return self

    ##################################################################

    ##################################################################
    # Select browser
    ##################################################################
    def firefox(self):
        self._state.browser = Browser.Firefox
        return self

    def safari(self):
        self._state.browser = Browser.Safari
        return self

    def iexplorer(self):
        self._state.browser = Browser.IExplorer
        return self

    def opera(self):
        self._state.browser = Browser.Opera
        return self

    def chrome(self):
        self._state.browser = Browser.Chrome
        return self

    ##################################################################

    ##################################################################
    def set_language(self, lang: Language):
        self._state.language = lang
        return self

    ##################################################################

    def _validate(self):
        try:
            Chipset.check_if_ok_for_os(self.chipset, self.os)
            return True
        except ValueError:
            pass

        return False

    def _randomize_os(self):
        if self._state.os:
            return

        while True:
            self._state.os = random.choice(list(OS.__members__.values()))
            if self._state.chipset and self._validate():
                return

    def _randomize_chipset(self):
        if self._state.chipset:
            return

        while True:
            self._state.chipset = random.choice(list(Chipset.__members__.values()))
            if self._validate():
                return

    def _randomize_browser(self):
        if self._state.browser:
            return

        self._state.browser = random.choice(list(Browser.__members__.values()))

    def _randomize_language(self):
        if self._state.language:
            return

        self._state.language = random.choice(list(Language.__members__.values()))

    def _randomize_firefox(self):
        ua = "Mozilla/5.0 "
        random_date = _random_date(date(2011, 1, 1), datetime.now().date()).strftime(
            "%Y%m%d"
        )
        ver = [
            f"Gecko/{random_date} Firefox/{random.randint(5, 7)}.0",
            f"Gecko/{random_date} Firefox/{random.randint(5, 7)}.0.1",
            f"Gecko/{random_date} Firefox/3.6.{random.randint(1, 20)}",
            f"Gecko/{random_date} Firefox/3.8",
        ]

        if self.os == OS.Windows:
            ua += f"(Windows NT {random.randint(5, 6)}.{random.randint(0, 1)}; "
            ua += self.language.value + "; "
            ua += f"rv:1.9.{random.randint(0, 2)}.20) "
            ua += random.choice(ver)
        elif self.os == OS.Linux:
            ua += f"(X11; Linux {self.chipset.value}; "
            ua += f"rv:{random.randint(5, 7)}.0) "
            ua += random.choice(ver)
        elif self.os == OS.MacOSX:
            ua += f"(Macintosh; {self.chipset.value} "
            ua += f"Mac OS X 10_{random.randint(5, 7)}_{random.randint(0, 9)} "
            ua += f"rv:{random.randint(2, 6)}.0) "
            ua += random.choice(ver)
        else:
            raise NotImplementedError

        return ua

    def _randomize_safari(self):
        ua = "Mozilla/5.0 "

        saf = (
            f"{random.randint(531, 535)}.{random.randint(1, 50)}.{random.randint(1, 7)}"
        )
        if random.randint(0, 1) == 0:
            ver = f"{random.randint(4, 5)}.{random.randint(0, 1)}"
        else:
            ver = f"{random.randint(4, 5)}.0.{random.randint(1, 5)}"

        if self.os == OS.Windows:
            ua += f"(Windows; U; Windows NT {random.randint(5, 6)}.{random.randint(0, 1)}) "
            ua += f"AppleWebKit/{saf} (KHTML, like Gecko) "
            ua += f"Version/{ver} "
            ua += f"Safari/{saf}"
        elif self.os == OS.MacOSX:
            ua += f"(Macintosh; U; {self.chipset.value} "
            ua += f"Mac OS X 10_{random.randint(5, 7)}_{random.randint(0, 9)} "
            ua += f"rv:{random.randint(2, 6)}.0; "
            ua += f"{self.language.value}) "
            ua += f"AppleWebKit/{saf} (KHTML, like Gecko) "
            ua += f"Version/{ver} "
            ua += f"Safari/{saf}"
        else:
            raise NotImplementedError

        return ua

    def _randomize_iexplorer(self):
        ua = f"Mozilla/{random.randint(4, 5)}.0 "
        ie_extra = [
            "",
            f"; .NET CLR 1.1.{random.randint(4320, 4325)}",
            "; WOW64",
        ]

        if self.os == OS.Windows:
            ua += "(compatible; "
            ua += f"MSIE {random.randint(5, 9)}.0; "
            ua += f"Windows NT {random.randint(5, 6)}.{random.randint(0, 1)}; "
            ua += f"Trident/{random.randint(3, 5)}.{random.randint(0, 1)})"
            ua += random.choice(ie_extra)
        else:
            raise NotImplementedError

        return ua

    def _randomize_opera(self):
        ua = f"Opera/{random.randint(8, 9)}.{random.randint(10, 99)} "

        op_extra = [
            "",
            f"; .NET CLR 1.1.{random.randint(4320, 4325)}",
            "; WOW64",
        ]

        if self.os == OS.Linux:
            ua += f"(X11; Linux {self.chipset.value}; U; "
            ua += f"{self.language.value}) "
            ua += f"Presto/2.9.{random.randint(160, 190)} "
            ua += f"Version/{random.randint(10, 12)}.00"
            ua += random.choice(op_extra)
        elif self.os == OS.Windows:
            ua += f"(Windows NT {random.randint(5, 6)}.{random.randint(0, 1)}; U; "
            ua += f"{self.language.value}) "
            ua += f"Presto/2.9.{random.randint(160, 190)} "
            ua += f"Version/{random.randint(10, 12)}.00"
            ua += random.choice(op_extra)
        else:
            raise NotImplementedError

        return ua

    def _randomize_chrome(self):
        ua = "Mozilla/5.0"
        saf = f"{random.randint(531, 536)}.{random.randint(0, 2)}"

        if self.os == OS.Linux:
            ua += f"(X11; Linux {self.chipset.value}) "
            ua += f"AppleWebKit/{saf} "
            ua += f"(KHTML, like Gecko) Chrome/{random.randint(13, 15)}.0.{random.randint(800, 899)}.0 "
            ua += f"Safari/{saf}"
        elif self.os == OS.Windows:
            ua += f"(Windows NT {random.randint(5, 6)}.{random.randint(0, 1)}) "
            ua += f"AppleWebKit/{saf} "
            ua += "(KHTML, like Gecko) "
            ua += f"Chrome/{random.randint(13, 15)}.0.{random.randint(800, 899)}.0 "
            ua += f"Safari/{saf}"
        elif self.os == OS.MacOSX:
            ua += f"(Macintosh; U; {self.chipset.value} Mac OS X "
            ua += f"10_{random.randint(5, 7)}_{random.randint(0, 9)}) "
            ua += f"AppleWebKit/{saf} "
            ua += "(KHTML, like Gecko) "
            ua += f"Chrome/{random.randint(13, 15)}.0.{random.randint(800, 899)}.0 "
            ua += f"Safari/{saf}"
        else:
            raise NotImplementedError

        return ua

    def build(self):
        current_state = deepcopy(self._state)

        error_counter = 20
        while error_counter > 0:  # Keep trying until you get a decent combination.
            try:
                self._randomize_os()
                self._randomize_chipset()
                self._randomize_browser()
                self._randomize_language()

                if not self._validate():
                    error_counter -= 1

                # Call it like _randomize_firefox
                return getattr(self, f"_randomize_{self._state.browser.name.lower()}")()
            except NotImplementedError:
                error_counter -= 1
                # restore previous state to try something else
                self._state = deepcopy(current_state)

        raise ValueError("Invalid combination passed. Can't handle this!")


if __name__ == "__main__":
    rua = RandomUserAgent()
    print(rua.linux().firefox().build())
