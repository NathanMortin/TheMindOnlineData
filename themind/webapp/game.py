import random
from webapp.agent import Agent
from enum import Enum


class Action(Enum):
    NO_ACTION = -1
    PLAY = 0
    WAIT = 1

    TURN_ON_THROWING_STAR_CARD = 2
    TURN_OFF_THROWING_STAR_CARD = 3


class Game:
    def __init__(self, number_of_players, deck_size):
        # game rules
        self.number_of_levels_rule = {2: 1, 3: 1, 4: 1}  # TODO number_of_levels_rule
        self.deck_size = deck_size
        self.number_of_players = number_of_players
        self.number_of_levels = self.get_number_of_levels()

        # game initializing
        self.number_of_wins = 0
        self.number_of_losses = 0
        self.players = []
        for i in range(number_of_players):
            player = Agent(i)
            player.set_clock_rate(random.randint(0, 10))  # TODO: is added for time distortion
            self.players.append(player)

        # reset parameters & distribute cards
        self.deck = list(range(1, deck_size + 1))
        self.game_time = 1
        self.level_time = 1
        self.current_card = 0
        self.current_level = 1
        self.number_of_lives = 1  # TODO number_of_players
        self.number_of_throwing_stars = 1
        self.level_cards = []
        self.players_cards = []
        self.players_main_actions = []
        self.players_secondary_actions = []
        self.players_throwing_star_flag = []
        self.players_out_index = []
        for i in range(number_of_players):
            self.players[i].clear_cards()
            self.players_throwing_star_flag.append(False)
            self.players_cards.append([])
            self.players_main_actions.append([])
            self.players_secondary_actions.append([])

        # distribute cards and make game ready
        self.distribute_cards()

    def get_number_of_levels(self):
        return self.number_of_levels_rule[self.number_of_players]

    def get_game_time(self):
        return self.game_time

    def get_card_from_deck(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        if len(self.deck) == 0:
            a = 1
        return card

    def get_current_card(self):
        return self.current_card

    def get_current_level(self):
        return self.current_level

    def get_number_of_lives(self):
        return self.number_of_lives

    def get_number_of_throwing_stars(self):
        return self.number_of_throwing_stars

    def level_up(self):
        self.level_time = 1
        # self.deck = list(range(1, self.deck_size+1))
        # rules about lives and throwing stars card
        level_reward = 0
        if self.current_level == 2:
            self.number_of_throwing_stars += 1
            level_reward = 1
        elif self.current_level == 3:
            self.number_of_lives += 1
            level_reward = 2
        elif self.current_level == 5:
            self.number_of_throwing_stars += 1
            level_reward = 1
        elif self.current_level == 6:
            if self.number_of_lives < 5:
                self.number_of_lives += 1
                level_reward = 2
        elif self.current_level == 8:
            if self.number_of_throwing_stars < 3:
                self.number_of_throwing_stars += 1
                level_reward = 1
        elif self.current_level == 9:
            if self.number_of_lives < 5:
                self.number_of_lives += 1
                level_reward = 2
        self.current_level += 1
        if self.current_level <= self.number_of_levels:
            self.distribute_cards()
        self.current_card = 0

        # reset agent current time TODO: add for time distortion
        for i in range(self.number_of_players):
            self.players[i].reset_current_time()
        return level_reward

    def distribute_cards(self):
        level_cards = []
        self.players_out_index = []
        for i in range(self.number_of_players):
            for j in range(self.current_level):
                card = self.get_card_from_deck()
                cards = self.players[i].add_to_cards(card)
                self.players_cards[i] = cards
                level_cards.append(card)
            self.players_main_actions[i] = [Action.PLAY.value, Action.WAIT.value]
            if self.number_of_throwing_stars:
                self.players_secondary_actions[i] = [Action.TURN_OFF_THROWING_STAR_CARD.value]
                # self.players_secondary_actions[i] = [Action.TURN_ON_THROWING_STAR_CARD.value,
                #                                      Action.TURN_OFF_THROWING_STAR_CARD.value]
        level_cards.sort()
        self.level_cards = level_cards
        self.deck = list(range(1, self.deck_size + 1))

    def get_number_of_other_players_cards(self, index):
        num_of_cards = []
        for i in range(self.number_of_players):
            if i == index:
                continue
            num_of_cards.append(len(self.players[i].cards))
        return num_of_cards

    def verification(self, player_index, playing_card):
        if not self.level_cards:
            return False
        if not self.level_cards.index(playing_card):
            self.level_cards.pop(0)
            self.players[player_index].remove_card(playing_card)
            if not len(self.players_cards[player_index]):
                if Action.PLAY.value in self.players_main_actions[player_index]:
                    self.players_main_actions[player_index].remove(Action.PLAY.value)
                if Action.TURN_ON_THROWING_STAR_CARD.value in self.players_secondary_actions[player_index]:
                    self.players_secondary_actions[player_index].remove(Action.TURN_ON_THROWING_STAR_CARD.value)
                # self.players_throwing_star_flag[player_index] = True
            self.current_card = playing_card
            return True
        else:
            self.number_of_lives -= 1
            for i in range(len(self.players_cards)):
                if i == player_index:
                    continue
                cards = self.players_cards[i]
                removed_cards = [card for card in cards if card < playing_card]
                for r in removed_cards:
                    self.players_cards[i].remove(r)
                    self.level_cards.remove(r)
                if not len(self.players_cards[i]):
                    if Action.PLAY.value in self.players_main_actions[i]:
                        self.players_main_actions[i].remove(Action.PLAY.value)
                    if Action.TURN_ON_THROWING_STAR_CARD.value in self.players_secondary_actions[i]:
                        self.players_secondary_actions[i].remove(Action.TURN_ON_THROWING_STAR_CARD.value)
                    # self.players_throwing_star_flag[i] = True
            self.players[player_index].remove_card(playing_card)
            if not len(self.players_cards[player_index]):
                if Action.PLAY.value in self.players_main_actions[player_index]:
                    self.players_main_actions[player_index].remove(Action.PLAY.value)
                if Action.TURN_ON_THROWING_STAR_CARD.value in self.players_secondary_actions[player_index]:
                    self.players_secondary_actions[player_index].remove(Action.TURN_ON_THROWING_STAR_CARD.value)
                # self.players_throwing_star_flag[player_index] = True
            self.level_cards.remove(playing_card)
            self.current_card = playing_card
            return False

    def throwing_star_process(self):
        if all(flag is True for flag in self.players_throwing_star_flag):
            self.using_throwing_star_card()
            if self.number_of_throwing_stars:
                for i in range(len(self.players)):
                    self.players_secondary_actions[i] = [Action.TURN_ON_THROWING_STAR_CARD.value,
                                                         Action.TURN_OFF_THROWING_STAR_CARD.value]
            else:
                for i in range(len(self.players)):
                    self.players_secondary_actions[i] = [Action.TURN_OFF_THROWING_STAR_CARD.value]
                    self.players_throwing_star_flag[i] = False
            return True
        return False

    def using_throwing_star_card(self):
        if self.number_of_throwing_stars > 0:
            self.number_of_throwing_stars -= 1
            for i in range(self.number_of_players):
                if len(self.players_cards[i]):
                    card = self.players_cards[i].pop(0)
                    self.players[i].remove_card(card)
                    self.level_cards.remove(card)
                if not len(self.players_cards[i]):
                    if Action.PLAY.value in self.players_main_actions[i]:
                        self.players_main_actions[i].remove(Action.PLAY.value)
                    if Action.TURN_ON_THROWING_STAR_CARD.value in self.players_secondary_actions[i]:
                        self.players_secondary_actions[i].remove(Action.TURN_ON_THROWING_STAR_CARD.value)
                    # self.players_throwing_star_flag[i] = True

    def run_game(self, number_of_games, common_pay_off, setting_state, last_games_with_zero_exploitation,
                 sample_rate, f):

        # results initialization
        learning_wins = 0
        list_of_sample_wins = []
        list_of_exp0_samples = []
        sample_wins = 0
        num_of_correct = 0
        num_of_wrong = 0
        num_of_out = 0
        game_result = True

        # execution of games
        for game_i in range(number_of_games):

            # update number of cards which are not played
            num_of_out += len(self.level_cards)

            # play until win (complete the levels) or loose (have no life)
            while self.number_of_lives > 0 and self.current_level <= self.number_of_levels:
                game_result = True  # default assumption for game result in this cycle

                # check agents have cards
                if len(self.level_cards):

                    players_main_actions = []
                    players_secondary_actions = []

                    # decision
                    for i in range(self.number_of_players):

                        # check that agent has at least one card
                        if i in self.players_out_index:
                            players_main_actions.insert(i, Action.NO_ACTION)
                            players_secondary_actions.insert(i, Action.NO_ACTION)
                            continue
                        # TODO: self.level_time is changed for time distortion
                        main_act, secondary_act = self.players[i].make_decision(self.current_card, self.deck_size,
                                                                                self.players[i].get_current_time(),
                                                                                self.players_throwing_star_flag,
                                                                                self.get_number_of_other_players_cards(i),
                                                                                self.players_main_actions[i],
                                                                                self.players_secondary_actions[i],
                                                                                setting_state)
                        main_act = Action(main_act)
                        secondary_act = Action(secondary_act)
                        players_main_actions.insert(i, main_act)
                        players_secondary_actions.insert(i, secondary_act)

                    # shuffle players' turn
                    players_index = list(range(self.number_of_players))
                    random.shuffle(players_index)

                    # check request for using throwing star card
                    # for i in range(self.number_of_players):
                    #     secondary_act = players_secondary_actions[i]
                    #     if secondary_act == Action.TURN_ON_THROWING_STAR_CARD:
                    #         self.players_throwing_star_flag[i] = True
                    #     else:
                    #         self.players_throwing_star_flag[i] = False
                    # throwing_used = self.throwing_star_process()
                    # if throwing_used:
                    #     f.write("\t\t\t && Throwing star card is used! &&\n")

                    # run players' action
                    for i in players_index:

                        # check that agent has at least one card
                        if i in self.players_out_index:
                            continue

                        # action PLAY
                        if players_main_actions[i] == Action.PLAY:

                            # check agent has card (because of throwing star card, empty hand may be happened)
                            if len(self.players_cards[i]) > 0:
                                min_card = self.players[i].play_card()  # run playing card
                                result = self.verification(i, min_card)  # check that agent played correctly or wrongly

                                # calculating the reward in non common pay off mode
                                if not common_pay_off:
                                    reward = self.players[i].get_reward(result)  # get reward +1 or -1
                                    self.players[i].set_current_reward(reward)  # set the reward

                                # check that agent played correctly or not
                                if not result:
                                    game_result = False  # stop the game if one agent played wrongly
                                    num_of_wrong += 1  # add 1 to number of cards which are played wrongly
                                    break
                                else:
                                    num_of_correct += 1  # add 1 to number of cards which are played correctly

                        # action WAIT
                        else:
                            self.players[i].wait()

                    # calculating the reward in non common pay off mode
                    if common_pay_off:
                        if Action.PLAY in players_main_actions:  # if one player played a card
                            for p in self.players:

                                # check that agent has at least one card
                                if p.player_id in self.players_out_index:
                                    continue

                                p.set_current_reward(p.get_reward(game_result))  # set the reward based on the result

                    # update the table of agent who played or waited
                    for i in range(self.number_of_players):

                        # check that agent has at least one card
                        if i in self.players_out_index:
                            continue

                        # set the next state TODO: self.level_time+1 is changed for time distortion
                        self.players[i].set_next_state(self.current_card, self.deck_size, self.players[i].get_next_time(),
                                                       self.players_throwing_star_flag,
                                                       self.get_number_of_other_players_cards(i),
                                                       setting_state)


                        # check whether the agent could play or wait and the game was not stopped
                        if self.players[i].get_played():
                            self.players[i].update_table(f)  # update Q-table

                        # check that agent has at least one card
                        if len(self.players_cards[i]) == 0:
                            self.players_out_index.append(i)

                    # increment level time
                    self.level_time += 1

                    # increase agents time TODO: add for time distortion
                    for i in range(self.number_of_players):
                        self.players[i].add_to_current_time()

                # all cards are played or are out
                else:
                    level_reward = self.level_up()
                    num_of_out += len(self.level_cards)

                # increase game time
                self.game_time += 1

            # end of game

            # winning if there is at least one life
            if self.number_of_lives > 0:
                self.number_of_wins += 1
                sample_wins += 1

            # losing if there is no remaining life
            else:
                self.number_of_losses += 1

            if game_i % sample_rate == (sample_rate - 2):
                # make all exploration rates 0 TODO: for exp0 sampling
                for i in range(self.number_of_players):
                    self.players[i].set_exploration_rate(0)

            # check game counter is equal to sample rate
            elif game_i % sample_rate == (sample_rate - 1):
                list_of_sample_wins.append(sample_wins)  # append number of wins in sample range
                sample_wins = 0  # reset sample wins counter

                # make all exploration rates 0 TODO: for exp0 sampling
                for i in range(self.number_of_players):
                    self.players[i].set_exploration_rate(0.5)
                list_of_exp0_samples.append(int(game_result))  # TODO: exp0 sampling

            # check the starting of the last games with zero exploitation
            if game_i == (number_of_games-last_games_with_zero_exploitation-1):
                for j in range(self.number_of_players):
                    self.players[j].set_exploration_rate(0)  # set exploration rate equal to zero for all agents
                    f.write("\t~player " + str(j) + "table size: "+str(len(self.players[j].get_table()))+"\n")

            # check the game counter during the last games with zero exploitation
            if game_i >= (number_of_games-last_games_with_zero_exploitation):

                # winning if there is at least one life (with zero exploration rate)
                if self.number_of_lives > 0:
                    learning_wins += 1

            # restart game
            self.restart_game()

        # update number of out card
        num_of_out -= (num_of_wrong + num_of_correct)

        f.write("\tnumber_of_wins: "+str(self.number_of_wins) + "\n")
        f.write("\tnumber_of_losses: "+str(self.number_of_losses) + "\n")
        f.write("\tnumber_of_learning_wins: "+str(learning_wins) + "\n")
        f.write("\tnum_of_correct: "+str(num_of_correct) + "\n")
        f.write("\tnum_of_wrong: "+str(num_of_wrong) + "\n")
        f.write("\tnum_of_out: "+str(num_of_out) + "\n\n")
        print("\tnumber_of_wins: "+str(self.number_of_wins) + "\n")
        print("\tnumber_of_losses: "+str(self.number_of_losses) + "\n")
        print("\tnumber_of_learning_wins: "+str(learning_wins) + "\n")
        print("\tnum_of_correct: "+str(num_of_correct) + "\n")
        print("\tnum_of_wrong: "+str(num_of_wrong) + "\n")
        print("\tnum_of_out: "+str(num_of_out) + "\n\n")
        # TODO: list_of_exp0_samples added for exp0 sampling
        return [self.number_of_wins, self.number_of_losses, learning_wins, list_of_sample_wins, list_of_exp0_samples,
                [num_of_correct, num_of_wrong, num_of_out]]

    def restart_game(self):

        # reset parameters & distribute cards
        self.deck = list(range(1, self.deck_size + 1))
        self.game_time = 1
        self.level_time = 1
        self.current_card = 0
        self.current_level = 1
        self.number_of_lives = 1  # TODO: self.number_of_players
        self.number_of_throwing_stars = 1
        self.level_cards = []
        self.players_cards = []
        self.players_main_actions = []
        self.players_secondary_actions = []
        self.players_throwing_star_flag = []
        self.players_out_index = []
        for i in range(self.number_of_players):
            self.players_throwing_star_flag.append(False)
            self.players[i].clear_cards()
            self.players_cards.append([])
            self.players_main_actions.append([])
            self.players_secondary_actions.append([])
            self.players[i].reset_current_time()  # TODO: add for time distortion

        # distribute cards and make game ready
        self.distribute_cards()
