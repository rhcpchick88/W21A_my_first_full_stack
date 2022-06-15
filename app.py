from flask import Flask, request, jsonify
from helpers.dbhelpers import run_query

app = Flask(__name__)

import sys

# the get requests returns the database data as an array and tells 
# the location in the array for each variable
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

# basic post request using only post text as id does not matter for input.
@app.post('/api/blog_posting')
def blog_post():
    data = request.json
    post_text=data.get("postText")
    if not post_text:
        return jsonify("Missing required argument 'postText'"), 422
    run_query("INSERT INTO blog_posts (text) VALUES (?)", [post_text])
    return jsonify("Blog post added"), 201

# basic delete request, using the post id as an argument.
@app.delete('/api/blog_posting')
def blog_delete():
    data = request.json
    post_id = data.get("postId")
    run_query("DELETE FROM blog_posts WHERE id=?", [post_id])
    return jsonify("Post successfully deleted"), 201

# patch request using both post id and post text as arguments, to update info.
@app.patch('/api/blog_posting')
def blog_update():
    data = request.json
    post_text = data.get("postText")
    post_id = data.get("postId")
    if not post_text:
        return jsonify("Missing required argument 'postText'"),422
    run_query("UPDATE blog_posts SET text=? WHERE id=?", [post_text, post_id])
    return jsonify("Blog post updated"),201

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