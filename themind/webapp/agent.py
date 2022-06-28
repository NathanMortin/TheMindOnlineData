import random
from webapp.state import State, State2, State3, State4
from webapp.node import Node
import numpy as np
import math

# random.seed(1)


class Agent:
    def __init__(self, player_id):
        self.player_id = player_id
        self.cards = []
        self.table = []
        self.current_state = None
        self.next_state = None
        self.played = False
        self.current_reward = 0
        self.main_action = None
        self.gamma = 0.99
        self.alpha = 0.01
        self.last_exploration_rate = 0.5
        self.last_table = []
        self.step_cost = -0.01
        self.cumulative_reward = 0

        self.current_time = 0
        self.clock_rate = 0
        self.clock_mu = 1
        self.clock_p_i = 1
        self.exploration_rate = 0.5
        self.decreasing_exp_rate = 0

    def set_decreasing_exp_rate(self, r):
        self.decreasing_exp_rate = r

    def get_decreasing_exp_rate(self):
        return self.decreasing_exp_rate

    def set_clock_p_i(self, pi):
        self.clock_p_i = pi

    def get_clock_p_i(self):
        return self.clock_p_i

    def add_to_cards(self, card):
        self.cards.append(card)
        self.cards.sort()
        return self.cards

    def clear_cards(self):
        self.cards = []

    def set_exploration_rate(self, e):
        self.last_exploration_rate = self.exploration_rate
        self.exploration_rate = e

    def set_table(self, t):
        self.last_table = self.table
        self.table = t

    def get_exploration_rate(self):
        return self.exploration_rate

    def get_last_exploration_rate(self):
        return self.last_exploration_rate

    def get_last_table(self):
        return self.last_table

    def get_cards(self):
        return self.cards

    def get_minimum_card(self):
        if len(self.cards) > 0:
            minimum_card = self.cards[0]
        else:
            minimum_card = -1
        return minimum_card

    def get_current_state(self):
        return self.current_state

    def play_card(self):
        min_card = self.get_minimum_card()
        self.played = True
        return min_card

    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        return False

    def wait(self):
        self.played = True

    def get_played(self):
        return self.played

    def set_current_reward(self, reward):
        self.current_reward = reward
        self.cumulative_reward += reward

    def set_current_action(self, action):
        self.main_action = action

    def get_next_state(self):
        return self.next_state

    @staticmethod
    def define_state(setting_state, current_card, deck_size, level_time, players_throwing_star_flag,
                     number_of_other_players_cards, number_of_agent_card, agent_minimum_card):
        if setting_state == 1:
            defined_state = State(current_card, deck_size, level_time, players_throwing_star_flag,
                                  number_of_other_players_cards, number_of_agent_card, agent_minimum_card)
        elif setting_state == 2:
            defined_state = State2(current_card, deck_size, level_time, players_throwing_star_flag,
                                   number_of_other_players_cards, number_of_agent_card, agent_minimum_card)
        elif setting_state == 3:
            defined_state = State3(current_card, deck_size, level_time, players_throwing_star_flag,
                                   number_of_other_players_cards, number_of_agent_card, agent_minimum_card)
        else:
            defined_state = State4(current_card, deck_size, level_time, players_throwing_star_flag,
                                   number_of_other_players_cards, number_of_agent_card, agent_minimum_card)
        return defined_state

    def set_next_state(self, current_card, deck_size, level_time, players_throwing_star_flag,
                       number_of_other_players_cards, setting_state):
        number_of_agent_card = len(self.cards)
        next_state = self.define_state(setting_state, current_card, deck_size, level_time, players_throwing_star_flag,
                                       number_of_other_players_cards, number_of_agent_card, self.get_minimum_card())
        self.next_state = next_state

    def make_decision(self, current_card, deck_size, level_time, players_throwing_star_flag,
                      number_of_other_players_cards, players_main_actions, players_secondary_actions, setting_state):
        number_of_agent_card = len(self.cards)
        current_state = self.define_state(setting_state, current_card, deck_size, level_time,
                                          players_throwing_star_flag, number_of_other_players_cards,
                                          number_of_agent_card, self.get_minimum_card())
        self.current_state = current_state

        rand = random.uniform(0, 1)
        if rand < self.exploration_rate:
            main_action = random.choice(players_main_actions)
        else:
            act = self.get_max_reward_index(self.current_state)
            if act in players_main_actions:
                main_action = act
            else:
                main_action = random.choice(players_main_actions)  # need attention

        secondary_action = random.choice(players_secondary_actions)

        self.main_action = main_action
        self.played = False
        self.current_reward = 0
        return [main_action, secondary_action]

    @staticmethod
    def get_reward(result):
        if result:
            return 1
        else:
            return -1

    def get_max_reward(self, state):
        for node in self.table:
            if node.get_state() == state:
                return max(node.get_act_reward())
        return 0.0

    def get_max_reward_index(self, state):
        for node in self.table:
            if node.get_state() == state:
                return node.get_act_reward().index(max(node.get_act_reward()))
        return random.randint(0, 1)

    def update_table(self):
        in_list = False
        for i in range(len(self.table)):
            node = self.table[i]
            if node.state == self.current_state:
                reward = self.current_reward + (self.gamma * self.get_max_reward(self.next_state)) + self.step_cost
                self.table[i].act_reward[self.main_action] = \
                    (reward * self.alpha) + (self.table[i].act_reward[self.main_action] * (1-self.alpha))
                in_list = True
                break
        if not in_list:
            node = Node(self.current_state)
            reward = self.current_reward + (self.gamma * self.get_max_reward(self.next_state)) + self.step_cost
            node.set_act_reward(self.main_action, (reward * self.alpha))
            self.table.append(node)

    def get_table(self):
        return self.table

    def set_clock_rate(self, rate):
        self.clock_rate = rate

    def add_to_current_time(self):
        self.current_time += self.clock_rate

    def add_to_current_time1(self):
        noise = 0.6  # a fixed noise rate
        rand = random.uniform(0, 1)
        if rand < noise:
            s = np.random.normal(self.clock_mu, 2, 1)
            # instead of adding 1 to the current time, a random integer number will be added
            #  to the current time which is randomly selected with a normal distribution using mu and sigma
            self.current_time += abs(math.ceil(s[0]))
        else:
            self.current_time += self.clock_rate

    def add_to_current_time2(self):
        rand = np.random.binomial(1, self.get_clock_p_i())
        if rand == 1:
            self.current_time += self.clock_rate + 1
        else:
            self.current_time += self.clock_rate

    def add_to_current_time3(self, n):
        if self.get_clock_p_i() < 0.33:
            self.current_time = n + 1  # f(n) = n agent counting time exactly like the steps
        elif self.get_clock_p_i() < 0.66:
            c = 2
            self.current_time = math.ceil(c * n * math.log10(n) + 1)
            # f(n) = c * n log(n) + 1 agent counting time faster, with an increasing speed-up as time passes
        else:
            b = 0.3
            self.current_time = math.ceil(b * n / math.log10(n + 1))
            # f(n) = b * n / log(n + 1) agent counting time faster, with an increasing speed-up as time passes

    def add_to_current_time4(self, n):
        if self.get_clock_p_i() < 0.33:
            self.current_time = n + 1  # f(n) = n agent counting time exactly like the steps
        elif self.get_clock_p_i() < 0.66:
            c = 4
            self.current_time = math.ceil(c * n * math.log10(n) + 1)
            # f(n) = c * n log(n) + 1 agent counting time faster, with an increasing speed-up as time passes
        else:
            b = 0.4
            self.current_time = math.ceil(b * n / math.log10(200 * n))
            # f(n) = b * n / log(200 * n) agent counting time faster, with an increasing speed-up as time passes
        print(self.player_id, ": ", self.current_time)

    def reset_current_time(self):
        self.current_time = 0

    def get_next_time(self):
        return self.current_time + self.clock_rate

    def get_current_time(self):
        return self.current_time

    def set_clock_mu(self, mu):
        self.clock_mu = mu



















