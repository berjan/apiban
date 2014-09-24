from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
from ui.views import HomepageView, IbanView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'apiban.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', HomepageView.as_view(), name="homepage"),

    url(r'^get-iban$', IbanView.as_view(), name="get_iban"),


    url(r'^admin/', include(admin.site.urls)),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
