from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import CohereEncoder
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')

load_dotenv()

# Initialize the encoder
encoder = CohereEncoder()
# Define FAQ route
faq = Route(
    name='faq',
    utterances=[
        "What is the return policy?",
        "How do I track my order?",
        "What payment methods are accepted?",
        "How can I contact customer support?",
        "Do you offer international shipping?"
    ],
)

# Define SQL route
sql = Route(
    name='sql',
    utterances=[
        "Show me the top 10 products for shoes",
        "What are the best-selling items in electronics?",
        "Are there any shoes under Rs. 3000?",
        "What is the price of products in the clothing category?",
    ]
)

# Initialize the router
r1 = SemanticRouter(routes=[faq, sql], encoder=encoder, auto_sync='local')

# 🚨 Build the index before querying
r1.index

# Test the router
if __name__ == "__main__":
    print(f"Name 1: {r1("When can I return my order").name}")      # Expected: 'faq'
    print(f"Name 2: {r1("Show me bags under Rs. 1000").name}")     # Expected: 'sql'
