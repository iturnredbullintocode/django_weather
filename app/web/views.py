from django.views.decorators.http import require_GET, require_POST

from django.shortcuts import render




######### move to diff file
####### :( not gonna log jira issues/git tickets, just gonna write notes here today ugh

class ContextData:

    def __init__(self, request, template=None):
        self.request = request 
        self.template = template

    def response(self):
        # turn all the instance variables into a dictionary
        context = vars(self)
        request = self.request
        template = self.template
        # delete the two extra vars from the context dictionary
        del context['request']
        del context['template']
        ####### make sure the deletion is safe
        ####### do validation checks on variables before rendering them, make sure theyre there and are right format
        ####### make sure the variables are sanitized and no sensitive data gets shown, since they will be available in templates
        # pass everything into the render function
        return render(
            request = request,
            template_name = template,
            context = context )
        

@require_GET
def home(request):    

    context = ContextData(request, "home.html")
    return context.response()



