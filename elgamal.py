from numbers import gcd, miller_rabin, prime_bitlen
import random


class ElGamalKeyring(object):


    bitlen = -1
    p = -1
    g = -1
    a = -1
    b = -1

    def __init__(self, bitlen):

        self.bitlen = bitlen
        q = -1

        # generate a safe prime
        safe_prime_found = False
        while not safe_prime_found:

            q = prime_bitlen(bitlen, mr_trials = 100)
            self.p = 2 * q + 1

            # find valid d for miller-rabin test
            d = self.p - 1

            while d % 2 == 0:
                d //= 2

            safe_prime_found = True

            for _ in range(0, 100):

                if not miller_rabin(self.p, d):

                    safe_prime_found = False
                    break

        # generate a safe g
        while True:

            self.g = pow(random.randrange(2, self.p), 2, self.p)

            ginv = pow(self.g, -1, self.p)

            if self.g == 1 or \
            self.g == 2 or \
            (self.p - 1) % int(self.g) == 0 or \
            (self.p - 1) % int(ginv) == 0:

                continue

            break

        # generate private key a
        self.a = random.randrange(2, self.p - 1)

        # generate public key b
        self.b = pow(self.g, self.a, self.p)


    def __encrypt_char(self, c):

        char_val = ord(c)
        key = random.randrange((2 ** (self.bitlen - 1)) + 1, self.p)

        while gcd(self.p, key) != 1:

            key = random.randrange((2 ** (self.bitlen - 1)) + 1, self.p)

        halfmask = pow(self.g, key, self.p)
        m = char_val * pow(self.b, key, self.p) % self.p

        return (halfmask, m)


    def __decrypt_char(self, enc_c):

        halfmask = enc_c[0]
        fullmask = pow(halfmask, self.a, self.p)
        m = enc_c[1]

        dec_m = (m * pow(fullmask, -1, self.p)) % self.p

        return chr(dec_m)


    def encrypt(self, text):

        encrypted = [ ]

        for c in text:

            enc = self.__encrypt_char(c)
            encrypted.append(enc)

        return encrypted


    def decrypt(self, enc_text):

        decrypted = ""

        for enc_c in enc_text:

            decrypted += self.__decrypt_char(enc_c)

        return decrypted


    def __str__(self):

        return "(public: p = {0.p}, g = {0.g}, b = {0.b}) (private: a = {0.a})".format(self)


    def __repr__(self):

        return self.__str__()



class PublicElGamalKeyring(ElGamalKeyring):


    def __init__(self, base_keyring):

        self.bitlen = base_keyring.bitlen
        self.p = base_keyring.p
        self.g = base_keyring.g
        self.b = base_keyring.b

        # no private key
        self.a = -1


    def __decrypt_char(self, enc_c):

        raise RuntimeError("Cannot decrypt a message with a public keyring")


    def decrypt(self, enc_text):

        raise RuntimeError("Cannot decrypt a message with a public keyring")


    def __str__(self):

        return "(public: p = {0.p}, g = {0.g}, b = {0.b})".format(self)



def gen_elgamal_keys():

    num_bits = int(input("Enter ElGamal bit length: "))
    keys = ElGamalKeyring(num_bits)
    return keys


if __name__ == "__main__":

    keys = gen_elgamal_keys()
    pub_keys = PublicElGamalKeyring(keys)
    msg_plain = input("Enter a message: ")
    msg_enc = pub_keys.encrypt(msg_plain)
    msg_dec = keys.decrypt(msg_enc)
    print(keys)
    print(pub_keys)
    print("ENCRYPTED:", msg_enc)
    print("DECRYPTED:", msg_dec)
