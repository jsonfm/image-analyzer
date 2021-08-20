from matplotlib.markers import MarkerStyle
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVC
import os 
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
os.sys.path.append('..')


def print_score(model, X_train, y_train, X_test, y_test, train=True):
    if train:
        y_pred = model.predict(X_train)
        report = pd.DataFrame(classification_report(y_train, y_pred, output_dict=True))
        accuracy = accuracy_score(y_train, y_pred)
        cfm = confusion_matrix(y_train, y_pred)
    else:
        y_pred = model.predict(X_test)
        report = pd.DataFrame(classification_report(y_test, y_pred, output_dict=True))
        accuracy = accuracy_score(y_test, y_pred)
        cfm = confusion_matrix(y_test, y_pred)

    title = 'TRAIN RESULTS' if train else 'TEST RESULTS'
    print(f"=============== {title} ================")
    print("-> REPORT: ")
    print(report)
    print("________")
    print(f"Accuaracy: {100*accuracy: .3f} %")
    print("________")
    print(f"Confusion Matrix: {cfm}")
    print()
    

def apply_svm(X_train, X_test, y_train, y_test,max_iter=20, test_size=0.3, random_state=42):
    model = SVC(max_iter=max_iter)
    model.fit(X_train, y_train)
    return model


def merge(df_1, df_2):
    frames = [df_1, df_2]
    df = pd.concat(frames)
    return df


def apply_pca(X_train, X_test, y_train, y_test, n_components=3):
    pca = PCA(n_components=n_components)
    scaler = StandardScaler()
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, y_train, y_test


dfs = pd.read_csv('../../dataloaders/left_hippo_sclerosis_data.csv', index_col=0)
dfo = pd.read_csv('../../dataloaders/left_hippo_others_data.csv', index_col=0)
targets = pd.read_csv('../../dataloaders/targets.csv', index_col=0)


X = merge(dfs, dfo)
y = targets['target'][X.index.values]

print(X)
print(y)

print(f" X shape: {X.shape}")
print(f" y shape: {y.shape}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

X_train, X_test, y_train, y_test = apply_pca(X_train, X_test, y_train, y_test, n_components=3)

classiffier = apply_svm(X_train, X_test, y_train, y_test)

print_score(classiffier, X_train, y_train, X_test, y_test, train=True)
print_score(classiffier, X_train, y_train, X_test, y_test, train=False)

plt.figure(figsize=(8,6))
plt.scatter(X_train[:,0],X_train[:,1], c=y_train, cmap='rainbow', s=60)
plt.xlabel('First principal component')
plt.ylabel('Second Principal Component')
plt.grid(True)
plt.show()


# print_score(model, X_train, y_train, X_test, y_test, train=True)
# print_score(model, X_train, y_train, X_test, y_test, train=False)

# model, X_train, X_test, y_train, y_test = apply_svm(X, y)
# print_score(model, X_train, y_train, X_test, y_test, train=True)
# print_score(model, X_train, y_train, X_test, y_test, train=False)
