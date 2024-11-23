from app.schemas import PostOut, PostResponse
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts')
    def validate(post):
        return PostOut(**post)
    
    posts = list(map(validate, res.json()))

    assert len(res.json()) == len(test_posts) 
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get('/posts')
    assert res.status_code == 200

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f'/posts/{test_posts[1].id}')
    assert res.status_code == 401

def test_get_non_existent_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/12345')
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[1].id}')
    post = PostOut(**res.json())
    
    assert res.status_code == 200
    assert post.Post.id == test_posts[1].id
    assert post.Post.content == test_posts[1].content
    assert post.Post.title == test_posts[1].title


@pytest.mark.parametrize('title, content, visible', [
    ('awesome new title', 'some new content', True),
    ('favorite pizza', 'i love milano', False),
    ('Secret password', 'supersecret123', True),
    
])
def test_create_post(authorized_client, test_user, test_posts, title, content, visible):
    res = authorized_client.post('/posts', json={'title': title, 'content': content, 'visible': visible})

    created_post = PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.author_id == test_user['id']
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.visible == visible

def test_create_post_default_visible_true(authorized_client, test_user, test_posts):
    res = authorized_client.post('/posts', json={'title': 'something', 'content': 'somethingsomething'})

    created_post = PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.visible == True

def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post('/posts', json={'title': 'title', 'content': 'content'})
 
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f'/posts/{test_posts[0].id}')
 
    assert res.status_code == 401

def test_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[0].id}')
 
    assert res.status_code == 204

def test_delete_nonexistent_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete('/posts/9999')

    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'/posts/{test_posts[3].id}')

    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[0].id
    }

    res = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)
    updated_post = PostResponse(**res.json())
    
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(authorized_client, test_user, second_test_user, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[3].id
    }
    res = authorized_client.put(f'/posts/{test_posts[3].id}', json=data)

    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f'/posts/{test_posts[0].id}')
 
    assert res.status_code == 401

def test_update_nonexistent_post(authorized_client, test_user, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[3].id
    }

    res = authorized_client.put('/posts/9999', json=data)

    assert res.status_code == 404