## Introduction
This is the take away assignment for fetch ETL Job

## Objective 
We need to fetch the data from sqs and write it into postgres post transformation

## Steps for running the code
    cd sqs_fetch
    docker-compose up

# Project Structure

## TakeHome

### sqs_fetch  (Project folder)
    packages are mentioned below
#### config  
  - `__init__.py`
  - `config.py`
  - `config.yaml`
        
        config folder contains the configuration details of the ETL job that we are going to run.
        config.yaml contains the details of the readers and writers for the ETL job and also the schema which the data needs to adhere to.
    

#### connections
  - `__init__.py`
  - `db_connection.py`
  - `sqs_connection.py`

        connections folder contains the details of the connections that we are going to use in our project.
        Here I have DBConnection and SQSConnection written in a singleton pattern as we dont want to duplicate connections.

#### models
  - `__init__.py`
  - `message_model.py`

        models folder contains the details of the ORM using sqlalchemy. This is the schema the database table have.
        Our data should adhere to this. Below, in utils you will see validator which only passes the validated data to the next step.


#### readers_writers
  - `__init__.py`
  - `client_registery.py`
  - `db_client.py`
  - `read_client.py`
  - `sqs_client.py`
    - `write_client.py`

          reader_writer folder contains the client_registery which registers the clients for reading and writing the data.
          I have ReadClient and WriteClient Abstract classes and their specific implemenation as SQSClient abd DBClient respectively.
          These ReadClient and WriteClient helps us to write code which is extensible and follows solid principle.
          In the main.py when I import the clients during that time the client registery registers the clients. 
          Hence we have the clients ready and instantiated before use.

#### utils
  - `__init__.py`
  - `pii_masking.py`
  - `schema_validator.py`
  - `transform.py`
  - `transformer.py`
  - `validator.py`


        utils folder contains the utilies required by the ETL job.
        One such utility is Transformer. So Transformer is an abstract class which defines the transformation.
        I also have the specific transformer define as transformer.py . It makes use of pii_masking.
        I also have validator defined here. All the validations required can be designed using this Abstract class.
        I have schema_validator which I am using in the ETL Job when doing the transformation in the do_transform function.
        (This ensures that I only pass on the valid messages).

        

### Root Directory Files
  - `docker-compose.yaml`
  - `Dockerfile`
  - `ETLJob.py`
  - `main.py`
  - `README.md`
  - `requirements.txt`


        ETL Job describes the basic steps in any ETL Job. Extract Transform Load. Here they are defined by read_messaged, do_transform and write.
        This is highly configurable. We can pass on different readers and writers in the main and the code will work efficiently.
        I have tried making the code as readable and modular as possible and easy to understand. It is extensible as well.


        docker-compose contains the details of the application build. For the etl job I am waiting for 10 seconds just to allow the other services to be up 
        and running completely.



## Questions
 - `How would you deploy this application in production?`
            
        I will use any ci/cd pipeline to first run all the tests that are written and then build the docker image and then deploy it on the Kubernetes server

- `What other components would you want to add to make this production ready?`

        I will definitely add more exception handling. MI will also try to log the exception to some locations in s3. 
        Once we have the log on s3 we can have some sort of notification using AWS SNS.
    
        I will include more tests such as integration test and write the implementation for the tests as well.

- `How can this application scale with a growing dataset.`
        
       We will have a deployment.yaml for deploying the app which will be deployed by ci/cd pipeline in prod. We can scale up the pods in Kubernetes. We can use autoscaler in kubernetes to scale up depending on the memory or number of connections. For very huge dataset, I would probably think of a spark based transformer.
        The code for that will be very easy to write as the our ETL Job is coded to the Abstract class and not any specific implementation. Also since our entire code follows idempotency so duplicacy is also not an issue here.

- `How can PII be recovered later on?`
        
        The Goal of masking is that it is not recoverable, other wise that destroys the whole idea to mask in the first place.
        However, if that is what is needed then we can use fernet keys to encrypt and decrypt the hashes. The fernet keys will be needed to be stored in 
        a very secure location like AWS secrets and injected via environment variables only (This injection can be the part of CI/CD pipeline as well).


- `What are the assumptions you made?`

        Assumptions made:
            1. Since in the table app_version was given as an integer and the data was string-based, I have taken the first number as the version.
            2. PIIs are not recoverable. (For recoverable PII, I will use a different strategy (see above) )
            3. Batch size in one round of ingestion - 10 messages. (Can be changed in SQSClient)
            




### Next Steps: 

        Testing and writing tests is one of the major steps that needs to be done for any project.
        Generally, I tend to follow TDD but given the time, I went for a direct solution. 
        
        Taking the current status as it is, I would add tests to the code.
            

### References used:

        https://docs.localstack.cloud/getting-started/
        https://docs.sqlalchemy.org/en/20/orm/quickstart.html#create-an-engine
        https://docs.sqlalchemy.org/en/20/orm/quickstart.html#create-objects-and-persist
        https://docs.sqlalchemy.org/en/20/orm/session_basics.html#basics-of-using-a-session
        https://www.geeksforgeeks.org/unit-testing-python-unittest/
        

