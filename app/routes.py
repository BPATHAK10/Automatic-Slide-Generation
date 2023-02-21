from flask import Flask, render_template, url_for, request
# import pandas as pd
import model.pipeline as pipeline # model\pipeline.py
import videogen as videogen
import slidegen as slidegen
import audiogen as audiogen

import parsing as parsing
import datetime

import shutil
import os

import json
from flask import jsonify
from app import app
from flask import Response

def execute_pipeline(document):
	os.mkdir('output')
	print (document['text'])
	document['slides'] = pipeline.get_slide_content(document['text'])

	#mutithreading can be used here
	slidegen.create_slides(document)
	audiogen.synthesize_audio(document)

	number_of_slides = len(document['slides'])+2
	videogen.generate_video(number_of_slides)
	shutil.rmtree('output', ignore_errors=True)

@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()

@app.route('/')
def home():
	return jsonify({'message': 'Welcome to the SlideIt-API'})


@app.route('/predict_text', methods=['POST', 'GET'])
def predict_text():

	if request.method == 'POST':
		# extract the prediction from the model
		request_data = json.loads(request.data.decode('utf-8'))
		raw_data = request_data['data']
		document = parsing.parse_text(raw_data)
		execute_pipeline(document)
		return jsonify({'message': "you now get the pdf and output video"})

	if request.method == 'GET':
		return jsonify({'message': 'Please use the POST method'})	

@app.route('/predict_url', methods=['POST', 'GET'])
def predict_url():

	if request.method == 'POST':
		# extract the prediction from the model
		request_data = json.loads(request.data.decode('utf-8'))
		raw_data = request_data['url']
		document = parsing.parse_url(raw_data)
		execute_pipeline(document)				
		return jsonify({'message': "you now get the pdf and output video"})

	if request.method == 'GET':
		return jsonify({'message': 'Please use the POST method'})	

@app.route('/predict_upload', methods=['POST', 'GET'])
def predict_upload():

	if request.method == 'POST':
		# extract the prediction from the model
		print ("hello")
		request_data = json.loads(request.data.decode('utf-8'))
		raw_data = request_data['upload']
		document = parsing.parse_upload(raw_data)
		execute_pipeline(document)			
		return jsonify({'message': "you now get the pdf and output video"})

	if request.method == 'GET':
		return jsonify({'message': 'Please use the POST method'})	
