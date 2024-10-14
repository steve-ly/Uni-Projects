########################################################################
# COMP1521 21T2 -- Assignment 1 -- Snake!
# <https://www.cse.unsw.edu.au/~cs1521/21T2/assignments/ass1/index.html>
#
#
# !!! IMPORTANT !!!
# Before starting work on the assignment, make sure you set your tab-width to 8!
# For instructions, see: https://www.cse.unsw.edu.au/~cs1521/21T2/resources/mips-editors.html
# !!! IMPORTANT !!!
#
#
# This program was written by YOUR-NAME-HERE (z5555555)
# on INSERT-DATE-HERE
#
# Version 1.0 (2021-06-24): Team COMP1521 <cs1521@cse.unsw.edu.au>
#

	# Requires:
	# - [no external symbols]
	#
	# Provides:
	# - Global variables:
	.globl	symbols
	.globl	grid
	.globl	snake_body_row
	.globl	snake_body_col
	.globl	snake_body_len
	.globl	snake_growth
	.globl	snake_tail

	# - Utility global variables:
	.globl	last_direction
	.globl	rand_seed
	.globl  input_direction__buf

	# - Functions for you to implement
	.globl	main
	.globl	init_snake
	.globl	update_apple
	.globl	move_snake_in_grid
	.globl	move_snake_in_array

	# - Utility functions provided for you
	.globl	set_snake
	.globl  set_snake_grid
	.globl	set_snake_array
	.globl  print_grid
	.globl	input_direction
	.globl	get_d_row
	.globl	get_d_col
	.globl	seed_rng
	.globl	rand_value


########################################################################
# Constant definitions.

N_COLS          = 15
N_ROWS          = 15
MAX_SNAKE_LEN   = N_COLS * N_ROWS

EMPTY           = 0
SNAKE_HEAD      = 1
SNAKE_BODY      = 2
APPLE           = 3

NORTH       = 0
EAST        = 1
SOUTH       = 2
WEST        = 3


########################################################################
# .DATA
	.data

# const char symbols[4] = {'.', '#', 'o', '@'};
symbols:
	.byte	'.', '#', 'o', '@'

	.align 2
# int8_t grid[N_ROWS][N_COLS] = { EMPTY };
grid:
	.space	N_ROWS * N_COLS

	.align 2
# int8_t snake_body_row[MAX_SNAKE_LEN] = { EMPTY };
snake_body_row:
	.space	MAX_SNAKE_LEN

	.align 2
# int8_t snake_body_col[MAX_SNAKE_LEN] = { EMPTY };
snake_body_col:
	.space	MAX_SNAKE_LEN

# int snake_body_len = 0;
snake_body_len:
	.word	0

# int snake_growth = 0;
snake_growth:
	.word	0

# int snake_tail = 0;
snake_tail:
	.word	0

# Game over prompt, for your convenience...
main__game_over:
	.asciiz	"Game over! Your score was "


########################################################################
#
# Your journey begins here, intrepid adventurer!
#
# Implement the following 6 functions, and check these boxes as you
# finish implementing each function
#
#  - [ ] main
#  - [ ] init_snake
#  - [ ] update_apple
#  - [ ] update_snake
#  - [ ] move_snake_in_grid
#  - [ ] move_snake_in_array
#



########################################################################
# .TEXT <main>
	.text
main:

	# Args:     void
	# Returns:
	#   - $v0: int
	#
	# Frame:    $ra, [...]
	# Uses:	    $a0, $v0, $t1, $t2
	# Clobbers: $a0, $v0, $t1, $t2
	#
	# Locals:
	#   - [...]
	#
	# Structure:
	#   main
	#   -> [prologue]
	#   -> body
	#   -> [epilogue]

	# Code:
main__prologue:
	# set up stack frame
	addiu	$sp, $sp, -4
	sw	$ra, ($sp)

