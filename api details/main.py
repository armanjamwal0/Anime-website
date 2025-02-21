
# import requests
# Anime_api = "d33fc7d9aa6569889a1fc893131eee85"

# params = {
#             "q": 'tomodachi game',   # Search for Naruto
#             "limit": 1       # Limit results to 5
#         }
# # url = "https://api.jikan.moe/v4/anime"
# manga_url = "https://api.jikan.moe/v4/manga"
# headers = {
#         "X-MAL-CLIENT-ID": Anime_api  # Authentication header
#     }
# # # Make the GET request
# response = requests.get(manga_url, params=params,headers=headers)

# data = response.json()
# # mal_id = data["data"][0]["mal_id"]
# # print(data['data'][0].get("title_english"))
# # print(data['synopsis'])
# print(data)
# # print(data['data'][0]['images']['jpg']['large_image_url'])




import requests


# MAL API endpoint for manga details
url = "https://api.jikan.moe/v4/manga"

# Example: Searching for manga by title
params = {
    "q": "tomodachi game ",  # Change this to any manga title
    "limit": 1
}

response = requests.get(url, params=params)
data = response.json()

print(data)