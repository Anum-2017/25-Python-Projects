import requests
from bs4 import BeautifulSoup

github_user = input("Enter the GitHub username: ")
url = f'https://github.com/{github_user}'

r = requests.get(url)

if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'html.parser')


    img_tag = soup.find('img', class_='avatar-user')

    if img_tag and 'src' in img_tag.attrs:
        profile_image = img_tag['src']
        print('✅ Profile image found!')
        print('Profile image URL:', profile_image)

        # Optional: download image
        download = input("Download image? (y/n): ")
        if download.lower() == 'y':
            img_data = requests.get(profile_image).content
            with open(f'{github_user}.jpg', 'wb') as handler:
                handler.write(img_data)
            print(f'📥 Image saved as {github_user}.jpg')

    else:
        print("❌ Profile image not found. Maybe default avatar or layout changed.")
else:
    print("❌ GitHub user not found. Check the username.")