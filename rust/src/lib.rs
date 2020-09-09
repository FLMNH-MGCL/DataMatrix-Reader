use std::process::{Command};
use std::collections::HashMap;
use std::time::Instant;
use std::io;
use std::io::prelude::*; 

extern crate regex;
extern crate glob;

use glob::glob;
// use regex::Regex;
use fancy_regex::Regex;

// #[derive(PartialEq, PartialOrd)]
// pub enum RUN_TYPES {
//     BOTH,
//     DATAMATRIX,
//     BARCODE
// }

/// Returns a string - the stdout from 'dmtxread' utility, CLI program
///
/// # Arguments
///
/// * `path` - A str filesystem path, the location of the image to scan
/// * `scan_time` - Milliseconds (as str) allowed to scan before quitting
pub fn dmtxread(path: &str, scan_time: &str) -> String {
    let ms_time = format!("{}{}", "-m", scan_time);

    let output = Command::new("dmtxread")
        .arg("--stop-after=1")
        .arg(ms_time.as_str())
        .arg(path)
        .output()
        .expect("dmtxread command failed to start. Please ensure it is installed in your system");

    let mgcl_number = String::from(String::from_utf8_lossy(&output.stdout));

    match mgcl_number.as_str() {
        "" => return String::default(),
        _ => return mgcl_number,
    }
}

/// Returns a string - the stdout from 'zbarimg' utility, CLI program
///
/// # Arguments
///
/// * `path` - A str filesystem path, the location of the image to scan
pub fn zbarimg(path: &str) -> String {
    let output = Command::new("zbarimg")
        .arg(path)
        .output()
        .expect("zbarimg command failed to start. Please ensure it is installed in your system");

    let mgcl_number = String::from(String::from_utf8_lossy(&output.stdout));

    match mgcl_number.as_str() {
        "" => return String::default(),
        _ => return mgcl_number,
    }
}

/// Collect all JPG and jpg files at and below a starting directory
///
/// # Arguments
///
/// * `starting_path` - A str filesystem path, the location to start at
pub fn collect(starting_path: &str) -> Vec<std::path::PathBuf>{
    print!("Collecting files...");
    io::stdout().flush().unwrap();


    let start = Instant::now();

    let pattern_JPG = format!("{}/**/*.JPG", starting_path);
    let pattern_jpg = format!("{}/**/*.jpg", starting_path);

    let  files_raw: Result<Vec<_>, _>  = glob(pattern_JPG.as_str())
        .unwrap()
        .chain(glob(pattern_jpg.as_str()).unwrap())
        .collect();

    let mut files = match files_raw {
        Ok(v) => v,
        _ => std::vec::Vec::default()
    };

    let end = start.elapsed();

    println!("done!");

    if files.len() < 1 {
        println!("No files to collect...");
        return files;
    }


    files.sort_by(|a,b| a.as_os_str().cmp(b.as_os_str()));

    println!("Files collected in {:?}...\n", end);


    files
}

fn convert_decoded_to_name(decoded_data: &str) -> String {
    let re = Regex::new(r"(.*?)MGCL\s?[0-9]{7,8}").unwrap();

    let mut regex_ret = re.captures(&decoded_data).unwrap();

    let mut result = "";

    match regex_ret {
        Some(captures) => {
            match captures.get(0) {
                Some(group) => {
                    let decoded_vec = decoded_data.split_at(group.start());
                    // println!("{:?}", text.split_at(group.start()));
                    result = decoded_vec.1;
                },
                _ => ()
            }
        },
        _ => ()
    }

    // remove trailing, leading whitespace, 
    // newlines, replace spaces with _ and remove instances of CODE-128
    result
        .trim()
        .replace("\n", "")
        .replace(" ", "_")
        .replace("CODE-128:", "").to_string()
}

/// Ensure the libraries / CLI utilities are installed on the system, will panic on failure
fn check_installations() {
    print!("Checking installations of dmtx-utils and zbar...");
    io::stdout().flush().unwrap();

    Command::new("dmtxread")
        .arg("--help")
        .output()
        .expect("dmtxread command failed to start. Please ensure dmtx-utils are installed in your system");

    Command::new("zbarimg")
        .arg("--help")
        .output()
        .expect("zbarimg command failed to start. Please ensure zbar is installed in your system");

    println!("passed!");
}