main__body:
	# TODO ... complete this function.
	jal	 init_snake        #call init_snake function and update_apple function
	jal	 update_apple

	loop:
		jal  print_grid
		jal  input_direction #prints grid and sets v0 register to be input direction
		move $a0, $v0
		jal  update_snake # takes $a0 and updates our snake
		beq  $v0, 1, loop 
	
	lw  $t1, snake_body_len
	la  $t2, main__game_over
	move $a0, $t2
	li $v0, 4 # prints game over 
	syscall
	div  $a0, $t1, 3  #calculate score
	li $v0, 1         # prints score  
	syscall
	li $a0, '\n'      # prints new line
	li $v0, 11
	syscall	



main__epilogue:
	# tear down stack frame
	lw	$ra, ($sp)
	addiu 	$sp, $sp, 4

	li	$v0, 0
	jr	$ra			# return 0;



########################################################################
# .TEXT <init_snake>
	.text
init_snake:

	# Args:     void
	# Returns:  void
	#
	# Frame:    $ra, $s0, $s1, $s2
	# Uses:     $a0, $a1, $a2, $s0, $s1, $s2
	# Clobbers: [...]
	#
	# Locals:
	#   - [...]
	#
	# Structure:
	#   init_snake
	#   -> [prologue]
	#   -> body
	#   -> [epilogue]

	# Code:
init_snake__prologue:
	# set up stack frame
	addiu	$sp, $sp, -12
	sw	$ra, 8($sp)
	sw	$s0, 4($sp)
	sw	$s1,  ($sp)

init_snake__body:
	# TODO ... complete this function.
	move  $s0, $a0  #save registers
	move  $s1, $a1
	move  $s2, $a2
	
	li  $a0, 7

	li  $a1, 7
	li  $a2, SNAKE_HEAD
	jal  set_snake
	
	
	li  $a1, 6
	li  $a2, SNAKE_BODY
	jal  set_snake

	li  $a1, 5
	li  $a2, SNAKE_BODY
	jal  set_snake

	li  $a1, 4
	li  $a2, SNAKE_BODY
	jal  set_snake

	move  $a0, $s0  #reset registers
	move  $a1, $s1
	move  $a2, $s2

init_snake__epilogue:
	# tear down stack frame
	lw	$s1,  ($sp)
	lw	$s0, 4($sp)
	lw	$ra, 8($sp)
	addiu 	$sp, $sp, 12

	jr	$ra			# return;




########################################################################
# .TEXT <update_apple>
	.text
update_apple:

	# Args:     void
	# Returns:  void
	#
	# Frame:    $ra, $s0, $s1, $s3
	# Uses:     $a0, $a1, $a2, $s0, $s1, $s3, $t0, $t1, $t2, $t3
	# Clobbers: $t0, $t1, $t2, $t3
	#
	# Locals:
	#   - [...]
	#
	# Structure:
	#   update_apple
	#   -> [prologue]
	#   -> body
	#   -> [epilogue]

	# Code:
update_apple__prologue:
	# set up stack frame
	addiu	$sp, $sp, -16
	sw	$ra, 12($sp)
	sw	$s0, 8($sp)
	sw	$s1, 4($sp)
	sw  $s2, ($sp) 

update_apple__body:
	# TODO ... complete this function.
	move  $s0, $a0	 #save registers
	move  $s1, $a1
	move  $s2, $a2


loop_1:
	li  $a0, N_ROWS
	jal  rand_value  #rand_value(N_ROWS)
	move  $t2, $v0	#Temp register to hold return value
	li  $a0, N_COLS	#$a0 register now holds N_COLS
	jal  rand_value	#rand_value(N_COLS)
	move  $t3, $v0	#Temp register to hold return value
	
	move  $a0, $t2	 #save t registers
	move  $a1, $t3

	li   $t0, N_COLS 
	mul  $t0, $t0, $a0 #15 * row
	add  $t0, $t0, $a1 #(15*row) + col

	li  $t3, EMPTY 
	lb  $a2, grid($t0)
	beq $a2, $t3, end_0 # if (grid[apple_row][apple_col] == EMPTY) move to end;
	j loop_1

