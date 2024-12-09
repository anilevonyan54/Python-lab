BASE_URL = "https://jsonplaceholder.typicode.com"

def get_filtered_posts():
    response = requests.get(f"{BASE_URL}/posts")
    if response.status_code == 200:
        posts = response.json()
        filtered_by_title = [
            post for post in posts
            if len(post["title"].split()) <= 6
        ]
        filtered_by_body = [
            post for post in filtered_by_title
            if len(post["body"].split("\n")) <= 3
        ]
        return filtered_by_body
    else:
        print(f"GET request failed with status code {response.status_code}")
        return []

def create_post():
    new_post = {
        "title": "New Post Title",
        "body": "This is a new post body.",
        "userId": 1
    }
    response = requests.post(f"{BASE_URL}/posts", json=new_post)
    if response.status_code == 201:
        print("POST request successful:", response.json())
    else:
        print(f"POST request failed with status code {response.status_code}")

def update_post(post_id):
    updated_post = {
        "title": "Updated Post Title",
        "body": "This is the updated post body.",
        "userId": 1
    }
    response = requests.put(f"{BASE_URL}/posts/{post_id}", json=updated_post)
    if response.status_code == 200:
        print("PUT request successful:", response.json())
    else:
        print(f"PUT request failed with status code {response.status_code}")

def delete_post(post_id):
    response = requests.delete(f"{BASE_URL}/posts/{post_id}")
    if response.status_code == 200:
        print(f"DELETE request successful for post ID {post_id}")
    else:
        print(f"DELETE request failed with status code {response.status_code}")

if __name__ == "__main__":
    print("Filtered GET results:")
    filtered_posts = get_filtered_posts()
    for post in filtered_posts:
        print(post)

    print("\nMaking a POST request:")
    create_post()

    print("\nMaking a PUT request:")
    update_post(1)

    print("\nMaking a DELETE request:")
    delete_post(1)
