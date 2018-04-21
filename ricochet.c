#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_DEPTH 32

#define NORTH 0x01
#define EAST  0x02
#define SOUTH 0x04
#define WEST  0x08
#define ROBOT 0x10

#define HAS_WALL(x, wall) (x & wall)
#define HAS_ROBOT(x) (x & ROBOT)
#define SET_ROBOT(x) (x |= ROBOT)
#define UNSET_ROBOT(x) (x &= ~ROBOT)

#define PACK_MOVE(robot, direction) (robot << 4 | direction)
#define UNPACK_ROBOT_FROM_MOVE(move) (move >> 4 & 0xFF)
#define UNPACK_DIRECTION_FROM_MOVE(move) (move & 0xF)
#define PACK_UNDO(robot, start, last, did_sort) (did_sort << 24 | robot << 16 | start << 8 | last)
#define UNPACK_ROBOT(undo) ((undo >> 16) & 0x0f)
#define UNPACK_START(undo) ((undo >> 8) & 0xff)
#define UNPACK_DID_SORT(undo) ((undo >> 24) & 0x0f)
#define UNPACK_LAST(undo) (undo & 0xff)
#define MAKE_KEY(x) (x[0] | (x[1] << 8) | (x[2] << 16) | (x[3] << 24))
#define MAKE_KEY_EIGHT(x) (x[0] | (x[1] << 8) | (x[2] << 16) | (x[3] << 24) | (x[4] << 32) | (x[5] << 40) | (x[6] << 48) | (x[7] << 56))

#define bool unsigned int
#define true 1
#define false 0


//contains oposite direction at array position of direction
// REVERSE[NORTH]=SOUTH
const unsigned int REVERSE[] = {
    0, SOUTH, WEST, 0, NORTH, 0, 0, 0, EAST
};
//index offset for stepping one square in direction
// should be dependent on size of row (board)

const int OFFSET[] = {
    0, -16, 1, 0, 16, 0, 0, 0, -1
};

const char* COLOR_NAMES[] = {
  "Red","Green","Blue","Yellow","Magenta"
};

const char* DIRECTION_NAMES[] = {
  "N/A","NORTH","EAST","N/A","SOUTH","N/A","N/A","N/A","WEST"
};

typedef struct {
    unsigned int grid[256];
    unsigned int moves[256];//grid of minimum moves
    unsigned int robots[8];
    unsigned int sorted_robots[8];
    unsigned int robot_index[8];
    unsigned int reverse_index[8];
    unsigned int robot_count;
    unsigned int token;
    unsigned int last;
} Game;

typedef struct {
    unsigned long long key;
    unsigned int depth;
} Entry;

typedef struct {
    unsigned int mask;
    unsigned int size;
    Entry *data;
} Set;

inline void swap(unsigned int *array, unsigned int a, unsigned int b) {
    unsigned int temp = array[a];
    array[a] = array[b];
    array[b] = temp;
}

inline unsigned long long make_key_shifts(int count, unsigned int *robots)
{
  unsigned long long key = robots[0];
  for(int i = 1; i < count; i++)
  {
    unsigned long long temp = robots[i];
    key = key | temp << (i*8);
  }
  return key;
}

void print_robots(int count, unsigned int* robots)
{
    printf("robots: {");
    for(int i = 0; i < count; i++)
    {
      printf("%i",robots[i]);
      if(i < count-1)
      {
        printf(",");
      }
    }
    printf("}\n");
}

void sort_robots(Game *game)
{
    memcpy(game->sorted_robots, game->robots, sizeof(unsigned int) * 8);
    bool unsorted = true;
    int iteration = 1;
    for(int j = 0; j < 8; j++)
    {
        game->robot_index[j] = j;
    }
    while(unsorted)
    {
        unsorted = false;
        for(int i = 1; i < game->robot_count-iteration; i++)
        {
            if (game->sorted_robots[i] > game->sorted_robots[i+1]) {
                unsorted = true;
                swap(game->sorted_robots, i, i+1);
                swap(game->robot_index, i, i+1);
            }
        }
        iteration++;
    }
}

inline unsigned int make_key(Game *game) {
    // unsigned int robots[8];
    // memcpy(robots, game->robots, sizeof(unsigned int) * 8);
    // if (robots[1] > robots[2]) {
    //     swap(robots, 1, 2);
    // }
    // if (robots[2] > robots[3]) {
    //     swap(robots, 2, 3);
    // }
    // if (robots[1] > robots[2]) {
    //     swap(robots, 1, 2);
    // }
    return make_key_shifts(game->robot_count,game->sorted_robots);
}

