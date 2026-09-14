'====================================================================================
' STAGE 1 - Baseline nominal Jalali monthly VECM pipeline
' EMBEDDED-DATA VERSION with IRF/FEVD using the previous working EViews syntax.
' Data calendar: Iranian Jalali months. No Gregorian conversion is used in estimation.
' Sample in embedded data: 1395/01-1405/02, 122 monthly observations.
'====================================================================================

close @all

' Set the working directory to the folder containing this PRG file.
%stage5_path = @runpath
cd %stage5_path

'------------------------------------------------------------------------------------
' 1. CREATE WORKFILE AND EMBED DATA
'------------------------------------------------------------------------------------
wfcreate(wf=JALALI_Q1) u 122
alpha month_jalali
series tedpix
series usd
series goldcoin
series housing
series vehicle

smpl 1 1
month_jalali = "1395/01"
tedpix = 80193.684211
usd = 34700.142857
goldcoin = 10236730
housing = 41317486
vehicle = 12.6596438195

smpl 2 2
month_jalali = "1395/02"
tedpix = 77453.52381
usd = 34486.55
goldcoin = 10305952.381
housing = 42135246
vehicle = 12.6801475006

smpl 3 3
month_jalali = "1395/03"
tedpix = 75435.238095
usd = 34602.714286
goldcoin = 10167271.4286
housing = 42445751
vehicle = 12.6600802373

smpl 4 4
month_jalali = "1395/04"
tedpix = 73895.05
usd = 34988.666667
goldcoin = 10868715.7895
housing = 42588469
vehicle = 12.6777552077

smpl 5 5
month_jalali = "1395/05"
tedpix = 77307.952381
usd = 35325.954545
goldcoin = 11100828.5714
housing = 42809232
vehicle = 12.77004824

smpl 6 6
month_jalali = "1395/06"
tedpix = 76926
usd = 35549.736842
goldcoin = 11154238.0952
housing = 42496061
vehicle = 12.8714978014

smpl 7 7
month_jalali = "1395/07"
tedpix = 77415.777778
usd = 35802.166667
goldcoin = 10984173.6842
housing = 43191738
vehicle = 12.936593947

smpl 8 8
month_jalali = "1395/08"
tedpix = 79295.238095
usd = 36329.761905
goldcoin = 11135852.381
housing = 43211137
vehicle = 12.9756737307

smpl 9 9
month_jalali = "1395/09"
tedpix = 80285.421053
usd = 38645.631579
goldcoin = 11312625
housing = 43335507
vehicle = 13.0305705406

smpl 10 10
month_jalali = "1395/10"
tedpix = 79284.05
usd = 39487.05
goldcoin = 11781114.2857
housing = 44133117
vehicle = 13.1115006539

smpl 11 11
month_jalali = "1395/11"
tedpix = 77564.238095
usd = 38316.380952
goldcoin = 11892723.8095
housing = 44140984
vehicle = 13.1181707709

smpl 12 12
month_jalali = "1395/12"
tedpix = 77123.65
usd = 37677.9
goldcoin = 11981895
housing = 44627525
vehicle = 13.1692140923

smpl 13 13
month_jalali = "1396/01"
tedpix = 77917.470588
usd = 37564.4375
goldcoin = 12099998.8235
housing = 43258124
vehicle = 13.1940323289

smpl 14 14
month_jalali = "1396/02"
tedpix = 79947.238095
usd = 37580.25
goldcoin = 12129170
housing = 44592486
vehicle = 13.252455557

smpl 15 15
month_jalali = "1396/03"
tedpix = 79996.380952
usd = 37393.952381
goldcoin = 12049818.0952
housing = 44914554
vehicle = 13.2781336003

smpl 16 16
month_jalali = "1396/04"
tedpix = 79229.736842
usd = 37811.611111
goldcoin = 12098554.7368
housing = 45390798
vehicle = 13.3167309173

