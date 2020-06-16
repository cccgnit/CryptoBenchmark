from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from benchmark.views import CipherResultViewSet, SystemInfoViewSet
from . import views

# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter()
router.register(r'^result', CipherResultViewSet, basename="CipherResult")
router.register(r'^system', SystemInfoViewSet, basename="SystemInfo")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # ex: /result/ or /system/
    url('', include(router.urls)),
    url('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
