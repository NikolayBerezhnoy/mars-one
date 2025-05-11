from requests import get, post, delete

# корректные
print(get('http://localhost:5000/api/v2/users').json())

user_data = {
    'surname': 'Doe',
    'name': 'John',
    'age': 30,
    'position': 'Developer',
    'speciality': 'aaa',
    'address': '123',
    'email': 'test@example.com'
}
print(post('http://localhost:5000/api/v2/users', json=user_data).json())

print(delete('http://localhost:5000/api/v2/users/1').json())

# некорректные
print(get('http://localhost:5000/api/v2/users/9999').json())

invalid_user_data = {
    'surname': 'Smith',
    'name': 'Jane',
    'age': 25,
    'position': 'dev',
    'speciality': 'a',
    'address': '456'
}
print(post('http://localhost:5000/api/v2/users', json=invalid_user_data).json())

print(delete('http://localhost:5000/api/v2/users/q').json())

#корректные
print(get('http://localhost:5000/api/v2/jobs').json())
print(get('http://localhost:5000/api/v2/jobs/1').json())
print(get('http://localhost:5000/api/v2/jobs/2').json())

#некорректные
print(get('http://localhost:5000/api/v2/jobs/q').json())
print(get('http://localhost:5000/api/v2/jobs/1aa').json())
print(get('http://localhost:5000/api/v2/jobs/2222').json())
