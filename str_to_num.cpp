#include<string>
#include<iostream>
#include<vector>

std::string hex(int num)
{
    const std::vector<char> charset = {
        '0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'
    };
    std::string temp;
    temp += charset[(int)(num / 16)];
    num -= (int)(num / 16) * 16;
    temp += charset[num];
    return temp;
}

int main()
{
    std::string str;
    std::cout << "write something: ";
    std::cin >> str;
    for(char c : str)
        std::cout << hex((int)c) << "\t" << (char)c << std::endl;
    return 0;
}