from django.urls import path

from . import views

app_name = "inventory"
urlpatterns = [
    path('<str:inv>/', views.ListAllInventory.as_view(), name='index'),
    path('<str:inv>/<int:pk>/', views.RecordDetail.as_view(), name='item_detail'),
    # path('<str:inv>/<int:pk>/borrow/', views.Createloan.as_view(), name='create_loan'),
    path('<str:inv>/new/', views.CreateRecord.as_view(), name='update_record'),
    path('<str:inv>/<int:pk>/edit/', views.UpdateRecord.as_view(), name='update_record'),
    path('<str:inv>/suggestions/new/', views.CreateSuggestion.as_view(), name='create_suggestion'),
    path('<str:inv>/suggestions/', views.ListAllSuggestions.as_view(), name='list_suggestions'),
    path('<str:inv>/suggestions/<int:pk>/', views.SuggestionDetail.as_view(), name='suggestion_detail'),
    path('<str:inv>/suggestions/<int:pk>/edit/', views.CreateSuggestion.as_view(), name='edit_suggestion'),
    path('<str:inv>/borrow/new/', views.CreateLoan.as_view(), name='create_loan'),
    path('<str:inv>/borrow/', views.ListAllLoans.as_view(), name='list_loans'),
    path('<str:inv>/borrow/<int:pk>/', views.LoanDetail.as_view(), name='loan_detail'),
    path('<str:inv>/borrow/<int:pk>/edit/', views.UpdateLoan.as_view(), name='edit_loan')
]

