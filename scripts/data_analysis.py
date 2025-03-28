"""
Data Analysis Module for Influencer-Brand Matching System
"""
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from transformers import pipeline
from config import DATA_DIR, update_progress

class InfluencerAnalyzer:
    def __init__(self, data_dir=DATA_DIR):
        self.data_dir = data_dir
        
        # Initialize sentiment analysis pipeline
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment"
        )
        
        # Initialize zero-shot classification pipeline for post categorization
        self.post_classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        
        # Common post categories
        self.categories = [
            "Fashion", "Beauty", "Lifestyle", "Travel", "Food", 
            "Fitness", "Tech", "Gaming", "Business", "Education",
            "Entertainment", "Arts", "Sports", "Health", "Parenting"
        ]
    
    def load_influencer_data(self, username):
        """Load the scraped data for a specific influencer"""
        file_path = os.path.join(self.data_dir, f"{username}_profile.json")
        
        if not os.path.exists(file_path):
            print(f"No data found for {username}. Please scrape the data first.")
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of the given text"""
        if not text or len(text.strip()) == 0:
            return {"label": "neutral", "score": 1.0}
        
        try:
            result = self.sentiment_analyzer(text)[0]
            return result
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {"label": "neutral", "score": 1.0}
    
    def categorize_post(self, caption):
        """Categorize a post based on its caption"""
        if not caption or len(caption.strip()) == 0:
            return {"label": "Uncategorized", "score": 1.0}
        
        try:
            result = self.post_classifier(caption, self.categories)
            return {
                "label": result["labels"][0],
                "score": result["scores"][0]
            }
        except Exception as e:
            print(f"Error categorizing post: {e}")
            return {"label": "Uncategorized", "score": 1.0}
    
    def analyze_influencer(self, username):
        """Analyze the influencer data and generate insights"""
        data = self.load_influencer_data(username)
        
        if not data:
            return None
        
        # Create an analysis results dictionary
        analysis = {
            "username": username,
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            "basic_metrics": {
                "followers": data["followers"],
                "following": data["following"],
                "posts_count": data["posts_count"],
                "engagement_rate": data["engagement_rate"]
            },
            "demographics": data.get("demographics", {}),
            "geographic_reach": data.get("geographic_reach", {}),
            "content_analysis": {
                "categories": {},
                "sentiment": {
                    "positive": 0,
                    "neutral": 0,
                    "negative": 0
                },
                "comment_sentiment": {
                    "positive": 0,
                    "neutral": 0,
                    "negative": 0
                },
                "posts": []
            },
            "language_distribution": {}
        }
        
        # Analyze posts and comments
        posts_df = pd.DataFrame(data["posts"])
        
        if len(posts_df) == 0:
            print(f"No posts found for {username}")
            return analysis
        
        # Process each post
        for idx, post in posts_df.iterrows():
            caption = post.get("caption", "")
            
            # Skip empty captions
            if not caption or len(caption.strip()) == 0:
                continue
            
            # Analyze post sentiment
            sentiment = self.analyze_sentiment(caption)
            sentiment_label = sentiment["label"]
            
            # Map sentiment labels to positive/neutral/negative
            if "positive" in sentiment_label or int(sentiment_label[0]) >= 4:
                sentiment_category = "positive"
            elif "negative" in sentiment_label or int(sentiment_label[0]) <= 2:
                sentiment_category = "negative"
            else:
                sentiment_category = "neutral"
            
            analysis["content_analysis"]["sentiment"][sentiment_category] += 1
            
            # Analyze comment sentiment if available
            if "comment_data" in post and post["comment_data"]:
                for comment in post["comment_data"]:
                    comment_text = comment.get("text", "")
                    if comment_text:
                        comment_sentiment = self.analyze_sentiment(comment_text)
                        comment_label = comment_sentiment["label"]
                        
                        if "positive" in comment_label or int(comment_label[0]) >= 4:
                            comment_category = "positive"
                        elif "negative" in comment_label or int(comment_label[0]) <= 2:
                            comment_category = "negative"
                        else:
                            comment_category = "neutral"
                        
                        analysis["content_analysis"]["comment_sentiment"][comment_category] += 1
            
            # Categorize post
            category = self.categorize_post(caption)
            category_label = category["label"]
            
            if category_label in analysis["content_analysis"]["categories"]:
                analysis["content_analysis"]["categories"][category_label] += 1
            else:
                analysis["content_analysis"]["categories"][category_label] = 1
            
            # Add post analysis
            post_analysis = {
                "post_id": post.get("post_id", ""),
                "likes": post.get("likes", 0),
                "comments": post.get("comments", 0),
                "sentiment": sentiment_label,
                "sentiment_score": sentiment["score"],
                "category": category_label,
                "category_score": category["score"],
                "engagement_rate": post.get("engagement_rate", 0),
                "posted_on": post.get("posted_on", "")
            }
            
            analysis["content_analysis"]["posts"].append(post_analysis)
        
        # Analyze language distribution
        if "posts" in data:
            lang_count = {}
            total_posts = len(data["posts"])
            
            for post in data["posts"]:
                lang = post.get("detected_language", "unknown")
                lang_count[lang] = lang_count.get(lang, 0) + 1
            
            # Convert to percentages
            analysis["language_distribution"] = {
                lang: (count / total_posts * 100) 
                for lang, count in lang_count.items()
            }
        
        # Save analysis to file
        analysis_file = os.path.join(self.data_dir, f"{username}_analysis.json")
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=4)
        
        print(f"Analysis for {username} saved to {analysis_file}")
        return analysis
    
    def generate_visualizations(self, username):
        """Generate visualizations from the analysis data"""
        analysis_file = os.path.join(self.data_dir, f"{username}_analysis.json")
        
        if not os.path.exists(analysis_file):
            analysis = self.analyze_influencer(username)
            if not analysis:
                return False
        else:
            with open(analysis_file, 'r', encoding='utf-8') as f:
                analysis = json.load(f)
        
        # Create visualization directory
        viz_dir = os.path.join(self.data_dir, f"{username}_visualizations")
        if not os.path.exists(viz_dir):
            os.makedirs(viz_dir)
            
        # Calculate comment sentiment percentages
        total_comments = sum(analysis["content_analysis"]["comment_sentiment"].values())
        if total_comments > 0:
            comment_sentiment = {
                k: (v / total_comments * 100)
                for k, v in analysis["content_analysis"]["comment_sentiment"].items()
            }
        
        # Set plotting style
        plt.style.use('ggplot')
        sns.set_palette("deep")
        
        # 1. Category Distribution Pie Chart
        if analysis["content_analysis"]["categories"]:
            plt.figure(figsize=(10, 6))
            categories = analysis["content_analysis"]["categories"]
            labels = list(categories.keys())
            sizes = list(categories.values())
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            plt.title(f'Content Category Distribution for @{username}')
            plt.tight_layout()
            plt.savefig(os.path.join(viz_dir, "category_distribution.png"))
            plt.close()
        
        # 2. Sentiment Analysis Pie Charts
        # Post sentiment
        plt.figure(figsize=(10, 6))
        sentiment = analysis["content_analysis"]["sentiment"]
        labels = list(sentiment.keys())
        sizes = list(sentiment.values())
        colors = ['green', 'gray', 'red']
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title(f'Post Sentiment Distribution for @{username}')
        plt.tight_layout()
        plt.savefig(os.path.join(viz_dir, "post_sentiment.png"))
        plt.close()
        
        # Comment sentiment (if available)
        if total_comments > 0:
            plt.figure(figsize=(10, 6))
            labels = list(comment_sentiment.keys())
            sizes = list(comment_sentiment.values())
            colors = ['green', 'gray', 'red']
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            plt.axis('equal')
            plt.title(f'Comment Sentiment Distribution for @{username}')
            plt.tight_layout()
            plt.savefig(os.path.join(viz_dir, "comment_sentiment.png"))
            plt.close()
        
        # 3. Language and Geographic Distribution Charts
        # Language distribution
        if analysis["language_distribution"]:
            plt.figure(figsize=(10, 6))
            languages = analysis["language_distribution"]
            langs = list(languages.keys())
            percentages = list(languages.values())
            
            # Sort by percentage (descending)
            sorted_indices = np.argsort(percentages)[::-1]
            langs = [langs[i] for i in sorted_indices]
            percentages = [percentages[i] for i in sorted_indices]
            
            plt.bar(langs, percentages)
            plt.xlabel('Language')
            plt.ylabel('Percentage (%)')
            plt.title(f'Language Distribution for @{username}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(viz_dir, "language_distribution.png"))
            plt.close()
            
        # Geographic reach
        if analysis["geographic_reach"]:
            plt.figure(figsize=(12, 6))
            locations = analysis["geographic_reach"]
            locs = list(locations.keys())
            counts = list(locations.values())
            
            # Sort by count (descending)
            sorted_indices = np.argsort(counts)[::-1]
            locs = [locs[i] for i in sorted_indices]
            counts = [counts[i] for i in sorted_indices]
            
            plt.bar(locs, counts)
            plt.xlabel('Location')
            plt.ylabel('Post Count')
            plt.title(f'Geographic Reach for @{username}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(viz_dir, "geographic_reach.png"))
            plt.close()
        
        # 4. Engagement Rate Trend Line
        if analysis["content_analysis"]["posts"]:
            plt.figure(figsize=(12, 6))
            posts = sorted(
                analysis["content_analysis"]["posts"],
                key=lambda x: x.get("posted_on", "")
            )
            
            dates = [post.get("posted_on", "") for post in posts]
            engagement_rates = [post.get("engagement_rate", 0) for post in posts]
            
            plt.plot(dates, engagement_rates, marker='o')
            plt.xlabel('Date')
            plt.ylabel('Engagement Rate (%)')
            plt.title(f'Engagement Rate Trend for @{username}')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(os.path.join(viz_dir, "engagement_trend.png"))
            plt.close()
        
        # 5. Likes vs Comments Scatter Plot
        if analysis["content_analysis"]["posts"]:
            plt.figure(figsize=(10, 6))
            likes = [post.get("likes", 0) for post in posts]
            comments = [post.get("comments", 0) for post in posts]
            
            plt.scatter(likes, comments, alpha=0.7)
            plt.xlabel('Likes')
            plt.ylabel('Comments')
            plt.title(f'Likes vs Comments for @{username}')
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(os.path.join(viz_dir, "likes_vs_comments.png"))
            plt.close()
        
        print(f"Visualizations for {username} generated in {viz_dir}")
        return True
    
    def generate_report(self, username):
        """Generate a markdown report from the analysis data"""
        analysis_file = os.path.join(self.data_dir, f"{username}_analysis.json")
        
        if not os.path.exists(analysis_file):
            analysis = self.analyze_influencer(username)
            if not analysis:
                return False
        else:
            with open(analysis_file, 'r', encoding='utf-8') as f:
                analysis = json.load(f)
        
        # Create visualization directory if it doesn't exist
        viz_dir = os.path.join(self.data_dir, f"{username}_visualizations")
        if not os.path.exists(viz_dir):
            self.generate_visualizations(username)
            
        # Calculate comment sentiment percentages
        total_comments = sum(analysis["content_analysis"]["comment_sentiment"].values())
        if total_comments > 0:
            comment_sentiment = {
                k: (v / total_comments * 100)
                for k, v in analysis["content_analysis"]["comment_sentiment"].items()
            }
        
        # Generate report
        report = f"""# Influencer Analysis Report: @{username}

