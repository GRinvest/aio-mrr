"""Tests for SecretMasker class.

This module tests the secret masking functionality for log messages.
"""

from __future__ import annotations

from aio_mrr.logging.masker import SecretMasker


class TestSecretMasker:
    """Tests for SecretMasker class."""

    def test_mask_api_key_with_colon(self) -> None:
        """Test masking API key with colon separator."""
        masker = SecretMasker()
        text = "x-api-key: abc123"
        result = masker.mask(text)
        assert result == "x-api-key: ***"

    def test_mask_api_sign_with_colon(self) -> None:
        """Test masking API signature with colon separator."""
        masker = SecretMasker()
        text = "x-api-sign: def456"
        result = masker.mask(text)
        assert result == "x-api-sign: ***"

    def test_mask_api_key_with_equals(self) -> None:
        """Test masking API key with equals separator."""
        masker = SecretMasker()
        text = "api_key=mysecretkey"
        result = masker.mask(text)
        assert result == "api_key=***"

    def test_mask_api_sign_with_equals(self) -> None:
        """Test masking API signature with equals separator."""
        masker = SecretMasker()
        text = "api_sign=abcdef123456"
        result = masker.mask(text)
        assert result == "api_sign=***"

    def test_mask_multiple_secrets(self) -> None:
        """Test masking multiple secrets in one string."""
        masker = SecretMasker()
        text = "api_key=mykey&api_secret=myservice"
        result = masker.mask(text)
        assert "mykey" not in result
        assert "myservice" not in result
        assert "api_key=***" in result
        assert "api_secret=***" in result

    def test_mask_nonce(self) -> None:
        """Test masking nonce value."""
        masker = SecretMasker()
        text = "x-api-nonce: 1234567890"
        result = masker.mask(text)
        assert result == "x-api-nonce: ***"

    def test_mask_sha256_hash(self) -> None:
        """Test masking SHA256 hash (64 hex chars)."""
        masker = SecretMasker()
        text = "signature: a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"
        result = masker.mask(text)
        assert "a1b2c3d4e5f6" not in result

    def test_mask_sha1_hash(self) -> None:
        """Test masking SHA1 hash (40 hex chars)."""
        masker = SecretMasker()
        text = "x-api-sign: a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"
        result = masker.mask(text)
        assert "a1b2c3d4e5f6" not in result

    def test_no_mask_normal_text(self) -> None:
        """Test that normal text is not masked."""
        masker = SecretMasker()
        text = "Request completed successfully"
        result = masker.mask(text)
        assert result == text

    def test_mask_with_quotes(self) -> None:
        """Test masking secrets with quotes."""
        masker = SecretMasker()
        text = 'apikey: "secret123"'
        result = masker.mask(text)
        assert "secret123" not in result

    def test_mask_case_insensitive(self) -> None:
        """Test that masking is case insensitive."""
        masker = SecretMasker()
        text = "X-API-KEY: ABC123"
        result = masker.mask(text)
        assert result == "X-API-KEY: ***"

    def test_mask_json_format(self) -> None:
        """Test masking secrets in JSON-like format."""
        masker = SecretMasker()
        text = '{"x-api-key": "abc123", "x-api-sign": "def456"}'
        result = masker.mask(text)
        assert "abc123" not in result
        assert "def456" not in result
