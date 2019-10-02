//
// Created by William Robert Murphy on 2019-09-24.
//

#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <math.h>


double simple_interest(double A, double r, int T) {
    double FV = A*(1 + r*T);
    return FV;
}

double compound_interest(double  A, double r, int n) {
    double FV = A*pow((1+(double)(r/n)), n);
    return FV;
}




int main() {


    double sfv = simple_interest(1000, 0.1, 5);

    double cfv = compound_interest(1, 0.058, 4);

    std::cout << "simple interest: FV = " << sfv << std::endl;
    std::cout << "compound interest: FV = " << cfv << std::endl;

    return 0;
}
