from flask import Flask, render_template, redirect, request
import joblib
import numpy as np
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.express as px
negative={}
app = Flask(__name__)
dict={"Low":0,"Medium":0,"High":0}
user_data = {"level1": {}, "level2": {}, "level3": {}, "final": {}}
Level={}
@app.route("/")
def home():
    global dict,user_data
    dict={"Low":0,"Medium":0,"High":0}
    user_data = {"level1": {}, "level2": {}, "level3": {}, "final": {}}
    return redirect("https://safepath4t.my.canva.site/")

@app.route("/start", methods=["POST", "GET"])
def fun1():
    if request.method == 'POST':
        try:
            age = int(request.form["age"])
            gender = request.form["gender"]
            family_history = request.form["family_history"]
            smoking = request.form["smoking"]
            alcohol = request.form["alcohol"]
            activity = int(request.form["activity"])
            diet = int(request.form["diet"])
            weight_loss = int(request.form["weight_loss"])
            fatigue = int(request.form["fatigue"])
            pain = int(request.form["pain"])
            user_data['level1'] = {
                "Age": age, "Gender": gender, "Family History": family_history,
                "Smoking": smoking, "Alcohol": alcohol, "Activity": activity,
                "Diet": diet, "Weight Loss": weight_loss, "Fatigue": fatigue, "Pain": pain
            }
            risk_score = 0 
            if(family_history==1):
                risk_score+=0.25
                negative["family"] = "Family History consists of Cancer !!! Maintain your health and take care."
            if(smoking =='Former'):
                risk_score+=0.5
                negative["smoking"] = "Patient can show slight potential in reducing Smoke"
            if(smoking=='Current'):
                risk_score+=0.7
                negative["smoking"] = "Patient must show high potential in reducing Smoke"
            if(alcohol=='Frequent'):
                risk_score+=0.5
                negative["drinking"] = "Patient must show high potential in reducing Smoke"
            if(alcohol=='Occasional'):
                risk_score+=0.4
            if(activity>=3 and activity<=6):
                risk_score+=0.5
                negative["activity"] = "Patient can slightly increase his physical activity level"
            if(activity<3):
                risk_score+=0.7
                negative["activity"] = "Patient must increase his physical activity level"
            if(diet<=3):
                risk_score+=0.4
                negative["diet"] = "Patient must maintain proper diet or else it definitely leads to severe health loss."
            if(diet>3 and diet<=6):
                risk_score+=0.2
                negative["diet"] = "Patient must maintain proper diet."
            if(weight_loss>=7 and weight_loss<=9):
                risk_score+=0.5
                negative["loss"] = "Weight loss might indicate abnormality"
            if(weight_loss>=10):
                negative["loss"] = "Weight loss is the strong indicator for abnormality"
                risk_score+=0.8
            if(weight_loss>=7):
                risk_score+=0.8
            if(fatigue>=4 and fatigue<=7):
                risk_score+=0.4
                negative["fatigue"] = "Fatigue might have Chance of low risk cancer"
            if(fatigue>7):
                risk_score+=0.5
                negative["fatigue"] = "Fatigue might have Chance of medium risk cancer"
            if(pain>=4 and pain<=7):
                negative["pain"] = "Patient's Chronic pain level indicates medium risk"
                risk_score+=0.4
            if(pain>7):
                negative["pain"] = "Patient's Chronic pain level indicates high risk"
                risk_score+=0.5
            if(risk_score>=0 and risk_score<=2.34):
                Level[1]="Level 1 : Predicted Low Risk"
                dict["Low"]+=1
            elif(risk_score>=2.34 and risk_score<=3.4):
                Level[1]="Level 1 : Predicted Medium Risk"
                dict["Medium"]+=1
            else:
                Level[1]="Level 1 : Predicted High Risk"
                dict["High"]+=1
            return redirect("/level2")
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return render_template("level1.html")




@app.route("/level2",methods=["POST","GET"])
def fun2():
    if request.method == 'POST':
        risk_score=0
        history_disease = int(request.form["history_disease"])
        past_cancer = int(request.form["past_cancer"])
        family_history = int(request.form["family_history"])
        cough_duration = int(request.form["cough_duration"])
        bleeding = int(request.form["bleeding"])
        lymph_nodes = int(request.form["lymph_nodes"])
        infections = int(request.form["infections"])
        radiation = int(request.form["radiation"])
        hazard_exposure = int(request.form["hazard_exposure"])
        inflammation = int(request.form["inflammation"])
        immunity = int(request.form["immunity"])
        
        if(history_disease==2):
            risk_score+=0.4
            negative["history"] = "Chronic diseases might effect the probability"
        if(history_disease==3):
            risk_score+=0.6
            negative["history"] = "Chronic diseases will effect the probability"       
        if(past_cancer==1):
            risk_score+=0.5
            negative["pastcancer"] = "Past cancer cell growth might effect"
        if(past_cancer==2):
            risk_score+=0.3
            negative["pastcancer"] = "Past cancer cell growth might start"
        if(family_history==3):
            risk_score+=0.5
        if(family_history==2):
            risk_score+=0.3
        if(cough_duration>=7):
            risk_score+=1.3
            negative["coughdur"] = "Persistant cough strongly indicates abnormality"
        if(cough_duration>=4 and cough_duration<=6):
            negative["coughdur"] = "Persistant cough moderately indicates abnormality"      
            risk_score+=0.8
        if(bleeding==3):
            risk_score+=0.9
            negative["bleeding"] = "Bleeding indicates abnormality"      
        if(bleeding==2):
            negative["bleeding"] = "Bleeding moderately indicates abnormality"      
            risk_score+=0.4
        if(lymph_nodes>=4):
            risk_score+=0.9
            negative["lymph"] = "Lymph more than 4 weeks is a sure shot symptom."      
        if(lymph_nodes>=2 and lymph_nodes<4):
            risk_score+=0.7
            negative["lymph"] = "Lymph might indicate cancer"      
        if(infections>=6):
            risk_score+=1.3
        if(infections>=3 and infections<6):
            risk_score+=0.9
        if(radiation==3):
            risk_score+=0.3
        if(radiation==2):
            risk_score+=0.1
        if(hazard_exposure==3):
            risk_score+=0.3
        if(hazard_exposure==2):
            risk_score+=0.1
        if(inflammation==1):
            risk_score+=0.5
        if(inflammation==2):
            risk_score+=0.3
        if(immunity==3):
            risk_score+=0.3
        if(immunity==2):
            risk_score+=0.1
        if(risk_score>=0 and risk_score<=3.4):
            Level[2]="Level 2 : Predicted Low Risk"
            dict["Low"]+=1
        elif(risk_score>3.4 and risk_score<4.5):
            Level[2]="Level 2 : Predicted Medium Risk"
            dict["Medium"]+=1
        else:
            Level[2]="Level 2 : Predicted High Risk"
            dict["High"]+=1
        return redirect("/step3")
    return render_template("level2.html")



