from rest_framework import routers
from django.urls import path, include
from .views import (
    BranchListView,
    BranchViewset,
    DistrictListView,
    PrintCreditReportViewset,
    PrintDebitReportViewset,
    PrintDebitViewset,
    PrintCreditViewset,
    FiscalSessionADViewset,
    FiscalSessionBSViewset,
    DistrictViewset,
)

router = routers.DefaultRouter(trailing_slash=False)

router.register("district", DistrictViewset)
router.register("district-list", DistrictListView)
router.register("branch-list", BranchListView)
router.register("branch", BranchViewset)
router.register("print-debit", PrintDebitViewset)
router.register("print-credit", PrintCreditViewset)
router.register("session-bs", FiscalSessionBSViewset)
router.register("session-ad", FiscalSessionADViewset)
router.register("print-credit-report", PrintCreditReportViewset)
router.register("print-debit-report", PrintDebitReportViewset)

urlpatterns = [path("", include(router.urls))]
