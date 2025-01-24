from rest_framework import serializers

from mutualfunds.models import MutualFunds


class MutualFundsSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = MutualFunds
        fields = [
            "id","name","nav","fund_type"
        ]