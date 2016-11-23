
typedef struct strdata{
char c;
short s;
int i;
char *data;
} _strdata;

typedef int (*data_callback)(const struct strdata d, int timeout);

int getint(int i);
short getshort(short j);
int getmessage(const char *msg, char *out);

int register_callback(data_callback ptr);