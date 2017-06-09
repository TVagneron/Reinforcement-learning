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

class TestThomasReduit(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    def __init__(self):
        self.tau = 0.02  # seconds between state updates
	#Initial datas
	self.vit = 1.0
        self.treeslocations = [3.0, 8.0];
	#Initilisation of ending counters
	self.count = 0
	self.counter = 0
	self.currentFireIndex = 0
        # Angle at which to fail the episode
        self.x_threshold = 1.0

        # Angle limit set to 2 * theta_threshold_radians so failing observation is still within bounds$
        high_value = [1]
        low_value = [0]
	#self.observation_space = spaces.Box(-high, high) # TODO TODO TODO WARNING: between -0 and 0!!! 
	upper_space = np.array([self.x_threshold]+high_value*len(self.treeslocations))
	lower_space = np.array([-self.x_threshold]+low_value*len(self.treeslocations))
	self.observation_space = spaces.Box(lower_space, upper_space)
	#print(self.observation_space)

        self.action_space = spaces.Discrete(3)


        self._seed()
        self.reset()
        self.viewer = None

        self.steps_beyond_done = None

        # Just need to initialize the relevant attributes
        self._configure()

    def _configure(self, display=None):
        self.display = display

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _step(self, action):
	screen_width = 600
        screen_height = 400
        reward = 0.0

        world_width = self.x_threshold*2
        scale = screen_width/world_width

        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        state = self.state
        #print("bla")
        #print(state)
        #x, x_dot, theta, theta_dot, v1, v2, v3, v4 = state # TODO TODO TODO access data from a tuple
        x = state[0]
        treesStatesList = []
        for i in range(len(self.treeslocations)):
            treesStatesList.append(state[1+i])
	treesStates = ()
        #print(treesStates)
        
        # fire starter	
        if (self.timecount > 0):
        	self.timecount += 1        
        if (self.timecount == 50):
        	self.timecount = 0
	
	#state of trees
	if ( (treesStatesList[self.currentFireIndex]==0) and (self.timecount == 0) and (self.firetrees == 0)):
            	treesStatesList[self.currentFireIndex] = 1 # ON FIRE!!
                self.firetrees = 1
                self.currentFireIndex += 1
                if (self.currentFireIndex == len(self.treeslocations)):
                	self.currentFireIndex = 0
       
	#movement
	vitesse = 0.0
	if ( (action == 1) and ( x < self.x_threshold-2*self.tau*self.vit) ):
		vitesse = self.vit*0.0
	elif ( (action == 0) and (x > -self.x_threshold + 2*self.tau*self.vit) ):
		vitesse = -self.vit
	#vitesse = 1
        x  = x + self.tau * vitesse
	#action of extinguishing the fire
	for i in range( len(self.treeslocations) ):
		if ( ((self.treeslocations[i]-5)/5*self.x_threshold-0.05 < x) and (x < (self.treeslocations[i]-5)/5*self.x_threshold+0.05) and (self.state[1+i]==1) and (action == 2) ):
			treesStatesList[i] = 0
			reward = 1.0
			self.timecount += 1
			self.firetrees = 0
			
	for i in range(len(self.treeslocations)):
               	treesStates += (treesStatesList[i],)

        #print(treesStates)
	#print(self.state[0]*scale/world_width+0.5)
        self.state = (x,) + treesStates 


        #time.sleep(0.5)
	self.count += 1
	done = False

	#ending conditions
	if (self.count == 20000):
		done = True
        #print(self.state)
        print(self.state)
        return np.array(self.state), reward, done, {}

    def _reset(self):
        treesStates = ()
        for i in range(len(self.treeslocations)):
	     treesStates += (0,)
        self.state = np.concatenate((self.np_random.uniform(low=-0.05, high=0.05, size=(1,)),treesStates), axis = 0)
	self.currentFireIndex = 0
	self.count = 0
	self.timecount = 0
	self.firetrees = 0
	#print(self.state)
        return np.array(self.state)
    def _render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return

        screen_width = 600
        screen_height = 400

        world_width = self.x_threshold*2
        scale = screen_width/world_width
        carty = 100 # TOP OF CART
        polewidth = 10.0
        polelen = scale * 1.0
        cartwidth = 50.0
        cartheight = 30.0
	
        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height, display=self.display)
            l,r,t,b = -cartwidth/2, cartwidth/2, cartheight/2, -cartheight/2

	    self.chose = []
            cart = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
	    self.chose.append(cart)
            self.carttrans = rendering.Transform()
            cart.add_attr(self.carttrans)
            self.viewer.add_geom(self.chose[0])
            self.track = rendering.Line((0,carty), (screen_width,carty))
            self.track.set_color(0,0,0)
            self.viewer.add_geom(self.track)
            self.truc = []
            cpt = 0
            for tree in self.treeslocations:
                self.truc.append(rendering.FilledPolygon([(tree*screen_width/10-10,carty-10), (tree*screen_width/10+10,carty-10), (tree*screen_width/10+10,carty+10), (tree*screen_width/10-10,carty+10)]))
                self.truc[cpt].set_color(0,1,0)
                #self.treeColor = rendering.Transform()
                #truc.add_attr(self.treeColor)
                self.viewer.add_geom(self.truc[cpt])
                cpt+=1
                
                

        pos = self.state
        cartx = pos[0]*scale+screen_width/2.0 # MIDDLE OF CART
        self.carttrans.set_translation(cartx, carty)
        for i in range(len(self.treeslocations)):
            if(pos[i+1]==1):
                self.truc[i].set_color(1,0,0)
            else:
		self.truc[i].set_color(0,1,0)

        return self.viewer.render(return_rgb_array = mode=='rgb_array')
