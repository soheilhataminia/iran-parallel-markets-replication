' JQ STAGE 3 - CPI REAL-PRICE ROBUSTNESS - FINAL WITH CPI-ADJUSTED ADF
' EViews only. Standalone embedded-data version. No Python. No graphs.
' Adds the ADF battery required for Supplementary Table SH, Panel A.
' Outputs are saved beside this PRG file.
close @all

' Set the working directory to the folder containing this PRG file.
%stage3_path = @linepath
cd %stage3_path

wfcreate(wf=JQCPI) u 122
alpha month_jalali
series tedpix
series usd
series goldcoin
series housing
series vehicle
series cpi
series xau

'------------------------------------------------------------------------------------
' 1. EMBEDDED DATA: main asset data + CPI + monthly average world gold close (USD/oz)
'------------------------------------------------------------------------------------
smpl 1 1
month_jalali = "1395/01"
tedpix = 80193.684211
usd = 34700.142857
goldcoin = 10236730
housing = 41317486
vehicle = 12.6596438195
cpi = 27.3136561922
xau = 1233.6309

smpl 2 2
month_jalali = "1395/02"
tedpix = 77453.52381
usd = 34486.55
goldcoin = 10305952.3809520006
housing = 42135246
vehicle = 12.6801475006
cpi = 27.3386144601
xau = 1265.2734695652

smpl 3 3
month_jalali = "1395/03"
tedpix = 75435.238095
usd = 34602.714286
goldcoin = 10167271.4285710007
housing = 42445751
vehicle = 12.6600802373
cpi = 27.5231842134
xau = 1249.8304809524

smpl 4 4
month_jalali = "1395/04"
tedpix = 73895.05
usd = 34988.666667
goldcoin = 10868715.7894739993
housing = 42588469
vehicle = 12.6777552077
cpi = 27.8179921878
xau = 1327.6491347826

smpl 5 5
month_jalali = "1395/05"
tedpix = 77307.952381
usd = 35325.954545
goldcoin = 11100828.5714289993
housing = 42809232
vehicle = 12.77004824
cpi = 28.1023010496
xau = 1342.0328571429

smpl 6 6
month_jalali = "1395/06"
tedpix = 76926
usd = 35549.736842
goldcoin = 11154238.0952380002
housing = 42496061
vehicle = 12.8714978014
cpi = 28.1958359479
xau = 1324.9817434783

smpl 7 7
month_jalali = "1395/07"
tedpix = 77415.777778
usd = 35802.166667
goldcoin = 10984173.6842110008
housing = 43191738
vehicle = 12.936593947
cpi = 28.3324307231
xau = 1284.2831818182

smpl 8 8
month_jalali = "1395/08"
tedpix = 79295.238095
usd = 36329.761905
goldcoin = 11135852.3809520006
housing = 43211137
vehicle = 12.9756737307
cpi = 28.4033875015
xau = 1262.025495

smpl 9 9
month_jalali = "1395/09"
tedpix = 80285.421053
usd = 38645.631579
goldcoin = 11312625
housing = 43335507
vehicle = 13.0305705406
cpi = 28.6252080253
xau = 1169.36

smpl 10 10
month_jalali = "1395/10"
tedpix = 79284.05
usd = 39487.05
goldcoin = 11781114.2857140005
housing = 44133117
vehicle = 13.1115006539
cpi = 28.858612908
xau = 1169.5036272727

smpl 11 11
month_jalali = "1395/11"
tedpix = 77564.238095
usd = 38316.380952
goldcoin = 11892723.8095239997
housing = 44140984
vehicle = 13.1181707709
cpi = 29.0016599991
xau = 1219.320952381

smpl 12 12
month_jalali = "1395/12"
tedpix = 77123.65
usd = 37677.9
goldcoin = 11981895
housing = 44627525
vehicle = 13.1692140923
cpi = 29.3581486516
xau = 1228.8204619048

smpl 13 13
month_jalali = "1396/01"
tedpix = 77917.470588
usd = 37564.4375
goldcoin = 12099998.8235289995
housing = 43258124
vehicle = 13.1940323289
cpi = 29.7802884121
xau = 1262.1956434783

smpl 14 14
month_jalali = "1396/02"
tedpix = 79947.238095
usd = 37580.25
goldcoin = 12129170
housing = 44592486
vehicle = 13.252455557
cpi = 29.7465518361
xau = 1246.8671428571

smpl 15 15
month_jalali = "1396/03"
tedpix = 79996.380952
usd = 37393.952381
goldcoin = 12049818.0952380002
housing = 44914554
vehicle = 13.2781336003
cpi = 29.7961196451
xau = 1264.2091304348

