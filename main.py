import platform
import json


if platform.system() == "Linux":
    from linux_platform import *


if __name__ == "__main__":
    import code
    code.interact(local=locals())
