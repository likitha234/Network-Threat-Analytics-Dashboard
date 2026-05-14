
from django.db.models import  Count, Avg
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import Q
import datetime
import xlwt
from django.http import HttpResponse


import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

# Create your views here.
from Remote_User.models import ClientRegister_Model,predict_cyber_attack,detection_ratio,detection_accuracy
from Service_Provider.models import ServiceProvider_Model


from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def serviceproviderlogin(request):
    if request.method  == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin.lower() == "admin" and password.lower() == "admin":
            user, _ = User.objects.get_or_create(username=admin)
            login(request, user)
            return redirect('View_Remote_Users')
        else:
            try:
                enter = ServiceProvider_Model.objects.get(username=admin, password=password)
                user, _ = User.objects.get_or_create(username=enter.username)
                login(request, user)
                request.session["sp_userid"] = enter.id
                return redirect('View_Remote_Users')
            except:
                return render(request, 'SProvider/serviceproviderlogin.html', {'msg': 'Invalid Credentials'})

    return render(request,'SProvider/serviceproviderlogin.html')

def serviceproviderregister(request):
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
        ServiceProvider_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city,address=address,gender=gender)

        obj = "Registered Successfully"
        return render(request, 'SProvider/serviceproviderregister.html',{'object':obj})
    else:
        return render(request,'SProvider/serviceproviderregister.html')

@login_required(login_url='serviceproviderlogin')
def Find_Prediction_Of_Cyber_Attack_Type_Ratio(request):
    detection_ratio.objects.all().delete()
    ratio = ""
    kword = 'DDoS'
    print(kword)
    obj = predict_cyber_attack.objects.all().filter(Q(Prediction=kword))
    obj1 = predict_cyber_attack.objects.all()
    count = obj.count()
    count1 = obj1.count()
    if count1 > 0:
        ratio = (count / count1) * 100
    else:
        ratio = 0
    if ratio != 0:
        detection_ratio.objects.create(names=kword, ratio=ratio)

    ratio12 = ""
    kword12 = 'Malware'
    print(kword12)
    obj12 = predict_cyber_attack.objects.all().filter(Q(Prediction=kword12))
    obj112 = predict_cyber_attack.objects.all()
    count12 = obj12.count()
    count112 = obj112.count()
    if count112 > 0:
        ratio12 = (count12 / count112) * 100
    else:
        ratio12 = 0
    if ratio12 != 0:
        detection_ratio.objects.create(names=kword12, ratio=ratio12)


    obj = detection_ratio.objects.all()
    return render(request, 'SProvider/Find_Prediction_Of_Cyber_Attack_Type_Ratio.html', {'objs': obj})

@login_required(login_url='serviceproviderlogin')
def View_Remote_Users(request):
    obj=ClientRegister_Model.objects.all()
    return render(request,'SProvider/View_Remote_Users.html',{'objects':obj})

@login_required(login_url='serviceproviderlogin')
def charts(request,chart_type):
    chart1 = detection_ratio.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts.html", {'form':chart1, 'chart_type':chart_type})

@login_required(login_url='serviceproviderlogin')
def charts1(request,chart_type):
    chart1 = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts1.html", {'form':chart1, 'chart_type':chart_type})

@login_required(login_url='serviceproviderlogin')
def View_Prediction_Of_Cyber_Attack_Type_Details(request):
    obj =predict_cyber_attack.objects.all()
    return render(request, 'SProvider/View_Prediction_Of_Cyber_Attack_Type_Details.html', {'list_objects': obj})

@login_required(login_url='serviceproviderlogin')
def likeschart(request,like_chart):
    charts =detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/likeschart.html", {'form':charts, 'like_chart':like_chart})


