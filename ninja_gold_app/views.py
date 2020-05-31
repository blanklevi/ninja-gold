from django.shortcuts import render, redirect
from time import strftime, gmtime
import random


def index(request):
    print(request.session['games'] + "index")
    if "game" in request.POST:
        request.session['games'] = request.POST['game']
    if 'message' not in request.session:
        request.session['message'] = []
    if 'gametype' not in request.session:
        request.session['games'] = []
    context = {
        'message': request.session['message'],
        'time': strftime("%m-%d-%Y %H:%M %p", gmtime()),
    }
    return render(request, "index.html", context)


def starting(request):
    if request.session['gold'] != 0:
        request.session['gold'] = 0
    request.session['message'] = []

    return render(request, "starting.html")


def process_money(request):
    game_type(request)
    print(request.session['games'] + "process money")
    time = strftime("%m-%d-%Y %H:%M %p", gmtime())
    if request.method == "POST" or "GET":
        if 'farm' in request.POST:
            score = random.randint(10, 20)
            message = "Earned " + str(score) + " from the farm! " + time

        elif 'cave' in request.POST:
            score = random.randint(5, 10)
            message = "Earned " + str(score) + " from the cave! " + time

        elif 'house' in request.POST:
            score = random.randint(2, 5)
            message = "Earned " + str(score) + " from the house! " + time

        elif 'casino' in request.POST:
            score = random.randint(-50, 50)
            if score > 0:
                message = "Earned " + str(score) + \
                    " gold from a casino! " + time
            else:
                message = "Entered a casino and lost " + \
                    str(score) + " gold... Ouch... " + time
        request.session['gold'] += score
        request.session['message'].append(message)
        request.session.save()
        print(request.session['gold'])
    return redirect('/')


def game_type(request):
    print(" i am alive gametype")
    if request.session['games'] == "movegame":
        if len(request.session['message']) == 20:
            if request.session['gold'] >= 275:
                request.session['message'].append(
                    'Winner Winner Chicken Dinner!')
                request.session.save()
            else:
                request.session['message'].append('You suck lol')
                request.session.save()
    if request.session['games'] == "goldgame":
        if request.session['gold'] >= 1000000:
            request.session['message'].append('Winner Winner Chicken Dinner!')
            request.session.save()
    return redirect('/')


def reset(request):
    if request.session['gold'] != 0:
        request.session['gold'] = 0
    request.session['message'] = []
    return render(request, "index.html")
