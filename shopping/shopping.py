import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from datetime import datetime

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []
    with open(filename) as f:
        reader = csv.reader(f)
        # Read each line and add appropriate value to appropriate list or sub-list
        for line in reader:
            if not line[0].isdecimal():
                continue
            evidence_line = []
            for i in range(len(line)):
                match i:
                    # Index 10 is month, some are full, others abbreviated
                    case 10:
                        if len(line[i]) == 3:
                            mon = datetime.strptime(line[i], '%b').month
                        else:
                            mon = datetime.strptime(line[i], '%B').month
                        evidence_line.append(mon - 1)
                    # Index 15 is visitor type
                    case 15:
                        if line[i].lower() == 'new_visitor':
                            evidence_line.append(0)
                        else:
                            evidence_line.append(1)
                    # Index 16 is weekend
                    case 16:
                        if line[i].lower() == 'false':
                            evidence_line.append(0)
                        else:
                            evidence_line.append(1)
                    # Index 17 is Revenue
                    case 17:
                        if line[i].lower() == 'false':
                            labels.append(0)
                        else:
                            labels.append(1)
                    # All other indexes are already int or float
                    case _:
                        # These indexes are meant to be int
                        if i == 0 or i == 2 or i == 4 or i == 11 or i == 12 or i == 13 or i == 14:
                            evidence_line.append(int(line[i]))
                        # other indexes are meant to be floats
                        else:
                            evidence_line.append(float(line[i]))
            evidence.append(evidence_line)
        return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1).fit(evidence, labels)
    return model



def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Actual true count
    act_sen = 0
    # Actual false count
    act_spec = 0
    # True positive count
    cor_sen = 0
    # True negative count
    cor_spec = 0
    # Get counts
    for actual, predicted in zip(labels, predictions):
        if actual == 1:
            act_sen += 1
        else:
            act_spec += 1
        if actual == predicted:
            if actual == 1:
                cor_sen += 1
            else:
                cor_spec += 1
    # Calculate and return rates
    sensitivity = cor_sen / act_sen
    specificity = cor_spec / act_spec
    return (sensitivity, specificity)
    

if __name__ == "__main__":
    main()
