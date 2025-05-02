# SIFT Logo Detection

This script performs feature matching using the **SIFT** algorithm. SIFT (Scale-Invariant Feature Transform) is chosen for both detection and description of points of interest (PoIs) due to its robustness against scale, rotation, and illumination changes. For feature matching, **FLANN-based matcher** is employed using OpenCV’s `cv2.FlannBasedMatcher`, with Lowe’s ratio test for filtering good matches.

## Data
A feature match is done between a Lakers logo and a full-frame basketball game screenshot.

### Reference Logo
![Lakers Logo](https://github.com/diyanair1/SIFT_logo_detection/blob/4cc2d32b11d67cf06380d578752e8ee586e83899/logo.jpg)

Fig. 1. Reference image of the Los Angeles Lakers logo.

### Frame from Broadcast
![Lakers Game](https://github.com/diyanair1/SIFT_logo_detection/blob/4cc2d32b11d67cf06380d578752e8ee586e83899/lakers_game.png)

Fig. 2. Frame from a basketball game broadcast, showing the Lakers logo on the scoreboard.

### SIFT Feature Matching Results
![Point correspondences using FLANN matcher.](https://github.com/diyanair1/SIFT_logo_detection/blob/4cc2d32b11d67cf06380d578752e8ee586e83899/feature_match.png)
