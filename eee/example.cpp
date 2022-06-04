#include <iostream>
#include <string>
#include <cassert>

using namespace std;

/////////////////////////
//Ide dolgozz!!

class Kutya {
private:
    string nev;
    unsigned int kor;

public:
    const string &get_nev() const {
        return nev;
    }

    unsigned int get_kor() const {
        return kor;
    }

    Kutya(const string &nev, unsigned int kor) : nev(nev), kor(kor) {
        cout << "Kutya letrehozva" << endl;
    }

    virtual string pedigre() const {
        return "nev:" + nev + ", " + "kor:" + to_string(kor) + " ev";
    }

    virtual string* terel(const string* nyaj, unsigned& nyajhossz) const {
        if (nyaj == nullptr || nyajhossz == 0) {
            nyajhossz = 0;
            return nullptr;
        }

        string* uj = new string[nyajhossz];
        for (int i = 0; i < nyajhossz; ++i) {
            uj[i] = nyaj[i];
        }
        return uj;
    }
};

class BorderCollie final:public Kutya {
private:
    unsigned int terelo_kapacitas;

public:
    unsigned int get_terelo_kapacitas() const {
        return terelo_kapacitas;
    }

    BorderCollie(const string &nev, unsigned int kor, unsigned int tereloKapacitas) : Kutya(nev, kor), terelo_kapacitas(
            tereloKapacitas) {}

    string pedigre() const override {
        return "nev:" + this->get_nev() + ", kor:" + to_string(this->get_kor()) + " ev, faj:border collie, terelo kapacitas:" + to_string(terelo_kapacitas) + " db birka";
    }

    unsigned int first_not_empty(const string* s, unsigned int len) const {
        for (int i = 0; i < len; ++i) {
            if (!s[i].empty()) {
                return i;
            }
        }
    }

//    void print_nyaj(const string* s, unsigned int len) const {
//        cout << "nyaj: ";
//        for (int i = 0; i < len; ++i) {
//            cout << (s[i].empty() ? "-, " : s[i] + ", ");
//        }
//        cout << endl;
//    }

    string* terel(const string* nyaj, unsigned& nyajhossz) const override {
        if (nyaj == nullptr || nyajhossz == 0) {
            nyajhossz = 0;
            return nullptr;
        }
//        print_nyaj(nyaj, nyajhossz);

        string* uj = new string [nyajhossz];

        string* copy = new string [nyajhossz];
        for (int i = 0; i < nyajhossz; ++i) {
            copy[i] = nyaj[i];
        }

        unsigned int counter = 0;
        int i = 0;
        int nyajidx = 0;
        for (; i < nyajhossz; ++i) {
//            print_nyaj(uj, nyajhossz);
            if (counter >= this->terelo_kapacitas) {
                break;
            }
            nyajidx = first_not_empty(copy, nyajhossz);
            uj[i] = nyaj[nyajidx];
            copy[nyajidx] = "";
            counter++;
        }

        for (int j = i; j < nyajhossz; ++j, nyajidx++) {
            uj[j] = copy[nyajidx];
        }

//        print_nyaj(uj, nyajhossz);

        int utolso = 0;
        for (int j = 0; j < nyajhossz; ++j) {
            if (!uj[j].empty()) {}
            utolso = j;
        }
        nyajhossz = utolso+1;

        return uj;
    }

};

void print(const Kutya& k) {
    cout << k.pedigre() << endl;
}

////////////////////////

//=== Teszteles bekapcsolasa kikommentezessel
#define TEST_kutya
#define TEST_pedige
#define TEST_terel
#define TEST_border_collie
#define TEST_pedigre_bc
#define TEST_terel_bc
//=== Teszteles bekapcsolas vege

/*
Készíts egy Kutya nevű osztályt!
Adattagok:
 - nev: a kutya neve 
 - kor: a kutya életkora (unsigned)

Készítsd el a Kutya osztály konstruktorát is, amely két paramétert vár az adattagok inicializálására. 
A konstruktorban az inicializálások után az alábbi szöveg kerüljön kiírásra a standard outputon:
"Kutya letrehozva"
A kiíratást sortörés kövesse.
*/
void test_kutya(){
  #if defined TEST_kutya && !defined TEST_BIRO
  const Kutya k("Lassie", 3);
  assert(k.get_nev() == "Lassie");
  assert(k.get_kor() == 3);
  #endif
}


/*
Készíts egy pedigre() publikus metódust a Kutya osztályban, mely sztring formában adja vissza a kutya adatait. A formátum a következő legyen:
nev:<nev>, kor:<kor> ev
A sztring végén ne legyen sortörés karakter, a kacsacsőrökkel jelzett értékek pedig helyettesítődjenek a megfelelő adattagok értékeivel (a vessző után illetve a <kor> és az ev között szóköz van). 
*/
void test_pedigre(){
  #if defined TEST_pedigre && !defined TEST_BIRO
  const Kutya k("Lassie", 3);
  string s = k.pedigre();
  assert(s == "nev:Lassie, kor:3 ev");
  #endif
}


