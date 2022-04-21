import pytest
from app import schemas
from tests.conftest import test_posts

def test_get_all_posts(authorized_client, test_posts):
    print("the post test ran")
    res = authorized_client.get("/posts/")
    print(res.json())

    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, res.json())
    print("-----------------")
    print(list(posts_map))

    posts_list = list(posts_map)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title
    

@pytest.mark.parametrize("title, content, published",[
    ("awesome new title", "awesome new content", True),
    ("awesome second title", "awesome second content", False),
    ("awesome whaattttt title", "awesome is this content", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "titletje", "content": "contetnje"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "titletje"
    assert created_post.content == "contetnje"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


# def test_unauthorized_user_create_posts(client, test_user, test_posts):
#     res = client.post("/posts/", json={"title": "titletje", "content": "contetnje"})    
#     assert res.status_code == 401

# def test_unautohrized_user_delete_post(client, test_user, test_posts):
#     res = client.delete(f"/posts/{test_posts[0].id}")
#     assert res.status_code == 401

# def test_delete_post_succes(authorized_client, test_user, test_posts):
#     print("hieronder -----------------------")
#     print(test_posts[0].title)
#     print(test_posts[0].id)
#     print(test_posts[0].owner_id)
#     print("hierboven -----------------------")
#     res = authorized_client.delete(f"/posts/{test_posts[0].id}")
#     assert res.status_code == 204


# def test_delete_post_non_exist(authorized_client, test_user, test_posts):
#     res = authorized_client.delete(f"/posts/5151515")
#     assert res.status_code == 404


# def test_delete_other_user_post(authorized_client, test_user, test_posts):
#     res = authorized_client.delete(
#         f"/posts/{test_posts[3].id}")
#     assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json= data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_unautohrized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/5151515", json = data)
    assert res.status_code == 404