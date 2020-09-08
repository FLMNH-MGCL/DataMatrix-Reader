use std::process::{Command};
use std::collections::HashMap;

extern crate regex;
extern crate glob;

use glob::glob;
use regex::Regex;

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

/// Collect all JPG and jpg files at and below a starting directory
///
/// # Arguments
///
/// * `starting_path` - A str filesystem path, the location to start at
pub fn collect(starting_path: &str) -> Vec<std::path::PathBuf>{
    println!("Collecting files...");

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

    if files.len() < 1 {
        println!("No files to collect...");
        return files;
    }


    files.sort_by(|a,b| a.as_os_str().cmp(b.as_os_str()));

    println!("Files collected...");


    files
}

fn convert_decoded_to_name(decoded_data: &str) -> String {
    // let re = Regex::new(r"").unwrap();
    // let result = re.replace_all("Hello World!", "x");

    let result = decoded_data.replace(" ", "_");

    result
}



// todo: remove return
pub fn run(starting_path: &str) -> usize {
    let mut specimen = HashMap::<String, std::vec::Vec<String>>::new();
    let mut edits = HashMap::<String, String>::new();

    let files = collect(starting_path);
    let ret = files.len();

    // println!("{:?}", files);

    for path_buffer in files {
        println!("Attempting to extract data from {}...", path_buffer.to_str().unwrap());

        let decoded_data = dmtxread(path_buffer.to_str().unwrap(), "30000");

        if decoded_data == "" {
            println!("No datamatrix data could be extracted for {}", path_buffer.to_str().unwrap());
            continue;
        }

        let proper_name = convert_decoded_to_name(decoded_data.as_str());

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

                println!("Data extracted, proper name determined to be: {}", full_name);
            },

            _ => {
                let full_name = format!("{}{}.{}", proper_name.clone(), "_D", path_buffer.extension().unwrap().to_str().unwrap());

                edits.insert(path_buffer.to_str().unwrap().to_string(), full_name.clone());
                specimen.insert(proper_name.as_str().to_string(), vec![path_buffer.to_str().unwrap().to_string()]);

                println!("Data extracted, proper name determined to be: {}", full_name);
            }
        };

    }

    println!("All computations completed... Now printing old file paths and their corresponding renames: ");
    
    for (old,new) in edits {
        println!("{} : {}", old, new);
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