end_0:

	li  $a2, APPLE
	jal set_snake_grid
	move  $a0, $s0	 #load back registers
	move  $a1, $s1
	move  $a2, $s2
	j update_apple__epilogue #tear down stack and end loop


update_apple__epilogue:
	# tear down stack frame
	lw  $s2,  ($sp)
	lw	$s1, 4($sp)
	lw	$s0, 8($sp)
	lw	$ra, 12($sp)
	addiu 	$sp, $sp, 16

	jr	$ra			# return;



########################################################################
# .TEXT <update_snake>
	.text
update_snake:

	# Args:
	#   - $a0: int direction
	# Returns:
	#   - $v0: bool
	#
	# Frame:    $ra, $s0, $s1, $s2
	# Uses:     $a0, $a1, $a2, $a3, $s0, $s1, $s2, $t0, $t1, $t2, $t3, $t4, $t5, $v0
	# Clobbers: $t0, $t1, $t2, $t3, $t4, $t5, $v0, $a3
	#
	# Locals:
	#   - `int direction` in $s0
	#
	# Structure:
	#   update_snake
	#   -> [prologue]
	#   -> body
	#   -> [epilogue]

	# Code:
update_snake__prologue:
	# set up stack frame
	addiu	$sp, $sp, -16
	sw	$ra, 12($sp)
	sw	$s0, 8($sp)
	sw	$s1, 4($sp)
	sw  $s2, ($sp) 


update_snake__body:
	# TODO ... complete this function.
	move  $s0, $a0  #s0 = direction
	move  $s1, $a1  #save a1 and a2 values
	move  $s2, $a2
	
	jal  get_d_row	
	move  $t1, $v0	# temp register  1 = get_d_row(direction)
	jal  get_d_col	# temp register 2= get_d_col(direction)
	move  $t2, $v0
	
	lb  $a0, snake_body_row($zero) #a0 =  snake_body_row[0]; head_row
	lb  $a1, snake_body_col($zero) #a1 =  snake_body_col[0]; head_col
	
	add  $t1, $a0, $t1  # new_head_row = head_row + d_row;
	add  $t2, $a1, $t2  # new_head_col = head_col + d_col;
    
	li  $a2, SNAKE_BODY
	jal set_snake_grid  #grid[head_row][head_col] = SNAKE_BODY;


	move $a0, $t1   #sets a0 register = new_head_row
	move $a1, $t2	#sets a1 register = new_head_col
	
	li  $t3, N_ROWS
	li  $t4, N_COLS

	bltz  $a0, end1  #if a1<0 move to end1 branch
	bge  $a0, $t3, end1   # if a0 >= N_rows move to end1 branch
	bltz  $a1, end1      #if a1<0 move to end1 branch
	bge   $a1, $t4, end1   #if a1>= N_cols move to end1 branch

	li   $t5, N_ROWS #setting t5 = grid[new_head_row][new_head_col]
	mul  $t5, $t5, $a0 #15 * new_head_row
	add  $t5, $t5, $a1 #(15*new_head_row) + new_head_col

	li  $t3, APPLE
	lb  $t4, grid($t5)	
	beq $t4, $t3, bool_apple  #grid[new_head_row][new_head_col] is apple
	li $a3, 0 #if it does not jump branch than $a3 = 0

	j cont1 #continue to cont branch

cont1:
	
	lw  $t3, snake_body_len
	sub  $t3, $t3, 1  #t0= snake_body_len - 1;
	sw  $t3, snake_tail #snake_tail = snake_body_len - 1;


	jal move_snake_in_grid
	beq $v0, 0, end1   #boolean to test if move_snake_in_grid is successful
	
	jal move_snake_in_array


	move  $a0, $s0  #load saved values
	move  $a1, $s1  #
	move  $a2, $s2


	beq  $a3, $v0, increase_apple  #if apple = true than increase snake_growth by 3
	li  $v0, 1 #return true


	j update_snake__epilogue #tear down stack frame

