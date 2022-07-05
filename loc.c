#include <stdio.h>
#include <stdlib.h>

// lines represents the line content of a file
struct lines {
  // blank is the amount of blank lines (0 chars between newlines)
  int blank;
  // comment is the amount of lines containing only line comments (only coutned
  // for file extensions where applicable)
  int comment;
  // content is the amount of lines containing any text
  int content; 
};

typedef struct lines lines_t;

int count_lines(FILE* f, lines_t* out) {
  // ln_count stores the amount of non-whitespace characters in the since the
  // last newline
  int ln_count = 0;
  
  // loop throught every byte of the file
  while(1) {
    int c = fgetc(f);

    // if we encounter a newline or the end of the file
    if(c == '\n' || c == EOF) {
      // count blank line or content line
      if(ln_count == 0)
        out->blank++;
      else 
        out->content++;
      // break out of loop if we reached the end
      if(c == EOF) break;
      // reset the line character count for the next line
      ln_count = 0;
    } else {
      // if we didn't encounter nl or eof, and this character is not whitespace,
      // add it to the line character count
      if(c != ' ' && c != '\t' && c != '\r' && c != '\v' && c != '\f')
        ln_count++;
    }
  }
  return 0;
}

int main(int argc, char** argv) {
  // ensure there is at least 1 file provided to count
  if(argc == 1) {
    fprintf(stderr, "Usage: %s <file 1> <file 2> ... <file n>\n\n", argv[0]);
    return 1;
  }

  // print the header of the output CSV
  printf("File,Blank,Comment,Content\n");

  FILE* f;
  // setup - prepare line counters both per-file and total,
  //         use calloc to ensure they are 0-initialized
  lines_t* ln = calloc(1, sizeof(lines_t));
  lines_t* total = calloc(1, sizeof(lines_t));

  // iterate files passed in via argv
  for(int i = 1; argv[i] != 0; i++) {
    // try to open the file
    if(fopen_s(&f, argv[i], "r")) {
      fprintf(stderr, "Could not open file %s.\n", argv[i]);
      // do not leak
      free(ln);
      free(total);

      exit(1);
    }

    // clear previous file's results
    ln->blank = 0;
    ln->comment = 0;
    ln->content = 0;

    // do the counting
    count_lines(f, ln);

    // add the file's results to the total
    total->blank += ln->blank;
    total->comment += ln->comment;
    total->content += ln->content;

    // print the results to the output
    printf("%s,%d,%d,%d\n", argv[i], ln->blank, ln->comment, ln->content);

    // finally, close the file
    fclose(f);
  }

  // print the totals
  printf("*,%d,%d,%d\n", total->blank, total->comment, total->content);

  // finally free the memory we were using
  free(ln);
  free(total);
}
