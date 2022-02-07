from flask import Flask,render_template,request,jsonify,send_file,redirect
import uuid
import os

app=Flask(__name__,static_folder="static",template_folder="templates")
IN_MEMORY_STORAGE = {}

@app.route('/data',methods=['POST'])
def handle_data():
    try:
        image=request.files['image']
        segment=request.files['segment']

        uid=uuid.uuid4()
        image_path=os.path.join(os.path.dirname(os.path.realpath(__file__)) ,"static","images", str(uid)+'.png')
        segment_path=os.path.join(os.path.dirname(os.path.realpath(__file__)) ,"static","images", str(uid)+'_segmented.png')

        image.save(image_path)
        segment.save(segment_path)

    except Exception as e:
        return str(e)
    return jsonify({"id":str(uid)})


@app.route('/wildfire',methods=['GET'])
def index():
    try:
        ID=request.args.get('id')
        datetime=request.args.get('datetime')
        latitude=request.args.get('latitude')
        longitude=request.args.get('longitude')
        image_path=str(ID)+'.png'
        segment_path=str(ID)+'_segmented.png'
    except Exception as e:
        return str(e)
    return render_template('index.html',image=image_path,segment=segment_path,datetime=datetime,latitude=latitude,longitude=longitude)


# This assumed to be special api endpoint that
# returns satellite imagenery based on center coordinates
# provided.

@app.route("/getphoto",methods=['GET'])
def getPhoto():
    # neglect coordinates send static image as response
    return send_file(os.path.join(os.path.dirname(os.path.realpath(__file__)) ,"static","images",'wildfire.png'),mimetype='image/jpg')



# In order to send urls via SMS we need to set shortener service 

@app.route("/urlshortener",methods=['POST',"GET"])
def urlshortener():
    try:
        if request.method=='POST':
            ID=len(IN_MEMORY_STORAGE)
            url=request.args.get('url')
            IN_MEMORY_STORAGE[str(ID)]=url
            return jsonify({"id":str(ID)})
        if request.method=='GET':
            ID=request.args.get('id')
            return redirect(IN_MEMORY_STORAGE[ID],code=302)
    except Exception as e:
        return str(e)


if __name__=="__main__":
    app.run("0.0.0.0",port=80,debug=False)
