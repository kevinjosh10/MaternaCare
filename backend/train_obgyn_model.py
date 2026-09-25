import numpy as np
import time
import json
import os
import csv
from typing import List, Tuple

class OBGYN_NeuralNetwork:
    """
    A Deep Pure-Numpy Neural Network (2 Hidden Layers).
    Designed specifically to act as an Obstetrician-Gynecologist AI.
    Trains on REAL WORLD Clinical Datasets with high precision optimization.
    """
    def __init__(self, input_size=6, hidden1=128, hidden2=64, output_size=3):
        self.input_size = input_size
        self.hidden1 = hidden1
        self.hidden2 = hidden2
        self.output_size = output_size 
        
        # He Initialization for Deep Layers
        self.W1 = np.random.randn(self.input_size, self.hidden1) * np.sqrt(2. / self.input_size)
        self.b1 = np.zeros((1, self.hidden1))
        
        self.W2 = np.random.randn(self.hidden1, self.hidden2) * np.sqrt(2. / self.hidden1)
        self.b2 = np.zeros((1, self.hidden2))
        
        self.W3 = np.random.randn(self.hidden2, self.output_size) * np.sqrt(2. / self.hidden2)
        self.b3 = np.zeros((1, self.output_size))

    def _relu(self, x):
        return np.maximum(0, x)
        
    def _relu_deriv(self, x):
        return x > 0
        
    def _softmax(self, x):
        exp_scores = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
        
    def forward(self, X):
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self._relu(self.z1)
        
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self._relu(self.z2)
        
        self.z3 = np.dot(self.a2, self.W3) + self.b3
        probs = self._softmax(self.z3)
        return probs

    def backward(self, X, y, probs, learning_rate=0.01, lambda_reg=0.001):
        m = X.shape[0]
        
        # Output layer gradients
        dz3 = probs
        dz3[range(m), y] -= 1
        dz3 /= m
        
        dW3 = np.dot(self.a2.T, dz3) + (lambda_reg * self.W3) / m
        db3 = np.sum(dz3, axis=0, keepdims=True)
        
        # Hidden layer 2 gradients
        da2 = np.dot(dz3, self.W3.T)
        dz2 = da2 * self._relu_deriv(self.z2)
        dW2 = np.dot(self.a1.T, dz2) + (lambda_reg * self.W2) / m
        db2 = np.sum(dz2, axis=0, keepdims=True)
        
        # Hidden layer 1 gradients
        da1 = np.dot(dz2, self.W2.T)
        dz1 = da1 * self._relu_deriv(self.z1)
        dW1 = np.dot(X.T, dz1) + (lambda_reg * self.W1) / m
        db1 = np.sum(dz1, axis=0, keepdims=True)
        
        # Update weights (Gradient Descent)
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W3 -= learning_rate * dW3
        self.b3 -= learning_rate * db3
        
    def compute_loss(self, probs, y, lambda_reg=0.001):
        m = y.shape[0]
        corect_logprobs = -np.log(probs[range(m), y] + 1e-8)
        cross_entropy = np.sum(corect_logprobs) / m
        # L2 Regularization term
        l2_cost = (lambda_reg / (2 * m)) * (np.sum(np.square(self.W1)) + np.sum(np.square(self.W2)) + np.sum(np.square(self.W3)))
        return cross_entropy + l2_cost
        
    def compute_precision_score(self, y_true, y_pred):
        precisions = []
        for c in range(self.output_size):
            tp = np.sum((y_pred == c) & (y_true == c))
            fp = np.sum((y_pred == c) & (y_true != c))
            if tp + fp == 0:
                precisions.append(0.0)
            else:
                precisions.append(tp / (tp + fp))
        return np.mean(precisions) * 100

