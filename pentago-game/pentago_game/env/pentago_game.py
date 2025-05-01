#!/usr/bin/env python3
from pentago_game.env.PentagoModel import Model
import functools

import os
import gymnasium as gym
import pygame
import numpy as np
from gymnasium.spaces import Discrete, MultiDiscrete, Box


from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers

BLANK = 0
BLACK = 1
WHITE = 2

I = 0
II = 1
III = 2
IV = 3

CCWISE = 0
CWISE = 1

NUM_ITERS = 18


def get_image(path, width, height):
    from os import path as os_path
    import pygame

    cwd = os_path.dirname(__file__)
    image = pygame.image.load(cwd + "/" + path)
    # Scale the image
    image = pygame.transform.scale(image, (width, height))
    sfc = pygame.Surface(image.get_size(), flags=pygame.SRCALPHA)
    sfc.blit(image, (0, 0))
    return sfc


def env(render_mode=None):
    """
    The env function often wraps the environment in wrappers by default.
    You can find full documentation for these methods
    elsewhere in the developer documentation.
    """
    internal_render_mode = render_mode# if render_mode != "ansi" else "human"
    env = raw_env(render_mode=internal_render_mode)
    # This wrapper is only for environments which print results to the terminal
    #if render_mode == "ansi":
      #  env = wrappers.CaptureStdoutWrapper(env)
    # this wrapper helps error handling for discrete action spaces
    env = wrappers.AssertOutOfBoundsWrapper(env)
    # Provides a wide vareity of helpful user errors
    # Strongly recommended
    env = wrappers.OrderEnforcingWrapper(env)
    return env