## Basic Profile Metrics
- **Followers:** {analysis["basic_metrics"]["followers"]:,}
- **Following:** {analysis["basic_metrics"]["following"]:,}
- **Posts Count:** {analysis["basic_metrics"]["posts_count"]:,}
- **Average Engagement Rate:** {analysis["basic_metrics"]["engagement_rate"]}%

## Demographics
- **Estimated Age:** {analysis["demographics"].get("estimated_age", "N/A")}
- **Gender:** {analysis["demographics"].get("gender", "N/A")}

## Content Analysis

### Content Categories
"""
        
        # Add categories
        categories = analysis["content_analysis"]["categories"]
        if categories:
            for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                percentage = count / sum(categories.values()) * 100
                report += f"- **{category}:** {percentage:.1f}%\n"
        else:
            report += "- No category data available\n"
        
        # Add sentiment analysis
        report += """
### Content Sentiment
"""
        # Post sentiment
        sentiment = analysis["content_analysis"]["sentiment"]
        total_sentiment = sum(sentiment.values())
        if total_sentiment > 0:
            report += "\n#### Post Sentiment\n"
            for label, count in sentiment.items():
                percentage = count / total_sentiment * 100
                report += f"- **{label.capitalize()}:** {percentage:.1f}%\n"
        else:
            report += "- No post sentiment data available\n"
            
        # Comment sentiment
        if total_comments > 0:
            report += "\n#### Comment Sentiment\n"
            for label, percentage in comment_sentiment.items():
                report += f"- **{label.capitalize()}:** {percentage:.1f}%\n"
        else:
            report += "- No comment sentiment data available\n"
        
        # Add language distribution
        report += """
