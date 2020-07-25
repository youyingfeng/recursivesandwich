import requests

# req = requests.get('http://localhost:3000/highscores')
# print(req.text)

post = requests.post('http://localhost:3000/highscores',
                      headers = {'User-Agent': 'The Tower - Game Clien'},
                      data = {'user': 'lmao', 'time': 95})
print(post.status_code)
print('Complete!')