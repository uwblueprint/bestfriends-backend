# Set-up server

```
pip install Flask
git clone git@github.com:uwblueprint/bestfriends-backend.git
cd ..
export FLASK_APP=bestfriends-backend
export FLASK_ENV=development
flask run
```

# Testing
Send a post request using the following python script, make sure to have the image you want to send in the directory
```
import requests

files = {'file': open('doggo.jpg', 'rb')}
r = requests.post('http://127.0.0.1:5000/upload', files=files)
```

# Docker Deployment

To build the docker image of the application you can run

```bash
docker build --rm -t bestfriends .
```

To run the image you can use

```bash
docker run -p 80:5000 bestfriends
```

[Information on deploying to docker can be found here.](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml)
