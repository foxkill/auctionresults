from urllib.parse import urlparse

import requests


class Load:
    def get(self, url):
        parts = urlparse(url)
        try:
            response = requests.get(url, timeout=(10, 10))
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            print(f'Timeout error when connecting to {parts.netloc}')
            exit(1)
        except requests.exceptions.TooManyRedirects:
            print(f'Too many redirects for {parts.netloc}')
            exit(1)
        except requests.exceptions.ConnectionError:
            print(f'Could not connect to server: {parts.netloc}')
            exit(1)
        except requests.exceptions.RequestException as e:
            print(f'Error loading auction results from: {parts.netloc}')
            exit(1)
        except Exception as e:
            print(f'Error loading auction results from: {parts.netloc}')
            exit(1)

        if response.status_code != 200:
            print(f'Error loading auction results: {response.status_code}')
            exit(1)

        return response.content
