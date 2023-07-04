# Carleton Schedule Grabber
Node script to parse HTML and extract course data from carleton central and create a new calendar in ICS format

# How do I use it?

### Step 0:

Clone this repo and install the dependencies. Ensure that you have node and yarn installed or use nvm to get the correct version required

```
git clone https://github.com/martindmtrv/Carleton-Schedule-Grabber.git

nvm

yarn
```

### Step 1:

Login to carleton central and visit your 'student timetable'

### Step 2:

Scroll to the bottom of the page and click the 'detail schedule' link

### Step 3:

Right click the page and Save As...
Save the page as 'schedule.html'

### Step 4:

Put the downloaded html file in the directory where the code is

### Step 5:

Run the program:

```
yarn run
```

It should generate a file called `newcal.ics` which will contain all the course information and can be imported into various calendar software such as [google calendar](https://support.google.com/calendar/answer/37118?hl=en&co=GENIE.Platform%3DDesktop).

# How does it work?
Given the .html file containing the tables with timetable information this program can sift through and grab important information such as class, prof, location, times as well as being able to repeat courses weekly until the end of the semester!

This works by using a nodejs in regular expressions module to find <td> tags in the html which contain course info required in building the timetable.
