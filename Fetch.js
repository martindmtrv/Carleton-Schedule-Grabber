const fs = require('fs');
const cheerio = require('cheerio');

// function to retrieve raw source from detail schedule
// plans to eventually make this an authorized request to central
function pull_html(){
    return fs.readFileSync('schedule.html')
}

function scraper(){
    source = pull_html();
    const $ = cheerio.load(source);

    var events = [];

    $('table.datadisplaytable').each((index, el)=>{
        var event = {};

        var title = $(el).find('a').html()

        if (title === null){
            rowdata = $(el).find('tr:nth-of-type(2)').text().trim().split('\n');

            // scrape data
            event.start = rowdata[1].substring(0,rowdata[1].indexOf('-')-1);
            event.end = rowdata[1].substring(rowdata[1].indexOf('-')+2);
            event.days = rowdata[2];
            event.location = rowdata[3];
            event.startDate = new Date(rowdata[4].substring(0,rowdata[4].indexOf('-')-1));
            event.endDate = new Date(rowdata[4].substring(rowdata[4].indexOf('-')+2));

            Object.assign(events[Math.floor(index/2)], event);

        } else{
            var prof = $(el).find('tr:nth-of-type(5)').find('td').text().trim();
            if (prof === ''){
                prof = 'N/A'
            }

            event.summary = title;
            event.description = `Prof: ${prof}`
            event.timezone = 'America/Toronto';
            events[index/2] = event;
        }
    })
    return events;
}

module.exports = {fetch: scraper};