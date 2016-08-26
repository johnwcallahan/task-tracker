import os
import sys
import shelve
import datetime

def print_logo():
	print '\n############################' 
	print '||      task-tracker      ||' 
	print '############################'

def prompt():
	while True:
		try:
			initial_choice = raw_input('\nWhat would you like to work on? ')
			if initial_choice == 'new' or os.path.isdir(initial_choice):
				return initial_choice
			else: 
				raise ValueError
		except ValueError: 
			print "\nType the name of an existing project, or type 'new project' to start a new one"
		else: 
			break

def setup_new_project():
	# Get project name 
	while True:
		try: 
			project_name = raw_input('\nProject name: ')
			if project_name == 'new': 
				raise ValueError
			elif os.path.exists(project_name): 
				raise OSError			
		except ValueError: 
			print '\nYou can\'t use that name!' 
		except OSError:
			print '\n{} already exists! Use another name.'.format(project_name)					
		else: 
			os.mkdir(project_name)
			break
	
	# Get units of measurement
	units = raw_input('Units of measurement: ')
	
	# Get target goal 
	while True: 
		try: 
			target_goal = int(raw_input('Target goal: '))
			if target_goal < 1: 
				raise ValueError
		except ValueError: 
			print '\nEnter a number greater than 0!'
		else: 
			break

	# create settings.db to save units and target goal
	settings = shelve.open('{}/settings'.format(project_name))
	settings['units'] = units
	settings['target_goal'] = target_goal
	settings.close()

	return project_name

def get_project_data(project_name): 
	project_data = {}
	
	settings = shelve.open('{}/settings'.format(project_name))
	project_data['units'] = settings['units']
	project_data['target_goal'] = settings['target_goal']

	if os.path.isfile('{}/data.txt'.format(project_name)):
		mode = 'r'
	else: 
		mode = 'w+'
	
	with open('{}/data.txt'.format(project_name), mode) as data: 
		values = data.readlines()
	project_data['values'] = values

	return project_data

	
def enter_data(project_name, project_data): 
	while True: 
		try: 
			values_to_enter = int(raw_input('How many {} did you complete today? '.format(project_data['units'])))
			if values_to_enter < 0:
				raise ValueError
		except ValueError: 
			print '\nEnter a number equal to or greater than zero!'
		else:
			with open('{}/data.txt'.format(project_name), 'a') as data:
				data.write('{}: {}\n'.format(datetime.datetime.now().strftime('%Y-%m-%d'), str(values_to_enter)))
			break


def show_data(project_data):
	if len(project_data['values']) == 0:
		print '\nLooks like nothing\'s here!'
		return
	print ''
	for value in project_data['values']:
		print value[:-1]

def show_data_info(project_data): 
	values = []
	for value in project_data['values']: 
		v = value[12:-1]
		try:
			v = int(v)
			values.append(v)
		except ValueError:
			print '\nIt looks like the data.txt file has been altered.'
			print 'Open it and make sure each line is in this format: 2016-08-01: <integer>'
			print 'Shutting down'
			sys.exit()

	units_to_date = sum(values)
	units_left = int(project_data['target_goal']) - int(units_to_date)

	print '\nYou\'ve completed {} {}'.format(units_to_date, project_data['units'])
	if units_left < 1: 
		print 'Your goal was {}'.format(project_data['target_goal'])
		print 'Congrats, you completed your goal!'
	else:
		print 'You\'ve got {} {} to go!'.format(units_left, project_data['units'])

def main():
	print_logo()
	initial_choice = prompt()
	if initial_choice == 'new': 
		project_name = setup_new_project()
	else: 
		project_name = initial_choice
	project_data = get_project_data(project_name)
	
	while True: 
		project_prompt_choice = raw_input('\nWhat would you like to do? (enter, show, exit) ').lower()
		if project_prompt_choice == 'enter': 
			enter_data(project_name, project_data)
			project_data = get_project_data(project_name)
			show_data_info(project_data)
		elif project_prompt_choice == 'show':
			show_data(project_data)
			show_data_info(project_data)
		elif project_prompt_choice == 'exit':
			break
		else: 
			print '\nI didn\'t catch that!'	

	print '\nGoodbye!'
	sys.exit()	

try: 
	main()	
except KeyboardInterrupt: 
	print '\nGoodbye!'
	sys.exit()