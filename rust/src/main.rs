
use std::time::Instant;

mod lib;


fn main() {
    let start = Instant::now();
    let num_files = lib::run("/Users/aaronleopold/Documents/museum/datamatrix/test_images");
    let end = start.elapsed();

    println!("\nCompleted... {} files handled in {:?}.", num_files, end);
    println!("Average time per image: {:?}", end / num_files as u32);
}