from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
# Create your views here.
from Remote_User.models import ClientRegister_Model,predict_cyber_attack,detection_ratio,detection_accuracy

def login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def logout(request):
    request.session.flush()
    return redirect('index')

def index(request):
    return render(request, 'RUser/index.html')

def Add_DataSet_Details(request):

    return render(request, 'RUser/Add_DataSet_Details.html', {"excel_data": ''})


def Register1(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city,address=address,gender=gender)

        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html',{'object':obj})
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    if 'userid' not in request.session:
        return redirect('login')
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def Prediction_Of_Cyber_Attack_Type(request):
    if 'userid' not in request.session:
        return redirect('login')
    if request.method == "POST":

        if request.method == "POST":

            Fid=request.POST.get('Fid')
            Timestamp=request.POST.get('Timestamp')
            Source_IP_Address=request.POST.get('Source_IP_Address')
            Destination_IP_Address=request.POST.get('Destination_IP_Address')
            Source_Port=request.POST.get('Source_Port')
            Destination_Port=request.POST.get('Destination_Port')
            Protocol=request.POST.get('Protocol')
            Packet_Length=request.POST.get('Packet_Length')
            Packet_Type=request.POST.get('Packet_Type')
            Traffic_Type=request.POST.get('Traffic_Type')
            Alerts_Warnings=request.POST.get('Alerts_Warnings')
            Action_Taken=request.POST.get('Action_Taken')
            Severity_Level=request.POST.get('Severity_Level')
            Device_Information=request.POST.get('Device_Information')
            Network_Segment=request.POST.get('Network_Segment')
            Geolocation_Data=request.POST.get('Geolocation_Data')
            ProxyInformation=request.POST.get('ProxyInformation')
            FirewallLogs=request.POST.get('FirewallLogs')
            IDS_IPS_Alerts=request.POST.get('IDS_IPS_Alerts')
            Log_Source=request.POST.get('Log_Source')



        import joblib
        import os
        import numpy as np

        model_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        classifier = joblib.load(os.path.join(model_dir, 'cyber_model.pkl'))
        scaler = joblib.load(os.path.join(model_dir, 'scaler.pkl'))
        selector = joblib.load(os.path.join(model_dir, 'selector.pkl'))
        le_protocol = joblib.load(os.path.join(model_dir, 'le_protocol.pkl'))
        le_severity = joblib.load(os.path.join(model_dir, 'le_severity.pkl'))
        le_device = joblib.load(os.path.join(model_dir, 'le_device.pkl'))
        le_sip = joblib.load(os.path.join(model_dir, 'le_sip.pkl'))
        le_dip = joblib.load(os.path.join(model_dir, 'le_dip.pkl'))
        le_geo = joblib.load(os.path.join(model_dir, 'le_geo.pkl'))
        le_traffic = joblib.load(os.path.join(model_dir, 'le_traffic.pkl'))

        try:
            proto_val = le_protocol.transform([str(Protocol).strip().upper()])[0]
        except ValueError:
            proto_val = 0
            
        try:
            sev_val = le_severity.transform([str(Severity_Level).strip().title()])[0]
        except ValueError:
            sev_val = 0
            
        try: device_val = le_device.transform([str(Device_Information).strip()])[0]
        except ValueError: device_val = 0
        
        try: sip_val = le_sip.transform([str(Source_IP_Address).strip()])[0]
        except ValueError: sip_val = 0
        
        try: dip_val = le_dip.transform([str(Destination_IP_Address).strip()])[0]
        except ValueError: dip_val = 0
        
        try: geo_val = le_geo.transform([str(Geolocation_Data).strip()])[0]
        except ValueError: geo_val = 0
        
        try: traf_val = le_traffic.transform([str(Traffic_Type).strip().upper()])[0]
        except ValueError: traf_val = 0
            
        try:
            features_raw = np.array([[int(str(Source_Port).strip()), int(str(Destination_Port).strip()), int(str(Packet_Length).strip()), proto_val, sev_val, device_val, sip_val, dip_val, geo_val, traf_val]])
        except ValueError:
             features_raw = np.array([[0, 0, 0, proto_val, sev_val, device_val, sip_val, dip_val, geo_val, traf_val]])

        features_scaled = scaler.transform(features_raw)
        features = selector.transform(features_scaled)

        probabilities = classifier.predict_proba(features)
        confidence = round(max(probabilities[0]) * 100, 2)
        prediction = classifier.predict(features)[0]

        if (prediction == 0):
            val = 'DDoS'
        else:
            val = 'Malware'

        val_with_confidence = f"{val} ({confidence}% Confidence)"

        print(val_with_confidence)

        # Explainable AI (SHAP) Logic
        import shap
        import pandas as pd
        
        df_bg = pd.read_csv(os.path.join(model_dir, 'Datasets.csv'), encoding='latin-1')
        # Skip unseen labels for transform by applying lambda or ignoring if background is clean
        # But since Datasets.csv matches exactly, we can transform
        df_bg['Protocol'] = le_protocol.transform(df_bg['Protocol'].astype(str))
        df_bg['Severity_Level'] = le_severity.transform(df_bg['Severity_Level'].astype(str))
        df_bg['Device_Information'] = le_device.transform(df_bg['Device_Information'].astype(str))
        df_bg['Source_IP_Address'] = le_sip.transform(df_bg['Source_IP_Address'].astype(str))
        df_bg['Destination_IP_Address'] = le_dip.transform(df_bg['Destination_IP_Address'].astype(str))
        df_bg['Geolocation_Data'] = le_geo.transform(df_bg['Geolocation_Data'].astype(str))
        df_bg['Traffic_Type'] = le_traffic.transform(df_bg['Traffic_Type'].astype(str))
        
        X_bg_raw = df_bg[['Source_Port', 'Destination_Port', 'Packet_Length', 'Protocol', 'Severity_Level', 'Device_Information', 'Source_IP_Address', 'Destination_IP_Address', 'Geolocation_Data', 'Traffic_Type']].sample(50, random_state=42)
        X_bg_scaled = scaler.transform(X_bg_raw)
        X_bg = selector.transform(X_bg_scaled)
        
        explainer = shap.KernelExplainer(classifier.predict_proba, X_bg)
        # Suppress show_progress 
        shap_values = explainer.shap_values(features, silent=True)
        
        pred_class_idx = int(prediction)
        
        if isinstance(shap_values, list):
            class_shap_values = shap_values[pred_class_idx][0]
        else:
            # If it returns a single array
            if len(shap_values.shape) == 3:
                # SHAP returns (n_samples, n_features, n_classes)
                class_shap_values = shap_values[0, :, pred_class_idx]
            else:
                class_shap_values = shap_values[0]

        feature_names_full = np.array(['Source Port', 'Destination Port', 'Packet Length', 'Protocol', 'Severity Level', 'Device Information', 'Source IP', 'Dest IP', 'Geolocation', 'Traffic Type'])
        feature_names = feature_names_full[selector.get_support()]
        
        shap_data = []
        for i in range(len(feature_names)):
            shap_data.append({
                'feature': feature_names[i],
                'value': float(abs(class_shap_values[i])),
                'raw_value': float(class_shap_values[i])
            })
        shap_data = sorted(shap_data, key=lambda x: x['value'], reverse=True)

        predict_cyber_attack.objects.create(
        Fid=Fid,
        Timestamp=Timestamp,
        Source_IP_Address=Source_IP_Address,
        Destination_IP_Address=Destination_IP_Address,
        Source_Port=Source_Port,
        Destination_Port=Destination_Port,
        Protocol=Protocol,
        Packet_Length=Packet_Length,
        Packet_Type=Packet_Type,
        Traffic_Type=Traffic_Type,
        Alerts_Warnings=Alerts_Warnings,
        Action_Taken=Action_Taken,
        Severity_Level=Severity_Level,
        Device_Information=Device_Information,
        Network_Segment=Network_Segment,
        Geolocation_Data=Geolocation_Data,
        ProxyInformation=ProxyInformation,
        FirewallLogs=FirewallLogs,
        IDS_IPS_Alerts=IDS_IPS_Alerts,
        Log_Source=Log_Source,
        Prediction=val)

        context = {
            'objs': val_with_confidence,
            'shap_data': shap_data,
            'prediction_type': val
        }
        return render(request, 'RUser/Prediction_Of_Cyber_Attack_Type.html', context)
    return render(request, 'RUser/Prediction_Of_Cyber_Attack_Type.html')


def provider_home(request):
    return render(request, 'RUser/provider_home.html')
