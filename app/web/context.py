from django.shortcuts import render



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
        ##### writing my to-dos here bc not gonna use git issues/ jira today :(
        # pass everything into the render function
        return render(
            request = request,
            template_name = template,
            context = context )
        
