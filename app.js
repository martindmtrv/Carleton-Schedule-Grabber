const ical = require('ical-generator');
const Filter = require('./Filter');
const fs = require('fs');

const cal = ical().timezone('America/Toronto');

events = Filter.filter();

cal.events(events);

cal.save('newcal', ()=>{
    console.log('saved');
})