smpl 16 16
month_jalali = "1396/04"
tedpix = 79229.736842
usd = 37811.611111
goldcoin = 12098554.7368420009
housing = 45390798
vehicle = 13.3167309173
cpi = 30.1079802351
xau = 1234.5909

smpl 17 17
month_jalali = "1396/05"
tedpix = 81550.863636
usd = 38138.652174
goldcoin = 12147165.6521739997
housing = 45862328
vehicle = 13.3559863857
cpi = 30.2244604956
xau = 1271.9913590909

smpl 18 18
month_jalali = "1396/06"
tedpix = 83615.15
usd = 38869.7
goldcoin = 12459280
housing = 46846337
vehicle = 13.4238901777
cpi = 30.2283935705
xau = 1316.8986782609

smpl 19 19
month_jalali = "1396/07"
tedpix = 85448.25
usd = 39750.4
goldcoin = 12847040
housing = 47157588
vehicle = 13.5021100771
cpi = 30.6297926334
xau = 1285.38949

smpl 20 20
month_jalali = "1396/08"
tedpix = 87647.8
usd = 40769.6
goldcoin = 13549452.3809520006
housing = 48095658
vehicle = 13.5194203572
cpi = 30.9445395249
xau = 1277.82045

smpl 21 21
month_jalali = "1396/09"
tedpix = 92396.47619
usd = 41794.315789
goldcoin = 13956165
housing = 50001074
vehicle = 13.5334134957
cpi = 31.1758020192
xau = 1268.4277136364

smpl 22 22
month_jalali = "1396/10"
tedpix = 97105.52381
usd = 43479.761905
goldcoin = 14702680.9523809999
housing = 51481867
vehicle = 13.6040616054
cpi = 31.3047430496
xau = 1313.1476095238

smpl 23 23
month_jalali = "1396/11"
tedpix = 98425.285714
usd = 46382.181818
goldcoin = 15182863.5
housing = 54067640
vehicle = 13.6937354618
cpi = 31.388668705
xau = 1338.4676047619

smpl 24 24
month_jalali = "1396/12"
tedpix = 96983.947368
usd = 47085.954545
goldcoin = 15744545.4545450006
housing = 56288507
vehicle = 13.9071852688
cpi = 31.4580262615
xau = 1322.9176095238

smpl 25 25
month_jalali = "1397/01"
tedpix = 96433.733333
usd = 51537.722222
goldcoin = 17914444.4444440007
housing = 55839522
vehicle = 14.0034894426
cpi = 31.8757852331
xau = 1338.9790863636

smpl 26 26
month_jalali = "1397/02"
tedpix = 94236.681818
usd = 61040.56
goldcoin = 19196923.0769230016
housing = 59843838
vehicle = 14.2246332927
cpi = 32.2202127901
xau = 1310.5828619048

smpl 27 27
month_jalali = "1397/03"
tedpix = 98127.333333
usd = 66817.318182
goldcoin = 22982173.9130429998
housing = 64900102
vehicle = 14.8579388881
cpi = 32.8208481959
xau = 1292.5521695652

smpl 28 28
month_jalali = "1397/04"
tedpix = 110310.714286
usd = 81677.68
goldcoin = 28998600
housing = 69874753
vehicle = 15.3436883828
cpi = 34.2735964582
xau = 1247.927147619

smpl 29 29
month_jalali = "1397/05"
tedpix = 123805.958333
usd = 103004.923077
goldcoin = 36982880.7692309991
housing = 74301929
vehicle = 18.0167409719
cpi = 36.062621863
xau = 1207.3339130435

smpl 30 30
month_jalali = "1397/06"
tedpix = 144624.2
usd = 129219.238095
goldcoin = 43391739.1304349974
housing = 81223596
vehicle = 23.0228711681
cpi = 38.006276097
xau = 1200.1218181818

smpl 31 31
month_jalali = "1397/07"
tedpix = 181837.590909
usd = 142900.72
goldcoin = 45302333.3333330005
housing = 86337581
vehicle = 22.1606951552
cpi = 40.6858421703
xau = 1205.901447619

smpl 32 32
month_jalali = "1397/08"
tedpix = 181037.2
usd = 122009.090909
goldcoin = 42082090.9090910032
housing = 91857644
vehicle = 22.4558524305
cpi = 41.7510117419
xau = 1222.8059045455

smpl 33 33
month_jalali = "1397/09"
tedpix = 164431.421053
usd = 109450.75
goldcoin = 36735857.1428570002
housing = 96314357
vehicle = 23.3566667418
cpi = 42.8289455209
xau = 1237.1309

smpl 34 34
month_jalali = "1397/10"
tedpix = 161850.954545
usd = 109244
goldcoin = 37429181.818181999
housing = 97784109
vehicle = 23.8105195876
cpi = 43.6946382991
xau = 1284.7726315789

