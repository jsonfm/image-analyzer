from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


y_true = [1, 0, 1, 1, 0, 1]
y_pred = [0, 0, 1, 0, 0, 1]
m = confusion_matrix(y_true, y_pred)
v = pd.DataFrame(m)
sns.heatmap(v, annot=True, cmap='Blues_r', fmt='g')
plt.ylabel('True')
plt.xlabel('Predicted')
plt.show()
