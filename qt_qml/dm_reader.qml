import QZXing 2.3

function decode(preview) {
    imageToDecode.source = preview
    decoder.decodeImageQML(imageToDecode)
}

Image {
    id: imageToDecode
}

QZXing {
    id: decoder
    enabledDecoders: QZXing.DecoderFormat_DM //look up format
    onDecodingStarted: console.log("Decoding of image started...")
    onTagFound: console.log("DM data: " + tag)
    onDecodingFinished: console.log("Decoding finished " + (succeeded==true ? "successfully" : "unsuccessfully"))
}