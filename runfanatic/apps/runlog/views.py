import datetime
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Sum, Count
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView

from apps.runlog.forms import AddRunForm, UserProfileForm
from apps.runlog.models import Run, UserProfile
from apps.runlog.cal import RunCalendar


class RunListView(ListView):
    """Use django generic ListView to list all the the runs for the current
    user."""

    def get_queryset(self):
        """Override get_querset so we can filter on request.user """
        return Run.objects.filter(user=self.request.user).order_by('-date')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """Force login required for this CBV."""
        return super(RunListView, self).dispatch(*args, **kwargs)


class UserProfileUpdateView(UpdateView):
    """Use generic update view so user can edit his profile and settings."""

    model = UserProfile
    form_class = UserProfileForm
    template_name = 'runlog/profile.html'

    def get_success_url(self):
        """On successful submission redirect to settings url."""
        return reverse('settings')

    def get_object(self, queryset=None):
        """Return the object associated with the request.user."""
        return UserProfile.objects.get(user=self.request.user)

    def form_valid(self, form):
        """Override the form valid method. We exclude the user in the
        UserProfileForm so add the user back in here."""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """Force login required for this CBV."""
        return super(UserProfileUpdateView, self).dispatch(*args, **kwargs)


def index(request):
    """Index view. If user is logged in redirect to dashboard, otherwise show
    the index."""

    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')
    return render(request, 'runlog/index.html', {})

def public_profile(request, username):
    u = User.objects.get(username=username)
    metrics = get_run_metrics_for_user(u)
    return render(request, 'runlog/public_profile.html', metrics)

def get_run_metrics_for_user(user):
    """Helper method to get run stats for a user."""

    today = datetime.datetime.now()

    week = datetime.timedelta(days=7)
    week_runs = Run.objects.filter(user=user,
            date__range=(today - week, today))
    weekly_distance = week_runs.aggregate(Sum('distance'))['distance__sum']
    days_run_week = week_runs.aggregate(
                Count('date', distinct=True)
            )['date__count']

    the_first_month = datetime.datetime(today.year, today.month, 1)
    monthly_runs = Run.objects.filter(user=user,
            date__range=(the_first_month, today))
    monthly_distance = monthly_runs.aggregate(Sum('distance'))['distance__sum']

    the_first_year = datetime.datetime(today.year, 1, 1, )
    yearly_runs = Run.objects.filter(user=user,
            date__range=(the_first_year, today))
    yearly_distance = yearly_runs.aggregate(Sum('distance'))['distance__sum']

    six_weeks = datetime.timedelta(days=42)
    six_week_runs = Run.objects.filter(user=user,
            date__range=(today - six_weeks, today))
    if six_week_runs:
        six_week_total = six_week_runs.aggregate(
                    Sum('distance')
                )['distance__sum']
        six_week_avg = six_week_total / 6
    else:
        six_week_avg = 0

    recent_runs = Run.objects.filter(user=user).order_by('-date')[:10]

    units = UserProfile.objects.get(user=user).units

    return {
        'today': today,
        'weekly_distance': weekly_distance,
        'monthly_distance': monthly_distance,
        'yearly_distance': yearly_distance,
        'days_run_week': days_run_week,
        'six_week_avg': six_week_avg,
        'recent_runs': recent_runs,
        'units': units,
        }

@login_required
def dashboard(request):
    """View that displays personal run metrics such as weekly milage, the days
    of the week run and 6 week run average."""
    return render(request, 'runlog/dashboard.html',
            get_run_metrics_for_user(request.user))

@login_required
def runcal(request):
    """View that displays an individuals run calendar. """

    now = datetime.datetime.now()
    day_week_starts = UserProfile.objects.get(user=request.user).day_week_starts
    month_runs = Run.objects.filter(
            user=request.user,
            date__month=now.month)
    cal = RunCalendar(day_week_starts, month_runs)
    cal_html = cal.formatmonth(now.year, now.month)

    return render(request, 'runlog/calendar.html', {'calendar':
        mark_safe(cal_html)})


@login_required
def add(request):
    """View that handles ajax of adding a run to the database."""
    if request.method == 'POST':
        runForm = AddRunForm(request.POST)
        if runForm.is_valid():
            newRun = Run(
                    user=request.user,
                    date=runForm.cleaned_data['date'],
                    hours=runForm.cleaned_data['hours'],
                    minutes=runForm.cleaned_data['minutes'],
                    seconds=runForm.cleaned_data['seconds'],
                    distance=runForm.cleaned_data['distance'])
            newRun.save()
            response = {'id': newRun.pk }
            return HttpResponse(json.dumps(response),
                    mimetype="application/json")
        else:
            # return errors
            return HttpResponse(json.dumps(runForm.errors),
                    mimetype="application/json")
    return HttpResponseRedirect('/')


@login_required
def delete(request, id):
    """View that deletes a particular run give an id."""

    try:
        to_delete = int(id)
        r = Run.objects.get(id=to_delete)
        if r.user == request.user:
            r.delete()
    except:
        raise Http404()
    return HttpResponseRedirect('/dashboard/')
