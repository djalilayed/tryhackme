Admin flag:

The secure cookie is created by splitting the string username:USER_AGENT:SECRET_KEY into 8-character chunks and encrypting each chunk with PHP's crypt() function.

Since "guest" and "admin" are both 5 characters long, they would affect only the first 8-character chunk (which would be something like "guest:XX" or "admin:XX" where XX is the beginning of the user agent).

By replacing just the first encrypted chunk (13 characters long, which is the standard output length of the PHP crypt() function with a 2-character salt), we're essentially changing just the part that identifies the username.

We keep the rest of the cookie exactly the same, which contains the encrypted chunks for the remainder of the user agent and secret key.
When the server verifies the cookie, it:

- Takes the salt from the first 2 characters
- Generates the expected cookie for "admin" (since that's in the user cookie)
- Compares it to our modified cookie, which now has "admin" in the first chunk but otherwise matches what it expects

This works because the verification logic doesn't have any additional checks beyond comparing the generated cookie with what we provide.

* exaplanation by Claudi AI
