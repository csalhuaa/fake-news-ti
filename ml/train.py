import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

def entrenar_y_guardar_modelos(X_train, y_train, model_dir):
    nb = MultinomialNB()
    nb.fit(X_train, y_train)
    joblib.dump(nb, os.path.join(model_dir, "nb_model.pkl"))

    svm = LinearSVC()
    svm.fit(X_train, y_train)
    joblib.dump(svm, os.path.join(model_dir, "svm_model.pkl"))