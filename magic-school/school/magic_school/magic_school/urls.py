from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import TemplateView


def bad(request):
    """ Simulates a server error """
    1 / 0


urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]


urlpatterns += i18n_patterns(
    path("bad/", bad),  # type: ignore
    path('', include('djvue.urls')),

    path(f"{settings.ADMIN_URL}/", admin.site.urls),

    path("user/", include("user.urls", namespace="user")),
    path("api/v1/", include("user.api.urls", namespace="user_api")),
    path("api/v1/", include("manager.urls", namespace="manager_api")),
    path("api/v1/", include("student.urls", namespace="student_api")),

)

if settings.DEBUG:
    urlpatterns += [
        # Testing 404 and 500 error pages
        path("404/", TemplateView.as_view(template_name="404.html"), name="404"),
        path("500/", TemplateView.as_view(template_name="500.html"), name="500"),
    ]

    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
