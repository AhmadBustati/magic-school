from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
app_name = "user_api"

router = SimpleRouter()

router.register("users", UserViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

     ]