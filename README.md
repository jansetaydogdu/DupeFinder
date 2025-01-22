# DupeFinder
This project finds product alternatives based on ingredient lists. By analyzing ingredients, it suggests similar products that maintain desired attributes. For example, it can provide cruelty-free options, more affordable alternatives, and/or allergen-free formulations.

Install python dependancies :  
`pip3 install --user -r DupeFinder/src/build/src/Required.txt`

# Build instructions
Use pip to install python dependancies as above.
Building this project requires
- python3-devel
- gcc
- cmake

If you want to contribute to the project just open DupeFinder in qtcreator and get started.  
If you simply want to build a version continue.

Go to build directory :  
`cd DupeFinder/src/build`  

Make a folder for your version. We will use Desktop-Release. See Optional Versions at the bottom and replace if you need.  
`mkdir Desktop-Release`  

Go to the new directory  
`cd Desktop-Release`  

Initialize cmake in the current directory  
`cmake build -DCMAKE_BUILD_TYPE=Desktop-Release ../../`  

Finally build with cmake  
`cmake --build .`  

Optional Versions : Desktop-Debug, Desktop-Release, Desktop-MinSizeRel, Desktop-RelWithDebInfo.