smpl 35 35
month_jalali = "1397/11"
tedpix = 159225.45
usd = 118814.583333
goldcoin = 42301526.3157889992
housing = 100661546
vehicle = 25.4452722083
cpi = 44.6511326732
xau = 1308.6704409091

smpl 36 36
month_jalali = "1397/12"
tedpix = 166757.15
usd = 130269.565217
goldcoin = 45719631.5789470002
housing = 110092974
vehicle = 31.4529198872
cpi = 46.4057605193
xau = 1306.8219142857

smpl 37 37
month_jalali = "1398/01"
tedpix = 191126.0625
usd = 134547.894737
goldcoin = 47772062.5
housing = 114116598
vehicle = 29.7640504613
cpi = 48.2595943618
xau = 1295.912852381

smpl 38 38
month_jalali = "1398/02"
tedpix = 211700.909091
usd = 145948.076923
goldcoin = 49644318.181818001
housing = 127125592
vehicle = 34.0287658791
cpi = 48.9946674389
xau = 1281.9577272727

smpl 39 39
month_jalali = "1398/03"
tedpix = 227900.722222
usd = 134615.5
goldcoin = 46068437.5
housing = 134253535
vehicle = 33.3187685912
cpi = 49.3769160228
xau = 1323.6378347826

smpl 40 40
month_jalali = "1398/04"
tedpix = 247256.863636
usd = 127636
goldcoin = 44368318.181818001
housing = 136156500
vehicle = 32.6755079202
cpi = 50.735098184
xau = 1413.5276190476

smpl 41 41
month_jalali = "1398/05"
tedpix = 256353.5
usd = 118705.478261
goldcoin = 41670222.2222220004
housing = 131872735
vehicle = 31.6309857642
cpi = 51.063529004
xau = 1471.3717347826

smpl 42 42
month_jalali = "1398/06"
tedpix = 290020.05
usd = 114116.25
goldcoin = 40588157.8947369978
housing = 127226350
vehicle = 30.7145684047
cpi = 51.3198980067
xau = 1515.3395238095

smpl 43 43
month_jalali = "1398/07"
tedpix = 316564.380952
usd = 114352.8
goldcoin = 39855285.7142859995
housing = 128481201
vehicle = 30.454375439
cpi = 52.2143630603
xau = 1496.7722681818

smpl 44 44
month_jalali = "1398/08"
tedpix = 305587.5
usd = 115539.130435
goldcoin = 40330388.8888889998
housing = 126175831
vehicle = 32.3479521494
cpi = 53.0308583008
xau = 1482.1877090909

smpl 45 45
month_jalali = "1398/09"
tedpix = 328353.904762
usd = 128555.6
goldcoin = 44541190.4761900008
housing = 134743944
vehicle = 34.6698829141
cpi = 54.7221634856
xau = 1468.4628571429

smpl 46 46
month_jalali = "1398/10"
tedpix = 376789.285714
usd = 133814.615385
goldcoin = 47784818.181818001
housing = 138827000
vehicle = 36.1512807803
cpi = 55.1859352052
xau = 1536.6476190476

smpl 47 47
month_jalali = "1398/11"
tedpix = 442791.9
usd = 137581.25
goldcoin = 50641500
housing = 144057000
vehicle = 40.0259750719
cpi = 55.7957197279
xau = 1573.8577272727

smpl 48 48
month_jalali = "1398/12"
tedpix = 516826.789474
usd = 154107.826087
goldcoin = 59553043.4782610014
housing = 156587733
vehicle = 42.6792400663
cpi = 56.6112528678
xau = 1605.2366666667

smpl 49 49
month_jalali = "1399/01"
tedpix = 590234.470588
usd = 155946.2
goldcoin = 63773000
housing = 155457113
vehicle = 43.1680142183
cpi = 57.8283780194
xau = 1641.0380904762

smpl 50 50
month_jalali = "1399/02"
tedpix = 921318.173913
usd = 165174.444444
goldcoin = 67658518.5185189992
housing = 170066211
vehicle = 50.4998330452
cpi = 59.2951986791
xau = 1713.5212869565

smpl 51 51
month_jalali = "1399/03"
tedpix = 1084496.529412
usd = 178892.380952
goldcoin = 75080900
housing = 190718765
vehicle = 49.3208702777
cpi = 60.4775912082
xau = 1721.7308954545

smpl 52 52
month_jalali = "1399/04"
tedpix = 1657673.8695650001
usd = 217190
goldcoin = 97992115.3846150041
housing = 209860676
vehicle = 54.364595219
cpi = 64.361621458
xau = 1789.7495318182

