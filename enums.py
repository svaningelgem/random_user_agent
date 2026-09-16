from enum import Enum, auto


class OS(Enum):
    Windows = auto()
    Linux = auto()
    MacOSX = auto()
    Android = auto()
    iOS = auto()


class Chipset(Enum):
    # Linux
    x86 = "i686"
    x64 = "x86_64"
    # Mac
    Intel = "Intel"
    PPC = "PPC"
    UIntel = "U; Intel"
    UPPC = "U; PPC"

    def check_if_ok_for_os(self, os: OS):
        if (
            (os == OS.Linux and self not in (Chipset.x86, Chipset.x64))
            or (os == OS.MacOSX and self not in (Chipset.Intel, Chipset.UIntel, Chipset.PPC, Chipset.UPPC))
            # or: ignored on Windows
        ):
            raise ValueError(f"Invalid chipset {self} for os {os}.")


class Browser(Enum):
    Firefox = auto()
    Safari = auto()
    IExplorer = auto()
    Opera = auto()
    Chrome = auto()


class Language(Enum):
    en_US = "en-US"
    en_GB = "en-GB"
    sl_SI = "sl-SI"
    nl_NL = "nl-NL"
    fr_FR = "fr-FR"
