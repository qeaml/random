#include "dir.h"
#include <filesystem>

void iterate_dir(const char *path, pathfunc f) {
  const std::filesystem::path dir_path{path};
  const std::filesystem::directory_iterator iter{dir_path};

  for(auto const& dir_entry: iter) {
    f(dir_entry.path().string().c_str());
  }
}