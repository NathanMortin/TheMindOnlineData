from webapp.console import Console


class MainBoard:

    def __init__(self):

        # Game Settings
        list_of_num_of_players = [2]  # 2, 3, 4 players
        list_of_deck_size = [8]  # 25, 50, 75, 100 deck size
        list_of_setting_states = [1, 2, 3, 4]  # 1, 2, 3, 4

        # Execution Settings
        number_of_games = 1200  # should be a factor of 1000
        common_pay_off = True
        last_games_with_exp0 = 4
        sample_rate = 2
        number_of_repetition = 2
        time_distortion = False
        decreasing_exp = False
        number_of_levels = 2
        number_of_lives = 2
        reset_level_time = False

        # Console Setup
        self.game_settings = {"list_of_num_of_players": list_of_num_of_players,
                              "list_of_deck_size": list_of_deck_size,
                              "list_of_setting_states": list_of_setting_states,
                              "number_of_levels": number_of_levels,
                              "number_of_lives": number_of_lives
                              }

        self.execution_settings = {"number_of_games": number_of_games,
                                   "common_pay_off": common_pay_off,
                                   "last_games_with_exp0": last_games_with_exp0,
                                   "sample_rate": sample_rate,
                                   "number_of_repetition": number_of_repetition,
                                   "time_distortion": time_distortion,
                                   "decreasing_exp": decreasing_exp,
                                   "reset_level_time": reset_level_time
                                   }
        # self.run_code(self.game_settings, self.execution_settings)

    @staticmethod
    def run_code(game_settings, execution_settings):

        game_setup = [game_settings, execution_settings]
        the_mind_console = Console(game_setup)
        return the_mind_console.run()