/*
Készíts egy publikus string* terel(const string* nyaj, unsigned& nyajhossz) metódust, melynek első paramétere egy std sztringeket tartalmazó tömb, a második egy unsigned érték, a tömb hossza. 
A paraméterben kapott tömb egy birkanyájat reprezentál, a visszatérési érték pedig egy olyan tömb, ami az összeterelt nyájat reprezentálja. 
Az input nyájat nem kell módosítani. 
Egy kutya alapból nem tud nyájat terelni, ezért ebben a metódusban mindössze annyi történjen, hogy legyen a teljes input tömb átmásolva egy dinamikusan lefoglalt tömbbe és ezzel térjen vissza a függvény. 
A dinamikusan foglalt tömb felszabadításával a metódusnak nem kell foglalkoznia! 
A nyajhossz paraméter értéke maradjon az eredeti érték. Amennyiben az input nyáj null pointer vagy a hossza nulla, akkor null pointert (nullptr) kell visszaadni és a nyajhossz paramétert 0-ra kell állítani. 
Működjön a metódus konstans objektumon is!
*/
void test_terel(){
  #if defined TEST_terel && !defined TEST_BIRO
  const Kutya k("Lassie", 3);
  string nyaj[] = {"Frici", "Julcsa", "Gyuri", "Margit"};
  unsigned nyajhossz = 4;

  string* dinamikus_nyaj = k.terel(nyaj, nyajhossz);
  assert(nyajhossz == 4);
  assert(dinamikus_nyaj[3] == "Margit");
  delete[] dinamikus_nyaj;
  #endif
}

/*
Készíts egy BorderCollie osztályt, mely publikusan öröklődik a Kutya osztályból. 
Új adattagok:
- terelo_kapacitas: hány birkát tud terelni (unsigned) 

A BorderCollie osztály rendelkezzen egy három paraméteres konstruktorral. 
Az első kettő az ősosztály adattagjait beállító string és unsigned érték, a harmadik paraméter pedig szintén egy unsigned, amely a terelő kapacitást állítja be.
*/
void test_border_collie(){
  #if defined TEST_border_collie && !defined TEST_BIRO
  const BorderCollie bc("Jess", 13, 5);
  assert(bc.get_nev() == "Jess");
  assert(bc.get_kor() == 13);
  assert(bc.get_terelo_kapacitas() == 5);
  #endif 
}

/*

Definiáld felül a BorderCollie osztályban a \texttt{pedigre} metódust. A létrehozott sztring így nézzen ki:
nev:<nev>, kor:<kor> ev, faj:border collie, terelo kapacitas:<terelo_kapacitas> db birka
*/
void test_pedigre_bc(){
  #if defined TEST_pedigre_bc && !defined TEST_BIRO
  const Kutya* bc = new BorderCollie("Jess", 13, 5);
  string s = bc->pedigre();
  assert(s == "nev:Jess, kor:13 ev, faj:border collie, terelo kapacitas:5 db birka");
  delete bc;
  #endif
}


/*
Definiáld felül a BorderCollie osztályban a terel metódust. Ez a kutyafaj már képes nyájat terelni. 
A terelés a következő módon történik. A paraméterben kapott tömbben minden 0 karakternél hosszabb sztring egy birka nevének felel meg, az üres sztringek pedig lyukaknak, ahol épp nincs birka. 
Az ügyes terelőkutya úgy tereli össze a nyájat, hogy ne legyenek lyukak benne, de megtartja a birkák kezdeti sorrendjét.

Az output/összeterelt nyáj lesz a viszatérési érték, melyet szintén dinamikus módon kell lefoglalni (és a felszabadítással nem kell törődni). 
A tömb méretét nem muszáj optimálisra (azaz az összeterelt nyáj méretére szabva megválasztani). 
A metódus módosítsa a paraméterben kapott nyajhossz értéket is. A módosított nyajhossz tartalmazza a visszaadott tömb méretét addig a pontig, ahol az utolsó birka van.

Amennyiben az input nyáj null pointer vagy a hossza nulla, akkor null pointert (nullptr) kell visszaadni és a nyajhossz paramétert 0-ra kell állítani.
Olyan eset nem lehetséges, hogy a paraméterben kapott nyáj lyukkal, azaz üres sztringgel/sztringekkel végződik.

Még egy esetet le kell kezelni. A border collie-k nem tudnak tetszőleges méretű nyájat terelni, de azért megpróbálják a legtöbbet tenni, ami tőlük telik. 
Abban az esetben, ha a terelo_kapacitas értéküket meghaladó birkán haladtak már keresztül, leállnak a tereléssel és a nyáj végét úgy hagyják, ahogy volt. 
(Példák a feladat.pdf-ben) 
*/
void test_terel_bc(){
  #if defined TEST_terel_bc && !defined TEST_BIRO
  const Kutya* bc = new BorderCollie("Jess", 13, 3);
  string nyaj[] = {"Frici", "", "Julcsa", "Gyuri", "", "Margit"};
  unsigned nyajhossz = 6;

  string* dinamikus_nyaj = bc->terel(nyaj, nyajhossz);
  assert(dinamikus_nyaj[0] == "Frici");
  assert(dinamikus_nyaj[1] == "Julcsa");
  assert(dinamikus_nyaj[2] == "Gyuri");
  assert(dinamikus_nyaj[3] == "");//terelokapacitas!
  assert(dinamikus_nyaj[4] == "");
  assert(dinamikus_nyaj[5] == "Margit");
  assert(nyajhossz == 6);
  delete[] dinamikus_nyaj;
  #endif
  
}

int main(){

  test_kutya();
  test_pedigre();
  test_terel();
  test_border_collie();
  test_pedigre_bc();
  test_terel_bc();
  return 0;
}