increase_apple: 
	lw  $t2, snake_growth
	add  $t2, $t2, 3      #t2 = snake_growth + 3
	sw  $t2, snake_growth  #snake_growth = $t2
	
	jal update_apple
	
	li  $v0, 1 #return true

	move  $a0, $s0  #load saved values
	move  $a1, $s1  #
	move  $a2, $s2
	j update_snake__epilogue #tear down stack frame


bool_apple:
	li $a3, 1  #sets apple to be true
	j cont1     #continue to cont branch

end1:
	li $v0, 0  #branch to return false
	move  $a0, $s0  #load saved values
	move  $a1, $s1  #
	move  $a2, $s2
	j update_snake__epilogue #tear down stack frame

	
update_snake__epilogue:
	# tear down stack frame
	lw  $s2,  ($sp)
	lw	$s1, 4($sp)
	lw	$s0, 8($sp)
	lw	$ra, 12($sp)
	addiu 	$sp, $sp, 16

	jr	$ra			# return;


########################################################################
# .TEXT <move_snake_in_grid>
	.text
move_snake_in_grid:

	# Args:
	#   - $a0: new_head_row
	#   - $a1: new_head_col
	# Returns:
	#   - $v0: bool
	#
	# Frame:    $ra, $s0, $s1, $s2
	# Uses:     $a0, $a1, $a2, $s0, $s1, $s2, $t0, $t1, $t2, $t3, $v0
	# Clobbers: $t0, $t1, $t2, $t3, $v0
	#
	# Locals:
	#   - `int new_head_row` - $s0
	#	- `int new_head_col` - $s1
	# Structure:
	#   move_snake_in_grid
	#   -> [prologue]
	#   -> body
	#   -> [epilogue]

	# Code:
move_snake_in_grid__prologue:
	# set up stack frame
	addiu	$sp, $sp, -16
	sw	$ra, 12($sp)
	sw	$s0, 8($sp)
	sw	$s1, 4($sp)
	sw  $s2, ($sp) 



move_snake_in_grid__body:
	# TODO ... complete this function.
	move  $s0, $a0  #save registers
	move  $s1, $a1
	move  $s2, $a2

	lw  $t0, snake_growth  #$t0 = snake_growth
	bgtz  $t0, snake_growth_branch  #if snake_growth > 0 true move to snake_growth 

	lw $t0, snake_tail #else statement, t0 = snake_tail
	lb  $a0, snake_body_row($t0) #a0 =  snake_body_row[0];
	lb  $a1, snake_body_col($t0) #a1 =  snake_body_col[0];
	li  $a2, EMPTY
	jal set_snake_grid



	j cont2 #move to cont branch


snake_growth_branch:
	lw  $t0, snake_tail  #t0 = snake_tail
	addi $t0, $t0, 1     #t0 = t0 + 1
	sw  $t0, snake_tail  #snake_tail++
	lw  $t0, snake_body_len  #t0 = snake_body_len
	addi  $t0, $t0, 1	#t0 = t0 + 1
	sw  $t0, snake_body_len #snake_body_len++
	lw  $t0, snake_growth  #t0 = snake_growth
	li  $t1, 1				#t1 = 1
	sub  $t0, $t0, $t1   #t0 = t0 - 1
	sw  $t0, snake_growth #snake_growth--

	j cont2 #continue to branch cont

