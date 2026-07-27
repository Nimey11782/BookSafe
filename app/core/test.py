from app.core.security import hash_password, verify_password

hashed=hash_password("hi123")

print(hashed)
print(verify_password("hi123",hashed))
print(verify_password("hi",hashed))