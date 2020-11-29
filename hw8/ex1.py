import requests
from phe import paillier

URL = 'http://localhost:8000'

def query_pred(input_vector):
    public_key, private_key = paillier.generate_paillier_keypair() # Gen Pailier keypair
    # Compute encrypted feature vector using public key
    # Floating point values need to be encoded as integers before encryption
    # Precision: maximum absolute error allowed when encoding value
    encrypted_number_list = [int(public_key.encrypt(x, precision = 2**(-16))) for x in input_vector] 
    response = requests.post(URL, data = {'pub_key_n' : public_key.n, 'enc_feature_vector' : encrypted_number_list})
    # Error check
    if response.status_code != 200:
        raise Exception(response.text)
    # Get encrypted prediction in the base-10 representation
    # Represent as Pailier encrypted object as decrypt using private key
    raw_enc_prediction = response.json()['enc_prediction']
    enc_prediction = paillier.EncryptedNumber(public_key = public_key, ciphertext = raw_enc_prediction, exponent = -8)
    prediction = private_key.decrypt(enc_prediction)
    return prediction



def main():

    input_vector = [0.48555949, 0.29289251, 0.63463107,
                    0.41933057, 0.78672205, 0.58910837,
                    0.00739207, 0.31390802, 0.37037496,
                    0.3375726]

    prediction = query_pred(input_vector)

    print(prediction)

    assert 2**(-16) > abs(prediction - 0.44812144746653826)


if __name__ == "__main__":
    main()