"""
Brand-Influencer Matching System
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from .pricing_calculator import calculate_pricing

@dataclass
class Brand:
    """Represents a brand looking for influencer partnerships"""
    name: str
    industry: str  # Fashion, Tech, Food etc.
    target_audience: Dict[str, str]  # {age: "18-25", gender: "male", location: "IN"}
    product_cost: float  # Cost per product in ₹
    roi_expectation: float  # Expected ROI percentage (e.g., 20 for 20%)

@dataclass
class Influencer:
    """Represents an influencer available for brand partnerships"""
    name: str
    content_type: str
    audience_stats: Dict[str, str]  # {age: "18-25", gender: "male", location: "IN"}
    average_reach: int  # Average number of people reached per post

def match_brands_to_influencers(brands: List[Brand], influencers: List[Influencer]) -> Dict[Brand, List[Influencer]]:
    """
    Match brands to suitable influencers based on:
    - Audience demographics alignment
    - Location alignment
    Returns dictionary of brand to list of matched influencers
    """
    matches = {}
    
    for brand in brands:
        matched_influencers = []
        for influencer in influencers:
            # Check audience match
            audience_match = all(
                influencer.audience_stats[key] == brand.target_audience[key]
                for key in brand.target_audience
            )
            
            # Check location match
            location_match = (
                influencer.audience_stats.get('location') == 
                brand.target_audience.get('location')
            )
            
            if audience_match and location_match:
                matched_influencers.append(influencer)
        
        matches[brand] = matched_influencers
    
    return matches

def get_matches_with_pricing(brands: List[Brand], influencers: List[Influencer]) -> Dict[Brand, Dict[Influencer, Dict[str, float]]]:
    """
    Get matches with pricing suggestions for each brand-influencer pair
    Returns nested dictionary with pricing details
    """
    matches = match_brands_to_influencers(brands, influencers)
    result = {}
    
    for brand, matched_influencers in matches.items():
        pricing_details = {}
        for influencer in matched_influencers:
            pricing_details[influencer] = calculate_pricing(brand, influencer)
        result[brand] = pricing_details
    
    return result
