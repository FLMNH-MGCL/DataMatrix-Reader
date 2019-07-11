import com.google.zxing.*;
import com.google.zxing.client.j2se.BufferedImageLuminanceSource;
import com.google.zxing.common.HybridBinarizer;
import com.google.zxing.datamatrix.DataMatrixReader;
import com.google.zxing.datamatrix.detector.Detector;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.EnumMap;
import java.util.EnumSet;
import java.util.Map;
import java.util.Scanner;

public class DM_Reader
{
    private static Map<DecodeHintType, Object> hints;

    private static String Decode(BufferedImage image) throws IOException
    {
        if (image == null) {
            throw new IllegalArgumentException("Null BufferedImage");
        }

        LuminanceSource source = new BufferedImageLuminanceSource(image);
        BinaryBitmap bitmap = new BinaryBitmap(new HybridBinarizer(source));
        MultiFormatReader reader = new MultiFormatReader();

        Result result;

        try {
            if (hints != null && !hints.isEmpty()) {
                result = reader.decode(bitmap, hints);
            }
            else {
                Detector detector = new Detector();
                result = reader.decode(bitmap);
            }

            if (result == null ) {
                return null;
            }
            else {
                return result.getText();
            }

        } catch (Exception e) {
            e.printStackTrace();
        }

        return null;

    }

    public static void main(String[] args)
    {
        Scanner scnr = new Scanner(System.in);
        System.out.print("Please enter the path to an image: \n --> ");
        String path = scnr.nextLine();
        System.out.println("\nDecoding...");

        /*
        if (path.charAt(path.length() - 1) != '/' || path.charAt(path.length() - 1) != '\\') {
            path += '/';
        }
        */

        hints = new EnumMap<DecodeHintType, Object>(DecodeHintType.class);
        hints.put(DecodeHintType.TRY_HARDER, Boolean.TRUE);
        hints.put(DecodeHintType.POSSIBLE_FORMATS, EnumSet.of(BarcodeFormat.DATA_MATRIX));

        try {
            BufferedImage image = ImageIO.read(new File(path));
            String decoded = Decode(image);

            if (decoded != null) {
                System.out.println(decoded);
            }
            else {
                System.out.println("Could not find matrix.");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }


    }
}
