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
    "Giới tính": {0: "Nữ", 1: "Nam"},
    "Loại đau ngực": {
        0: "Đau ngực điển hình",
        1: "Đau ngực không điển hình ",
        2: "Không phải đau thắt ngực",
        3: "Không có triệu chứng",
    },
    "Lượng glucose huyết tương lúc đói >120mg/dl": {
        0: "Không (≤ 120 mg/dl)",
        1: "Đúng (> 120 mg/dl)",
    },
    "Kết quả đo điện tâm đồ lúc nghỉ ngơi": {
        0: "Bình thường",
        1: "Có bất thường sóng ST-T ",
        2: "Có dấu hiệu phì đại thất trái ",
    },
    "Đau ngực lúc vận động": {
        0: "Có ",
        1: "Không ",
    },
    "Sự thay đổi đoạn ST vận động": {
        0: "Dốc lên ",
        1: "Phẳng",
        2: "Dốc xuống",
    },
    "Xạ hình tưới máu cơ tim": {
        1: "Bình thường",
        2: "Khiếm khuyết cố định",
        3: "Khiếm khuyết có hồi phục",
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
                "Tuổi": int(request.POST.get("age")),
                "Giới tính": int(request.POST.get("sex")),
                "Loại đau ngực": int(request.POST.get("cp")),
                "Huyết áp lúc nghỉ ngơi (mm Hg)": int(request.POST.get("trestbps")),
                "Nồng độ cholesterol đo được trong huyết thanh (mg/dl)": int(request.POST.get("chol")),
                "Lượng glucose huyết tương lúc đói >120mg/dl": int(request.POST.get("fbs")),
                "Kết quả đo điện tâm đồ lúc nghỉ ngơi": int(request.POST.get("restecg")),
                "Nhịp tim lớn nhất đo được": int(request.POST.get("thalach")),
                "Đau ngực lúc vận động": int(request.POST.get("exang")),
                "Đoạn ST chênh xuống do vận động so với lúc nghỉ ngơi": float(request.POST.get("oldpeak")),
                "Sự thay đổi đoạn ST vận động": int(request.POST.get("slope")),
                "Số lượng mạch chính phát hiện bởi nội soi huỳnh quang mạch vành": int(request.POST.get("ca")),
                "Xạ hình tưới máu cơ tim": int(request.POST.get("thal"))
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