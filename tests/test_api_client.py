import unittest
from unittest.mock import patch

from src import api_client


class AuthenticatedApiClientTests(unittest.TestCase):
    @patch("src.api_client.requests.get")
    def test_get_sends_bearer_token(self, mock_get):
        with patch.object(api_client, "RAG_API_TOKEN", "test-token"), patch.object(
            api_client, "API_BASE_URL", "http://api.test"
        ):
            api_client.api_get("/documents")
        self.assertEqual(mock_get.call_args.args[0], "http://api.test/documents")
        self.assertEqual(mock_get.call_args.kwargs["headers"]["Authorization"], "Bearer test-token")

    @patch("src.api_client.requests.post")
    def test_post_sends_bearer_token_and_preserves_upload_arguments(self, mock_post):
        files = {"file": ("sample.pdf", b"%PDF-", "application/pdf")}
        with patch.object(api_client, "RAG_API_TOKEN", "test-token"), patch.object(
            api_client, "API_BASE_URL", "http://api.test"
        ):
            api_client.api_post("/upload", files=files, timeout=60)
        self.assertEqual(mock_post.call_args.args[0], "http://api.test/upload")
        self.assertEqual(mock_post.call_args.kwargs["headers"]["Authorization"], "Bearer test-token")
        self.assertEqual(mock_post.call_args.kwargs["files"], files)
        self.assertEqual(mock_post.call_args.kwargs["timeout"], 60)

    @patch("src.api_client.requests.get")
    def test_get_omits_authorization_when_no_token_is_configured(self, mock_get):
        with patch.object(api_client, "RAG_API_TOKEN", ""):
            api_client.api_get("/health")
        self.assertEqual(mock_get.call_args.kwargs["headers"], {})


if __name__ == "__main__":
    unittest.main()
