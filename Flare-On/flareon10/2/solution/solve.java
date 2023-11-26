import java.util.zip.CRC32;
import javax.crypto.Cipher;
import java.nio.charset.StandardCharsets;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.security.NoSuchAlgorithmException;
import java.security.InvalidKeyException;

class HelloWorld {
	private static final byte[] decrypt(String str, byte[] bArr, SecretKeySpec secretKeySpec, IvParameterSpec ivParameterSpec) throws Exception {
        Cipher cipher = Cipher.getInstance(str);
        cipher.init(Cipher.DECRYPT_MODE, secretKeySpec, ivParameterSpec);
        byte[] doFinal = cipher.doFinal(bArr);
        return doFinal;
    }

    private static final long hash_CRC32(byte[] bArr) {
        CRC32 crc32 = new CRC32();
        crc32.update(bArr);
        return crc32.getValue();
    }

    private static final String key_arr() {
        String string = "https://flare-on.com/evilc2server/report_token/report_token.php?token=";
        String string2 = "wednesday";
        StringBuilder sb = new StringBuilder();
        sb.append(string.subSequence(4, 10));
        sb.append(string2.subSequence(2, 5));
        String sb2 = sb.toString();
        
        byte[] bytes = sb2.getBytes(StandardCharsets.UTF_8);
        long a2 = hash_CRC32(bytes);

        StringBuilder sb3 = new StringBuilder();
        sb3.append(a2);
        sb3.append(a2);
        String sb4 = sb3.toString();
        
        StringBuilder slice = new StringBuilder();
        slice.append(sb4.subSequence(0, 16));
        return slice.toString();
    }

    public static void main(String[] args) throws Exception {
	    String key_arr = key_arr();
	    byte[] bytes = key_arr.getBytes(StandardCharsets.UTF_8);
	    SecretKeySpec secretKeySpec = new SecretKeySpec(bytes, "AES");

		String string2 = "abcdefghijklmnop";
	    byte[] bytes2 = string2.getBytes(StandardCharsets.UTF_8);
	   	IvParameterSpec ivParameterSpec = new IvParameterSpec(bytes2);
	        	        	        
	    FileInputStream inputStream = new FileInputStream("iv.png");
	    byte[] encryptedFile = new byte[inputStream.available()];
        inputStream.read(encryptedFile);

        byte[] decryptedFile = decrypt("AES/CBC/PKCS5Padding", encryptedFile, secretKeySpec, ivParameterSpec);

	    FileOutputStream outputStream = new FileOutputStream("flag.png");
	    outputStream.write(decryptedFile);
		outputStream.close();
    }
}