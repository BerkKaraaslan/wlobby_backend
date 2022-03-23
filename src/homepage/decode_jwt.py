# Copyright 2017-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file
# except in compliance with the License. A copy of the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under the License.

import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode

region = 'us-east-1'
userpool_id = 'us-east-1_2kkPUknf2'
app_client_id = '6m7fmpsps3p1s3cbp3o30hkr70'
keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)

# instead of re-downloading the public keys every time
# we download them only on cold start
# https://aws.amazon.com/blogs/compute/container-reuse-in-lambda/
with urllib.request.urlopen(keys_url) as f:
    response = f.read()
keys = json.loads(response.decode('utf-8'))['keys']


def lambda_handler(event, context):
    print(keys_url)
    token = event['token']
    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    # search for the kid in the downloaded public keys
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        print('Public key not found in jwks.json')
        return False
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print('Signature verification failed')
        return False
    print('Signature successfully verified')
    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # additionally we can verify the token expiration
    if time.time() > claims['exp']:
        print('Token is expired')
        return False
    # and the Audience  (use claims['client_id'] if verifying an access token)
    if claims['aud'] != app_client_id:
        print('Token was not issued for this audience')
        return False
    # now we can use the claims
    print(claims)
    return claims


# the following is useful to make this script executable in both
# AWS Lambda and any other local environments
"""  if __name__ == '__main__':
    # for testing locally you can enter the JWT ID Token here
    event = {'token': "eyJraWQiOiJ6QUpFRTdkQVdQb3kzXC9VWlBqdUc4M0RBcmV3Yk5FTnF6bkpheWt4SzA1MD0iLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoiSDZ1ZW9PZVFoRWcxaE1NQ240cWtLUSIsInN1YiI6IjhiNWVhNGZjLTZlOWQtNDc1Mi1iODk1LWY2MDIzNGQ4ZjJiNyIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV8ya2tQVWtuZjIiLCJjb2duaXRvOnVzZXJuYW1lIjoiOGI1ZWE0ZmMtNmU5ZC00NzUyLWI4OTUtZjYwMjM0ZDhmMmI3Iiwib3JpZ2luX2p0aSI6IjBhOGQ3MmQ3LTU2MGMtNDExNC1iZjgzLWRjODU4MWQwNjhmZSIsImF1ZCI6IjZtN2ZtcHNwczNwMXMzY2JwM28zMGhrcjcwIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2NDgwNzY1NjUsIm5hbWUiOiJidWdyYSIsImV4cCI6MTY0ODE2Mjk2NSwiaWF0IjoxNjQ4MDc2NTY1LCJqdGkiOiI5MTJiNjg2MC0wOWE2LTQxMDMtYmVkNi0wNTI2OGM1NmUwNTgiLCJlbWFpbCI6ImFyZ3Vibmlrc2F0QGdtYWlsLmNvbSJ9.Xnhu3nhazecLOeWclA5GX37j6KnR9Cnx7S5UTwL7V9W2DsP43cH45BzoO91eq9OH6M_xkLTO1TkaL5jwXH73wNxB0l26IdKrMAtdzYhc2ayFj0aaUn8gv-78Rc2C7QIobu0Wx3u_en5ewadq7wqIVvz7amZ1rG4gj0h_D2JE9vwFp7Q7oTIrQiafP9eRTIq_Fy0cgWmU-kFMuCinL61JUoMFnfZu3graifO31_AQg33aCXMakBA7auDXVRB-18eaNCKdASP6wCQeoSG4dwMSkPKXwPR7xgUbwpcmG08YRVZ6x4NwkW_DrDRn4fhev7eOTLgwEHM_RZ6DJ5wYPxarzQ"}
    lambda_handler(event, None) 
"""