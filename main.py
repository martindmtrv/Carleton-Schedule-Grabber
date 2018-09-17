# import standard library modules
import re
import calendar
import os
import datetime

# google calendar api modules
try:
    from googleapiclient.discovery import build
    from oauth2client import file, client, tools
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    os.system('pip3 install --upgrade google-api-python-client')
    os.system('pip3 install --upgrade oauth2client')
    os.system('pip3 install --upgrade google_auth_oauthlib')
    os.system('clear')
    from googleapiclient.discovery import build
    from oauth2client import file, client, tools
    from google_auth_oauthlib.flow import InstalledAppFlow

def userAuth():
    # start user auth flow with google calendar scope
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_id.json',
        scopes=['https://www.googleapis.com/auth/calendar'])

    # go to google sign-on page and ask for user to login
    credentials = flow.run_local_server(host='localhost',
        port=8080,
        authorization_prompt_message='Sign in in the browser!',
        success_message='The auth flow is complete; you may close this window.',
        open_browser=True)

    # build google calendar service
    service = build('calendar','v3', credentials=credentials)
    return service

def militaryClock(time):
    if time[:2] == '12' and time[-2:] == 'am':    # if 12:00am set time to 00:00
        time = '00:00'
    elif time[-2:] == 'am':   # check if time is am or pm
        time = time[:-3]
    elif time [-2:] == 'pm':    # check if time is pm
        colon = time.find(':')
        if not int(time[:colon]) == 12:
            time = str(int(time[:colon]) + 12) + str(time[colon:-3])
        else:
            time = '12' + time[colon:-3]
    return time

def firstClass(code,span):
    weekDays = []
    for letter in code:
        # append number correspondant to day codes
        if letter == 'M': weekDays.append(0)
        if letter == 'T': weekDays.append(1)
        if letter == 'W': weekDays.append(2)
        if letter == 'R': weekDays.append(3)
        if letter == 'F': weekDays.append(4)

    # find month number
    if span[:3] == 'Jan': month = '01'
    if span[:3] == 'Sep': month = '09'
    if span[:3] == 'Dec': month = '12'
    if span[:3] == 'May': month = '05'
    if span[:3] == 'Jun': month = '06'
    if span[:3] == 'Jul': month = '07'
    if span[:3] == 'Aug': month = '08'

    # find start date number:
    date = span[4:6]

    # find year
    dash = span.find('-')
    year = int(span[dash-5:dash-1])
    # get a list of tuples with date and day type
    chart = calendar.Calendar(year).monthdays2calendar(year,int(month))
    found = False

    for week in chart:
        for day in week:
            for classDay in weekDays:
                if day[0] >= int(date):
                    if day[1] == classDay:
                        firstDayNum = day[0]
                        found = True
                        break
            if found:
                break
        if found:
            break

    if len(str(firstDayNum)) == 1:
        firstDayNum = '0'+str(firstDayNum)
    else:
        firstDayNum = str(firstDayNum)
    return str(year) + '-' + month + '-' + firstDayNum + 'T'

def lastClass(span):
    dash = span.find('-')

    # find month number
    if span[dash+2:dash+5] == 'Jan': month = '01'
    if span[dash+2:dash+5] == 'Apr': month = '04'
    if span[dash+2:dash+5] == 'Sep': month = '09'
    if span[dash+2:dash+5] == 'Dec': month = '12'
    if span[dash+2:dash+5] == 'May': month = '05'
    if span[dash+2:dash+5] == 'Jun': month = '06'
    if span[dash+2:dash+5] == 'Jul': month = '07'
    if span[dash+2:dash+5] == 'Aug': month = '08'

    # find start date number:
    date = span[dash+6:dash+8]

    # find year
    year = int(span[-4:])
    return str(year) + month + date

