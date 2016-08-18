import os, sys, shelve, datetime

def main():
	def print_logo():
		print ''
		print '############################' 
		print '||      task-tracker      ||' 
		print '############################'
		print ''

	def prompt():
		initial_choice = raw_input('What would you like to work on? ')
		
		if initial_choice == 'new project':
			new_project()
		elif os.path.isdir(initial_choice): 
			project(initial_choice)
		else:
			print ''
			print "Type the name of an existing project, or type 'new project' to start a new one"
			prompt()

	def new_project():
		project_name = raw_input('Project name: ')
		if os.path.exists(project_name): 
			print
			print '%s already exists! Use another name.' % (project_name)
			new_project()
		elif project_name == 'new project':
			print ''
			print "You can't use that name! It's reserved for this program"
			new_project()
		else: 
			os.mkdir(project_name)
		
		units = raw_input('Name of units: ')
		
		def get_total_goal(): 
			while True: 
				try: 
					total_goal = int(raw_input('Total goal: '))
					if total_goal < 1: 
						print 'Enter a number greater than 0!'
						continue
					return total_goal
					break
				except ValueError: 
					print 'Enter a number greater than 0!'
					continue
				else: 
					return total_goal
					break

		total_goal = get_total_goal()

		settings = shelve.open('./' + project_name + '/settings')
		settings['units'] = units
		settings['total_goal'] = total_goal
		settings['date_created'] = datetime.datetime.now().strftime('%Y-%m-%d')
		settings.close()

		project(project_name)

	def project(project_name): 
		os.chdir('./' + project_name)
		settings = shelve.open('settings')
		units = settings['units']
		total_goal = settings['total_goal']
		data = open('data.txt', 'a')

		def project_prompt():
			print
			project_prompt_choice = raw_input('What would you like to do? ')
			if project_prompt_choice == 'enter data': 
				enter_data()
			elif project_prompt_choice == 'show data':
				show_data()
			elif project_prompt_choice == 'exit' or project_prompt_choice == 'close':
				sys.exit()
			else: 
				print 
				print "Uh oh! I didn't catch that"
				print "You can type 'enter data' to submit data, or type 'show data' to display it" 
				project_prompt()
			
		def enter_data(): 
			data = open('data.txt', 'a')
			while True: 
				try: 
					data_to_enter = int(raw_input('How many %s did you complete today? ' % units))
					if data_to_enter < 0: 
						print ''
						print 'Enter a number equal to or greater than zero!'
						continue
					break
				except ValueError: 
					print ''
					print 'Enter a number equal to or greater than zero!'
					continue
			data.write(datetime.datetime.now().strftime('%Y-%m-%d') + ': ' + str(data_to_enter) + '\n')		
			data.close()
			display_data_info()
			project_prompt()

		def show_data():
			if os.path.getsize('data.txt') < 1: 
				print "Looks like nothing's here!"
				return project_prompt()
			
			data = open('data.txt')
			print ''
			print data.read()
			data.close()
			
			display_data_info()
			project_prompt()

		def display_data_info(): 
			data = open('data.txt', 'r')
			data_list = data.readlines()
			values = []
			
			for d in data_list: 
				t = d[12:-1]
				try:
					t = int(t)
					values.append(t)
				except ValueError:
					print 'Uh oh! It looks like the data.txt file has been altered.'
					print 'Open it and make sure each line is in this format: 2016-08-01: <number>'
					sys.exit()

			units_to_date = sum(values)
			units_left = int(total_goal) - int(units_to_date)

			print
			print "You've completed %d %s" % (units_to_date, units)
			if units_left < 1: 
				print "Your goal was %d" % (total_goal)
				print "Congrats, you completed your goal!"
			else:
				print "You've got %d %s to go!" % (units_left, units)
			
		project_prompt()

	print_logo()
	prompt()

try: 
	main()	
except KeyboardInterrupt: 
	print ''
	print 'Shutting down'
	sys.exit()