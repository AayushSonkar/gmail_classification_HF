#every single url in the project will be configured over here 
from django.urls import path
from .views import go_syncwise,index

urlpatterns = [
    # Other URL patterns
    path('', index, name='beta_v1'), 
    path('go_syncwise/', go_syncwise, name='syncwise_function'),
   
]



