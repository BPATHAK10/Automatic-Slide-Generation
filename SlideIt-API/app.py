from flask import Flask, render_template, url_for, request, send_file
# import pandas as pd
import pickle
import slides
import json

from flask import jsonify
from flask_cors import CORS,cross_origin

# load the model from disk
# filename = 'model.pkl'
# model = pickle.load(open(filename, 'rb'))

app = Flask(__name__)
cors=CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def home():
	return jsonify({'message': 'Welcome to the SlideIt-API'})

@app.route('/download-slide', methods=['Get'])
def download_slide():
	return send_file(f'presentation_pdfs/{generatedSlides}.pdf', attachment_filename=f'{generatedSlides}.pdf', as_attachment=True)


@app.route('/predict', methods=['POST', 'GET'])
def predict():

	if request.method == 'POST':
		# extract the prediction from the model

		request_data = json.loads(request.data.decode('utf-8'))

		dataFromFrontend = request_data['data']
		# presentationContent = modelPrediction(dataFromFrontend)

		presentationContent = {
			"title": "Our first slide",
			"subtitle": "This is our first slide",
			"slides": [
				[
					"this is a bullet point",
					"this is another bullet point",
					" this is another bullet point",
				],
			],
		}
		

		generatedSlides = slides.generateSlidesFromAPI(presentationContent)
		# print(generatedSlides)
	
		# return send_file(f'presentation_pdfs/{generatedSlides}.pdf', download_name=f'{generatedSlides}.pdf',as_attachment=False)
		return jsonify({'message': 'Slides generated successfully'})

	
	if request.method == 'GET':
		return jsonify({'message': 'Please use the POST method'})	


if __name__ == '__main__':
	app.run(debug=True)
