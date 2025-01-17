from django.views.decorators.http import require_GET, require_POST

from .forms import ZipcodeForm
from .services import fetch_weather
from .context import ContextData




@require_GET
def home(request):    

    context = ContextData(request, "home.html")

    # create a blank form
    context.form = ZipcodeForm()

    return context.response()





@require_POST
def weather_ajax(request):

    context = ContextData(request)
    context.template = 'weather_ajax.html'

    # create a form instance and populate it with data from the request
    context.form = ZipcodeForm(request.POST)

    # if forn data isn't valid, return early
    # I could probably auto-execute this in my response class
    # and I could throw and catch the errors there and return early if needed
    if not context.form.is_valid():
        return context.response()

    # context.form.cleaned_data now contains validated data
    clean_zip_code = context.form.cleaned_data['zipcode']
    forecast = context.form.cleaned_data['forecast']

    # fetch weather from either API or cache,
    # the logic of doing so is abstracted in this function
    context.weather = fetch_weather(clean_zip_code, forecast=forecast)

    # final return
    return context.response()






