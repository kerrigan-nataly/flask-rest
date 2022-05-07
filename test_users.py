from requests import get, post, delete, put

print('получаем пользователей')
print(get('http://localhost:5000/api/users').json())

print('получаем одного пользователя')
print(get('http://localhost:5000/api/users/1').json())

print('Добавляем пользователя')
print(post('http://localhost:5000/api/users',
           json={
               'name': 'test user',
               'email': 'testuser@mars.org',
               'about': 'test user about',
               'password': 'testpass'
           }).json())

print('проверяем наличие нового пользователя')
print(get('http://localhost:5000/api/users').json())

print('проверяем возможность логина нового пользователя')
print(post('http://localhost:5000/api/users/login',
           json={
               'email': 'testuser@mars.org',
               'password': 'testpass'
           }).json())

user = post('http://localhost:5000/api/users/login',
            json={
                'email': 'testuser@mars.org',
                'password': 'testpass'
            }).json()
user_id = str(user['user_id'])

print('проверяем возможность логина несущестующего пользователя')
print(post('http://localhost:5000/api/users/login',
           json={
               'email': 'hacker@mars.org',
               'password': 'passwd'
           }).json())

print('проверяем возможность логина пользователя с неправельным паролем')
print(post('http://localhost:5000/api/users/login',
           json={
               'email': 'testuser@mars.org',
               'password': 'passwd'
           }).json())

print('Обновляем пользователя')
print(put('http://localhost:5000/api/users/' + user_id,
          json={
              'name': 'test user updated',
              'email': 'testuser@marsone.org',
              'about': 'test user about updated'
          }).json())

print('проверяем результат обновления пользователя')
print(get('http://localhost:5000/api/users/' + user_id).json())

print('Обновляем пользователя с паролем')
print(put('http://localhost:5000/api/users/' + user_id,
          json={
              'name': 'test user updated 2',
              'email': 'testuser@marsone.org',
              'about': 'test user about updated 2',
              'password': 'newpass'
          }).json())

print('проверяем результат обновления пользователя')
print(get('http://localhost:5000/api/users/' + user_id).json())

print('проверяем возможность логина пользователя с новым паролем')
print(post('http://localhost:5000/api/users/login',
           json={
               'email': 'testuser@marsone.org',
               'password': 'newpass'
           }).json())

print('удаляем пользователя')
print(delete('http://localhost:5000/api/users/' + user_id).json())

print('проверяем результат удаления пользователя')
print(get('http://localhost:5000/api/users/' + user_id).json())
