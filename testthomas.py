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

class TestThomas(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    def __init__(self):
        self.gravity = 9.8
        self.masscart = 1.0
        self.masspole = 0.1
        self.total_mass = (self.masspole + self.masscart)
        self.length = 0.5 # actually half the pole's length
        self.polemass_length = (self.masspole * self.length)
        self.force_mag = 10.0
        self.tau = 0.02  # seconds between state updates
	#Initial datas
	self.vit = 1
        self.treeslocations = [1.0,3.0, 5.0, 8.0];
	#Initilisation of ending counters
	self.count = 0
	self.counter = 0
	self.reservoir = 100
	self.batterie = 10000000000000000
	self.temperature = 0
	self.tempLim = 200
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

	#movement
	vitesse = 0
	if (action == 1 and x<0.9):
		vitesse = self.vit
	elif (action == 0 and x > -0.9):
		vitesse = -self.vit
	#vitesse = 1
        x  = x + self.tau * vitesse
        

	#temperature indicator
	tempcounter = 0
	for i in range(len(self.treeslocations)):
		ifcounter = 0
		if (self.temperature != 0 and ((0.1*self.treeslocations[i]-0.05)>(self.state[0]*scale/screen_width+0.5)) and ifcounter == 0):
			ifcounter +=1
			tempcounter += 1
		elif (self.temperature != 0 and (self.state[0]*scale/screen_width+0.5)>(0.1*self.treeslocations[i]+0.05) and ifcounter == 0):
			ifcounter +=1
			tempcounter +=1
		elif ((0.1*self.treeslocations[i]-0.05<self.state[0]*scale/screen_width+0.5<0.1*self.treeslocations[i]+0.05) and self.state[4+i]==0 and self.temperature != 0 and ifcounter == 0):
			tempcounter += 1

	#increase or decrease of the robot temperature
	if (tempcounter == len(self.treeslocations) and self.temperature != 0):
		self.temperature -= 1
	if ((0.1*self.treeslocations[i]-0.05<self.state[0]*scale/screen_width+0.5<0.1*self.treeslocations[i]+0.05) and self.state[4+i]==1):
		self.temperature += 1
	#decrease of the initial values due to actions
	if (action == 0 or action == 1 or action == 2):
		self.batterie -= 1
	if (action ==2):
		self.reservoir -= 1

	#action of extinguishing the fire
	for i in range(len(self.treeslocations)):
		if ((0.1*self.treeslocations[i]-0.05<self.state[0]*scale/screen_width+0.5<0.1*self.treeslocations[i]+0.05) and self.state[4+i]==1 and action == 2):
			treesStatesList[i] = 0
			reward = 1.0			

	
	#state of trees
        for i in range(len(self.treeslocations)):
            b = treesStatesList[i]
            if((treesStatesList[i]==0) and (self.np_random.uniform(0,1)>0.95)):
                b=1
            treesStates += (b,)
        #print(treesStates)
	#print(self.state[0]*scale/world_width+0.5)
        self.state = (x,x_dot,theta,theta_dot) + treesStates 


        #time.sleep(0.5)
	self.count += 1
	done = False

	#ending conditions
	if (self.temperature == self.tempLim):
		done = True
		reward = self.counter
		return np.array(self.state), reward, done, {}
	elif (self.batterie == 0):
		done = True
		reward = self.counter
		return np.array(self.state), reward, done, {}
	elif (self.reservoir == 0):
		done = True
		reward = self.counter
		return np.array(self.state), reward, done, {}
	elif (self.count == 20000):
		done = True
		reward = self.counter
        
	
	reward = self.counter
	return np.array(self.state), reward, done, {}

    def _reset(self):
        treesStates = []
        for i in range(len(self.treeslocations)):
            treesStates.append(0)
        self.state = np.concatenate( (self.np_random.uniform(low=-0.05, high=0.05, size=(4,)),treesStates), axis=0)
	self.counter = 0
	self.count = 0
	self.temperature = 0
	self.batterie = 100000000000
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
	red_color = self.temperature /self.tempLim
	self.chose[0].set_color(red_color,0,0)
        return self.viewer.render(return_rgb_array = mode=='rgb_array')
