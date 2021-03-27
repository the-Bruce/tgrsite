from random import randint
from django.contrib.messages import add_message
from django.contrib.messages import constants as messages

def mystery_middleware(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            # Perform the extremely complex TabletopCoin algorithm
            action_worth = randint(-80, 20)
            if action_worth >= 0:
                coins_won = 1 + action_worth * 4
                request.user.member.award_coin(coins_won)
                add_message(request, messages.SUCCESS,
                    f"You earned {coins_won} TabletopCoin for interacting with the website!")
        response = get_response(request)
        return response
    return middleware