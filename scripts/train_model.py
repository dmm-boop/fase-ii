from pathlib import Path
import json
import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

ROOT = Path(__file__).resolve().parents[1]
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_test)
joblib.dump(model, ROOT / 'backend' / 'modelo.joblib')
metrics = {'dataset': 'sklearn.datasets.load_iris', 'samples_train': len(X_train), 'samples_test': len(X_test), 'accuracy': accuracy_score(y_test,pred), 'confusion_matrix': confusion_matrix(y_test,pred).tolist(), 'classification_report': classification_report(y_test,pred, target_names=['setosa','versicolor','virginica'],output_dict=True)}
(ROOT / 'docs' / 'metricas.json').write_text(json.dumps(metrics, indent=2), encoding='utf-8')
print(json.dumps({k:v for k,v in metrics.items() if k!='classification_report'}, indent=2))
