"""
Pricing Calculator for Influencer Partnerships
"""

def calculate_pricing(brand, influencer) -> dict:
    """
    Calculate pricing range for influencer partnership based on:
    - Product cost
    - ROI expectation
    - Influencer reach
    Returns dictionary with min and max price suggestions
    
    Args:
        brand: Brand object containing product_cost and roi_expectation
        influencer: Influencer object containing average_reach
        
    Returns:
        dict: {'min_price': float, 'max_price': float, 'recommended_price': float}
    """
    # Worst case scenario (5% engagement, 1% conversion)
    min_price = (
        (0.05 * influencer.average_reach) * 
        (0.01) * 
        (brand.product_cost * (1 + brand.roi_expectation/100))
    )
    
    # Best case scenario (15% engagement, 3% conversion)
    max_price = (
        (0.15 * influencer.average_reach) * 
        (0.03) * 
        (brand.product_cost * (1 + brand.roi_expectation/100))
    )
    
    return {
        'min_price': round(min_price, 2),
        'max_price': round(max_price, 2),
        'recommended_price': round((min_price + max_price) / 2, 2)
    }
