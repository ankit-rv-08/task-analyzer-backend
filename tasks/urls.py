from django.urls import path
from .views import AnalyzeTasksView, SuggestTasksView

urlpatterns = [
    path('tasks/analyze/', AnalyzeTasksView.as_view()),
    path('tasks/suggest/', SuggestTasksView.as_view()),
]
