from rest_framework import serializers

from ..models import Garment,GarmentMen,GarmentWomen, MenGarmentScores, WomenGarmentScores;

class GarmentMenSerializer(serializers.ModelSerializer):
    class Meta:
        model = GarmentMen
        fields = ('id','image_path')

class GarmentWomenSerializer(serializers.ModelSerializer):
    class Meta:
        model = GarmentWomen
        fields = ('id','image_path')

class GarmentWomenRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GarmentWomen
        fields = ('id','image_path','combined_count_for_each_ranking','combined_score')
    
class WomenGarmentScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = WomenGarmentScores
        fields = ('id','garment_id','user_gender','count_for_each_ranking','score')

class MenGarmentScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenGarmentScores
        fields = ('id','garment_id','user_gender','count_for_each_ranking','score')