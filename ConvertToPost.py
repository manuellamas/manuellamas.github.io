import sys
import os
from os import listdir
import datetime

""" Instructions
Run the file with no arguments to convert the post note with today's date attribute
OR
Give an argument (date in format YYYY-mm-dd) to convert the note with that date attribute
OR
Give the argument "all" and it runs on all posts present (useful for some kind of global reformatting)
"""


FIELD_TITLE = "title"
FIELD_DATE = "date"
FIELD_LINK = "link"


# Python File (Project) Location
program_directory = os.path.dirname(__file__) # Where the Python script being ran is
website_directory = os.path.split(program_directory)[0]
m_directory = "D:\\M"

## Obsidian original MD location
# SSD Location where I'll move Obsidian to, in an attempt to achieve faster loading times, as the first loading of Obsidian (per boot) is quite slow ~20s.
vault_thoughts_directory = "C:\\Users\\ManuelLamas\\Documents\\M\\Sihlbi_World\\Thoughts"
# Previous location in second disk (HDD)
# vault_thoughts_directory = m_directory + "\\Sihlbi_World\\Thoughts"

# Website posts location
posts_directory = program_directory + "\\source\\_posts"

# Obtain a list of the file names of all .md files in the thoughts directory (in Obsidian).
# Only those in the "root" and not in a subdirectory. So be careful if you plan to place them on subfolders
list_files = [f for f in listdir(vault_thoughts_directory) if (os.path.isfile(os.path.join(vault_thoughts_directory, f)) and f[-2:]) == "md"]



def obsidianToPost(note_date = datetime.datetime.now().strftime("%Y-%m-%d"), all = False):
    """ Creates (or updates) a post in the website source files by getting the content
    from the Obsidian Note with the corresponding date (or if ommited the date of today)  """
    date = "" # Initializing the variable
    note_title = ""
    lines = ""


    for i in range(len(list_files)):

        file = open(vault_thoughts_directory + "\\" + list_files[i], "r")
        
        lines = file.readlines() # List with all the lines of the file



        date_line = lines[1] # Second line of the file
        file.close()

        date = date_line.replace("date: ", "").replace("\n", "")
        year = note_date[:4]
        # post_date = date_line[6:16]

        if date == note_date:
            # Get file_name
            note_title = list_files[i]
            break


    frontMatter, noteContent = splitFrontAndContent(lines)

    link_title = findFrontMatterField(FIELD_LINK, frontMatter).lower().replace(" ", "-")
    date = findFrontMatterField(FIELD_DATE, frontMatter)
    # date = date_line.replace("date: ", "").replace("\n", "")



    if note_title != "":
        # Checking if there's no note (already as on the website) has the same title or link
        # if check_same_title(note_date[:4], note_title, link_title):
        if check_same_title(note_title, link_title):
            return

        # Create the .md file in the _posts directory
        file_name = note_title.lower().replace(" ","-")
        post_title = date + "-" + file_name
        post_file = open(posts_directory + "\\" + post_title, "w")

        print(note_title)
        print(post_title)
        note_file = open(vault_thoughts_directory + "\\" + note_title, "r")
        note_lines = note_file.readlines()
        # note_content = note_lines[5:] # Ignores the first five lines (original yaml frontmatter)

        # To be added at the beginning of the file

        if not all: # If we're not changing all thoughts
            if note_date == datetime.datetime.now().strftime("%Y-%m-%d"): # If the date is the one of today, update "latest" link
                update_latest(link_title)
                print("The link to latest was updated to", link_title)
            else:
                reply = input("Is the thought being updated the latest? y/n\n")
                if reply.lower() == "y":
                    update_latest(link_title)
                    print("The link to latest was updated to", link_title)
                else:
                    print("The link to latest wasn't updated.")


        link = "permalink: /" + link_title
        thought_title = findFrontMatterField(FIELD_TITLE, frontMatter)
        # link = "permalink: /" + year +  "/" + link_title
        yaml_header = "---\nlayout: post\n" + link
        if thought_title is not None:
            yaml_header += "\ntitle: " + thought_title

        yaml_header += "\n---\n"
        post_file.write(yaml_header)
        print(link_title)

        for line in noteContent:
            post_file.write(line)

        # Close files
        post_file.close()
        note_file.close()
    else:
        print("No note with that date was found")



