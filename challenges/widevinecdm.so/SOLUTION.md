# How to hack libwidevinecdm.so

*by Javantea*  
*Aug 4, 2019*

Well this is fun. We get to finally crack all these encrypted HTML videos we've been watching on Netflix, VRV, Amazon, and HBO.

This code has no copyright, I wonder who wrote it.

https://shaka-player-demo.appspot.com/docs/api/tutorial-drm-config.html

https://shaka-player-demo.appspot.com/docs/api/tutorial-license-server-auth.html

Okay, so it was copied directly from the demo. That seems promising.

https://google.github.io/shaka-packager/html/tutorials/widevine.html

Okay, so there are keys in this tutorial. Did they copy the tutorial?

```
packager \
  in=h264_baseline_360p_600.mp4,stream=audio,output=audio.mp4 \
  in=h264_baseline_360p_600.mp4,stream=video,output=h264_360p.mp4 \
  in=h264_main_480p_1000.mp4,stream=video,output=h264_480p.mp4 \
  in=h264_main_720p_3000.mp4,stream=video,output=h264_720p.mp4 \
  in=h264_high_1080p_6000.mp4,stream=video,output=h264_1080p.mp4 \
  --enable_widevine_encryption \
  --key_server_url https://license.uat.widevine.com/cenc/getcontentkey/widevine_test \
  --content_id 7465737420636f6e74656e74206964 \
  --signer widevine_test \
  --aes_signing_key 1ae8ccd0e7985cc0b6203a55855a1034afc252980e970ca90e5202689f947ab9 \
  --aes_signing_iv d58ce954203b7c9a9a9d467f59839249 \
  --mpd_output h264.mpd \
  --hls_master_playlist_output h264_master.m3u8


```

I didn't see h264_master.m3u8 in the Network request tab of Firefox, is that on the server?

```
curl -i -k https://localhost:4443/sp/h264_master.m3u8
HTTP/1.0 404 File not found
```

Okay, wait, they are using the suffix 2.

```
curl -i -k https://localhost:4443/sp/h264_master2.m3u8
HTTP/1.0 200 OK
Server: Neg9CTFHTTP/0.1 Python/3.6.8
Date: Mon, 05 Aug 2019 03:30:49 GMT
Content-type: application/x-mpegURL
Content-Length: 211
Last-Modified: Mon, 05 Aug 2019 02:41:44 GMT

#EXTM3U
## Generated with https://github.com/google/shaka-packager version 3c26dfbd53-release

#EXT-X-STREAM-INF:BANDWIDTH=1823548,AVERAGE-BANDWIDTH=313674,CODECS="avc1.42c01e",RESOLUTION=1280x720
stream_0.m3u8

```

Okay, now we might have the key. Let's try to decrypt.

I can't find a decrypter that works. Let's try the key. It works. The flag is: 1ae8ccd0e7985cc0b6203a55855a1034afc252980e970ca90e5202689f947ab9

Now we just need the IV. J/K =]
