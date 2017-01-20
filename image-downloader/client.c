#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

int main(int argc, char *argv[])
{
    int sockfd, portno, n;
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in serv_addr; 

    memset(&serv_addr, '0', sizeof(serv_addr)); 
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(80); 
    
    inet_pton(AF_INET, "213.186.33.40", &serv_addr.sin_addr);

    connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));

    char buffer[103] = "GET /ifipnetworking2017/diynetworking_2017_supporters.png HTTP/1.1\r\nHost: diynetworking.net\r\n\r\n";

    write(sockfd,buffer,strlen(buffer));

    char rbuffer[2048];

    int i;
    int img_start = -1;
    int n_last_read = 0;

    FILE *img = fopen("download.png", "wb");

    while (img_start < 0)
    {
        n_last_read = read(sockfd,rbuffer,2048);
        printf("Read %d\n", n_last_read);
        for (i=0; i<n_last_read; i++)
        {
            if (rbuffer[i] == '\r' &&
                    rbuffer[i+1] == '\n' &&
                    rbuffer[i+2] == '\r' &&
                    rbuffer[i+3] == '\n')
            {
                img_start = i+4;
                printf("PNG starts in %d\n", img_start);
                break;
            }
        }
    }

    fwrite(&rbuffer[img_start], 1, n_last_read-img_start, img);

    char *end;
    int falta;
    falta = 32670-n_last_read+img_start;
    end = malloc(falta);

    while (falta != 0)
    {
        n_last_read = read(sockfd,end,falta);
        printf("Read %d\n", n_last_read);
        fwrite(end, 1, n_last_read, img);
        falta = falta - n_last_read;
    }

    fflush(img);
    fclose(img);
}
