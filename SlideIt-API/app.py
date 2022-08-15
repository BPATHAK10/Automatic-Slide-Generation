from flask import Flask, render_template, url_for, request
# import pandas as pd
import pickle
import slides

from flask import jsonify

# load the model from disk
# filename = 'model.pkl'
# model = pickle.load(open(filename, 'rb'))

app = Flask(__name__)


@app.route('/')
def home():
	return jsonify({'message': 'Welcome to the SlideIt-API'})


@app.route('/predict', methods=['POST', 'GET'])
def predict():

	if request.method == 'POST':
		# extract the prediction from the model

		# presentationContent = request.get_json()
		# print(presentationContent)

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
		print(generatedSlides)

		return jsonify({'message': "you now get the slides pdf"})

	if request.method == 'GET':
		return jsonify({'message': 'Please use the POST method'})	


if __name__ == '__main__':
	app.run(debug=True)