@login_required(login_url='serviceproviderlogin')
def Download_Predicted_DataSets(request):

    response = HttpResponse(content_type='application/ms-excel')
    # decide file name
    response['Content-Disposition'] = 'attachment; filename="Predicted_Datasets.xls"'
    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')
    # adding sheet
    ws = wb.add_sheet("sheet1")
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    # writer = csv.writer(response)
    obj = predict_cyber_attack.objects.all()
    data = obj  # dummy method to fetch data.
    for my_row in data:

        row_num = row_num + 1

        ws.write(row_num, 0, my_row.Fid, font_style)
        ws.write(row_num, 1, my_row.Timestamp, font_style)
        ws.write(row_num, 2, my_row.Source_IP_Address, font_style)
        ws.write(row_num, 3, my_row.Destination_IP_Address, font_style)
        ws.write(row_num, 4, my_row.Source_Port, font_style)
        ws.write(row_num, 5, my_row.Destination_Port, font_style)
        ws.write(row_num, 6, my_row.Protocol, font_style)
        ws.write(row_num, 7, my_row.Packet_Length, font_style)
        ws.write(row_num, 8, my_row.Packet_Type, font_style)
        ws.write(row_num, 9, my_row.Traffic_Type, font_style)
        ws.write(row_num, 10, my_row.Alerts_Warnings, font_style)
        ws.write(row_num, 11, my_row.Action_Taken, font_style)
        ws.write(row_num, 12, my_row.Severity_Level, font_style)
        ws.write(row_num, 13, my_row.Device_Information, font_style)
        ws.write(row_num, 14, my_row.Network_Segment, font_style)
        ws.write(row_num, 15, my_row.Geolocation_Data, font_style)
        ws.write(row_num, 16, my_row.ProxyInformation, font_style)
        ws.write(row_num, 17, my_row.FirewallLogs, font_style)
        ws.write(row_num, 18, my_row.IDS_IPS_Alerts, font_style)
        ws.write(row_num, 19, my_row.Log_Source, font_style)
        ws.write(row_num, 20, my_row.Prediction, font_style)

    wb.save(response)
    return response

