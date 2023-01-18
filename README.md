# Fraud-Detection-And-Analysis

This GitHub repository contains various machine learning models for analyzing and detecting fraudulent activity. The models include methods for identifying patterns and anomalies in financial transactions, as well as techniques for predicting the likelihood of fraud in new transactions. The repository includes code for training and evaluating the models. It's useful for researchers, data scientists and engineers who are interested in developing and implementing fraud detection systems. Various techniques such as supervised and unsupervised have been used in this repository, allowing for a comprehensive analysis and detection of fraud cases.

The main technique used for handling the highly imbalanced data is "Under-Sampling". 

## Fraud Detection Data:
we will be exploring a dataset of credit card transactions that has been modified to protect sensitive information. Instead of using the original features, the data contains 28 principal component analysis (PCA) transformed features, as well as two additional features that were not transformed: time and amount.

The "time" feature represents the number of seconds that have elapsed between each transaction and the first transaction in the dataset. The "amount" feature, on the other hand, represents the monetary value of the transaction.

The response variable, or the variable we are interested in predicting, is called "Class" and it takes on a value of 1 if the transaction is a fraud transaction, and 0 if it is not. We will be using this variable to train and evaluate our models. The data source can be found in the [Link](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud).
