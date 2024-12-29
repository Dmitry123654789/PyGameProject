<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.10" tiledversion="1.11.0" name="Water" tilewidth="16" tileheight="16" tilecount="18" columns="6">
 <image source="../Others/Water.png" width="96" height="48"/>
 <tile id="0">
  <objectgroup draworder="index" id="2">
   <object id="1" x="5" y="7" width="11" height="9"/>
  </objectgroup>
 </tile>
 <tile id="1">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="5" width="16" height="11"/>
  </objectgroup>
 </tile>
 <tile id="2">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="6" width="11" height="10"/>
  </objectgroup>
 </tile>
 <tile id="4">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="16" height="16"/>
  </objectgroup>
 </tile>
 <tile id="5">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="16" height="16"/>
  </objectgroup>
 </tile>
 <tile id="6">
  <objectgroup draworder="index" id="2">
   <object id="1" x="5" y="0" width="11" height="16"/>
  </objectgroup>
 </tile>
 <tile id="8">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="11" height="16"/>
   <object id="2" x="0" y="0" width="11" height="16"/>
  </objectgroup>
 </tile>
 <tile id="10">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="16" height="16"/>
  </objectgroup>
 </tile>
 <tile id="11">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="16" height="16"/>
  </objectgroup>
 </tile>
 <tile id="12">
  <objectgroup draworder="index" id="2">
   <object id="1" x="5" y="0" width="11" height="9"/>
  </objectgroup>
 </tile>
 <tile id="13">
  <objectgroup draworder="index" id="2">
   <object id="1" x="0" y="0" width="16" height="11"/>
  </objectgroup>
 </tile>
 <wangsets>
  <wangset name="water" type="corner" tile="-1">
   <wangcolor name="" color="#ff0000" tile="-1" probability="1"/>
   <wangtile tileid="0" wangid="0,0,0,1,0,0,0,0"/>
   <wangtile tileid="1" wangid="0,0,0,1,0,1,0,0"/>
   <wangtile tileid="2" wangid="0,0,0,0,0,1,0,0"/>
   <wangtile tileid="4" wangid="0,1,0,1,0,1,0,0"/>
   <wangtile tileid="5" wangid="0,0,0,1,0,1,0,1"/>
   <wangtile tileid="6" wangid="0,1,0,1,0,0,0,0"/>
   <wangtile tileid="7" wangid="0,1,0,1,0,1,0,1"/>
   <wangtile tileid="8" wangid="0,0,0,0,0,1,0,1"/>
   <wangtile tileid="10" wangid="0,1,0,1,0,0,0,1"/>
   <wangtile tileid="11" wangid="0,1,0,0,0,1,0,1"/>
   <wangtile tileid="12" wangid="0,1,0,0,0,0,0,0"/>
   <wangtile tileid="13" wangid="0,1,0,0,0,0,0,1"/>
   <wangtile tileid="14" wangid="0,0,0,0,0,0,0,1"/>
  </wangset>
 </wangsets>
</tileset>
