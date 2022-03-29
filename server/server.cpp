
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <signal.h>
#include <cstdio>
#include <memory>
#include <stdexcept>
#include <string>
#include <array>
#include "FileWatcher.h"

using namespace std;

string exec(const char* cmd) {
    array<char, 128> buffer;
    string result;
    unique_ptr<FILE, decltype(&_pclose)> pipe(_popen(cmd, "r"), _pclose);
    if (!pipe) {
        throw runtime_error("popen() failed!");
    }
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    return result;
}

int main(int argc, char* argv[]) {
  FileWatcher fw{"L:", chrono::milliseconds(500)};

  fw.start([] (string path_to_watch, FileStatus status) -> void {
  // Process only regular files, all other file types are ignored
    if(!filesystem::is_regular_file(filesystem::path(path_to_watch)) && status != FileStatus::erased) {
      return;
    }
 
    switch(status) {
      case FileStatus::created:
        //cout << "File created: " << path_to_watch << '\n';
        break;
      case FileStatus::modified:
		cout << path_to_watch << endl;
        if(path_to_watch == "L:\in.laps") {
          string computer_name = "";
          string line;
          ifstream request_file;
          request_file.open("L:\\in.laps", ios::in);
          while (getline (request_file,line)) {
            computer_name += line;
          }
          request_file.close();

          ofstream response_file;
          response_file.open("L:\\out.laps", ios::trunc);
          string command = "powershell \"Get-AdmPwdPassword -ComputerName " + computer_name + " | select -ExpandProperty Password\"";
          string password = exec(command.c_str()).replace("\n", "");
          response_file << password;
          response_file.close();
        }
        //cout << "File modified: " << path_to_watch << '\n';
        break;
      case FileStatus::erased:
        //cout << "File erased: " << path_to_watch << '\n';
        break;
      default:
        cout << "Error! Unknown file status.\n";
    }
  });
}