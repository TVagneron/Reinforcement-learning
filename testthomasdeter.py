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
	#Initial datas
        self.treeslocations = [3.0, 5.0];
	#Initilisation of ending counters
	self.count = 0
	self.counter = 0
	self.timecount = 0
	self.firetrees = 0
        # Angle at which to fail the episode
        self.theta_threshold_radians = 12 * 2 * math.pi / 360
        self.x_threshold = 2.4

        # Angle limit set to 2 * theta_threshold_radians so failing observation is still within bounds$
        high = np.array([
            self.x_threshold * 2,
            np.finfo(np.float32).max,
            self.theta_threshold_radians * 2,
            np.finfo(np.float32).max]+[0]*len(self.treeslocations))


        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(-high, high)

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

        world_width = self.x_threshold*2
        scale = screen_width/world_width

        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        state = self.state
        #print("bla")
        #print(state)
        #x, x_dot, theta, theta_dot, v1, v2, v3, v4 = state # TODO TODO TODO access data from a tuple
        x = state[0]
        x_dot = state[1]
        theta = state[2]
        theta_dot = state[3]
        treesStatesList = []
	for i in range(len(self.treeslocations)):
            treesStatesList.append(state[4+i])
	treesStates = ()
	
        #print(treesStates)
        
        if (self.timecount > 0):
        	self.timecount += 1
        
        if (self.timecount == 50):
        	self.timecount = 0
        	

        if((treesStatesList[self.counter]==0) and (self.timecount == 0 and self.firetrees == 0)):
            	treesStatesList[self.counter] = 1
                self.firetrees = 1
                self.counter += 1
                if (self.counter == len(self.treeslocations)):
                	self.counter = 0
                	
        
                	
                
               
  
        
        	
        for i in range(len(self.treeslocations)):
        	if (treesStatesList[i] == 1 and action == i):
        		treesStatesList[i] = 0
        		reward = 1.0
        		self.firetrees = 0
        		self.timecount += 1
        	else :
        		reward = 0.0
	for i in range(len(self.treeslocations)):
               	treesStates += (treesStatesList[i],)
	self.state = (x,x_dot,theta,theta_dot) + treesStates 
	
	#state of trees

	
                	
        #print(treesStates)
	#print(self.state[0]*scale/world_width+0.5)
        self.state = (x,x_dot,theta,theta_dot) + treesStates 


        #time.sleep(0.5)
	self.count += 1
	done = False

	if (self.count == 20000):
		done = True
        
	
	return np.array(self.state), reward, done, {}

    def _reset(self):
        treesStates = []
        for i in range(len(self.treeslocations)):
            treesStates.append(0)
        self.state = np.concatenate( (self.np_random.uniform(low=-0.05, high=0.05, size=(4,)),treesStates), axis=0)
	self.counter = 0
	self.count = 0
	self.timecount = 0
        #print("reset")
        #print(firstPart)
        #print(treesStates)
        #self.state = np.concatenate((firstPart , treesStates), axis=0)
	#print("self.state")
        #print(self.state)	
        self.steps_beyond_done = None
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
            axleoffset =cartheight/4.0
	    self.chose = []
            cart = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
	    self.chose.append(cart)
            self.carttrans = rendering.Transform()
            cart.add_attr(self.carttrans)
            self.viewer.add_geom(self.chose[0])
            l,r,t,b = -polewidth/2,polewidth/2,polelen-polewidth/2,-polewidth/2
            pole = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            pole.set_color(.8,.6,.4)
            self.poletrans = rendering.Transform(translation=(0, axleoffset))
            pole.add_attr(self.poletrans)
            pole.add_attr(self.carttrans)
            self.viewer.add_geom(pole)
            self.axle = rendering.make_circle(polewidth/2)
            self.axle.add_attr(self.poletrans)
            self.axle.add_attr(self.carttrans)
            self.axle.set_color(.5,.5,.8)
            self.viewer.add_geom(self.axle)
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
                
                

        x = self.state
        cartx = x[0]*scale+screen_width/2.0 # MIDDLE OF CART
        self.carttrans.set_translation(cartx, carty)
        self.poletrans.set_rotation(-x[2])
        for i in range(len(self.treeslocations)):
            if(x[i+4]==1):
                self.truc[i].set_color(1,0,0)
            else:
		self.truc[i].set_color(0,1,0)
	#red_color = self.temperature /self.tempLim
	#self.chose[0].set_color(red_color,0,0)
        return self.viewer.render(return_rgb_array = mode=='rgb_array')
