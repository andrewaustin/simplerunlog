from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from apps.runlog.models import Run
from apps.runlog.forms import addRunForm
from django.db.models import Sum, Count
import datetime

def index(request):
    """View that displays personal run metrics such as weekly milage, the days
    of the week run and 6 week run average."""


    today = datetime.datetime.now()

    week = datetime.timedelta(days=7)
    week_runs = Run.objects.filter(date__range=(today-week,today))
    weekly_milage = week_runs.aggregate(Sum('distance'))['distance__sum']
    days_run_week = week_runs.aggregate(Count('date', distinct=True))['date__count']

    the_first_month = datetime.datetime(today.year, today.month, 1)
    monthly_runs = Run.objects.filter(date__range=(the_first_month,today))
    monthly_milage = monthly_runs.aggregate(Sum('distance'))['distance__sum']

    the_first_year = datetime.datetime(today.year, 1,1,)
    yearly_runs = Run.objects.filter(date__range=(the_first_year,today))
    yearly_milage = yearly_runs.aggregate(Sum('distance'))['distance__sum']

    six_weeks = datetime.timedelta(days=42)
    six_week_runs = Run.objects.filter(date__range=(today-six_weeks,today))
    if six_week_runs:
        six_week_total = six_week_runs.aggregate(Sum('distance'))['distance__sum']
        six_week_avg = six_week_total / 6
    else:
        six_week_avg = 0

    return render(request, 'runlog/index.html', {
        'today': today, 'weekly_milage' : weekly_milage, 'monthly_milage': monthly_milage, 'yearly_milage' : yearly_milage,
        'days_run_week' : days_run_week, 'six_week_avg' : six_week_avg
        })

def add(request):
    """View that displays a Django form to add new run data and saves that new
    data to the database."""

    if request.method == 'POST':
        runForm = addRunForm(request.POST)
        if runForm.is_valid():
            newRun = Run(
                    date = runForm.cleaned_data['date'], hours = runForm.cleaned_data['hours'], minutes = runForm.cleaned_data['minutes'],
                    seconds = runForm.cleaned_data['seconds'], distance = runForm.cleaned_data['distance'])
            newRun.save()
            return HttpResponseRedirect('/')
        else:
            # return errors
            return render(request, 'runlog/add.html', {'form' : runForm})
    else:
        runForm = addRunForm()

    return render(request, 'runlog/add.html', {'form' : runForm})

def delete(request, id):
    """View that deletes a particular run give an id."""

    # TODO: if make multi user system, need more auth here
    try:
        to_delete = int(id)
        r = Run.objects.get(id=to_delete)
        r.delete()
    except:
        raise Http404()
    return HttpResponseRedirect('/')
