import sys
import os.path
from os import listdir
import datetime

""" Instructions
Run the file with no arguments to convert the post note with today's date attribute
OR
Give an argument (date in format YYYY-mm-dd) to convert the note with that date attribute
OR
Give the argument "all" and it runs on all posts present (useful for some kind of global reformatting)
"""


# Python File (Project) Location
program_directory = os.path.dirname(__file__) # Where the Python script being ran is
m_directory = "D:\\M"

# Website output html files location
output_files_directory = program_directory + "\\docs\\"

# list_files = [f for f in listdir(vault_thoughts_directory) if (os.path.isfile(os.path.join(vault_thoughts_directory, f)) and f[-2:]) == "md"]
for f in listdir(output_files_directory):
    if (os.path.isfile(os.path.join(output_files_directory, f)) and f[-5:]) == ".html":
        os.rename(os.path.join(output_files_directory, f), os.path.join(output_files_directory, f[:-5]))