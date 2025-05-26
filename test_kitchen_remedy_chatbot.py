import unittest
from unittest.mock import patch, MagicMock
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

from retrieverFAISS import get_or_create_vectorstore


class TestKitchenRemedyChatbot(unittest.TestCase):
    def setUp(self):
        """Setup test case."""
        self.urls = [
            "https://www.chkd.org/patient-family-resources/our-blog/home-remedies-for-sick-kids/",
            "https://www.webmd.com/parenting/baby/ss/slideshow-home-remedies",
            "https://www.babycenter.com/health/illness-and-infection/safe-home-remedies-for-your-childs-cough-cold-or-flu_10014077"
        ]
        self.embedding = OpenAIEmbeddings()  # Replace with your actual embedding model
        self.faiss_index_path = "test_faiss_index"  # Use a test FAISS index path

    @patch('main.load_documents_from_urls')
    @patch('langchain_community.vectorstores.FAISS.load_local')# Mock document loading function
    def test_get_or_create_vectorstore(self, mock_load_local, mock_load_documents):
        mock_load_documents.return_value = ["Document 1", "Document 2"]

        mock_vectorstore = MagicMock()
        mock_vectorstore.as_retriever.return_value = "mock_retriever"
        mock_vectorstore.add_documents.return_value = None
        mock_vectorstore.save_local.return_value = None

        mock_load_local.return_value = mock_vectorstore

        result = get_or_create_vectorstore(self.urls)

        self.assertEqual(result, "mock_retriever")

    @patch('main.load_documents_from_urls')  # Mock document loading function
    def test_retriever_functionality(self, mock_load_documents):
        """Test retriever functionality after the vectorstore is created."""
        mock_load_documents.return_value = ["Document 1", "Document 2"]

        # Create or update the vectorstore
        vectorstore = get_or_create_vectorstore(self.urls)

        # Simulate a query to the retriever
        query = "What are some remedies for a child's cough?"
        result = vectorstore.get_relevant_documents(query)

        # Check if the result is as expected (mocked response here)
        self.assertTrue(result)  # Ensure that there is some result

    def tearDown(self):
        """Cleanup after each test."""
        # Optionally, remove the test FAISS index or any files used during testing
        # os.remove(self.faiss_index_path)
        pass


if __name__ == "__main__":
    unittest.main()