unsigned long long hash(unsigned int key) {
	key = (~key) + (key << 21); // key = (key << 21) - key - 1;
	key = key ^ (key >> 24);
	key = (key + (key << 3)) + (key << 8); // key * 265
	key = key ^ (key >> 14);
	key = (key + (key << 2)) + (key << 4); // key * 21
	key = key ^ (key >> 28);
	key = key + (key << 31);
	return key;
}

void set_alloc(Set *set, unsigned int count) {
    for (unsigned int i = 0; i < count; i++) {
        set->mask = 0xfff;
        set->size = 0;
        set->data = (Entry *)calloc(set->mask + 1, sizeof(Entry));
        set++;
    }
}

void set_free(Set *set, unsigned int count) {
    for (unsigned int i = 0; i < count; i++) {
        free(set->data);
        set++;
    }
}

void set_grow(Set *set);

bool set_add(Set *set, unsigned long long key, unsigned int depth) {
    unsigned long long index = hash(key) & set->mask;
    Entry *entry = set->data + index;
    while (entry->key && entry->key != key) {
        index = (index + 1) & set->mask;
        entry = set->data + index;
    }
    if (entry->key) {
        if (entry->depth < depth) {
            entry->depth = depth;
            return true;
        }
        return false;
    }
    else {
        entry->key = key;
        entry->depth = depth;
        set->size++;
        if (set->size * 2 > set->mask) {
            set_grow(set);
        }
        return true;
    }
}

void set_grow(Set *set) {
    Set new_set;
    new_set.mask = (set->mask << 2) | 3;
    new_set.size = 0;
    new_set.data = (Entry *)calloc(new_set.mask + 1, sizeof(Entry));
    for (unsigned int index = 0; index <= set->mask; index++) {
        Entry *entry = set->data + index;
        if (entry->key) {
            set_add(&new_set, entry->key, entry->depth);
        }
    }
    free(set->data);
    set->mask = new_set.mask;
    set->size = new_set.size;
    set->data = new_set.data;
}

inline bool game_over(Game *game) {
    if (game->robots[0] == game->token) {
        // printf("Game Over: %i -> Token: %i", game->robots[0], game->token);
        return true;
    }
    else {
        return false;
    }
}

bool can_move(
    Game *game,
    unsigned int robot,
    unsigned int direction)
{
    unsigned int index = game->robots[robot];
    if (HAS_WALL(game->grid[index], direction)) {
        return false;
    }
    if (game->last == PACK_MOVE(robot, REVERSE[direction])) {
        return false;
    }
    unsigned int new_index = index + OFFSET[direction];
    if (HAS_ROBOT(game->grid[new_index])) {
        return false;
    }
    return true;
}

unsigned int compute_move(
    Game *game,
    unsigned int robot,
    unsigned int direction)
{
    unsigned int index = game->robots[robot] + OFFSET[direction];
    while (true) {
        if (HAS_WALL(game->grid[index], direction)) {
            break;
        }
        unsigned int new_index = index + OFFSET[direction];
        if (HAS_ROBOT(game->grid[new_index])) {
            break;
        }
        index = new_index;
    }
    return index;
}

inline void swap_robots(Game *game, unsigned int a, unsigned int b )
{
    // printf("swapping %i <-> %i\n",a, b);
    swap(game->sorted_robots, a, b);
    swap(game->robot_index, game->reverse_index[a], game->reverse_index[b]);
    for(int i = 1; i < game->robot_count; i++ )
    {
        game->reverse_index[game->robot_index[i]] = i;
    }
}

unsigned int do_move(
    Game *game,
    unsigned int robot,
    unsigned int direction)
{
    unsigned int start = game->robots[robot];
    unsigned int end = compute_move(game, robot, direction);
    unsigned int last = game->last;
    game->robots[robot] = end;

    unsigned int robot_index = game->robot_index[robot];
    game->sorted_robots[robot_index] = end;

    game->last = PACK_MOVE(robot, direction);
    UNSET_ROBOT(game->grid[start]);
    SET_ROBOT(game->grid[end]);
    // printf("Move: %i %i -> %i\n",robot, start, end);
    unsigned int did_sort = 0;
    // printf("PreSort:\n");
    // print_robots(game->robot_count,game->sorted_robots);
    // printf("index:\n");
    // print_robots(game->robot_count,game->robot_index);
    // if(robot_index > 8)
    // {
    //     printf("faulty robot index in do");
    // }
    if(robot != 0)
    {
        if(end > start)
        {
            while(robot_index < game->robot_count - 1)
            {
                if(game->sorted_robots[robot_index] > game->sorted_robots[robot_index+1])
                {
                    did_sort++;
                    swap_robots(game, robot_index, robot_index+1);
                    robot_index++;
                }
                else
                {
                    break;
                }
            }
        }

        if(end < start)
        {
            while(robot_index > 1)
            {
                if(game->sorted_robots[robot_index] < game->sorted_robots[robot_index-1])
                {
                    did_sort++;
                    swap_robots(game, robot_index, robot_index-1);
                    robot_index--;
                }
                else
                {
                    break;
                }
            }
        }
    }
    // if(did_sort > 0)
    // {
    //     printf("PostSort:\n");
    //     print_robots(game->robot_count,game->sorted_robots);
    //     printf("index:\n");
    //     print_robots(game->robot_count,game->robot_index);
    // }
    // if(robot > 8)
    // {
    //     printf("MOVE: Faulty Robot: %i\n",robot);
    // }
    return PACK_UNDO(robot, start, last, did_sort);
}