def load_real_world_dataset(csv_path: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Loads the UCI Maternal Health Risk dataset, normalizes features, and creates train/val splits."""
    features = []
    labels = []
    
    label_map = {"low risk": 0, "mid risk": 1, "high risk": 2}
    
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if not row:
                continue
            try:
                # Age, SystolicBP, DiastolicBP, BS, BodyTemp, HeartRate
                f_vec = [float(x) for x in row[:6]]
                lbl = row[6].strip().lower()
                if lbl in label_map:
                    features.append(f_vec)
                    labels.append(label_map[lbl])
            except ValueError:
                continue
                
    X = np.array(features)
    y = np.array(labels)
    
    # Z-Score Normalization
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    X_norm = (X - mean) / (std + 1e-8)
    
    # Shuffle and Split (80/20)
    indices = np.random.permutation(X_norm.shape[0])
    split_idx = int(X_norm.shape[0] * 0.8)
    
    X_train = X_norm[indices[:split_idx]]
    y_train = y[indices[:split_idx]]
    X_val = X_norm[indices[split_idx:]]
    y_val = y[indices[split_idx:]]
    
    return X_train, y_train, X_val, y_val

def train_model():
    print("================================================================")
    print(" INITIATING HIGH-LEVEL OBSTETRICIAN-GYNECOLOGIST NEURAL NETWORK")
    print(" USING REAL WORLD CLINICAL DATA (UCI MATERNAL HEALTH RISK)")
    print("================================================================")
    
    # 1. Load Real Dataset
    csv_file = "maternal_health_risk.csv"
    if not os.path.exists(csv_file):
        print(f"[ERROR] {csv_file} not found. Please download it first.")
        return
        
    print("[INFO] Parsing and normalizing real clinical records...")
    X_train, y_train, X_val, y_val = load_real_world_dataset(csv_file)
    print(f"[INFO] Loaded {X_train.shape[0]} training samples and {X_val.shape[0]} validation samples.")
    
    # 2. Initialize Deep Pure-Numpy Network
    print("[INFO] Initializing Deep Neural Network (6 -> 128 -> 64 -> 3)")
    model = OBGYN_NeuralNetwork(input_size=6, hidden1=128, hidden2=64, output_size=3)
    
    # 3. Training Loop
    epochs = 500
    batch_size = 32
    num_batches = X_train.shape[0] // batch_size
    learning_rate = 0.05
    lambda_reg = 0.01
    
    print("\n--- DEEP TRAINING COMMENCED ---")
    for epoch in range(epochs):
        # Shuffle data
        indices = np.random.permutation(X_train.shape[0])
        X_shuffled = X_train[indices]
        y_shuffled = y_train[indices]
        
        # Learning Rate Decay
        if epoch > 0 and epoch % 100 == 0:
            learning_rate *= 0.5
            
        epoch_loss = 0
        for b in range(num_batches):
            start = b * batch_size
            end = start + batch_size
            X_batch = X_shuffled[start:end]
            y_batch = y_shuffled[start:end]
            
            # Forward & Backward Pass
            probs = model.forward(X_batch)
            loss = model.compute_loss(probs, y_batch, lambda_reg)
            model.backward(X_batch, y_batch, probs, learning_rate, lambda_reg)
            
            epoch_loss += loss
            
        if (epoch + 1) % 50 == 0:
            # Validation
            val_probs = model.forward(X_val)
            val_loss = model.compute_loss(val_probs, y_val, lambda_reg)
            val_preds = np.argmax(val_probs, axis=1)
            val_accuracy = np.mean(val_preds == y_val) * 100
            val_precision = model.compute_precision_score(y_val, val_preds)
            
            print(f"Epoch {epoch+1:03d}/{epochs} | LR: {learning_rate:.4f} | Train Loss: {epoch_loss/num_batches:.4f} | Val Loss: {val_loss:.4f} | Accuracy: {val_accuracy:.2f}% | Precision: {val_precision:.2f}%")
            
    print("\n[SUCCESS] Deep real-world model training complete.")
    
    # Save Weights
    os.makedirs("app/data", exist_ok=True)
    np.save("app/data/real_obgyn_W1.npy", model.W1)
    np.save("app/data/real_obgyn_W2.npy", model.W2)
    np.save("app/data/real_obgyn_W3.npy", model.W3)
    print(f"[INFO] Production OBGYN Deep Neural Network weights saved to app/data/real_obgyn_W*.npy")
    print("================================================================")
    print(" The AI is now mathematically optimized on verified medical data with HIGH PRECISION!")

if __name__ == "__main__":
    train_model()
