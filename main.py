#from typing_extensions import Required
import numpy as np
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
api = Api(app)



person_post_args = reqparse.RequestParser()
person_post_args.add_argument("name", type=str, required=True,  help="name of the person")
person_post_args.add_argument("features", action='append', required=True, help="person features vector")

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
            print('YOU ARE YOU, skip', name)
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
    print(f"top 3 are: {top_3}")
    print([(d['name'], d['distance']) for d in top_3])
    return [(d['name'], d['distance']) for d in top_3]

def is_not_in_db(name):
    if name not in persons_data:
        abort(404, message = f"name: {name} was not found in DB")

def person_exist(name):
    if name in persons_data:
        abort(409, message = f"Features for 'name': {name} already exists in DB")


def limitation():
    if len(persons_data) > 10000:
        abort(404, message = "[ERROR] Cannot add new person - DB is full.")

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
            limitation()
            name = args["name"]
            # check if person already exist in DB
            person_exist(name)
            features = args["features"]
            persons_data[name] = features
            return 'SUCESS', 201
        except:
            return 'FAIL', 400
        #return {"data": "Posted Hello World"} 

    def delete(self, name):
        is_not_in_db(name)
        del persons_data[name]
        # Deleted succesfully 
        return '', 204

#api.add_resource(Person, "/person")
api.add_resource(Person, "/person/<string:name>")
#args = person_post_args.parse_args()
#api.add_resource(Person, '/person',  resource_class_kwargs={ 'name': args.name, 'features': args.feature})

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db = SQLAlchemy(app)

# class VideoModel(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(100), nullable=False)
# 	views = db.Column(db.Integer, nullable=False)
# 	likes = db.Column(db.Integer, nullable=False)

# 	def __repr__(self):
# 		return f"Video(name = {name}, views = {views}, likes = {likes})"

# video_put_args = reqparse.RequestParser()
# video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
# video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
# video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)

# video_update_args = reqparse.RequestParser()
# video_update_args.add_argument("name", type=str, help="Name of the video is required")
# video_update_args.add_argument("views", type=int, help="Views of the video")
# video_update_args.add_argument("likes", type=int, help="Likes on the video")

# resource_fields = {
# 	'id': fields.Integer,
# 	'name': fields.String,
# 	'views': fields.Integer,
# 	'likes': fields.Integer
# }

# class Video(Resource):
# 	@marshal_with(resource_fields)
# 	def get(self, video_id):
# 		result = VideoModel.query.filter_by(id=video_id).first()
# 		if not result:
# 			abort(404, message="Could not find video with that id")
# 		return result

# 	@marshal_with(resource_fields)
# 	def put(self, video_id):
# 		args = video_put_args.parse_args()
# 		result = VideoModel.query.filter_by(id=video_id).first()
# 		if result:
# 			abort(409, message="Video id taken...")

# 		video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
# 		db.session.add(video)
# 		db.session.commit()
# 		return video, 201

# 	@marshal_with(resource_fields)
# 	def patch(self, video_id):
# 		args = video_update_args.parse_args()
# 		result = VideoModel.query.filter_by(id=video_id).first()
# 		if not result:
# 			abort(404, message="Video doesn't exist, cannot update")

# 		if args['name']:
# 			result.name = args['name']
# 		if args['views']:
# 			result.views = args['views']
# 		if args['likes']:
# 			result.likes = args['likes']

# 		db.session.commit()

# 		return result


# 	def delete(self, video_id):
# 		abort_if_video_id_doesnt_exist(video_id)
# 		del videos[video_id]
# 		return '', 204


#api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
	app.run(debug=True)