smpl 53 53
month_jalali = "1399/05"
tedpix = 1940474.95
usd = 226971.2
goldcoin = 109076400
housing = 229405325
vehicle = 59.8211146364
cpi = 66.6026848075
xau = 1963.5552043478

smpl 54 54
month_jalali = "1399/06"
tedpix = 1643801.6666669999
usd = 250366
goldcoin = 118886875
housing = 245349207
vehicle = 69.8468981348
cpi = 68.9938472482
xau = 1944.5455

smpl 55 55
month_jalali = "1399/07"
tedpix = 1532150.6190480001
usd = 296335.043478
goldcoin = 144984565.2173910141
housing = 270033068
vehicle = 90.3385391126
cpi = 73.8530479411
xau = 1896.0915181818

smpl 56 56
month_jalali = "1399/08"
tedpix = 1278576.7777780001
usd = 273529.590909
goldcoin = 131223136.3636360019
housing = 278282330
vehicle = 86.8702668005
cpi = 77.6579152853
xau = 1890.2496954545

smpl 57 57
month_jalali = "1399/09"
tedpix = 1447596.409091
usd = 256970.04
goldcoin = 118715560
housing = 269257382
vehicle = 79.4795482951
cpi = 79.2252261136
xau = 1835.401325

smpl 58 58
month_jalali = "1399/10"
tedpix = 1335007.857143
usd = 250447.666667
goldcoin = 114550291.6666669995
housing = 277312291
vehicle = 79.0179623207
cpi = 80.6722127047
xau = 1875.5206590909

smpl 59 59
month_jalali = "1399/11"
tedpix = 1219526.1000000001
usd = 243506
goldcoin = 111238400
housing = 282997657
vehicle = 79.3974076455
cpi = 82.6896032208
xau = 1831.2310590909

smpl 60 60
month_jalali = "1399/12"
tedpix = 1215112.3999999999
usd = 248514.545455
goldcoin = 108726666.6666669995
housing = 304788799
vehicle = 80.2779758402
cpi = 84.1797756815
xau = 1739.6914428571

smpl 61 61
month_jalali = "1400/01"
tedpix = 1256697.055556
usd = 248907.952381
goldcoin = 106732857.1428570002
housing = 293227000
vehicle = 84.0227499496
cpi = 87.383536691
xau = 1737.6523409091

smpl 62 62
month_jalali = "1400/02"
tedpix = 1181387.3999999999
usd = 227003.73913
goldcoin = 99201913.0434779972
housing = 287966000
vehicle = 84.2683886351
cpi = 88.1704623415
xau = 1815.3501869565

smpl 63 63
month_jalali = "1400/03"
tedpix = 1141726.3333330001
usd = 237314.8
goldcoin = 105524400
housing = 296736000
vehicle = 86.5804927049
cpi = 89.9638224405
xau = 1869.6030952381

smpl 64 64
month_jalali = "1400/04"
tedpix = 1266209.1499999999
usd = 247717.28
goldcoin = 106105560
housing = 300447000
vehicle = 89.6072860432
cpi = 92.8807138613
xau = 1795.6648217391

smpl 65 65
month_jalali = "1400/05"
tedpix = 1406234.1875
usd = 261071.363636
goldcoin = 114163478.2608699948
housing = 309701000
vehicle = 94.7979608814
cpi = 95.6899535209
xau = 1786.2065095238

smpl 66 66
month_jalali = "1400/06"
tedpix = 1500982.391304
usd = 274651.111111
goldcoin = 119788518.5185189992
housing = 317034000
vehicle = 100.3460526393
cpi = 99.2478656613
xau = 1794.4465086957

smpl 67 67
month_jalali = "1400/07"
tedpix = 1445776.444444
usd = 276270.285714
goldcoin = 117769800
housing = 316311000
vehicle = 100.4405549266
cpi = 102.4271994117
xau = 1762.8543636364

smpl 68 68
month_jalali = "1400/08"
tedpix = 1405729.8095239999
usd = 279696
goldcoin = 121695600
housing = 320090000
vehicle = 105.204605128
cpi = 104.5351363441
xau = 1822.48848

smpl 69 69
month_jalali = "1400/09"
tedpix = 1339646.6363639999
usd = 295543.461538
goldcoin = 129362307.6923079938
housing = 325908000
vehicle = 111.0651332699
cpi = 106.3327137811
xau = 1784.8684636364

smpl 70 70
month_jalali = "1400/10"
tedpix = 1351534.7619050001
usd = 283784.608696
goldcoin = 126629200
housing = 329364000
vehicle = 114.3837636248
cpi = 109.0779965079
xau = 1813.2221136364

