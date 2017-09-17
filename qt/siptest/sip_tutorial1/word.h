// Define the interface to the word library.

class Word {
    char *the_word;

public:
    Word(const char *w);
    ~Word();

    char *reverse() const;
};