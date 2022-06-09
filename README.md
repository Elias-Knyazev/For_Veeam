# Readme siinc_dir_to_dir.py

sync_dir_to_dir.py - программа синхронизации каталогов и файлов между каталогом-источником и каталогом-репликой.

Программу следует запускать из командной строки в виде: path_to_program\sync_dir_to_dir.py dir_prime to dir_second  -l dir_log_file  -p  time_to_repeat

Где:
path_to_program - путь до программы.
dir_prime - путь до каталога-источника(включая сам каталог).

dir_second - путь до каталога-реплики(включая сам каталог). Если каталога не существет программа создаст его.

to  обязательный ключ, от него строится пути каталога-источника(dir_prime) и каталога-реплики (dir_prime).

-l опциональный ключ, создает лог-файл. Путь, имя файла лога и расширение задается пользователем. Если не задан, сделает лог в папку где лежит программа. 

-p  опциональный ключ, задается значение в секундах. Значение задает перод повторения программы. Если не задан или равен 0, то программа выполнится  один раз.

Приятного пользования! 
