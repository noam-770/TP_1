#include <iostream>
using namespace std;
int main() {
    string alphabet;
    cout<< "Bonjour, veuillez saisir un alphabet :" <<endl;
    cin>>alphabet;
    
    int nombre_de_caracteres;
    cout<< "Veuillez saisir le nombre de caractères du mot de passe :" <<endl;
    cin>>nombre_de_caracteres;

    if (nombre_de_caracteres<0)
    {
        nombre_de_caracteres = 0;
    }
    

    for (int i=0;i<nombre_de_caracteres;i++) {
        cout<< alphabet[i];
        
    }

    return 0;
    
}
