import calendar
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc


class RunCalendar(calendar.HTMLCalendar):

    def __init__(self, week_start_date, runs):
        if week_start_date == 'Monday':
            super(RunCalendar, self).__init__(calendar.MONDAY)
        else:
            super(RunCalendar, self).__init__(calendar.SUNDAY)
        self.runs = self.group_by_day(runs)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.runs:
                cssclass += ' filled'
                body = ''
                for run in self.runs[day]:
                    body += '<span class="run">'
                    body += esc(run.distance) + ' mi. ('
                    body += esc(run.hours) + ':' + esc(run.minutes)
                    body += ':' + esc(run.seconds)
                    body += ')</span>'
                return self.day_cell(cssclass, day, body)
            return self.day_cell(cssclass, day, '')
        return self.day_cell('noday', '&nbsp;', '')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(RunCalendar, self).formatmonth(year, month)

    def group_by_day(self, runs):
        field = lambda run: run.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(runs, field)]
        )

    def day_cell(self, cssclass, day, body):
        return '<td class="%s"><div class="day">%s</div>%s</td>' % \
            (cssclass, day, body)
