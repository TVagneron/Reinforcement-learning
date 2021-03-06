"""
Classic cart-pole system implemented by Rich Sutton et al.
Copied from https://webdocs.cs.ualberta.ca/~sutton/book/code/pole.c
"""

import logging
import math
import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
import time


logger = logging.getLogger(__name__)

class TestThomasDeter(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    def __init__(self):
        self.tau = 0.02  # seconds between state updates

	# Trees location
        self.treeslocations = [3.0, 8.0];

	# Initilization of counters	
	self.count = 0     # ending of the process
	self.currentFireIndex = 0   # tictac
	self.timecount = 0 # 0 -> 1 -> ... -> 50 -> 0
	self.firetrees = 0 # number of trees on fire

	# Actions: 0: fire 1 / 1: fire 2 / 2: nothing
        self.action_space = spaces.Discrete(3)

	# TODO necessary?
	self.worldWidth = 4.8
	self.worldWidth2 = 2*24*math.pi/360
        
	# Observation space definition (TODO redefine with actual observation space)
        high_value = [1]
        low_value = [0]
	#self.observation_space = spaces.Box(-high, high) # TODO TODO TODO WARNING: between -0 and 0!!! 
	upper_space = np.array(high_value*len(self.treeslocations))
	lower_space = np.array(low_value*len(self.treeslocations))
	self.observation_space = spaces.Box(lower_space, upper_space)
# TODO
# self.observation_space = spaces.Discrete(2)
# loop from 1 to nbtree
# self.observation_space = Tuple(spaces.Discrete(2), self.observation_space )

	# seed, init values, viewer reset
        self._seed()
        self.reset()
        self.viewer = None

        # Just need to initialize the relevant attributes
        self._configure()

    def _configure(self, display=None):
        self.display = display

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    # =======================================================================================================================================================
    # ============ STEP =====================================================================================================================================
    # =======================================================================================================================================================
    def _step(self, action):

	screen_width = 600
        screen_height = 400
        world_width = self.worldWidth
        scale = screen_width/world_width

        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        state = self.state

	# parse state (fire states)
        treesStatesList = []
	for i in range(len(self.treeslocations)):
           treesStatesList.append(state[i])
	treesStates = ()

	# fire starter	
        if (self.timecount > 0):
        	self.timecount += 1        
        if (self.timecount == 50):
        	self.timecount = 0
        	
	# ONLY ONE FIRE AT EACH STEP
        if (treesStatesList[self.currentFireIndex]==0) and (self.timecount == 0) and (self.firetrees == 0):
            	treesStatesList[self.currentFireIndex] = 1 # ON FIRE!!
                self.firetrees = 1
                self.currentFireIndex += 1
                if (self.currentFireIndex == len(self.treeslocations)):
                	self.currentFireIndex = 0

        for i in range(len(self.treeslocations)):
        	if (treesStatesList[i] == 1 and action == i):
        		treesStatesList[i] = 0 	# EXTIGUISHED BY ROBOT
        		reward = 1.0 		# REWARD++
        		self.firetrees = 0
        		self.timecount += 1
        	else :
        		reward = 0.0 		# NO REWARD
	for i in range(len(self.treeslocations)):
               	treesStates += (treesStatesList[i],)
	self.state = treesStates 
	
	self.count += 1
	done = False

	# END OF THE EPISODE
	if (self.count == 20000):
		done = True
        #time.sleep(0.5)
	return np.array(self.state), reward, done, {}

    def _reset(self):
	treesStates = ()
        for i in range(len(self.treeslocations)):
	     treesStates += (0,)
        self.state = treesStates
	self.currentFireIndex = 0
	self.count = 0
	self.timecount = 0
	self.firetrees =0
        return np.array(self.state)


    # =======================================================================================================================================================
    # ============ VIEWER ===================================================================================================================================
    # =======================================================================================================================================================
    def _render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        screen_width = 600
        screen_height = 400

        world_width = self.worldWidth
        scale = screen_width/world_width
        carty = 100 # y-position
	
        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height, display=self.display)
            self.truc = []
            cpt = 0
		# trees view definition
            for tree in self.treeslocations:
                self.truc.append(rendering.FilledPolygon([(tree*screen_width/10-10,carty-10), (tree*screen_width/10+10,carty-10), (tree*screen_width/10+10,carty+10), (tree*screen_width/10-10,carty+10)]))
                self.truc[cpt].set_color(0,1,0)
                self.viewer.add_geom(self.truc[cpt])
                cpt+=1

        x = self.state
	# tree color management
        for i in range(len(self.treeslocations)):
            if(x[i]==1):
                self.truc[i].set_color(1,0,0)
            else:
		self.truc[i].set_color(0,1,0)
        return self.viewer.render(return_rgb_array = mode=='rgb_array')
