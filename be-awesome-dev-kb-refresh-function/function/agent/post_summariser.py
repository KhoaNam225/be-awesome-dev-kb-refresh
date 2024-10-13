from utils.llm_utils import init_chat_model, init_summary_chain
from models.summary import Summary


bedrock_llm = init_chat_model().with_structured_output(Summary)
summariser_chain = init_summary_chain(llm=bedrock_llm)
