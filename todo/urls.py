from django.urls import path
from . views import index, recordupdate, searchtodo, signup, userlogin, viewlogout, recorddelete

urlpatterns = [
    path('', index),
    path('signup/', signup),
    path('login/', userlogin),
    path('logout/', viewlogout),
    path('delete/<int:id>/', recorddelete),
    path('update/<int:id>/', recordupdate),
    path('searchrecord/', searchtodo)
]
