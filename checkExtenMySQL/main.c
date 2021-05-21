#include <stdio.h>
#include <stdlib.h>
#include <mysql.h>

#define DB_HOST "localhost"
#define DB_USER "asteriskuser"
#define DB_PASS "asteriskpass"
#define DB_NAME "asteriskdb"
#define DB_TABLE "ps_contacts"

char *idcolumn = "id", *addrcolumn = "via_addr";

void finish_with_error(MYSQL *con) {
    fprintf(stderr, "%s\n", mysql_error(con));
    printf("Check connection. Exiting\n");
    mysql_close(con);
    exit(1);
}

int main (int argc, char *argv[]) {
    if(argc <= 1) return 1;
    MYSQL *con = mysql_init(NULL);
    if(con == NULL) {
	fprintf(stderr, "mysql_init() failed\n");
	exit(1);
    }
    if(mysql_real_connect(con, DB_HOST, DB_USER, DB_PASS, DB_NAME, 0, NULL, 0) == NULL) finish_with_error(con);
    char queryAors[1024];
    sprintf(queryAors, "SELECT %s FROM " DB_TABLE " WHERE id LIKE '%%%s%%'", addrcolumn, argv[1]);
    if(mysql_query(con, queryAors)) finish_with_error(con);
    MYSQL_RES *result = mysql_store_result(con);
    if(result == NULL) finish_with_error(con);

    int rows = mysql_num_rows(result); // 1 - exists, 0 - not exists
    if(rows) printf("SET VARIABLE checkNumVar \"PJSIP/%s\"\n", argv[1]);
    else printf("SET VARIABLE checkNumVar \"OOH323/old-ats-h323/%s\"\n", argv[1]);
    mysql_free_result(result);
    mysql_close(con);
}
