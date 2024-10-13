import logging
from pprint import pprint
from utils.s3_utils import get_posts_from_bucket
from agent.post_summariser import summariser_chain
from utils.llm_utils import generate_summaries


def lambda_handler(event, context):
    posts = get_posts_from_bucket(bucket="be-awesome-dev-posts")
    summaries = generate_summaries(
        posts=posts,
        summary_chain=summariser_chain,
        output_file_name="summary.md",
    )

    pprint(summaries)
    logging.info("Function triggered with events")
    logging.info(event)

    return 1
