from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status

from django.shortcuts import render
from django.http import JsonResponse

from .data.serializer import GarmentMenSerializer,GarmentWomenSerializer, GarmentWomenRankingSerializer, WomenGarmentScoresSerializer
from .models import GarmentMen,GarmentWomen,GarmentOthers,Garment, MenGarmentScores, MenGarmentScoresSerializer, WomenGarmentScores
from .models import num_ranks,gender_choices,gender_choices_dict

import random
import traceback
from collections import defaultdict
import json
import logging

class MenClothesRetrievalView(APIView):
    def get(self,request,num_clothes):
        """
        Return an arbitrary number (defined by num_clothes) of random garments 
        """
        #history = request.data["history"]
        all_clothes = GarmentMen.objects.all().order_by('?')
        if(all_clothes.count() < 10):
            return Response("Not enough clothes", status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = GarmentMenSerializer(all_clothes[0:10],many=True)
            return Response(data = serializer.data, status=status.HTTP_200_OK)
        
class WomenClothesRetrievalView(APIView):
    def get(self,request,num_clothes):
        """
        Return an arbitrary number (defined by num_clothes) of random garments 
        """
        #history = request.data["history"]
        all_clothes = GarmentWomen.objects.all().order_by('?')
        if(all_clothes.count() < 10):
            return Response("Not enough clothes", status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = GarmentWomenSerializer(all_clothes[0:10],many=True)
            return Response(data = serializer.data, status=status.HTTP_200_OK)

class ClothesSummaryRankingsView(APIView):
    def post(self,request):
        """
        Args:
            request.data["gender"](string): gender of clothing to return
            request.data["clothing_id"](int): id of the garment
            request.data["num_clothes"](int): number of garments to retrieve. If 1, then retrieves clothing by given id no matter what. Else, get the top ranking clothings.
        Returns:
            Given its ID, returns rank of clothing, and number of 1st,2nd and 3rd positions the clothing got.
            Given num_clothes>1, returns a dictionary of dictionaries with top n (n=num_clothes) number of clothings as rated by each user_gender category (men,women,non-binary,prefer not to say) as a dictionary

        """
        if(request.data["gender"]=="men"):
            Garment = GarmentMen
            GarmentScores = MenGarmentScores
        elif (request.data["gender"]=="women"):
            Garment = GarmentWomen
            GarmentScores = WomenGarmentScores
        else:
            return Response(data = None, status = status.HTTP_400_BAD_REQUEST)
        if(request.data["num_clothes"]==1):
            clothing = Garment.objects.get(id=request.data["clothing_id"])
            #get garment rank
            clothing_score = clothing.score
            clothing_rank = Garment.get_rank(clothing_score)
            #get garment rankings
            clothing_rankings = GarmentScores.objects.filter(garment_id = request.data["clothing_id"])
            combined_garment_rankings = {'rank_'+str(rank+1):0 for rank in range(num_ranks)}
            for i in range(len(clothing_rankings)):
                user_rated_garment_rankings = clothing_rankings[i].count_for_each_ranking
                for (key,val) in combined_garment_rankings.items():
                    combined_garment_rankings[str(key)]+=user_rated_garment_rankings[str(key)]
            return Response(data = {"rank":clothing_rank,"rankings":combined_garment_rankings}, status = status.HTTP_200_OK)
        elif(request.data["num_clothes"]<=0):
            return Response(data = None, status = status.HTTP_400_BAD_REQUEST)
        else:
            num_clothes = request.data["num_clothes"]
            rated_by_all = Garment.get_top_n_clothes(num_clothes)
            rated_by_men = GarmentScores.get_top_n_clothes(num_clothes,"men")
            rated_by_women = GarmentScores.get_top_n_clothes(num_clothes,"women")
            rated_by_nb = GarmentScores.get_top_n_clothes(num_clothes,"non-binary")
            rated_by_un = GarmentScores.get_top_n_clothes(num_clothes,"prefer not to say")
            return Response(data = {"rated_by_all":rated_by_all,"rated_by_men":rated_by_men,"rated_by_women":rated_by_women,"rated_by_nb":rated_by_nb,"rated_by_un":rated_by_un}, status = status.HTTP_200_OK)

class ClothesUpdateRankingsView(APIView):
    def post(self,request):
        """
        updates rankings from game and returns cumulative rankings for winning clothes
        """
        if(request.data["gender"]=="men"):
            Garment = GarmentMen
            GarmentScores = MenGarmentScores
        elif (request.data["gender"]=="women"):
            Garment = GarmentWomen
            GarmentScores = WomenGarmentScores
        else:
            return Response(data = None, status = status.HTTP_400_BAD_REQUEST)
        results = request.data
        user_gender = request.data["user_gender"]
        clothes = Garment.objects.filter(id__in = request.data["game_rankings"].keys())
        clothes_id = [int(x) for x in request.data["game_rankings"].keys()]
        clothes_scores = GarmentScores.objects.filter(garment_id__in = request.data["game_rankings"].keys(),user_gender=gender_choices_dict[user_gender])
        clothes_index = defaultdict(lambda: "Not present")
        clothes_score_index = defaultdict(lambda: "Not present")
        #store queryset indexes of garment scores
        for i in range(len(clothes_scores)):
            clothes_score_index[clothes_scores[i].garment_id.id] = i
        #store queryset indexes of garment
        for i in range(len(clothes)):
            garment_id = clothes[i].id
            rank = results["game_rankings"][str(garment_id)]
            #obtain score for garment rank
            rank_score = Garment.get_rank_score(rank)
            #update scores for garment based on user gender
            if(clothes_score_index[garment_id] == 'Not present'):
                count_for_each_ranking={'rank_'+str(rank+1):0 for rank in range(num_ranks)}
                count_for_each_ranking['rank_'+str(rank)]+=1
                score = round(rank_score,2)
                garment_score = GarmentScores.objects.create(
                    garment_id=clothes[i],
                    user_gender=gender_choices_dict[user_gender],
                    count_for_each_ranking = count_for_each_ranking,
                    score = score,
                    )
                
            else:
                garment_score = clothes_scores[clothes_score_index[garment_id]]
                garment_score.count_for_each_ranking['rank_'+str(rank)]+=1
                garment_score.score = round(garment_score.score + rank_score,2)
            
            #update combined scores for garment
            clothes[i].score = round(clothes[i].score+rank_score,2)
            clothes_index[clothes[i].id] = i
            clothes[i].count_for_each_ranking['rank_'+str(rank)]+=1
        #update scores
        Garment.objects.bulk_update(clothes,["score","count_for_each_ranking"])
        GarmentScores.objects.bulk_update(clothes_scores,["score","count_for_each_ranking"])
        #get winning garment scores and rank
        if(clothes_index[int(results["winning_clothes_id"])]=="Not present"):
            return Response(data = None, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        winning_garment_index = clothes_index[int(results["winning_clothes_id"])]
        winning_garment = clothes[winning_garment_index]

        #get garment rank
        winning_garment_score = winning_garment.score
        winning_garment_rank = Garment.get_rank(winning_garment_score)
        #get garment rankings
        winning_garment_rankings = GarmentScores.objects.filter(garment_id = results["winning_clothes_id"])
        combined_garment_rankings = {'rank_'+str(rank+1):0 for rank in range(num_ranks)}
        for i in range(len(winning_garment_rankings)):
            user_rated_garment_rankings = winning_garment_rankings[i].count_for_each_ranking
            for (key,val) in combined_garment_rankings.items():
                combined_garment_rankings[str(key)]+=user_rated_garment_rankings[str(key)]
        return Response(data = {"rank":winning_garment_rank,"rankings":combined_garment_rankings}, status = status.HTTP_200_OK)

class ClothesOverview(APIView):
    def get(self,request,num_clothes_per_gender):
        if(num_clothes_per_gender<=0):
            return Response(data = None, status = status.HTTP_400_BAD_REQUEST)
        women_clothes = GarmentWomen.get_top_n_clothes(num_clothes_per_gender)
        men_clothes = GarmentMen.get_top_n_clothes(num_clothes_per_gender)
        return Response(data = women_clothes+men_clothes,status = status.HTTP_200_OK)

class UpdateScores(APIView):
    def get(self,request):
        garment_list = [GarmentMen,GarmentWomen,WomenGarmentScores,MenGarmentScores]
        for garment in garment_list:
            clothings = garment.objects.all()
            for i in range(len(clothings)):
                clothings[i].score = round(clothings[i].score,2)
            garment.objects.bulk_update(clothings,["score"])
        serializer = MenGarmentScoresSerializer(clothings[0:10],many=True)
        return Response(data = serializer.data, status=status.HTTP_200_OK)

class UpdateView(APIView):
    def get(self,request):
        clothings = GarmentWomen.objects.all()
        for clothes in clothings:
            combined_score = {'rank_'+str(x+1):0 for x in range(10)}
            clothes_scores = WomenGarmentScores.objects.filter(garment_id = clothes.id)
            if (clothes_scores.count()>0):
                print("STUPIDE")
                for clothes_score in clothes_scores:
                    for (key,value) in combined_score.items():
                        combined_score[key]+=clothes_score.count_for_each_ranking[key]
                for (key,value) in combined_score.items():
                    clothes.count_for_each_ranking[key]+=combined_score[key]
            else:
                pass
        GarmentWomen.objects.bulk_update(clothings,["count_for_each_ranking"])
        return Response(data = "HI", status = status.HTTP_200_OK)
    
class LogError(APIView):
    def post(self,request):
        error_types = {
            1:"blank_server_data"
        }
        if(type(request.data) is not dict):
            return Response(data = "Request body needs to be a dictionary", status = status.HTTP_400_BAD_REQUEST)
        if(request.data["error_type"] not in error_types.keys()):
            return Response(data = "Error type not valid", status = status.HTTP_400_BAD_REQUEST)
        with open(error_types[request.data["error_type"]]+".json","a+") as file:
            if("error_details" not in request.data):
                file.close()
            else:
                data = json.dumps(request.data["error_details"])+"\n"
                file.write(data)
                file.close()
        return Response(data = "Successfully logged error", status = status.HTTP_200_OK)
