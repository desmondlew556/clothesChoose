from django.db import models
from django import forms
from django.conf import settings
from django.utils.translation import ungettext

import os
import math

from rest_framework import serializers

#add on library for colors
#from colorfield.fields import ColorField

#number values for char length 
short_len=100
middle_len=500
long_len = 1000

gender_choices = [
    ('M','men'),
    ('W','women'),
    ('NB','non-binary'),
    ('UN','prefer not to say')
]
gender_choices_dict = {
    gender_choices[0][1]:gender_choices[0][0],
    gender_choices[1][1]:gender_choices[1][0],
    gender_choices[2][1]:gender_choices[2][0],
    gender_choices[3][1]:gender_choices[3][0],
}
gender_choices_symbols_to_strings = {
    gender_choices[0][0]:gender_choices[0][1],
    gender_choices[1][0]:gender_choices[1][1],
    gender_choices[2][0]:gender_choices[2][1],
    gender_choices[3][0]:gender_choices[3][1],
}
num_ranks = 10
class Characteristics(models.Model):
    characteristic_name = models.CharField(primary_key = True, max_length = short_len)

#class Color(models.Model):
    #colors = ColorField(default=None)

class Garment(models.Model):
    #ranking_initializer = lambda x: {'rank_'+str(rank+1):0 for rank in range(10)}
    #def ranking_initializer():
    #    return {'rank_'+str(rank+1):0 for rank in range(10)}
    image_path=models.CharField(max_length = middle_len)
    #colors = models.ManyToManyField(Color)
    characteristics = models.ManyToManyField(Characteristics)
    #combined scores
    score = models.FloatField(default = 0)
    #combined count for each ranking
    count_for_each_ranking=models.JSONField(default = {'rank_'+str(rank+1):0 for rank in range(num_ranks)})
    def __str__(self):
        return self.image_path
    #save float in 2dp.
    def save(self, *args, **kwargs):
        self.score = round(self.score, 2)
        super(Garment, self).save(*args, **kwargs)
    @staticmethod
    def get_rank_score(rank):
        scores = [round(math.log(11-x),2) for x in range(num_ranks+1)]
        return scores[int(rank)]
    
    class Meta:
        abstract = True

class GarmentMen(Garment):
    def __str__(self):
        return self.image_path
    @staticmethod
    def get_rank(score):
        g_score = GarmentMen.objects.filter(id__in = [x.garment_id.id for x in MenGarmentScores.objects.all()]).order_by('-score')
        garments = GarmentMen.objects.filter(score__gt=score).order_by("-score")
        rank = 1
        for i in range(len(garments)):
            rank+=1
        return rank
    @staticmethod
    def get_num_clothes():
        return GarmentMen.objects.all().count()
    @staticmethod
    def get_num_clothes_ranked():
        return MenGarmentScores.objects.all().count()
    @staticmethod
    def get_top_n_clothes(n):
        num_clothes = GarmentMen.get_num_clothes_ranked()
        all_ranked_clothes = GarmentMen.objects.order_by('-score')
        if(num_clothes<n):
            serializer = MenGarmentRankingSerializer(all_ranked_clothes[0:num_clothes],many = True)
        else:
            serializer = MenGarmentRankingSerializer(all_ranked_clothes[0:n],many = True)

        clothes_data = serializer.data
        #compute rank for each person
        rank = 1
        score = -1
        index = 0
        #add image_path

        for i in range(0,len(clothes_data)):
            clothes_data[i]["garment_id"]=clothes_data[i]["id"]
            del clothes_data[i]["id"]
            if all_ranked_clothes[i].score != score:
                rank+=(i-index)
                index = i
                score = all_ranked_clothes[i].score
            clothes_data[i]["rank"]=rank
        return clothes_data

class GarmentWomen(Garment):
    def __str__(self):
        return self.image_path
    @staticmethod
    def get_rank(score):
        g_score = GarmentWomen.objects.filter(id__in = [x.garment_id.id for x in WomenGarmentScores.objects.all()]).order_by('-score')
        garments = GarmentWomen.objects.filter(score__gt=score).order_by("-score")
        rank = 1
        for i in range(len(garments)):
            rank+=1
        return rank
    @staticmethod
    def get_num_clothes():
        return GarmentWomen.objects.all().count()
    @staticmethod
    def get_num_clothes_ranked():
        return WomenGarmentScores.objects.all().count()
    @staticmethod
    def get_top_n_clothes(n):
        num_clothes = GarmentWomen.get_num_clothes_ranked()
        all_ranked_clothes = GarmentWomen.objects.order_by('-score')
        if(num_clothes<n):
            serializer = WomenGarmentRankingSerializer(all_ranked_clothes[0:num_clothes],many = True)
        else:
            serializer = WomenGarmentRankingSerializer(all_ranked_clothes[0:n],many = True)

        clothes_data = serializer.data
        #compute rank for each person
        rank = 1
        score = -1
        index = 0
        #add image_path

        for i in range(0,len(clothes_data)):
            clothes_data[i]["garment_id"]=clothes_data[i]["id"]
            del clothes_data[i]["id"]
            if all_ranked_clothes[i].score != score:
                rank+=(i-index)
                index = i
                score = all_ranked_clothes[i].score
            clothes_data[i]["rank"]=rank
        return clothes_data

