8.6	Example - Listing Directories
A different kind of file system interaction is sometimes called for - determining information about a file, not what it contains. A directory-listing program such as the UNIX command ls is an example - it prints the names of files in a directory, and, optionally, other information, such as sizes, permissions, and so on. The MS-DOS dir command is analogous.
Since a UNIX directory is just a file, ls need only read it to retrieve the filenames. But is is necessary to use a system call to access other information about a file, such as its size. On other systems, a system call may be needed even to access filenames; this is the case on MS-DOS for instance. What we want is provide access to the information in a relatively system-independent way, even though the implementation may be highly system-dependent.
We will illustrate some of this by writing a program called fsize. fsize is a special form of ls that prints the sizes of all files named in its commandline argument list. If one of the files is a directory, fsize applies itself recursively to that directory. If there are no arguments at all, it processes the current directory.
Let us begin with a short review of UNIX file system structure. A directory is a file that contains a list of filenames and some indication of where they are located. The ``location'' is an index into another table called the ``inode list.'' The inode for a file is where all information about the file except its name is kept. A directory entry generally consists of only two items, the filename and an inode number.
Regrettably, the format and precise contents of a directory are not the same on all versions of the system. So we will divide the task into two pieces to try to isolate the non-portable parts. The outer level defines a structure called a Dirent and three routines opendir, readdir, and closedir to provide system-independent access to the name and inode number in a directory entry. We will write fsize with this interface. Then we will show how to implement these on
  systems that use the same directory structure as Version 7 and System V UNIX; variants are left as exercises.
The Dirent structure contains the inode number and the name. The maximum length of a filename component is NAME_MAX, which is a system-dependent value. opendir returns a pointer to a structure called DIR, analogous to FILE, which is used by readdir and closedir. This information is collected into a file called dirent.h.
	
#define NAME_MAX	14 /* longest filename component; */
/* system-dependent */ typedef struct {	/* portable directory entry */ long ino;		/* inode number */ char name[NAME_MAX+1];	/* name + '\0' terminator */
} Dirent; typedef struct {	/* minimal DIR: no buffering, etc. */ int fd;	/* file descriptor for the directory */
Dirent d;	/* the directory entry */
} DIR;
DIR *opendir(char *dirname); Dirent *readdir(DIR *dfd); void closedir(DIR *dfd);
The system call stat takes a filename and returns all of the information in the inode for that file, or -1 if there is an error. That is, char *name; struct stat stbuf; int stat(char *, struct stat *); stat(name, &stbuf); fills the structure stbuf with the inode information for the file name. The structure describing the value returned by stat is in <sys/stat.h>, and typically looks like this: struct stat	/* inode information returned by stat */
{ dev_t	st_dev;	/* device of inode */ ino_t	st_ino;	/* inode number */ short	st_mode;	/* mode bits */ short	st_nlink;	/* number of links to file */ short	st_uid;	/* owners user id */ short	st_gid;	/* owners group id */ dev_t	st_rdev;	/* for special files */ off_t	st_size;	/* file size in characters */ time_t	 st_atime;	 /* time last accessed */ time_t	 st_mtime;	 /* time last modified */ time_t	 st_ctime;	 /* time originally created */
};
Most of these values are explained by the comment fields. The types like dev_t and ino_t are defined in <sys/types.h>, which must be included too.
The st_mode entry contains a set of flags describing the file. The flag definitions are also included in <sys/types.h>; we need only the part that deals with file type:

#define S_IFMT	 0160000 /* type of file: */ #define S_IFDIR	0040000 /* directory */
#define S_IFCHR	0020000 /* character special */ #define S_IFBLK	0060000 /* block special */ #define S_IFREG	0010000 /* regular */
/* ... */
 
Now we are ready to write the program fsize. If the mode obtained from stat indicates that a file is not a directory, then the size is at hand and can be printed directly. If the name is a directory, however, then we have to process that directory one file at a time; it may in turn contain sub-directories, so the process is recursive.
The main routine deals with command-line arguments; it hands each argument to the function fsize.