smpl 17 17
month_jalali = "1396/05"
tedpix = 81550.863636
usd = 38138.652174
goldcoin = 12147165.6522
housing = 45862328
vehicle = 13.3559863857

smpl 18 18
month_jalali = "1396/06"
tedpix = 83615.15
usd = 38869.7
goldcoin = 12459280
housing = 46846337
vehicle = 13.4238901777

smpl 19 19
month_jalali = "1396/07"
tedpix = 85448.25
usd = 39750.4
goldcoin = 12847040
housing = 47157588
vehicle = 13.5021100771

smpl 20 20
month_jalali = "1396/08"
tedpix = 87647.8
usd = 40769.6
goldcoin = 13549452.381
housing = 48095658
vehicle = 13.5194203572

smpl 21 21
month_jalali = "1396/09"
tedpix = 92396.47619
usd = 41794.315789
goldcoin = 13956165
housing = 50001074
vehicle = 13.5334134957

smpl 22 22
month_jalali = "1396/10"
tedpix = 97105.52381
usd = 43479.761905
goldcoin = 14702680.9524
housing = 51481867
vehicle = 13.6040616054

smpl 23 23
month_jalali = "1396/11"
tedpix = 98425.285714
usd = 46382.181818
goldcoin = 15182863.5
housing = 54067640
vehicle = 13.6937354618

smpl 24 24
month_jalali = "1396/12"
tedpix = 96983.947368
usd = 47085.954545
goldcoin = 15744545.4545
housing = 56288507
vehicle = 13.9071852688

smpl 25 25
month_jalali = "1397/01"
tedpix = 96433.733333
usd = 51537.722222
goldcoin = 17914444.4444
housing = 55839522
vehicle = 14.0034894426

smpl 26 26
month_jalali = "1397/02"
tedpix = 94236.681818
usd = 61040.56
goldcoin = 19196923.0769
housing = 59843838
vehicle = 14.2246332927

smpl 27 27
month_jalali = "1397/03"
tedpix = 98127.333333
usd = 66817.318182
goldcoin = 22982173.913
housing = 64900102
vehicle = 14.8579388881

smpl 28 28
month_jalali = "1397/04"
tedpix = 110310.714286
usd = 81677.68
goldcoin = 28998600
housing = 69874753
vehicle = 15.3436883828

smpl 29 29
month_jalali = "1397/05"
tedpix = 123805.958333
usd = 103004.923077
goldcoin = 36982880.7692
housing = 74301929
vehicle = 18.0167409719

smpl 30 30
month_jalali = "1397/06"
tedpix = 144624.2
usd = 129219.238095
goldcoin = 43391739.1304
housing = 81223596
vehicle = 23.0228711681

smpl 31 31
month_jalali = "1397/07"
tedpix = 181837.590909
usd = 142900.72
goldcoin = 45302333.3333
housing = 86337581
vehicle = 22.1606951552

smpl 32 32
month_jalali = "1397/08"
tedpix = 181037.2
usd = 122009.090909
goldcoin = 42082090.9091
housing = 91857644
vehicle = 22.4558524305

smpl 33 33
month_jalali = "1397/09"
tedpix = 164431.421053
usd = 109450.75
goldcoin = 36735857.1429
housing = 96314357
vehicle = 23.3566667418

smpl 34 34
month_jalali = "1397/10"
tedpix = 161850.954545
usd = 109244
goldcoin = 37429181.8182
housing = 97784109
vehicle = 23.8105195876

smpl 35 35
month_jalali = "1397/11"
tedpix = 159225.45
usd = 118814.583333
goldcoin = 42301526.3158
housing = 100661546
vehicle = 25.4452722083

smpl 36 36
month_jalali = "1397/12"
tedpix = 166757.15
usd = 130269.565217
goldcoin = 45719631.5789
housing = 110092974
vehicle = 31.4529198872

smpl 37 37
month_jalali = "1398/01"
tedpix = 191126.0625
usd = 134547.894737
goldcoin = 47772062.5
housing = 114116598
vehicle = 29.7640504613

