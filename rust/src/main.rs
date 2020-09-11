
mod lib;

extern crate zbar_rust;
extern crate image;

use std::time::Instant; 
use std::env::args;



fn display_help() {
    let help = "
Aaron Leopold <aaronleopold1221@gmail.com>
datamatrix scanner 1.0.0   

USAGE:
    cargo run --release -- [OPTIONS] [FLAGS]
    /path/to/binary [OPTIONS] [FLAGS]

FLAGS:
    -h, --help                  Prints help information

OPTIONS:
    --start_dir <DIR>           The directory to start searching for and decoding datamatrices    
    --scan_time <TIME (in ms)>  The maximum time allowed to attempt decoding one datamatrix    
    --barcode                   If present, will search for and decode CODE-128 barcodes    
    ";

    println!("{}", help);
}

fn interpret_arg(argument: String) -> Option<Vec<String>> {
    let allowed_args = ["--start_dir", "--scan_time", "--barcode"];

    let arg_vec: Vec<String> = argument.split(" ").into_iter().map(|s| String::from(s)).collect();

    if allowed_args.iter().any(|&i| i == arg_vec[0]) {
        if arg_vec[0] != "--barcode" && arg_vec.len() != 2 {
            return None;
        }

        return Some(arg_vec);
    }

    None
}


pub fn main() {
    // clap argument parser broke the STDOUT collection for flow, so I had to implement 
    // my own argument handling.
    let arguments: Vec<String> = args().collect();

    let mut barcode = false;
    let mut starting_path = String::default();
    let mut scan_time = String::default();

    if arguments.len() < 2 {
        println!("No arguments detected... Please run with the --help flag to see usage");
        std::process::exit(1);
    }

    // check if help is present
    if arguments.iter().any(|i| i.as_str() == "--help") {
        display_help();
        std::process::exit(0);
    }

    for (index, argument) in arguments.iter().enumerate() {
        if index == 0 {
            continue;
        }

        match interpret_arg(argument.clone()) {
            Some(arg_vec) => {
                let arg_flag = arg_vec[0].clone();

                match arg_flag.clone().as_str() {
                    "--start_dir" => {
                        let arg_value = arg_vec[1].clone();
                        starting_path = arg_value;
                    },
                    "--scan_time" => {
                        let arg_value = arg_vec[1].clone();
                        scan_time = arg_value;
                    },
                    "--barcode" => {
                        barcode = true;
                    },
                    _ => {
                        println!("Invalid usage, please run with the --help flag");
                        std::process::exit(1);
                    }
                }
            },
            None => {
                println!("Invalid usage, please run with the --help flag");
                std::process::exit(1);
            }
        }
    }

    let start = Instant::now();

    let num_files = lib::run(starting_path.as_str(), scan_time.as_str(), barcode);
    
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

