"""
Configuration settings for the Influencer-Brand Matching System
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Instagram credentials (if needed)
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")

# Google Vision API key (if needed)
GOOGLE_VISION_API_KEY = os.getenv("GOOGLE_VISION_API_KEY", "")

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Supported languages
SUPPORTED_LANGUAGES = ["en", "hi", "ml"]

# Data storage
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Project progress tracking
PROJECT_PROGRESS = {
    "step_1_data_collection": "in_progress",
    "step_2_data_analysis": "pending",
    "step_3_brand_matching": "pending",
    "step_4_outreach": "pending",
    "step_5_campaign_tracking": "pending"
}

def update_progress(step, status):
    """Update the progress of a specific step"""
    if step in PROJECT_PROGRESS:
        PROJECT_PROGRESS[step] = status
        
        # Save progress to a file
        progress_file = os.path.join(DATA_DIR, "project_progress.json")
        
        # Create DATA_DIR if it doesn't exist
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            
        with open(progress_file, 'w') as f:
            import json
            json.dump(PROJECT_PROGRESS, f, indent=4)
        
        return True
    return False