#ifndef _DIR_H
#define _DIR_H

#ifdef __cplusplus
extern "C" {
#endif

typedef void(*pathfunc)(const char*);

void iterate_dir(const char* path, pathfunc f);

#ifdef __cplusplus
}
#endif

#endif