smpl 38 38
month_jalali = "1398/02"
tedpix = 211700.909091
usd = 145948.076923
goldcoin = 49644318.1818
housing = 127125592
vehicle = 34.0287658791

smpl 39 39
month_jalali = "1398/03"
tedpix = 227900.722222
usd = 134615.5
goldcoin = 46068437.5
housing = 134253535
vehicle = 33.3187685912

smpl 40 40
month_jalali = "1398/04"
tedpix = 247256.863636
usd = 127636
goldcoin = 44368318.1818
housing = 136156500
vehicle = 32.6755079202

smpl 41 41
month_jalali = "1398/05"
tedpix = 256353.5
usd = 118705.478261
goldcoin = 41670222.2222
housing = 131872735
vehicle = 31.6309857642

smpl 42 42
month_jalali = "1398/06"
tedpix = 290020.05
usd = 114116.25
goldcoin = 40588157.8947
housing = 127226350
vehicle = 30.7145684047

smpl 43 43
month_jalali = "1398/07"
tedpix = 316564.380952
usd = 114352.8
goldcoin = 39855285.7143
housing = 128481201
vehicle = 30.454375439

smpl 44 44
month_jalali = "1398/08"
tedpix = 305587.5
usd = 115539.130435
goldcoin = 40330388.8889
housing = 126175831
vehicle = 32.3479521494

smpl 45 45
month_jalali = "1398/09"
tedpix = 328353.904762
usd = 128555.6
goldcoin = 44541190.4762
housing = 134743944
vehicle = 34.6698829141

smpl 46 46
month_jalali = "1398/10"
tedpix = 376789.285714
usd = 133814.615385
goldcoin = 47784818.1818
housing = 138827000
vehicle = 36.1512807803

smpl 47 47
month_jalali = "1398/11"
tedpix = 442791.9
usd = 137581.25
goldcoin = 50641500
housing = 144057000
vehicle = 40.0259750719

smpl 48 48
month_jalali = "1398/12"
tedpix = 516826.789474
usd = 154107.826087
goldcoin = 59553043.4783
housing = 156587733
vehicle = 42.6792400663

smpl 49 49
month_jalali = "1399/01"
tedpix = 590234.470588
usd = 155946.2
goldcoin = 63773000
housing = 155457113
vehicle = 43.1680142183

smpl 50 50
month_jalali = "1399/02"
tedpix = 921318.173913
usd = 165174.444444
goldcoin = 67658518.5185
housing = 170066211
vehicle = 50.4998330452

smpl 51 51
month_jalali = "1399/03"
tedpix = 1084496.52941
usd = 178892.380952
goldcoin = 75080900
housing = 190718765
vehicle = 49.3208702777

smpl 52 52
month_jalali = "1399/04"
tedpix = 1657673.86957
usd = 217190
goldcoin = 97992115.3846
housing = 209860676
vehicle = 54.364595219

smpl 53 53
month_jalali = "1399/05"
tedpix = 1940474.95
usd = 226971.2
goldcoin = 109076400
housing = 229405325
vehicle = 59.8211146364

smpl 54 54
month_jalali = "1399/06"
tedpix = 1643801.66667
usd = 250366
goldcoin = 118886875
housing = 245349207
vehicle = 69.8468981348

smpl 55 55
month_jalali = "1399/07"
tedpix = 1532150.61905
usd = 296335.043478
goldcoin = 144984565.217
housing = 270033068
vehicle = 90.3385391126

smpl 56 56
month_jalali = "1399/08"
tedpix = 1278576.77778
usd = 273529.590909
goldcoin = 131223136.364
housing = 278282330
vehicle = 86.8702668005

smpl 57 57
month_jalali = "1399/09"
tedpix = 1447596.40909
usd = 256970.04
goldcoin = 118715560
housing = 269257382
vehicle = 79.4795482951

