from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('ajax/',views.home, name = "dashboard"),
    path('profile', views.profile),
    path('hello', views.hello),
    path('watchlist',views.watchlist),
    path('share_info',views.share_info),
    path('login',views.login),
    path('login-save',views.login_save,name = "login_save"),
    path('info/<slug:ticker>/<slug:market>',views.display_data),
    path('info/<slug:ticker>/<slug:market>/<str:time>',views.display_data),
    path('<slug:ticker>/<slug:market>/',views.add_to_watchlist, name = "add_to_watchlist"),
    path('buy/<slug:ticker>/<slug:market>',views.buy_stock,name = "buy_stock"),
    path('sell/<slug:ticker>/<slug:market>/<str:time>', views.sell_stock, name = "sell_stock"),
    path('chart',views.line_chart,name = "line_chart"),
    path('chartJSON',views.line_chart_json, name = "line_chart_json"),
    path('search_stock', views.search_stocks, name = "search_stocks"),
    path('ajax/predict/<slug:ticker>/<slug:market>',views.predict, name = "predict_stock"),
]