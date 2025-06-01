// code generate with assitance of Google Gemeni Pro
// code for TryHackMe room Custom Tooling using Burp https://tryhackme.com/room/customtoolingviaburp
// YouTube video walk through: https://youtu.be/qOYyzWXnH_I

package burp; // Use the old package name if your Burp version requires it, or adjust if using Montoya API directly

import burp.api.montoya.BurpExtension;
import burp.api.montoya.MontoyaApi;
import burp.api.montoya.http.handler.*;
import burp.api.montoya.logging.Logging;
import burp.api.montoya.core.ByteArray;
import burp.api.montoya.http.message.requests.HttpRequest;
import burp.api.montoya.http.message.responses.HttpResponse;

import javax.crypto.Cipher;
import java.nio.charset.StandardCharsets;
import java.security.*;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class BurpExtender implements BurpExtension, HttpHandler {

    private MontoyaApi api;
    private Logging logging;

    // --- IMPORTANT: REPLACE THESE WITH THE ACTUAL PEM KEYS FROM THE APPLICATION ---
    private static final String SERVER_PUBLIC_KEY_PEM =
            "-----BEGIN PUBLIC KEY-----\n" +
            "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvwpg2aBRLT9RftlcE8Qn\n" + // This is now Key B
            "cmYi2weLT0EnHwXDsAE4A/zvR1dT9X4pFIrNXVnTKlIq8RBMilyoTn3GHUgJoFHG\n" +
            "GdqZfnCCHxf0IVX2NhpYi1HqZeXNCgqY4FtMH9WvjYEH2/twhUnvymT8egG3c50a\n" +
            "pT8sTsJrhWi2M+lhQ2yYXGecZHgAM7EddavpyTEdMw1xhIeeNHo1QxPjii1+dJIU\n" +
            "8iIJ8F3NQtukTe/EQyTjJGx7qDxVobO+njnnreqdqHZ6PqYD/6jlm9myXtUuJQqg\n" +
            "xMWwbxJNuS5Ay9JQSRGEfwEugJHuKEuofJdTkW/PibG9G3zaws4Nhmco8rw59j1r\n" +
            "bQIDAQAB\n" +
            "-----END PUBLIC KEY-----";

    // Not strictly needed for this extension's primary encrypt/decrypt flow, but good to have if expanding
    private static final String SERVER_PRIVATE_KEY_PEM =
            "-----BEGIN PRIVATE KEY-----\n" +
"MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC/CmDZoFEtP1F+\n" +
"2VwTxCdyZiLbB4tPQScfBcOwATgD/O9HV1P1fikUis1dWdMqUirxEEyKXKhOfcYd\n" +
"SAmgUcYZ2pl+cIIfF/QhVfY2GliLUepl5c0KCpjgW0wf1a+NgQfb+3CFSe/KZPx6\n" +
"AbdznRqlPyxOwmuFaLYz6WFDbJhcZ5xkeAAzsR11q+nJMR0zDXGEh540ejVDE+OK\n" +
"LX50khTyIgnwXc1C26RN78RDJOMkbHuoPFWhs76eOeet6p2odno+pgP/qOWb2bJe\n" +
"1S4lCqDExbBvEk25LkDL0lBJEYR/AS6Ake4oS6h8l1ORb8+Jsb0bfNrCzg2GZyjy\n" +
"vDn2PWttAgMBAAECggEAQ8Mco1TYNmJ1N7dFj8VN8KgFyQceBNipVbmntbBY/CEl\n" +
"hnqVT0iWrbCmM2x/GE3Y6XTMkW9YS68VLKG2uGUJDXaaZ1zk6r6GW6SwFnS134UI\n" +
"zWf7mIo1u67mi4wyHtEbxo2jVcPqCDJV07j0J1AceWy0/KK9nK6NolAvrcjBKlUA\n" +
"F9PIOzwS7tlmoX6tN7X8xKcoTwa+W/2poFZFlsBrWDlrQO0+mnIu/ne/nTlBZHIR\n" +
"53n4Qg+G7bxs3xKp5DJ9T+K8hd/4iv2zYLBqC1T3WmdNWHD7CDFP4D4GJw9sqoWO\n" +
"IYxI8GjJn+jWN6pUvSIHu0HFTOpieJl/v+Hc/FSlCQKBgQD4NEFLiu4eo9ZNk4I2\n" +
"a/x8Ixi/NroDhEqtYutdn7IH+IEol7nTtEKkRrA1Z7FMnYh1/1iRQwms8YIr9KsG\n" +
"3GeFCGNP8g+9YZ8aXIEU11gML8T+jpN2Y3z7mqRnJIzDeOzPiMYmaopmyKcP7RYS\n" +
"L+h2fdjYJtxFu8D3C3ZZS4WXkwKBgQDFCnxZWmoT0lZakIBJwUhH4VtYl0FmxioJ\n" +
"+HpLJyO7vR3V46igmarvU3KW+U7ouoYf2lDcfLWOK3VXpW5FpXzp3WNRe7KA70vQ\n" +
"QeVTV8vKtIOBfXz5jJNhlm5Dp5iDgfgr4Q+zbR+RjxXLPwc02AbZWyx+q4q1dKmr\n" +
"zFcdJWzQ/wKBgQCnO6Ym/RPVxzQ0jsf0XSwAhDE/XONWTUN3sae+LERrBHAZ5qkJ\n" +
"UHJ6dzpwsU4PvjDcuFB3h4C0awD3FuJJPCXvx6gKjKE4S9dEjsFWRoYHqAQGNBB9\n" +
"eykR6a8N492IMyjz6EcCSVS5Tkbp/yeY13i8pax+byiJP6kTi0CRh8YaSwKBgQCh\n" +
"fQaM9N0bgbfkYanCyPZEcx46bTzczmyF32/bSCixJT3enscFWOwPWYUA1zMk6joi\n" +
"wPqkulDSRCvXuW23BvppcViE36xcn8Ky3E7nD32mlGtzJTXYEK55vKCCMkl8/ng2\n" +
"/i2wEC9fTLW/7dgqJyL14ROGfXEhZovokYCUEqgsYQKBgG4bMelGkTgiGPLc2g7c\n" +
"TvAc9T7XlUkRqS5ZvoulZuJsJ2BfnDtYjzzVlRU35kDzEBja0Rkv9Rwys+Ft47Md\n" +
"CEaGB/Nz8hBvA3wQjpLYUW4HXul3j5igRvZ/u8CwW+YDqkMpoCcYqTFJnqDOx8I9\n" +
"KmaZV/MVPurxIhmwtUrMOjzH\n" +
"-----END PRIVATE KEY-----";

    // Not strictly needed for this extension's primary encrypt/decrypt flow, but good to have if expanding
    private static final String CLIENT_PUBLIC_KEY_PEM =
            "-----BEGIN PUBLIC KEY-----\n" +
"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhxYZMHH4GTVQ3iqIC2M0\n" +
"Ek06/MIAou1jXqanjLk00lyF9tkm85Sv4GJSrTzz8YticwpH2vVZ0y7E3dzOGQC+\n" +
"ndK36Ny9Cif0ijD6vFZxlff8uWBsj5oGxNQ8vEdpZT9JuRrjuIIgKGoWV3jx7D24\n" +
"TcbULjVvxIhinGWs+RkByCxEJNv9Gc6k9Hv/I0DJY6Z2zFKBinuMoU+CRkBge8O8\n" +
"D7UKRYQ3AEnLVDvI923Di/Lcqz31HKTSha5EjWNF09YKpzrintvWD9GJwt2xP5uV\n" +
"D5+2rQcT/+Ba1UWkLzNkvbWvrWYg1OYz/sVN7AZjC5WQcmOSohHlBpLxMxY32jB4\n" +
"oQIDAQAB\n" +
"-----END PUBLIC KEY-----";

    private static final String CLIENT_PRIVATE_KEY_PEM =
            "-----BEGIN PRIVATE KEY-----\n" +
"MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCHFhkwcfgZNVDe\n" +
"KogLYzQSTTr8wgCi7WNepqeMuTTSXIX22SbzlK/gYlKtPPPxi2JzCkfa9VnTLsTd\n" +
"3M4ZAL6d0rfo3L0KJ/SKMPq8VnGV9/y5YGyPmgbE1Dy8R2llP0m5GuO4giAoahZX\n" +
"ePHsPbhNxtQuNW/EiGKcZaz5GQHILEQk2/0ZzqT0e/8jQMljpnbMUoGKe4yhT4JG\n" +
"QGB7w7wPtQpFhDcASctUO8j3bcOL8tyrPfUcpNKFrkSNY0XT1gqnOuKe29YP0YnC\n" +
"3bE/m5UPn7atBxP/4FrVRaQvM2S9ta+tZiDU5jP+xU3sBmMLlZByY5KiEeUGkvEz\n" +
"FjfaMHihAgMBAAECggEAAMiqAvD721dW47Gh7EU+L/Of1afxZ5CeoaXQWcOoutZh\n" +
"qn5tRHdAv6HJbJb6nESKkMvi0apoG+6g4r/PaDer63v1sEuw2v9jKta8uzlaD5B+\n" +
"uGOG4LzQSI3J2A625dEImjLlxrAmXC6sqFN3zaboaAbg+/9IUabYEePRBYlhpEv7\n" +
"jP9IquO6pO3q13gDhot0fS7MM4sTfYKdPfb8qEwYCpsz3Qi7lFdbBqZxz/O/tkPq\n" +
"giNJNJnHBLmXNOIdSCocMldIhZaPMmcDODPXAehmrru7l/Kh5hnfdK7Njcoph5T4\n" +
"EJqAPOU7XVSyBeJKiKj1x/S+2jzLn8s3hOKCiBbbwQKBgQC+IvSbRXVA16he1yBE\n" +
"183VRAALdVRDDTZcFALaexuNfly2SMU9SL/AAFrbNMaQ83y79XtAbDqk8C6YRhyi\n" +
"z2Il9puVu8G61UB2lWzD5DvDYbb4OS+AroluYZQzeR1+02sZUkR4R0QnfNRQUtMR\n" +
"3awfBIgf9B6Kr90Dnn/OLmQrYQKBgQC14V2azqz4Nkg4bg1LLk612H2fhwz38Evj\n" +
"mlMmxAxdIqGJUz+wGb3tSGmGz7fPxmIga9k8n22nMpfZOyyGF9D93LVa+/9NeFEV\n" +
"DWH5yph+xBN7SSyQMb+Q1xD6gTigLmkIynUXzcucgZB8oUGtexR2IoFu3Li7R9F3\n" +
"HYpUpsKVQQKBgQCFB3X20TEJbhm6SW+lWwwDY7FYUv3ib/MRl1qrvCh55eg+DUoa\n" +
"57RpRJZM+m7XadRiuY1DdLXPQtCG778HVmvIPfN7XsNb0eppTYCsyhnaSJq4r2IB\n" +
"+ZvkI9eJ7/poCsnLDJklQk94BUmS7XAJ9vt/NC99k9JunD7ZUmL/QcwJ4QKBgQCG\n" +
"a812gJEt0VCHBC8nBU5+70XJBVL8W8h6qrAR0osguluQ1soXKK9KE16KmDJNiV00\n" +
"gQDI4Tt1etrnXeiGIkv/k4Mlf2EsrGOgn4dtyeHyro+HaolY+KuQLKMLwT1MhYBz\n" +
"Us4/jYWSYd+bfMLBqFlzBgWLHe4Z2/ZfhqGZ9rWRAQKBgGX7uHz9nUaldXxt4lBn\n" +
"94FR8D6FJxyKGr0/35XrPE3gc1nDJIQGl62E9vk8eVuBsFgqhm2ISroRSxeRI6ml\n" +
"djzuBNJ/gQ5hxhj7ifv1ZakiwvxR2D5uJBPU5gve19Fyrq5On6R+KvVR4b+vcZ5A\n" +
"0HuYuUaGZhtLd9ouH49CvSXj\n" +
"-----END PRIVATE KEY-----";
    // --- END OF KEY PLACEHOLDERS ---

    private PublicKey serverPublicKey;
    private PrivateKey clientPrivateKey;
    // Add other keys if needed:
    private PrivateKey serverPrivateKey;
    private PublicKey clientPublicKey;


    @Override
    public void initialize(MontoyaApi api) {
        this.api = api;
        this.logging = api.logging();
        api.extension().setName("RSA Encrypt/Decrypt Handler");

        try {
            loadKeys();
            logging.logToOutput("RSA keys loaded successfully.");
        } catch (Exception e) {
            logging.logToError("Failed to load RSA keys: " + e.getMessage());
            logging.logToError("Extension might not function correctly.");
            e.printStackTrace(logging.error()); // Print stack trace to Burp's error stream
            return; // Stop initialization if keys can't be loaded
        }

        api.http().registerHttpHandler(this);
        logging.logToOutput("RSA Encrypt/Decrypt Handler registered and loaded.");
    }

    private void loadKeys() throws Exception {
        serverPublicKey = getPublicKeyFromString(SERVER_PUBLIC_KEY_PEM);
        clientPrivateKey = getPrivateKeyFromString(CLIENT_PRIVATE_KEY_PEM);
        // Load other keys if you defined them:
        serverPrivateKey = getPrivateKeyFromString(SERVER_PRIVATE_KEY_PEM);
        clientPublicKey = getPublicKeyFromString(CLIENT_PUBLIC_KEY_PEM);
    }

    // Helper to convert PEM string to PublicKey
    private PublicKey getPublicKeyFromString(String pem) throws Exception {
        String publicKeyPEM = pem
                .replace("-----BEGIN PUBLIC KEY-----", "")
                .replaceAll(System.lineSeparator(), "")
                .replace("-----END PUBLIC KEY-----", "");
        byte[] encoded = Base64.getDecoder().decode(publicKeyPEM);
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        X509EncodedKeySpec keySpec = new X509EncodedKeySpec(encoded);
        return keyFactory.generatePublic(keySpec);
    }

    // Helper to convert PEM string to PrivateKey
    private PrivateKey getPrivateKeyFromString(String pem) throws Exception {
        String privateKeyPEM = pem
                .replace("-----BEGIN PRIVATE KEY-----", "")
                .replaceAll(System.lineSeparator(), "")
                .replace("-----END PRIVATE KEY-----", "");
        byte[] encoded = Base64.getDecoder().decode(privateKeyPEM);
        KeyFactory keyFactory = KeyFactory.getInstance("RSA");
        PKCS8EncodedKeySpec keySpec = new PKCS8EncodedKeySpec(encoded);
        return keyFactory.generatePrivate(keySpec);
    }

    // RSA Encryption (mimics client-side: encrypt with server public key)
    private String encryptRSA(String plaintext, PublicKey key) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding"); // Common default
        cipher.init(Cipher.ENCRYPT_MODE, key);
        byte[] encryptedBytes = cipher.doFinal(plaintext.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }

    // RSA Decryption (mimics client-side: decrypt with client private key)
    private String decryptRSA(String base64Ciphertext, PrivateKey key) throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        cipher.init(Cipher.DECRYPT_MODE, key);
        byte[] encryptedBytes = Base64.getDecoder().decode(base64Ciphertext);
        byte[] decryptedBytes = cipher.doFinal(encryptedBytes);
        return new String(decryptedBytes, StandardCharsets.UTF_8);
    }

    @Override
    public RequestToBeSentAction handleHttpRequestToBeSent(HttpRequestToBeSent requestToBeSent) {
        // Ensure keys are loaded
        if (serverPublicKey == null) {
            logging.logToError("Server public key not loaded. Skipping request encryption.");
            return RequestToBeSentAction.continueWith(requestToBeSent);
        }

        // Only process requests to the target host (optional, but good practice)
        if (!requestToBeSent.url().startsWith("http://10.10.229.122")) { // Replace with your target
            return RequestToBeSentAction.continueWith(requestToBeSent);
        }

        // Check if the request has a body and is of type JSON (simple check)
        if (requestToBeSent.body().length() > 0 && requestToBeSent.contentType().equals(burp.api.montoya.http.message.ContentType.JSON)) {
            String originalRequestBody = requestToBeSent.bodyToString();
            logging.logToOutput("[RSA Ext] Original request body: " + originalRequestBody);

            // Regex to find {"data":"action=login..."}
            // This pattern looks for "data":" followed by action=login and captures everything until the next quote
            Pattern pattern = Pattern.compile("\"data\"\\s*:\\s*\"(action=login[^\"]*)\"");
            Matcher matcher = pattern.matcher(originalRequestBody);

            if (matcher.find()) {
                String plaintextPayload = matcher.group(1); // This is "action=login..."
                logging.logToOutput("[RSA Ext] Plaintext payload to encrypt: " + plaintextPayload);

                try {
                    String encryptedPayload = encryptRSA(plaintextPayload, serverPublicKey);
                    logging.logToOutput("[RSA Ext] Encrypted payload (Base64): " + encryptedPayload);

                    // Construct the new JSON body: {"data":"ENCRYPTED_STRING"}
                    // Be careful with escaping inside the JSON string
                    String newJsonBody = "{\"data\":\"" + encryptedPayload + "\"}";

                    // Update the request with the new encrypted body
                    HttpRequest modifiedRequest = requestToBeSent.withBody(newJsonBody);
                    logging.logToOutput("[RSA Ext] Modified request body: " + newJsonBody);
                    return RequestToBeSentAction.continueWith(modifiedRequest);

                } catch (Exception e) {
                    logging.logToError("[RSA Ext] RSA Encryption failed: " + e.getMessage());
                    e.printStackTrace(logging.error());
                }
            } else {
                logging.logToOutput("[RSA Ext] '{\"data\":\"action=login...' pattern not found in request body.");
            }
        }
        return RequestToBeSentAction.continueWith(requestToBeSent);
    }

    @Override
    public ResponseReceivedAction handleHttpResponseReceived(HttpResponseReceived responseReceived) {

        // Check if the Client Private Key is loaded (should be at the start of the method)
        if (clientPrivateKey == null) {
            logging.logToError("[RSA Ext] Client private key not loaded. Skipping response decryption.");
            return ResponseReceivedAction.continueWith(responseReceived);
        }

        // Initial check for response body presence
        if (responseReceived.body().length() > 0) {
            // Check the Content-Type header from the response
            String contentTypeHeader = "";
            // Iterate through headers to find Content-Type (case-insensitive)
            for (burp.api.montoya.http.message.HttpHeader header : responseReceived.headers()) {
                if (header.name().equalsIgnoreCase("Content-Type")) {
                    contentTypeHeader = header.value().toLowerCase();
                    break;
                }
            }

            // YOUR PROVIDED SNIPPET STARTS HERE (with slight integration)
            if (contentTypeHeader.contains("application/json")) {
                String originalResponseBody = responseReceived.bodyToString();
                logging.logToOutput("[RSA Ext] Original response body (JSON): " + originalResponseBody);

                // Regex to capture the content of the "data" field.
                // Using ([^\"]+) is safer for now to ensure we capture the value.
                Pattern pattern = Pattern.compile("\"data\"\\s*:\\s*\"([^\"]+)\"");
                Matcher matcher = pattern.matcher(originalResponseBody);

                if (matcher.find()) {
                    String capturedValue = matcher.group(1); // This might contain "\\/" for escaped slashes
                    logging.logToOutput("[RSA Ext] Captured value for 'data' field: " + capturedValue);

                    // ** NEW STEP: Unescape any "\/" sequences to "/" **
                    String unescapedValue = capturedValue.replace("\\/", "/");
                    logging.logToOutput("[RSA Ext] Unescaped value for Base64 decoding: " + unescapedValue);

                    // Now use the unescapedValue for Base64 decoding
                    String encryptedPayloadBase64 = unescapedValue;

                    try {
                        String decryptedPayload = decryptRSA(encryptedPayloadBase64, clientPrivateKey); // decryptRSA will do Base64.decode
                        logging.logToOutput("-----------------------------------------");
                        logging.logToOutput("[RSA Ext] Decrypted Server Response:");
                        logging.logToOutput(decryptedPayload);
                        logging.logToOutput("-----------------------------------------");

                    } catch (Exception e) {
                        logging.logToError("[RSA Ext] RSA Decryption failed: " + e.getMessage());
                        e.printStackTrace(logging.error());
                    }
                } else {
                    logging.logToOutput("[RSA Ext] JSON 'data' field pattern not found in response body. Cannot decrypt.");
                }
            } else {
                logging.logToOutput("[RSA Ext] Response Content-Type (" + contentTypeHeader + ") is not application/json. Skipping decryption attempt.");
            }
        } else {
            logging.logToOutput("[RSA Ext] Response body is empty. Skipping response decryption.");
        }

        return ResponseReceivedAction.continueWith(responseReceived);
    }

   
}

