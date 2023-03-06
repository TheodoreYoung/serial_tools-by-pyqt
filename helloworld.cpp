#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main(int argc, const char** argv) {

    vector<string> msg{"Hello", "C++", "World", "from", "VS Code"};
    vector<string> name{"Yangdonghe","is a","hero"};

    for (const string &word : msg)
    {
        cout << word << " ";
    }
    cout << endl;
    for(const string & ydh : name)
    {
        cout<<ydh<<"+";
    }
    


    cout << endl;
    return 0;
}