### Language & Geographic Distribution
"""
        # Language distribution
        languages = analysis["language_distribution"]
        if languages:
            report += "\n#### Language Distribution\n"
            for lang, percentage in sorted(languages.items(), key=lambda x: x[1], reverse=True):
                report += f"- **{lang}:** {percentage:.1f}%\n"
        else:
            report += "- No language data available\n"
            
        # Geographic reach
        locations = analysis["geographic_reach"]
        if locations:
            report += "\n#### Geographic Reach\n"
            for loc, count in sorted(locations.items(), key=lambda x: x[1], reverse=True):
                report += f"- **{loc}:** {count} posts\n"
        else:
            report += "- No geographic data available\n"
        
        # Add engagement insights
        report += """
## Engagement Insights
"""
        
        if analysis["content_analysis"]["posts"]:
            posts = analysis["content_analysis"]["posts"]
            engagement_rates = [post.get("engagement_rate", 0) for post in posts]
            
            if engagement_rates:
                avg_engagement = sum(engagement_rates) / len(engagement_rates)
                max_engagement = max(engagement_rates)
                min_engagement = min(engagement_rates)
                
                report += f"- **Average Engagement Rate:** {avg_engagement:.2f}%\n"
                report += f"- **Highest Engagement Rate:** {max_engagement:.2f}%\n"
                report += f"- **Lowest Engagement Rate:** {min_engagement:.2f}%\n"
        else:
            report += "- No engagement data available\n"
        
        # Add top performing posts
        report += """