smpl 71 71
month_jalali = "1400/11"
tedpix = 1274276.2
usd = 270528.318182
goldcoin = 120312409.0909090042
housing = 330562000
vehicle = 115.2699491397
cpi = 111.2631560755
xau = 1833.1736190476

smpl 72 72
month_jalali = "1400/12"
tedpix = 1313482.631579
usd = 259928.695652
goldcoin = 121571782.6086959988
housing = 351200000
vehicle = 114.0130630576
cpi = 113.027443363
xau = 1943.33452

smpl 73 73
month_jalali = "1401/01"
tedpix = 1458297.210526
usd = 274992.727273
goldcoin = 128699545.4545450062
housing = 342727000
vehicle = 118.0769358048
cpi = 116.1101900842
xau = 1945.3859

smpl 74 74
month_jalali = "1401/02"
tedpix = 1549367.3888890001
usd = 284614.380952
goldcoin = 136422409.0909090042
housing = 363515000
vehicle = 126.6520733925
cpi = 119.9981636112
xau = 1865.96035

smpl 75 75
month_jalali = "1401/03"
tedpix = 1545722
usd = 314238.52381
goldcoin = 151930733.3333329856
housing = 394145000
vehicle = 128.3092644871
cpi = 132.7083309353
xau = 1846.5638818182

smpl 76 76
month_jalali = "1401/04"
tedpix = 1498058.5263159999
usd = 315837.666667
goldcoin = 150405416.6666670144
housing = 417049000
vehicle = 129.17919135
cpi = 138.4824832765
xau = 1762.0957826087

smpl 77 77
month_jalali = "1401/05"
tedpix = 1446004.8095239999
usd = 308950.333333
goldcoin = 144600000
housing = 427299000
vehicle = 129.3388485976
cpi = 141.4740769547
xau = 1765.4604238095

smpl 78 78
month_jalali = "1401/06"
tedpix = 1411496
usd = 306236.84
goldcoin = 140671538.461537987
housing = 432169000
vehicle = 127.821024326
cpi = 144.5909443142
xau = 1707.3524913043

smpl 79 79
month_jalali = "1401/07"
tedpix = 1318095.944444
usd = 326417.545455
goldcoin = 149252954.5454550087
housing = 437249000
vehicle = 129.3033720636
cpi = 148.2830016219
xau = 1664.1628095238

smpl 80 80
month_jalali = "1401/08"
tedpix = 1344733.181818
usd = 346721.56
goldcoin = 158382692.3076919913
housing = 467048000
vehicle = 133.9103660313
cpi = 151.4953642848
xau = 1699.3544238095

smpl 81 81
month_jalali = "1401/09"
tedpix = 1431938.2727270001
usd = 371325.28
goldcoin = 177687160
housing = 480737000
vehicle = 145.9583548829
cpi = 154.8255224926
xau = 1779.9240090909

smpl 82 82
month_jalali = "1401/10"
tedpix = 1620455.8947370001
usd = 410590.666667
goldcoin = 210781428.5714290142
housing = 519814000
vehicle = 177.3372328593
cpi = 160.7486743108
xau = 1858.7272272727

smpl 83 83
month_jalali = "1401/11"
tedpix = 1573749.0526320001
usd = 450395.736842
goldcoin = 249105473.6842109859
housing = 571444000
vehicle = 185.78024645
cpi = 166.2350638709
xau = 1890.772365

smpl 84 84
month_jalali = "1401/12"
tedpix = 1787448
usd = 510005.263158
goldcoin = 291396105.2631580234
housing = 652414000
vehicle = 206.2274818217
cpi = 174.078005262
xau = 1861.8131857143

smpl 85 85
month_jalali = "1402/01"
tedpix = 2162883
usd = 512881.368421
goldcoin = 318478157.8947370052
housing = 664400000
vehicle = 229.0221755678
cpi = 180.5159817073
xau = 1991.0535318182

smpl 86 86
month_jalali = "1402/02"
tedpix = 2373097.2105259998
usd = 529363.8695649999
goldcoin = 323922227.2727270126
housing = 753200000
vehicle = 222.3392457528
cpi = 185.4993720834
xau = 2003.7588238095

smpl 87 87
month_jalali = "1402/03"
tedpix = 2238705.7619050001
usd = 500240.8
goldcoin = 295176000
housing = 783000000
vehicle = 204.5001091889
cpi = 189.2614765771
xau = 1954.2077608696

smpl 88 88
month_jalali = "1402/04"
tedpix = 2120824.4285710002
usd = 494227.2
goldcoin = 282198800
housing = 765400000
vehicle = 198.2157057564
cpi = 193.0038685984
xau = 1935.2224