cont2:
	move  $a0, $s0  #load back registers
	move  $a1, $s1
	move  $a2, $s2
	
	li	$t0, N_COLS
	mul	$t0, $t0, $a0		#  15 * new_head_row
	add	$t0, $t0, $a1		# (15 * new_head_row) + new_head_col
	li  $t1, SNAKE_BODY
	lb $t3, grid($t0)
	beq  $t3, $t1, end2  #if grid[new_head_row][new_head_col] == SNAKE_BODY is true move to end

	li  $a2, SNAKE_HEAD
	jal set_snake_grid
	li  $v0, 1
	
	move  $a0, $s0  #load back registers
	move  $a1, $s1
	move  $a2, $s2
	j move_snake_in_grid__epilogue

end2:
	move  $a0, $s0  #load back registers
	move  $a1, $s1
	move  $a2, $s2
	li $v0, 0
	j  move_snake_in_grid__epilogue

move_snake_in_grid__epilogue:
	# tear down stack frame
	lw  $s2,  ($sp)
	lw	$s1, 4($sp)
	lw	$s0, 8($sp)
	lw	$ra, 12($sp)
	addiu 	$sp, $sp, 16

	jr	$ra			# return;




########################################################################
# .TEXT <move_snake_in_array>
	.text
move_snake_in_array:

	# Arguments:
	#   - $a0: int new_head_row
	#   - $a1: int new_head_col
	# Returns:  void
	#
	# Frame:    $ra, $s0, $s1, $s2
	# Uses:     $a0, $a1, $a2, $s0, $s1, $s2, $t0, $t1, $t2
	# Clobbers: [...]
	#
	# Locals:
	#   - `int new_head_row`- $s0
	#	- `int new_head_col` - $s1
	# Structure:
	#   move_snake_in_array
	#   -> [prologue]
	#   -> body
	#   -> [epilogue]

	# Code:
move_snake_in_array__prologue:
	# set up stack frame
	addiu	$sp, $sp, -16
	sw	$ra, 12($sp)
	sw	$s0, 8($sp)
	sw	$s1, 4($sp)
	sw  $s2, ($sp) 



move_snake_in_array__body:
	# TODO ... complete this function.
	move  $s0, $a0  #save registers
	move  $s1, $a1
	move  $s2, $a2
	
	lw  $t0, snake_tail   #t0 = snake_tail
	li  $t1, 1
loop2:
	blt  $t0, 1, end3 # if $t0 < 1 go to end
	sub  $t2, $t0, $t1  # t2 = i -1
	lb  $a0, snake_body_row($t2)
	lb  $a1, snake_body_col($t2)
	move  $a2, $t0  #a2 = i  
	jal  set_snake_array
	sub  $t0, $t0, $t1  #i--
	j  loop2  #continue loop
end3:
	move  $a0, $s0  #reloading registers for new_head_row and new_head_col
	move  $a1, $s1
	li  $a2, 0 #a2 = 0
	jal  set_snake_array
	move  $a2, $s2 #reseting a2 to original value
	j move_snake_in_array__epilogue


move_snake_in_array__epilogue:
	# tear down stack frame
	lw  $s2,  ($sp)
	lw	$s1, 4($sp)
	lw	$s0, 8($sp)
	lw	$ra, 12($sp)
	addiu 	$sp, $sp, 16

	jr	$ra			# return;


########################################################################
####                                                                ####
####        STOP HERE ... YOU HAVE COMPLETED THE ASSIGNMENT!        ####
####                                                                ####
########################################################################

##
## The following is various utility functions provided for you.
##
## You don't need to modify any of the following.  But you may find it
## useful to read through --- you'll be calling some of these functions
## from your code.
##

	.data

last_direction:
	.word	EAST

rand_seed:
	.word	0

input_direction__invalid_direction:
	.asciiz	"invalid direction: "

input_direction__bonk:
	.asciiz	"bonk! cannot turn around 180 degrees\n"

	.align	2
input_direction__buf:
	.space	2



########################################################################
# .TEXT <set_snake>
	.text