def check_same_title(title, link):
    """ Checks if there's already a post with the same title or link """
    # Now checking for all notes (and not just in the same year)
    # def check_same_title(year, title, link):

    # Remove the file in question from the list. We're using the date itself 
    list_files_exclude = list_files[:] # Creating a copy of the list
    list_files_exclude.remove(title) # This only removes one instance of the list.
    # I.e., if there are two that are the same, only one will be removed and it'll still detect that there's another file with the same title/link

    for file in list_files_exclude:
        same_title_link = False # If there's a file with same title or link

        with open(vault_thoughts_directory + "\\" + file, "r") as file_note:
            lines = file_note.readlines()
            date = lines[1][6:-1] # Getting the date
            # date_year = date[:4] # Getting the year

            # if date != "" and date_year == year: # Checking only the files that have date, and the date year is the same
            if file == title:
                print("There's already a file with that title")
                print(date)
                print(file) # Title
                print(lines[2][6:]) # Link
                same_title_link = True
                break
            elif link == lines[2][6:]:
                print("There's already a file with that link")
                print(date)
                print(file) # Title
                print(lines[2][6:]) # Link
                same_title_link = True
                break

    return same_title_link



def update_latest(link):
    """ Updates the latest.html source file to link to the newly created thought """
    latest_html_location = program_directory + "/source/latest.html" # Location of latest.html

    # Reading the file
    with open(latest_html_location, "r") as latest_html:
        read_lines = latest_html.readlines()

    # Editing the line with the link
    with open(latest_html_location, "w") as latest_html:
        read_lines[3] = 'meta-redirect: <meta http-equiv = "refresh" content = "0; url = /' + link + '" />' + '\n'
        read_lines[5] = 'For the latest thought please follow <a href="/' + link + '">this link</a>.'
        latest_html.writelines(read_lines)



def splitFrontAndContent(lines):
    # Define which lines are of the yaml front matter
    finalSeparatorFound = False
    finalSeparatorLine = 1 # Ignoring the first (0) as it'll have to be the first "---"
    while (not finalSeparatorFound):
        if finalSeparatorLine == len(lines):
            print("The front matter of this note does not have a final separator line '---'")
            break
        if lines[finalSeparatorLine].strip() == "---":
            finalSeparatorFound = True
        finalSeparatorLine += 1

    frontMatter = lines[1:finalSeparatorLine-1]
    noteContent = lines[finalSeparatorLine:]
    return frontMatter, noteContent



def findFrontMatterField(fieldName, frontMatter):
    for line in frontMatter:
        key, value = line.split(": ", 1)
        if fieldName == key:
            return value.replace("\n","")
    return



if __name__ == "__main__":

    if len(sys.argv) == 1: # No file specified so it looks for the note that has the date attribute of today
        obsidianToPost()

    else: # Searches for the note with the specified date
        if sys.argv[-1].lower() == "all": # Run on all posts
            
            # Obsidian original MD location
            # vault_thoughts_directory = m_directory + "\\Sihlbi_World\\Thoughts"

            # Website posts location
            posts_directory = program_directory + "\\source\\_posts"

            # Obtain a list of the file names of all .md files in the thoughts directory (in Obsidian).
            # Only those in the "root" and not in a subdirectory. So be careful if you plan to place them on subfolders
            print(vault_thoughts_directory)
            list_files = [f for f in listdir(vault_thoughts_directory) if (os.path.isfile(os.path.join(vault_thoughts_directory, f)) and f[-2:]) == "md"]

            # Get Dates (just because that's the input that obsidianToPost allows)
            list_file_dates = []
            for i in range(len(list_files)):
                file = open(vault_thoughts_directory + "\\" + list_files[i], "r")

                lines = file.readlines() # List with all the lines of the file
                date_line = lines[1] # Second line of the file
                file.close()

                date = date_line.replace("date: ", "").replace("\n", "")
                
                if date != "":
                    list_file_dates.append(date)

            for date in list_file_dates: # Running on all files
                obsidianToPost(date, all = True)
                print("---\n")

        else: # Running on specific file with the given date
            note_date = sys.argv[-1]
            obsidianToPost(note_date)


    confimationToRunFinalScripts = input("Run Jekyll build and RemoveHtmlExtension script? (Enter for Yes)")
    if confimationToRunFinalScripts.lower() in ["", "yes"]:
        # Run Jekyll build command
        jekyllBuildOutput = os.popen('powershell -Command bundle exec jekyll build').read()
        print(jekyllBuildOutput)
        print("-----\nThe Jekyll Build command was executed")

        # Run script to remove html extensions of the output files. Needed for my current configuration of NginX on Mlair
        removeHtmlExtensionOutput = os.popen('powershell -Command py .\RemoveHtmlExtensionFromOutputFiles.py').read()
        print(removeHtmlExtensionOutput)
        print("-----\nThe RemoveHtmlExtensionFromOutputFiles python script was executed")