smpl 58 58
month_jalali = "1399/10"
tedpix = 1335007.85714
usd = 250447.666667
goldcoin = 114550291.667
housing = 277312291
vehicle = 79.0179623207

smpl 59 59
month_jalali = "1399/11"
tedpix = 1219526.1
usd = 243506
goldcoin = 111238400
housing = 282997657
vehicle = 79.3974076455

smpl 60 60
month_jalali = "1399/12"
tedpix = 1215112.4
usd = 248514.545455
goldcoin = 108726666.667
housing = 304788799
vehicle = 80.2779758402

smpl 61 61
month_jalali = "1400/01"
tedpix = 1256697.05556
usd = 248907.952381
goldcoin = 106732857.143
housing = 293227000
vehicle = 84.0227499496

smpl 62 62
month_jalali = "1400/02"
tedpix = 1181387.4
usd = 227003.73913
goldcoin = 99201913.0435
housing = 287966000
vehicle = 84.2683886351

smpl 63 63
month_jalali = "1400/03"
tedpix = 1141726.33333
usd = 237314.8
goldcoin = 105524400
housing = 296736000
vehicle = 86.5804927049

smpl 64 64
month_jalali = "1400/04"
tedpix = 1266209.15
usd = 247717.28
goldcoin = 106105560
housing = 300447000
vehicle = 89.6072860432

smpl 65 65
month_jalali = "1400/05"
tedpix = 1406234.1875
usd = 261071.363636
goldcoin = 114163478.261
housing = 309701000
vehicle = 94.7979608814

smpl 66 66
month_jalali = "1400/06"
tedpix = 1500982.3913
usd = 274651.111111
goldcoin = 119788518.519
housing = 317034000
vehicle = 100.346052639

smpl 67 67
month_jalali = "1400/07"
tedpix = 1445776.44444
usd = 276270.285714
goldcoin = 117769800
housing = 316311000
vehicle = 100.440554927

smpl 68 68
month_jalali = "1400/08"
tedpix = 1405729.80952
usd = 279696
goldcoin = 121695600
housing = 320090000
vehicle = 105.204605128

smpl 69 69
month_jalali = "1400/09"
tedpix = 1339646.63636
usd = 295543.461538
goldcoin = 129362307.692
housing = 325908000
vehicle = 111.06513327

smpl 70 70
month_jalali = "1400/10"
tedpix = 1351534.76191
usd = 283784.608696
goldcoin = 126629200
housing = 329364000
vehicle = 114.383763625

smpl 71 71
month_jalali = "1400/11"
tedpix = 1274276.2
usd = 270528.318182
goldcoin = 120312409.091
housing = 330562000
vehicle = 115.26994914

smpl 72 72
month_jalali = "1400/12"
tedpix = 1313482.63158
usd = 259928.695652
goldcoin = 121571782.609
housing = 351200000
vehicle = 114.013063058

smpl 73 73
month_jalali = "1401/01"
tedpix = 1458297.21053
usd = 274992.727273
goldcoin = 128699545.455
housing = 342727000
vehicle = 118.076935805

smpl 74 74
month_jalali = "1401/02"
tedpix = 1549367.38889
usd = 284614.380952
goldcoin = 136422409.091
housing = 363515000
vehicle = 126.652073393

smpl 75 75
month_jalali = "1401/03"
tedpix = 1545722
usd = 314238.52381
goldcoin = 151930733.333
housing = 394145000
vehicle = 128.309264487

smpl 76 76
month_jalali = "1401/04"
tedpix = 1498058.52632
usd = 315837.666667
goldcoin = 150405416.667
housing = 417049000
vehicle = 129.17919135

smpl 77 77
month_jalali = "1401/05"
tedpix = 1446004.80952
usd = 308950.333333
goldcoin = 144600000
housing = 427299000
vehicle = 129.338848598

smpl 78 78
month_jalali = "1401/06"
tedpix = 1411496
usd = 306236.84
goldcoin = 140671538.462
housing = 432169000
vehicle = 127.821024326

