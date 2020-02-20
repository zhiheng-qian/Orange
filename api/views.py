import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotFound, JsonResponse)
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from games.forms import GameForm
from games.models import Game, GameScore
from games.serializers import GameSerializer

User = get_user_model()

# get all games data by GET and add game by POST
@api_view(['GET', 'POST'])
def games(request):
    if request.method == 'GET':
        context = {
            "games": Game.objects.all(),
            "scores": GameScore.objects.all()
        }
        return render(request, 'home.html', context)
    elif request.method == 'POST':
        game = request.data.copy()
        name = request.data['name']
        game['developer'] = request.user.username
        serializer = GameSerializer(data=game)
        # form = GameForm()
        # return render(request, 'game_form.html', context={'form': form, 'create': True})
        if serializer.is_valid():
            serializer.save()
            g = Game.objects.get(name=name)
            request.user.games.add(g)
            return redirect('inventory')
        return redirect('game_upload_fail')

# edit game by PUT and delte by DELETE
@login_required
@api_view(['GET', 'PUT', 'DELETE'])
def game_detail(request, id):
    if request.method == 'PUT':
        game =get_object_or_404(Game, id=id)
        serializer = GameSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("saved")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        game =get_object_or_404(Game, id=id)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return redirect('game_upload_fail')

# get all game information and return to game info page
@api_view(['GET'])
def game_info(request, id):
    if request.method == 'GET':
        try:
            game = Game.objects.get(pk=id)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        context = {
            "game": game
        }
        return render(request, 'game_info.html', context)

# api for game, use for game service
@api_view(['GET', 'POST'])
def game_api(request, id):
    try:
        game = Game.objects.get(pk=id)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = {"results": {
            "state": game.gameStates,
            "globalScore": game.globalScore,
            "score": game.localScore
        }}
        return JsonResponse(data)
    if request.method == 'POST':
        json_data = json.loads(request.body)
        test = json_data['test']
        localScore = test['score']
        state = test['state']
        globalScore = test['globalScore']
        game.localScore = localScore
        game.gameStates = state
        game.globalScore = globalScore
        game.save()
        data = {"test": {
            "state": game.gameStates,
            "globalScore": game.globalScore,
            "score": game.localScore
        }}
        return JsonResponse(json_data)

# return game's logo
@api_view(['GET'])
def game_logo(request, id):
    if request.method == 'GET':
        try:
            game = Game.objects.get(pk=id)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return HttpResponse(game.logo, content_type="image/png")

def game_upload_fail(request):
    return render(request, 'upload_fail.html')
