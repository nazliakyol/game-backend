import boto3
import io
from flask import request, Flask, jsonify, Response

s3_bucket_name = "nnaest"
s3 = boto3.Session(profile_name='avatars3').client('s3')

app = Flask(__name__)

#add avatar
@app.route("/users/<user_id>/avatar", methods = ["POST"])
def addAvatar(user_id):
    file = request.files['file']
    file_contents = io.BytesIO(file.read())
    # TODO make sure it is a png file
    s3.upload_fileobj(file_contents, s3_bucket_name, f'{user_id}.png')

    return jsonify({"message": "File uploaded successfully"})


#get avatar
@app.route("/users/<user_id>/avatar", methods = ["GET"])
def getAvatar(user_id):
    try:
        s3_object = s3.get_object(Bucket=s3_bucket_name, Key=f'{user_id}.png')
        file_contents = s3_object['Body'].read()
        return Response(file_contents, mimetype='image/x-png')
    except:
        return jsonify({"message": "File not found"})

if __name__ == '__main__':
    app.run(debug=True, port=5002)