def infoGrabber():
    while True:
        try:
            with open('schedule.html', 'r') as sourceFile:
                input('Found schedule.html press enter to start!')
                # convert the source code to a string
                htmlFile = str(sourceFile.read())

                # find all the table headers (class names) and the table data (class times)
                headers = re.findall(r'<a[^>]*>([^<]+)</a>', htmlFile, flags=re.IGNORECASE)
                table = re.findall(r'<td[^>]*>([^<]+)</td>', htmlFile, flags=re.IGNORECASE)

                # table data pattern: n/a, n/a, prof, n/a, n/a, n/a, n/a, n/a, time, day char, location, range, type, n/a
                """
                ---- Legend ----
                prof = index 3
                time = index 9
                dayChar = index 10
                location = index 11
                range = index 12 (might be irrelevant)
                type = index 13
                NEW COURSE BLOCK EVERY 14 indices
                """

                # initialize variables
                info = []
                #table = table[2:]
                if table[0][0] == '\n':
                    del table[0]
                headers = headers[8:-4]
                x = 0

                # clear random strings in html code to keep pattern consistent
                for index, item in enumerate(table,0):
                    if item[0] == '&':
                        del table[index]

                # run this loop until out of course data
                while table != []:
                    # initialize temporary dictionary
                    course = {}
                    
                    # get rid of online only classes (they don't belong in calendar)
                    if table[9] == 'Video on Demand':
                        table = table[10:]
                        
                    # if index 2 isn't in regular prof style add an empty block
                    if table[3][0] != '\n':
                        table.insert(3,'N/A')
                        course['prof'] = 'N/A'

                    # if location is TBA add that
                    try:
                        if table[11][:3] == 'Sep' or table[11][:3] == 'Dec' or table[11][:3] == 'May' or table[11][:3] == 'Jun' or table[11][:3] == 'Jul' or table[11][:3] == 'Aug' or table[11][:3] == 'Jan':
                            table.insert(11,'TBA')

                    # if there is no location (aka online class) insert n/a
                    except:
                        table.insert(11,'N/A')

                    # append each index of relevance according to legend to course dictionary
                    if table[3] != 'N/A':
                        course['prof'] = table[3][1:-1]
                    course['name'] = headers[x]
                    course['time'] = table[9]
                    course['dayChar'] = table[10]
                    course['location'] = table[11]
                    course['range'] = table[12]
                    course['type'] = table[13]


                    # append to timeTable
                    info.append(course)
                    table = table[14:]
                    
                    # increment header counter
                    x += 1
            return info

        except FileNotFoundError:
            print('Could not find HTML file to parse. Make sure file name is schedule.html and is in current working directory'.center(80,' '))
            input('Press enter to try again')


def findCalendar(service):
    page_token = None
    found = False
    while not found:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if calendar_list_entry['summary'] == 'Carleton Class Grabber':
                calendar = calendar_list_entry
                prompt = input('Calendar already exists! Overwrite existing schedule? (y/n)\n > ')
                while prompt != 'y' and prompt != 'n':
                    prompt = input('Invalid input!\n > ')
                if prompt =='y':
                    service.calendars().delete(calendarId=calendar['id']).execute()
                else:
                    found = True
                break
        page_token = calendar_list.get('nextPageToken')
        if not page_token and not found:
            calendar = service.calendars().insert(body={'summary': 'Carleton Class Grabber', 'timeZone': 'America/Los_Angeles','visibility':'public'}).execute()
            break
    return calendar

def createEvent(course,service,calendar_new):
    course = {
          'summary': course['name'],
          'location': course['location'],
          'description': 'Prof: ' + course['prof'],
          'start': {
            'dateTime': course['firstDay'] + course['start'] + ':00' + '-04:00',
            'timeZone': 'America/Toronto'
          },
          'end': {
            'dateTime': course['firstDay'] + course['end'] + ':00' + '-04:00',
            'timeZone': 'America/Toronto'
          },
          'reminders': {
            'useDefault': True,
          },
          'recurrence': [
            'RRULE:FREQ=WEEKLY;BYDAY=' + course['recurrence'] + ';UNTIL=' + course['lastDay'],
            ],
        }
    print("'"+course['summary']+"'",'Event created!')
    course = service.events().insert(calendarId=calendar_new['id'], body=course).execute()

def dayCodeTrans(code):
    weekDays = ''
    for letter in code:
        # append number correspondant to day codes
        if letter == 'M': weekDays += 'MO,'
        if letter == 'T': weekDays += 'TU,'
        if letter == 'W': weekDays += 'WE,'
        if letter == 'R': weekDays += 'TH,'
        if letter == 'F': weekDays += 'FR,'
    weekDays = weekDays[:-1]
    return weekDays

def main():
    service = userAuth()
    timeTable = infoGrabber()
    calendar_new = findCalendar(service)

    for course in timeTable:
        middle = course['time'].find('-')

        # convert raw data to google calendar format
        course['start'] = militaryClock(course['time'][:middle-1])
        course['end'] = militaryClock(course['time'][middle+2:])
        course['firstDay'] = firstClass(course['dayChar'],course['range'])
        course['lastDay'] = lastClass(course['range'])
        course['recurrence'] = dayCodeTrans(course['dayChar'])

        # create each event
        createEvent(course,service,calendar_new)
if __name__ == '__main__':
    main()
