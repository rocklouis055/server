from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify,request
from time import time
import pandas as pd
import glob
import requests
from flask_cors import CORS
import numpy as np
d=pd.DataFrame()

def init():
    global d
    for i in glob.glob("*.csv"):
        print("Loading",i)
        d=pd.concat([d,pd.read_csv(i,lineterminator='\n',index_col="Unnamed: 0",low_memory=False).transpose()])
    d=d.replace(to_replace = np.nan, value ="Not Available")
def sensor():
    print("Scheduler is alive!")

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',minutes=600)
sched.start()

app = Flask(__name__)
CORS(app)
@app.route("/api/movie",methods=['GET'])
def get_movie():
    print(request.args)
    k={}
    t=[]
    if 'video' in request.args and 'id' in request.args:
        id=request.args['id']
        """
        <iframe width="919" height="517" src="https://www.youtube.com/embed/hXCCYS_5Unc" title="Rosa Linn - Snap (Lyrics)" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        """
        # https://api.themoviedb.org/3/movie/550/videos?api_key=f402763558fa01cd47786609b9177842
        # print("https://api.themoviedb.org/3/movie/"+id+"/videos?api_key=f402763558fa01cd47786609b9177842")
        
        s=requests.get(url = "https://api.themoviedb.org/3/movie/"+id+"/videos?api_key=f402763558fa01cd47786609b9177842").json()
        key=s['results'][0]['key']
        n=s['results'][0]['name']
        b="""<html>
<body>

<iframe width="1280" height="720" src="https://www.youtube.com/embed/"""+key+"""">
</iframe>

</body>
</html>"""
        print(b)
        return(b)
    if "start" in request.args and "end" in request.args:
        # return("hello")
        start=int(request.args['start'])
        end=min(len(d),int(request.args['end']))
        # print(start,end)
        for i in range(start,end):
            k={}
            # print(d.iloc[i])
            k['id']=d.iloc[i]['id']
            if str(d.iloc[i]['poster_path'])!="Not Available":
                k['poster']="https://image.tmdb.org/t/p/original"+str(d.iloc[i]['poster_path'])
            else:
                k['poster']="https://www.movienewz.com/img/films/poster-holder.jpg"
            k['title']=d.iloc[i]['original_title']
            k['year']=d.iloc[i]['release_date']
            k['rating']=d.iloc[i]['vote_average']
            t.append(k)
        # print(t)
        return(jsonify(t))
    if 'id' in request.args:
        id = request.args['id']
    else:
        return("Error:No id is there")
    if id in d.index:
        k['id']=id
        k['poster']="https://image.tmdb.org/t/p/original"+d.loc[id]['poster_path']
        k['title']=d.loc[id]['original_title']
        k['year']=d.loc[id]['release_date']
        k['rating']=d.loc[id]['vote_average']
    else:
        return("Wrong ID")
    return jsonify(k)
@app.route("/api/update",methods=['GET'])
def update():
    print(request.args)
    global d
    if "show" in request.args:
        return("hello")
        return(glob.glob("*"))
    if "file" in request.args:
        print(request.args["file"],request.args['file'] in glob.glob("*"))
        if request.args['file'] in glob.glob("*"):
            print("loading")
            d=pd.concat([d,pd.read_csv(request.args['file'],lineterminator='\n',index_col="Unnamed: 0",low_memory=False).transpose()])
            print("Loaded file "+request.args['file'])
            return("Loaded file "+request.args['file'])
        else:
            return("Not available")   
if __name__ == "__main__":
    # init()
    app.run(host="0.0.0.0")
