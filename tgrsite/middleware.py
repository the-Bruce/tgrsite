from users.achievements import give_achievement_once

from random import randint
from django.contrib.messages import add_message
from django.contrib.messages import constants as messages
from django.http import JsonResponse

def tabletopcoin_algo():
    return randint(0, 100)

def tabletopcoin_uncertainty():
    return randint(0, 2)

def mystery_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        if not isinstance(response, JsonResponse) and response.status_code == 200 and request.method == 'GET' and request.user.is_authenticated:
            # Perform the extremely complex TabletopCoin algorithm
            action_worth = tabletopcoin_algo()
            uncertainty = tabletopcoin_uncertainty()
            if 70 <= action_worth <= 100:
                coins_won = uncertainty + (action_worth - 69) * 3
                request.user.member.award_coin(coins_won)
                add_message(request, messages.SUCCESS,
                    f"You earned {coins_won} TabletopCoin for interacting with the website!")
            elif 0 <= action_worth <= 20:
                coins_lost = uncertainty + 1 + action_worth * 2
                request.user.member.award_coin(-coins_lost)
                add_message(request, messages.ERROR,
                    f"You lost {coins_lost} TabletopCoin for interacting badly with the website.")
            if request.user.member.coin() >= 1000:
                give_achievement_once(request.user.member, "moneybags")
        return response
    return middleware