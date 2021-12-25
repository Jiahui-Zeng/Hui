#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <curses.h>
#include <termios.h>
#include <fcntl.h>

#define ROW 10 
#define COLUMN 50 

int status = 0; 
//game status: 0 go on, 1 for win, 2 for lose, 3 for quit

struct Node{
	int x , y; 
	Node( int _x , int _y ) : x( _x ) , y( _y ) {}; 
	Node(){} ; 
} frog ; 

int logs_pos[ROW];
int isQuit = 0;

char map[ROW+1][COLUMN] ; 

// Determine a keyboard is hit or not. If yes, return 1. If not, return 0. 
int kbhit(void){
	struct termios oldt, newt;
	int ch;
	int oldf;

	tcgetattr(STDIN_FILENO, &oldt);

	newt = oldt;
	newt.c_lflag &= ~(ICANON | ECHO);

	tcsetattr(STDIN_FILENO, TCSANOW, &newt);
	oldf = fcntl(STDIN_FILENO, F_GETFL, 0);

	fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

	ch = getchar();

	tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
	fcntl(STDIN_FILENO, F_SETFL, oldf);

	if(ch != EOF)
	{
		ungetc(ch, stdin);
		return 1;
	}
	return 0;
}


void *logs_move( void *t ){
		
	while (!status) {

		/*  Move the logs  */
		for (int i = 1; i < ROW; i++) {

			if (i % 2 == 1) { // left
					
				map[i][(logs_pos[i] + 14) % (COLUMN - 1)] = ' ';
				logs_pos[i] = (logs_pos[i] - 1 + COLUMN - 1) % (COLUMN - 1);
				map[i][logs_pos[i]] = '=';

				if (frog.x == i) { // frog moves with the log
					map[i][frog.y] = '=';			
					frog.y -= 1;
					map[i][frog.y] = '0';
				}
			}

			else { // right

				map[i][(logs_pos[i] - 14 + COLUMN - 1) % (COLUMN - 1)] = ' ';
				logs_pos[i] = (logs_pos[i] + 1) % (COLUMN - 1);
				map[i][logs_pos[i]] = '=';

				if (frog.x == i) {
					map[i][frog.y] = '=';				
					frog.y += 1;
					map[i][frog.y] = '0';
				}
			}
		}

		// sleep(1);
		usleep(500000);

		/*  Check keyboard hits, to change frog's position or quit the game. */
		if (kbhit()) {

			// clear the frog's last position
			if (frog.x == ROW)
				map[frog.x][frog.y] = '|';

			else
				map[frog.x][frog.y] = '=';

			char dir = getchar();

			if (dir == 'w' || dir == 'W')  // up
				frog.x -= 1;

			if (dir == 's' || dir == 'S') // down
				frog.x += 1;

			if (dir == 'a' || dir == 'A') // left
				frog.y -= 1;

			if (dir == 'd' || dir == 'D') // right
				frog.y += 1;

			if (dir == 'q' || dir == 'Q') // exit
				isQuit = 1;
						
			if (map[frog.x][frog.y] == ' ') { // jump into the river
				status = 2;
				pthread_exit(NULL);
			}
			
			// show the frog's current position
			map[frog.x][frog.y] = '0';

		}


		/*  Check game's status  */
		if (frog.x == 0) { // win
			status = 1;
			pthread_exit(NULL);
		}

		if (frog.y == 0 || frog.y == (COLUMN - 1)) { // lose
			status = 2;
			pthread_exit(NULL);
		}

		if (isQuit) { // quit
			status = 3;
			pthread_exit(NULL);
		}


		/*  Print the map on the screen  */
		printf("\033[H\033[2J");
		for(int i = 0; i <= ROW; i++)	
			puts( map[i] );
		
	}
	pthread_exit(NULL);
}


int main( int argc, char *argv[] ){

	// Initialize the river map and frog's starting position
	memset( map , 0, sizeof( map ) ) ;
	int i , j ; 
	for( i = 1; i < ROW; ++i ){	
		for( j = 0; j < COLUMN - 1; ++j )	
			map[i][j] = ' ' ;  
	}	

	for( j = 0; j < COLUMN - 1; ++j )	
		map[ROW][j] = map[0][j] = '|' ;

	for( j = 0; j < COLUMN - 1; ++j )	
		map[0][j] = map[0][j] = '|' ;

	frog = Node( ROW, (COLUMN-1) / 2 ) ; 
	map[frog.x][frog.y] = '0' ; 

	//Print the map into screen
	for( i = 0; i <= ROW; ++i)	
		puts( map[i] );

	// initialize the logs
	srand(time(0));
	for (i = 1; i < ROW; i++) {

		logs_pos[i] = rand() % (COLUMN - 1);

		if (i % 2 == 1) // left
			for (j = 0; j < 15; j++)
				map[i][(logs_pos[i] + j) % (COLUMN - 1)] = '=';
		
		else // right
			for (j = 0; j < 15; j++)
				map[i][(logs_pos[i] - j + COLUMN - 1) % (COLUMN - 1)] = '=';
	}
		
	
	/*  Create pthreads for wood move and frog control.  */
	pthread_t logs, frog;

	pthread_create(&logs, NULL, logs_move, NULL);
	pthread_create(&frog, NULL, logs_move, NULL);

	pthread_join(logs, NULL);
	pthread_join(frog, NULL);


	/*  Display the output for user: win, lose or quit.  */
	
	printf("\033[H\033[2J");

	if (status == 1)
		printf ("Congratulations! You win the game!\n");

	if (status == 2)
		printf ("Sorry. You lose the game.\n");
	
	if (status == 3)
		printf ("Strangly. You exit the game.\n");
	
	pthread_exit(NULL);
	
	return 0;

}
