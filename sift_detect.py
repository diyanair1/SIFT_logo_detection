# This script performs feature matching using the SIFT algorithm
# between a logo image and a game screenshot. 
# 
# It uses the FLANN-based matcher to find point correspondences, 
# visualizes the results, computes match quality scores, and filters out low-confidence matches.

import cv2
import numpy as np
from matplotlib import pyplot as plt

def expand(logo_path, scale_percent, output_path=None):
    # Read the image
    img = cv2.imread(logo_path)
    
    if img is None:
        print("Error: Unable to load image.")
        return

    # Get original dimensions
    height, width = img.shape[:2]

    # Calculate new dimensions
    nwidth = int(img.shape[1] * scale_percent / 100)
    nheight = int(img.shape[0] * scale_percent / 100)
    new_dim = (nwidth, nheight)

    # Resize image
    resized = cv2.resize(img, new_dim, interpolation=cv2.INTER_AREA)

    # Save image and return output path
    if output_path:
        cv2.imwrite(output_path, resized)
        print(f"Reduced resolution image saved to: {output_path}")
        return output_path
    else:
        print("Reduced resolution image not saved. Use output_path to save!")
    

def sift_feature_matching(logo_path, screenshot_path):
    # Load the images
    logo = cv2.imread(logo_path, cv2.IMREAD_GRAYSCALE)
    screenshot = cv2.imread(screenshot_path, cv2.IMREAD_GRAYSCALE)
    
    if logo is None or screenshot is None:
        print("Error: Could not load images")
        return
    
    # Initialize SIFT detector
    sift = cv2.SIFT_create()
    
    # Find keypoints and descriptors
    kp1, des1 = sift.detectAndCompute(logo, None)
    kp2, des2 = sift.detectAndCompute(screenshot, None)
    
    # FLANN parameters and matcher 
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    
    # Apply ratio test to filter good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)
    
    # Draw matches
    img_matches = cv2.drawMatches(
        logo, kp1, 
        screenshot, kp2, 
        good_matches, None, 
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    # Show the result
    plt.figure(figsize=(20, 10))
    plt.imshow(img_matches, cmap='gray')
    plt.title('SIFT Feature Matching Results')
    plt.axis('off')
    plt.show()
    
    # Print matching statistics
    print(f"\nTotal keypoints in logo: {len(kp1)}")
    print(f"Total keypoints in screenshot: {len(kp2)}")
    print(f"Good matches found: {len(good_matches)}\n")
    
    # After FLANN matching, calculate normalized scores  
    match_scores = [m.distance for m in good_matches]  
    max_distance = max(match_scores) if match_scores else 0  
    normalized_scores = [round(100 * (1 - m.distance / max_distance), 2) for m in good_matches]  

    print(f"\nMatch quality scores: {normalized_scores}")  
    print(f"Average score: {np.mean(normalized_scores):.1f}/100\n") 

    # Keep only high-confidence matches (e.g., >60/100)  
    high_confidence_matches = [
        m for m, score in zip(good_matches, normalized_scores)
        if score > 60
    ]
    print(f"High-confidence matches: {len(high_confidence_matches)}\n")  


# Run the matching
known_logo = expand('/Users/diya/Desktop/Git/SIFT_logo_detection/logos/Los_Angeles_Lakers_processed.jpg', scale_percent=300, output_path="logo.jpg")

known_cropped_logo = '/Users/diya/Desktop/Git/SIFT_logo_detection/lakers_game.png'
sift_feature_matching(known_logo, known_cropped_logo)

