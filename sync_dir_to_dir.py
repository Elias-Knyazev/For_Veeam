import os, datetime, time, shutil, sys
from pathlib import Path

#Модуль синхронизации каталогов и файлов каталога-реплики с каталогом-источника
def synchrone_prime_dir(path_p, path_s, log):
	ms_start=('Начало работы модуля синхронизации каталогов и файлов каталога-реплики с каталогом-источника'+'\n\n')
	ms_end=('Конец работы модуля синхронизации каталогов и файлов каталога реплики с каталогом источника:')
	log = open(log, 'a')
	print(ms_start)
	log.write(ms_start)
	start_time=datetime.datetime.now()
	tree=[]
	n=len(path_p)+1

	for address, dirs, files in os.walk(path_p): #начало обхода каталогов и файлов в каталоге источнике

		for file in files:
			tree.append(Path(address[n:]).joinpath(file)) #формирование списка путей до файлов без пути каталога-источника

		address_rep=address.replace(path_p, path_s)
		if not os.path.exists(address_rep): #проверка существования каталогов в каталоге-реплике равных каталогу-источнику
			shutil.copytree(address, address_rep, ignore_dangling_symlinks=True) # копирование файлов и каталогов из каталога-источника в каталог-реклику(игноририрует ссылки)
			message_1=('Каталог ' +address_rep+ ' был создан, т.к. отсутвовал в каталоге-реплике')
			message_2='Файл '+str(Path(address[n:]).joinpath(file))+' отсутвовал и был скопирован из каталога-источника'
			log.write(message_1+'\n')
			log.write(message_2+'\n')
			print(message_2)
			print(message_1)

	for line in tree:     #Проверка наличия и синхронизация файлов в каталоге-реплике с каталогом-источником
		path_p_f=Path(path_p).joinpath(line)
		path_s_f=Path(path_s).joinpath(line)

		if os.path.exists(path_s_f): #проверка наличия файлов в каталоге-источнике
			if (os.path.getmtime(path_p_f)!=os.path.getmtime(path_s_f)): # проверка на изменение файлов
				shutil.copy2((path_p_f), (path_s_f), follow_symlinks=False) 
				message = 'Файл '+str(path_s_f)+' был синхронизирован'
				log.write(message+'\n')
				print(message)
		else: #при отсутвии файла в каталоге-реплике скопирует его из каталога-источника
			shutil.copy2((path_p_f), (path_s),follow_symlinks=False)
			message = ('Файл '+str(path_s_f)+' отсутвовал и был скопирован из каталога-источника')
			log.write(message+'\n')
			print(message)


	end_time = datetime.datetime.now()-start_time
	log.write(ms_end +str(end_time)+'\n\n')
	print(ms_end+str(end_time)+'\n\n')
	log.close()

	return tree

#Модуль удаления лишних каталогов и файлов в каталоге-реплике
def delete_second_dir(path_p, path_s, log):
	ms_start=('Начало работы модуля удаления лишних каталогов и файлов в каталоге-реплике'+'\n\n')
	ms_end=('Конец работы модуля удаления лишних катологов. Время выполнения:')
	log = open(log, 'a')
	log.write(ms_start)
	print(ms_start)
	start_time=datetime.datetime.now()
	for address, dirs, files in os.walk(path_s):
		address_p=address.replace(path_s, path_p)
		if not os.path.exists(address_p):
			shutil.rmtree(address, ignore_errors=True)
			message = ('Каталог ' +address+ ' был удален, т.к. отсутвовал в каталоге-источнике')
			log.write(message+'\n')
			print(message)
		for file in files:
			if not os.path.exists(Path(address_p).joinpath(file)):
				os.remove(Path(address).joinpath(file))
				message = ('Файл ' +str(Path(address).joinpath(file))+ ' был удален, т.к. отсутвовал в каталоге-источнике')
				log.write(message+'\n')
				print(message)

	end_time = datetime.datetime.now()-start_time
	log.write(ms_end +str(end_time)+'\n\n')
	print(ms_end+str(end_time)+'\n\n')
	log.close()
	return

def welcome(s):
	if len(s)<4:
		print('Введены не допустимые параметры. ')
		return
	elif  len(s)>=4:
		per_time=0
		path_prime=''
		path_second=''
		log=str(Path(os.getcwd()).joinpath('log.txt'))
		for i in s:
			if i=='to' in s and s.count('to'):
				for j in range(1,s.index('to')):
					if j==s.index('to')-1:
						path_prime+=s[j]
					else:
						path_prime+=s[j]+' '
				path_second=s[s.index('to')+1]
				if not os.path.exists(path_second):
					os.mkdir(path_second)
			elif i=='-l' in s:
				ms_start_program='===Начало работы программы==='+'\n'
				log=s[s.index('-l')+1]
				log_file=open(log, 'w')
				log_file.write(ms_start_program)
				print(ms_start_program)
				log_file.close()
			elif i=='-p' in s:
				per_time=int(s[s.index('-p')+1])

		print('Добро пожаловать в программу sync_dir_to_dir.py'+'\n')
		print('Каталог-источник: '+path_prime+'\n')
		print('Каталог-реплика: '+path_second+'\n')
		print('Путь до файла-лога: '+log+'\n')
		answer=input('ВНИМАНИЕ! Каталоги и файлы каталога-реплики, несоответсвующие структуре католога-источника, будут безвозвратно удалены. '+'\n'+'\
Для продолжения нажмите два раза enter...')
		input()
		if per_time==0:
			delete_second_dir(path_prime, path_second, log)
			synchrone_prime_dir(path_prime, path_second, log)			
		else:
			while True:
				delete_second_dir(path_prime, path_second, log)
				synchrone_prime_dir(path_prime, path_second, log)
				for i in range(1, per_time):
					print('Время до повторного выполнения: '+'{} '.format(per_time-i), end='\r')
					time.sleep(1)
				time.sleep(per_time)
	return

if __name__ == '__main__':
	welcome(sys.argv)



	








