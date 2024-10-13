import boto3


def sync_knowledge_base_with_data_source(kb_id: str, data_source_id: str) -> bool:
    boto_session = boto3.Session(region_name="us-east-1")
    bedrock_client = boto_session.client("bedrock-agent")

    bedrock_client.start_ingestion_job(
        dataSourceId=data_source_id,
        knowledgeBaseId=kb_id,
        description="Sync from lambda",
    )

    return True
