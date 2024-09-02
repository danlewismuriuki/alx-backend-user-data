# Basic Authentication with Base64 Encoding

This project explains the concept of authentication, Base64 encoding, and how to implement Basic Authentication in HTTP requests. It also provides a simple guide on how to send an `Authorization` header using Basic Authentication.

## What Authentication Means

**Authentication** is the process of verifying the identity of a user or entity. It ensures that only authorized users can access certain resources or data. Common methods of authentication include:

- **Password-based authentication**: Using a username and password.
- **Token-based authentication**: Using tokens like JWT.
- **Multi-factor authentication**: Combining two or more authentication methods, such as passwords and one-time codes.

Authentication is crucial for ensuring that sensitive information and resources are protected from unauthorized access.

## What Base64 Is

**Base64** is an encoding scheme that converts binary data (like images or credentials) into ASCII text. It is commonly used to encode data that needs to be transmitted over text-based protocols such as HTTP, email, or XML.

- Base64 encoding is *not* encryption; it is a reversible encoding method.
- It uses a set of 64 characters (A-Z, a-z, 0-9, +, /) to represent binary data.

### How to Encode a String in Base64

To encode a string in Base64, follow these steps:

1. Convert the string to bytes.
2. Encode the bytes using the Base64 algorithm.
3. Convert the encoded bytes back to a string.

**Example in Python**:

```python
import base64

# Original string
original_string = "username:password"

# Encode the string to Base64
encoded_bytes = base64.b64encode(original_string.encode('utf-8'))
encoded_string = encoded_bytes.decode('utf-8')

print(encoded_string)  # Output: dXNlcm5hbWU6cGFzc3dvcmQ=

