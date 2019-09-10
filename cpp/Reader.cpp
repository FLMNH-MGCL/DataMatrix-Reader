#include <dmtx.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <fstream>
#include <vector>

int main()
{
    size_t width, height, bytesPerPixel;
    unsigned char *pxl;
    DmtxImage *img;
    DmtxDecode *dec;
    DmtxRegion *reg;
    DmtxMessage *msg;

    std::ifstream in("../images/MGCL_1085340.png", std::ios::binary);
    std::istream_iterator<unsigned char> begin(in), end;

    std::vector<unsigned char> buffer(begin,end);

    pxl = new unsigned char[buffer.size()];

    for (int i = 0; i < buffer.size(); i++) {
        pxl[i] = buffer[i];
    }

    // need to obtain width and height first
    img = dmtxImageCreate(pxl, width, height, DmtxPack24bppRGB);



    //img = dmtxImageCreate(pxl_arr, width, height, pack_type);
    /*
    img = dmtxImageCreate(pxl, width, height, DmtxPack24bppRGB);
    assert(img != NULL);

    dec = dmtxDecodeCreate(img, 1);
    assert(dec != NULL);

    reg = dmtxRegionFindNext(dec, NULL);
    if(reg != NULL) {
        msg = dmtxDecodeMatrixRegion(dec, reg, DmtxUndefined);
        if(msg != NULL) {
            fputs("output: \"", stdout);
            fwrite(msg->output, sizeof(unsigned char), msg->outputIdx, stdout);
            fputs("\"\n", stdout);
            dmtxMessageDestroy(&msg);
        }
        dmtxRegionDestroy(&reg);
    }

    dmtxDecodeDestroy(&dec);
    dmtxImageDestroy(&img);
    free(pxl);

     */


    return 0;
}
