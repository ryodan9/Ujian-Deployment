'''
	Contoh Deloyment untuk Domain Data Science (DS)
	Orbit Future Academy - AI Mastery - KM Batch 3
	Tim Deployment
	2022
'''

# =[Modules dan Packages]========================

from distutils.command.upload import upload
from importlib.resources import path
import json
# from django.shortcuts import render
from flask import Flask,render_template,request,jsonify,session
#from flask_wtf import FlaskForm
#from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
#from wtforms.validators import InputRequired
import os
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from joblib import load

# =[Variabel Global]=============================

app   = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'asd82a'
app.config['UPLOAD_FOLDER'] = 'static/files'

model = None

#class UploadFileForm(FlaskForm):
    #file = FileField("File", validators=[InputRequired()])
    #submit = SubmitField("Upload File")

# =[Routing]=====================================

# [Routing untuk Halaman Utama atau Home]	

@app.route('/')
def beranda():
	# form = UploadFileForm()
	# if form.validate_on_submit():
	# 	file = form.file.data #mengambil file
	# 	file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) #menyimpan file
	return render_template('index.html')

# [Routing untuk API]	
@app.route("/api/deteksi",methods=['POST'])
def apiDeteksi():
	# Nilai default untuk variabel input atau features (X) ke model
	input_sepal_length = 5.1
	input_sepal_width  = 3.5
	input_petal_length = 1.4
	input_petal_width  = 0.2
	
	if request.method=='POST':
		# Set nilai untuk variabel input atau features (X) berdasarkan input dari pengguna
		input_sepal_length = float(request.form['sepal_length'])
		input_sepal_width  = float(request.form['sepal_width'])
		input_petal_length = float(request.form['petal_length'])
		input_petal_width  = float(request.form['petal_width'])
		
		# Prediksi kelas atau spesies bunga iris berdasarkan data pengukuran yg diberikan pengguna
		df_test = pd.DataFrame(data={
			"SepalLengthCm" : [input_sepal_length],
			"SepalWidthCm"  : [input_sepal_width],
			"PetalLengthCm" : [input_petal_length],
			"PetalWidthCm"  : [input_petal_width]
		})

		hasil_prediksi = model.predict(df_test[0:1])[0]

		# Set Path untuk gambar hasil prediksi
		if hasil_prediksi == 'Iris-setosa':
			gambar_prediksi = '/static/images/iris_setosa.jpg'
		elif hasil_prediksi == 'Iris-versicolor':
			gambar_prediksi = '/static/images/iris_versicolor.jpg'
		else:
			gambar_prediksi = '/static/images/iris_virginica.jpg'
		
		# Return hasil prediksi dengan format JSON
		return jsonify({
			"prediksi": hasil_prediksi,
			"gambar_prediksi" : gambar_prediksi
		})

# @app.route("/deteksicsv", methods=['POST'])
# def deteksicsv():
# 	form = UploadFileForm()
# 	if form.validate_on_submit():
# 		file = form.file.data #mengambil file
# 		file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) #menyimpan file

# 		file_csv = pd.read_csv(file)
# 		prediksi_csv = model.predict(file_csv.iloc[:, :-1])

# 		file_csv['Species'] = prediksi_csv
# 		file_csv.to_csv('hasil.csv', index=False)

# 		return render_template('index.html', form=form)

@app.route("/deteksicsv", methods=["POST", "GET"])
def deteksicsv():
	error = None
	try:
		if request.method == 'POST':
			uploaded_df = request.files['uploaded-file']
			data_filename = secure_filename(uploaded_df.filename)
			uploaded_df.save(os.path.join(app.config['UPLOAD_FOLDER'], data_filename))
			session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], data_filename)

			data_file_path = session.get('uploaded_data_file_path', None)

			uploaded_df = pd.read_csv(data_file_path)
			prediksi_csv = model.predict(uploaded_df.iloc[:, :-1])
			uploaded_df['Species'] = prediksi_csv

			uploaded_df.to_csv(os.path.join(app.config['UPLOAD_FOLDER'],'hasil.csv'))

			# uploaded_df_html = uploaded_df.to_html()
			return render_template("download.html", tables=[uploaded_df.to_html()], titles=[''])
	except Exception as e:
		error = "File yang anda input salah."
		return render_template("index.html", error=error)

# =[Main]========================================

if __name__ == '__main__':
	
	# Load model yang telah ditraining
	model = load('model_iris_dt.model')

	# Run Flask di localhost 
	app.run(host="localhost", port=5000, debug=True)
	
	


