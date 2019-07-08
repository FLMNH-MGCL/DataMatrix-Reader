#include "dm_reader.h"

/*======================================================
 * Initialization Functions
======================================================*/
DM_Reader::DM_Reader(std::string dir)
{
    // check if folder exists
    // if it does, proceed
    this->parent_directory = dir;
    recursively = false;
}

/*======================================================
 * Main Functions
======================================================*/
int DM_Reader::Decode(std::string path)
{
    QImage image(path.c_str());
    QZXing decoder;
    decoder.setDecoder( 1 << 6 );
    QString result = decoder.decodeImage(image);

    std::cout << result.toUtf8().constData() << std::endl;
    return 0;
}

bool DM_Reader::RecursiveRename(std::string path)
{
    std::vector<std::string> sub_dirs = GetSubFolders(path);
    for (std::string folder : sub_dirs) {
        RecursiveRename(path + folder + '/');
    }
    std::vector<std::string> files = GetFiles(path);
    for (std::string file : files) {
        int scanned_id = Decode(path + file);
        Rename(path + file, scanned_id);
    }

    return true;
}

bool DM_Reader::Rename(std::string path, int scanned_id)
{
    std::string new_name = this->GetNewName(scanned_id);

    // separate path from file (research more efficient solution)
    std::string old_path = "";
    std::string old_name = "";
    std::stringstream ss(path);
    std::vector<std::string> parsed_path;
    std::string token;
    while (std::getline(ss, token, '/')) {
        parsed_path.push_back(token);
    }
    for (unsigned int i = 0; i < parsed_path.size(); i++) {
        if (i != parsed_path.size() - 1) {
            old_path += (parsed_path[i] + '/');
        }
        else {
            old_name = token;
        }
    }


    // create new path
    std::string new_path = old_path + new_name;
    old_path += old_name;

    // rename
    /*
    if (std::rename(new_path, old_path) != 0) { => UNCOMMENT AFTER TESTING
        return false;
    }
    */
    printf("Renaming %s as %s", old_path.c_str(), new_path.c_str());

    this->old_new_paths.push_back(std::tuple<std::string,std::string>(old_path, new_path));

    return true;
}

bool DM_Reader::Undo()
{
    for (unsigned int i = 0; i < this->old_new_paths.size(); i++)
    {
        std::tuple<std::string,std::string> curr = this->old_new_paths.at(i);
        const char *old_path = (std::get<0>(curr)).c_str();
        const char *new_path = (std::get<1>(curr)).c_str();

        /*
        if (std::rename(new_path, old_path) != 0) { => UNCOMMENT AFTER TESTING
            return false;
        }
        */
        printf("Renaming %s as %s", new_path, old_path);
    }

    return true;
}


/*======================================================
 * Accessor Functions
======================================================*/
std::string DM_Reader::GetNewName(int scanned_id)
{
    std::string new_name = "MGCL_" + std::to_string(scanned_id);
    int occurrences = this->GetOccurrences(scanned_id);

    if (occurrences == 0) {
        // decide on formatting
    }
    else if (occurrences == 1) {
        // decide on formatting
    }
    else {
        // edge case, mark as such (could be lateral view)
    }

    return new_name;
}

int DM_Reader::GetOccurrences(int scanned_id)
{
    return this->occurrences[scanned_id];
}

std::vector<std::string> DM_Reader::GetSubFolders(std::string path)
{
    std::vector<std::string> sub_dirs;

    short safe = IsDir(path);
    if (safe != -1 && safe != 0) {
        DIR *dir;
        struct dirent *file;
        dir = opendir(path.c_str());
        if (dir) {
            while ((file = readdir(dir)) != NULL) {
                //std::cout << file->d_name << std::endl;
                std::string filename = path + file->d_name;
                if (std::string(file->d_name) == "." || std::string(file->d_name) == "..") { continue; }

                short is_file = IsDir(filename);
                if (is_file == -1 || is_file == 0) { continue; }

                // is dir
                sub_dirs.push_back(filename);
            }
            closedir(dir);

            //for (std::string name : sub_dirs) {std::cout << name << std::endl;}

            return sub_dirs;
        }
        else {
            return sub_dirs;
        }

    }
    else {
        return sub_dirs;
    } // temporary
}

std::vector<std::string> DM_Reader::GetFiles(std::string path)
{
    std::vector<std::string> files;

    short safe = IsDir(path);
    if (safe != -1 && safe != 0) {
        DIR *dir;
        struct dirent *file;
        dir = opendir(path.c_str());
        if (dir) {
            while ((file = readdir(dir)) != NULL) {
                // std::cout << file->d_name << std::endl;
                std::string filename = path + file->d_name;
                if (std::string(file->d_name) == "." || std::string(file->d_name) == "..") { continue; }

                short is_file = IsDir(filename);
                if (is_file == -1 || is_file == 1) { continue; }

                // is file
                files.push_back(filename);
            }
            closedir(dir);

            //for (std::string name : files) {std::cout << name << std::endl;}

            return files;
        }
        else {
            return files;
        }

    }
    else {
        return files;
    }
}


/*======================================================
 * Mutator Functions
======================================================*/
void DM_Reader::ToggleRecursion()
{
    if (this->recursively) {
        this->recursively = false;
    }
    else {
        this->recursively = true;
    }
}

void DM_Reader::SetStatus(std::string new_status)
{
    this->status = new_status;
}



short DM_Reader::IsDir(std::string path)
{
    struct stat file;
    if (stat(path.c_str(), &file) < 0) {
        // does not exist
        return -1;
    }
    else if (!S_ISDIR(file.st_mode)) {
        // exists, it is not a directory
        return 0;
    }
    else {
        // exists and is dir
        return 1;
    }
}
