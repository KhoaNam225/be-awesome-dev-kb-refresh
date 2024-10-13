import logging
from utils.s3_utils import (
    get_posts_from_bucket,
    write_posts_summary_content,
    sync_buckets_content,
    upload_object_to_bucket,
)
from utils.llm_utils import generate_summaries
from agent.post_summariser import summariser_chain


def lambda_handler(event, context):
    source_posts_bucket = "be-awesome-dev-posts"
    destination_kb_bucket = "be-awesome-dev-chatbot-knowledge-base"

    # Sync content between source posts bucket and the KB bucket
    sync_buckets_content(
        source_bucket=source_posts_bucket, dest_bucket=destination_kb_bucket
    )

    # Create the summary of all posts
    posts = get_posts_from_bucket(bucket=source_posts_bucket)
    summaries = generate_summaries(posts=posts, summary_chain=summariser_chain)

    print("Generating summary.md file")
    summary_output_file = "/tmp/summary.md"
    write_posts_summary_content(file_path=summary_output_file, summaries=summaries)

    # Upload summary to KB bucket
    upload_object_to_bucket(
        bucket_name=destination_kb_bucket,
        source_file_path=summary_output_file,
        bucket_file_path="summary.md",
    )

    print("Uploaded summary file to KB bucket")

    return 1
