import bcrypt

def hash_senha(senha):
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

senha_hashed = hash_senha('123')
print(senha_hashed)