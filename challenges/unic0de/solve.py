"""
echo -n $'\xc9\x91\xef' | nc -u localhost 2044
'utf-16-le' codec can't decode byte 0xef in position 2: truncated data+2DXcH//o2ADcXAJR/0c +2DXdztg13V/YNd8E2DXdvNg13CjYNd1V2DXcUg +BU/YNdyw2DXcaqTXBAU-

python3
"""

a = b'+2DXcH//o2ADcXAJR/0c +2DXdztg13V/YNd8E2DXdvNg13CjYNd1V2DXcUg +BU/YNdyw2DXcaqTXBAU-'.decode('utf-7')
a
'𝐟￨𐁜ɑｇ 𝗎𝕟𝜄𝖼𝐨𝕕𝑒 Տ𝒰𝑪ꓗЅ'
