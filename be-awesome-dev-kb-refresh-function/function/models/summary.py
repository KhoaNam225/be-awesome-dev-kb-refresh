from pydantic import BaseModel, Field


class Summary(BaseModel):
    """The summary of the content, including the main topic and the summarised content"""

    main_topic: str = Field(
        description="The overall topic of the whole article, this should be only 10 words long at maximum",
    )
    summary_content: str = Field(
        description="The content of the summary, this should be very concise and should only be 10 sentences max in length.",
    )