#include <stdio.h> #include <string.h> #include "syscalls.h"
#include <fcntl.h>	/* flags for read and write */ #include <sys/types.h> /* typedefs */
#include <sys/stat.h>	/* structure returned by stat */ #include "dirent.h" void fsize(char *)
/* print file name */ main(int argc, char **argv)
{ if (argc == 1) /* default: current directory */ fsize("."); else while (--argc > 0) fsize(*++argv); return 0;
}
The function fsize prints the size of the file. If the file is a directory, however, fsize first calls dirwalk to handle all the files in it. Note how the flag names S_IFMT and S_IFDIR are used to decide if the file is a directory. Parenthesization matters, because the precedence of & is lower than that of ==. int stat(char *, struct stat *); void dirwalk(char *, void (*fcn)(char *));
/* fsize: print the name of file "name" */ void fsize(char *name)
{ struct stat stbuf; if (stat(name, &stbuf) == -1) { fprintf(stderr, "fsize: can't access %s\n", name); return;
} if ((stbuf.st_mode & S_IFMT) == S_IFDIR) dirwalk(name, fsize); printf("%8ld %s\n", stbuf.st_size, name);
}
The function dirwalk is a general routine that applies a function to each file in a directory. It opens the directory, loops through the files in it, calling the function on each, then closes the directory and returns. Since fsize calls dirwalk on each directory, the two functions call each other recursively.
#define MAX_PATH 1024
/* dirwalk: apply fcn to all files in dir */ void dirwalk(char *dir, void (*fcn)(char *))
{ char name[MAX_PATH]; Dirent *dp;
DIR *dfd;
  if ((dfd = opendir(dir)) == NULL) { fprintf(stderr, "dirwalk: can't open %s\n", dir); return;
} while ((dp = readdir(dfd)) != NULL) { if (strcmp(dp->name, ".") == 0
|| strcmp(dp->name, "..")) continue;	/* skip self and parent */ if (strlen(dir)+strlen(dp->name)+2 > sizeof(name)) fprintf(stderr, "dirwalk: name %s %s too long\n", dir, dp->name); else { sprintf(name, "%s/%s", dir, dp->name); (*fcn)(name);
}
} closedir(dfd);
}
Each call to readdir returns a pointer to information for the next file, or NULL when there are no files left. Each directory always contains entries for itself, called ".", and its parent, ".."; these must be skipped, or the program will loop forever.
Down to this last level, the code is independent of how directories are formatted. The next step is to present minimal versions of opendir, readdir, and closedir for a specific system. The following routines are for Version 7 and System V UNIX systems; they use the directory information in the header <sys/dir.h>, which looks like this:

#ifndef DIRSIZ #define DIRSIZ 14 #endif struct direct {	/* directory entry */ ino_t d_ino;		/* inode number */ char d_name[DIRSIZ]; /* long name does not have '\0' */
};
Some versions of the system permit much longer names and have a more complicated directory structure.
The type ino_t is a typedef that describes the index into the inode list. It happens to be unsigned short on the systems we use regularly, but this is not the sort of information to embed in a program; it might be different on a different system, so the typedef is better. A complete set of ``system'' types is found in <sys/types.h>. opendir opens the directory, verifies that the file is a directory (this time by the system call fstat, which is like stat except that it applies to a file descriptor), allocates a directory structure, and records the information:
 int fstat(int fd, struct stat *);
/* opendir: open a directory for readdir calls */ DIR *opendir(char *dirname)
{ int fd; struct stat stbuf; DIR *dp; if ((fd = open(dirname, O_RDONLY, 0)) == -1
|| fstat(fd, &stbuf) == -1
|| (stbuf.st_mode & S_IFMT) != S_IFDIR
|| (dp = (DIR *) malloc(sizeof(DIR))) == NULL) return NULL; dp->fd = fd; return dp;
}
  closedir closes the directory file and frees the space:
/* closedir: close directory opened by opendir */ void closedir(DIR *dp)
{ if (dp) { close(dp->fd); free(dp);
}
}
Finally, readdir uses read to read each directory entry. If a directory slot is not currently in use (because a file has been removed), the inode number is zero, and this position is skipped. Otherwise, the inode number and name are placed in a static structure and a pointer to that is returned to the user. Each call overwrites the information from the previous one.
#include <sys/dir.h>	/* local directory structure */
/* readdir: read directory entries in sequence */ Dirent *readdir(DIR *dp)
{ struct direct dirbuf; /* local directory structure */ static Dirent d;	/* return: portable structure */ while (read(dp->fd, (char *) &dirbuf, sizeof(dirbuf))
== sizeof(dirbuf)) { if (dirbuf.d_ino == 0) /* slot not in use */ continue; d.ino = dirbuf.d_ino; strncpy(d.name, dirbuf.d_name, DIRSIZ); d.name[DIRSIZ] = '\0'; /* ensure termination */ return &d;
} return NULL;
}
Although the fsize program is rather specialized, it does illustrate a couple of important ideas. First, many programs are not ``system programs''; they merely use information that is maintained by the operating system. For such programs, it is crucial that the representation of the information appear only in standard headers, and that programs include those headers instead of embedding the declarations in themselves. The second observation is that with care it is possible to create an interface to system-dependent objects that is itself relatively system-independent. The functions of the standard library are good examples.
Exercise 8-5. Modify the fsize program to print the other information contained in the inode entry.