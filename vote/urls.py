from django.urls import include, path
from . import views


urlpatterns=[
    path('api/votes/', views.VoteList.as_view()),
    path('api/votes/<int:pk>/', views.VoteDetail.as_view()),
    path('api/items/', views.ItemList.as_view()),
    path('api/random/', views.Item_Random.as_view()),
    path('api/colleges/', views.CollegeList.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]