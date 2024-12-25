import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
# from imblearn.over_sampling import SMOTE

class CNN_model:
    class TabularCNN(nn.Module):
        def __init__(self, num_filters=16, fc1_size=64):
            super(CNN_model.TabularCNN, self).__init__()
            self.conv1 = nn.Conv2d(1, num_filters, kernel_size=1)
            self.conv2 = nn.Conv2d(num_filters, num_filters * 2, kernel_size=2)
            self.fc1 = nn.Linear(self._get_flatten_size(num_filters), fc1_size)
            self.fc2 = nn.Linear(fc1_size, 1)

        def _get_flatten_size(self, num_filters):
            with torch.no_grad():
                dummy_input = torch.zeros(1, 1, 4, 4)
                x = nn.functional.relu(self.conv1(dummy_input))
                x = nn.functional.relu(self.conv2(x))
                return x.view(1, -1).size(1)

        def forward(self, x):
            x = nn.functional.relu(self.conv1(x))
            x = nn.functional.relu(self.conv2(x))
            x = x.view(x.size(0), -1)
            x = nn.functional.relu(self.fc1(x))
            x = self.fc2(x)
            return x

    def __init__(self, X_train=None, y_train=None, X_test=None, y_test=None):
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.best_model = None

    def predict(self, X_test):
        if self.best_model is None:
            raise ValueError("Best model has not been trained. Load the model using load_best_model.")
        X_test_padded = np.pad(X_test, ((0, 0), (0, 3)), 'constant')
        side_length = 4
        X_test_cnn = X_test_padded.reshape(-1, 1, side_length, side_length).astype(np.float32)
        X_test_tensor = torch.tensor(X_test_cnn, dtype=torch.float32)
        self.best_model.eval()
        with torch.no_grad():
            y_pred = self.best_model(X_test_tensor).squeeze()
            y_pred = torch.sigmoid(y_pred)
            #y_pred = torch.round(y_pred) 
        return y_pred.numpy()

    def load_best_model(self, file_path):
        model_data = torch.load(file_path)
        num_filters = model_data["num_filters"]
        fc1_size = model_data["fc1_size"]
        self.best_model = CNN_model.TabularCNN(num_filters=num_filters, fc1_size=fc1_size)
        self.best_model.load_state_dict(model_data["state_dict"])
        self.best_model.eval()