set_snake:

	# Args:
	#   - $a0: int row
	#   - $a1: int col
	#   - $a2: int body_piece
	# Returns:  void
	#
	# Frame:    $ra, $s0, $s1
	# Uses:     $a0, $a1, $a2, $t0, $s0, $s1
	# Clobbers: $t0
	#
	# Locals:
	#   - `int row` in $s0
	#   - `int col` in $s1
	#
	# Structure:
	#   set_snake
	#   -> [prologue]
	#   -> body
	#   -> [epilogue]

	# Code:
set_snake__prologue:
	# set up stack frame
	addiu	$sp, $sp, -12
	sw	$ra, 8($sp)
	sw	$s0, 4($sp)
	sw	$s1,  ($sp)

set_snake__body:
	move	$s0, $a0		# $s0 = row
	move	$s1, $a1		# $s1 = col

	jal	set_snake_grid		# set_snake_grid(row, col, body_piece);

	move	$a0, $s0
	move	$a1, $s1
	lw	$a2, snake_body_len
	jal	set_snake_array		# set_snake_array(row, col, snake_body_len);

	lw	$t0, snake_body_len
	addiu	$t0, $t0, 1
	sw	$t0, snake_body_len	# snake_body_len++;

set_snake__epilogue:
	# tear down stack frame
	lw	$s1,  ($sp)
	lw	$s0, 4($sp)
	lw	$ra, 8($sp)
	addiu 	$sp, $sp, 12

	jr	$ra			# return;



########################################################################
# .TEXT <set_snake_grid>
	.text
set_snake_grid:

	# Args:
	#   - $a0: int row
	#   - $a1: int col
	#   - $a2: int body_piece
	# Returns:  void
	#
	# Frame:    None
	# Uses:     $a0, $a1, $a2, $t0
	# Clobbers: $t0
	#
	# Locals:   None
	#
	# Structure:
	#   set_snake
	#   -> body

	# Code:
	li	$t0, N_COLS
	mul	$t0, $t0, $a0		#  15 * row
	add	$t0, $t0, $a1		# (15 * row) + col
	sb	$a2, grid($t0)		# grid[row][col] = body_piece;

	jr	$ra			# return;



########################################################################
# .TEXT <set_snake_array>
	.text
set_snake_array:

	# Args:
	#   - $a0: int row
	#   - $a1: int col
	#   - $a2: int nth_body_piece
	# Returns:  void
	#
	# Frame:    None
	# Uses:     $a0, $a1, $a2
	# Clobbers: None
	#
	# Locals:   None
	#
	# Structure:
	#   set_snake_array
	#   -> body

	# Code:
	sb	$a0, snake_body_row($a2)	# snake_body_row[nth_body_piece] = row;
	sb	$a1, snake_body_col($a2)	# snake_body_col[nth_body_piece] = col;

	jr	$ra				# return;



########################################################################
# .TEXT <print_grid>
	.text
print_grid:

	# Args:     void
	# Returns:  void
	#
	# Frame:    None
	# Uses:     $v0, $a0, $t0, $t1, $t2
	# Clobbers: $v0, $a0, $t0, $t1, $t2
	#
	# Locals:
	#   - `int i` in $t0
	#   - `int j` in $t1
	#   - `char symbol` in $t2
	#
	# Structure:
	#   print_grid
	#   -> for_i_cond
	#     -> for_j_cond
	#     -> for_j_end
	#   -> for_i_end

	# Code:
	li	$v0, 11			# syscall 11: print_character
	li	$a0, '\n'
	syscall				# putchar('\n');

	li	$t0, 0			# int i = 0;

print_grid__for_i_cond:
	bge	$t0, N_ROWS, print_grid__for_i_end	# while (i < N_ROWS)

	li	$t1, 0			# int j = 0;