smpl 79 79
month_jalali = "1401/07"
tedpix = 1318095.94444
usd = 326417.545455
goldcoin = 149252954.545
housing = 437249000
vehicle = 129.303372064

smpl 80 80
month_jalali = "1401/08"
tedpix = 1344733.18182
usd = 346721.56
goldcoin = 158382692.308
housing = 467048000
vehicle = 133.910366031

smpl 81 81
month_jalali = "1401/09"
tedpix = 1431938.27273
usd = 371325.28
goldcoin = 177687160
housing = 480737000
vehicle = 145.958354883

smpl 82 82
month_jalali = "1401/10"
tedpix = 1620455.89474
usd = 410590.666667
goldcoin = 210781428.571
housing = 519814000
vehicle = 177.337232859

smpl 83 83
month_jalali = "1401/11"
tedpix = 1573749.05263
usd = 450395.736842
goldcoin = 249105473.684
housing = 571444000
vehicle = 185.78024645

smpl 84 84
month_jalali = "1401/12"
tedpix = 1787448
usd = 510005.263158
goldcoin = 291396105.263
housing = 652414000
vehicle = 206.227481822

smpl 85 85
month_jalali = "1402/01"
tedpix = 2162883
usd = 512881.368421
goldcoin = 318478157.895
housing = 664400000
vehicle = 229.022175568

smpl 86 86
month_jalali = "1402/02"
tedpix = 2373097.21053
usd = 529363.869565
goldcoin = 323922227.273
housing = 753200000
vehicle = 222.339245753

smpl 87 87
month_jalali = "1402/03"
tedpix = 2238705.76191
usd = 500240.8
goldcoin = 295176000
housing = 783000000
vehicle = 204.500109189

smpl 88 88
month_jalali = "1402/04"
tedpix = 2120824.42857
usd = 494227.2
goldcoin = 282198800
housing = 765400000
vehicle = 198.215705756

smpl 89 89
month_jalali = "1402/05"
tedpix = 1992791.31818
usd = 492445.2
goldcoin = 282846240
housing = 757900000
vehicle = 194.900667735

smpl 90 90
month_jalali = "1402/06"
tedpix = 2101480.21053
usd = 494222.608696
goldcoin = 279816521.739
housing = 753300000
vehicle = 193.1770099

smpl 91 91
month_jalali = "1402/07"
tedpix = 2046556.3
usd = 505855.086957
goldcoin = 283542173.913
housing = 760600000
vehicle = 194.009333164

smpl 92 92
month_jalali = "1402/08"
tedpix = 2016702.63636
usd = 511505.384615
goldcoin = 291476538.462
housing = 757700000
vehicle = 195.357200206

smpl 93 93
month_jalali = "1402/09"
tedpix = 2125611.05
usd = 504429.75
goldcoin = 291991875
housing = 740900000
vehicle = 196.315564308

smpl 94 94
month_jalali = "1402/10"
tedpix = 2176320.85714
usd = 515226.153846
goldcoin = 305908076.923
housing = 753900000
vehicle = 207.031866688

smpl 95 95
month_jalali = "1402/11"
tedpix = 2104630
usd = 561256.863636
goldcoin = 326835590.909
housing = 784800000
vehicle = 218.719239624

smpl 96 96
month_jalali = "1402/12"
tedpix = 2124936.57895
usd = 593417.272727
goldcoin = 357312000
housing = 814400000
vehicle = 228.855036726

smpl 97 97
month_jalali = "1403/01"
tedpix = 2235167.1875
usd = 623795.7
goldcoin = 423586500
housing = 816300000
vehicle = 240.056197265

smpl 98 98
month_jalali = "1403/02"
tedpix = 2234730.72727
usd = 614919.230769
goldcoin = 413981153.846
housing = 847500000
vehicle = 242.251603996

