from training_model import Train_Model
from prediction_model import Predict_Model
from training_insertion import Train_Insertion
from prediction_insertion import Predict_Insertion
from wsgiref import simple_server
from flask import Flask, request, render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin
import flask_monitoringdashboard as dashboard
import json

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRouteClient():
    try:
        if request.form is not None:
            
            path = request.form['filepath']

            pred_val = Predict_Insertion()  # object initialization

            pred_val.Insertion()  # calling the prediction_validation function

            pred = Predict_Model()  # object initialization

            # predicting for dataset present in database
            json_predictions = pred.model_prediction()
            return Response(f"Cost is: \n {str(json.loads(json_predictions))}")

        else:
            print('Nothing Matched')
    except ValueError:
        return Response(f"Error Occurred! {ValueError}")
    except KeyError:
        return Response(f"Error Occurred! {KeyError}")
    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.route("/train", methods=['GET', 'POST'])
@cross_origin()
def trainRouteClient():
    try:
        folder_path = "training_batch_file"
        if folder_path is not None:
            path = folder_path

            train_ins = Train_Insertion()  # object initialization

            train_ins.Insertion()  # calling the training_validation function

            train_model = Train_Model()  # object initialization

            train_model.model_training()  # training the model for the files in the table

    except ValueError:

        return Response(f"Error Occurred! {ValueError}")

    except KeyError:

        return Response(f"Error Occurred! {KeyError}")

    except Exception as e:

        return Response(f"Error Occurred! {e}")

    return Response("Training successful!")


port = int(os.getenv("PORT", 5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    # port = 5000
    httpd = simple_server.make_server(host, port, app)
    # print("Serving on %s %d" % (host, port))
    httpd.serve_forever()