print_grid__for_j_cond:
	bge	$t1, N_COLS, print_grid__for_j_end	# while (j < N_COLS)

	li	$t2, N_COLS
	mul	$t2, $t2, $t0		#                             15 * i
	add	$t2, $t2, $t1		#                            (15 * i) + j
	lb	$t2, grid($t2)		#                       grid[(15 * i) + j]
	lb	$t2, symbols($t2)	# char symbol = symbols[grid[(15 * i) + j]]

	li	$v0, 11			# syscall 11: print_character
	move	$a0, $t2
	syscall				# putchar(symbol);

	addiu	$t1, $t1, 1		# j++;

	j	print_grid__for_j_cond

print_grid__for_j_end:

	li	$v0, 11			# syscall 11: print_character
	li	$a0, '\n'
	syscall				# putchar('\n');

	addiu	$t0, $t0, 1		# i++;

	j	print_grid__for_i_cond

print_grid__for_i_end:
	jr	$ra			# return;



########################################################################
# .TEXT <input_direction>
	.text
input_direction:

	# Args:     void
	# Returns:
	#   - $v0: int
	#
	# Frame:    None
	# Uses:     $v0, $a0, $a1, $t0, $t1
	# Clobbers: $v0, $a0, $a1, $t0, $t1
	#
	# Locals:
	#   - `int direction` in $t0
	#
	# Structure:
	#   input_direction
	#   -> input_direction__do
	#     -> input_direction__switch
	#       -> input_direction__switch_w
	#       -> input_direction__switch_a
	#       -> input_direction__switch_s
	#       -> input_direction__switch_d
	#       -> input_direction__switch_newline
	#       -> input_direction__switch_null
	#       -> input_direction__switch_eot
	#       -> input_direction__switch_default
	#     -> input_direction__switch_post
	#     -> input_direction__bonk_branch
	#   -> input_direction__while

	# Code:
input_direction__do:
	li	$v0, 8			# syscall 8: read_string
	la	$a0, input_direction__buf
	li	$a1, 2
	syscall				# direction = getchar()

	lb	$t0, input_direction__buf

input_direction__switch:
	beq	$t0, 'w',  input_direction__switch_w	# case 'w':
	beq	$t0, 'a',  input_direction__switch_a	# case 'a':
	beq	$t0, 's',  input_direction__switch_s	# case 's':
	beq	$t0, 'd',  input_direction__switch_d	# case 'd':
	beq	$t0, '\n', input_direction__switch_newline	# case '\n':
	beq	$t0, 0,    input_direction__switch_null	# case '\0':
	beq	$t0, 4,    input_direction__switch_eot	# case '\004':
	j	input_direction__switch_default		# default:

input_direction__switch_w:
	li	$t0, NORTH			# direction = NORTH;
	j	input_direction__switch_post	# break;

input_direction__switch_a:
	li	$t0, WEST			# direction = WEST;
	j	input_direction__switch_post	# break;

input_direction__switch_s:
	li	$t0, SOUTH			# direction = SOUTH;
	j	input_direction__switch_post	# break;

input_direction__switch_d:
	li	$t0, EAST			# direction = EAST;
	j	input_direction__switch_post	# break;

input_direction__switch_newline:
	j	input_direction__do		# continue;

input_direction__switch_null:
input_direction__switch_eot:
	li	$v0, 17			# syscall 17: exit2
	li	$a0, 0
	syscall				# exit(0);

input_direction__switch_default:
	li	$v0, 4			# syscall 4: print_string
	la	$a0, input_direction__invalid_direction
	syscall				# printf("invalid direction: ");

	li	$v0, 11			# syscall 11: print_character
	move	$a0, $t0
	syscall				# printf("%c", direction);

	li	$v0, 11			# syscall 11: print_character
	li	$a0, '\n'
	syscall				# printf("\n");

	j	input_direction__do	# continue;

input_direction__switch_post:
	blt	$t0, 0, input_direction__bonk_branch	# if (0 <= direction ...
	bgt	$t0, 3, input_direction__bonk_branch	# ... && direction <= 3 ...

	lw	$t1, last_direction	#     last_direction
	sub	$t1, $t1, $t0		#     last_direction - direction
	abs	$t1, $t1		# abs(last_direction - direction)
	beq	$t1, 2, input_direction__bonk_branch	# ... && abs(last_direction - direction) != 2)

	sw	$t0, last_direction	# last_direction = direction;

	move	$v0, $t0
	jr	$ra			# return direction;

