package main

import (
	"errors"
	"fmt"
	"net/http"
	"time"

	jwt "github.com/dgrijalva/jwt-go"
)

var Key = []byte("This\x66is\x60a\x01very\x99secret\xffkey\x00\x13\x27\xde\xad\xbe\xef")

const Around_The_World = "https://www.youtube.com/watch?v=yca6UsllwYs"

func AccessDenied(w http.ResponseWriter, err error) {
	w.WriteHeader(403)
	w.Write([]byte(err.Error()))
}

func Error(w http.ResponseWriter, err error) {
	w.WriteHeader(500)
	w.Header().Add("Content-Type", "text/sadness")
	w.Write([]byte(err.Error()))
}

func AppendIfMissing(slice []string, s string) []string {
	for _, ele := range slice {
		if ele == s {
			return slice
		}
	}
	return append(slice, s)
}

func SetCookie(w http.ResponseWriter, token *jwt.Token) error {
	signed_val, err := token.SignedString(Key)
	if err != nil {
		return err
	}
	if claims, ok := token.Claims.(*HackerClaims); ok {
		expires := time.Unix(claims.ExpiresAt, 0).UTC()
		cookie := &http.Cookie{
			Name:    CookieName,
			Value:   signed_val,
			Expires: expires,
		}
		http.SetCookie(w, cookie)
	} else {
		return errors.New("Invalid Token, I fucked up")
	}
	return nil
}

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case "GET", "HEAD":
			cookie, err := r.Cookie(CookieName)
			if err == http.ErrNoCookie {
				w.Header().Add("Content-Type", "text/memes")
				token := NewToken()
				err = SetCookie(w, token)
				if err != nil {
					Error(w, err)
					return
				}
				http.Redirect(w, r, Around_The_World, http.StatusSeeOther)
				return
			}

			token, err := ParseToken(cookie.Value)
			if err != nil {
				AccessDenied(w, err)
				return
			}
			if claims, ok := token.Claims.(*HackerClaims); ok {
				w.Header().Add("Content-Type", "text/plain")
				var ip string
				if ips, ok := r.Header["X-Forwarded-For"]; ok {
					ip = ips[0]
				} else {
					ip = r.RemoteAddr
				}
				location, err := LookupIpLocation(ip)
				if err != nil {
					Error(w, err)
					return
				}
				claims.Passport = AppendIfMissing(claims.Passport, location)
				err = SetCookie(w, token)
				if err != nil {
					Error(w, err)
					return
				}
				if len(claims.Passport) > 10 {
					w.Write([]byte("flag{wh4t_4_t4ng313d_w3b_w3_w34v3}"))
				} else {
					w.Write([]byte(fmt.Sprintf("You have %d/10 stamps on your passport.\n", len(claims.Passport))))
					for i, stamp := range claims.Passport {
						w.Write([]byte(fmt.Sprintf("%d. %s\n", i, stamp)))
					}
				}
			} else {
				Error(w, errors.New("No is Hacker..."))
				return
			}
		default:
			w.WriteHeader(501)
			w.Write([]byte("wtf"))
		}
	})
	http.ListenAndServe("0.0.0.0:5000", nil)
}