void undo_move(
    Game *game,
    unsigned int undo)
{
    unsigned int robot = UNPACK_ROBOT(undo);
    // if(robot > 8)
    // {
    //     printf("Faulty robot in Undo: %i\n", robot);
    // }
    unsigned int start = UNPACK_START(undo);
    unsigned int last = UNPACK_LAST(undo);
    unsigned int end = game->robots[robot];
    game->robots[robot] = start;
    game->last = last;
    SET_ROBOT(game->grid[start]);
    UNSET_ROBOT(game->grid[end]);
    
    unsigned int robot_index = game->robot_index[robot];
    game->sorted_robots[robot_index] = start;
    
    unsigned int did_sort = UNPACK_DID_SORT(undo);
    // if(robot_index > 8)
    // {
    //     printf("Faulty robot index in Undo: %i\n",);
    // }
    if(did_sort > 0 && robot != 0)
    {
        if(start > end)
        {
            while(robot_index < game->robot_count - 1)
            {
                if(game->sorted_robots[robot_index] > game->sorted_robots[robot_index+1])
                {
                    swap_robots(game, robot_index, robot_index+1);
                    robot_index++;
                }
                else
                {
                    break;
                }
            }
        }

        if(start < end)
        {
            while(robot_index > 1)
            {
                if(game->sorted_robots[robot_index] < game->sorted_robots[robot_index-1])
                {
                    swap_robots(game, robot_index, robot_index-1);
                    robot_index--;
                }
                else
                {
                    break;
                }
            }
        }
    }
}

void precompute_minimum_moves(
    Game *game)
{
    bool status[256];
    for (unsigned int i = 0; i < 256; i++) {
        game->moves[i] = 0xffffffff;
        status[i] = false;
    }
    game->moves[game->token] = 0;
    status[game->token] = true;
    bool done = false;
    while (!done) {
        done = true;
        for (unsigned int i = 0; i < 256; i++) {
            if (!status[i]) {
                continue;
            }
            status[i] = false;
            unsigned int depth = game->moves[i] + 1;
            for (unsigned int direction = 1; direction <= 8; direction <<= 1) {
                unsigned int index = i;
                while (!HAS_WALL(game->grid[index], direction)) {
                    index += OFFSET[direction];
                    if (game->moves[index] > depth) {
                        game->moves[index] = depth;
                        status[index] = true;
                        done = false;
                    }
                }
            }
        }
    }
}

unsigned int _nodes;
unsigned int _hits;
unsigned int _inner;

unsigned int _search(
    Game *game,
    unsigned int depth,
    unsigned int max_depth,
    unsigned char *path,
    Set *set)
{
    _nodes++;
    //if solution is found return depth
    if (game_over(game)) {
        return depth;
    }

    //if max depth is reached return 0
    if (depth == max_depth) {
        return 0;
    }

    //height is the room left for search
    // if the minimum number or moves for the robot to reach goal is higher then height return 0
    unsigned int height = max_depth - depth;
    if (game->moves[game->robots[0]] > height) {
        return 0;
    }

    if (height != 1 && !set_add(set, make_key(game), height)) {
        _hits++;
        return 0;
    }
    _inner++;
    for (unsigned int robot = 0; robot < game->robot_count; robot++) {
        if (robot && game->moves[game->robots[0]] == height) {
            continue;
        }
        for (unsigned int direction = 1; direction <= 8; direction <<= 1) {
            if (!can_move(game, robot, direction)) {
                continue;
            }
            unsigned int undo = do_move(game, robot, direction);
            unsigned int result = _search(
                game, depth + 1, max_depth, path, set
            );
            undo_move(game, undo);
            if (result) {
                path[depth] = PACK_MOVE(robot, direction);
                return result;
            }
        }
    }
    return 0;
}

void print_game_grid(unsigned int *grid)
{
  for(int row = 0; row < 16; row++)
  {
    for(int column = 0; column < 16; column++)
    {
      printf("%i,",grid[(row*16)+column]);
    }
    printf("\n");
  }
}



