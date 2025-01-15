


from django.views.decorators.http import require_GET, require_POST

from django.http import HttpResponse


@require_GET
def index(request):    

    return HttpResponse("testing that views work")