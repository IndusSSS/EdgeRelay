"""
EdgeRelay Security Manager
MESSS Compliant - Modular, Efficient, Scalable, Secure, Stable
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.hash import bcrypt
import secrets
import string

from .config import get_settings

logger = logging.getLogger(__name__)


class SecurityManager:
    """
    Security manager for authentication and authorization.
    MESSS Compliant: Secure, Efficient authentication management.
    """
    
    def __init__(self, settings):
        self.settings = settings
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
    async def initialize(self):
        """Initialize security manager."""
        logger.info("✅ Security manager initialized")
    
    async def close(self):
        """Close security manager."""
        logger.info("✅ Security manager closed")
    
    def hash_password(self, password: str) -> str:
        """
        Hash password using bcrypt.
        MESSS Compliant: Secure password hashing.
        """
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify password against hash.
        MESSS Compliant: Secure password verification.
        """
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create JWT access token.
        MESSS Compliant: Secure token generation.
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        
        encoded_jwt = jwt.encode(
            to_encode, 
            self.settings.SECRET_KEY, 
            algorithm=self.settings.JWT_ALGORITHM
        )
        
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """
        Verify JWT token.
        MESSS Compliant: Secure token verification.
        """
        try:
            payload = jwt.decode(
                token, 
                self.settings.SECRET_KEY, 
                algorithms=[self.settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError as e:
            logger.error(f"Token verification failed: {e}")
            raise ValueError("Invalid token")
    
    def generate_secure_password(self, length: int = 12) -> str:
        """
        Generate secure password.
        MESSS Compliant: Secure password generation.
        """
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
    
    def generate_api_key(self, length: int = 32) -> str:
        """
        Generate secure API key.
        MESSS Compliant: Secure API key generation.
        """
        alphabet = string.ascii_letters + string.digits
        api_key = ''.join(secrets.choice(alphabet) for _ in range(length))
        return api_key
    
    def validate_password_strength(self, password: str) -> bool:
        """
        Validate password strength.
        MESSS Compliant: Secure password validation.
        """
        if len(password) < 8:
            return False
        
        if not any(c.isupper() for c in password):
            return False
        
        if not any(c.islower() for c in password):
            return False
        
        if not any(c.isdigit() for c in password):
            return False
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False
        
        return True
