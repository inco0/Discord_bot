import boto3


def get_discord_token(region="eu-central-1"):
    """
    :param region: The region where the token exists in
    :return: Returns the discord token string from SSM on the region specified
    """
    ssm = boto3.client('ssm', region)
    return get_parameters(ssm, "discord_token")


def get_parameters(ssm, parameter_name):
    """
    :param ssm: AWS SSM object
    :param parameter_name: The parameter that needs to be returned
    :return: A string with the value of the parameter_name stored in SSM
    """
    response = ssm.get_parameters(
        Names=[parameter_name],
        WithDecryption=True
    )
    for parameter in response['Parameters']:
        return parameter['Value']
