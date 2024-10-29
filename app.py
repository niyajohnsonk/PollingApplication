import os.path #to check is certain files exist already
import pandas as pd
from flask import Flask, render_template,redirect,request,url_for,make_response

app=Flask(__name__,template_folder="templates")
#storing all the required data into a csv file by first 
#storing it into a simple dictionary and then using pandas to put it into a database

if not os.path.exists("polls.csv"): #if such a path doesn't exist, make one first
    structure={
        "poll_id":[], 
        "poll":[],
        "option1":[],
        "option2":[],
        "option3":[],
        "votes1":[],
        "votes2":[],
        "votes3":[],
    }

    pd.DataFrame(structure).set_index("poll_id").to_csv("polls.csv") #to convert data to dataframe into polls.csv

polls_df=pd.read_csv("polls.csv").set_index(poll_"id")



#one endpoint:  It is typically a uniform resource locator (URL) that
# provides the location of a resource on the server
@app.route("/") #default url
def index():
    return render_template("index.html",polls=polls_df)

#another endpoint
@app.route("/polls/<poll_id>") #eg: mypolling.com/polls/2 -leading people to poll number 2
def polls(poll_id):
    poll=polls_df.loc[int(poll_id)]
    return render_template("showpoll.html",poll=poll)

#endpoint
@app.route("/polls", methods=["GET", "POST"]) #depending on get or post, the responses will be different
def create_poll():
    if request.method=="GET":
        return render_template("newpoll.html")
    elif request.method=="POST":
        poll=request.form['poll']
        option1=request.form['option1']
        option2=request.form['option2']
        option3=request.form['option3']
        polls_df.loc[max(polls_df.index.values) +1]= [poll, option1, option2, option3, 0, 0, 0]
        polls_df.to_csv("polls.csv")
        return redirect(url_for("index"))


#endpoint
@app.route("/vote/<poll_id>/<option>")
def vote(poll_id,option):
    if request.cookies.get(f"vote_{poll_id}_cookie") is None:
        polls_df.at[int(poll_id), "votes"+str(option)]+=1
        polls_df.to_csv("polls.csv")
        response=make_response(redirect(url_for("polls",poll_id=poll_id)))
        response.set_cookie(f"vote_{poll_id}_cookie",str(option))
        return response
    else:
        return "Cannot vote more than once."




if __name__=="__main__": #to run everything
    app.run(host="localhost", debug=True)
