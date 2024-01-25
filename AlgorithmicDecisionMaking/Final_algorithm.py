#!/usr/bin/env python3

"""
File: algorithmicdecisionmaker.py
---------------------------------
This program presents an example of algorithmic decision making for you to analyze.  You should
feel free to modify the code in this file (or any other file in this project) if it helps you
better understand the results of this algorithm and allows you to create a more "fair" algorithm.
In it's current form, we train a PerceptronModel on the recidivism training data, where we only
consider "non-protected" attributes/features.  We then test the trained model on the recidivism
testing data.  Various performance statistics of the model on the training and testing data are
printed and the model weights are saved to a file.
"""

import constants
from dataset import Dataset
from perceptronmodel import PerceptronModel

# Constants

# Training data set input file name
TRAINING_DATAFILE = "recidivism-training-data.csv"

# Testing data set input file name
TESTING_DATAFILE = "recidivism-testing-data.csv"

# Name of output file for saving trained model weights
MODEL_FILE = "model.txt"


def main():
    # Read training data from file
    print("Reading training data: " + TRAINING_DATAFILE)
    training_set = Dataset(TRAINING_DATAFILE)

    # Select the features that we want to use to train the model
    features_to_use = select_features_to_use()

    # Train a PerceptronModel using the training data
    # (with only the input features in features_to_use list)
    print()
    print("Training PerceptronModel")
    pm = PerceptronModel(training_set, features_to_use)

    # Print the weights from the model after training
    print()
    print("Trained PerceptronModel weights:")
    print_labeled_weights(pm)

    # Determine accuracy and other results of model on training data
    print()
    print("Training Set Results:")
    print_results(pm, training_set)

    # Read testing data from file
    print()
    print("Reading testing data: " + TESTING_DATAFILE)
    testing_set = Dataset(TESTING_DATAFILE)

    # Determine accuracy and other results of model on testing data
    print()
    print("Testing Set Results:")
    print_results(pm, testing_set)

    # Determine accuracy and other results of model on testing data for just a particular
    # subgroup that has value 1 for the feature given by feature_index.  This is just one
    # example to show you how to use the print_results function.
    print()
    feature_index = constants.AGE_LESS_THAN_25
    print("Testing set results for " + constants.feature_names[feature_index])
    print_results(pm, testing_set, feature_index)

    feature_index = constants.RACE_AFRICAN_AMERICAN
    print("Testing set results for " + constants.feature_names[feature_index])
    print("\n \n \n")
    print_results(pm,testing_set,feature_index)

    feature_index = constants.RACE_CAUCASIAN
    print("Testing set results for " + constants.feature_names[feature_index])
    print("\n \n \n")
    print_results(pm, testing_set, feature_index)


    pm.save_model_weights(MODEL_FILE, constants.feature_names)