smpl 89 89
month_jalali = "1402/05"
tedpix = 1992791.318182
usd = 492445.2
goldcoin = 282846240
housing = 757900000
vehicle = 194.9006677347
cpi = 197.7298425844
xau = 1926.5209590909

smpl 90 90
month_jalali = "1402/06"
tedpix = 2101480.2105259998
usd = 494222.608696
goldcoin = 279816521.7391300201
housing = 753300000
vehicle = 193.1770099002
cpi = 201.7326265112
xau = 1924.1108695652

smpl 91 91
month_jalali = "1402/07"
tedpix = 2046556.3
usd = 505855.086957
goldcoin = 283542173.9130430222
housing = 760600000
vehicle = 194.009333164
cpi = 206.4621945317
xau = 1883.356745

smpl 92 92
month_jalali = "1402/08"
tedpix = 2016702.6363639999
usd = 511505.384615
goldcoin = 291476538.4615380168
housing = 757700000
vehicle = 195.3572002062
cpi = 210.9113980533
xau = 1974.83485

smpl 93 93
month_jalali = "1402/09"
tedpix = 2125611.0499999998
usd = 504429.75
goldcoin = 291991875
housing = 740900000
vehicle = 196.3155643082
cpi = 217.0056910561
xau = 2021.7136318182

smpl 94 94
month_jalali = "1402/10"
tedpix = 2176320.8571429998
usd = 515226.153846
goldcoin = 305908076.9230769873
housing = 753900000
vehicle = 207.0318666885
cpi = 222.6517623432
xau = 2044.2162285714

smpl 95 95
month_jalali = "1402/11"
tedpix = 2104630
usd = 561256.863636
goldcoin = 326835590.9090909958
housing = 784800000
vehicle = 218.7192396238
cpi = 225.7348842916
xau = 2023.3195428571

smpl 96 96
month_jalali = "1402/12"
tedpix = 2124936.5789470002
usd = 593417.2727269999
goldcoin = 357312000
housing = 814400000
vehicle = 228.8550367256
cpi = 230.2470479347
xau = 2105.0486285714

smpl 97 97
month_jalali = "1403/01"
tedpix = 2235167.1875
usd = 623795.7
goldcoin = 423586500
housing = 816300000
vehicle = 240.0561972654
cpi = 236.2937383591
xau = 2290.5304681818

smpl 98 98
month_jalali = "1403/02"
tedpix = 2234730.7272729999
usd = 614919.230769
goldcoin = 413981153.8461539745
housing = 847500000
vehicle = 242.2516039963
cpi = 242.9728971156
xau = 2339.2714761905

smpl 99 99
month_jalali = "1403/03"
tedpix = 2073244.1111109999
usd = 606078.26087
goldcoin = 402951521.7391300201
housing = 859100000
vehicle = 240.0126489481
cpi = 249.7275076188
xau = 2339.2607173913

smpl 100 100
month_jalali = "1403/04"
tedpix = 2142929.6842109999
usd = 593144.166667
goldcoin = 411628750
housing = 874600000
vehicle = 240.3814146462
cpi = 255.1721889201
xau = 2371.5360333333

smpl 101 101
month_jalali = "1403/05"
tedpix = 2053255.5
usd = 594792.3076919999
goldcoin = 420735000
housing = 885000000
vehicle = 238.6785662597
cpi = 260.2010617905
xau = 2434.6713391304

smpl 102 102
month_jalali = "1403/06"
tedpix = 2083915.0588239999
usd = 594083.333333
goldcoin = 434588095.2380949855
housing = 950000000
vehicle = 237.5315080929
cpi = 264.7311605525
xau = 2529.5573136364

smpl 103 103
month_jalali = "1403/07"
tedpix = 2100072.681818
usd = 624332.6923080001
goldcoin = 493067307.6923080087
housing = 960000000
vehicle = 240.3563495242
cpi = 271.7864958658
xau = 2657.6088

smpl 104 104
month_jalali = "1403/08"
tedpix = 2092621.8636360001
usd = 683417.3076919999
goldcoin = 518903846.1538460255
housing = 980000000
vehicle = 244.8368420031
cpi = 279.4725234089
xau = 2685.1892409091

smpl 105 105
month_jalali = "1403/09"
tedpix = 2494783.5
usd = 723904.166667
goldcoin = 527729166.6666669846
housing = 990000000
vehicle = 257.380812771
cpi = 285.1209277008
xau = 2648.4947818182

smpl 106 106
month_jalali = "1403/10"
tedpix = 2831455.6190479998
usd = 801408
goldcoin = 560426000
housing = 1010000000
vehicle = 262.4227947025
cpi = 293.3715084015
xau = 2653.5087444444

