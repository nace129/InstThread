# Nidhi
import os
from flask import Flask, render_template, request, redirect, flash, session
from dotenv import load_dotenv
from mastodon import Mastodon

load_dotenv()

app = Flask(__name__)
app.secret_key = 'FBlYM8VNqG5DXma2wKnw1vdKq4ENn2Q3QS-T_QFz4p8'

# Initializating the Mastodon API client
mastodon = Mastodon(
    access_token=os.getenv('ACCESS_TOKEN'),
    api_base_url=os.getenv('API_BASE_URL')
)

post_id = None
post_content = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global post_id, post_content
    
    if request.method == 'POST':
        if 'post' in request.form:
            # Creating a new post
            content = request.form['content']
            if content:
                try:
                    response = mastodon.status_post(content)
                    post_id = response.id
                    post_content = response.content
                    flash('Post created successfully!', 'success')
                except Exception as e:
                    flash(f'Error creating post: {e}', 'danger')
        
        elif 'retrieve' in request.form:
            # Retrieving
            #  the post using the stored post_id
            if post_id is not None:
                try:
                    post = mastodon.status(post_id)
                    post_content = post.content
                    flash('Post retrieved successfully!', 'success')
                except Exception as e:
                    flash(f'Error retrieving post: {e}', 'danger')
            else:
                flash('No post ID available to retrieve.', 'warning')
        
        elif 'delete' in request.form:
            if post_id is not None:
                try:
                    mastodon.status_delete(post_id)
                    post_id = None
                    post_content = None
                    # Clear post_id from session
                    session.pop('post_id', None)
                    flash('Post deleted successfully!', 'success')
                except Exception as e:
                    flash(f'Error deleting post: {e}', 'danger')
            else:
                flash('No post ID available to delete.', 'warning')

    return render_template('index.html', post_content=post_content)

if __name__ == "__main__":
    app.run(debug=True)