def select_features_to_use():
    """
    This function returns a list containing the indexes of all the feature that we would like to use
    when training our PerceptronModel.  The order of features indexes in the list does not matter.
    For simplicity, we include code for adding all the input feature indexes to the list, but comment
    out the the lines for the features we don't use in training the model.  You may want to modify the set
    of features used for training to see the effects on the model's performance.
    """
    # Start with an empty set of features and add the ones to use in the model below
    Filters_to_use = ""
    Valid_choices = ["b","k","l","j","i","h","f","e","d",]
    Be_cautious = ["i","f","e"]
    while (Filters_to_use.lower() not in Valid_choices):
        Filters_to_use = input("A) No Charge \n" 
                           "B) License Issue \n"
                           "C) Public Disturbance \n"
                           "D) Negligence \n"
                           "E) Drug Related\n"
                           "F) Alcohol Related\n"
                           "G) Weapons Related\n"
                           "H) Evading Arrest\n"
                           "I) Non-Violent Crime\n"
                           "J) Theft/Fraud/Burglary\n"
                           "K) Lewdness Prostitution\n"
                            "L) Violent Crime \n "
                           "Select a criminal charge (please only input the letter!):  \n")
        if (Filters_to_use in Be_cautious):
            print("Executing program, HOWEVER, the crime you selected has a significant disparity (greater than 3%) in ensuring"
                  "positive outcomes for marginalized groups in comparison to privileged groups \n \n \n")

        if (Filters_to_use in Valid_choices):
            print(
                "Please note that this risk assessment tool is still in development, and the classification Accuracy is nearly\n"
                "60% for most charges, and rarely nears a 70% accuracy. These predictions should be taken to be contextualized\n"
                "with the individual's background and not taken at face value.")
        else:
            print("Please select a different crime category, the system is unable to supply accurate classifications for the currently chosen crime \n")

    features_to_use = []

    # Input features based on number of prior juvenile felony convictions (bucketed into 4 categories)
    features_to_use.append(constants.JUVENILE_FELONY_COUNT_0)
    features_to_use.append(constants.JUVENILE_FELONY_COUNT_1)
    features_to_use.append(constants.JUVENILE_FELONY_COUNT_2)
    features_to_use.append(constants.JUVENILE_FELONY_COUNT_3_OR_MORE)

    # Input features based on number of prior juvenile misdemeanor convictions (bucketed into 4 categories)
    features_to_use.append(constants.JUVENILE_MISDEMEANOR_COUNT_0)
    features_to_use.append(constants.JUVENILE_MISDEMEANOR_COUNT_1)
    features_to_use.append(constants.JUVENILE_MISDEMEANOR_COUNT_2)
    features_to_use.append(constants.JUVENILE_MISDEMEANOR_COUNT_3_OR_MORE)

    # Input features based on number of prior non-felony/non-misdemeanor juvenile convictions
    # (bucketed into 4 categories)
    features_to_use.append(constants.JUVENILE_OTHER_COUNT_0)
    features_to_use.append(constants.JUVENILE_OTHER_COUNT_1)
    features_to_use.append(constants.JUVENILE_OTHER_COUNT_2)
    features_to_use.append(constants.JUVENILE_OTHER_COUNT_3_OR_MORE)

    # Input features based on number of prior (adult) criminal convictions (bucketed into 4 categories)
    features_to_use.append(constants.PRIOR_CONVICTIONS_COUNT_0)
    features_to_use.append(constants.PRIOR_CONVICTIONS_COUNT_1)
    features_to_use.append(constants.PRIOR_CONVICTIONS_COUNT_2)
    features_to_use.append(constants.PRIOR_CONVICTIONS_COUNT_3_OR_MORE)


    # Input features based on degree of criminal charge (felony or misdemeanor)
    features_to_use.append(constants.CHARGE_DEGREE_FELONY)
    features_to_use.append(constants.CHARGE_DEGREE_MISDEMEANOR)



    # Input features based on description of criminal charge (bucketed into 12 categories)
    Filters_to_use = Filters_to_use.lower()
    if (Filters_to_use == "b"):
        features_to_use.append(constants.CHARGE_DESC_LICENSE_ISSUE)


    elif (Filters_to_use == "c"):
        features_to_use.append(constants.CHARGE_DESC_NEGLIGENCE)

    elif (Filters_to_use == "d"):
        features_to_use.append(constants.CHARGE_DESC_DRUG_RELATED)

    elif (Filters_to_use == "e"):
        features_to_use.append(constants.CHARGE_DESC_ALCOHOL_RELATED)



    elif (Filters_to_use == "f"):
        features_to_use.append(constants.CHARGE_DESC_EVADING_ARREST)

    elif (Filters_to_use == "g"):
        features_to_use.append(constants.CHARGE_DESC_NONVIOLENT_HARM)
    elif (Filters_to_use == "h"):
        features_to_use.append(constants.CHARGE_DESC_NONVIOLENT_HARM)

    elif(Filters_to_use == "i"):
        features_to_use.append(constants.CHARGE_DESC_NONVIOLENT_HARM)

    elif(Filters_to_use == "j"):
        features_to_use.append(constants.CHARGE_DESC_LEWDNESS_PROSTITUTION)


    elif (Filters_to_use == "k"):
        features_to_use.append(constants.CHARGE_DESC_VIOLENT_CRIME)

    # The features below are intentionally commented out, so they are not currently used in training the model


    # Input features based on age (bucketed into 3 categories)


    #
    # # Input features based on gender (bucketed into 2 categories)
    features_to_use.append(constants.GENDER_FEMALE)
    features_to_use.append(constants.GENDER_MALE)
    #
    # # Input features based on race (bucketed into 6 categories)
    #
    features_to_use.append(constants.RACE_OTHER)
    features_to_use.append(constants.RACE_ASIAN)
    features_to_use.append(constants.RACE_NATIVE_AMERICAN)
    features_to_use.append(constants.RACE_CAUCASIAN)
    features_to_use.append(constants.RACE_HISPANIC)
    features_to_use.append(constants.RACE_AFRICAN_AMERICAN)


    return features_to_use


def print_labeled_weights(perceptronmodel):
    """
    This function prints the weights for all input features in the model.  It also
    prints the input feature name for each weight for easier comprehension.
    """
    weights = perceptronmodel.get_model_weights()
    for i in range(len(weights)):
        print(constants.feature_names[i] + ", weight:", weights[i])


def print_results(perceptronmodel, data, feature_index=None):
    """
    This function prints several statistical results determined by applying the PerceptronModel
    passed in to just the data in the Dataset that has value 1 for the given feature_index.
    If featureIndex is None (default), then we report statistics for all the data.
    """
    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    # Make a pass through all of the data
    for i in range(data.get_size()):
        instance = data.get_instance(i)

        # Only consider this instance for making a prediction if we are gathering statistics
        # on all the data or this instance has value 1 for the feature at feature_index.
        if (feature_index is None) or (instance[feature_index] == 1):

            # Make prediction for this instance
            prediction = perceptronmodel.predict(instance)

            # Get the actual output value corresponding to this data instance
            actual_output = data.get_output(i)

            # Determine whether our prediction is correct or not, and what sort of
            # correct/incorrect prediction it is.
            if prediction == 1:
                if actual_output == 1:
                    true_positive += 1     # predicted 1 (positive), actual output is 1 (positive)
                else:
                    false_positive += 1    # predicted 1 (positive), but actual output is 0 (negative)
            else:
                if actual_output == 0:
                    true_negative += 1
                else:
                    false_negative += 1

    total = true_positive + false_positive + true_negative + false_negative

    # Print various statistics based on the results of the model
    print("Overall accuracy (percentage of predictions that are correct) =", (true_positive + true_negative)/total)
    print("Count of True Positives (people detained who would have recidivated):", true_positive)
    print("Count of True Negatives (people released who did not recidivate):", true_negative)
    print("Count of False Positives (people detained who would not have recidivated):", false_positive)
    print("Count of False Negatives (people released who recidivated):", false_negative)

    print("Of those people detained, percentage who would not have recidivated =",
          false_positive/(true_positive + false_positive))
    print("Of those people released, percentage who recidivated =",
          false_negative/(true_negative + false_negative))

    print("Of those people who would not have recidivated, percentage detained =",
          false_positive/(true_negative + false_positive))
    print("Of those who would have recidivated, percentage released =",
          false_negative/(true_positive + false_negative))




# This provided line is required at the end of a Python file to call the main() function.
if __name__ == '__main__':
    main()
