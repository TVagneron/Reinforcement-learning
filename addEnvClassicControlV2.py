import os
from distutils.sysconfig import get_python_lib
from shutil import copyfile

# TODO detect className = "TestThomas2DRota"

def isInFile(line,afile):
	res = False
	for l in afile:
		if line in l:
			res = True	
	return res;

def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

try:
	print('---------------------------------------------------------------')
	print(' addEnv -- add a new environment in gym set up with virtualenv. The env is pushed in classic_control group ')
	newEnvName = "CartPole-v6"
	className = "TestThomas2DRotalittle"
	print(' The id of this env will be ' + newEnvName)
	print('---------------------------------------------------------------')
	print('I modify files in gym (which is set up in ' + os.environ['VIRTUAL_ENV'] + ').')
	for srcfile in files(os.getcwd()):
		if ('.py' in srcfile) and ('addEnvClassicControl.py' not in srcfile) and ('~' not in srcfile):
			envfilename = os.getcwd() + '/' + srcfile 	
			envfile = open(envfilename,"r")
			
			for line in envfile:
				if 'class ' in line:
					line = line.replace("class ","")
					line = line.replace("(gym.Env):","")
					line = line.replace(" ","")
					line = line.replace("\n","")
					cRlassName = line
					print(className)
			
			#torch-twrl/venv/lib/python2.7/site-packages/gym/envs/__init__.py
			general_init_file_path = get_python_lib() + '/gym/envs/__init__.py'
			print(general_init_file_path)
			general_init_file = open(general_init_file_path,"r")
			gen_init_def = isInFile(newEnvName,general_init_file) 
			print(gen_init_def)
			general_init_file.close()
			if not gen_init_def:
				general_init_file_write = open(general_init_file_path,"a")
				general_init_file_write.write("\nregister(\n")
				general_init_file_write.write("    id='" + newEnvName +"',\n")
				general_init_file_write.write("    entry_point='gym.envs.classic_control:" + className + "',\n")
				general_init_file_write.write("    timestep_limit=500,\n")
				general_init_file_write.write("    reward_threshold=475.0,\n")
				general_init_file_write.write(")")
				general_init_file_write.close()

			#torch-twrl/venv/lib/python2.7/site-packages/gym/envs/classic_control/__init__.py
			init_file_path = get_python_lib() + '/gym/envs/classic_control/__init__.py'
			init_file = open(init_file_path,"r")
			init_def = isInFile(srcfile.replace('.py',''),init_file) 
			print(init_def)
			init_file.close()
			if not init_def:
				init_file_write = open(init_file_path,"a")
				init_file_write.write("from gym.envs.classic_control." + srcfile.replace('.py','') + " import " + className + "\n")
				init_file_write.close()


			#torch-twrl/venv/lib/python2.7/site-packages/gym/scoreboard/__init__.py
			sb_init_file_path = get_python_lib() + '/gym/scoreboard/__init__.py'
			sb_init_file = open(sb_init_file_path,"r")
			sb_init_def = isInFile(newEnvName,sb_init_file)
			print(sb_init_def)
			sb_init_file.close()
			if not sb_init_def:
				sb_init_file_read = open(sb_init_file_path,"r")
				sb_file_lines = []
				for line in sb_init_file_read:
					sb_file_lines.append(line)
				sb_init_file_read.close()
				sb_init_file_write = open(sb_init_file_path,"w")
				for line in sb_file_lines:
					if 'registry.finalize()' not in line:
						sb_init_file_write.write(line)
				sb_init_file_write.write('add_task(\n')
				sb_init_file_write.write("    id='" + newEnvName + "',\n")
				sb_init_file_write.write("    group='classic_control',\n")
				sb_init_file_write.write("    summary=\"New environment added to gym in classic control group\",\n")
				sb_init_file_write.write("    description='Not available',\n")
				sb_init_file_write.write("    background='Not available',\n")
				sb_init_file_write.write(")\n")
				sb_init_file_write.write("\n")
				sb_init_file_write.write("registry.finalize()\n")	
				sb_init_file_write.close()

			print("do you want to run this with reinforce, tdlambda or random?")
			method = raw_input("enter it here : ")
			
			if (method == "reinforce"):
				#torch-twrl/examples/cartpole-pg.sh
				# example file creation
				print("creation of an example file for " + newEnvName)
				new_example_file_name = os.getcwd() + '/../examples/' + newEnvName + '-pg.sh'
				new_example_file = open(new_example_file_name,"w")
				new_example_file.write('#! /bin/bash\n')
				new_example_file.write('\n')
				new_example_file.write('clear\n')
				new_example_file.write("echo \"REINFORCE on " + newEnvName + " Environment\"\n")
				new_example_file.write("echo '************************************'\n")
				new_example_file.write("th run.lua \\\n")
				new_example_file.write("   -env '" + newEnvName + "' \\\n")
				new_example_file.write("   -policy categorical \\\n")
				new_example_file.write("   -learningUpdate reinforce \\\n")
				new_example_file.write("   -model mlp \\\n")
				new_example_file.write("   -optimAlpha 0.9 \\\n")
				new_example_file.write("   -timestepsPerBatch 1000 \\\n")
				new_example_file.write("   -stepsizeStart 0.3 \\\n")
				new_example_file.write("   -gamma 1 \\\n")
				new_example_file.write("   -nHiddenLayerSize 10 \\\n")
				new_example_file.write("   -gradClip 5 \\\n")
				new_example_file.write("   -baselineType padTimeDepAvReturn \\\n")
				new_example_file.write("   -beta 0.01 \\\n")
				new_example_file.write("   -weightDecay 0 \\\n")
				new_example_file.write("   -windowSize 10 \\\n")
				new_example_file.write("   -nSteps 1000 \\\n")
				new_example_file.write("   -nIterations 1000 \\\n")
				new_example_file.write("   -video 100 \\\n")
				new_example_file.write("   -optimType rmsprop \\\n")
				new_example_file.write("   -verboseUpdate true \\\n")
				new_example_file.write("   -uploadResults false \\\n")
				new_example_file.write("   -renderAllSteps false \n")		
				new_example_file.close()
		
			elif(method == "tdlambda"):
				print("creation of an example file for " + newEnvName)
				new_example_file_name = os.getcwd() + '/../examples/' + newEnvName + '-td.sh'
				new_example_file = open(new_example_file_name,"w")
				new_example_file.write('#! /bin/bash\n')
				new_example_file.write('\n')
				new_example_file.write('clear\n')
				new_example_file.write("echo \"TD(Lambda) agent on " + newEnvName + " Environment\"\n")
				new_example_file.write("echo '************************************'\n")
				new_example_file.write("th run.lua \\\n")
   				new_example_file.write("   -env '" + newEnvName + "' \\\n")
   				new_example_file.write("   -policy egreedy \\\n")
   				new_example_file.write("   -learningUpdate tdLambda \\\n")
   				new_example_file.write("   -model qFunction \\\n")
   				new_example_file.write("   -learningType noBatch \\\n")
   				new_example_file.write("   -epsilon 0.2 \\\n")
   				new_example_file.write("   -epsilonDecayRate 0.9999 \\\n")
   				new_example_file.write("   -initialWeightVal 0 \\\n")
   				new_example_file.write("   -tdLearnUpdate SARSA \\\n")
   				new_example_file.write("   -relativeAlpha 0.05 \n")
				new_example_file.close()

			elif(method == "random"):
				print("creation of an example file for " + newEnvName)
				new_example_file_name = os.getcwd() + '/../examples/' + newEnvName + '-td.sh'
				new_example_file = open(new_example_file_name,"w")
				new_example_file.write('#! /bin/bash\n')
				new_example_file.write('\n')
				new_example_file.write('clear\n')
				new_example_file.write("echo \"Random agent on " + newEnvName + " Environment\"\n")
				new_example_file.write("echo '************************************'\n")
				new_example_file.write("th run.lua \\\n")
   				new_example_file.write("   -env 'CartPole-v0' \\\n")
   				new_example_file.write("   -policy random \\\n")
   				new_example_file.write("   -learningUpdate noLearning \\\n")
   				new_example_file.write("   -model noModel \\\n")
   				new_example_file.write("   -video 0 \\\n")
   				new_example_file.write("   -renderAllSteps false \\\n")
   				new_example_file.write("   -nIterations 10 \n")
				new_example_file.close()


			# update torch-twrl/venv/lib/python2.7/site-packages/gym/envs/classic_control/testcodethomas.py
			filenameout = os.getcwd() + '/' + srcfile 
			filenamein = get_python_lib() + '/gym/envs/classic_control/' + srcfile
			copyfile(filenameout, filenamein)


except KeyError as e:
	print('--Error--')
	print('You should probably source the accurate file e.g. write ')
	print('   source venv/bin/activate')
	print('       or')
	print('   source ../venv/bin/activate')
	print('in the shell.')	
	print('I do nothing!')
