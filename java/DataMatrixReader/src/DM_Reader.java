import com.google.zxing.*;
import com.google.zxing.client.j2se.BufferedImageLuminanceSource;
import com.google.zxing.common.HybridBinarizer;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class DM_Reader
{
    private static String Decode(File image) throws IOException
    {
        BufferedImage bufferedImage = ImageIO.read(image);
        LuminanceSource source = new BufferedImageLuminanceSource(bufferedImage);
        BinaryBitmap bitmap = new BinaryBitmap(new HybridBinarizer(source));

        try {
            Result result = new MultiFormatReader().decode(bitmap);
            return result.getText();
        } catch (NotFoundException e) {
            System.out.println("There is no DataMatrix");
            return null;
        }
    }

    public static void main(String[] args)
    {
        try {
            File file = new File ("/home/aaron/Documents/data_science/DataMatrix-Reader/images/test/test.png");
            String decodedText = Decode(file);

            if (decodedText == null) {
                System.out.println("No DataMatrix found in image");
            }
            else {
                System.out.println("Decoded Text " +decodedText);;
            }
        } catch (IOException e) {
            System.out.println("Could not decode DataMatix, IOExcetpion: " + e.getMessage());
        }
    }
}
