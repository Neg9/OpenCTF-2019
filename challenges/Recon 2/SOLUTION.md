1. The prime minister of Canada in the summer of 1926 was Arthur Meighen.
2. An island in the Arctic Ocean is named after him.
3. The only amenity OpenStreetMap lists on this island is a fake coffee shop named after the district the island is in.
    1. You can find it with any OSM tool.  Overpass works well if you run a search for shop:coffee by placing the island in the viewport and running this query:
```
<osm-script output="json" timeout="25">
  <!-- gather results -->
  <union>
    <!-- query part for: “amenity=restaurant and cuisine=vietnamese” -->
    <query type="node">
      <has-kv k="shop" v="coffee"/>
      <bbox-query {{bbox}}/>
    </query>
  </union>
  <!-- print results -->
  <print mode="body"/>
  <recurse type="down"/>
  <print mode="skeleton" order="quadtile"/>
</osm-script>
```
    2. You can also just look in the edit history around there; not much exists
4. No hours are listed, just a phone number.  You have to call +883 (5100) 0990 3277.
    1. +883 is an inum.  Call it on something that supports it (not much)
    2.  Get a SIP softphone up and call the inum, like +883510009903277@sip.inum.net.  You could use a softphone (on windows, microsip, but configure a stun server like stun1.l.google.com:19302)
5. It will tell you the number is not in service twice, then read the decimal ASCII values for flag{ (words twice), and then the flag, zb4fj+ptk#lcz
