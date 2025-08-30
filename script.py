from dotenv import load_dotenv

load_dotenv()

product_hunt_api = os.getenv("PRODUCT_HUNT_API_TOKEN")
product_hunt_url = "https://api.producthunt.com/v2/api/graphql"

def get_product_hunt_data(after = None):
    headers = {
        "Authorization": f"Bearer {product_hunt_api}",
        "Content-Type": "application/json"
    }
    query ="""
    query getPosts($after: String) {
      posts(first: 3, after: $after) {
        edges {
          cursor
          node {
            name
            tagline
            url
            votesCount
            commentsCount
            thumbnail {
              url
            }
            topics(first: 3) {
              edges {
                node {
                  name
                }
              }
            }
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
      }
    }        
    """
    variables = {"after": after}
    response = requests.post(product_hunt_url, headers=headers, json={"query": query, "variables": variables})
    response.raise_for_status()
    return response.json()