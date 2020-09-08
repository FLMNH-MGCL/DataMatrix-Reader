
mod lib;

extern crate zbar_rust;
extern crate image;

use zbar_rust::{ZBarConfig, ZBarImageScanner, ZBarSymbolType};

use image::GenericImageView;
use std::time::Instant;


fn test_zbar() {

    let img = image::open("/Users/aaronleopold/Documents/museum/datamatrix/test_images/2d/code128.jpg").unwrap();

    let (width, height) = img.dimensions();
    
    let luma_img = img.to_luma();
    
    // let img_data: Vec<u8> = img.to_bytes();
    let img_data: Vec<u8> = luma_img.to_vec();
    
    let mut scanner = ZBarImageScanner::new();
    // scanner.set_config(ZBarSymbolType::ZBarCode128, ZBarConfig::ZBarCfgEnable, 1).unwrap();
    
    // let results = scanner.scan(&luma_img_data, width, height).unwrap();

    println!("{} - {}", width, height);

    
    let results = scanner.scan(&img_data, width, height, ZBarSymbolType::ZBarCode128 as u32);

    println!("DONE");



    println!("{:?}", results);

    
    for result in results {
        // println!("{}", String::from_utf8(result.data).unwrap())
        println!("{:?}", result)
    }
}

fn test_dmtx() {
    let start = Instant::now();
    let num_files = lib::run("/Users/aaronleopold/Documents/museum/datamatrix/test_images");
    let end = start.elapsed();

    println!("\nCompleted... {} files handled in {:?}.", num_files, end);
    println!("Average time per image: {:?}", end / num_files as u32);
}


pub fn main() {
    test_dmtx();

    // test_zbar();
}