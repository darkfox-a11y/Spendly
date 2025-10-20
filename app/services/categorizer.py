# app/services/categorizer_service.py
from typing import Optional

# Predefined keyword-based domain mapping
CATEGORY_KEYWORDS = {
    "Entertainment": [
        "netflix", "spotify", "youtube", "hotstar", "prime", "disney", "hbo",
        "crunchyroll", "zee5", "mxplayer", "sony", "gaana"
    ],
    "Productivity": [
        "notion", "slack", "asana", "trello", "clickup", "monday", "todoist",
        "evernote", "zoom", "loom", "google workspace", "office", "microsoft 365"
    ],
    "Cloud & Storage": [
        "google one", "icloud", "dropbox", "onedrive", "mega", "pcloud", "aws",
        "azure", "gcp"
    ],
    "Design & Editing": [
        "adobe", "canva", "figma", "sketch", "premiere", "final cut", "lightroom",
        "photoshop", "illustrator", "davinci"
    ],
    "Finance & Business": [
        "quickbooks", "xero", "zoho books", "razorpay", "stripe", "paypal",
        "intuit", "wise", "revolut"
    ],
    "Utilities": [
        "electricity", "water", "internet", "wifi", "broadband", "jio", "airtel",
        "vi", "phone", "sim", "mobile", "data", "bsnl"
    ],
    "Gaming": [
        "playstation", "xbox", "steam", "epic", "game pass", "riot", "ea", "ubisoft"
    ],
    "AI Tools": [
        "chatgpt", "claude", "midjourney", "runway", "notion ai", "copilot",
        "github copilot", "perplexity", "firefly", "gemini"
    ],
    "Education": [
        "udemy", "coursera", "edx", "skillshare", "khan", "byjus", "unacademy",
        "brilliant", "datacamp"
    ],
    "Health & Fitness": [
        "fitbit", "myfitnesspal", "strava", "nike training", "headspace", "calm"
    ],
    "Other": []
}


def categorize_service(name: str, description: Optional[str] = None) -> str:
    """
    Determine a category for a given service name/description.
    Returns 'Other' if no keywords match.
    """
    text = f"{name} {description or ''}".lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return category

    return "Other"
