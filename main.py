import urllib.request, json
import icalendar, pytz
from datetime import datetime
from dateutil import parser

link = "https://public.mai.ru/schedule/data/bdc71a9a967c1e24f6e55a208f452202.json"
rasp = urllib.request.urlopen(link).read()
rasp = json.loads(rasp)

cal = icalendar.Calendar()
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')

rasp.pop("group")

for day in rasp.items():
    date = datetime.fromisoformat(str(parser.parse(day[0], dayfirst=True)))
    #print(date.date())
    pary = day[1]["pairs"]

    for _para in pary.items():
        para = _para[1]

        time_start = datetime.fromisoformat(str(parser.parse(para["time_start"])))
        time_start = datetime.combine(date.date(), time_start.time())
        time_end = datetime.fromisoformat(str(parser.parse(para["time_end"])))
        time_end = datetime.combine(date.date(), time_end.time())

        name = []
        for _name in para["class"].items():
            name.append(_name[0])
        name = ' / '.join(name)

        lector = []
        for _lector in para["lector"].items():
            lector.append(_lector[1])
        lector = ', '.join(lector)

        type = []
        for _type in para["type"].items():
            type = _type[0]

        room = []
        for _room in para["room"].items():
            room.append(_room[1])
        room = ', '.join(room)

        event = icalendar.Event()
        event.add('summary', str(type + " " + name))
        event.add('dtstart', time_start)
        event.add('dtend', time_end)
        event.add('dtstamp', time_start)
        event.add('location', room)
        event.add('description', lector)
        cal.add_component(event)

       # print(time_start, time_end, name, type, lector, room)

    #print(json.loads(day))

f = open("rasp_test.ics", "wb")
f.write(cal.to_ical())
f.close()

'''
cal = icalendar.Calendar()

cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')

event = icalendar.Event()
event.add('summary', 'Python meeting about calendaring')
event.add('dtstart', datetime(2005,4,4,8,0,0,tzinfo=pytz.utc))
event.add('dtend', datetime(2005,4,4,10,0,0,tzinfo=pytz.utc))
event.add('dtstamp', datetime(2005,4,4,0,10,0,tzinfo=pytz.utc))

cal.add_component(event)

f = open("rasp.ics", "wb")
f.write(cal.to_ical())
f.close()
'''