We wanted to test the dataset with another Model as the Logistic Regression model results did not meet our expectations.

We set the Random Forest Model with the following settings:
- 250 trees,
- Max depth 12,
- at least 5 sample sper leaf,
- a random state as 42

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

rf = RandomForestClassifier(
    n_estimators=250,
    max_depth=12,
    random_state=42,
    min_samples_leaf=5,
)

rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

rf.score(X_test, y_test)

print(classification_report(y_test, y_pred))



The model reached an accuracy of 86% on the test set of 9589 accidents.

With the `less severe` class the model performed quite well, with a precision of 87% and a recall of 99%. This means that the model almost always recognized these accidents correctly.

With the `severe` class, the model performed poorly as the recall for this was only 7% meaning it found only 7% of the severe accidents and incorrectly predicted the rest to be less severe. However, when the model predicted an accident to be severe, it was correct slightly more than a half of the time.