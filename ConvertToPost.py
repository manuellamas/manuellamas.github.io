import sys
import os.path
from os import listdir
import datetime

""" Instructions
Run the file with no arguments to convert the post note with today's date attribute
OR
Give an argument (date in format YYYY-mm-dd) to convert the note with that date attribute
"""

def obsidianToPost(note_date = datetime.datetime.now().strftime("%Y-%m-%d")):
    # Python File (Project) Location
    program_directory = os.path.dirname(__file__) # Where the Python script being ran is
    website_directory = os.path.split(program_directory)[0]
    projects_directory = os.path.split(website_directory)[0]
    m_directory = os.path.split(projects_directory)[0]

    # Obsidian original MD location
    vault_directory = m_directory + "\\Sihlbi_World\\Thoughts"

    # Website posts location
    posts_directory = program_directory + "\\source\\_posts"

    # Obtain a list of the file names of all .md files in the thoughts directory (in Obsidian).
    # Only those in the "root" and not in a subdirectory. So be careful if you plan to place them on subfolders
    list_files = [f for f in listdir(vault_directory) if (os.path.isfile(os.path.join(vault_directory, f)) and f[-2:]) == "md"]

    date = "" # Initializing the variable
    note_title = ""

    for i in range(len(list_files)):

        file = open(vault_directory + "\\" + list_files[i], "r")
        
        lines = file.readlines() # List with all the lines of the file
        date_line = lines[1] # Second line of the file
        file.close()

        date = date_line.replace("date: ", "").replace("\n", "")
        # post_date = date_line[6:16]

        if date == note_date:
            # Get file_name
            note_title = list_files[i]
            break

    if note_title != "":
        # Create the .md file in the _posts directory
        file_name = note_title.lower().replace(" ","-")
        post_title = date + "-" + file_name
        post_file = open(posts_directory + "\\" + post_title, "w")

        print(note_title)
        print(post_title)
        note_file = open(vault_directory + "\\" + note_title, "r")
        note_lines = note_file.readlines()
        note_content = note_lines[4:] # Ignores the first four lines (original yaml frontmatter)

        # To be added at the beginning of the file
        link_title = note_lines[2][6:-1].lower().replace(" ", "-")
        link = "permalink: /" + link_title + ".html"
        yaml_header = "---\nlayout: post\n" + link + "\n---\n"
        post_file.write(yaml_header)

        for line in note_content:
            post_file.write(line)

        # Close files
        post_file.close()
        note_file.close()
    else:
        print("No note with that date was found")


if __name__ == "__main__":

    if len(sys.argv) == 1: # No file specified so it looks for the note that has the date attribute of today
        obsidianToPost()

    else: # Searches for the note with the specified date
        note_date = sys.argv[-1]
        obsidianToPost(note_date)