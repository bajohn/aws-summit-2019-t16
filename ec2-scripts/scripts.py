aws cloudformation validate-template template-body file://create_instance.yml --profile hack

aws cloudformation create-stack --stack-name test-ec2 \
        --template-body file://create_instance.yml \
        --profile hack \
        --parameters ParameterKey=SSHKey,ParameterValue=test_keypair

aws cloudformation wait stack-create-complete --stack-name test-ec2 --profile hack


aws cloudformation create-stack --stack-name create-profile \
    --template-body file://instance_profile.yml \
        --profile hack \
            --capabilities "CAPABILITY_NAMED_IAM"

aws cloudformation wait stack-create-complete --stack-name create-profile --profile hack

# aws cloudformation  delete-stack --stack-name test-ec2 --profile hack