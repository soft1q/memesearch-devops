from django.urls import path

from .api import CreateNewTagAPI, TagsViewSet, GetMemesByTagViewSet, DeleteTagAPI, TinderTagsViewSet

urlpatterns = [
    path('api/create', CreateNewTagAPI.as_view()),
    path('api/all/', TagsViewSet.as_view({'get': 'list'})),
    path('api/tagged', GetMemesByTagViewSet.as_view({'get': 'list'})),
    path('api/remove', DeleteTagAPI.as_view()),
    path('api/tinder', TinderTagsViewSet.as_view({'get': 'list'}))
]