smpl 107 107
month_jalali = "1403/11"
tedpix = 2777380.7368419999
usd = 864977.083333
goldcoin = 672197916.6666669846
housing = 1030000000
vehicle = 269.1864725538
cpi = 305.5230684951
xau = 2826.42965

smpl 108 108
month_jalali = "1403/12"
tedpix = 2766307.7999999998
usd = 921897.826087
goldcoin = 785186956.521739006
housing = 1070000000
vehicle = 273.8488316351
cpi = 315.6911686339
xau = 2941.4612772727

smpl 109 109
month_jalali = "1404/01"
tedpix = 2860957.875
usd = 952690
goldcoin = 891266666.6666669846
housing = 1062000000
vehicle = 283.7537136465
cpi = 328.1147138993
xau = 3114.94106

smpl 110 110
month_jalali = "1404/02"
tedpix = 3153188.521739
usd = 827661.538462
goldcoin = 737511538.4615379572
housing = 1140000000
vehicle = 281.5429731455
cpi = 336.9226449663
xau = 3299.7201130435

smpl 111 111
month_jalali = "1404/03"
tedpix = 3059180.9444439998
usd = 825046.875
goldcoin = 737766666.6666669846
housing = 1120000000
vehicle = 288.165181126
cpi = 348.0585874095
xau = 3348.5763454545

smpl 112 112
month_jalali = "1404/04"
tedpix = 2805394.3500000001
usd = 880670.454545
goldcoin = 792645833.3333330154
housing = 1110000000
vehicle = 294.3342019278
cpi = 360.2368232962
xau = 3338.6359090909

smpl 113 113
month_jalali = "1404/05"
tedpix = 2610007.3333330001
usd = 919010.416667
goldcoin = 827110416.6666669846
housing = 1100000000
vehicle = 295.3405654506
cpi = 370.5359264908
xau = 3348.0217521739

smpl 114 114
month_jalali = "1404/06"
tedpix = 2537229.7000000002
usd = 1005047.916667
goldcoin = 934700000
housing = 1100000000
vehicle = 303.7211005771
cpi = 384.559349954
xau = 3571.902847619

smpl 115 115
month_jalali = "1404/07"
tedpix = 2871553.1363639999
usd = 1109580.769231
goldcoin = 1128396153.8461539745
housing = 1180000000
vehicle = 328.800922149
cpi = 403.7841139904
xau = 3995.6141318182

smpl 116 116
month_jalali = "1404/08"
tedpix = 3160949.3500000001
usd = 1094718
goldcoin = 1134042000
housing = 1230000000
vehicle = 343.0916564823
cpi = 417.5422415407
xau = 4047.8818272727

smpl 117 117
month_jalali = "1404/09"
tedpix = 3493649.5714289998
usd = 1229150
goldcoin = 1309404000
housing = 1220000000
vehicle = 380.078779667
cpi = 435.0844009723
xau = 4235.396455

smpl 118 118
month_jalali = "1404/10"
tedpix = 4234804.2999999998
usd = 1417688
goldcoin = 1593354000
housing = 1300000000
vehicle = 418.2381933557
cpi = 469.3638947498
xau = 4497.6500318182

smpl 119 119
month_jalali = "1404/11"
tedpix = 4048153.9473680002
usd = 1561676.6666669999
goldcoin = 1891418750
housing = 1450000000
vehicle = 479.9898878221
cpi = 513.6373920119
xau = 5002.1962583333

smpl 120 120
month_jalali = "1404/12"
tedpix = 3702776.1666669999
usd = 1624947.9166669999
goldcoin = 2009472916.6666669846
housing = 1390000000
vehicle = 485.7001616221
cpi = 542.3414344085
xau = 5084.1888

smpl 121 121
month_jalali = "1405/01"
tedpix = 3713956
usd = 1563352.0833330001
goldcoin = 1858568000
housing = 1477000000
vehicle = 497.3190390088
cpi = 569.3288044195
xau = 4652.8704347826

smpl 122 122
month_jalali = "1405/02"
tedpix = 3716222.818182
usd = 1736209.259259
goldcoin = 1918511111.1111109257
housing = 1570000000
vehicle = 635.8631784513
cpi = 619.5740765631
xau = 4641.8632

smpl @all


'------------------------------------------------------------------------------------
' 2. TRANSFORMATIONS: NOMINAL LOGS, CPI LOG, REAL LOGS
'------------------------------------------------------------------------------------
series LUSD   = log(usd)
series LGC    = log(goldcoin)
series LST    = log(tedpix)
series LVEH   = log(vehicle)
series LHOUS  = log(housing)
series LCPI   = log(cpi)

series RLUSD  = LUSD  - LCPI
series RLGC   = LGC   - LCPI
series RLST   = LST   - LCPI
series RLVEH  = LVEH  - LCPI
series RLHOUS = LHOUS - LCPI