// todo: remove return - maybe?
/// Decoded datamatrices and barcodes at and below given OS path starting point
///
/// # Arguments
///
/// * `starting_path` - A str filesystem path, the location to start at
/// * `scane_time` - A str representing the maximum time in ms to search for a datamatrix
/// * `include_barcodes` - A bool that will include barcode (zbar) attempts on failed dmtx decodes
pub fn run(starting_path: &str, scan_time: &str, include_barcodes: bool) -> usize {
    check_installations();
    
    let mut specimen: HashMap::<String, std::vec::Vec<String>> = HashMap::new();
    let mut edits: HashMap::<String, String> = HashMap::new();
    let mut failures: Vec<String> = Vec::new();

    let files = collect(starting_path);
    let ret = files.len();

    // println!("{:?}", files);

    for path_buffer in files {
        print!("Attempting to extract datamatrix data from {}...", path_buffer.to_str().unwrap());
        io::stdout().flush().unwrap();

        let mut decoded_data = dmtxread(path_buffer.to_str().unwrap(), scan_time);

        if decoded_data == "" {
            println!("failed! (no datamatrix data could be extracted)\n");

            if include_barcodes {
                print!("Attempting to extract barcode data from {}...", path_buffer.to_str().unwrap());
                io::stdout().flush().unwrap();


                decoded_data = zbarimg(path_buffer.to_str().unwrap());

                if decoded_data == "" {
                    println!("failed! (no barcode data could be extracted)\n");
                    failures.push(path_buffer.to_str().unwrap().to_string());

                    continue;
                }
            } else {
                failures.push(path_buffer.to_str().unwrap().to_string());
                continue;
            }
        }

        let proper_name = convert_decoded_to_name(decoded_data.as_str());

        // TODO: FIXME: not working right, not registering as existing so everthing is marked as _D
        let specimen_vec = specimen.get_mut(proper_name.as_str());
        match specimen_vec {
            Some(occurrences) => {
                let suffix = match occurrences.len() {
                    1 => "_D",
                    2 => "_V",
                    _ => "_MANUAL"
                };

                let full_name = format!("{}{}.{}", proper_name.clone(), suffix, path_buffer.extension().unwrap().to_str().unwrap());

                edits.insert(path_buffer.to_str().unwrap().to_string(), full_name.clone());

                occurrences.push(path_buffer.to_str().unwrap().to_string());

                println!("success!\nProper name determined to be: {}\n", full_name);
            },

            _ => {
                let full_name = format!("{}{}.{}", proper_name.clone(), "_D", path_buffer.extension().unwrap().to_str().unwrap());

                edits.insert(path_buffer.to_str().unwrap().to_string(), full_name.clone());
                specimen.insert(proper_name.as_str().to_string(), vec![path_buffer.to_str().unwrap().to_string()]);

                println!("success!\nProper name determined to be: {}\n", full_name);
            }
        };

    }

    println!("All computations completed... Now printing old file paths and their corresponding renames: ");
    
    for (old,new) in edits {
        println!("{} : {}", old, new);
    }

    if ret != 0 {
        println!("\nThere were {} failed attempts at reading datamatrices / barcodes", failures.len());
        println!("Failure rate: {}", failures.len() as u32 / ret as u32);

    }

    ret

}

#[cfg(test)]
mod tests {
    use super::*;
    // #[test]
    // fn test_collect() {
    //     collect("/Users/aaronleopold/Documents/museum/datamatrix/test_images")
    // }

    // #[test]
    // fn test_run() {
    //     run("/Users/aaronleopold/Documents/museum/datamatrix/test_images")
    // }

    #[test]
    fn test_pass() {
        assert_eq!(dmtxread("/Users/aaronleopold/Documents/museum/datamatrix/test_images/matrices/MGCL_1037779_D.JPG", "30000"), String::from("MGCL 1037795"));
    }

    #[test]
    fn test_fail() {
        assert_eq!(dmtxread("/Users/aaronleopold/Documents/museum/datamatrix/test_images/2d/IMG017.jpg", "30000"), String::from(""));
    }
}

