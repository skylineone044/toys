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
K??sz??ts egy Kutya nev?? oszt??lyt!
Adattagok:
 - nev: a kutya neve 
 - kor: a kutya ??letkora (unsigned)

K??sz??tsd el a Kutya oszt??ly konstruktor??t is, amely k??t param??tert v??r az adattagok inicializ??l??s??ra. 
A konstruktorban az inicializ??l??sok ut??n az al??bbi sz??veg ker??lj??n ki??r??sra a standard outputon:
"Kutya letrehozva"
A ki??rat??st sort??r??s k??vesse.
*/
void test_kutya(){
  #if defined TEST_kutya && !defined TEST_BIRO
  const Kutya k("Lassie", 3);
  assert(k.get_nev() == "Lassie");
  assert(k.get_kor() == 3);
  #endif
}


/*
K??sz??ts egy pedigre() publikus met??dust a Kutya oszt??lyban, mely sztring form??ban adja vissza a kutya adatait. A form??tum a k??vetkez?? legyen:
nev:<nev>, kor:<kor> ev
A sztring v??g??n ne legyen sort??r??s karakter, a kacsacs??r??kkel jelzett ??rt??kek pedig helyettes??t??djenek a megfelel?? adattagok ??rt??keivel (a vessz?? ut??n illetve a <kor> ??s az ev k??z??tt sz??k??z van). 
*/
void test_pedigre(){
  #if defined TEST_pedigre && !defined TEST_BIRO
  const Kutya k("Lassie", 3);
  string s = k.pedigre();
  assert(s == "nev:Lassie, kor:3 ev");
  #endif
}


/*
K??sz??ts egy publikus string* terel(const string* nyaj, unsigned& nyajhossz) met??dust, melynek els?? param??tere egy std sztringeket tartalmaz?? t??mb, a m??sodik egy unsigned ??rt??k, a t??mb hossza. 
A param??terben kapott t??mb egy birkany??jat reprezent??l, a visszat??r??si ??rt??k pedig egy olyan t??mb, ami az ??sszeterelt ny??jat reprezent??lja. 
Az input ny??jat nem kell m??dos??tani. 
Egy kutya alapb??l nem tud ny??jat terelni, ez??rt ebben a met??dusban mind??ssze annyi t??rt??njen, hogy legyen a teljes input t??mb ??tm??solva egy dinamikusan lefoglalt t??mbbe ??s ezzel t??rjen vissza a f??ggv??ny. 
A dinamikusan foglalt t??mb felszabad??t??s??val a met??dusnak nem kell foglalkoznia! 
A nyajhossz param??ter ??rt??ke maradjon az eredeti ??rt??k. Amennyiben az input ny??j null pointer vagy a hossza nulla, akkor null pointert (nullptr) kell visszaadni ??s a nyajhossz param??tert 0-ra kell ??ll??tani. 
M??k??dj??n a met??dus konstans objektumon is!
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
K??sz??ts egy BorderCollie oszt??lyt, mely publikusan ??r??kl??dik a Kutya oszt??lyb??l. 
??j adattagok:
- terelo_kapacitas: h??ny birk??t tud terelni (unsigned) 

A BorderCollie oszt??ly rendelkezzen egy h??rom param??teres konstruktorral. 
Az els?? kett?? az ??soszt??ly adattagjait be??ll??t?? string ??s unsigned ??rt??k, a harmadik param??ter pedig szint??n egy unsigned, amely a terel?? kapacit??st ??ll??tja be.
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

Defini??ld fel??l a BorderCollie oszt??lyban a \texttt{pedigre} met??dust. A l??trehozott sztring ??gy n??zzen ki:
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
Defini??ld fel??l a BorderCollie oszt??lyban a terel met??dust. Ez a kutyafaj m??r k??pes ny??jat terelni. 
A terel??s a k??vetkez?? m??don t??rt??nik. A param??terben kapott t??mbben minden 0 karaktern??l hosszabb sztring egy birka nev??nek felel meg, az ??res sztringek pedig lyukaknak, ahol ??pp nincs birka. 
Az ??gyes terel??kutya ??gy tereli ??ssze a ny??jat, hogy ne legyenek lyukak benne, de megtartja a birk??k kezdeti sorrendj??t.

Az output/??sszeterelt ny??j lesz a viszat??r??si ??rt??k, melyet szint??n dinamikus m??don kell lefoglalni (??s a felszabad??t??ssal nem kell t??r??dni). 
A t??mb m??ret??t nem musz??j optim??lisra (azaz az ??sszeterelt ny??j m??ret??re szabva megv??lasztani). 
A met??dus m??dos??tsa a param??terben kapott nyajhossz ??rt??ket is. A m??dos??tott nyajhossz tartalmazza a visszaadott t??mb m??ret??t addig a pontig, ahol az utols?? birka van.

Amennyiben az input ny??j null pointer vagy a hossza nulla, akkor null pointert (nullptr) kell visszaadni ??s a nyajhossz param??tert 0-ra kell ??ll??tani.
Olyan eset nem lehets??ges, hogy a param??terben kapott ny??j lyukkal, azaz ??res sztringgel/sztringekkel v??gz??dik.

M??g egy esetet le kell kezelni. A border collie-k nem tudnak tetsz??leges m??ret?? ny??jat terelni, de az??rt megpr??b??lj??k a legt??bbet tenni, ami t??l??k telik. 
Abban az esetben, ha a terelo_kapacitas ??rt??k??ket meghalad?? birk??n haladtak m??r kereszt??l, le??llnak a terel??ssel ??s a ny??j v??g??t ??gy hagyj??k, ahogy volt. 
(P??ld??k a feladat.pdf-ben) 
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
