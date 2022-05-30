from django.http import HttpResponse
from webapp.main_board import MainBoard
from django.shortcuts import render
from webapp.main_board import MainBoard
from django.http import JsonResponse


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'webapp/index.html')


def run_the_code(request):
    record = {"status": 0}
    if request.method == 'POST':
        number_of_players = int(request.POST['number_of_players'])
        deck_size = int(request.POST['deck_size'])
        setting_state = int(request.POST['setting_state'])
        list_of_num_of_players = [number_of_players]
        list_of_deck_size = [deck_size]
        list_of_setting_states = [setting_state]
        number_of_games = int(request.POST['number_of_games'])
        last_games_with_exp0 = int(request.POST['last_games_with_exp0'])
        sample_rate = int(request.POST['sample_rate'])
        number_of_repetition = int(request.POST['number_of_repetition'])
        number_of_levels = int(request.POST['number_of_levels'])
        number_of_lives = int(request.POST['number_of_lives'])
        common_pay_off = True if (request.POST['common_pay_off'] == "True") else False
        time_distortion = True if (request.POST['time_distortion'] == "True") else False
        decreasing_exp = True if (request.POST['decreasing_exp'] == "True") else False
        reset_level_time = True if (request.POST['reset_level_time'] == "True") else False

        game_settings = {"list_of_num_of_players": list_of_num_of_players,
                         "list_of_deck_size": list_of_deck_size,
                         "list_of_setting_states": list_of_setting_states,
                         "number_of_levels": number_of_levels,
                         "number_of_lives": number_of_lives
                              }

        execution_settings = {"number_of_games": number_of_games,
                              "common_pay_off": common_pay_off,
                              "last_games_with_exp0": last_games_with_exp0,
                              "sample_rate": sample_rate,
                              "number_of_repetition": number_of_repetition,
                              "time_distortion": time_distortion,
                              "decreasing_exp": decreasing_exp,
                              "reset_level_time": reset_level_time
                                   }

        record = MainBoard.run_code(game_settings, execution_settings)
        record["status"] = 1
    return JsonResponse(record)


def show_the_results(request):
    return render(request, 'webapp/results.html')

