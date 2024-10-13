from typing import List
import logging
import boto3

from models.post import Post
from models.summary import Summary


def get_posts_from_bucket(bucket: str) -> List[Post]:
    s3_client = boto3.client("s3")
    post_objects = list(
        filter(
            lambda object: object["Key"].endswith(".md"),
            s3_client.list_objects_v2(Bucket=bucket).get("Contents", []),
        )
    )
    filenames = list(map(lambda object: object["Key"], post_objects))

    posts: List[Post] = []

    for name in filenames:
        object = s3_client.get_object(Bucket=bucket, Key=name)
        content = object["Body"].read().decode("utf-8")

        new_post = Post(content=content, filename=name)
        posts.append(new_post)

    return posts


def clear_bucket_content(bucket: str) -> bool:
    print(f"Clearing content of bucket {bucket}")
    s3_client = boto3.client("s3")
    objects = s3_client.list_objects_v2(Bucket=bucket).get("Contents", [])
    delete_request = {
        "Objects": list(map(lambda obj: {"Key": obj["Key"]}, objects)),
        "Quiet": False,
    }
    s3_client.delete_objects(Bucket=bucket, Delete=delete_request)
    print(f"Content of bucket {bucket} cleared")

    return True


def copy_bucket_content_from_source(source_bucket: str, dest_bucket: str) -> bool:
    print(f"Copying content of bucket {source_bucket} to bucket {dest_bucket}")

    s3_client = boto3.client("s3")
    source_objects = s3_client.list_objects_v2(Bucket=source_bucket).get("Contents", [])

    for obj in source_objects:
        copy_source = {"Bucket": source_bucket, "Key": obj["Key"]}
        s3_client.copy_object(
            CopySource=copy_source, Bucket=dest_bucket, Key=obj["Key"]
        )
    print(f"Copy content of bucket {source_bucket} to bucket {dest_bucket} completed")
    return True


def sync_buckets_content(source_bucket: str, dest_bucket: str) -> bool:
    print(f"Starting syncing content between bucket {source_bucket} and {dest_bucket}")

    clear_bucket_content(dest_bucket)
    copy_bucket_content_from_source(
        source_bucket=source_bucket, dest_bucket=dest_bucket
    )

    print(f"Finished syncing content between bucket {source_bucket} and {dest_bucket}")

    return True


def write_posts_summary_content(file_path: str, summaries: List[Summary]) -> bool:
    print(f"Starting writing summary content to file {file_path}")
    with open(file_path, "w", encoding="utf-8") as output_file:
        for s in summaries:
            output_file.write(f"Topic: {s.main_topic}\n")
            output_file.write(f"Summary:\n{s.summary_content}\n\n")
            output_file.write("\n\n===================================\n\n")
            print(f"Written summary content of {s.main_topic} to file")

    return True


def upload_object_to_bucket(
    bucket_name: str, source_file_path: str, bucket_file_path: str
) -> bool:
    print(
        f"Uploading file {source_file_path} to bucket {bucket_name} as {bucket_file_path}"
    )
    s3_client = boto3.client("s3")
    s3_client.upload_file(
        Filename=source_file_path, Bucket=bucket_name, Key=bucket_file_path
    )

    return True
