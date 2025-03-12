"""
Data Collection Module for Influencer-Brand Matching System
"""
import os
import json
import instaloader
import pandas as pd
from datetime import datetime
from transformers import pipeline

class InfluencerScraper:
    def __init__(self, save_dir="data"):
        """Initialize the scraper"""
        self.instance = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=True,
            save_metadata=True
        )
        self.save_dir = save_dir
        
        # Create data directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        # Initialize language detection pipeline
        self.language_detector = pipeline(
            "text-classification", 
            model="papluca/xlm-roberta-base-language-detection"
        )
            
    def login(self, username, password):
        """Login to Instagram (optional, for private profiles)"""
        try:
            self.instance.login(username, password)
            print("Login successful")
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False
            
    def scrape_profile(self, username):
        """Scrape profile data for a given Instagram username"""
        try:
            profile = instaloader.Profile.from_username(self.instance.context, username)
            
            # Basic profile metrics
            profile_data = {
                "username": profile.username,
                "full_name": profile.full_name,
                "biography": profile.biography,
                "followers": profile.followers,
                "following": profile.followees,
                "posts_count": profile.mediacount,
                "is_business": profile.is_business_account,
                "business_category": profile.business_category_name,
                "scrape_date": datetime.now().strftime("%Y-%m-%d"),
            }
            
            # Calculate engagement rate based on last 12 posts
            posts_data = []
            engagement_sum = 0
            post_count = 0
            
            print(f"Scraping posts for {username}...")
            for post in profile.get_posts():
                if post_count >= 12:
                    break
                
                # Extract post data
                post_data = {
                    "post_id": post.shortcode,
                    "post_url": f"https://www.instagram.com/p/{post.shortcode}/",
                    "likes": post.likes,
                    "comments": post.comments,
                    "caption": post.caption if post.caption else "",
                    "hashtags": post.caption_hashtags if post.caption else [],
                    "posted_on": post.date.strftime("%Y-%m-%d"),
                }
                
                # Detect language
                if post.caption:
                    try:
                        language_result = self.language_detector(post.caption)
                        post_data["detected_language"] = language_result[0]["label"]
                        post_data["language_confidence"] = language_result[0]["score"]
                    except:
                        post_data["detected_language"] = "unknown"
                        post_data["language_confidence"] = 0.0
                
                # Calculate engagement for this post
                post_engagement = (post.likes + post.comments) / profile.followers if profile.followers > 0 else 0
                post_data["engagement_rate"] = post_engagement * 100  # as percentage
                
                engagement_sum += post_engagement
                post_count += 1
                posts_data.append(post_data)
            
            # Calculate average engagement rate
            avg_engagement_rate = 0
            if post_count > 0:
                avg_engagement_rate = (engagement_sum / post_count) * 100  # as percentage
            
            profile_data["engagement_rate"] = round(avg_engagement_rate, 2)
            profile_data["posts"] = posts_data
            
            # Save profile data to JSON
            profile_file = os.path.join(self.save_dir, f"{username}_profile.json")
            with open(profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, ensure_ascii=False, indent=4)
            
            print(f"Profile data for {username} saved to {profile_file}")
            return profile_data
            
        except Exception as e:
            print(f"Error scraping profile for {username}: {e}")
            return None
    
    def analyze_language_distribution(self, profile_data):
        """Analyze language distribution in the posts"""
        if not profile_data or "posts" not in profile_data:
            return {}
        
        lang_count = {}
        total_posts = len(profile_data["posts"])
        
        for post in profile_data["posts"]:
            lang = post.get("detected_language", "unknown")
            lang_count[lang] = lang_count.get(lang, 0) + 1
        
        # Convert to percentages
        lang_distribution = {
            lang: (count / total_posts * 100) 
            for lang, count in lang_count.items()
        }
        
        return lang_distribution

# Example usage
if __name__ == "__main__":
    scraper = InfluencerScraper()
    
    # Optional: Login (only needed for private profiles)
    # scraper.login("your_username", "your_password")
    
    # Scrape profile
    influencer = input("Enter Instagram username to scrape: ")
    profile_data = scraper.scrape_profile(influencer)
    
    if profile_data:
        # Analyze language distribution
        lang_dist = scraper.analyze_language_distribution(profile_data)
        print("\nLanguage Distribution:")
        for lang, percentage in lang_dist.items():
            print(f"{lang}: {percentage:.2f}%")
        
        # Basic profile stats
        print(f"\nBasic Profile Stats for {influencer}:")
        print(f"Followers: {profile_data['followers']}")
        print(f"Posts: {profile_data['posts_count']}")
        print(f"Avg. Engagement Rate: {profile_data['engagement_rate']}%")