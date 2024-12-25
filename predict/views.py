from django.shortcuts import render
from django.http import JsonResponse
from . import cnn_model
import numpy as np
import os

means = np.array([
    5.44389439e+01, 6.79867987e-01, 3.15841584e+00, 1.31689769e+02,
    2.46693069e+02, 1.48514851e-01, 9.90099010e-01, 1.49607261e+02,
    3.26732673e-01, 1.03960396e+00, 1.60066007e+00, 6.72240803e-01,
    4.73421927e+00
])
std_devs = np.array([
    9.02373483, 0.46652707, 0.95853994, 17.57068124, 51.69140647, 0.3556096,
    0.99332807, 22.83722455, 0.46901859, 1.15915747, 0.61520843, 0.9296715,
    1.93007938
])
explanation_dict = {
    "sex": {0: "Female (Nữ)", 1: "Male (Nam)"},
    "Chest Pain Type": {
        0: "Typical Angina (Đau thắt ngực điển hình)",
        1: "Atypical Angina (Đau thắt ngực không điển hình)",
        2: "Non-Anginal Pain (Không đau thắt ngực)",
        3: "Asymptomatic (Không có triệu chứng)",
    },
    "Fasting Blood Sugar > 120 mg/dl": {
        0: "False (≤ 120 mg/dl)",
        1: "True (> 120 mg/dl)",
    },
    "Resting ECG": {
        0: "Normal (Bình thường)",
        1: "ST-T wave abnormality (Bất thường sóng ST-T)",
        2: "Left ventricular hypertrophy (Phì đại thất trái)",
    },
    "Exercise Induced Angina": {
        0: "No (Không đau thắt ngực do gắng sức)",
        1: "Yes (Có đau thắt ngực do gắng sức)",
    },
    "Slope of the ST Segment": {
        0: "Upsloping (Dốc lên)",
        1: "Flat (Phẳng)",
        2: "Downsloping (Dốc xuống)",
    },
    "Thalassemia": {
        1: "Normal (Bình thường)",
        2: "Fixed Defect (Khuyết điểm cố định)",
        3: "Reversible Defect (Khuyết điểm có thể đảo ngược)",
    },
}

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'models', 'best_model.pth')
model = cnn_model.CNN_model()
model.load_best_model(model_path)
def standard_data(x):
    return (x - means) / std_devs

def access(request):
    return render(request, "predict/input.html")

def predict_heart_disease(request):
    if request.method == "POST":
        try:
            # Lấy dữ liệu từ form
            form_data = {
                "age": int(request.POST.get("age")),
                "sex": int(request.POST.get("sex")),
                "Chest Pain Type": int(request.POST.get("cp")),
                "Resting Blood Pressure": int(request.POST.get("trestbps")),
                "Cholesterol": int(request.POST.get("chol")),
                "Fasting Blood Sugar > 120 mg/dl": int(request.POST.get("fbs")),
                "Resting ECG": int(request.POST.get("restecg")),
                "Max Heart Rate Achieved": int(request.POST.get("thalach")),
                "Exercise Induced Angina": int(request.POST.get("exang")),
                "ST Depression": float(request.POST.get("oldpeak")),
                "Slope of the ST Segment": int(request.POST.get("slope")),
                "Number of Major Vessels Colored": int(request.POST.get("ca")),
                "Thalassemia": int(request.POST.get("thal"))
            }

            # Chuẩn bị dữ liệu đầu vào
            input_data = np.array([[form_data[key] for key in form_data]])
            input_data = standard_data(input_data)  # Hàm chuẩn hóa dữ liệu
            for key, value in form_data.items():
                if key in explanation_dict:
                    form_data[key] = explanation_dict[key].get(value, value)
            #print(form_data)
            # Dự đoán kết quả
            result = model.predict(input_data)
            result=f"{result * 100:.2f}%"


            # Render kết quả ra output.html
            return render(request, "predict/output.html", {
                "prediction": result,
                "form_data": form_data
            })

        except Exception as e:
            # Xử lý lỗi và hiển thị thông báo
            return render(request, "predict/output.html", {"error": str(e)})

    # Nếu không phải POST, render input form
    return render(request, "predict/input.html")