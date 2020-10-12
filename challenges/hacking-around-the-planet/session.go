package main

import (
	"errors"
	"log"
	"time"

	jwt "github.com/dgrijalva/jwt-go"
)

const SessionTimeout = (time.Minute * 7) + (time.Second * 10)

const CookieName = "passport"

func NewToken() *jwt.Token {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, &HackerClaims{
		ExpiresAt: time.Now().UTC().Add(SessionTimeout).Unix(),
		Passport:  []string{},
	})
	return token
}

func ParseToken(tokenString string) (*jwt.Token, error) {
	token, err := jwt.ParseWithClaims(tokenString, &HackerClaims{}, func(token *jwt.Token) (interface{}, error) {
		return Key, nil
	})
	if err != nil {
		log.Print(err)
		return nil, errors.New("Invalid Token")
	}
	err = token.Claims.Valid()
	if err != nil {
		return nil, err
	}
	return token, nil
}

type HackerClaims struct {
	ExpiresAt int64    `json:"exp"`
	Passport  []string `json:"passport"`
}

func (claims HackerClaims) Valid() error {
	now := time.Now().UTC().Unix()
	if claims.ExpiresAt < now {
		return errors.New("Expired")
	}
	return nil
}
