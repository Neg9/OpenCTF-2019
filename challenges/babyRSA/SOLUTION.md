This is really just a simple modular arithmetic problem. Since `n` is prime and `e` has no obvious multiplicative inverses that can be found via the extended euclidean algorithm,  we don't "really" have any RSA. Instead, we must find the roots of `pt^(e) - ct` modulo `n`. Thus, we are left to solve:

`ct = pt^(e) mod n`

To run `sage solve.sage` you need to have:
- python2.7
- sage installed (https://doc.sagemath.org/html/en/installation/)
- pycrypto installed for sage (e.g. `sage -pip install pycrypto`)


`solve-direct.py` is a python only implementation that does not derive the roots, but given a hardcoded one, will convert it to bytes.

