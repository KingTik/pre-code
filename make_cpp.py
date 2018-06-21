#!/usr/bin/env python
import os
import sys

def make_makefile():
    makefile = open('makefile', "w+")
    makefile.write("all:\n")
    makefile.write("clean:")
    makefile.close()

cpp_file_content = '''#include <iostream>
#include <algorithm>
#include <vector>
#include <functional>
#include <chrono>

namespace tw{
    template <typename T> void print(const T &list);
    template<typename TimeScale = std::chrono::milliseconds>
    auto benchmark(std::function<void(void)> tested_function) 
        -> decltype(std::chrono::duration_cast<TimeScale>(static_cast<std::chrono::duration<int>>(0)).count());
}

int main(int argc, char** argv){
    std::vector<std::string> arguments(argv, argv+argc);

}


namespace tw{
    template <typename T>
    void print(const T &list)
    {
        auto start = std::begin(list);
        auto end = std::end(list);
        if(start != end) { 
            std::cout << "[";
            std::for_each(start, --end, [](auto element){
                std::cout << element << ", ";
            });

            std::cout << *end << "]" <<std::endl;
        }else{
            std::cout <<"[]" <<std::endl;
        }
    }


    template<typename TimeScale = std::chrono::milliseconds>
    auto benchmark(std::function<void(void)> tested_function) 
        -> decltype(std::chrono::duration_cast<TimeScale>(static_cast<std::chrono::duration<int>>(0)).count())
    {
        auto start = std::chrono::system_clock::now();

        tested_function();

        auto end = std::chrono::system_clock::now();
        auto elapsed = std::chrono::duration_cast<TimeScale>(end - start);
        return elapsed.count();
    }
}


'''

c_file_content='''#include <stdio.h>
#include <string.h>



int main(int argc, char** argv){
  

}

'''

if len(sys.argv) > 1:

    
    
    new_code_file = sys.argv[1].strip()
    for element in os.listdir(os.getcwd()):
        if os.path.isfile(os.path.join(os.getcwd(),element)):
            if element == new_code_file:
                sys.exit("You have that file already, jesus who do i work with")

    if new_code_file.find('.') < 0:
        sys.exit("What is this? Give me a proper file idiot")

    #Lets check what file type we're dealing with
    compiler = ''
    file_content = ''
    if new_code_file.endswith('.cpp'): #oh, its a cpp file!
        compiler = 'g++ -std=c++17'
        file_content = cpp_file_content
    elif new_code_file.endswith('.c'): #oh, its a c file!
        compiler = 'gcc'
        file_content = c_file_content
    else:
        sys.exit("I can't handle this shity file format!") #oh, its a shit file!

    #file name withot extension
    just_name = new_code_file[0:new_code_file.find('.')]

    # create and fill file
    new_cpp_file_handle = open(new_code_file, "w+")
    new_cpp_file_handle.write(file_content)
    new_cpp_file_handle.close()

    # check for makefile
    if not os.path.isfile('makefile'):
        make_makefile()
        
    #Lets check if we already have something like that in makefile
    #for example if we have test.cpp and test.c would get 'test: ' in makefile 
    with open('makefile', 'r') as makefile_handler:
        all_lines = makefile_handler.readlines()
        for line in all_lines:
            if line.strip().startswith(just_name+':'):
                just_name+='-'+new_code_file[new_code_file.find('.')+1:]

    #add new file to makefile
    with open('makefile', "a") as makefile_handler:
        makefile_handler.write('\n')
        makefile_handler.write(just_name)
        makefile_handler.write(': ')
        makefile_handler.write(new_code_file)
        makefile_handler.write("\n\t"+compiler+" -o ")
        makefile_handler.write(just_name)
        makefile_handler.write(" ")
        makefile_handler.write(new_code_file)

# got to add clean procedure to makefile


    
    lines = open('makefile').read().splitlines()
    lines[0] = lines[0]+" " + just_name
    
    open('makefile','w').write('\n'.join(lines))            

else: 
    print "Give me a name, moron"
