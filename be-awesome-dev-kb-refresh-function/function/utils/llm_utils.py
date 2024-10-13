import boto3
from langchain_aws import ChatBedrockConverse
from langchain_core.prompts import ChatPromptTemplate
from typing import List

from models.summary import Summary
from models.post import Post


def init_chat_model():
    boto_session = boto3.Session(region_name="us-west-2")
    sts_client = boto_session.client("sts")

    assumed_role = sts_client.assume_role(
        RoleArn="arn:aws:iam::629872170007:role/bedrock-consumer",
        RoleSessionName="be-awesome-dev-bedrock-consumer",
    )

    credentials = assumed_role["Credentials"]

    bedrock_client = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
        region_name="us-west-2",
    )

    model = ChatBedrockConverse(
        model="meta.llama3-1-70b-instruct-v1:0",
        region_name="us-west-2",
        client=bedrock_client,
    )

    return model


def init_summary_chain(llm):
    system_prompt_template = """
  You are a helpful assistant that can give summary over markdown documents.
  Given a markdown article, summarise its content with the following requirement:

  * DO NOT write code in your summary.
  * DO NOT include code examples in your summary, you must keep the summary as concise as possible.
  * For each article, briefly describe what it is about overall and mention the main topics without further explanation.
  * Be as concise as possible with your summary.

  Below is the markdown name of the article and its content:

  Article name: 

  {article_name}

  Content:

  {content}
  """

    prompt = ChatPromptTemplate.from_template(system_prompt_template)

    chain = prompt | llm

    return chain


def generate_summaries(posts: List[Post], summary_chain, output_file_name: str):
    summaries: List[Summary] = []
    for post in posts:
        post_content = post.content
        post_name = post.filename

        MAX_ATTEMPT = 3
        attempt = 1
        response: Summary = summary_chain.invoke(
            {"content": post_content, "article_name": post_name.split("/")[-1]}
        )

        while attempt < MAX_ATTEMPT and response is None:
            response: Summary = summary_chain.invoke(
                {"content": post_content, "article_name": post_name.split("/")[-1]}
            )
            attempt += 1

        print(response)
        summaries.append(response)

    with open(output_file_name, "w", encoding="utf-8") as output_file:
        for s in summaries:
            output_file.write(f"Topic: {s.main_topic}\n")
            output_file.write(f"Summary:\n{s.summary_content}\n\n")
            output_file.write("\n\n===================================\n\n")
            print(f"Written summary content of {s.main_topic} to file")

    return summaries
