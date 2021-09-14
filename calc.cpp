#include<stdio.h>
#include<vector>
#include<fstream>
#include<sstream>
#include<string.h>
#include <algorithm>

using namespace std;

vector<vector<vector<int>>> options;
vector<int> max_values;
vector<int> values;
int n_options;

void read_csv(string filename){
    vector<int> result;
    ifstream file(filename, ios::in);
    if(!file.is_open())
        throw runtime_error("Could not open file");
    string line;
    int val;
    int line_count = 0;
    while(getline(file, line)){
        stringstream ss(line);
        while(ss >> val){
            result.push_back(val);
            if(ss.peek() == ',')
                ss.ignore();
        }
        int index = result[0];
        result.erase(result.begin());
        int sz = (int)options.size();
        if (sz <= index){
            vector<vector<int>> l;
            l.push_back(result);
            options.push_back(l);
        }else{
            options[sz-1].push_back(result);
        }
        result.clear();
    }
}

vector<int> intersection(vector<int> &v1, vector<int> &v2){
    vector<int> v3;
    set_intersection(v1.begin(), v1.end(), v2.begin(), v2.end(), back_inserter(v3));
    return v3;
}

bool increment(){
    bool done = false;
    int i = 0;
    while ((!done) && (i < n_options)){
        values[i]++;
        if (values[i] > max_values[i]){
            values[i] = 0;
            i++;
        }else{
            done = true;
        }
    }

    if (!done){
        return true;
    }
    return false;
}

int main(){
    read_csv("horarios.csv");

    
    n_options = (int)options.size();    
    for (int i = 0; i < n_options; i++){
        max_values.push_back((int)options[i].size());
        values.push_back(0);
    }
    

    vector<vector<int>> generated;

    vector<vector<int>> horarios;
    while (true){
        bool valid = true;
        horarios.clear();
        for (int i = 0; i < n_options; i++){
            if(values[i] != 0)
                horarios.push_back(options[i][values[i]-1]);
        }
        
        int sz = (int)horarios.size();
        for(int i = 0; i < sz; i++){
            for(int j = 0; j < sz; j++){
                if ((i == j)||(values[i] == 0)||(values[j] == 0))
                    continue;
                auto inter = intersection(horarios[i], horarios[j]);
                if ((int)inter.size() > 0){
                    valid = false;
                    break;
                }
            }
            if(!valid)
                break;
        }
        if (valid){
            generated.push_back(values);
        }
        if (increment()){
            break;
        }
    }
    vector<int> indexes;
    bool found = false;
    for(int k = 0; k < 4 && !found; k++){
        int look_for = k;
        int count = 0;
        for(int i = 0; i < (int)generated.size(); i++){
            vector<int> v = generated[i];
            int count_0 = 0;
            for(int i: v){
                if (i == 0){
                    count_0++;
                }
            }
            if(count_0 == look_for){
                count++;
                found = true;
                indexes.push_back(i);
            }
        }
    }
    for(int i: indexes){
        for(int j: generated[i]){
            printf("%d ", j);
        }
        printf("\n");
    }
    
    return 0;
}