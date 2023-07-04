const Fetch = require('./Fetch.js');
const calendar = require('node-calendar');


const months = {
    Jan:'01', Feb:'02', Mar:'03', Apr:'04', May:'05',
    Jun:'06', Jul:'07', Aug:'08', Sep:'09', Oct:'10',
    Nov:'11', Dec:'12'
}

// receives time string returns military time in array [hrs, min]
function militaryTime(time){
    let meridian = time.substring(time.length-2);
    let hrs = Number(time.substring(0, time.indexOf(':')));
    let mins = Number(time.substring(time.indexOf(':')+1,time.length-3));
    
    if (meridian === 'am'){
        if (hrs === 12){
            return [0,mins];
        }
    } else{
        if (hrs != 12){
            return [hrs+12, mins];
        }
    }
    return [hrs,mins];
}

// create days for rrule
function dateCode(code){
    weekDays = [];
    for (let x=0; x<code.length; x++){
        letter = code.charAt(x);
        if (letter === 'M'){ weekDays.push('mo')};
        if (letter === 'T'){weekDays.push('tu')};
        if (letter == 'W'){weekDays.push('we')};
        if (letter == 'R') {weekDays.push('th')};
        if (letter == 'F') {weekDays.push('fr')};
    }

    return weekDays;
}

// create end date for rrule
function strdateform(date){
    let month = months[date.substring(0,3)];
    let day = date.substring(4,6);
    let year = date.substring(8);

    return `${year}${month}${day}`
}

function firstclass(date, days){
    const day_num = { M:0, T:1, W:2, R:3, F:4};

    let weekdays = [];
    let month = date.getMonth()+1;
    let year = date.getFullYear();
    let day = date.getDate();

    for (let x=0; x<days.length; x++){
        weekdays[x] = day_num[days.charAt(x)];
    }

    const matrix = new calendar.Calendar().monthdays2calendar(year,month);
    let firstdaynum = 0;
    let found = false

    for (let week=0; week<matrix.length; week++){
        for (let weekday=0; weekday< matrix[week].length; weekday++){
            for (let x=0; x< weekdays.length; x++){
                if (matrix[week][weekday][0] >=day){
                    if (matrix[week][weekday][1] == weekdays[x]){
                        firstdaynum = matrix[week][weekday][0];
                        found = true;
                        break;
                    }
                }
            }
            if (found) { break };
        }
        if (found) { break };
    }
    date.setDate(firstdaynum);

    return date;

}


function filter(){
    // get rid of any online/unscheduled classes
    let events = Fetch.fetch();
    events = events.filter((value)=>{
        if (value.start === ''){
            return false;
        }
        return true;
    });
    
    // prepare events for ics conversion (start/end time step)
    events.forEach((value)=>{
        let time = militaryTime(value.start);
        // get start date (all classes will appear on day 1 for now)
        value.start = firstclass(value.startDate, value.days);

        // set the time
        value.start.setHours(time[0]);
        value.start.setMinutes(time[1]);

        time = militaryTime(value.end);
        value.end = new Date(value.start.getTime());
        value.end.setHours(time[0]);
        value.end.setMinutes(time[1]);

        delete value.startDate;

        // set the recurrance pattern
        value.repeating = {
            freq: 'MONTHLY',
            byDay: dateCode(value.days),
            until: value.endDate
        };

        delete value.days;
        delete value.endDate;
    });
    return events;
}

module.exports = {filter: filter}