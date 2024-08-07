from django.contrib import admin
from django.urls import path,include
from django.contrib.auth  import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',user_views.register,name="register"),
    path('profile/',user_views.profile,name="profile"),
    path('login/', user_views.CustomLoginView.as_view(), name='login'),
    path('password-reset/',user_views.CustomPasswordResetView.as_view(),name="password_reset"),
      path('password-reset/done',user_views.CustomPasswordResetDoneView.as_view(template_name='password_reset_done.html'),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',user_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name="password_reset_confirm"),
    path('password-reset-complete/',user_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name="password_reset_complete"),
    path("logout/", user_views.logout_view, name="logout"),
    path('',include('store.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)