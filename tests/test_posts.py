import pytest
from app import schemas


def test_get_all_posts(autherized_client, test_posts):
    res = autherized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    posts_map = map(validate, res.json())
    print(list(posts_map))

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get("/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(autherized_client, test_posts):
    res = autherized_client.get("/posts/88888")
    assert res.status_code == 404


def test_get_one_post(autherized_client, test_posts):
    res = autherized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize(
    "title,content,published",
    [
        ("awesome new title", "awesome new content", True),
        ("favorite pizza", "i love pepperoni", False),
        ("tallest skyscrapers", "wahoo", True),
        ("worst day ever", "i am tired", False),
    ],
)
def test_create_post(
    autherized_client, test_user, test_posts, title, content, published
):
    res = autherized_client.post(
        "/posts", json={"title": title, "content": content, "published": published}
    )
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_published_true(autherized_client, test_user, test_posts):
    res = autherized_client.post(
        "/posts", json={"title": "art title", "content": "art content"}
    )
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "art title"
    assert created_post.content == "art content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]


def test_unautherized_user_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/", json={"title": "awesome new title", "content": "awesome new content"}
    )
    assert res.status_code == 401


def test_unautherized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(autherized_client, test_user, test_posts):
    res = autherized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(autherized_client, test_user, test_posts):
    res = autherized_client.delete(f"/posts/8000000")
    assert res.status_code == 404
    res = autherized_client.delete(f"/posts/8989898")
    assert res.status_code == 404


def test_delete_other_user_post(autherized_client, test_user, test_posts):
    res = autherized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(autherized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    res = autherized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(autherized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }
    res = autherized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unautherized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(autherized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    res = autherized_client.put(f"/posts/8000000", json=data)
    assert res.status_code == 404
