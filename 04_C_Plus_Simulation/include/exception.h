/**
 * @file exception.h
 * @brief Exception handling
 * @author caixc (171586490@qq.com)
 * @version 1.0
 * @date 2021-05-09
 * 
 * @copyright Copyright (c) {2020}
 * 
 * @par 修改日志:
 * <table>
 * <tr><th>Date       <th>Version <th>Author  <th>Description
 * <tr><td>2021-05-09 <td>1.0     <td>caixc     <td>第一次提交
 * </table>
 */

#ifndef EXCEPTION_H
#define EXCEPTION_H

#include <exception>
#include <string>

using namespace std;

/**
 * @brief Exception handling
 */
class MyException : public exception {
    public:
        MyException(string str) : message("Error: " + str) {}
        ~MyException() throw () {}

        virtual const char* what() const throw () {
            return message.c_str();
        }

    private:
        string message;
};

#endif
