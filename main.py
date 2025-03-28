"""
Main application for the Influencer-Brand Matching System
"""
import os
import json
from scripts.data_collection import InfluencerScraper
from scripts.data_analysis import InfluencerAnalyzer
from config import DATA_DIR, update_progress

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

def run_data_analysis():
    """Run the data analysis module"""
    analyzer = InfluencerAnalyzer(data_dir=DATA_DIR)
    
    # Check if there are any influencer profiles scraped already
    profile_files = [f for f in os.listdir(DATA_DIR) if f.endswith('_profile.json')]
    
    if not profile_files:
        print("No influencer data found. Please run data collection first.")
        return
    
    # Extract usernames from filenames
    available_influencers = [f.replace('_profile.json', '') for f in profile_files]
    
    print(f"\nFound data for {len(available_influencers)} influencers:")
    for idx, influencer in enumerate(available_influencers, 1):
        print(f"{idx}. {influencer}")
    
    # Get user choice
    choice = input("\nEnter influencer number to analyze, or 'all' for all: ")
    
    influencers_to_analyze = []
    if choice.lower() == 'all':
        influencers_to_analyze = available_influencers
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(available_influencers):
                influencers_to_analyze = [available_influencers[idx]]
            else:
                print("Invalid selection.")
                return
        except ValueError:
            print("Invalid input. Please enter a number or 'all'.")
            return
    
    # Track successful analyses
    successful = 0
    
    for influencer in influencers_to_analyze:
        print(f"\nAnalyzing profile for: {influencer}")
        
        # Run analysis
        analysis = analyzer.analyze_influencer(influencer)
        if analysis:
            # Generate visualizations
            viz_success = analyzer.generate_visualizations(influencer)
            
            # Generate report
            report_file = analyzer.generate_report(influencer)
            
            if report_file and viz_success:
                print(f"Analysis completed successfully for {influencer}.")
                successful += 1
                
                # Ask if user wants to view report
                view_report = input(f"Would you like to see the report for {influencer}? (y/n): ")
                if view_report.lower() == 'y':
                    with open(report_file, 'r', encoding='utf-8') as f:
                        print("\n" + "="*50)
                        print(f.read())
                        print("="*50)
    
    if successful > 0:
        update_progress("step_2_data_analysis", "completed")
        print(f"\nData analysis completed successfully for {successful} influencers.")
    else:
        print("\nNo analysis was completed. Please check your inputs and try again.")

def display_menu():
    """Display main menu"""
    print("\nInfluencer-Brand Matching System")
    print("================================")
    print("1. Run Data Collection")
    print("2. Run Data Analysis & Insights")
    print("3. View Project Progress")
    print("4. Exit")
    
    return input("\nEnter your choice (1-4): ")

def view_progress():
    """View current project progress"""
    progress_file = os.path.join(DATA_DIR, "project_progress.json")
    
    if not os.path.exists(progress_file):
        print("Progress file not found. Initializing project...")
        init_project()
    
    with open(progress_file, 'r') as f:
        progress = json.load(f)
    
    print("\nProject Progress:")
    print("================")
    
    steps = {
        "step_1_data_collection": "Step 1: Data Collection",
        "step_2_data_analysis": "Step 2: Data Analysis & Insights",
        "step_3_brand_matching": "Step 3: Brand Matching Algorithm",
        "step_4_outreach": "Step 4: Brand Outreach",
        "step_5_campaign_tracking": "Step 5: Campaign Tracking"
    }
    
    status_emoji = {
        "completed": "✅",
        "in_progress": "🔄",
        "pending": "⏳"
    }
    
    for step_key, step_name in steps.items():
        status = progress.get(step_key, "pending")
        emoji = status_emoji.get(status, "⏳")
        print(f"{emoji} {step_name}: {status.replace('_', ' ').title()}")

if __name__ == "__main__":
    init_project()
    
    while True:
        choice = display_menu()
        
        if choice == "1":
            run_data_collection()
        elif choice == "2":
            run_data_analysis()
        elif choice == "3":
            view_progress()
        elif choice == "4":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")