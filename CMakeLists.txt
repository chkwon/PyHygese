cmake_minimum_required(VERSION 3.15)

set(CMAKE_INSTALL_PREFIX ${CMAKE_SOURCE_DIR} CACHE PATH "install prefix" FORCE)
set(CMAKE_BUILD_TYPE "Release")

project(
    ${SKBUILD_PROJECT_NAME}
    VERSION ${SKBUILD_PROJECT_VERSION}
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 17)

include(FetchContent)
FetchContent_Declare(
  hgscvrp
  GIT_REPOSITORY https://github.com/mdealencar/HGS-CVRP.git
  GIT_TAG main
)
FetchContent_MakeAvailable(hgscvrp)

# runtime library
if(CMAKE_HOST_WIN32)
  install(TARGETS lib RUNTIME DESTINATION hygese)
else()
  install(TARGETS lib LIBRARY DESTINATION hygese)
endif()
