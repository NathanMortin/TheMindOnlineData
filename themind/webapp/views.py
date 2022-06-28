from django.http import HttpResponse
from webapp.main_board import MainBoard
from django.shortcuts import render
from webapp.main_board import MainBoard
from django.http import JsonResponse
import os
from django.core.files.storage import FileSystemStorage
import errno
import random
from django.conf import settings
from django.shortcuts import redirect, render
from .analyzer import Analyzer
import numpy as np
BASE_DIR = settings.BASE_DIR

from webapp.models import Game, Agent


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'webapp/index.html')


def q_learning(request):
    return render(request, 'webapp/q_learning.html')


def q_learning_process(request):
    return render(request, 'webapp/q_learning_process.html')


def online_game(request):
    return render(request, 'webapp/online_game.html')


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

        console_settings = {"list_of_num_of_players": list_of_num_of_players,
                            "list_of_deck_size": list_of_deck_size,
                            "list_of_setting_states": list_of_setting_states}

        game_settings = {"number_of_levels": number_of_levels,
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

        record = MainBoard.run_code(console_settings, game_settings, execution_settings)
        record["status"] = 1
    return JsonResponse(record)


def show_the_results(request, record_filename="saa"):
    game_analyzer = Analyzer('records/'+record_filename)
    game_analyzer.interpretation()
    xml_dict = game_analyzer.get_xml_dict()
    avg_exp0_samples = xml_dict["root"]["experiment"]["avg_exp0_samples"]
    avg_number_of_wins_in_100 = xml_dict["root"]["experiment"]["avg_number_of_wins_in_100"]
    sample_rate = int(xml_dict["root"]["execution_settings"]["sample_rate"])
    number_of_games = int(xml_dict["root"]["execution_settings"]["number_of_games"])
    deck_size = int(xml_dict["root"]["game_settings"]["deck_size"])
    number_of_players = int(xml_dict["root"]["game_settings"]["number_of_players"])
    number_of_levels = int(xml_dict["root"]["game_settings"]["number_of_levels"])
    setting_state = int(xml_dict["root"]["execution_settings"]["setting_state"])
    avg_number_of_wins_in_100_list = []
    for e in range(0, len(avg_number_of_wins_in_100["item"])):
        avg_number_of_wins_in_100_list.append(float(avg_number_of_wins_in_100["item"][e]))
    avg_exp0_samples_list = []
    if type(avg_exp0_samples['item']) == list:
        for e in range(0, len(avg_exp0_samples["item"])):
            avg_exp0_samples_list.append(float(avg_exp0_samples["item"][e]))
    else:
        avg_exp0_samples_list.append(float(avg_exp0_samples['item']))
    game_rounds1 = np.arange(sample_rate, number_of_games + 1, sample_rate).tolist()
    game_rounds2 = np.arange((10*sample_rate), number_of_games + 1, (10*sample_rate)).tolist()

    winning_rate = xml_dict["root"]["experiment"]["winning_rate"]
    winning_rate_with_exploration_rate_0 = xml_dict["root"]["experiment"]["winning_rate_with_exploration_rate_0"]
    avg_num_of_correct_play = xml_dict["root"]["experiment"]["avg_num_of_correct_play"]
    avg_learning_wins = xml_dict["root"]["experiment"]["avg_learning_wins"]
    avg_number_of_losses = xml_dict["root"]["experiment"]["avg_number_of_losses"]
    avg_number_of_wins = xml_dict["root"]["experiment"]["avg_number_of_wins"]

    number_of_lives = int(xml_dict["root"]["game_settings"]["number_of_lives"])
    last_games_with_exp0 = int(xml_dict["root"]["execution_settings"]["last_games_with_exp0"])
    common_pay_off = 'true' if (xml_dict["root"]["execution_settings"]["common_pay_off"]) == 'True' else 'false'
    time_distortion = 'true' if (xml_dict["root"]["execution_settings"]["time_distortion"]) == 'True' else 'false'
    decreasing_exp = 'true' if (xml_dict["root"]["execution_settings"]["decreasing_exp"]) == 'True' else 'false'
    reset_level_time = 'true' if (xml_dict["root"]["execution_settings"]["reset_level_time"]) == 'True' else 'false'

    arg = {'avg_exp0_samples_list': avg_exp0_samples_list,
           'avg_number_of_wins_in_100_list': avg_number_of_wins_in_100_list,
           'sample_rate': sample_rate,
           'number_of_games': number_of_games,
           'deck_size': deck_size,
           'number_of_players': number_of_players,
           'number_of_levels': number_of_levels,
           'setting_state': setting_state,
           'game_rounds1': game_rounds1,
           'game_rounds2': game_rounds2,
           'winning_rate': winning_rate,
           'winning_rate_with_exploration_rate_0': winning_rate_with_exploration_rate_0,
           'avg_num_of_correct_play': avg_num_of_correct_play,
           'avg_learning_wins': avg_learning_wins,
           'avg_number_of_losses': avg_number_of_losses,
           'avg_number_of_wins': avg_number_of_wins,
           'number_of_lives': number_of_lives,
           'last_games_with_exp0': last_games_with_exp0,
           'common_pay_off': common_pay_off,
           'time_distortion': time_distortion,
           'decreasing_exp': decreasing_exp,
           'reset_level_time': reset_level_time
           }
    return render(request, 'webapp/results.html', arg)


def results(request):
    record_filename = request.GET['record_filename']
    return redirect('show_the_results', record_filename=record_filename)


def analyzer(request):
    return render(request, 'webapp/analyzer.html')


def __silent_remove(target_file_path):
    try:
        os.remove(target_file_path)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise e


def __save_uploaded_file(file):
    file_name, file_extension = str(file.name).rsplit('.', 1)

    if file_extension != 'xml':
        return None

    file_new_name = "records/"+file_name+".xml"
    FileSystemStorage().save(file_new_name, file)  # save file in BASIC-DIR for getting its size
    file_size = os.stat(file_new_name).st_size

    if file_size == 0:
        __silent_remove(file_new_name)
        return None

    return file_new_name


def upload(request):
    is_xml: bool = False
    response_data = {}

    if request.method == 'POST' and request.FILES['file']:
        try:
            uploaded_file_name = __save_uploaded_file(request.FILES['file'])
            if uploaded_file_name:  # set requested values
                is_xml = True
        except Exception as e:
            # clear all
            is_xml: bool = False

        response_data = {
                'is_xml': is_xml,
                'filename': uploaded_file_name}

    return JsonResponse(response_data)


def play_game(request):
    arg = {}
    if request.method == 'POST':
        number_of_players = int(request.POST['number_of_players'])
        deck_size = int(request.POST['deck_size'])
        setting_state = int(request.POST['setting_state'])
        number_of_levels = int(request.POST['number_of_levels'])
        number_of_lives = int(request.POST['number_of_lives'])
        common_pay_off = True if (request.POST['common_pay_off'] == "True") else False
        time_distortion = True if (request.POST['time_distortion'] == "True") else False
        decreasing_exp = True if (request.POST['decreasing_exp'] == "True") else False
        reset_level_time = True if (request.POST['reset_level_time'] == "True") else False

        game_settings = {"number_of_levels": number_of_levels,
                         "number_of_lives": number_of_lives,
                         "number_of_players": number_of_players,
                         "deck_size": deck_size
                         }

        execution_settings = {"common_pay_off": common_pay_off,
                              "time_distortion": time_distortion,
                              "decreasing_exp": decreasing_exp,
                              "reset_level_time": reset_level_time,
                              "setting_state": setting_state
                              }
        current_settings = {}
        players_settings = {}

        simulator = MainBoard.play_game(game_settings, execution_settings, current_settings, players_settings)
        ## DB

        # new_game = Game.objects.create(number_of_players=number_of_players, deck_size=deck_size,
        #                                number_of_levels=number_of_levels, deck=simulator["deck"],
        #                                game_time=simulator["game_time"], level_time=simulator["level_time"],
        #                                current_card=simulator["current_card"], current_level=simulator["current_level"],
        #                                number_of_lives=simulator["number_of_lives"],
        #                                number_of_throwing_stars=simulator["number_of_throwing_stars"],
        #                                level_cards=simulator["level_cards"], players_cards=simulator["players_cards"],
        #                                players_main_actions=simulator["players_main_actions"],
        #                                players_secondary_actions=simulator["players_secondary_actions"],
        #                                players_throwing_star_flag=simulator["players_throwing_star_flag"],
        #                                players_out_index=simulator["players_out_index"])
        # for i in range(number_of_players):
        #     new_agent = Agent.objects.create(game_id=new_game.game_id, cards= , )
        # arg["game_id"] = new_game.game_id
        # document_setting = DocumentSetting.objects.create(user=user, document=thesis)
        ##

    return render(request, 'webapp/play_game.html', arg)


