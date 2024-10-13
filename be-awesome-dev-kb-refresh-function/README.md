# Be Awesome Dev Knowledge Base Auto Refresh

## I. How to setup up knowledge base

1. Go to AWS Bedrock console and create a new Knowledge Base, specify the knowledge base bucket as the source
2. Retrieve the Knowledge Base ID and the Data Source ID.
3. In the `function/app.py` file, replace the ids above in the appropriate place.
4. Run `sam build` to re-build the function
5. Run `sam deploy` to re-deploy the function
6. Configure the max concurrency of the function to 10 in the AWS Console.
