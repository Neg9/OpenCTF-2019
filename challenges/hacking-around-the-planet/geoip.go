package main

import (
	"errors"
	"log"
	"net"
	"strings"

	maxminddb "github.com/oschwald/maxminddb-golang"
)

const GeoIP_DB_FileName = "GeoLite2-City.mmdb"

func LookupIpLocation(ip_string string) (string, error) {
	db, err := maxminddb.Open(GeoIP_DB_FileName)
	if err != nil {
		log.Println(err)
		return "", err
	}
	defer db.Close()

	ip_parts := strings.Split(ip_string, ":")
	reconstructed_ip := strings.Join(ip_parts[:len(ip_parts)-1], ":")
	ip := net.ParseIP(reconstructed_ip)
	if ip == nil {
		// ipv6 addrs don't work well with ParseIP
		return "", errors.New("Try ipv4")
	}

	var record struct {
		Country struct {
			ISOCode string `maxminddb:"iso_code"`
		} `maxminddb:"country"`

		City struct {
			Names map[string]string `maxminddb:"names"`
		} `maxminddb:"city"`
	}

	err = db.Lookup(ip, &record)
	if err != nil {
		log.Println(err)
		return "", err
	}
	if record.Country.ISOCode == "" || record.City.Names["en"] == "" {
		return "", errors.New("I don't know where you are")
	}
	return record.Country.ISOCode + " - " + record.City.Names["en"], nil
}