@app.route("/step3", methods=["POST", "GET"])
def fun3():
    if request.method == 'POST':
        risk_score=0
        night_sweats = int(request.form["night_sweats"])
        body_swelling = int(request.form["body_swelling"])
        physical_activity = int(request.form["physical_activity"])
        sleep_quality = int(request.form["sleep_quality"])
        sleep_duration = float(request.form["sleep_duration"])
        smoking_change = int(request.form["smoking_change"])
        alcohol_change = int(request.form["alcohol_change"])
        body_odor = int(request.form["body_odor"])
        taste_sensation = int(request.form["taste_sensation"])
        smell_sensation = int(request.form["smell_sensation"])
        memory_problems = int(request.form["memory_problems"])
        mood_swings = int(request.form["mood_swings"])
        difficulty_concentrating = int(request.form["difficulty_concentrating"])
        anxiety_stress = int(request.form["anxiety_stress"])
        loss_interest = int(request.form["loss_interest"])
        if(night_sweats==3):
            risk_score+=0.5
        if(night_sweats==2):
            risk_score+=0.3
        if(body_swelling==1):
            risk_score+=0.5
            negative["swelling"] = "Body Swelling is not considered as a healthy body."
        if(sleep_quality==3):
            risk_score+=0.5
            negative["sleep"] = "Sleeping cycle also impacts mental health and might cause cancer cells grow"
        if(sleep_quality==2):
            risk_score+=0.3
            negative["sleep"] = "Suggested to sleep well."
        if(sleep_duration<=4):
            risk_score+=0.2
        if(smoking_change==3):
            risk_score+=0.4
        if(smoking_change==2):
            risk_score+=0.1
        if(alcohol_change==3):
            risk_score+=0.4
        if(alcohol_change==2):
            risk_score+=0.1
        if(body_odor==1):
            risk_score+=0.4
            negative["body"] = "Bad body odor is a indication of some illness"
        if(taste_sensation==1):
            risk_score+=0.4
        if(smell_sensation==1):
            risk_score+=0.4
        if(memory_problems==1):
            risk_score+=0.4
        if(risk_score>=0 and risk_score<1):
            dict["Low"]+=1
            Level[3]="Level 3 : Predicted Low Risk"
        elif(risk_score>=1 and risk_score<3.1):
            dict["Medium"]+=1
            Level[3]="Level 3 : Predicted Medium Risk"
        else:
            dict["High"]+=1
            Level[3]="Level 3 : Predicted High Risk"
        return redirect("/final")
    return render_template("level3.html")






@app.route("/final", methods=["POST", "GET"])
def fun4():
    if request.method == "POST":
        risk_score=0
        weight_loss = int(request.form["weight_loss"])
        fatigue = int(request.form["fatigue"])
        bleeding = int(request.form["bleeding"])
        lumps = int(request.form["lumps"])
        cough = int(request.form["cough"])
        breathlessness = int(request.form["breathlessness"])
        pain = int(request.form["pain"])
        skin_changes = int(request.form["skin_changes"])
        if(weight_loss==1):
            risk_score+=0.8
        if(fatigue==1):
            risk_score+=0.8
        if(bleeding==1):
            risk_score+=0.8
        if(lumps==1):
            risk_score+=0.8
        if(cough==1):
            risk_score+=0.8
        if(breathlessness==1):
            risk_score+=0.8
        if(pain==1):
            risk_score+=0.8
        if(skin_changes==1):
            risk_score+=0.8
        if(risk_score<=2.4):
            dict["Low"]+=1
            Level[4]="Level 4 : Predicted Low Risk"
        elif(risk_score>2.4 and risk_score<=3.2):
            dict["Medium"]+=1
            Level[4]="Level 4 : Predicted Medium Risk"
        else:
            dict["High"]+=1
            Level[4]="Level 4 : Predicted High Risk"
        return redirect("/club_result")
    return render_template("final.html")



@app.route("/club_result")
def club_result():
    lowcount = dict["Low"]
    highcount = dict["High"]
    mediumcount = dict["Medium"]

    # Calculate total reports
    total_reports = lowcount + highcount + mediumcount


    return render_template(
        "club_result.html",
        total=total_reports,
        low=lowcount,
        medium=mediumcount,
        high=highcount,
        level = Level,
        negative = negative
    )


app.run(port=7334,debug=True)            
            
            
            
            
        
