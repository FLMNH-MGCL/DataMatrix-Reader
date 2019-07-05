#include <QZXing.h>

int main()
{
    QImage imageToDecode("../images/MGCL_1085297.png");
    QZXing decoder;
    decoder.setDecoder(DecoderFormat_DM); // look up enum for data matrix
    QString result = decoder.decodeImage(imageToDecode);
}