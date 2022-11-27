cmake_minimum_required(VERSION 3.0.2)
project(Xcen)

add_compile_options(-std=c++11)
# find_package(OpenCV REQUIRED)

include_directories(
    ${PROJECT_SOURCE_DIR}/include
    ${PROJECT_SOURCE_DIR}/include/layer
    ${PROJECT_SOURCE_DIR}/include/matrix
    ${PROJECT_SOURCE_DIR}/include/comparison
    # ${OpenCV_INCLUDE_DIRS}
)

file(GLOB sources 
    ${PROJECT_SOURCE_DIR}/src/layer/*.cpp
    ${PROJECT_SOURCE_DIR}/src/matrix/*.cpp
    ${PROJECT_SOURCE_DIR}/src/comparison/*.cpp
)
file(GLOB headers 
    ${PROJECT_SOURCE_DIR}/include/*.h
    ${PROJECT_SOURCE_DIR}/include/layer/*.h
    ${PROJECT_SOURCE_DIR}/include/matrix/*.h
    ${PROJECT_SOURCE_DIR}/include/comparison/*.h
)

add_executable(Xcen
    main.cpp
    ${sources}
    ${headers}
)

# set(TENSORRT_LIB_DIR /home/xx/Documents/software//TensorRT-7.2.3.4/lib)
# link_directories(${TENSORRT_LIB_DIR})

target_link_libraries(Xcen
#   ${OpenCV_LIBRARIES}
)