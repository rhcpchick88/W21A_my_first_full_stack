from flask import Flask, request, Response, jsonify
from helpers.dbhelpers import run_query

app = Flask(__name__)

import sys

@app.get('/api/blog_posting')
def get_post():
    post_list= run_query("SELECT * FROM blog_posts")
    resp = []
    for post in post_list:
        post_obj= {}
        post_obj["postId"] = post[0]
        post_obj["postText"] = post[1]
        resp.append(post_obj)
    return jsonify(post_list), 200





if (len(sys.argv)>1):
    mode = sys.argv[1]
else:
    print("No mode argument, must pass a mode")
    exit()
    
if mode == "testing":
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
elif mode == "production":
    import bjoern
    print("Running in production mode!")
    bjoern.run(app, "0.0.0.0", 5000)
else:
    print("Invalid mode, must be one of: testing|production")
    exit() 

app.run(debug=True)