smpl 99 99
month_jalali = "1403/03"
tedpix = 2073244.11111
usd = 606078.26087
goldcoin = 402951521.739
housing = 859100000
vehicle = 240.012648948

smpl 100 100
month_jalali = "1403/04"
tedpix = 2142929.68421
usd = 593144.166667
goldcoin = 411628750
housing = 874600000
vehicle = 240.381414646

smpl 101 101
month_jalali = "1403/05"
tedpix = 2053255.5
usd = 594792.307692
goldcoin = 420735000
housing = 885000000
vehicle = 238.67856626

smpl 102 102
month_jalali = "1403/06"
tedpix = 2083915.05882
usd = 594083.333333
goldcoin = 434588095.238
housing = 950000000
vehicle = 237.531508093

smpl 103 103
month_jalali = "1403/07"
tedpix = 2100072.68182
usd = 624332.692308
goldcoin = 493067307.692
housing = 960000000
vehicle = 240.356349524

smpl 104 104
month_jalali = "1403/08"
tedpix = 2092621.86364
usd = 683417.307692
goldcoin = 518903846.154
housing = 980000000
vehicle = 244.836842003

smpl 105 105
month_jalali = "1403/09"
tedpix = 2494783.5
usd = 723904.166667
goldcoin = 527729166.667
housing = 990000000
vehicle = 257.380812771

smpl 106 106
month_jalali = "1403/10"
tedpix = 2831455.61905
usd = 801408
goldcoin = 560426000
housing = 1010000000
vehicle = 262.422794702

smpl 107 107
month_jalali = "1403/11"
tedpix = 2777380.73684
usd = 864977.083333
goldcoin = 672197916.667
housing = 1030000000
vehicle = 269.186472554

smpl 108 108
month_jalali = "1403/12"
tedpix = 2766307.8
usd = 921897.826087
goldcoin = 785186956.522
housing = 1070000000
vehicle = 273.848831635

smpl 109 109
month_jalali = "1404/01"
tedpix = 2860957.875
usd = 952690
goldcoin = 891266666.667
housing = 1062000000
vehicle = 283.753713646

smpl 110 110
month_jalali = "1404/02"
tedpix = 3153188.52174
usd = 827661.538462
goldcoin = 737511538.462
housing = 1140000000
vehicle = 281.542973145

smpl 111 111
month_jalali = "1404/03"
tedpix = 3059180.94444
usd = 825046.875
goldcoin = 737766666.667
housing = 1120000000
vehicle = 288.165181126

smpl 112 112
month_jalali = "1404/04"
tedpix = 2805394.35
usd = 880670.454545
goldcoin = 792645833.333
housing = 1110000000
vehicle = 294.334201928

smpl 113 113
month_jalali = "1404/05"
tedpix = 2610007.33333
usd = 919010.416667
goldcoin = 827110416.667
housing = 1100000000
vehicle = 295.340565451

smpl 114 114
month_jalali = "1404/06"
tedpix = 2537229.7
usd = 1005047.91667
goldcoin = 934700000
housing = 1100000000
vehicle = 303.721100577

smpl 115 115
month_jalali = "1404/07"
tedpix = 2871553.13636
usd = 1109580.76923
goldcoin = 1128396153.85
housing = 1180000000
vehicle = 328.800922149

smpl 116 116
month_jalali = "1404/08"
tedpix = 3160949.35
usd = 1094718
goldcoin = 1134042000
housing = 1230000000
vehicle = 343.091656482

smpl 117 117
month_jalali = "1404/09"
tedpix = 3493649.57143
usd = 1229150
goldcoin = 1309404000
housing = 1220000000
vehicle = 380.078779667

smpl 118 118
month_jalali = "1404/10"
tedpix = 4234804.3
usd = 1417688
goldcoin = 1593354000
housing = 1300000000
vehicle = 418.238193356

smpl 119 119
month_jalali = "1404/11"
tedpix = 4048153.94737
usd = 1561676.66667
goldcoin = 1891418750
housing = 1450000000
vehicle = 479.989887822

