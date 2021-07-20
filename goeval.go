package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"os/exec"
	"strings"
)

var ver = "1"

func main() {
	goexec, err := exec.LookPath("go")
	if err != nil {
		fail(err.Error())
	}

	imports := []string{}
	code := []string{}
	ctx := ""
	reader := bufio.NewReader(os.Stdin)

	fmt.Println("GoEval v" + ver)

	for {
		fmt.Print(">> ")
		ctx, err = reader.ReadString('\n')
		if err == io.EOF {
			break
		}
		if err != nil {
			fail(err.Error())
		}
		ctx = strings.TrimSpace(ctx)

		if strings.HasPrefix(ctx, "//+import ") && len(ctx) > 10 {
			imp := strings.TrimSpace(ctx[10:])
			if imp != "" {
				imports = append(imports, imp)
				fmt.Println("Added import:", imp)
			}
		} else if ctx == "" {
			path := os.Getenv("TEMP") + string(os.PathSeparator) + "goeval"

			// get info on the directory the code is going to be executed in
			_, err := os.Stat(path)
			// if it doesn't exist, simply make it
			if os.IsNotExist(err) {
				err = os.Mkdir(path, os.ModePerm)
				// if it exists, delete it all and then make it over again
			} else {
				err = os.RemoveAll(path)
				if err != nil {
					fail(err.Error())
				}
				err = os.Mkdir(path, os.ModePerm)
			}
			if err != nil {
				fail(err.Error())
			}

			// prepare the imports to be added to the file
			fileImports := []string{}
			for _, im := range imports {
				// in case you'd want to use sth like _ "embed"
				// without the outer if you'd get "_ "embed" or "_ embed"
				// instead
				// TODO: parse imports to automatically add quotes
				if !strings.HasPrefix(im, "_") && !strings.HasPrefix(im, ".") {
					if !strings.HasPrefix(im, `"`) {
						im = `"` + im
					}
					if !strings.HasSuffix(im, `"`) {
						im += `"`
					}
				}
				fileImports = append(fileImports, im)
			}

			// dump code
			f, err := os.Create(path + string(os.PathSeparator) + "main.go")
			if err != nil {
				fail(err.Error())
			}

			fmt.Fprint(f, "package main\n\n")
			if len(fileImports) > 0 {
				fmt.Fprint(f, "import(\n")
				for _, fim := range fileImports {
					fmt.Fprintf(f, "\t%s\n", fim)
				}
				fmt.Fprint(f, ")\n\n")
			}
			fmt.Fprint(f, "func main() {\n")
			for _, fcl := range code {
				fmt.Fprintf(f, "\t%s\n", fcl)
			}
			fmt.Fprint(f, "}")

			fmt.Println("creating module...")
			mod := exec.Cmd{
				Path:   goexec,
				Args:   []string{"go", "mod", "init", "goeval"},
				Dir:    path,
				Stdout: os.Stderr,
				Stderr: os.Stderr,
			}
			err = mod.Run()
			if err != nil {
				fail(err.Error())
			}

			// go through the imports to find ones that are not in the standard
			// library, so they can be fetched
			// TODO: find a better way to do this (look at the stdlib var)
			extImports := []string{}
			for _, im := range imports {
				if strings.HasPrefix(im, "_") || strings.HasPrefix(im, ".") {
					im = strings.TrimSpace(im[1:])
				}
				if strings.HasPrefix(im, `"`) {
					im = im[1:]
				}
				if strings.HasPrefix(im, `"`) {
					im = im[:len(im)-1]
				}
				for _, stdim := range stdlib {
					if strings.HasPrefix(im, stdim) {
						continue
					}
				}
				extImports = append(extImports, im)
			}

			if len(extImports) > 0 {
				fmt.Println("getting external packages...")
			}
			for _, pkg := range extImports {
				get := exec.Cmd{
					Path:   goexec,
					Args:   []string{"go", "get", pkg},
					Dir:    path,
					Stdout: os.Stderr,
					Stderr: os.Stderr,
				}
				err = get.Run()
				if err != nil {
					fail(err.Error())
				}
			}

			fmt.Println("running code...")
			fmt.Println("==================================================")
			run := exec.Cmd{
				Path:   goexec,
				Args:   []string{"go", "run", "main.go"},
				Dir:    path,
				Stdout: os.Stdout,
				Stderr: os.Stderr,
			}
			err = run.Run()
			if err != nil {
				fail(err.Error())
			}
			break
		} else {
			code = append(code, ctx)
		}
	}
}

func fail(msg string) {
	fmt.Println("ERROR:", msg)
	os.Exit(-1)
}

// stdlib contains the names of packages included in the go standard library.
// it is used to check for external packages in imports.
var stdlib = []string{
	"archive",
	"bufio",
	"builtin",
	"bytes",
	"compress",
	"container",
	"context",
	"crypto",
	"database",
	"debug",
	"embed",
	"emcoding",
	"errors",
	"expvar",
	"flag",
	"fmt",
	"go",
	"hash",
	"html",
	"image",
	"index",
	"io",
	"log",
	"math",
	"mime",
	"net",
	"os",
	"path",
	"plugin",
	"reflect",
	"regexp",
	"runtime",
	"sort",
	"strconv",
	"strings",
	"sync",
	"syscal",
	"testing",
	"text",
	"time",
	"unicode",
	"unsafe",
	"internal",
}