series DRLUSD  = d(RLUSD)
series DRLGC   = d(RLGC)
series DRLST   = d(RLST)
series DRLVEH  = d(RLVEH)
series DRLHOUS = d(RLHOUS)

group RLEV5 RLUSD RLGC RLST RLVEH RLHOUS

'------------------------------------------------------------------------------------
' 4. CPI REAL-PRICE ROBUSTNESS: DESCRIPTIVES, LAG SELECTION, JOHANSEN, VECM
'------------------------------------------------------------------------------------
group RLEV4 RLUSD RLGC RLVEH RLHOUS

'------------------------------------------------------------------------------------
' 3. ADF UNIT-ROOT TESTS FOR CPI-ADJUSTED FOUR-VARIABLE SYSTEM
'    Same specification as the baseline EViews ADF battery:
'    AIC lag selection, maximum 12 lags
'------------------------------------------------------------------------------------

' Levels: intercept only
freeze(ADF_RLUSD_C)  RLUSD.uroot(adf,exog=const,dif=0,lagmethod=aic,maxlag=12)
freeze(ADF_RLGC_C)   RLGC.uroot(adf,exog=const,dif=0,lagmethod=aic,maxlag=12)
freeze(ADF_RLVEH_C)  RLVEH.uroot(adf,exog=const,dif=0,lagmethod=aic,maxlag=12)
freeze(ADF_RLHOUS_C) RLHOUS.uroot(adf,exog=const,dif=0,lagmethod=aic,maxlag=12)

' Levels: intercept + linear trend
freeze(ADF_RLUSD_CT)  RLUSD.uroot(adf,exog=trend,dif=0,lagmethod=aic,maxlag=12)
freeze(ADF_RLGC_CT)   RLGC.uroot(adf,exog=trend,dif=0,lagmethod=aic,maxlag=12)
freeze(ADF_RLVEH_CT)  RLVEH.uroot(adf,exog=trend,dif=0,lagmethod=aic,maxlag=12)
freeze(ADF_RLHOUS_CT) RLHOUS.uroot(adf,exog=trend,dif=0,lagmethod=aic,maxlag=12)

' First differences: intercept only
freeze(ADF_DRLUSD_C)  RLUSD.uroot(adf,exog=const,dif=1,lagmethod=aic,maxlag=12)
freeze(ADF_DRLGC_C)   RLGC.uroot(adf,exog=const,dif=1,lagmethod=aic,maxlag=12)
freeze(ADF_DRLVEH_C)  RLVEH.uroot(adf,exog=const,dif=1,lagmethod=aic,maxlag=12)
freeze(ADF_DRLHOUS_C) RLHOUS.uroot(adf,exog=const,dif=1,lagmethod=aic,maxlag=12)

freeze(M01_REAL4_STATS) RLEV4.stats

var RVAR4_LAG.ls 1 4 RLUSD RLGC RLVEH RLHOUS
freeze(M02_REAL4_LAG_SELECT) RVAR4_LAG.laglen(4)

var RVEC4.ec(c,1) 1 1 RLUSD RLGC RLVEH RLHOUS
freeze(M03_REAL4_JOH_CASE3) RVEC4.coint(rank)
freeze(M04_REAL4_VEC_R1) RVEC4.output

'------------------------------------------------------------------------------------
' 5. OUTPUT SPOOL
'------------------------------------------------------------------------------------
spool S3FINAL

' CPI-adjusted ADF outputs: Table SH, Panel A
S3FINAL.append ADF_RLUSD_C
S3FINAL.append ADF_RLGC_C
S3FINAL.append ADF_RLVEH_C
S3FINAL.append ADF_RLHOUS_C

S3FINAL.append ADF_RLUSD_CT
S3FINAL.append ADF_RLGC_CT
S3FINAL.append ADF_RLVEH_CT
S3FINAL.append ADF_RLHOUS_CT

S3FINAL.append ADF_DRLUSD_C
S3FINAL.append ADF_DRLGC_C
S3FINAL.append ADF_DRLVEH_C
S3FINAL.append ADF_DRLHOUS_C

' Existing Stage 3 outputs
S3FINAL.append M01_REAL4_STATS
S3FINAL.append M02_REAL4_LAG_SELECT
S3FINAL.append M03_REAL4_JOH_CASE3
S3FINAL.append M04_REAL4_VEC_R1

S3FINAL.save(t=rtf) "JQ_STAGE3_CPI_REAL_FINAL_WITH_ADF.rtf"
wfsave "JQ_STAGE3_CPI_REAL_FINAL_WITH_ADF.wf1"

' END