### Top Performing Posts
"""
        
        if analysis["content_analysis"]["posts"]:
            # Sort posts by engagement rate
            top_posts = sorted(
                analysis["content_analysis"]["posts"],
                key=lambda x: x.get("engagement_rate", 0),
                reverse=True
            )[:3]  # Top 3 posts
            
            for i, post in enumerate(top_posts, 1):
                report += f"""
#### Top Post #{i}
- **Engagement Rate:** {post.get("engagement_rate", 0):.2f}%
- **Likes:** {post.get("likes", 0):,}
- **Comments:** {post.get("comments", 0):,}
- **Category:** {post.get("category", "Unknown")}
- **Sentiment:** {post.get("sentiment", "Unknown")}
- **Posted On:** {post.get("posted_on", "Unknown")}
"""
        else:
            report += "- No post data available\n"
        
        # Add report footer
        report += f"""
## Summary
This report provides an analysis of the Instagram account @{username} based on recent posts. 
The analysis includes engagement metrics, content categorization, sentiment analysis, 
and language distribution.

Report generated on: {datetime.now().strftime("%Y-%m-%d")}
"""
        
        # Save report to file
        report_file = os.path.join(self.data_dir, f"{username}_report.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"Analysis report for {username} saved to {report_file}")
        return report_file

# Example usage
if __name__ == "__main__":
    analyzer = InfluencerAnalyzer()
    
    # Get influencer username
    username = input("Enter Instagram username to analyze: ")
    
    if username:
        # Analyze influencer data
        analysis = analyzer.analyze_influencer(username)
        
        if analysis:
            # Generate visualizations
            analyzer.generate_visualizations(username)
            
            # Generate report
            report_file = analyzer.generate_report(username)
            
            if report_file:
                print(f"Analysis completed successfully for {username}.")
                update_progress("step_2_data_analysis", "completed")
            else:
                print(f"Failed to generate report for {username}.")
        else:
            print(f"Analysis failed for {username}.")
    else:
        print("No username provided. Exiting...")
