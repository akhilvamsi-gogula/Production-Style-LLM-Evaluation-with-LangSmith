import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from _env import load_project_env


class EnvLoadingTests(unittest.TestCase):
    def test_load_project_env_reads_repo_dotenv(self) -> None:
        os.environ.pop("GROQ_API_KEY", None)
        os.environ.pop("LANGCHAIN_API_KEY", None)
        os.environ.pop("LANGCHAIN_TRACING_V2", None)

        load_project_env()

        self.assertTrue(os.environ.get("GROQ_API_KEY"))
        self.assertTrue(os.environ.get("LANGCHAIN_API_KEY"))
        self.assertEqual(os.environ.get("LANGCHAIN_TRACING_V2", "").lower(), "true")


if __name__ == "__main__":
    unittest.main()
