from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from projectFocusapi.views import register_user, login_user
from projectFocusapi.views import LotView, ProjectView, LotNoteView, ProjectNoteView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'lots', LotView, 'lot')
router.register(r'projects', ProjectView, 'project')
router.register(r'lotnotes', LotNoteView, 'lotnote')
router.register(r'projectnotes', ProjectNoteView, 'projectnote')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
