import urllib.request
from serpapi import GoogleSearch


def get_google_images(query_search_terms):
    # check query_search_terms is a list containing strings or a single string
    if isinstance(query_search_terms, str):
        query_search_terms = [query_search_terms]
    elif isinstance(query_search_terms, list):
        if not all(isinstance(item, str) for item in query_search_terms):
            raise TypeError("query_search_terms must be a list of strings")


    image_results = []
    
    for query in query_search_terms:
        print("the current query is: ", query)
        # search query parameters
        params = {
            "engine": "google",               # search engine. Google, Bing, Yahoo, Naver, Baidu...
            "q": query,                       # search query
            "tbm": "isch",                    # image results
            "num": "100",                     # number of images per page
            "ijn": 0,                         # page number: 0 -> first page, 1 -> second...
            "api_key": "57e6649848917f5e5b744d2e95fc295b31083475d91a6d84bd51600f89b277bd", # https://serpapi.com/manage-api-key
        }
    
        search = GoogleSearch(params)         # where data extraction happens
    
        images_is_present = True
        while images_is_present:
            results = search.get_dict()       # JSON -> Python dictionary
            print("results: ", results)
    
            # checks for "Google hasn't returned any results for this query."
            if "error" not in results:
                for image in results["images_results"]:
                    if image["original"] not in image_results:
                        image_results.append(image["original"])
                
                # update to the next page
                params["ijn"] += 1
            else:
                print(results["error"])
                images_is_present = False
    
    # -----------------------
    # Downloading images

    
    print(image_results)
    for index, image in enumerate(image_results, start=1):
        try:
                
            print("index: ", index)
            print("image: ", image)
            print(f"Downloading {index} image...")
            
            opener=urllib.request.build_opener()
            opener.addheaders=[("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")]
            urllib.request.install_opener(opener)

            urllib.request.urlretrieve(image, f"PWS-IMAGES/original_size_img_{index}.jpg")
        except:
            pass


get_google_images([
    "port wine stain birthmark face adult",
    "port wine stain birthmark face single person",
    "port wine birtmark single person",
])