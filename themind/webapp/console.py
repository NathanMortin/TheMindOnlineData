from webapp.game import Game
from webapp.timer import Timer
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString


class Console:
    record = {}

    def __init__(self, game_setup):
        self.console_settings, self.game_settings, self.execution_settings = game_setup
        self.record_file_name = Timer.get_current_date() + "_" + Timer.get_current_time() + ".xml"

    @staticmethod
    def get_record_file_name():
        return Timer.get_current_date() + "_" + Timer.get_current_time()

    def run(self):
        list_of_num_of_players = self.console_settings["list_of_num_of_players"]
        list_of_deck_size = self.console_settings["list_of_deck_size"]
        list_of_setting_states = self.console_settings["list_of_setting_states"]

        number_of_games = self.execution_settings["number_of_games"]
        number_of_repetition = self.execution_settings["number_of_repetition"]
        last_games_with_exp0 = self.execution_settings["last_games_with_exp0"]
        sample_rate = self.execution_settings["sample_rate"]

        running_time = Timer(name="run_all_code")
        running_time.start()

        file_counter = 1
        for number_of_players in list_of_num_of_players:
            for deck_size in list_of_deck_size:
                for setting_state in list_of_setting_states:
                    self.game_settings["number_of_players"] = number_of_players
                    self.game_settings["deck_size"] = deck_size

                    self.execution_settings["setting_state"] = setting_state

                    t = Timer(name="run_game")

                    # record
                    print("number_of_players: " + str(number_of_players))
                    print("deck_size: " + str(deck_size))
                    print("number_of_games: " + str(number_of_games))
                    print("setting_state: " + str(setting_state))

                    experiment = {"number_of_players": number_of_players,
                                  "deck_size": deck_size,
                                  "setting_state": setting_state}
                    try:
                        # results initialization
                        sum_number_of_wins = 0
                        sum_number_of_losses = 0
                        sum_learning_wins = 0
                        sum_of_correct_play = 0
                        list_of_winning_samples = []
                        list_of_exp0_samples = []
                        repeated_executions = []

                        # Executions
                        for i in range(number_of_repetition):
                            exe_info = {"execution_number": i}

                            # Game running
                            t.start()

                            simulator = Game(self.game_settings)
                            result = simulator.run_game(self.execution_settings)

                            elapsed_time = t.stop()
                            exe_info["elapsed_time"] = round(elapsed_time, 4)

                            number_of_wins, number_of_losses, learning_wins, winning_samples, exp0_samples, [
                                num_of_correct,
                                num_of_wrong,
                                num_of_out] = result

                            print("\tnumber_of_wins: " + str(number_of_wins) + "\n")
                            print("\tnumber_of_losses: " + str(number_of_losses) + "\n")
                            print("\tnumber_of_learning_wins: " + str(learning_wins) + "\n")
                            print("\tnum_of_correct: " + str(num_of_correct) + "\n")
                            print("\tnum_of_wrong: " + str(num_of_wrong) + "\n")
                            print("\tnum_of_out: " + str(num_of_out) + "\n\n")
                            exe_info["number_of_wins"] = number_of_wins
                            exe_info["number_of_losses"] = number_of_losses
                            exe_info["number_of_learning_wins"] = learning_wins
                            exe_info["num_of_correct"] = num_of_correct
                            exe_info["num_of_wrong"] = num_of_wrong
                            exe_info["num_of_out"] = num_of_out
                            repeated_executions.append(exe_info)

                            # sums of the results for getting the averages
                            sum_number_of_wins += number_of_wins
                            sum_number_of_losses += number_of_losses
                            sum_learning_wins += learning_wins
                            sum_of_correct_play += (num_of_correct / (num_of_correct + num_of_wrong))
                            list_of_winning_samples.append(winning_samples)
                            list_of_exp0_samples.append(exp0_samples)

                        experiment["executions"] = repeated_executions
                        accu_time = Timer.timers["run_game"]
                        print(f"All games were run in {accu_time:0.2f} seconds")
                        experiment["executions_time"] = round(accu_time, 4)

                        # average of winning rates
                        avg_number_of_wins = sum_number_of_wins / number_of_repetition
                        avg_number_of_losses = sum_number_of_losses / number_of_repetition
                        avg_learning_wins = sum_learning_wins / number_of_repetition
                        avg_num_of_correct_play = sum_of_correct_play / number_of_repetition

                        # average of winning samples
                        avg_winning_samples = []
                        avg_exp0_samples = []
                        for j in range(int(number_of_games / sample_rate)):
                            sum_value = 0
                            for i in range(number_of_repetition):
                                sum_value += list_of_winning_samples[i][j]
                            avg_winning_samples.append(sum_value / number_of_repetition)

                        for j in range(int(number_of_games / (10 * sample_rate))):
                            sum_result = 0
                            for i in range(number_of_repetition):
                                sum_result += list_of_exp0_samples[i][j]
                            avg_exp0_samples.append(sum_result / number_of_repetition)

                        # record
                        print("\tavg_number_of_wins: " + str(round(avg_number_of_wins, 4)) + "\n")
                        print("\tavg_number_of_losses: " + str(round(avg_number_of_losses, 4)) + "\n")
                        print("\tavg_learning_wins: " + str(round(avg_learning_wins, 4)) + "\n")
                        print("\tavg_num_of_correct_play: " + str(round(avg_num_of_correct_play, 4)))
                        print("\twinning rate: " + str(round((avg_number_of_wins / number_of_games), 4)) + "\n")
                        print("\twinning rate with exploration rate 0: " +
                              str(round((avg_learning_wins / last_games_with_exp0), 4)) + "\n")

                        experiment["avg_number_of_wins_in_100"] = avg_winning_samples
                        experiment["avg_exp0_samples"] = avg_exp0_samples
                        experiment["avg_number_of_wins"] = round(avg_number_of_wins, 4)
                        experiment["avg_number_of_losses"] = round(avg_number_of_losses, 4)
                        experiment["avg_learning_wins"] = round(avg_learning_wins, 4)
                        experiment["avg_num_of_correct_play"] = round(avg_num_of_correct_play, 4)
                        experiment["winning_rate"] = round((avg_number_of_wins / number_of_games), 4)
                        experiment["winning_rate_with_exploration_rate_0"] = \
                            round((avg_learning_wins / last_games_with_exp0), 4)

                    except Exception as e:
                        print("Error!!", e)

                        self.record["game_settings"] = self.game_settings
                        self.record["execution_settings"] = self.execution_settings
                        self.record["experiment"] = experiment
                        record_filename = self.get_record_file_name()+str(file_counter)+".xml"
                        self.record["record_file_name"] = record_filename
                        xml = dicttoxml(self.record, attr_type=False)
                        dom = parseString(xml)
                        with open("records/" + record_filename, 'w') as result_file:
                            result_file.write(dom.toprettyxml())

                        return self.record

                    self.record["game_settings"] = self.game_settings
                    self.record["execution_settings"] = self.execution_settings
                    self.record["experiment"] = experiment
                    record_filename = self.get_record_file_name() + str(file_counter) + ".xml"
                    self.record["record_file_name"] = record_filename
                    xml = dicttoxml(self.record, attr_type=False)
                    dom = parseString(xml)
                    with open("records/" + record_filename, 'w') as result_file:
                        result_file.write(dom.toprettyxml())
                    file_counter += 1
        elapsed_time = running_time.stop()
        print(elapsed_time)
        return self.record

    def play_game(self, current_settings, players_settings):
        simulator = Game(self.game_settings)
        simulator.set_game_state(current_settings, players_settings)
        return simulator.play_game(self.execution_settings)



