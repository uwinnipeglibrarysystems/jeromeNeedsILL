from random import SystemRandom
sysrandom = SystemRandom()
def get_random_secret_key():
    return ''.join(
        sysrandom.choice(
            'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
        for i in range(50))

if __name__ == "__main__":
    print("SECRET_KEY='" + get_random_secret_key() + "'")
