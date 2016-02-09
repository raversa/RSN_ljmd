from ctypes import *

filename = "test_data.inp"
mode = "w+"

# Create the file for the input parameters used to test

in_file = open(filename, mode)
in_file.write("150	#Try an integer\n")
in_file.write("15.3	#Try an float\n")
in_file.write("try.xyz	#Try an string\n")
in_file.close()

# To fill the file to the C routine, change the mode

mode = "r"

# Create string buffer to store the results from the called C routine

strbuff1 = create_string_buffer(200)
strbuff2 = create_string_buffer(200)
strbuff3 = create_string_buffer(200)

# In C we need a file pointer, which is a novel type:
# call the standard C routine that opens a file
# and returns the file pointer (in libc)

libc = CDLL("libc.so.6")
fopen = libc.fopen
fopen.argtypes = [c_char_p, c_char_p] # 1: file name, 2: mode

fclose = libc.fclose
fclose.argtypes = [c_void_p] # void pointer

# Setup ctypes also for the ljmd routine

ljmd = CDLL("../lib/library.so")
get_a_line = ljmd.get_a_line
get_a_line.argtypes = [c_void_p, c_char_p] # 1: file pointer, 2: result input parameter

# open the input file from C and get the file stream pointer

fpointer = fopen(filename, mode)

# call the ljmd routine and store the result in the strbuff1

print "Try integer"
status = get_a_line(fpointer, strbuff1) # status should be 0 if no error
print "Status = ", status
#print "Result = ", repr(strbuff1.value), "Expected =", "'150'"
if (repr(strbuff1.value) == "'150'"):
	print "Match strbuff1 passed!"
else: 
	print "Match strbuff1 failed!"

# call the ljmd routine and store the result in the strbuff1

print "Try float"
status = get_a_line(fpointer, strbuff2) # status should be 0 if no error
print "Status = ", status
#print "Result = ", repr(strbuff2.value), "Expected =", "'15.3'"
if (repr(strbuff2.value) == "'15.3'"):
	print "Match strbuff2 passed!"
else: 
	print "Match strbuff2 failed!"

# call the ljmd routine and store the result in the strbuff1

print "Try string"
status = get_a_line(fpointer, strbuff3) # status should be 0 if no error
print "Status = ", status
#print "Result = ", repr(strbuff3.value), "Expected =", "'try.xyz'"
if (repr(strbuff3.value) == "'try.xyz'"):
	print "Match strbuff3 passed!"
else: 
	print "Match strbuff3 failed!"

# Call the C function to close the file

status =fclose(fpointer)
print "Status of fclose = ", status # status should be 0 if no error
print "UNIT TESTS COMPLETED!"



