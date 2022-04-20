import enum

BOOTSTRAP_SERVER: str = "localhost:29092"
SCHEMA_REGISTRY_URL: str = "http://localhost:8081"
TOPIC: str = "corporate-events"


class State(str, enum.Enum):
    BADEN_WUETTEMBERG = "bw"
    BAYERN = "by"
    BERLIN = "be"
    BRANDENBURG = "br"
    BREMEN = "hb"
    HAMBURG = "hh"
    HESSEN = "he"
    MECKLENBURG_VORPOMMERN = "mv"
    NIEDERSACHSEN = "ni"
    NORDRHEIN_WESTFALEN = "nw"
    RHEILAND_PFALZ = "rp"
    SAARLAND = "sl"
    SACHSEN = "sn"
    SACHSEN_ANHALT = "st"
    SCHLESWIG_HOLSTEIN = "sh"
    THUERINGEN = "th"
