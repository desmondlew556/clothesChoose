from django.urls import path,re_path
from .views import ClothesOverview, ClothesSummaryRankingsView, ClothesUpdateRankingsView, LogError, MenClothesRetrievalView, UpdateScores, UpdateView, WomenClothesRetrievalView

from . import views

app_name = 'clothesChoose'
urlpatterns = [
    path("api/garment/summary_rankings/",ClothesSummaryRankingsView.as_view()),
    path("api/garment/rankings_overview/<int:num_clothes_per_gender>/",ClothesOverview.as_view()),
    path("api/garment/rankings/",ClothesUpdateRankingsView.as_view()),
    re_path(r'api/garment/men/(?P<num_clothes>[0-9]+)/$',MenClothesRetrievalView.as_view()),
    re_path(r'api/garment/women/(?P<num_clothes>[0-9]+)/$',WomenClothesRetrievalView.as_view()),
    path("api/error_logging",LogError.as_view()),
    #paths for development
    path("api/garment/scores/women",UpdateView.as_view()),
    path("api/garment/rankings/update",UpdateScores.as_view()),
]