class GarmentOthers(Garment):
    garment_type_options = [
        ("U","Unisex"),
        (None,"Unknown")
    ]
    garment_type = models.CharField(
        choices = garment_type_options,
        max_length = short_len
    )

class GarmentScores(models.Model):
    user_gender = models.CharField(max_length = short_len, choices = gender_choices)
    count_for_each_ranking=models.JSONField(default = {'rank_'+str(rank+1):0 for rank in range(num_ranks)})
    score = models.FloatField(default = 0)
    def save(self, *args, **kwargs):
        self.score = round(self.score, 2)
        super(GarmentScores, self).save(*args, **kwargs)
    class Meta:
        abstract = True

class MenGarmentScores(GarmentScores):
    garment_id = models.ForeignKey(GarmentMen,on_delete = models.PROTECT)
    class Meta:
        unique_together = ['garment_id','user_gender']
    @staticmethod
    def get_num_clothes(rated_by):
        if rated_by not in gender_choices_dict.keys():
            return 0
        else:
            return MenGarmentScores.objects.filter(user_gender = gender_choices_dict[rated_by]).count()
    @staticmethod
    def get_top_n_clothes(n,rated_by):
        if rated_by not in gender_choices_dict.keys():
            return None
        num_clothes = MenGarmentScores.get_num_clothes(rated_by)
        all_ranked_clothes = MenGarmentScores.objects.filter(user_gender = gender_choices_dict[rated_by]).order_by("-score")
        if(num_clothes<n):
            serializer = MenGarmentScoresSerializer(all_ranked_clothes[0:num_clothes],many = True)
        else:
            serializer = MenGarmentScoresSerializer(all_ranked_clothes[0:n],many = True)

        clothes_data = serializer.data
        #initialize data
        rank = 1
        score = -1
        index = 0

        for i in range(0,len(clothes_data)):
            #compute new rank
            if all_ranked_clothes[i].score != score:
                rank+=(i-index)
                index = i
                score = all_ranked_clothes[i].score
            #compute rank
            clothes_data[i]["rank"]=rank
            #add image_path
            clothes_data[i]["image_path"]=GarmentMen.objects.get(id = all_ranked_clothes[i].garment_id.id).image_path
        return clothes_data

class WomenGarmentScores(GarmentScores):
    garment_id = models.ForeignKey(GarmentWomen,on_delete = models.PROTECT)
    class Meta:
        unique_together = ['garment_id','user_gender']
    @staticmethod
    def get_num_clothes(rated_by):
        if rated_by not in gender_choices_dict.keys():
            return 0
        else:
            return WomenGarmentScores.objects.filter(user_gender = gender_choices_dict[rated_by]).count()
    @staticmethod
    def get_top_n_clothes(n,rated_by):
        if rated_by not in gender_choices_dict.keys():
            return None
        num_clothes = WomenGarmentScores.get_num_clothes(rated_by)
        all_ranked_clothes = WomenGarmentScores.objects.filter(user_gender = gender_choices_dict[rated_by]).order_by("-score")
        if(num_clothes<n):
            serializer = WomenGarmentScoresSerializer(all_ranked_clothes[0:num_clothes],many = True)
        else:
            serializer = WomenGarmentScoresSerializer(all_ranked_clothes[0:n],many = True)

        clothes_data = serializer.data
        #initialize data
        rank = 1
        score = -1
        index = 0

        for i in range(0,len(clothes_data)):
            #compute new rank
            if all_ranked_clothes[i].score != score:
                rank+=(i-index)
                index = i
                score = all_ranked_clothes[i].score
            #compute rank
            clothes_data[i]["rank"]=rank
            #add image_path
            clothes_data[i]["image_path"]=GarmentWomen.objects.get(id = all_ranked_clothes[i].garment_id.id).image_path
        return clothes_data




class OtherGarmentScores(GarmentScores):
    garment_id = models.ForeignKey(GarmentOthers,on_delete = models.PROTECT)
    class Meta:
        unique_together = ['garment_id','user_gender']


#serializers
class WomenGarmentRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GarmentWomen
        fields = ('id','image_path','count_for_each_ranking','score')
    
class WomenGarmentScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = WomenGarmentScores
        fields = ('garment_id','count_for_each_ranking','score')

class MenGarmentRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GarmentMen
        fields = ('id','image_path','count_for_each_ranking','score')

class MenGarmentScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenGarmentScores
        fields = ('garment_id','count_for_each_ranking','score')