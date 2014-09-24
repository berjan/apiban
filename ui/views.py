from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, FormView
from gen_bank_numbers.models import BankAccount
from ui.forms import SearchForm


class HomepageView(FormView):
    template_name = 'homepage.html'
    form_class = SearchForm
    iban = None

    def get_context_data(self, **kwargs):
        data = super(HomepageView, self).get_context_data(**kwargs)
        data['iban'] = self.iban
        return data



    def get(self, request, *args, **kwargs):
        result = super(HomepageView,self).get(request, *args, **kwargs)
        return result

    def form_valid(self, form):
        context = {}
        context['form'] = form
        context['iban'] = BankAccount.get_iban_number(self.request.POST['search'])

        return self.render_to_response(context=context)
    def post(self, request, *args, **kwargs):

        result = super(HomepageView, self).post(request, *args, **kwargs)
        return result

    def get_success_url(self):
        return reverse('homepage')


from django import http
from django.utils import simplejson as json

class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)

class IbanView(FormView):
    template_name = 'homepage.html'
    form_class = SearchForm


    def get_context_data(self, **kwargs):
        data = super(IbanView, self).get_context_data(**kwargs)
        return data

    def get(self, request, *args, **kwargs):
        result = super(IbanView,self).get(request, *args, **kwargs)
        return result

    def post(self, request, *args, **kwargs):
        result = super(IbanView, self).post(request, *args, **kwargs)
        return result

    def get_success_url(self):
        return reverse('homepage')

