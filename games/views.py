from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import (PermissionDenied, login_required,
                                            permission_required)
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from games.forms import GameForm
from .models import Game, GameScore, GameState
from .serializers import GameSerializer
from django.views.decorators.cache import never_cache
import json
User = get_user_model()

MESSAGE_TYPE_SCORE = 'SCORE'
MESSAGE_TYPE_SAVE = 'SAVE'
MESSAGE_TYPE_LOAD_REQUEST = 'LOAD_REQUEST'
MESSAGE_BAD_REQUEST = "400 Bad request"

#game server
@login_required
def play_game(request, game_id):
    game = Game.objects.get(id = game_id)
    my_score = GameScore.objects.filter(player = request.user, ).order_by('-score')
    my_score = my_score.filter(game = game).order_by('-score').first()
    top_score = GameScore.objects.filter(game = game).order_by('-score').first()
    if request.is_ajax():
        message_type = request.POST.get("messageType")
        if message_type == MESSAGE_TYPE_SCORE:
            action_func = save_score
        elif message_type == MESSAGE_TYPE_SAVE:
            action_func = save_state
        elif message_type == MESSAGE_TYPE_LOAD_REQUEST:
            action_func = load_game
        else:
            return HttpResponseBadRequest()
        return action_func(request, game)
    context = {
        'game': game,
        'my_score': my_score,
        'top_score': top_score, 
        "games": Game.objects.filter(users=request.user) #games that user owns
    }
    return render(request, "game_play.html", context)

#save and show game score
@never_cache
def save_score(request, game):
    try:
        score_value = request.POST["score"]
    except KeyError:
        return HttpResponseBadRequest(MESSAGE_BAD_REQUEST)
    if( int(score_value) < 0 ):
        return HttpResponseBadRequest(MESSAGE_BAD_REQUEST)
    GameScore.objects.create(
        score=score_value, game=game, player=request.user
    )
    global_best_score = GameScore.objects.filter(game=game).order_by('-score').first()
    my_high_score = game.user_best_score(request.user)
    g = Game.objects.get(name=game.name)
    if (g.globalScore):
        if(int(score_value) > int(g.globalScore) ):
            g.globalScore = int(score_value)
            g.save()
    else:
        g.globalScore = int(score_value)
        g.save()
    return JsonResponse({
        'myBestScore': my_high_score,
        'globalBestScore': global_best_score.score
    })

#save game state
@never_cache
def save_state(request, game):
    try:
        game_state_data = json.loads(request.POST['gameState'])
    except KeyError:
        return HttpResponseBadRequest(MESSAGE_BAD_REQUEST)
    GameState.objects.create(
        player=request.user, game=game, state_data=game_state_data
    )
    return JsonResponse(game_state_data)

#load game state
@never_cache
def load_game(request, game):
    last_state = game.user_last_state(request.user)
    if last_state is None:
        return HttpResponseBadRequest(MESSAGE_BAD_REQUEST)
    else:
        return JsonResponse(last_state.state_data)

#create game
@login_required
def game_create(request):
    form = GameForm()
    return render(request, 'game_form.html', context={'form': form, 'create': True, 'isDeveloper': request.user.isDeveloper})

#edit game
@login_required
def game_edit(request, id):
    game = get_object_or_404(Game, id=id)
    if not request.user.created_game(game):
        raise PermissionDenied
    if request.POST:
        form = GameForm(data=request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = GameForm(instance=game)
    return render(request, 'game_form.html', context={'form': form, 'create': False, 'game':game.id})

@login_required
def game_delete(request, id):
    game = get_object_or_404(Game, id=id)

    if not request.user.created_game(game):
        raise PermissionDenied
    
    game.delete()
    return redirect('inventory')
    