void print_game_robots(Game *game)
{
    print_robots(game->robot_count, game->robots);
}

unsigned int search(
    Game *game,
    unsigned char *path,
    void (*callback)(unsigned int, unsigned int, unsigned int, unsigned int))
{
    print_game_grid(game->grid);
    print_game_robots(game);
    sort_robots(game);
    print_robots(game->robot_count,game->sorted_robots);
    // printf("token: %i\n", game->token);
    if (game_over(game)) {
        return 0;
    }
    unsigned int result = 0;
    Set set;
    set_alloc(&set, 1);
    precompute_minimum_moves(game);
    for (unsigned int max_depth = 1; max_depth < MAX_DEPTH; max_depth++) {
        _nodes = 0;
        _hits = 0;
        _inner = 0;
        result = _search(game, 0, max_depth, path, &set);
        if (callback) {
            callback(max_depth, _nodes, _inner, _hits);
        }
        if (result) {
            break;
        }
    }
    set_free(&set, 1);
    return result;
}

void _callback(
    unsigned int depth,
    unsigned int nodes,
    unsigned int inner,
    unsigned int hits)
{
    printf("%u %u %u %u\n", depth, nodes, inner, hits);
}

int main(int argc, char *argv[]) {
    // Game game = {
    //     {9, 1, 5, 1, 3, 9, 1, 1, 1, 3, 9, 1, 1, 1, 1, 3, 8, 2, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 8, 6, 8, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1, 0, 3, 8, 0, 0, 0, 0, 2, 12, 0, 2, 9, 0, 0, 0, 0, 4, 2, 12, 0, 0, 0, 4, 0, 1, 0, 0, 0, 0, 0, 0, 0, 3, 10, 9, 0, 0, 0, 3, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 8, 6, 8, 0, 0, 0, 0, 4, 4, 0, 0, 2, 12, 0, 0, 2, 8, 1, 0, 0, 0, 0, 2, 9, 3, 8, 0, 0, 1, 0, 0, 2, 8, 0, 4, 0, 2, 12, 2, 12, 6, 8, 0, 0, 0, 0, 0, 6, 8, 18, 9, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 4, 0, 3, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 9, 0, 2, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 8, 0, 0, 0, 2, 9, 0, 0, 0, 4, 0, 0, 0, 0, 0, 1, 0, 0, 2, 12, 2, 8, 0, 0, 16, 3, 8, 0, 0, 0, 4, 0, 0, 0, 0, 1, 2, 8, 6, 8, 0, 0, 0, 0, 0, 0, 3, 8, 0, 0, 0, 16, 2, 12, 5, 4, 4, 4, 6, 12, 4, 4, 4, 4, 6, 12, 4, 4, 6},
    //     {0},
    //     {176, 145, 211, 238},
    //     54,
    //     0
    // };
    Game game = {
        {9,1,1,1,3,9,1,1,1,3,9,1,1,1,5,3,8,0,22,8,0,0,0,0,0,0,0,0,0,2,9,2,8,0,1,0,0,0,0,0,0,0,2,28,0,0,0,2,26,12,0,0,0,0,4,0,0,0,0,1,0,0,0,6,12,1,0,0,0,2,9,0,0,0,0,0,0,0,0,3,9,0,0,0,0,4,0,0,0,0,0,0,0,0,0,2,8,0,0,0,0,3,8,4,4,0,4,0,0,6,8,2,8,0,0,6,8,0,2,9,3,8,3,8,0,1,0,2,8,0,0,5,0,0,2,12,6,8,0,0,0,0,4,2,8,0,0,3,8,0,0,1,1,0,0,0,0,2,9,2,8,0,0,0,0,0,0,0,0,0,2,12,0,0,0,6,10,12,0,0,0,0,0,0,0,4,0,1,0,0,0,3,8,1,0,0,0,0,6,8,0,3,8,0,0,0,0,2,12,0,4,0,0,0,1,0,0,0,0,0,0,0,0,2,9,2,25,0,0,0,0,0,0,0,0,0,0,6,8,2,12,4,4,4,4,6,12,4,4,4,6,12,4,5,4,6},
        {0},
        {43, 48, 226, 18, 254},
        {0},
        {0},
        {0},
        5,
        201,
        0
    };

    unsigned char path[32];
    int solutionLength = search(&game, path, _callback);
    printf("solution:\n");
    for(int i = 0; i < solutionLength && i < 32; i++)
    {
      unsigned int robot = UNPACK_ROBOT_FROM_MOVE(path[i]);
      unsigned int direction = UNPACK_DIRECTION_FROM_MOVE(path[i]);
    	printf("%i: r:%s\td:%s\n", i, COLOR_NAMES[robot], DIRECTION_NAMES[direction]);
    }
}
