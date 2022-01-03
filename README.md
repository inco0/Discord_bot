# Discord_bot
A discord bot that listens to a channel and suggests sophisticated words to help you improve your vocabulary.

# Deployment
Builds a docker image and uploads it to the ECR repo specified in the `buildspec.yml` file. Deployed using a container made from the aforementioned image in ECS.