smpl 120 120
month_jalali = "1404/12"
tedpix = 3702776.16667
usd = 1624947.91667
goldcoin = 2009472916.67
housing = 1390000000
vehicle = 485.700161622

smpl 121 121
month_jalali = "1405/01"
tedpix = 3713956
usd = 1563352.08333
goldcoin = 1858568000
housing = 1477000000
vehicle = 497.319039009

smpl 122 122
month_jalali = "1405/02"
tedpix = 3716222.81818
usd = 1736209.25926
goldcoin = 1918511111.11
housing = 1570000000
vehicle = 635.863178451

smpl @all

'------------------------------------------------------------------------------------
' 2. CONSTRUCT LOG LEVELS AND RETURNS
'------------------------------------------------------------------------------------
series LUSD     = log(usd)
series LGCOIN   = log(goldcoin)
series LSTOCK   = log(tedpix)
series LVEHICLE = log(vehicle)
series LHOUSING = log(housing)

series DLUSD     = d(LUSD)
series DLGCOIN   = d(LGCOIN)
series DLSTOCK   = d(LSTOCK)
series DLVEHICLE = d(LVEHICLE)
series DLHOUSING = d(LHOUSING)

group G5  LUSD LGCOIN LSTOCK LVEHICLE LHOUSING
group DG5 DLUSD DLGCOIN DLSTOCK DLVEHICLE DLHOUSING
group G4  LUSD LGCOIN LVEHICLE LHOUSING
group DG4 DLUSD DLGCOIN DLVEHICLE DLHOUSING



'------------------------------------------------------------------------------------
' 3. STAGE 5 V3: ALTERNATIVE CHOLESKY ORDERINGS BY RE-ORDERED VECM OBJECTS
'------------------------------------------------------------------------------------
' This safer version avoids explicit @ @ ordering syntax.
' Each VECM is estimated with the variable order that defines the Cholesky ordering.
' Output: 12-month FEVD only, for appendix use.
'------------------------------------------------------------------------------------

' BASE ordering: LUSD LGCOIN LVEHICLE LHOUSING
var VEC4B.ec(c,1) 1 1 LUSD LGCOIN LVEHICLE LHOUSING
freeze(FEVD_BASE_12) VEC4B.decomp(12,imp=chol) LUSD LGCOIN LVEHICLE LHOUSING @ @ LUSD LGCOIN LVEHICLE LHOUSING

' REVERSE ordering: LHOUSING LVEHICLE LGCOIN LUSD
var VEC4R.ec(c,1) 1 1 LHOUSING LVEHICLE LGCOIN LUSD
freeze(FEVD_REVERSE_12) VEC4R.decomp(12,imp=chol) LHOUSING LVEHICLE LGCOIN LUSD @ @ LHOUSING LVEHICLE LGCOIN LUSD

' SWAP ordering: LGCOIN LUSD LHOUSING LVEHICLE
var VEC4S.ec(c,1) 1 1 LGCOIN LUSD LHOUSING LVEHICLE
freeze(FEVD_SWAP_12) VEC4S.decomp(12,imp=chol) LGCOIN LUSD LHOUSING LVEHICLE @ @ LGCOIN LUSD LHOUSING LVEHICLE

spool SP_STAGE5_ALT_CHOL_V3
SP_STAGE5_ALT_CHOL_V3.append FEVD_BASE_12
SP_STAGE5_ALT_CHOL_V3.append FEVD_REVERSE_12
SP_STAGE5_ALT_CHOL_V3.append FEVD_SWAP_12

' Save the report and complete EViews workfile beside this PRG file.
SP_STAGE5_ALT_CHOL_V3.save(t=rtf) "JQ_STAGE5_ALT_CHOL_FEVD_V3.rtf"
wfsave "JQ_STAGE5_ALT_CHOL_FEVD_V3.wf1"

'============================================================
' END: Stage 5 outputs are saved beside the running PRG file.
'============================================================
