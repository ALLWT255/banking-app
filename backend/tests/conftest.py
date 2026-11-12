
import os

# Dummy environment variables for automated tests
os.environ["DATABASE_URL"] = "sqlite:///./test_auth.db"
os.environ["JWT_SECRET_KEY"] = (
    "local-pytest-only-secret-not-for-production-2026-long-enough"
)
