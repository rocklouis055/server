# from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify,request
from time import time
import pandas as pd
import glob
d=pd.DataFrame()

def init():
    global d
    print(glob.glob("*"))
    for i in glob.glob("*.csv"):
        print(i)
        d=pd.concat([d,pd.read_csv(i,lineterminator='\n',index_col="Unnamed: 0").transpose()])

# def sensor():
#     print("Scheduler is alive!")

# sched = BackgroundScheduler(daemon=True)
# sched.add_job(sensor,'interval',minutes=600)
# sched.start()

app = Flask(__name__)

@app.route("/api/movie",methods=['GET'])
def get_movie():
    print(request.args)
    k={}
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

if __name__ == "__main__":
    init()
    app.run()
