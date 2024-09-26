import requests
import re
import argparse

def get_user_info(identifier, by_id=False):
    if by_id:
        # URL for user ID
        url = f"https://www.tiktok.com/@{identifier}"
    else:
        # Remove the @ symbol if present
        if identifier.startswith('@'):
            identifier = identifier[1:]
        # URL for username
        url = f"https://www.tiktok.com/@{identifier}"

    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        
        # Regular expressions to extract information
        user_info_pattern = r'"webapp.user-detail":{"userInfo":{"user":{"id":"(\d+)"'
        unique_id_pattern = r'"uniqueId":"(.*?)"'
        nickname_pattern = r'"nickname":"(.*?)"'
        followers_pattern = r'"followerCount":(\d+)'
        following_pattern = r'"followingCount":(\d+)'
        likes_pattern = r'"heartCount":(\d+)'
        videos_pattern = r'"videoCount":(\d+)'
        signature_pattern = r'"signature":"(.*?)"'
        verified_pattern = r'"verified":(true|false)'
        secUid_pattern = r'"secUid":"(.*?)"'
        commentSetting_pattern = r'"commentSetting":(\d+)'
        privateAccount_pattern = r'"privateAccount":(true|false)'
        region_pattern = r'"region":"(.*?)"'
        heart_pattern = r'"heart":(\d+)'
        diggCount_pattern = r'"diggCount":(\d+)'
        friendCount_pattern = r'"friendCount":(\d+)'
        profile_pic_pattern = r'"avatarLarger":"(.*?)"'
        
        # Extract information
        user_id_match = re.search(user_info_pattern, html_content)
        user_id = user_id_match.group(1) if user_id_match else "No ID found"
        
        unique_id_match = re.search(unique_id_pattern, html_content)
        unique_id = unique_id_match.group(1) if unique_id_match else "No unique ID found"
        
        nickname_match = re.search(nickname_pattern, html_content)
        nickname = nickname_match.group(1) if nickname_match else "No nickname found"
        
        followers_match = re.search(followers_pattern, html_content)
        followers = followers_match.group(1) if followers_match else "No followers count found"
        
        following_match = re.search(following_pattern, html_content)
        following = following_match.group(1) if following_match else "No following count found"
        
        likes_match = re.search(likes_pattern, html_content)
        likes = likes_match.group(1) if likes_match else "No likes count found"
        
        videos_match = re.search(videos_pattern, html_content)
        videos = videos_match.group(1) if videos_match else "No videos count found"
        
        signature_match = re.search(signature_pattern, html_content)
        signature = signature_match.group(1) if signature_match else "No signature found"
        
        verified_match = re.search(verified_pattern, html_content)
        verified = verified_match.group(1) if verified_match else "No verified status found"
        
        secUid_match = re.search(secUid_pattern, html_content)
        secUid = secUid_match.group(1) if secUid_match else "No secUid found"
        
        commentSetting_match = re.search(commentSetting_pattern, html_content)
        commentSetting = commentSetting_match.group(1) if commentSetting_match else "No comment setting found"
        
        privateAccount_match = re.search(privateAccount_pattern, html_content)
        privateAccount = privateAccount_match.group(1) if privateAccount_match else "No private account status found"
        
        region_match = re.search(region_pattern, html_content)
        region = region_match.group(1) if region_match else "No region found"
        
        heart_match = re.search(heart_pattern, html_content)
        heart = heart_match.group(1) if heart_match else "No heart count found"
        
        diggCount_match = re.search(diggCount_pattern, html_content)
        diggCount = diggCount_match.group(1) if diggCount_match else "No digg count found"
        
        friendCount_match = re.search(friendCount_pattern, html_content)
        friendCount = friendCount_match.group(1) if friendCount_match else "No friend count found"
        
        profile_pic_match = re.search(profile_pic_pattern, html_content)
        profile_pic = profile_pic_match.group(1).replace('\\u002F', '/') if profile_pic_match else "No profile picture found"

        print("User Information:")
        print(f"User ID: {user_id}")
        print(f"Username: {unique_id}")
        print(f"Nickname: {nickname}")
        print(f"Followers: {followers}")
        print(f"Following: {following}")
        print(f"Likes: {likes}")
        print(f"Videos: {videos}")
        print(f"Biography: {signature}")
        print(f"Verified: {verified}")
        print(f"SecUid: {secUid}")
        print(f"Comment Setting: {commentSetting}")
        print(f"Private Account: {privateAccount}")
        print(f"Region: {region}")
        print(f"Heart: {heart}")
        print(f"Digg Count: {diggCount}")
        print(f"Friend Count: {friendCount}")
        print(f"Profile Picture URL: {profile_pic}")

        # Download the profile picture
        profile_pic_response = requests.get(profile_pic)
        if profile_pic_response.status_code == 200:
            with open(f"{unique_id}_profile_pic.jpg", "wb") as file:
                file.write(profile_pic_response.content)
            print(f"Profile picture downloaded as {unique_id}_profile_pic.jpg")
        else:
            print("Error downloading profile picture")
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get TikTok user information")
    parser.add_argument("identifier", type=str, help="TikTok username or user ID")
    parser.add_argument("--by_id", action="store_true", help="Indicates if the provided identifier is a user ID")
    args = parser.parse_args()
    
    get_user_info(args.identifier, args.by_id)
