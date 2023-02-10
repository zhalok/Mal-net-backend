# How to run the backend

pip install -r requirement.txt

Download pretrained models from [Link text Here](https://drive.google.com/drive/u/0/folders/1-KiwRxHOWfSFxlANekYvvLbRCUoMgX2Y) and place then in the models folder

python3 app.py (Run the application)

You will get a public link of proxy server put that link in the axios instance in the front-end /utils/axios.js file in order to connect the front-end with the back-end

or simply comment the 38 no line of the app.py file in case if you don't want to use a proxy server

`public_url = ngrok.connect(port,"http",remote_addr="http://127.0.0.1:3000").public_url
`

then start the project

in case if you want to run the project in debug mode then simply run the command

flask --debug run

but make sure that you are not using a proxy server while running the project in debug mode
