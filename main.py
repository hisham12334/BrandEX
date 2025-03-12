"""
Main application for the Influencer-Brand Matching System
"""
import os
import json
from scripts.data_collection import InfluencerScraper
from scripts.data_analysis import InfluencerAnalyzer
from config import DATA_DIR, update_progress

def init

def init_project():
    """Initialize the project and create necessary directories"""
    # Create data directory if it doesn't exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Create progress file if it doesn't exist
    progress_file = os.path.join(DATA_DIR, "project_progress.json")
    if not os.path.exists(progress_file):
        with open(progress_file, 'w') as f:
            from config import PROJECT_PROGRESS
            json.dump(PROJECT_PROGRESS, f, indent=4)
    
    print("Project initialized successfully.")

def run_data_collection():
    """Run the data collection module"""
    scraper = InfluencerScraper(save_dir=DATA_DIR)
    
    # Get list of influencers to scrape
    influencers = input("Enter comma-separated list of Instagram usernames to scrape: ").split(',')
    influencers = [username.strip() for username in influencers]
    
    # Track successful scrapes
    successful = 0
    
    for influencer in influencers:
        if influencer:
            print(f"\nScraping profile for: {influencer}")
            profile_data = scraper.scrape_profile(influencer)
            
            if profile_data:
                lang_dist = scraper.analyze_language_distribution(profile_data)
                print("\nLanguage Distribution:")
                for lang, percentage in lang_dist.items():
                    print(f"{lang}: {percentage:.2f}%")
                
                print(f"\nBasic Profile Stats for {influencer}:")
                print(f"Followers: {profile_data['followers']}")
                print(f"Posts: {profile_data['posts_count']}")
                print(f"Avg. Engagement Rate: {profile_data['engagement_rate']}%")
                successful += 1
    
    if successful > 0:
        update_progress("step_1_data_collection", "completed")
        print(f"\nData collection completed successfully for {successful} influencers.")
    else:
        print("\nNo data was collected. Please check your inputs and try again.")

if __name__ == "__main__":
    init_project()
    
    print("Influencer-Brand Matching System")
    print("================================")
    print("1. Run Data Collection")
    print("2. Exit")
    
    choice = input("\nEnter your choice (1-2): ")
    
    if choice == "1":
        run_data_collection()
    else:
        print("Exiting program...")