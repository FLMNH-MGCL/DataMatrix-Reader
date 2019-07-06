#ifndef DM_READER_H
#define DM_READER_H

#include <QZXing.h>
#include <tuple>
#include <vector>
#include <map>
#include <stdio.h>
#include <stdlib.h>
#include <string>


class DM_Reader
{
private:
    // tuple: old path,new path
    std::vector<std::tuple<std::string,std::string>> old_new_paths;

    // map: specimen id,occurence count
    std::map<int,int> occurrences;

    // target directory
    std::string parent_directory;

    bool recursively;
    // virtual file system (not sure if necessary)

public:
    /*======================================================
     * Initialization Functions
    ======================================================*/
    DM_Reader(std::string);

    /*======================================================
     * Main Functions
    ======================================================*/
    bool RecursiveRename(std::string);
    bool Rename(std::string, int);
    bool Undo();

    /*======================================================
     * Accessor Functions
    ======================================================*/
    std::string GetNewName(int);
    std::vector<std::string> GetSubFolders(std::string);
    int GetOccurrences(int);

    /*======================================================
     * Mutator Functions
    ======================================================*/
    void ToggleRecursion();
};

#endif // DM_READER_H
