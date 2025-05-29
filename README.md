# SMARTBEAR PROJECT

## 


````shell
user: raforios@gmail.com
parrword: MotoPassword

docker build -t smartbear .

docker run -dit -v /Users/rafael/Work/projects/back/SmartBear/app/api:/app -p 8888:3000 --name smartbear smartbear

docker exec -ti smartbear /bin/bash 

docker pull postgres

docker run -d --rm -v /Users/rafael/Work/projects/back/bi/data/:/tmp --name pgsql-dev -e POSTGRES_PASSWORD=test1234 -e POSTGRES_USER=postgres -p 5432:5432 postgres

docker exec -it pgsql-dev bash



# API
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
deactivate

pip install fastapi
pip install uvicorn
pip install pymysql
pip install SQLAlchemy
pip install python-dotenv

uvicorn main:app --port 8080 --reload


pip freeze > requirements.txt
pip install -r requirements.txt




$ terraform init
$ terraform plan -out=tfplan
$ terraform apply --auto-approve

````
## CI/CD Steps:



## Manual Deploy Steps:

````shell
IMAGE=smartbear
ENV=staging
API_GATEWAY_NAME=$IMAGE
AWS_LAMBDA_ROLE_NAME="$IMAGE-lambda-role"
AWS_LAMBDA_FUNC_NAME="$IMAGE-$ENV"


# Get AWS_ACCOUNT and AWS_REGION. Both will be used in future commands
AWS_ACCOUNT=$(aws sts get-caller-identity --query 'Account' --output text)
AWS_REGION=$(aws ec2 describe-availability-zones --query 'AvailabilityZones[0].RegionName' --output text)

# login AWS ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com
# aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 732887652913.dkr.ecr.us-east-1.amazonaws.com

# create repo
aws ecr create-repository --repository-name $IMAGE --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE

# docker build --platform linux/x86_64 -t smartbear-api .
docker build --platform linux/arm64 -t "$IMAGE":latest .

# Create a timestamp tag
TAG=$(date +%Y%m%d_%H%M%S)

# Tag the image
docker tag "$IMAGE":latest $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/"$IMAGE":"$TAG"
# docker tag smartbear-api:latest 732887652913.dkr.ecr.us-east-1.amazonaws.com/smartbear-api:latest

docker push $AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/"$IMAGE":"$TAG"
# docker push 732887652913.dkr.ecr.us-east-1.amazonaws.com/smartbear-api:latest


# Give the Lambda execution role a name in AWS_LAMBDA_ROLE_NAME
aws iam create-role --role-name $AWS_LAMBDA_ROLE_NAME --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
aws iam attach-role-policy --role-name $AWS_LAMBDA_ROLE_NAME --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name $AWS_LAMBDA_ROLE_NAME --policy-arn arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess


aws lambda create-function \
    --function-name $AWS_LAMBDA_FUNC_NAME \
    --package-type Image \
    --code ImageUri=$AWS_ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com/$IMAGE:$TAG \
    --role $(aws iam get-role --role-name $AWS_LAMBDA_ROLE_NAME --query 'Role.Arn' --output text)

# Upload the current ENV to Lambda
aws lambda update-function-configuration \
    --function-name $AWS_LAMBDA_FUNC_NAME \
    --environment "Variables={ENV=$ENV}"


# Update ENV variables for the lambda function
# comment_re="^#.*"
# VARIABLES="Variables={"
# while IFS= read -r line || [ -n "$line" ]; do
#     trimmed="$(echo $line | sed -e 's/^[[:space:]]*//')"
#     if [[ ! $trimmed =~ $comment_re ]] && [ "$trimmed" != "" ];
#     then
#         VARIABLES+="$trimmed,"
#     fi
# done < .env.$ENV
# VARIABLES+="ENV=$ENV}"


# Upload the current ENV to Lambda
# aws lambda update-function-configuration \
#     --function-name $AWS_LAMBDA_FUNC_NAME \
#     --environment $VARIABLES


# Create API Gateway
aws apigateway create-rest-api --name $API_GATEWAY_NAME --region $AWS_REGION

# Get the API Gateway ID.
# API_GATEWAY_ID might not be available immediately after the creation of the
# new API Gateway. You might have to wait.
API_GATEWAY_ID=$(aws apigateway get-rest-apis --query "items[?name=='$API_GATEWAY_NAME'].id" --output text)


# First obtain the parent ID of the newly created API Gateway
PARENT_ID=$(aws apigateway get-resources --rest-api-id $API_GATEWAY_ID --region $AWS_REGION --query 'items[0].id' --output text)

# Then create a proxy resource under the parent ID.
# PARENT_ID might not be available immediately after the creation of the
# new API Gateway. You might have to wait.
aws apigateway create-resource --rest-api-id $API_GATEWAY_ID --region $AWS_REGION --parent-id $PARENT_ID --path-part {proxy+}


# First obtain the ID of the proxy resource just created
RESOURCE_ID=$(aws apigateway get-resources --rest-api-id $API_GATEWAY_ID --query "items[?parentId=='$PARENT_ID'].id" --output text)

RESOURCE_ID=$(aws apigateway get-resources --rest-api-id $API_GATEWAY_ID --query "items[?path=='/{proxy+}'].id" --output text)


# Then add "ANY" method to the resource
# RESOURCE_ID might not be available immediately after the creation of the
# proxy resource. You might have to wait.
aws apigateway put-method --rest-api-id $API_GATEWAY_ID --region $AWS_REGION --resource-id $RESOURCE_ID --http-method ANY --authorization-type "NONE"


# get the ARN of the Lambda function we created earlier
LAMBDA_ARN=$(aws lambda get-function --function-name $AWS_LAMBDA_FUNC_NAME --query 'Configuration.FunctionArn' --output text)

aws apigateway put-integration \
    --region $AWS_REGION \
    --rest-api-id $API_GATEWAY_ID \
    --resource-id $RESOURCE_ID \
    --http-method ANY \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri arn:aws:apigateway:${AWS_REGION}:lambda:path/2015-03-31/functions/arn:aws:lambda:$AWS_REGION:$AWS_ACCOUNT:function:$IMAGE-$ENV/invocations

aws lambda add-permission --function-name $LAMBDA_ARN --source-arn "arn:aws:execute-api:$AWS_REGION:$AWS_ACCOUNT:$API_GATEWAY_ID/*/*/{proxy+}" --principal apigateway.amazonaws.com --statement-id apigateway-access --action lambda:InvokeFunction

# Deploy to $ENV
aws apigateway create-deployment --rest-api-id $API_GATEWAY_ID --stage-name $ENV --variables env=$ENV


https://$API_GATEWAY_ID.execute-api.$AWS_REGION.amazonaws.com/$ENV/docs

https://9oppktxx97.execute-api.us-east-1.amazonaws.com/docs


echo $AWS_REGION
echo $API_GATEWAY_ID
echo $RESOURCE_ID


cdk bootstrap aws://732887652913/us-east-1

````