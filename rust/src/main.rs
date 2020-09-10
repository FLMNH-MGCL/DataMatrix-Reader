
mod lib;

extern crate zbar_rust;
extern crate image;
extern crate clap;

use clap::{Arg, App};

use std::time::Instant;  

pub fn main() {
    let matches = App::new("Datamatrix Scanner")
        .version("1.0")
        .author("Aaron Leopold <aaronleopold1221@gmail.com>")
        .about("Decodes datamatrices and code128 barcodes from specimen images")
        .arg(Arg::with_name("start_dir")
            .short("d")
            .long("start_dir")
            .value_name("DIR")
            .help("Sets the starting path")
            .required(true)
            .takes_value(true))
        .arg(Arg::with_name("scan_time")
            .short("s")
            .long("scan_time")
            .value_name("TIME (in ms)")
            .help("Sets the time to scan for a datamatrix")
            .required(true)
            .takes_value(true))
        .arg(Arg::with_name("barcode")
            .short("b")
            .long("barcode")
            .help("Sets the program to search for code128 on datamatrix failed reads")
            .required(false)
            .takes_value(false))
        .get_matches();

    let starting_path = matches.value_of("start_dir").unwrap();
    let scan_time = matches.value_of("scan_time").unwrap();
    let include_barcodes = matches.is_present("barcode");

    let start = Instant::now();
    // I am setting scan_time to 1 ms because I know there are no datamatrices here and right now it can only be run
    // including dmtxread
    let num_files = lib::run(starting_path, scan_time, include_barcodes);
    let end = start.elapsed();

    println!("\nCompleted... {} files handled in {:?}.", num_files, end);

    if num_files != 0 {
        println!("Average time per image: {:?}", end / num_files as u32);
    }
}

// TESTS
// cargo run --release -- --scan_time 30000 --start_dir /Volumes/flmnh/NaturalHistory/Lepidoptera/Kawahara/Digitization/LepNet/PINNED_COLLECTION/IMAGES_PROBLEMS/Catocala_rename_me/MGCL_green_barcodes_manual_rename/2016_10_25_MANUAL_RENAME --barcode
// cargo run --release -- --scan_time 30000 --start_dir /Volumes/flmnh/NaturalHistory/Lepidoptera/Kawahara/Digitization/LepNet/PINNED_COLLECTION/IMAGES_PROBLEMS/Catocala_rename_me/MGCL_green_barcodes_manual_rename/RAW_2016_10_10 --barcode
// cargo run --release -- --scan_time 30000 --start_dir /Volumes/flmnh/NaturalHistory/Lepidoptera/Kawahara/Digitization/LepNet/PINNED_COLLECTION/IMAGES_UPLOADED/IMAGES_UPLOADED_NAMED/EREBIDAE/Catocala/2019_07_10/2019_07_10_LOW-RES

