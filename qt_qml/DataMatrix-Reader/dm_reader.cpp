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
bool DM_Reader::RecursiveRename(std::string)
{
    return false;
}

bool DM_Reader::Rename(std::string path, int scanned_id)
{
    std::string new_name = this->GetNewName(scanned_id);

    // separate path from file
    std::string old_path = "";

    // create new path
    std::string new_path = old_path + new_name;

    // rename
    // std::rename(old_path.c_str(), new_path.c_str()); => UNCOMMENT AFTER TESTING
    printf("Renaming %s as %s", old_path.c_str(), new_path.c_str());
}

bool DM_Reader::Undo()
{
    for (unsigned int i = 0; i < this->old_new_paths.size(); i++)
    {
        std::tuple<std::string,std::string> curr = this->old_new_paths.at(i);
        const char *old_path = (std::get<0>(curr)).c_str();
        const char *new_path = (std::get<1>(curr)).c_str();
        // std::rename(new_path, old_path); => UNCOMMENT AFTER TESTING
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