@login_required(login_url='serviceproviderlogin')
def train_model(request):
    detection_accuracy.objects.all().delete()

    import os
    model_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(model_dir, 'Datasets.csv')
    df = pd.read_csv(dataset_path, encoding='latin-1')

    # 1. Handling Missing Values
    df = df.ffill().bfill()

    def apply_response(Label):
        if (Label == 0): # DDoS
            return 0
        elif (Label == 1): # Malware
            return 1

    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.feature_selection import SelectKBest, f_classif
    from sklearn.model_selection import RandomizedSearchCV, train_test_split
    import joblib
    from sklearn.ensemble import VotingClassifier

    df['results'] = df['AttackType'].apply(apply_response)

    le_protocol = LabelEncoder()
    df['Protocol'] = le_protocol.fit_transform(df['Protocol'].astype(str))

    le_severity = LabelEncoder()
    df['Severity_Level'] = le_severity.fit_transform(df['Severity_Level'].astype(str))

    le_device = LabelEncoder()
    df['Device_Information'] = le_device.fit_transform(df['Device_Information'].astype(str))
    
    le_sip = LabelEncoder()
    df['Source_IP_Address'] = le_sip.fit_transform(df['Source_IP_Address'].astype(str))
    
    le_dip = LabelEncoder()
    df['Destination_IP_Address'] = le_dip.fit_transform(df['Destination_IP_Address'].astype(str))
    
    le_geo = LabelEncoder()
    df['Geolocation_Data'] = le_geo.fit_transform(df['Geolocation_Data'].astype(str))

    le_traffic = LabelEncoder()
    df['Traffic_Type'] = le_traffic.fit_transform(df['Traffic_Type'].astype(str))

    X = df[['Source_Port', 'Destination_Port', 'Packet_Length', 'Protocol', 'Severity_Level', 'Device_Information', 'Source_IP_Address', 'Destination_IP_Address', 'Geolocation_Data', 'Traffic_Type']]
    y = df['results']

    models = []
    from sklearn.utils import resample
    train_data = pd.concat([X, y], axis=1)
    majority = train_data[train_data.results==0]
    minority = train_data[train_data.results==1]
    minority_upsampled = resample(minority, replace=True, n_samples=len(majority), random_state=42)
    upsampled = pd.concat([majority, minority_upsampled])
    X_up = upsampled.drop('results', axis=1)
    y_up = upsampled['results']

    X_train, X_test, y_train, y_test = train_test_split(X_up, y_up, test_size=0.20, random_state=42)
    
    # 2. Standardization
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 3. Feature Selection
    selector = SelectKBest(score_func=f_classif, k=10)
    X_train_sel = selector.fit_transform(X_train_scaled, y_train)
    X_test_sel = selector.transform(X_test_scaled)

    # Artificial Neural Network (ANN) - Tuned
    print("Artificial Neural Network (ANN)")
    from sklearn.neural_network import MLPClassifier
    mlp_params = {'hidden_layer_sizes': [(150, 100, 50), (100, 50)], 'alpha': [0.0001, 0.001]}
    mlpc = RandomizedSearchCV(MLPClassifier(max_iter=500, random_state=42), mlp_params, n_iter=2, cv=3)
    mlpc.fit(X_train_sel, y_train)
    y_pred = mlpc.predict(X_test_sel)
    print("ACCURACY", accuracy_score(y_test, y_pred) * 100)
    models.append(('MLPClassifier', mlpc.best_estimator_))
    detection_accuracy.objects.create(names="ANN", ratio=accuracy_score(y_test, y_pred) * 100)

    # Decision Tree Classifier - Tuned
    print("Decision Tree Classifier")
    dt_params = {'max_depth': [None], 'min_samples_split': [2]}
    dtc = RandomizedSearchCV(DecisionTreeClassifier(random_state=42), dt_params, n_iter=1, cv=3)
    dtc.fit(X_train_sel, y_train)
    dtcpredict = dtc.predict(X_test_sel)
    print("ACCURACY", accuracy_score(y_test, dtcpredict) * 100)
    models.append(('DecisionTreeClassifier', dtc.best_estimator_))
    detection_accuracy.objects.create(names="Decision Tree", ratio=accuracy_score(y_test, dtcpredict) * 100)

    # SVM Model - Tuned
    print("SVM")
    from sklearn import svm
    svm_params = {'C': [10], 'kernel': ['rbf']}
    lin_clf = RandomizedSearchCV(svm.SVC(probability=True, random_state=42), svm_params, n_iter=1, cv=3)
    lin_clf.fit(X_train_sel, y_train)
    predict_svm = lin_clf.predict(X_test_sel)
    svm_acc = accuracy_score(y_test, predict_svm) * 100
    print("ACCURACY", svm_acc)
    models.append(('svm', lin_clf.best_estimator_))
    detection_accuracy.objects.create(names="SVM", ratio=svm_acc)

    # Logistic Regression - Tuned
    print("Logistic Regression")
    from sklearn.linear_model import LogisticRegression
    lr_params = {'C': [0.1, 1, 10]}
    reg = RandomizedSearchCV(LogisticRegression(random_state=42, solver='lbfgs'), lr_params, n_iter=3, cv=3)
    reg.fit(X_train_sel, y_train)
    y_pred_lr = reg.predict(X_test_sel)
    print("ACCURACY", accuracy_score(y_test, y_pred_lr) * 100)
    models.append(('logistic', reg.best_estimator_))
    detection_accuracy.objects.create(names="Logistic Regression", ratio=accuracy_score(y_test, y_pred_lr) * 100)

    # Voting Classifier (Ensemble)
    print("Voting Classifier (Ensemble)")
    
    acc_mlp = accuracy_score(y_test, y_pred)
    acc_dtc = accuracy_score(y_test, dtcpredict)
    acc_svm = accuracy_score(y_test, predict_svm)
    acc_lr = accuracy_score(y_test, y_pred_lr)
    
    classifier = VotingClassifier(models, voting='soft', weights=[acc_mlp, acc_dtc, acc_svm, acc_lr])
    classifier.fit(X_train_sel, y_train)
    
    y_pred_voting = classifier.predict(X_test_sel)
    voting_acc = accuracy_score(y_test, y_pred_voting) * 100
    print("ENSEMBLE ACCURACY:", voting_acc)
    detection_accuracy.objects.create(names="Ensemble", ratio=voting_acc)

    # Save models and transformers using joblib
    joblib.dump(classifier, os.path.join(model_dir, 'cyber_model.pkl'))
    joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))
    joblib.dump(selector, os.path.join(model_dir, 'selector.pkl'))
    joblib.dump(le_protocol, os.path.join(model_dir, 'le_protocol.pkl'))
    joblib.dump(le_severity, os.path.join(model_dir, 'le_severity.pkl'))
    joblib.dump(le_device, os.path.join(model_dir, 'le_device.pkl'))
    joblib.dump(le_sip, os.path.join(model_dir, 'le_sip.pkl'))
    joblib.dump(le_dip, os.path.join(model_dir, 'le_dip.pkl'))
    joblib.dump(le_geo, os.path.join(model_dir, 'le_geo.pkl'))
    joblib.dump(le_traffic, os.path.join(model_dir, 'le_traffic.pkl'))

    csv_format = 'Results.csv'
    df.to_csv(csv_format, index=False)

    obj = detection_accuracy.objects.all()
    return render(request,'SProvider/train_model.html', {'objs': obj})