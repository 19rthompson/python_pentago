#!/usr/bin/env python3

# import rock_paper_scissors.rock_paper_scissorsv0 as rps
import pentago_game.pentago_game as pen
from pentago_game.env.PentagoModel import Model

BLANK = 0
BLACK = 1
WHITE = 2

RIGHT=0
LEFT=1

I = 0
II = 1
III = 2
IV = 3

CCWISE = 0
CWISE = 1

def main():
    env = pen.env(render_mode="ansi")
    env.reset()

    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()

        if termination or truncation:
            action = None
        else:
            loop=True
            while loop:
                action = random_agent(env,agent)
                if observation[action[0]]==BLANK:
                    loop = False
        env.step(action)
    print(reward)    
    env.close()

def random_agent(env,agent):
    return env.action_space(agent).sample()

if __name__ == "__main__":
    main()