from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Branch, District, FiscalSessionAD, FiscalSessionBS, Print
from util.get_current_user import current_user
from user.models import User


class DistrictListSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ["id", "name", "name_nepali"]


class BranchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name"]


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"
        read_only_fields = ["created_date_ad", "created_date_bs", "created_by"]

    def create(self, validated_data):
        user = current_user(self.context)
        district = District.objects.create(**validated_data, created_by=user)
        return district


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"
        read_only_fields = ["created_date_ad", "created_date_bs", "created_by"]

    def create(self, validated_data):
        user = current_user(self.context)
        branch = Branch.objects.create(**validated_data, created_by=user)
        return branch


class FiscalSessionADSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiscalSessionAD
        fields = "__all__"
        read_only_fields = ["created_date_ad", "created_date_bs", "created_by"]

    def create(self, validated_data):
        user = current_user(self.context)
        session = FiscalSessionAD.objects.create(**validated_data, created_by=user)
        return session


class FiscalSessionBSSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiscalSessionBS
        fields = "__all__"
        read_only_fields = ["created_date_ad", "created_date_bs", "created_by"]

    def create(self, validated_data):
        user = current_user(self.context)
        session = FiscalSessionBS.objects.create(**validated_data, created_by=user)
        return session


class PrintCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Print
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["created_by"] is not None:
            user = User.objects.get(id=data["created_by"])
            branch = Branch.objects.get(id=data["branch"])
            district = District.objects.get(id=data["district"])
            user_data = UserSerializer(user)
            branch_data = BranchSerializer(branch)
            district_data = DistrictSerializer(district)
            data["created_by"] = user_data.data
            data["branch"] = branch_data.data
            data["district"] = district_data.data
        return data


class PrintDebitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Print
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["created_by"] is not None:
            user = User.objects.get(id=data["created_by"])
            branch = Branch.objects.get(id=data["branch"])
            district = District.objects.get(id=data["district"])
            user_data = UserSerializer(user)
            branch_data = BranchSerializer(branch)
            district_data = DistrictSerializer(district)
            data["created_by"] = user_data.data
            data["branch"] = branch_data.data
            data["district"] = district_data.data
        return data


class PrintDebitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Print
        fields = "__all__"
        read_only_fields = [
            "created_date_ad",
            "created_date_bs",
            "created_by",
            "name",
            "card_no",
            "card_type",
        ]

    def create(self, validated_data):
        user = current_user(self.context)
        count = Print.objects.filter(card_type=1).count() + 1
        # fiscalYear = FiscalSessionBS.objects.last()
        unique_no = (
            # "PN-" + fiscalYear.session_short_name + "-" + "{0:0=5d}".format(count)
            "D-"
            + "{0:0=5d}".format(count)
        )

        first_name = validated_data.get("first_name")
        middle_name = validated_data.get("middle_name")
        last_name = validated_data.get("last_name")

        if middle_name == "":
            full_name = f"{first_name} {last_name}"
        else:
            full_name = f"{first_name} {middle_name} {last_name}"
        instance = Print.objects.create(
            **validated_data,
            card_no=unique_no,
            name=full_name,
            created_by=user,
            card_type=1,
        )
        return instance


class PrintCreditCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Print
        fields = "__all__"
        read_only_fields = [
            "created_date_ad",
            "created_date_bs",
            "created_by",
            "name",
            "card_no",
            "card_type",
        ]

    def create(self, validated_data):
        user = current_user(self.context)
        count = Print.objects.filter(card_type=2).count() + 1
        # fiscalYear = FiscalSessionBS.objects.last()
        unique_no = (
            # "PN-" + fiscalYear.session_short_name + "-" + "{0:0=5d}".format(count)
            "C-"
            + "{0:0=5d}".format(count)
        )

        first_name = validated_data.get("first_name")
        middle_name = validated_data.get("middle_name")
        last_name = validated_data.get("last_name")
        # card_no = validated_data.get("card_no")
        # address = validated_data.get("address")
        # citizenship_no = validated_data.get("citizenship_no")
        # mobile_no = validated_data.get("mobile_no")
        # branch = validated_data.get("branch")
        # district = validated_data.get("district")

        if middle_name == "":
            full_name = f"{first_name} {last_name}"
        else:
            full_name = f"{first_name} {middle_name} {last_name}"
        instance = Print.objects.create(
            **validated_data,
            card_no=unique_no,
            name=full_name,
            created_by=user,
            card_type=2,
        )
        return instance


class PrintDebitReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Print
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["created_by"] is not None:
            user = User.objects.get(id=data["created_by"])
            branch = Branch.objects.get(id=data["branch"])
            district = District.objects.get(id=data["district"])
            user_data = UserSerializer(user)
            branch_data = BranchSerializer(branch)
            district_data = DistrictSerializer(district)
            data["created_by"] = user_data.data
            data["branch"] = branch_data.data
            data["district"] = district_data.data
        return data


class PrintCreditReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Print
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["created_by"] is not None:
            user = User.objects.get(id=data["created_by"])
            branch = Branch.objects.get(id=data["branch"])
            district = District.objects.get(id=data["district"])
            user_data = UserSerializer(user)
            branch_data = BranchSerializer(branch)
            district_data = DistrictSerializer(district)
            data["created_by"] = user_data.data
            data["branch"] = branch_data.data
            data["district"] = district_data.data
        return data
