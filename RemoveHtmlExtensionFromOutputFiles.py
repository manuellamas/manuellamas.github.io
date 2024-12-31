import sys
import os.path
from os import listdir
import datetime

""" Instructions
Run the file without arguments
Removes extension from all html output files
"""


# Python File (Project) Location
program_directory = os.path.dirname(__file__) # Where the Python script being ran is
m_directory = "D:\\M"

# Website output html files location
output_files_directory = program_directory + "\\docs\\"

# list_files = [f for f in listdir(vault_thoughts_directory) if (os.path.isfile(os.path.join(vault_thoughts_directory, f)) and f[-2:]) == "md"]
for f in listdir(output_files_directory):
    if (os.path.isfile(os.path.join(output_files_directory, f)) and f[-5:] == ".html" and f != "index.html"): # Excluding index.html because I couldn't get Nginx to see it without the extension
        os.rename(os.path.join(output_files_directory, f), os.path.join(output_files_directory, f[:-5]))