input_direction__bonk_branch:
	li	$v0, 4			# syscall 4: print_string
	la	$a0, input_direction__bonk
	syscall				# printf("bonk! cannot turn around 180 degrees\n");

input_direction__while:
	j	input_direction__do	# while (true);



########################################################################
# .TEXT <get_d_row>
	.text
get_d_row:

	# Args:
	#   - $a0: int direction
	# Returns:
	#   - $v0: int
	#
	# Frame:    None
	# Uses:     $v0, $a0
	# Clobbers: $v0
	#
	# Locals:   None
	#
	# Structure:
	#   get_d_row
	#   -> get_d_row__south:
	#   -> get_d_row__north:
	#   -> get_d_row__else:

	# Code:
	beq	$a0, SOUTH, get_d_row__south	# if (direction == SOUTH)
	beq	$a0, NORTH, get_d_row__north	# else if (direction == NORTH)
	j	get_d_row__else			# else

get_d_row__south:
	li	$v0, 1
	jr	$ra				# return 1;

get_d_row__north:
	li	$v0, -1
	jr	$ra				# return -1;

get_d_row__else:
	li	$v0, 0
	jr	$ra				# return 0;



########################################################################
# .TEXT <get_d_col>
	.text
get_d_col:

	# Args:
	#   - $a0: int direction
	# Returns:
	#   - $v0: int
	#
	# Frame:    None
	# Uses:     $v0, $a0
	# Clobbers: $v0
	#
	# Locals:   None
	#
	# Structure:
	#   get_d_col
	#   -> get_d_col__east:
	#   -> get_d_col__west:
	#   -> get_d_col__else:

	# Code:
	beq	$a0, EAST, get_d_col__east	# if (direction == EAST)
	beq	$a0, WEST, get_d_col__west	# else if (direction == WEST)
	j	get_d_col__else			# else

get_d_col__east:
	li	$v0, 1
	jr	$ra				# return 1;

get_d_col__west:
	li	$v0, -1
	jr	$ra				# return -1;

get_d_col__else:
	li	$v0, 0
	jr	$ra				# return 0;



########################################################################
# .TEXT <seed_rng>
	.text
seed_rng:

	# Args:
	#   - $a0: unsigned int seed
	# Returns:  void
	#
	# Frame:    None
	# Uses:     $a0
	# Clobbers: None
	#
	# Locals:   None
	#
	# Structure:
	#   seed_rng
	#   -> body

	# Code:
	sw	$a0, rand_seed		# rand_seed = seed;

	jr	$ra			# return;



########################################################################
# .TEXT <rand_value>
	.text
rand_value:

	# Args:
	#   - $a0: unsigned int n
	# Returns:
	#   - $v0: unsigned int
	#
	# Frame:    None
	# Uses:     $v0, $a0, $t0, $t1
	# Clobbers: $v0, $t0, $t1
	#
	# Locals:
	#   - `unsigned int rand_seed` cached in $t0
	#
	# Structure:
	#   rand_value
	#   -> body

	# Code:
	lw	$t0, rand_seed		#  rand_seed

	li	$t1, 1103515245
	mul	$t0, $t0, $t1		#  rand_seed * 1103515245

	addiu	$t0, $t0, 12345		#  rand_seed * 1103515245 + 12345

	li	$t1, 0x7FFFFFFF
	and	$t0, $t0, $t1		# (rand_seed * 1103515245 + 12345) & 0x7FFFFFFF

	sw	$t0, rand_seed		# rand_seed = (rand_seed * 1103515245 + 12345) & 0x7FFFFFFF;

	rem	$v0, $t0, $a0
	jr	$ra			# return rand_seed % n;

