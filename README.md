# python_prediction_server

A one file python web server for predicting a keras model.

### Motivation
I want a simple system to show others to use the trained model easily(=without a framework:django/flask, just BaseHTTPServer) even on the NotePC (on ubuntu 18.04 without a GPU).
Because in my company managers who don't know programmings are seriously talking about deciding the spec of a PC for using a machine learning. I can't believe but they're going...

### How to use

I tried on Ubuntu 18.04 (without GPU, on NotePC).
I referred to [【第1回】Pythonではじめるディープラーニング](https://qiita.com/naoyoshinori/items/5389294c4121bc5eccb1) to prepare the environment.

1. `sudo apt install python3-pip python3-dev`
1. `pip3 install tensorflow`
1. `pip3 install keras`
1. Prepare a trained model by keras. I referred to [少ない画像から画像分類を学習させる方法（kerasで転移学習：fine tuning）](https://spjai.com/keras-fine-tuning/) (...so the default model file name is `fruits.hdf5`)
1. Edit variables in `prediction_server.py` as you like
1. `python prediction_server.py`
1. Access to http://localhost:8180

### Screen Shots

|Good Case|Bad Case|
|---|---|
|![good case](https://raw.githubusercontent.com/wiki/u-ryo/python_prediction_server/images/good.png)|![bad case](https://raw.githubusercontent.com/wiki/u-ryo/python_prediction_server/images/bad.png)|

![prediction](https://raw.githubusercontent.com/wiki/u-ryo/python_prediction_server/images/prediction.gif)
