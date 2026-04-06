"""
Service Photo URLs with fallback images
All images are from reliable CDNs that work globally
"""

SERVICE_PHOTOS = {
    # Venue Photos
    'venue_banquet': 'https://images.unsplash.com/photo-1519167758993-a0ac84e35b98?w=400&h=300&fit=crop',
    'venue_garden': 'https://images.unsplash.com/photo-1519671482677-16ae8f00f3f9?w=400&h=300&fit=crop',
    'venue_rooftop': 'https://images.unsplash.com/photo-1519634592104-3fed9a4f92c2?w=400&h=300&fit=crop',
    
    # Catering Photos
    'catering_buffet': 'https://images.unsplash.com/photo-1504674900769-a86cc1d7c0c0?w=400&h=300&fit=crop',
    'catering_dinner': 'https://images.unsplash.com/photo-1467093528519-e21cc028cb29?w=400&h=300&fit=crop',
    'catering_cocktail': 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=400&h=300&fit=crop',
    
    # Photography Photos
    'photo_photography': 'https://images.unsplash.com/photo-1502123656149-3520287d726d?w=400&h=300&fit=crop',
    'photo_videography': 'https://images.unsplash.com/photo-1499978306869-87d7195277c0?w=400&h=300&fit=crop',
    'photo_booth': 'https://images.unsplash.com/photo-1516035069371-29ad0afe3f3d?w=400&h=300&fit=crop',
    
    # Decoration Photos
    'decor_floral': 'https://images.unsplash.com/photo-1546182990-dffeafbe841d?w=400&h=300&fit=crop',
    'decor_lighting': 'https://images.unsplash.com/photo-1516565143236-c5a48f118e4a?w=400&h=300&fit=crop',
    'decor_balloons': 'https://images.unsplash.com/photo-1551638820-7dd773b36987?w=400&h=300&fit=crop',
    
    # Music Photos
    'music_dj4': 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=400&h=300&fit=crop',
    'music_dj8': 'https://images.unsplash.com/photo-1487180144351-b8472da7d491?w=400&h=300&fit=crop',
    'music_band': 'https://images.unsplash.com/photo-1539571696357-5a69c006ae30?w=400&h=300&fit=crop',
}

# Fallback placeholder image (gray placeholder)
PLACEHOLDER_IMAGE = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="300"%3E%3Crect fill="%23e0e0e0" width="400" height="300"/%3E%3Ctext x="50%25" y="50%25" text-anchor="middle" dy=".3em" fill="%23999" font-family="Arial" font-size="16"%3EService Photo%3C/text%3E%3C/svg%3E'
