from rest_framework import viewsets
from .models import Branch, District, FiscalSessionAD, FiscalSessionBS, Print
from .serializers import (
    BranchListSerializer,
    BranchSerializer,
    DistrictListSerializer,
    PrintCreditReportSerializer,
    PrintDebitReportSerializer,
    PrintCreditSerializer,
    PrintDebitSerializer,
    PrintCreditCreateSerializer,
    PrintDebitCreateSerializer,
    FiscalSessionBSSerializer,
    FiscalSessionADSerializer,
    DistrictSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from util.fiscal import get_financial_year_bs, get_financial_year_ad
from util.get_current_user import current_user
from django_filters.rest_framework import DjangoFilterBackend, DateFromToRangeFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from core.core_permission import (
    BranchPermission,
    DistrictPermission,
    PrintPermission,
    PrintReportPermission,
)


# Create your views here.
class DistrictListView(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.filter(is_active=True)
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ["name"]
    ordering_fields = ["id", "name"]
    serializer_class = DistrictListSerializer
    permission_classes = [PrintPermission]


class BranchListView(viewsets.ReadOnlyModelViewSet):
    queryset = Branch.objects.filter(is_active=True)
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ["name"]
    ordering_fields = ["id", "name"]
    serializer_class = BranchListSerializer
    permission_classes = [PrintPermission]


class DistrictViewset(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name"]
    filterset_fields = ["name"]
    ordering_fields = ["id"]
    permission_classes = [DistrictPermission]


class BranchViewset(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name", "code"]
    filterset_fields = ["name", "code"]
    ordering_fields = ["id", "name"]
    permission_classes = [BranchPermission]


class FiscalSessionADViewset(viewsets.ModelViewSet):
    queryset = FiscalSessionAD.objects.all()
    serializer_class = FiscalSessionADSerializer
    permission_classes = [IsAuthenticated]


class FiscalSessionBSViewset(viewsets.ModelViewSet):
    queryset = FiscalSessionBS.objects.all()
    serializer_class = FiscalSessionBSSerializer
    permission_classes = [IsAuthenticated]


class PrintDebitViewset(viewsets.ModelViewSet):
    queryset = Print.objects.filter(card_type=1)
    filter_backends = [
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["first_name", "middle_name", "last_name"]
    filterset_fields = ["first_name", "middle_name", "last_name"]
    ordering_fields = ["id", "first_name"]
    permission_classes = [PrintPermission]

    def get_queryset(self):
        requesting_user = self.request.user
        if not requesting_user.is_anonymous:
            if requesting_user.is_superuser is True:
                return Print.objects.filter(card_type=1)
            return Print.objects.filter(card_type=1)

    def get_serializer_class(self):
        if self.action == "list":
            return PrintDebitSerializer
        if self.action == "create":
            return PrintDebitCreateSerializer
        return PrintDebitSerializer

    def create(self, request):
        serializer = PrintDebitCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            remarks = str(request.data["remarks"]).strip()
            if len(remarks) <= 0:
                return Response(
                    {"remarks": "Please give at least one word for remarks"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except KeyError:
            return Response(
                {"remarks": "Please Provide remarks"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance = self.get_object()
        serializer = PrintDebitCreateSerializer(
            instance, data=request.data, partial=True, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrintCreditViewset(viewsets.ModelViewSet):
    queryset = Print.objects.filter(card_type=2)
    filter_backends = [
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["first_name", "middle_name", "last_name"]
    filterset_fields = ["first_name", "middle_name", "last_name"]
    ordering_fields = ["id", "first_name"]
    permission_classes = [PrintPermission]

    def get_queryset(self):
        requesting_user = self.request.user
        if not requesting_user.is_anonymous:
            if requesting_user.is_superuser is True:
                return Print.objects.filter(card_type=2)

            return Print.objects.filter(card_type=2)

    def get_serializer_class(self):
        if self.action == "list":
            return PrintCreditSerializer
        if self.action == "create" or self.action == "partial_update":
            return PrintCreditCreateSerializer
        return PrintCreditSerializer

    def create(self, request):

        serializer = PrintCreditCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            remarks = str(request.data["remarks"]).strip()
            if len(remarks) <= 0:
                return Response(
                    {"remarks": "Please give at least one word for remarks"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except KeyError:
            return Response(
                {"remarks": "Please Provide remarks"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance = self.get_object()
        serializer = PrintCreditCreateSerializer(
            instance, data=request.data, partial=True, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrintReportFilter(filters.FilterSet):
    date = DateFromToRangeFilter(field_name="created_date_ad")

    class Meta:
        model = Print

        exclude = ["qr", "owner_photo"]


class PrintDebitReportViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Print.objects.filter(card_type=1)
    serializer_class = PrintDebitReportSerializer
    filter_backends = [
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ["id"]
    permission_classes = [PrintReportPermission]
    filterset_class = PrintReportFilter


class PrintCreditReportViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Print.objects.filter(card_type=2)
    serializer_class = PrintCreditReportSerializer
    permission_classes = [PrintReportPermission]
    filter_backends = [
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ["id"]
    filterset_class = PrintReportFilter
