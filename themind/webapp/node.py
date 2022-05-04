

class Node:

    def __init__(self, state):
        self.state = state
        self.act_reward = [0.0, 0.0]

    def set_state(self, state):
        self.state = state

    def set_act_reward(self, action, reward):
        self.act_reward[action] = reward

    def get_state(self):
        return self.state

    def get_act_reward(self):
        return self.act_reward

