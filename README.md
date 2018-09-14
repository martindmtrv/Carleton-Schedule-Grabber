# Carleton Schedule Grabber
Python script to parse HTML and extract course data from carleton central and create a new calendar in Google calendar for classes

# How do I use it?

Step 1:

Login to carleton central and visit your 'student timetable'

Step 2:

Scroll to the bottom of the page and click the 'detail schedule' link

Step 3:

Right click the page and Save As...
Save the page as 'schedule.html'

Step 4:

Put the downloaded html file in the directory with main.py and client_id.json (required for google authentication)

Step 5:

Run the python file; it will ask you to login to your google account (this program creates a new calendar called 'Carleton Schedule Grabber' so it won't overwrite existing events unless you have another calendar called 'Carleton Schedule Grabber')

Step 6:

Follow the prompts in the terminal; when it completes, profit by being organized this school year!

# How does it work?
Given the .html file containing the tables with timetable information this program can sift through and grab important information such as class, prof, location, times as well as being able to repeat courses weekly until the end of the semester!

This works by using python's built in regular expressions module to find <td> tags in the html which contain course info required in building the timetable.
