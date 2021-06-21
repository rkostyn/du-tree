package main

import (
	"fmt"
	"flag"
)

func init(){
	var help bool

	flag.BoolVar( &help, "help", true, "Pass to print help message" )

	flag.Parse()
}

func main(){
	fmt.Println("help has value", help)

	fmt.Println("Hello World")

}