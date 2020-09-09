
mod lib;

extern crate zbar_rust;
extern crate image;

use zbar_rust::{ZBarConfig, ZBarImageScanner, ZBarSymbolType};
use std::process::{Command};

use image::GenericImageView;
use std::time::Instant;


fn test_zbar_lib() {

    let img = image::open("/Users/aaronleopold/Documents/museum/datamatrix/test_images/2d/barcode.JPG").unwrap();

    let (width, height) = img.dimensions();
    
    // let luma_img = img.to_luma();
    
    let img_data: Vec<u8> = img.to_bytes();
    // let img_data: Vec<u8> = luma_img.to_vec();
    
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

fn test_read_dir(path: &str) {
    let output = Command::new("ls")
        .arg(path)
        .output()
        .expect("ls command failed to start.");

    let listed_dir = String::from(String::from_utf8_lossy(&output.stdout));

    let result = match listed_dir.as_str() {
        "" => String::default(),
        _ => listed_dir,
    };

    if result == "" {
        println!("Recieved nothing....")
    } else {
        println!("{}", result)
    }

}

// fn test_zbar_cli() {
//     let img_path = "/Users/aaronleopold/Documents/museum/datamatrix/test_images/2d/barcode.JPG";
//     // let img_path = "/Users/aaronleopold/Documents/museum/datamatrix/test_images/2d/IMG016.jpg";

//     let decoded = lib::zbarimg(img_path);

//     println!("{}", decoded)
// }

// fn test_dmtx_only() {
//     let start = Instant::now();
//     let num_files = lib::run("/Users/aaronleopold/Documents/museum/datamatrix/test_images", "30000",false);
//     let end = start.elapsed();

//     println!("\nCompleted... {} files handled in {:?}.", num_files, end);
//     if num_files != 0 {
//         println!("Average time per image: {:?}", end / num_files as u32);
//     }
// }

fn test_dmtx_zbar() {
    let start = Instant::now();
    // I am setting scan_time to 1 ms because I know there are no datamatrices here and right now it can only be run
    // including dmtxread
    let num_files = lib::run("/Volumes/flmnh/NaturalHistory/Lepidoptera/Kawahara/Digitization/LepNet/PINNED_COLLECTION/IMAGES_PROBLEMS/Catocala_rename_me/MGCL_green_barcodes_manual_rename/2016_10_25_MANUAL_RENAME", "1", true);
    let end = start.elapsed();

    println!("\nCompleted... {} files handled in {:?}.", num_files, end);

    if num_files != 0 {
        println!("Average time per image: {:?}", end / num_files as u32);
    }
}


pub fn main() {
    // test_dmtx_only();

    // test_zbar_cli();

    // test_read_dir("/Volumes/flmnh/NaturalHistory/Lepidoptera/Kawahara/Digitization/LepNet/PINNED_COLLECTION/IMAGES_PROBLEMS/Catocala_rename_me/MGCL_green_barcodes_manual_rename/2016_10_25_MANUAL_RENAME");

    test_dmtx_zbar();
}