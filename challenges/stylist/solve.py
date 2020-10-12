"""
stylist solution
by Javantea
Jan 24, 2019
"""

a = """      <div id="n07" style="background: #000065;"></div>
       <div id="n29" style="background: #000074;"></div>
       <div id="n18" style="background: #000074;"></div>
       <div id="n02" style="background: #000061;"></div>
       <div id="n14" style="background: #000074;"></div>
       <div id="n06" style="background: #000068;"></div>
       <div id="n08" style="background: #00005f;"></div>
       <div id="n21" style="background: #00005f;"></div>
       <div id="n27" style="background: #000063;"></div>
       <div id="n26" style="background: #00005f;"></div>
       <div id="n05" style="background: #000074;"></div>
       <div id="n04" style="background: #00007b;"></div>
       <div id="n17" style="background: #00006f;"></div>
       <div id="n11" style="background: #000062;"></div>
       <div id="n22" style="background: #000068;"></div>
       <div id="n09" style="background: #000072;"></div>
       <div id="n15" style="background: #00005f;"></div>
       <div id="n25" style="background: #000065;"></div>
       <div id="n23" style="background: #000061;"></div>
       <div id="n30" style="background: #00007d;"></div>
       <div id="n19" style="background: #00005f;"></div>
       <div id="n24" style="background: #000072;"></div>
       <div id="n01" style="background: #00006c;"></div>
       <div id="n13" style="background: #000069;"></div>
       <div id="n03" style="background: #000067;"></div>
       <div id="n20" style="background: #000061;"></div>
       <div id="n28" style="background: #000075;"></div>
       <div id="n12" style="background: #000062;"></div>
       <div id="n00" style="background: #000066;"></div>
       <div id="n10" style="background: #000061;"></div>
       <div id="n16" style="background: #000067;"></div>
"""
b = a.split('\n')

c = [d.strip() for d in b]
[chr(int(d[38:40], 16)) for d in c if d]
['e', 't', 't', 'a', 't', 'h', '_', '_', 'c', '_', 't', '{', 'o', 'b', 'h', 'r', '_', 'e', 'a', '}', '_', 'r', 'l', 'i', 'g', 'a', 'u', 'b', 'f', 'a', 'g']
c.sort()
print(''.join([chr(int(d[38:40], 16)) for d in c if d]))
'flag{the_rabbit_got_a_hare_cut}'
