import random
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests

problem_suffixes_by_rating = {}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parts = self.path.split("/")
        rating_min = int(parts[1])
        rating_max = int(parts[2])
        selection = []

        for rating in range(rating_min, rating_max+1, 100):
            selection += problem_suffixes_by_rating[rating]

        url = "https://codeforces.com/problemset/problem/" + random.choice(selection)

        self.send_response(301)
        self.send_header('Location', url)
        self.end_headers()


if __name__ == "__main__":
    response = requests.get("https://codeforces.com/api/problemset.problems")

    for rating in range(800, 3501, 100):
        problem_suffixes_by_rating[rating] = []

    for problem in response.json()["result"]["problems"]:
        if "rating" not in problem:
            continue

        rating = problem["rating"]
        suffix = str(problem["contestId"]) + "/" + problem["index"]
        problem_suffixes_by_rating[rating].append(suffix)

    HTTPServer(("", 1234), Handler).serve_forever()
