from webapp.game import Game
import traceback


class MainBoard:

    def __init__(self):
        pass

    @staticmethod
    def run_code():
        # Game Settings
        list_of_num_of_players = [2]  # 2, 3, 4 players
        list_of_deck_size = [4]  # 25, 50, 75, 100 deck size
        list_of_setting_states = [3]  # 1, 2, 3, 4

        for number_of_players in list_of_num_of_players:
            for deck_size in list_of_deck_size:
                for setting_state in list_of_setting_states:

                    # Execution Settings
                    number_of_games = 500000  # should be a factor of 100
                    common_pay_off = True
                    last_games_with_zero_exploitation = 200
                    sample_rate = 100
                    number_of_repetition = 1  # 10

                    # record
                    print("number_of_players: " + str(number_of_players))
                    print("deck_size: " + str(deck_size))
                    print("number_of_games: " + str(number_of_games))
                    print("setting_state: " + str(setting_state))
                    f = open("report_"+str(number_of_players)+"_"+str(deck_size)+"_"+str(setting_state)+".txt", "a")
                    f.write("#### The Mind ####\n")
                    f.write("\tnumber_of_players: "+str(number_of_players)+"\n")
                    f.write("\tdeck_size: "+str(deck_size)+"\n")
                    f.write("\tnumber_of_games: "+str(number_of_games)+"\n")
                    f.write("\tsetting_state: "+str(setting_state)+"\n\n")

                    try:
                        # results initialization
                        sum_number_of_wins = 0
                        sum_number_of_losses = 0
                        sum_learning_wins = 0
                        sum_of_correct_play = 0
                        list_of_winning_samples = []
                        list_of_exp0_samples = []  # TODO: exp0 sampling

                        # Executions
                        for i in range(number_of_repetition):
                            # Game running
                            simulator = Game(number_of_players, deck_size)
                            result = simulator.run_game(number_of_games, common_pay_off, setting_state,
                                                        last_games_with_zero_exploitation, sample_rate, f)
                            # TODO: exp0_samples is added
                            number_of_wins, number_of_losses, learning_wins, winning_samples, exp0_samples, [num_of_correct,
                                                                                                             num_of_wrong,
                                                                                                             num_of_out] = result

                            # sums of the results for getting the averages
                            sum_number_of_wins += number_of_wins
                            sum_number_of_losses += number_of_losses
                            sum_learning_wins += learning_wins
                            sum_of_correct_play += (num_of_correct / (num_of_correct + num_of_wrong))
                            list_of_winning_samples.append(winning_samples)
                            list_of_exp0_samples.append(exp0_samples)  # TODO: exp0 sampling

                        # average of winning rates
                        avg_number_of_wins = sum_number_of_wins / number_of_repetition
                        avg_number_of_losses = sum_number_of_losses / number_of_repetition
                        avg_learning_wins = sum_learning_wins / number_of_repetition
                        avg_num_of_correct_play = sum_of_correct_play / number_of_repetition

                        # average of winning samples
                        avg_winning_samples = []
                        avg_exp0_samples = []  # TODO: exp0 sampling
                        for j in range(int(number_of_games/sample_rate)):
                            sum_value = 0
                            sum_result = 0
                            for i in range(number_of_repetition):
                                sum_value += list_of_winning_samples[i][j]
                                sum_result += list_of_exp0_samples[i][j]
                            avg_winning_samples.append(sum_value/number_of_repetition)
                            avg_exp0_samples.append(sum_result/number_of_repetition)  # TODO: exp0 sampling

                        # record
                        print("\tavg_number_of_wins: " + str(round(avg_number_of_wins, 4)) + "\n")
                        print("\tavg_number_of_losses: " + str(round(avg_number_of_losses, 4)) + "\n")
                        print("\tavg_learning_wins: " + str(round(avg_learning_wins, 4)) + "\n")
                        print("\tavg_num_of_correct_play: " + str(round(avg_num_of_correct_play, 4)))
                        print("\twinning rate: " + str(round((avg_number_of_wins/number_of_games), 4)) + "\n")
                        print("\twinning rate with exploration rate 0: " +
                              str(round((avg_learning_wins/last_games_with_zero_exploitation), 4)) + "\n")

                        f.write("\tavg_number_of_wins_in_100: " + str(avg_winning_samples) + "\n")
                        f.write("\tavg_exp0_samples: " + str(avg_exp0_samples) + "\n")
                        f.write("\tavg_number_of_wins: " + str(round(avg_number_of_wins, 4)) + "\n")
                        f.write("\tavg_number_of_losses: " + str(round(avg_number_of_losses, 4)) + "\n")
                        f.write("\tavg_learning_wins: " + str(round(avg_learning_wins, 4)) + "\n")
                        f.write("\tavg_learning_wins: " + str(round(avg_learning_wins, 4)) + "\n")
                        f.write("\tavg_num_of_correct_play: " + str(round(avg_num_of_correct_play, 4)) + "\n")
                        f.write("\twinning rate: " + str(round((avg_number_of_wins / number_of_games), 4)) + "\n")
                        f.write("\twinning rate with exploration rate 0: " +
                                str(round((avg_learning_wins / last_games_with_zero_exploitation), 4)) + "\n")
                        f.close()
                    except Exception as e:
                        f.write("^ "+str(repr(e))+"\n")
                        traceback.print_exc()
                        f.close()