class raw_env(AECEnv):
    """
    The metadata holds environment constants. From gymnasium, we inherit the "render_modes",
    metadata which specifies which modes can be put into the render() method.
    At least human mode should be supported.
    The "name" metadata allows the environment to be pretty printed.
    """

    metadata = {"render_modes": ["human","ansi"], "name": "Pentago"}

    def __init__(self, render_mode=None):
        
        """
        The init method takes in environment arguments and
         should define the following attributes:
        - possible_agents
        - render_mode

        Note: as of v1.18.1, the action_spaces and observation_spaces attributes are deprecated.
        Spaces should be defined in the action_space() and observation_space() methods.
        If these methods are not overridden, spaces will be inferred from self.observation_spaces/action_spaces, raising a warning.

        These attributes should not be changed after initialization.
        """
        self.possible_agents = ["player_" + str(r) for r in range(2)]

        # optional: a mapping between agent name and ID
        self.agent_name_mapping = dict(
            zip(self.possible_agents, list(range(len(self.possible_agents))))
        )

        # optional: we can define the observation and action spaces here as attributes to be used in their corresponding methods
        self._action_spaces = {agent: MultiDiscrete([6,6,4,2]) for agent in self.possible_agents}
        self._observation_spaces = {
            agent: MultiDiscrete([[3]*6]*6) for agent in self.possible_agents
        }
        self.render_mode = render_mode
        
        self.model = Model()
        

    # Observation space should be defined here.
    # lru_cache allows observation and action spaces to be memoized, reducing clock cycles required to get each agent's space.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)

    def observation_space(self, agent):
        # gymnasium spaces are defined and documented here: https://gymnasium.farama.org/api/spaces/
        return MultiDiscrete([[3]*6]*6)

    # Action space should be defined here.
    # If your spaces change over time, remove this line (disable caching).
    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        return MultiDiscrete([6,6,4,2])

    def render(self):
        
        if self.render_mode == "ansi":
            self.model.printBoard()
            return
        if self.render_mode != "human":
            return
        return
        """
        if not hasattr(self, 'screen'):
            pygame.init()
            self.screen = pygame.display.set_mode((600, 400))
            self.font = pygame.font.Font(None, 36)
            self.clock = pygame.time.Clock()

            # Load images for each move
            self.images = {
                ROCK: get_image(os.path.join("img", "Rock.png"), 100, 100),  # Example size
                PAPER: get_image(os.path.join("img", "Paper.png"), 100, 100),
                SCISSORS: get_image(os.path.join("img", "Scissors.png"), 100, 100),
                NONE: None  # Placeholder for no move
            }


        self.screen.fill((255, 255, 255))
        
        if len(self.agents) == 2:
            # Display images for Agent 1 and Agent 2 moves
            agent1_move = self.state[self.agents[0]]
            agent2_move = self.state[self.agents[1]]
            
            if self.images[agent1_move]:
                self.screen.blit(self.images[agent1_move], (150, 150))  # Agent 1 image position
            if self.images[agent2_move]:
                self.screen.blit(self.images[agent2_move], (350, 150))  # Agent 2 image position

            # Display the move result text
            result_text = f"Agent1: {MOVES[agent1_move]} vs Agent2: {MOVES[agent2_move]}"
        else:
            result_text = "Game Over"

        text = self.font.render(result_text, True, (0, 0, 0))
        self.screen.blit(text, (50, 50))

        pygame.display.flip()
        self.clock.tick(60)"""


    def close(self):
        if self.render_mode == "human" and hasattr(self, 'screen'):
            pygame.quit()
            del self.screen


    def observe(self, agent):
        """
        Observe should return the observation of the specified agent. This function
        should return a sane observation (though not necessarily the most up to date possible)
        at any time after reset() is called.
        """
        # observation of one agent is the previous state of the other
        return np.array(self.observations[agent])

    def close(self):
        """
        Close should release any graphical displays, subprocesses, network connections
        or any other environment data which should not be kept around after the
        user is no longer using the environment.
        """
        pass

    def reset(self, seed=None, options=None):
        """
        Reset needs to initialize the following attributes
        - agents
        - rewards
        - _cumulative_rewards
        - terminations
        - truncations
        - infos
        - agent_selection
        And must set up the environment so that render(), step(), and observe()
        can be called without issues.
        Here it sets up the state dictionary which is used by step() and the observations dictionary which is used by step() and observe()
        """
        self.agents = self.possible_agents[:]
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        self.model.reset()
        self.observations = {agent: self.model.getBoard() for agent in self.agents}
        self.num_moves = 0
        """
        Our agent_selector utility allows easy cyclic stepping through the agents list.
        """
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()

    def step(self, action):
        """
        step(action) takes in an action for the current agent (specified by
        agent_selection) and needs to update
        - rewards
        - _cumulative_rewards (accumulating the rewards)
        - terminations
        - truncations
        - infos
        - agent_selection (to the next agent)
        And any internal state used by observe() or render()
        """
        if (
            self.terminations[self.agent_selection]
            or self.truncations[self.agent_selection]
        ):
            # handles stepping an agent which is already dead
            # accepts a None action for the one agent, and moves the agent_selection to
            # the next dead agent,  or if there are no more dead agents, to the next live agent
            self._was_dead_step(action)
            return

        agent = self.agent_selection

        # the agent which stepped last had its _cumulative_rewards accounted for
        # (because it was returned by last()), so the _cumulative_rewards for this
        # agent should start again at 0
        self._cumulative_rewards[agent] = 0

        #update model based on action"
        print(self.agent_selection)
        if self.agent_selection == self.possible_agents[0]:
            marble_color = BLACK
        elif self.agent_selection == self.possible_agents[1]:
            marble_color = WHITE
        self.model.placeMarble(action[0],action[1], marble_color)
        
        if action[1] == CCWISE:
            self.model.rotateQuadrantLeft(action[3])
        elif action[2] == CWISE:
            self.model.rotateQuadrantRight(action[3])

        # collect reward if it is the last agent to act
        if self._agent_selector.is_last():
            # rewards for all agents are placed in the .rewards dictionary
            if self.model.checkVictory() == BLACK:
                self.rewards[self.agents[0]], self.rewards[self.agents[1]] = (1,-1)
                self.terminations = {agent: True for agent in self.agents}
                print("terminated for black")
            elif self.model.checkVictory() == WHITE:
                self.rewards[self.agents[0]], self.rewards[self.agents[1]] = (-1,1)
                self.terminations = {agent: True for agent in self.agents}
                print("terminated for white")
            elif self.model.checkVictory() == BLANK:
                self.rewards[self.agents[0]], self.rewards[self.agents[1]] = (0,0) 

            self.num_moves += 1
            # The truncations dictionary must be updated for all players.
            self.truncations = {
                agent: self.num_moves >= NUM_ITERS for agent in self.agents
            }

            # observe the current state
            for i in self.agents:
                self.observations[i] = self.model.getBoard()
        else:
            # necessary so that observe() returns a reasonable observation at all times.
            # self.state[self.agents[1 - self.agent_name_mapping[agent]]] = NONE

            # no rewards are allocated until both players give an action
            self._clear_rewards()

        # selects the next agent.
        self.agent_selection = self._agent_selector.next()
        # Adds .rewards to ._cumulative_rewards
        self._accumulate_rewards()

        if self.render_mode == "human":
            self.render()
        elif self.render_mode == "ansi":
            self.model.printBoard()
