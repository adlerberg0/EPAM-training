from django.urls import path

from . import views

# why can't I import from forecast.forecast_app
app_name = "forecast_app"
urlpatterns = [
    path("", views.choose_country, name="country"),
    path("<int:page>", views.choose_country, name="country"),
    path("city/<str:country_id>", views.choose_city, name="city"),
    path("city/<str:country_id>/<int:page>", views.choose_city, name="city"),
    path(
        "statistic_time_interval/<str:city_id>",
        views.set_statistic_time_interval,
        name="set_statistic_time_interval",
    ),
    path(
        "station_statistic/<str:stationid>",
        views.get_station_statistic,
        name="get_station_statistic",
    ),
]
