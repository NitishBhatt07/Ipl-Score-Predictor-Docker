from flask import Flask ,request,render_template
import joblib
import pandas as pd

app = Flask(__name__)

model = joblib.load(open('Ipl_randomforest_model.pkl','rb')) 

df = pd.read_csv('last_csv_data.csv')
batting_teams_list = df['batting_team'].unique()
bowling_teams_list = df['bowling_team'].unique()
city_list = df['city'].unique()


@app.route('/')
def hello_world():
    return render_template("main_page.html")


@app.route('/predict_api',methods=['GET', 'POST'])
def predict_score_api():
    bat_team = request.args.get('batting_team')
    bowl_team = request.args.get('bowling_team')
    city = request.args.get('city')
    current_score = request.args.get('current_score')
    ball_left = request.args.get('ball_left')
    wicket_left = request.args.get('wicket_left')
    current_run_rate = request.args.get('current_run_rate')
    last_five = request.args.get('last_five')

    current_score = int(current_score)
    ball_left = int(ball_left)
    wicket_left = (wicket_left)
    current_run_rate = float(current_run_rate)
    last_five = float(last_five)

    df_to_pred = pd.DataFrame([[bat_team,bowl_team,city,current_score,
    ball_left,wicket_left,current_run_rate,last_five]],
    columns=['batting_team', 'bowling_team', 'city', 'current_score', 'balls_left',
    'wicket_left', 'crr', 'last_five'])

    predication = model.predict(df_to_pred)

    return "The Score is "+str(predication[0])

    #return bat_team+"\t"+bowl_team+"\t"+city+"\t"+str(current_score)+"\t"+str(ball_left)+"\t"+str(wicket_left)+"\t"+str(current_run_rate)+"\t"+str(last_five)
    

@app.route('/predict',methods=['GET', 'POST'])
def predict_score():

    predication = "0"
    bat_team = ""
    bowl_team = ""
    city = ""
    current_score = 0
    ball_left = 0
    wicket_left = 0
    current_run_rate = 0.0
    last_five = 0
    
    if request.method == "POST":        

        bat_team = request.form['batting_team']
        bowl_team = request.form['bowling_team']
        city = request.form['city']
        current_score = request.form['current_score']
        ball_left = request.form['ball_left']
        wicket_left = request.form['wicket_left']
        current_run_rate = request.form['current_run_rate']
        last_five = request.form['last_five']
    
        current_score = int(current_score)
        ball_left = int(ball_left)
        wicket_left = (wicket_left)
        current_run_rate = float(current_run_rate)
        last_five = float(last_five)
        
        df_to_pred = pd.DataFrame([[bat_team,bowl_team,city,current_score,
        ball_left,wicket_left,current_run_rate,last_five]],
        columns=['batting_team', 'bowling_team', 'city', 'current_score', 'balls_left',
        'wicket_left', 'crr', 'last_five'])

        predication = model.predict(df_to_pred)
        predication=  str(predication[0]).split(".")[0]  


    return render_template('index.html',predication=predication,batting_teams_list=batting_teams_list,bowling_teams_list=bowling_teams_list,city_list=city_list)
 
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='3000')