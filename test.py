from requests import get, post, delete, put

print('корректный запрос на добавление работы')
print(post('http://localhost:5000/api/jobs',
           json={
               'id': 4,
               'job': 'new job id 4',
               'team_leader': 1,
               'collaborators': '1, 2',
               'work_size': 2,
               'start_date': None,
               'end_date': None,
               'is_finished': False,
           }).json())

print('проверяем наличие добавленной работы')
print(get('http://localhost:5000/api/jobs').json())

print('корректный запрос на обновление работы')
print(put('http://localhost:5000/api/jobs/4',
          json={
              'job': 'job id 4 Updated!',
              'team_leader': 2,
              'collaborators': '3'
          }).json())

print('проверяем обновление работы с id 4')
print(get('http://localhost:5000/api/jobs/4').json())

print('не корректный запрос на обновление работы со строковым id')
print(put('http://localhost:5000/api/jobs/a',
          json={
              'job': 'job id 4 Updated!'
          }).json())

print('не корректный запрос на обновление работы без параметра id')
print(put('http://localhost:5000/api/jobs',
          json={
              'job': 'job id 4 Updated!'
          }).json())

print('проверяем обновление работы с id 4')
print(get('http://localhost:5000/api/jobs/4').json())

print('удаляем работу с id 4')
print(delete('http://localhost:5000/api/jobs/4').json())

print('проверяем отсутствие работы с id 4')
print(get('http://localhost:5000/api/jobs').json())

# корректный запрос на добавление работы
# {'success': 'OK'}
# проверяем наличие добавленной работы
# {'jobs': [{'collaborators': None, 'end_date': None, 'is_finished': True, 'job': 'New job 1', 'start_date': None, 'team_leader': 1, 'work_size': 2}, {'collaborators'
# : None, 'end_date': None, 'is_finished': False, 'job': 'New job 2', 'start_date': None, 'team_leader': 2, 'work_size': 5}, {'collaborators': '1, 2', 'end_date': Non
# e, 'is_finished': False, 'job': 'new job id 4', 'start_date': None, 'team_leader': 1, 'work_size': 2}]}
# корректный запрос на обновление работы
# {'success': 'OK'}
# проверяем обновление работы с id 4
# {'job': {'collaborators': '3', 'end_date': None, 'is_finished': None, 'job': 'job id 4 Updated!', 'start_date': None, 'team_leader': 2, 'work_size': None}}
# не корректный запрос на обновление работы со строковым id
# {'error': 'Not found'}
# не корректный запрос на обновление работы без параметра id
# {'error': 'Method Not Allowed'}
# проверяем обновление работы с id 4
# {'job': {'collaborators': '3', 'end_date': None, 'is_finished': None, 'job': 'job id 4 Updated!', 'start_date': None, 'team_leader': 2, 'work_size': None}}


# print(post('http://localhost:5000/api/news').json())

# print(post('http://localhost:5000/api/news',
#            json={'title': 'Заголовок'}).json())

# print(post('http://localhost:5000/api/news',
#            json={'title': 'Заголовок',
#                  'content': 'Текст новости',
#                  'user_id': 1,
#                  'is_private': False}).json())

# print(delete('http://localhost:5000/api/news/999').json())

# print(delete('http://localhost:5000/api/news/1').json())
