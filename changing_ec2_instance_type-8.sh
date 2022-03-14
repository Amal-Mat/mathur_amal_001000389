# Change ec2 instance type from t2.micro to t2.small
Instance_ID="i-0fcac52ce85fd4dfe"

# Displays the EC2 instance details which is in running state
aws ec2 describe-instances \
--query "Reservations[*].Instances[*].{PublicIP:PublicIpAddress,Name:Tags[?Key=='Name']|[0].Value,Status:State.Name,InstanceID:InstanceId}" \
--filters Name=instance-state-name,Values=running \
--output table

# Command to stop the paticular EC2 instance
aws ec2 stop-instances --instance-ids "$Instance_ID"

# Displays the current state (Stopping) of the EC2 instance
aws ec2 describe-instances \
--instance-ids  "$Instance_ID" \
--query "Reservations[*].Instances[*].{PublicIP:PublicIpAddress,Name:Tags[?Key=='Name']|[0].Value,Status:State.Name,InstanceID:InstanceId,Instancetype:InstanceType}"  \
--output table

# Some downtime for the instance to be stopped
sleep 45

# Confirms that the instance is now stopped!
aws ec2 describe-instances \
--query "Reservations[*].Instances[*].{PublicIP:PublicIpAddress,Name:Tags[?Key=='Name']|[0].Value,Status:State.Name,InstanceID:InstanceId,Instancetype:InstanceType}" \
--output table

# Changes the instance type to t2.small
aws ec2 modify-instance-attribute \
--instance-id "$Instance_ID" \
--instance-type "{\"Value\": \"t2.small\"}"

# Displays the changed Instance type
aws ec2 describe-instances \
--query "Reservations[*].Instances[*].{PublicIP:PublicIpAddress,Name:Tags[?Key=='Name']|[0].Value,Status:State.Name,InstanceID:InstanceId,Instancetype:InstanceType}" \
--output table

# Restart the EC2 instance with the changed Instance Type
aws ec2 start-instances --instance-ids "$Instance_ID"
