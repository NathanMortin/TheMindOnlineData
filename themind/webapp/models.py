from django.db import models


class Game(models.Model):
    game_id = models.AutoField(db_column='game_id', primary_key=True)
    number_of_players = models.PositiveSmallIntegerField(db_column='number_of_players', blank=True, null=True)
    deck_size = models.PositiveSmallIntegerField(db_column='deck_size', blank=True, null=True)
    number_of_levels = models.PositiveSmallIntegerField(db_column='number_of_levels', blank=True, null=True)
    deck = models.TextField(db_column='deck', blank=True, null=True)
    game_time = models.PositiveIntegerField(db_column='game_time', blank=True, null=True)
    level_time = models.PositiveIntegerField(db_column='level_time', blank=True, null=True)
    current_card = models.PositiveSmallIntegerField(db_column='current_card', blank=True, null=True)
    current_level = models.PositiveSmallIntegerField(db_column='current_level', blank=True, null=True)
    number_of_lives = models.PositiveSmallIntegerField(db_column='number_of_lives', blank=True, null=True)
    number_of_throwing_stars = models.PositiveSmallIntegerField(db_column='number_of_throwing_stars', blank=True, null=True)
    level_cards = models.TextField(db_column='level_cards', blank=True, null=True)
    players_cards = models.TextField(db_column='players_cards', blank=True, null=True)
    players_main_actions = models.TextField(db_column='players_main_actions', blank=True, null=True)
    players_secondary_actions = models.TextField(db_column='players_secondary_actions', blank=True, null=True)
    players_throwing_star_flag = models.TextField(db_column='players_throwing_star_flag', blank=True, null=True)
    players_out_index = models.TextField(db_column='players_out_index', blank=True, null=True)

    class Meta:
        db_table = 'game'


class AgentTable(models.Model):
    agent_table_id = models.AutoField(db_column='agent_table_id', primary_key=True)

    class Meta:
        db_table = 'agent_table'


class State(models.Model):
    state_id = models.AutoField(db_column='state_id', primary_key=True)
    current_card = models.PositiveSmallIntegerField(db_column='current_card', blank=True, null=True)
    level_time = models.PositiveIntegerField(db_column='level_time', blank=True, null=True)
    players_throwing_star_flag = models.TextField(db_column='players_throwing_star_flag', blank=True, null=True)
    number_of_other_players_cards = models.TextField(db_column='number_of_other_players_cards', blank=True, null=True)
    number_of_agent_card = models.PositiveSmallIntegerField(db_column='number_of_agent_card', blank=True, null=True)
    minimum_agent_card = models.PositiveSmallIntegerField(db_column='minimum_agent_card', blank=True, null=True)
    dist = models.PositiveSmallIntegerField(db_column='dist', blank=True, null=True)
    point = models.FloatField(db_column='point', blank=True, null=True)

    class Meta:
        db_table = 'state'


class Agent(models.Model):
    agent_id = models.AutoField(db_column='agent_id', primary_key=True)
    game_id = models.ForeignKey(Game, on_delete=models.DO_NOTHING, db_column='fk_game_id', blank=True,
                                null=True)
    cards = models.TextField(db_column='cards', blank=True, null=True)
    table = models.ForeignKey(AgentTable, on_delete=models.DO_NOTHING, db_column='fk_agent_table_id', blank=True,
                              null=True)
    current_state = models.ForeignKey(State, on_delete=models.DO_NOTHING, db_column='fk_current_state_id',
                                      related_name='fk_current_state_id', blank=True, null=True)
    next_state = models.ForeignKey(State, on_delete=models.DO_NOTHING, db_column='fk_next_state_id',
                                   related_name='fk_next_state_id', blank=True, null=True)
    played = models.BooleanField(db_column='played', blank=True, null=True)
    current_reward = models.FloatField(db_column='current_reward', blank=True, null=True)
    cumulative_reward = models.FloatField(db_column='cumulative_reward', blank=True, null=True)
    current_time = models.PositiveIntegerField(db_column='current_time', blank=True, null=True)
    clock_rate = models.PositiveSmallIntegerField(db_column='clock_rate', blank=True, null=True)
    clock_mu = models.PositiveSmallIntegerField(db_column='clock_mu', blank=True, null=True)
    clock_p_i = models.FloatField(db_column='clock_p_i', blank=True, null=True)
    exploration_rate = models.FloatField(db_column='exploration_rate', blank=True, null=True)
    decreasing_exp_rate = models.FloatField(db_column='decreasing_exp_rate', blank=True, null=True)

    class Meta:
        db_table = 'agent'


class Node(models.Model):
    node_id = models.AutoField(db_column='node_id', primary_key=True)
    agent_table = models.ForeignKey(AgentTable, on_delete=models.CASCADE, db_column='fk_agent_table_id')
    state = models.OneToOneField(State, on_delete=models.CASCADE, db_column='fk_state_id')
    act_reward_play = models.FloatField(db_column='act_reward_play', blank=True, null=True)
    act_reward_wait = models.FloatField(db_column='act_reward_wait', blank=True, null=True)

    class Meta:
        db_table = 'node'


