from django.urls import path
from . import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("news/", views.NewsView.as_view(), name="news"),
    path("<slug:slug>/pay/", views.PaySculptureView.as_view(), name='pay_sculpture'),
    path("free/sculpture/", views.DevSculptureView.as_view(), name='development_list'),
    path("free/portals/", views.DevPortalView.as_view(), name='development_list'),
    path("sculpture/", views.SculptureView.as_view(), name='sculpture_list'),
    path("portals/", views.PortalView.as_view(), name='portals_list'),
    path("dev/<slug:slug>/", views.DevSculptureDetailView.as_view(), name='development'),
    path("<slug:slug>/", views.SculptureDetailView.as_view(), name="sculpture_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("order/<int:pk>/", views.NewOrder.as_view(), name="new_order"),

]
