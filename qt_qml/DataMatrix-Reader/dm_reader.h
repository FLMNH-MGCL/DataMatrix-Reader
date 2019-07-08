#ifndef DM_READER_H
#define DM_READER_H

#include <QZXing.h>
#include <tuple>
#include <vector>
#include <map>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>
#include <sstream>
#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <dirent.h>


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

    std::string status;

public:
    /*======================================================
     * Initialization Functions
    ======================================================*/
    DM_Reader(std::string);

    /*======================================================
     * Main Functions
    ======================================================*/
    int RecursiveDecode(std::string);
    int Decode(std::string);
    bool RecursiveRename(std::string);
    bool Rename(std::string, int);
    bool Undo();
    // int Run(); ??

    /*======================================================
     * Accessor Functions
    ======================================================*/
    std::string GetNewName(int);
    std::vector<std::string> GetSubFolders(std::string);
    std::vector<std::string> GetFiles(std::string);
    int GetOccurrences(int);

    /*======================================================
     * Mutator Functions
    ======================================================*/
    void ToggleRecursion();
    void SetStatus(std::string);

    /*======================================================
     * Helper Functions
    ======================================================*/
    short IsDir(std::string);
};

#endif // DM_READER_H
