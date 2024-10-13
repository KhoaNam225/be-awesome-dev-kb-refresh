from typing import List
import boto3

from models.post import Post


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
