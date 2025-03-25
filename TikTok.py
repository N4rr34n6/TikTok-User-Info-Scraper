import requests
import re
import argparse
import urllib.parse
from bs4 import BeautifulSoup

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

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        
        # Try to use lxml parser if available, otherwise use html.parser
        try:
            soup = BeautifulSoup(html_content, 'lxml')
        except:
            soup = BeautifulSoup(html_content, 'html.parser')
        
        # Regular expressions to extract information
        patterns = {
            'user_id': r'"webapp.user-detail":{"userInfo":{"user":{"id":"(\d+)"',
            'unique_id': r'"uniqueId":"(.*?)"',
            'nickname': r'"nickname":"(.*?)"',
            'followers': r'"followerCount":(\d+)',
            'following': r'"followingCount":(\d+)',
            'likes': r'"heartCount":(\d+)',
            'videos': r'"videoCount":(\d+)',
            'signature': r'"signature":"(.*?)"',
            'verified': r'"verified":(true|false)',
            'secUid': r'"secUid":"(.*?)"',
            'commentSetting': r'"commentSetting":(\d+)',
            'privateAccount': r'"privateAccount":(true|false)',
            'region': r'"region":"(.*?)"',
            'heart': r'"heart":(\d+)',
            'diggCount': r'"diggCount":(\d+)',
            'friendCount': r'"friendCount":(\d+)',
            'profile_pic': r'"avatarLarger":"(.*?)"'
        }
        
        # Extract information using the defined patterns
        info = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, html_content)
            info[key] = match.group(1) if match else f"No {key} found"
        
        # Process profile pic URL
        if "profile_pic" in info:
            info['profile_pic'] = info['profile_pic'].replace('\\u002F', '/')
        
        # Initialize the list of social links
        social_links = []
        
        # Get the biography content
        bio = info.get('signature', "")
        
        # ============= SOCIAL LINKS EXTRACTION =============
        
        # METHOD 1: Extract links with target parameter
        link_urls = re.findall(r'href="(https://www\.tiktok\.com/link/v2\?[^"]*?scene=bio_url[^"]*?target=([^"&]+))"', html_content)
        for full_url, target in link_urls:
            # Decode the target parameter
            target_decoded = urllib.parse.unquote(target)
            # Look for the text associated with this URL
            text_pattern = rf'href="{re.escape(full_url)}"[^>]*>.*?<span[^>]*SpanLink[^>]*>([^<]+)</span>'
            text_match = re.search(text_pattern, html_content, re.DOTALL)
            if text_match:
                link_text = text_match.group(1)
            else:
                # If we don't find the text, use the target as text
                link_text = target_decoded
                
            # Add to social links if not already present
            if not any(target_decoded in s for s in social_links):
                social_links.append(f"Link: {link_text} - {target_decoded}")
            
        # METHOD 2: Find all SpanLink classes that look like URLs
        span_links = re.findall(r'<span[^>]*class="[^"]*SpanLink[^"]*">([^<]+)</span>', html_content)
        for span_text in span_links:
            # Check if it looks like a URL (contains a dot and no spaces)
            if '.' in span_text and ' ' not in span_text and not any(span_text in s for s in social_links):
                social_links.append(f"Link: {span_text} - {span_text}")
        
        # METHOD 3: Find all target parameters in URLs
        all_targets = re.findall(r'scene=bio_url[^"]*?target=([^"&]+)', html_content)
        for target in all_targets:
            target_decoded = urllib.parse.unquote(target)
            if not any(target_decoded in s for s in social_links):
                # Try to find the associated text
                text_pattern = rf'target={re.escape(target)}[^>]*>.*?<span[^>]*>([^<]+)</span>'
                text_match = re.search(text_pattern, html_content, re.DOTALL)
                if text_match:
                    link_text = text_match.group(1)
                else:
                    link_text = target_decoded
                
                social_links.append(f"Link: {link_text} - {target_decoded}")
        
        # METHOD 4: Extract bioLink links from JSON
        bio_link_pattern = r'"bioLink":{"link":"([^"]+)","risk":(\d+)}'
        bio_links_matches = re.findall(bio_link_pattern, html_content)

        for link, risk in bio_links_matches:
            # Clean escape characters in URLs
            clean_link = link.replace('\\u002F', '/')
            if not any(clean_link in s for s in social_links):
                social_links.append(f"💎 **{clean_link}**: `{clean_link}`")

        # Also search for links in other JSON data patterns
        shared_links_pattern = r'"shareUrl":"([^"]+)"'
        shared_links_matches = re.findall(shared_links_pattern, html_content)

        for shared_url in shared_links_matches:
            # Clean escape characters in URLs
            clean_url = shared_url.replace('\\u002F', '/')
            if not any(clean_url in s for s in social_links):
                social_links.append(f"💎 **{clean_url}**: `{clean_url}`")

        # Also search within divs containing DivShareLinks to ensure we capture all links
        share_links_div_pattern = re.compile(r'<div[^>]*class="[^"]*DivShareLinks[^"]*"[^>]*>(.*?)</div>', re.DOTALL)
        for div_match in share_links_div_pattern.finditer(html_content):
            div_content = div_match.group(1)
            
            # Search for links inside these divs
            div_links = re.finditer(r'<a[^>]*href="[^"]*scene=bio_url[^"]*target=([^"&]+)"[^>]*>.*?<span[^>]*class="[^"]*SpanLink[^"]*">([^<]+)</span>', div_content, re.DOTALL)
            
            for link_match in div_links:
                target = urllib.parse.unquote(link_match.group(1))
                link_text = link_match.group(2)
                
                if not any(target in s or link_text in s for s in social_links):
                    social_links.append(f"💎 **{link_text}**: `{target}`")
        
        # Find spans with SpanLink class
        span_matches = re.findall(r'<span[^>]*class="[^"]*SpanLink[^"]*">([^<]+)</span>', html_content)
        for span_text in span_matches:
            if '.' in span_text and not any(span_text in s for s in social_links):
                # Looks like a link (contains a dot) and we don't have it yet
                social_links.append(f"Link: {span_text} - {span_text}")
        
        # Look for a specific combination of ABioLink + SpanLink
        biolink_matches = re.findall(r'class="[^"]*ABioLink[^"]*"[^>]*>.*?<span[^>]*class="[^"]*SpanLink[^"]*">([^<]+)</span>', html_content, re.DOTALL)
        for span_text in biolink_matches:
            if not any(span_text in s for s in social_links):
                social_links.append(f"Link: {span_text} - {span_text}")
        
        # METHOD 5: Extract Instagram and other social networks mentioned in the bio
        # Instagram
        ig_pattern = re.search(r'[iI][gG]:\s*@?([a-zA-Z0-9._]+)', bio)
        if ig_pattern:
            instagram_username = ig_pattern.group(1)
            if not any(f"Instagram: @{instagram_username}" in s for s in social_links):
                social_links.append(f"Instagram: @{instagram_username}")
        
        # Other social networks in bio
        social_patterns = {
            'snapchat': r'([sS][cC]|[sS]napchat):\s*@?([a-zA-Z0-9._]+)',
            'twitter': r'([tT]witter|[xX]):\s*@?([a-zA-Z0-9._]+)',
            'facebook': r'[fF][bB]:\s*@?([a-zA-Z0-9._]+)',
            'youtube': r'([yY][tT]|[yY]outube):\s*@?([a-zA-Z0-9._]+)',
            'telegram': r'[tT]elegram:\s*@?([a-zA-Z0-9._]+)'
        }
        
        for platform, pattern in social_patterns.items():
            match = re.search(pattern, bio)
            if match:
                username = match.group(2) if len(match.groups()) > 1 else match.group(1)
                if platform == 'snapchat':
                    social_link = f"Snapchat: {username}"
                elif platform == 'twitter':
                    social_link = f"Twitter/X: @{username}"
                elif platform == 'facebook':
                    social_link = f"Facebook: {username}"
                elif platform == 'youtube':
                    social_link = f"YouTube: {username}"
                elif platform == 'telegram':
                    social_link = f"Telegram: @{username}"
                
                if not any(social_link in s for s in social_links):
                    social_links.append(social_link)
        
        # Look for email addresses in the bio
        email_pattern = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', bio)
        if email_pattern:
            email = email_pattern.group(0)
            if not any(email in s for s in social_links):
                social_links.append(f"Email: {email}")
        
        # Add social links to the info dictionary
        info['social_links'] = social_links

        # Print basic user information
        print("\n=== User Information ===")
        print(f"User ID: {info['user_id']}")
        print(f"Username: {info['unique_id']}")
        print(f"Nickname: {info['nickname']}")
        print(f"Verified: {info['verified']}")
        print(f"Private Account: {info['privateAccount']}")
        print(f"Region: {info['region']}")
        print(f"Followers: {info['followers']}")
        print(f"Following: {info['following']}")
        print(f"Likes: {info['likes']}")
        print(f"Videos: {info['videos']}")
        print(f"Friends: {info['friendCount']}")
        print(f"Heart: {info['heart']}")
        print(f"Digg Count: {info['diggCount']}")
        print(f"SecUid: {info['secUid']}")
        
        # Print biography
        print("\n=== Biography ===")
        print(info['signature'].replace('\\n', '\n'))
        
        # Print social links
        if social_links:
            print("\n=== Social Links ===")
            for link in social_links:
                print(link)
        else:
            print("\nNo social links found.")
        
        # Print TikTok profile link
        print(f"\nTikTok Profile: https://www.tiktok.com/@{info['unique_id']}")

        # Download the profile picture
        if "profile_pic" in info and info["profile_pic"].startswith("http"):
            try:
                profile_pic_response = requests.get(info["profile_pic"])
                if profile_pic_response.status_code == 200:
                    with open(f"{info['unique_id']}_profile_pic.jpg", "wb") as file:
                        file.write(profile_pic_response.content)
                    print(f"\nProfile picture downloaded as {info['unique_id']}_profile_pic.jpg")
                else:
                    print("\nError downloading profile picture")
            except Exception as e:
                print(f"\nError downloading profile picture: {str(e)}")
        
        return info
    else:
        print(f"Error: Unable to fetch profile. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhanced TikTok User Information Scraper")
    parser.add_argument("identifier", type=str, help="TikTok username or user ID")
    parser.add_argument("--by_id", action="store_true", help="Indicates if the provided identifier is a user ID")
    args = parser.parse_args()
    
    get_user_info(args.identifier, args.by_id)
