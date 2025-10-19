import sys
from pathlib import Path

# Ensure the project root (the directory containing this script) is on sys.path
# so absolute imports like 'app.services...' resolve when running this file directly.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.services.ai_categorizer import predict_category

print(predict_category("Netflix"))
print(predict_category("ChatGPT Plus"))
print(predict_category("Adobe Creative Cloud"))
