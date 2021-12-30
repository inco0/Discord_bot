import boto3


def get_discord_token(region="eu-central-1"):
    ssm = boto3.client('ssm', region)
    return get_parameters(ssm, "discord_token")


def get_parameters(ssm, parameter_name):
    response = ssm.get_parameters(
        Names=[parameter_name],
        WithDecryption=True
    )
    for parameter in response['Parameters']:
        return parameter['Value']
