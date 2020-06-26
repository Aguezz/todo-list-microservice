package main

import (
	"log"

	"github.com/fasthttp/router"
	"github.com/valyala/fasthttp"
)

func main() {
	r := router.New()

	r.GET("/", func(ctx *fasthttp.RequestCtx) {
		ctx.WriteString("Hello World")
	})

	log.Fatal(fasthttp.ListenAndServe(":8010", r.Handler))
}
