
import numpy as np
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort


app = Flask(__name__)
api = Api(app)

#DB SIZE LIMITATIONs
LIMITATION = 10000
PORT = 5000

#POST arguments
person_post_args = reqparse.RequestParser()
person_post_args.add_argument("name", type=str, required=True,  help="name of the person")
person_post_args.add_argument("features", action='append', required=True, help="person features vector")

#GET arguments
person_get_args = reqparse.RequestParser()
person_get_args.add_argument("features", action='append', required=True, help="person features vector")

persons_data = {}

def get_norm(vec):
    norm = np.linalg.norm(vec)
    return vec / norm

def get_closest(db, input_person):
    #print(f"DB BEFORE REMOVE: {db}")
    res = []
   # tmp_db = {key:val for key, val in db.items() if val != input_person}
    #print(f"DB AFTER REMOVE: {tmp_db}")
    for name, feature in db.items():
        feature = np.array(feature).astype(np.float)
        if np.array_equal(feature,input_person):
            continue
      #  print('KEY', name)
     #   print('VAL == INPUT' , feature, input_person)
        try:
            #normalize the vectors
            norm_vec = list(map(get_norm, [feature, input_person]))
            res.append({"name" :  name, "distance": np.dot(norm_vec[0], norm_vec[1])})
           # print(f'cheching dot product between seatch: {input_person} and db feature {feature}')
           # res.append({"name": name, "distance": np.dot(input_person, feature)})
          #  print(f'results is : {np.dot(input_person, feature)}')
        except Exception as e:
            print(e)
            abort(500, message = "[ERROR] calculating closest person")
    top_3 = sorted(res, key=lambda d: d['distance'], reverse=True)[:3]
  #  print(f"top 3 are: {top_3}")
   # print(db[name])
   # print([(d['name'], d['distance']) for d in top_3])
    return [(d['name'], db[name]) for d in top_3]

def is_not_in_db(name):
    if name not in persons_data:
        abort(404, message = f"name: {name} was not found in DB")

def person_exist(name):
    if name in persons_data:
        abort(409, message = f"Features for 'name': {name} already exists in DB")


def limitation():
    if len(persons_data) > LIMITATION:
        return True


class Person(Resource):
    def get(self, name):
        args = person_get_args.parse_args()
        nparray = np.array(args['features']).astype(np.float)
        res = get_closest(persons_data, nparray)
        return {'SUCESS' :  res}

    def post(self, name):
        try:
            args = person_post_args.parse_args()
            #check 10K limitation
            if limitation():

                return 'DB IS FULL', 403

            name = args["name"]
            # check if person already exist in DB
            person_exist(name)
            features = args["features"]
            persons_data[name] = features
            return 'SUCESS', 201
        except:
            return 'FAIL', 400


    def delete(self, name):
        is_not_in_db(name)
        del persons_data[name]
        # Deleted succesfully 
        return '', 204


api.add_resource(Person, "/person/<string:name>")


if __name__ == "__main__":
	app.run(debug=True)
    #app.run(debug=True, host="0.0.0.0")
   # app.run(host="0.0.0.0", port=PORT)