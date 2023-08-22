import requests


class MovieDB:
    def __init__(self,HEADERS):
        self.base_url = "https://api.themoviedb.org/3"
        self.headers = HEADERS

    def check_connection(self):
        url = f"{self.base_url}/authentication"
        response = requests.get(url, headers=self.headers)
        return response.text

    def search_movie(self,movie_title):
        search_endpoint = "/search/movie"
        page = 1

        # Construct the full URL for the search endpoint
        search_url = f"{self.base_url}{search_endpoint}"

        # Construct the query parameters
        params = {
            "query": movie_title,
            "page": page
        }

        # Make the API request
        response = requests.get(search_url, headers=self.headers, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return data["results"][:5]
        else:
            return f"Error: {response.status_code}"  

    def get_movie_details(self,movie_id):
        url = f"{self.base_url}/movie/{movie_id}"

        response = requests.get(url, headers=self.headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
        else:
            return f"Error: {response.status_code}"  

        return data

    def get_movie_provider(self,movie_id):
        url = f"{self.base_url}/movie/{movie_id}/watch/providers"

        response = requests.get(url, headers=self.headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
        else:
            return f"Error: {response.status_code}"  

        try:
            provider = data["results"]["US"]["flatrate"][0]["provider_name"]
        except:
            try:
                provider = data["results"]["US"]["buy"][0]["provider_name"]
            except:
                provider = ""

        return provider

    def search_series(self,series_title):
        search_endpoint = "/search/tv"
        page = 1

        # Construct the full URL for the search endpoint
        search_url = f"{self.base_url}{search_endpoint}"

        # Construct the query parameters
        params = {
            "query": series_title,
            "page": page
        }

        # Make the API request
        response = requests.get(search_url, headers=self.headers, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return data["results"][:5]
        else:
            return f"Error: {response.status_code}"  


    def get_series_details(self,series_id):
        url = f"{self.base_url}/tv/{series_id}"

        response = requests.get(url, headers=self.headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
        else:
            return f"Error: {response.status_code}"  

        return data

    def get_season_details(self,series_id,season_number):
        url = f"{self.base_url}/tv/{series_id}/season/{season_number}"

        response = requests.get(url, headers=self.headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
        else:
            return f"Error: {response.status_code}"  

        return data
