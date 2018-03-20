from difflib import SequenceMatcher
import jellyfish
import os
pyaccessibility_path = os.path.dirname(os.path.abspath(__file__))
files_in_folders = os.listdir(pyaccessibility_path)
for each in files_in_folders:
    if each.endswith(".py"):
        if each.startswith("__init__") is False:
            execfile(os.path.join(pyaccessibility_path, each))
