# Fraud-Detection-ML-Docker-AWS-Sagemaker-Deployment

This GitHub repository contains various machine learning models for analyzing and detecting fraudulent activity. The models include methods for identifying patterns and anomalies in financial transactions, as well as techniques for predicting the likelihood of fraud in new transactions. The repository includes python scripts for data analysis, model building, model evaluation and Docker containerization, as well as instructions for deploying the model on AWS SageMaker using ECR repository. It's useful for researchers, data scientists and engineers who are interested in developing and implementing fraud detection systems. Various techniques such as supervised and unsupervised have been used in this repository, allowing for a comprehensive analysis and detection of fraud cases.

## Fraud Detection Data:
we will be exploring a dataset of credit card transactions that has been modified to protect sensitive information. Instead of using the original features, the data contains 28 principal component analysis (PCA) transformed features, as well as two additional features that were not transformed: time and amount.

The "time" feature represents the number of seconds that have elapsed between each transaction and the first transaction in the dataset. The "amount" feature, on the other hand, represents the monetary value of the transaction.

The response variable, or the variable we are interested in predicting, is called "Class" and it takes on a value of 1 if the transaction is a fraud transaction, and 0 if it is not. We will be using this variable to train and evaluate our models. The data source can be found in the [Link](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud).

## Data Exploration and Model Building:

The main issue with this dataset is that it is highly imbalanced, with a large majority of transactions being non-fraudulent. To address this issue, we used two techniques: under-sampling and over-sampling using the Synthetic Minority Over-sampling Technique (SMOTE) method. These techniques allowed us to balance the dataset and improve the performance of our models.

We then evaluated various classification models for their performance in detecting fraudulent transactions using metrics such as F1-score, recall, precision, ROC AUC, and average precision. We found that the XGBoost and Logistic Regression models performed similarly and better than other models, but the XGBoost Classifier generalized the model learning slightly better than the Logistic Regression Classifier.

## Deployment:

As a result, we chose the XGBoost Classifier to include in a Docker container and deploy it on AWS SageMaker. This allows us to easily deploy the model in a production environment and make predictions on new data.


# Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Installing Docker and testing locally:
1. Clone the repository to your local machine by

```bash
git clone https://github.com/vspvikram/Fraud-Detection-ML-Docker-AWS-Sagemaker-Deployment.git
```

2. Navigate to the downloaded directory.

```bash
cd Fraud-Detection-ML-Docker-AWS-Sagemaker-Deployment
```

3. Build the docker image on your computer. Before building the image you must generate the ```train.csv``` and ```test.csv``` files using the notebook ```fraud_data_EDA_and_model_building.ipynb```. Also copy these files in the ```test-dir``` for local test.

```bash
docker build --platform=linux/amd64 -t fraud-detect .
```

4. Testing the docker container locally by running:
```bash
docker run --rm -v "$(pwd)/test_dir:/opt/ml" fraud-detect train
```

5. If the training runs without any error then it ready to be deployed to Amazon Elastic Container Registry (ECR). For any errors, feel free to open a issue request in this repository.


## Deploying on Sagemaker using Amazon Elastic Container Registry (ECR):

1. Go to your AWS dashboard and create an ECR repository. 
2. On your local machine install and authenticate Amazon command line interface (CLI) using these links: [CLI Installation](https://github.com/tchapi/markdown-cheatsheet/blob/master/README.md) and [CLI Authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/Registries.html#registry_auth).
3. Now login to your AWS account in the CLI using
```bash
aws ecr get-login-password --region <region name> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region name>.amazonaws.com
```
4. Now, go to AWS sagemaker and create a new sagemaker notebook. Once notebook is ready, click on ```open jupyter``` to start the jupyter notebook session. Upload the sagemaker notebook ```sagemaker_notebook_fraud_detection.ipynb``` from this repository to the AWS sagemaker jupyter session.
5. Select the container image in the notebook that was pushed to ECR. Run the notebook to train and deploy the model by creating an endpoint.
6. Delete the endpoint by running the last cell in the notebook when you are done to avoid being charged by AWS.

## Authers:
* Vikram Singh
