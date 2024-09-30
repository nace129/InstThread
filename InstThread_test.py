# Siri and Roshini
import os
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from InstThread_app import app  # Import Flask InstThread_app

class TestMastodonInstThread_app(unittest.TestCase):
    def setUp(self):
        # Set up a test client for the Flask InstThread_application
        self.InstThread_app = app.test_client()
        self.InstThread_app.testing = True
        self.post_id = 12345  # Sample post ID for testing
        self.post_content = "Hello, InstThread!"  # Sample post content

    @patch('InstThread_app.mastodon.status_post')
    def test_create_post(self, mock_status_post):
        # Mock the API response for creating a post
        mock_status_post.return_value = MagicMock(id=self.post_id, content=self.post_content)

        response = self.InstThread_app.post('/', data={'content': self.post_content, 'post': 'Post'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post created successfully!', response.data)
        self.assertIn(self.post_content.encode(), response.data)

    @patch('InstThread_app.mastodon.status_post')
    @patch('InstThread_app.mastodon.status')
    def test_retrieve_post(self, mock_status, mock_status_post):
        # Mock the API response for creating a post
        mock_status_post.return_value = MagicMock(id=self.post_id, content=self.post_content)

        # Creating the post and setting the post_id in session
        with self.InstThread_app.session_transaction() as sess:
            sess['post_id'] = self.post_id  # Setting post_id in session

        # Mock the API response for retrieving the post
        mock_status.return_value = MagicMock(content=self.post_content)

        # Calling the create post to ensure post_id is set in session
        self.InstThread_app.post('/', data={'content': self.post_content, 'post': 'Post'})

        # Retrieving the post
        response = self.InstThread_app.post('/', data={'retrieve': 'Retrieve'})
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post retrieved successfully!', response.data)
        self.assertIn(self.post_content.encode(), response.data)



    @patch('InstThread_app.mastodon.status_delete')
    def test_delete_post(self, mock_status_delete):
        # Mock the API response for deleting a post
        mock_status_delete.return_value = None

        # Setting the post_id manually
        with self.InstThread_app.session_transaction() as sess:
            sess['post_id'] = self.post_id

        response = self.InstThread_app.post('/', data={'delete': 'Delete'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post deleted successfully!', response.data)

        # Verifying that the post_id is reset
        with self.InstThread_app.session_transaction() as sess:
            self.assertIsNone(sess.get('post_id'))


if __name__ == '__main__':
    unittest.main()
