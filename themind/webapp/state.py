import math


class State:

    def __init__(self, current_card, deck_size, level_time, players_throwing_star_flag,
                 number_of_other_players_cards, number_of_agent_card, minimum_agent_card):
        self.current_card = current_card
        self.level_time = level_time
        self.players_throwing_star_flag = players_throwing_star_flag
        self.number_of_other_players_cards = number_of_other_players_cards
        self.number_of_agent_card = number_of_agent_card
        self.minimum_agent_card = minimum_agent_card

    def __eq__(self, other):
        if isinstance(other, State):
            return self.current_card == other.current_card and self.level_time == other.level_time and \
                   self.players_throwing_star_flag == other.players_throwing_star_flag and \
                   self.number_of_other_players_cards == other.number_of_other_players_cards and \
                   self.number_of_agent_card == other.number_of_agent_card and \
                   self.minimum_agent_card == other.minimum_agent_card

    def print(self):
        return "current_card: "+str(self.current_card) + ", level_time: " + str(self.level_time) +\
               ", players_throwing_star_flag: " + str(self.players_throwing_star_flag) +\
               ", number_of_other_players_cards: " + str(self.number_of_other_players_cards) +\
               ", number_of_agent_card:" + str(self.number_of_agent_card) + ", minimum_agent_card:" +\
               str(self.minimum_agent_card)


class State2:

    def __init__(self, current_card, deck_size, level_time, players_throwing_star_flag,
                 number_of_other_players_cards, number_of_agent_card, minimum_agent_card):
        self.level_time = level_time
        remaining_range = deck_size - current_card
        number_of_points_in_range = number_of_agent_card + sum(number_of_other_players_cards)
        range_value = remaining_range / (number_of_points_in_range + 1)
        if number_of_points_in_range == 0:
            self.point = 0
            self.dist = 0
        else:
            self.point = math.ceil((minimum_agent_card - current_card) / range_value)
            self.dist = (current_card + (self.point * range_value)) - minimum_agent_card

    def __eq__(self, other):
        if isinstance(other, State2):
            return self.level_time == other.level_time and \
                self.dist == other.dist and \
                self.point == other.point

    def print(self):
        return "level_time: " + str(self.level_time) +\
               ", point: " + str(self.point) +\
               ", dist: " + str(self.dist)


class State3:

    def __init__(self, current_card, deck_size, level_time, players_throwing_star_flag,
                 number_of_other_players_cards, number_of_agent_card, minimum_agent_card):
        self.level_time = level_time
        self.minimum_agent_card = minimum_agent_card

    def __eq__(self, other):
        if isinstance(other, State3):
            return self.level_time == other.level_time and \
                   self.minimum_agent_card == other.minimum_agent_card

    def print(self):
        return "level_time: " + str(self.level_time) +\
               ", minimum_agent_card_range:" +\
               str(self.minimum_agent_card)


class State4:

    def __init__(self, current_card, deck_size, level_time, players_throwing_star_flag,
                 number_of_other_players_cards, number_of_agent_card, minimum_agent_card):
        self.level_time = level_time
        self.minimum_agent_card = minimum_agent_card
        self.current_card = current_card

    def __eq__(self, other):
        if isinstance(other, State4):
            return self.level_time == other.level_time and \
                   self.minimum_agent_card == other.minimum_agent_card and \
                   self.current_card == other.current_card

    def print(self):
        return "level_time: " + str(self.level_time) +\
               ", minimum_agent_card_range:" +\
               str(self.minimum_agent_card) +\
               ", current_card:" + \
               str(self.current_card)


