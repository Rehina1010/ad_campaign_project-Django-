from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [
    path('', views.campaign_list, name='campaign_list'),
    path('campaign/<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('campaign/create/', views.create_campaign, name='create_campaign'),
    path('campaign/<int:pk>/edit/', views.edit_campaign, name='edit_campaign'),
    path('campaign/<int:pk>/delete/', views.delete_campaign, name='delete_campaign'),
    path('campaign/<int:pk>/improve/', views.improve_campaign, name='improve_campaign'),
    path('campaign/<int:pk>/save_improvements/', views.save_improvements, name='save_improvements'),

]
