import cv2
import numpy as np


def match_stars(image1, image2):
    # Resize images to the same dimensions
    image1 = cv2.resize(image1, (640, 480))
    image2 = cv2.resize(image2, (640, 480))

    # Convert images to grayscale
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Detect keypoints and compute descriptors using ORB
    orb = cv2.ORB_create()
    keypoints1, descriptors1 = orb.detectAndCompute(gray1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(gray2, None)

    # Create a BFMatcher object
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match keypoints between the two images
    matches = matcher.match(descriptors1, descriptors2)

    # Sort the matches by distance
    matches = sorted(matches, key=lambda x: x.distance)

    # Filter matches using triangular matching
    good_matches = []
    for match1 in matches:
        # Get the keypoints for the matched stars
        kp1 = keypoints1[match1.queryIdx]
        kp2 = keypoints2[match1.trainIdx]

        for match2 in matches:
            if match1 != match2:
                kp3 = keypoints1[match2.queryIdx]
                kp4 = keypoints2[match2.trainIdx]

                # Calculate similarity between triangles
                sim = calculate_triangle_similarity(kp1, kp2, kp3, kp4)

                # Filter matches based on similarity threshold
                if sim > 0.8:
                    good_matches.append(match1)
                    good_matches.append(match2)
                    break

    # Draw lines between the matched stars
    result = np.hstack((image1, image2))
    for match in good_matches:
        # Get the keypoints for the matched stars
        kp1 = keypoints1[match.queryIdx]
        kp2 = keypoints2[match.trainIdx]

        # Draw a line between the matched stars with a thicker line (e.g., thickness=4)
        pt1 = (int(kp1.pt[0]), int(kp1.pt[1]))
        pt2 = (int(kp2.pt[0]) + image1.shape[1], int(kp2.pt[1]))
        cv2.line(result, pt1, pt2, (0, 255, 0), thickness=4)
    cv2.imwrite('../static/post_track/star_match_result.jpg', result)
    # Display the result image
    # cv2.imshow("Star Matching", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def calculate_triangle_similarity(kp1, kp2, kp3, kp4):
    # Calculate similarity between two triangles
    sim = cv2.matchShapes(np.float32([kp1.pt, kp2.pt, kp3.pt]), np.float32([kp2.pt, kp3.pt, kp4.pt]),
                          cv2.CONTOURS_MATCH_I1, 0)
    return sim


image1 = cv2.imread("../static/uploads/1.jpg")
image2 = cv2.imread("../static/uploads/2.jpg")

# Call the function to match stars between the images
match_stars(image1, image2)
