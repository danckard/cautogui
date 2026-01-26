#ifndef PLATFORM_H
#define PLATFORM_H

#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT __attribute__((visibility("default")))
#endif

#endif