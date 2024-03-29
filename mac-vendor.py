import re
import sys

# extracted from https://gist.github.com/aallan/b4bb86db86079509e6159810ae9bd3e4
vendors = """
000000	Officially Xerox
000001	SuperLAN-2U
000002	BBN (was internal usage only, no longer used)
000003	XEROX CORPORATION
000004	XEROX CORPORATION
000005	XEROX CORPORATION
000006	XEROX CORPORATION
000007	XEROX CORPORATION
000008	XEROX CORPORATION
000009	powerpipes?
00000A	OMRON TATEISI ELECTRONICS CO.
00000B	MATRIX CORPORATION
00000C	Cisco
00000D	FIBRONICS LTD.
00000E	Fujitsu
00000F	Next
000010	Hughes
000011	Tektrnix
000012	INFORMATION TECHNOLOGY LIMITED
000013	Camex
000014	Netronix
000015	Datapoint Corporation
000016	DU PONT PIXEL SYSTEMS     .
000017	Oracle
000018	Webster Computer Corporation	Appletalk/Ethernet Gateway
000019	APPLIED DYNAMICS INTERNATIONAL
00001A	AMD
00001B	Novell (now Eagle Technology)
00001C	JDR Microdevices		generic, NE2000 drivers
00001D	Cabletron
00001E	TELSIST INDUSTRIA ELECTRONICA
00001F	Cryptall Communications Corp.
000020	DIAB
000021	SC&C
000022	Visual Technology
000023	ABB Automation AB, Dept. Q
000024	Olicom
000025	RAMTEK CORP.
000026	SHA-KEN CO., LTD.
000027	JAPAN RADIO COMPANY
000028	PRODIGY SYSTEMS CORPORATION
000029	Imc
00002A	Trw
00002B	CRISP AUTOMATION, INC
00002C	NRC - Network Resources Corporation - MultiGate Hub1+, Hub2, etc
00002D	CHROMATICS INC
00002E	SOCIETE EVIRA
00002F	TIMEPLEX INC.
000030	VG LABORATORY SYSTEMS LTD
000031	QPSX COMMUNICATIONS, LTD.
000032	GPT Limited (reassigned from GEC Computers Ltd)
000033	EGAN MACHINERY COMPANY
000034	NETWORK RESOURCES CORPORATION
000035	SPECTRAGRAPHICS CORPORATION
000036	ATARI CORPORATION
000037	Oxford Metrics Ltd
000038	CSS LABS
000039	TOSHIBA CORPORATION
00003A	CHYRON CORPORATION
00003B	Hyundai/	# Hyundai/Axil			Sun clones
00003C	Auspex
00003D	AT&T
00003E	Simpact
00003F	Syntrex Inc
000040	APPLICON, INC.
000041	ICE CORPORATION
000042	METIER MANAGEMENT SYSTEMS LTD.
000043	MICRO TECHNOLOGY
000044	Castelle
000045	FORD AEROSPACE & COMM. CORP.
000046	ISC-BR
000047	NICOLET INSTRUMENTS CORP.
000048	Epson
000049	Apricot Ltd.
00004A	ADC CODENOLL TECHNOLOGY CORP.
00004B	APT
00004C	NEC Corporation
00004D	DCI CORPORATION
00004E	AMPEX CORPORATION
00004F	Logicraft 386-Ware P.C. Emulator
000050	RADISYS CORPORATION
000051	Hob Electronic Gmbh & Co. KG
000052	Optical Data Systems
000053	COMPUCORP
000054	Schneider Electric
000055	AT&T
000056	DR. B. STRUCK
000057	SCITEX CORPORATION LTD.
000058	Racore Computer Products Inc
000059	Hellige GMBH
00005A	SK	(Schneider & Koch in Europe and Syskonnect outside of Europe)
00005B	Eltec
00005C	TELEMATICS INTERNATIONAL INC.
00005D	Rce
00005E	U.S. Department of Defense (IANA)
00005F	Sumitomo
000060	KONTRON ELEKTRONIK GMBH
000061	Gateway Communications
000062	Honeywell
000063	HP
000064	Yokogawa Digital Computer Corp
000065	Network General
000066	Talaris
000067	SOFT * RITE, INC.
000068	Rosemount Controls
000069	SGI
00006A	COMPUTER CONSOLES INC.
00006B	MIPS
00006C	Private
00006D	Case
00006E	Artisoft, Inc.
00006F	Madge Networks Ltd.		Token-ring adapters
000070	HCL LIMITED
000071	ADRA SYSTEMS INC.
000072	MINIWARE TECHNOLOGY
000073	Dupont
000074	RICOH COMPANY LTD.
000075	Bell Northern Research (BNR)
000076	ABEKAS VIDEO SYSTEM
000077	Interphase		[Used in other systems, e.g. MIPS, Motorola]
000078	Labtam Australia
000079	Networth Incorporated	[bought by Compaq, used in Netelligent series]
00007A	Ardent
00007B	Research Machines
00007C	AMPERE INCORPORATED
00007D	Cray
00007E	NetFRAME multiprocessor network servers
00007F	Linotype-Hell AG		Linotronic typesetters
000080	Cray Communications (formerly Dowty Network Services)	[Also shows as "Harris (3M) (new)" and/or "Imagen(?)" elsewhere]
000081	Synoptics
000082	LECTRA SYSTEMES SA
000083	Tadpole Technology  [had Optical Data Systems which is wrong according to both]
000084	Aquila (?), ADI Systems Inc.(?)
000085	CANON INC.
000086	Gateway Communications Inc. (then Megahertz & now 3com)
000087	Hitachi
000088	Brocade Communications Systems, Inc.
000089	Cayman Systems			Gatorbox
00008A	Datahouse Information Systems
00008B	Infotron
00008C	Alloy Computer Products (Australia) Pty Ltd
00008D	Cryptek Inc.
00008E	Solbourne(?), Jupiter(?) (I've had confirming mail on Solbourne)
00008F	Raytheon
000090	Microcom
000091	ANRITSU CORPORATION
000092	Unisys, Cogent (both reported)
000093	Proteon
000094	Asante				MAC
000095	Sony/Tektronix
000096	MARCONI ELECTRONICS LTD.
000097	Epoch
000098	Cross Com
000099	Memorex Telex Corporations
00009A	RC COMPUTER A/S
00009B	INFORMATION INTERNATIONAL, INC
00009C	RolmMil-               # ROLM MIL-SPEC COMPUTERS
00009D	LOCUS COMPUTING CORPORATION
00009E	MARLI S.A.
00009F	Ameristar Technology
0000A0	Sanyo Electronics
0000A1	MARQUETTE ELECTRIC CO.
0000A2	Wellfleet
0000A3	NAT
0000A4	Acorn
0000A5	CSC
0000A6	Network General (internal assignment, not for products)
0000A7	NCD
0000A8	Stratus Computer, Inc.
0000A9	Network Systems
0000AA	Xerox				Xerox machines
0000AB	LOGIC MODELING CORPORATION
0000AC	Conware Netzpartner		[had Apollo, claimed incorrect]
0000AD	BRUKER INSTRUMENTS INC.
0000AE	Dassault Automatismes et Telecommunications
0000AF	Nuclear Data			Acquisition Interface Modules (AIM)
0000B0	RND (RAD Network Devices)
0000B1	Alpha Microsystems Inc.
0000B2	TELEVIDEO SYSTEMS, INC.
0000B3	Cimlinc
0000B4	Edimax
0000B5	Datability			Terminal Servers
0000B6	Micro-matic Research
0000B7	Dove				Fastnet
0000B8	SEIKOSHA CO., LTD.
0000B9	MCDONNELL DOUGLAS COMPUTER SYS
0000BA	SIIG, INC.
0000BB	TRI-DATA Systems Inc.		Netway products, 3274 emulators
0000BC	Allen-Bradley
0000BD	MITSUBISHI CABLE COMPANY
0000BE	THE NTI GROUP
0000BF	SYMMETRIC COMPUTER SYSTEMS
0000C0	Western Digital now SMC (Std. Microsystems Corp.)
0000C1	Olicom A/S
0000C2	INFORMATION PRESENTATION TECH.
0000C3	HARRIS CORP COMPUTER SYS DIV
0000C4	WATERS DIV. OF MILLIPORE
0000C5	Farallon Computing Inc
0000C6	HP Intelligent Networks Operation (formerly Eon Systems)
0000C7	ARIX CORPORATION
0000C8	Altos
0000C9	Emulex				Terminal Servers, Print Servers
0000CA	LANcity Cable Modems (now owned by BayNetworks)
0000CB	COMPU-SHACK ELECTRONIC GMBH
0000CC	Densan Co., Ltd.
0000CD	Industrial Research Limited
0000CE	MEGADATA CORP.
0000CF	HAYES MICROCOMPUTER PRODUCTS
0000D0	Develcon Electronics, Ltd.
0000D1	Adaptec, Inc.			"Nodem" product
0000D2	SBE Inc
0000D3	Wang Labs
0000D4	Puredata
0000D5	MICROGNOSIS INTERNATIONAL
0000D6	PUNCH LINE HOLDING
0000D7	Dartmouth College (NED Router)
0000D8	old Novell NE1000's (before about 1987?) (also 3Com)
0000D9	NIPPON TELEGRAPH & TELEPHONE
0000DA	Atex
0000DB	British Telecommunications plc
0000DC	HAYES MICROCOMPUTER PRODUCTS
0000DD	Gould
0000DE	Unigraph
0000DF	BELL & HOWELL PUB SYS DIV
0000E0	QUADRAM CORP.
0000E1	Hitachi
0000E2	Acer Counterpoint
0000E3	Integrated Micro Products Ltd
0000E4	Mips?
0000E5	SIGMEX LTD.
0000E6	Aptor Produits De Comm Indust
0000E7	Star Gate Technologies
0000E8	Accton Technology Corporation
0000E9	ISICAD, Inc.
0000EA	UPNOD AB
0000EB	MATSUSHITA COMM. IND. CO. LTD.
0000EC	MICROPROCESS
0000ED	April
0000EE	Network Designers Limited [also KNX Ltd, a former division]
0000EF	Alantec				(now owned by ForeSystems)
0000F0	Samsung
0000F1	MAGNA COMPUTER CORPORATION
0000F2	Spider Communications		(Montreal, not Spider Systems)
0000F3	Gandalf Data Ltd. - Canada
0000F4	Allied Telesis, Inc.
0000F5	DIAMOND SALES LIMITED
0000F6	Madge
0000F7	YOUTH KEEP ENTERPRISE CO LTD
0000F8	Dec
0000F9	QUOTRON SYSTEMS INC.
0000FA	MICROSAGE COMPUTER SYSTEMS INC
0000FB	Rechner zur Kommunikation
0000FC	Meiko
0000FD	High Level Hardware (Orion, UK)
0000FE	ANNAPOLIS MICRO SYSTEMS
0000FF	Camtec Electronics (UK) Ltd.
000100	EQUIP'TRANS
000101	Private
000102	BBN (Bolt Beranek and Newman, Inc.)	internal usage (not registered)
000103	3COM CORPORATION
000104	DVICO Co., Ltd.
000105	Beckhoff Automation GmbH
000106	Tews Datentechnik GmbH
000107	Leiser GmbH
000108	AVLAB Technology, Inc.
000109	Nagano Japan Radio Co., Ltd.
00010A	CIS TECHNOLOGY INC.
00010B	Space CyberLink, Inc.
00010C	System Talks Inc.
00010D	Teledyne DALSA Inc.
00010E	Bri-Link Technologies Co., Ltd
00010F	Brocade Communications Systems, Inc.
000110	Gotham Networks
000111	iDigm Inc.
000112	Shark Multimedia Inc.
000113	OLYMPUS CORPORATION
000114	KANDA TSUSHIN KOGYO CO., LTD.
000115	EXTRATECH CORPORATION
000116	Netspect Technologies, Inc.
000117	Canal+                 # Canal +
000118	EZ Digital Co., Ltd.
000119	RTUnet (Australia)
00011A	Hoffmann und Burmeister GbR
00011B	Unizone Technologies, Inc.
00011C	Universal Talkware Corporation
00011D	Centillium Communications
00011E	Precidia Technologies, Inc.
00011F	RC Networks, Inc.
000120	OSCILLOQUARTZ S.A.
000121	Watchguard Technologies, Inc.
000122	Trend Communications, Ltd.
000123	DIGITAL ELECTRONICS CORP.
000124	Acer Incorporated
000125	YAESU MUSEN CO., LTD.
000126	PAC Labs
000127	OPEN Networks Pty Ltd
000128	EnjoyWeb, Inc.
000129	DFI Inc.
00012A	Telematica Sistems Inteligente
00012B	TELENET Co., Ltd.
00012C	Aravox Technologies, Inc.
00012D	Komodo Technology
00012E	PC Partner Ltd.
00012F	Twinhead International Corp
000130	Extreme Networks
000131	Bosch Security Systems, Inc.
000132	Dranetz-               # Dranetz - BMI
000133	KYOWA Electronic Instruments C
000134	Selectron Systems AG
000135	KDC Corp.
000136	CyberTAN Technology Inc.
000137	IT Farm Corporation
000138	XAVi Technologies Corp.
000139	Point Multimedia Systems
00013A	SHELCAD COMMUNICATIONS, LTD.
00013B	BNA SYSTEMS
00013C	TIW SYSTEMS
00013D	RiscStation Ltd.
00013E	Ascom Tateco AB
00013F	Neighbor World Co., Ltd.
000140	Sendtek Corporation
000141	CABLE PRINT
000142	Cisco Systems, Inc
000143	IEEE 802
000144	EMC Corporation
000145	WINSYSTEMS, INC.
000146	Tesco Controls, Inc.
000147	Zhone Technologies
000148	X-traWeb Inc.
000149	T.D.T. Transfer Data Test GmbH
00014A	Sony Corporation
00014B	Ennovate Networks, Inc.
00014C	Berkeley Process Control
00014D	Shin Kin Enterprises Co., Ltd
00014E	WIN Enterprises, Inc.
00014F	Adtran Inc
000150	Megahertz (now 3com) modem
000151	Ensemble Communications
000152	CHROMATEK INC.
000153	ARCHTEK TELECOM CORPORATION
000154	G3M Corporation
000155	Promise Technology, Inc.
000156	FIREWIREDIRECT.COM, INC.
000157	SYSWAVE CO., LTD
000158	Electro Industries/Gauge Tech
000159	S1 Corporation
00015A	Digital Video Broadcasting
00015B	ITALTEL S.p.A/RF-UP-I
00015C	CADANT INC.
00015D	Oracle Corporation
00015E	BEST TECHNOLOGY CO., LTD.
00015F	DIGITAL DESIGN GmbH
000160	ELMEX Co., LTD.
000161	Meta Machine Technology
000162	Cygnet Technologies, Inc.
000163	NDC (National Datacomm Corporation)
000164	Cisco Systems, Inc
000165	AirSwitch Corporation
000166	TC GROUP A/S
000167	HIOKI E.E. CORPORATION
000168	W&G (Wandel & Goltermann)	[incorrect according to W&G]
000169	Celestix Networks Pte Ltd.
00016A	Alitec
00016B	LightChip, Inc.
00016C	Foxconn
00016D	CarrierComm Inc.
00016E	Conklin Corporation
00016F	Inkel Corp.
000170	ESE Embedded System Engineer'g
000171	Allied Data Technologies
000172	TechnoLand Co., LTD.
000173	Amcc
000174	CyberOptics Corporation
000175	Radiant Communications Corp.
000176	Orient Silver Enterprises
000177	Edsl
000178	MARGI Systems, Inc.
000179	WIRELESS TECHNOLOGY, INC.
00017A	Chengdu Maipu Electric Industrial Co., Ltd.
00017B	Heidelberger Druckmaschinen AG
00017C	AG-E GmbH
00017D	ThermoQuest
00017E	ADTEK System Science Co., Ltd.
00017F	Experience Music Project
000180	AOpen, Inc.
000181	Nortel Networks
000182	DICA TECHNOLOGIES AG
000183	ANITE TELECOMS
000184	SIEB & MEYER AG
000185	Hitachi Aloka Medical, Ltd.
000186	Uwe Disch
000187	I2SE GmbH
000188	LXCO Technologies ag
000189	Refraction Technology, Inc.
00018A	ROI COMPUTER AG
00018B	NetLinks Co., Ltd.
00018C	Mega Vision
00018D	AudeSi Technologies
00018E	Logitec Corporation
00018F	Kenetec, Inc.
000190	Smk-M
000191	SYRED Data Systems
000192	Texas Digital Systems
000193	Hanbyul Telecom Co., Ltd.
000194	Capital Equipment Corporation
000195	Sena Technologies, Inc.
000196	Cisco Systems, Inc
000197	Cisco Systems, Inc
000198	Darim Vision
000199	HeiSei Electronics
00019A	LEUNIG GmbH
00019B	Kyoto Microcomputer Co., Ltd.
00019C	JDS Uniphase Inc.
00019D	E-Control Systems, Inc.
00019E	ESS Technology, Inc.
00019F	Readynet
0001A0	Infinilink Corporation
0001A1	Mag-Tek, Inc.
0001A2	Logical Co., Ltd.
0001A3	GENESYS LOGIC, INC.
0001A4	Microlink Corporation
0001A5	Nextcomm, Inc.
0001A6	Scientific-Atlanta Arcodan A/S
0001A7	UNEX TECHNOLOGY CORPORATION
0001A8	Welltech Computer Co., Ltd.
0001A9	BMW AG
0001AA	Airspan Communications, Ltd.
0001AB	Main Street Networks
0001AC	Sitara Networks, Inc.
0001AD	Coach Master International  d.b.a. CMI Worldwide, Inc.
0001AE	Trex Enterprises
0001AF	Artesyn Embedded Technologies
0001B0	Fulltek Technology Co., Ltd.
0001B1	General Bandwidth
0001B2	Digital Processing Systems, Inc.
0001B3	Precision Electronic Manufacturing
0001B4	Wayport, Inc.
0001B5	Turin Networks, Inc.
0001B6	SaejinT&               # SAEJIN T&M Co., Ltd.
0001B7	Centos, Inc.
0001B8	Netsensity, Inc.
0001B9	SKF Condition Monitoring
0001BA	IC-Net, Inc.
0001BB	Frequentis
0001BC	Brains Corporation
0001BD	Peterson Electro-Musical Products, Inc.
0001BE	Gigalink Co., Ltd.
0001BF	Teleforce Co., Ltd.
0001C0	CompuLab, Ltd.
0001C1	Vitesse Semiconductor Corporation
0001C2	ARK Research Corp.
0001C3	Acromag, Inc.
0001C4	NeoWave, Inc.
0001C5	Simpler Networks
0001C6	Quarry Technologies
0001C7	Cisco Systems, Inc
0001C8	Thomas Conrad Corp.
0001C9	Cisco Systems, Inc
0001CA	Geocast Network Systems, Inc.
0001CB	Evr
0001CC	Japan Total Design Communication Co., Ltd.
0001CD	Artem
0001CE	Custom Micro Products, Ltd.
0001CF	Alpha Data Parallel Systems, Ltd.
0001D0	VitalPoint, Inc.
0001D1	CoNet Communications, Inc.
0001D2	inXtron, Inc.
0001D3	PAXCOMM, Inc.
0001D4	Leisure Time, Inc.
0001D5	HAEDONG INFO & COMM CO., LTD
0001D6	manroland AG
0001D7	F5 Networks, Inc.
0001D8	Teltronics, Inc.
0001D9	Sigma, Inc.
0001DA	WINCOMM Corporation
0001DB	Freecom Technologies GmbH
0001DC	Activetelco
0001DD	Avail Networks
0001DE	Trango Systems, Inc.
0001DF	ISDN Communications, Ltd.
0001E0	Fast Systems, Inc.
0001E1	Kinpo Electronics, Inc.
0001E2	Ando Electric Corporation
0001E3	Siemens AG
0001E4	Sitera, Inc.
0001E5	Supernet, Inc.
0001E6	Hewlett Packard
0001E7	Hewlett Packard
0001E8	Force10 Networks, Inc.
0001E9	Litton Marine Systems B.V.
0001EA	Cirilium Corp.
0001EB	C-COM Corporation
0001EC	Ericsson Group
0001ED	SETA Corp.
0001EE	Comtrol Europe, Ltd.
0001EF	Camtel Technology Corp.
0001F0	Tridium, Inc.
0001F1	Innovative Concepts, Inc.
0001F2	Mark of the Unicorn, Inc.
0001F3	QPS, Inc.
0001F4	Enterasys
0001F5	ERIM S.A.
0001F6	Association of Musical Electronics Industry
0001F7	Image Display Systems, Inc.
0001F8	TEXIO TECHNOLOGY CORPORATION
0001F9	TeraGlobal Communications Corp.
0001FA	Compaq
0001FB	DoTop Technology, Inc.
0001FC	Keyence Corporation
0001FD	Digital Voice Systems, Inc.
0001FE	DIGITAL EQUIPMENT CORPORATION
0001FF	Data Direct Networks, Inc.
000200	Net & Sys Co., Ltd.
000201	IFM Electronic gmbh
000202	Amino Communications, Ltd.
000203	Woonsang Telecom, Inc.
000204	Novell
000205	Hamilton (Sparc Clones)
000206	Telital R&D Denmark A/S
000207	VisionGlobal Network Corp.
000208	Unify Networks, Inc.
000209	Shenzhen SED Information Technology Co., Ltd.
00020A	Gefran Spa
00020B	Native Networks, Inc.
00020C	Metro-Optix
00020D	Micronpc.com
00020E	ECI Telecom Ltd.
00020F	Aatr
000210	Fenecom
000211	Nature Worldwide Technology Corp.
000212	SierraCom
000213	S.D.E.L.
000214	Dtvro
000215	Cotas Computer Technology A/B
000216	ESI (Extended Systems, Inc)	print servers
000217	Cisco Systems, Inc
000218	Advanced Scientific Corp
000219	Paralon Technologies
00021A	Zuma Networks
00021B	Kollmorgen-Servotronix
00021C	Network Elements, Inc.
00021D	Data General Communication Ltd.
00021E	SIMTEL S.R.L.
00021F	Aculab PLC
000220	CANON FINETECH INC.
000221	DSP Application, Ltd.
000222	Chromisys, Inc.
000223	Clicktv
000224	C-Cor
000225	One Stop Systems
000226	XESystems, Inc.
000227	ESD Electronic System Design GmbH
000228	Necsom, Ltd.
000229	Adtec Corporation
00022A	Asound Electronic
00022B	SAXA, Inc.
00022C	ABB Bomem, Inc.
00022D	Agere Systems
00022E	TEAC Corp. R& D
00022F	P-Cube, Ltd.
000230	Intersoft Electronics
000231	Axis
000232	Avision, Inc.
000233	Mantra Communications, Inc.
000234	Imperial Technology, Inc.
000235	Paragon Networks International
000236	INIT GmbH
000237	Cosmo Research Corp.
000238	Serome Technology, Inc.
000239	Visicom
00023A	ZSK Stickmaschinen GmbH
00023B	Ericsson
00023C	Creative Technology, Ltd.
00023D	Cisco Systems, Inc
00023E	Selta Telematica S.p.a
00023F	COMPAL ELECTRONICS, INC.
000240	Seedek Co., Ltd.
000241	Amer.com
000242	Videoframe Systems
000243	Raysis Co., Ltd.
000244	SURECOM Technology Co.
000245	Lampus Co, Ltd.
000246	All-Win Tech Co., Ltd.
000247	Great Dragon Information Technology (Group) Co., Ltd.
000248	Pilz GmbH & Co.
000249	Aviv Infocom Co, Ltd.
00024A	Cisco Systems, Inc
00024B	Cisco Systems, Inc
00024C	SiByte, Inc.
00024D	Mannesman Dematic Colby Pty. Ltd.
00024E	Datacard Group
00024F	IPM Datacom S.R.L.
000250	Geyser Networks, Inc.
000251	Soma Networks, Inc.
000252	Carrier Corporation
000253	Televideo, Inc.
000254	WorldGate
000255	IBM Corp
000256	Alpha Processor, Inc.
000257	Microcom Corp.
000258	Flying Packets Communications
000259	Tsann Kuen China (Shanghai)Enterprise Co., Ltd. IT Group
00025A	Catena Networks
00025B	Cambridge Silicon Radio
00025C	SCI Systems (Kunshan) Co., Ltd.
00025D	Calix Networks
00025E	High Technology Ltd
00025F	Nortel Networks
000260	Accordion Networks, Inc.
000261	Tilgin AB
000262	Soyo Group Soyo Com Tech Co., Ltd
000263	UPS Manufacturing SRL
000264	AudioRamp.com
000265	Virditech Co. Ltd.
000266	Thermalogic Corporation
000267	NODE RUNNER, INC.
000268	Harris Government Communications
000269	Nadatel Co., Ltd
00026A	Cocess Telecom Co., Ltd.
00026B	BCM Computers Co., Ltd.
00026C	Philips CFT
00026D	Adept Telecom
00026E	NeGeN Access, Inc.
00026F	Senao International Co., Ltd.
000270	Crewave Co., Ltd.
000271	Zhone Technologies
000272	CC&C Technologies, Inc.
000273	Coriolis Networks
000274	Tommy Technologies Corp.
000275	SMART Technologies, Inc.
000276	Primax Electronics Ltd.
000277	Cash Systemes Industrie
000278	SAMSUNG ELECTRO MECHANICS CO., LTD.
000279	Control Applications, Ltd.
00027A	IOI Technology Corporation
00027B	Amplify Net, Inc.
00027C	Trilithic, Inc.
00027D	Cisco Systems, Inc
00027E	Cisco Systems, Inc
00027F	ask-technologies.com
000280	Mu Net, Inc.
000281	Madge Ltd.
000282	ViaClix, Inc.
000283	Spectrum Controls, Inc.
000284	AREVA T&D
000285	Riverstone Networks
000286	Occam Networks
000287	Adapcom
000288	Global Village (PCcard in Mac portable)
000289	DNE Technologies
00028A	Ambit Microsystems Corporation
00028B	VDSL Systems OY
00028C	Micrel-Synergy Semiconductor
00028D	Movita Technologies, Inc.
00028E	Rapid 5 Networks, Inc.
00028F	Globetek, Inc.
000290	Woorigisool, Inc.
000291	Open Network Co., Ltd.
000292	Logic Innovations, Inc.
000293	Solid Data Systems
000294	Tokyo Sokushin Co., Ltd.
000295	IP.Access Limited
000296	Lectron Co,. Ltd.
000297	C-COR.net
000298	Broadframe Corporation
000299	Apex, Inc.
00029A	Storage Apps
00029B	Kreatel Communications AB
00029C	3com
00029D	Merix Corp.
00029E	Information Equipment Co., Ltd.
00029F	L-3 Communication Aviation Recorders
0002A0	Flatstack Ltd.
0002A1	World Wide Packets
0002A2	Hilscher GmbH
0002A3	ABB Switzerland Ltd, Power Systems
0002A4	AddPac Technology Co., Ltd.
0002A5	Hewlett Packard
0002A6	Effinet Systems Co., Ltd.
0002A7	Vivace Networks
0002A8	Air Link Technology
0002A9	RACOM, s.r.o.
0002AA	PLcom Co., Ltd.
0002AB	CTC Union Technologies Co., Ltd.
0002AC	3PAR data
0002AD	HOYA Corporation
0002AE	Scannex Electronics Ltd.
0002AF	TeleCruz Technology, Inc.
0002B0	Hokubu Communication & Industrial Co., Ltd.
0002B1	Anritsu, Ltd.
0002B2	Cablevision
0002B3	Intel Corporation
0002B4	Daphne
0002B5	Avnet, Inc.
0002B6	Acrosser Technology Co., Ltd.
0002B7	Watanabe Electric Industry Co., Ltd.
0002B8	WHI KONSULT AB
0002B9	Cisco Systems, Inc
0002BA	Cisco Systems, Inc
0002BB	Continuous Computing Corp
0002BC	LVL 7 Systems, Inc.
0002BD	Bionet Co., Ltd.
0002BE	Totsu Engineering, Inc.
0002BF	dotRocket, Inc.
0002C0	Bencent Tzeng Industry Co., Ltd.
0002C1	Innovative Electronic Designs, Inc.
0002C2	Net Vision Telecom
0002C3	Arelnet Ltd.
0002C4	Vector International BVBA
0002C5	Evertz Microsystems Ltd.
0002C6	Data Track Technology PLC
0002C7	ALPS ELECTRIC CO.,LTD.
0002C8	Technocom Communications Technology (pte) Ltd
0002C9	Mellanox Technologies, Inc.
0002CA	EndPoints, Inc.
0002CB	TriState Ltd.
0002CC	M.C.C.I
0002CD	TeleDream, Inc.
0002CE	FoxJet, Inc.
0002CF	ZyGate Communications, Inc.
0002D0	Comdial Corporation
0002D1	Vivotek, Inc.
0002D2	Workstation AG
0002D3	NetBotz, Inc.
0002D4	PDA Peripherals, Inc.
0002D5	Acr
0002D6	NICE Systems
0002D7	EMPEG Ltd
0002D8	BRECIS Communications Corporation
0002D9	Reliable Controls
0002DA	ExiO Communications, Inc.
0002DB	Netsec
0002DC	Fujitsu General Limited
0002DD	Bromax Communications, Ltd.
0002DE	Astrodesign, Inc.
0002DF	Net Com Systems, Inc.
0002E0	ETAS GmbH
0002E1	Integrated Network Corporation
0002E2	NDC Infared Engineering
0002E3	LITE-ON Communications, Inc.
0002E4	JC HYUN Systems, Inc.
0002E5	Timeware Ltd.
0002E6	Gould Instrument Systems, Inc.
0002E7	CAB GmbH & Co KG
0002E8	E.D.&A.
0002E9	CS Systemes De Securite - C3S
0002EA	Focus Enhancements
0002EB	Pico Communications
0002EC	Maschoff Design Engineering
0002ED	DXO Telecom Co., Ltd.
0002EE	Nokia Danmark A/S
0002EF	CCC Network Systems Group Ltd.
0002F0	AME Optimedia Technology Co., Ltd.
0002F1	Pinetron Co., Ltd.
0002F2	eDevice, Inc.
0002F3	Media Serve Co., Ltd.
0002F4	PCTEL, Inc.
0002F5	VIVE Synergies, Inc.
0002F6	Equipe Communications
0002F7	Arm
0002F8	SEAKR Engineering, Inc.
0002F9	MIMOS Berhad
0002FA	DX Antenna Co., Ltd.
0002FB	Baumuller Aulugen-Systemtechnik GmbH
0002FC	Cisco Systems, Inc
0002FD	Cisco Systems, Inc
0002FE	Viditec, Inc.
0002FF	Handan BroadInfoCom
000300	Barracuda Networks, Inc.
000301	Exfo
000302	Charles Industries, Ltd.
000303	JAMA Electronics Co., Ltd.
000304	Pacific Broadband Communications
000305	MSC Vertriebs GmbH
000306	Fusion In Tech Co., Ltd.
000307	Secure Works, Inc.
000308	AM Communications, Inc.
000309	Texcel Technology PLC
00030A	Argus Technologies
00030B	Hunter Technology, Inc.
00030C	Telesoft Technologies Ltd.
00030D	Uniwill Computer Corp.
00030E	Core Communications Co., Ltd.
00030F	Digital China (Shanghai) Networks Ltd.
000310	E-Globaledge Corporation
000311	Micro Technology Co., Ltd.
000312	TR-Systemtechnik GmbH
000313	Access Media SPA
000314	Teleware Network Systems
000315	Cidco Incorporated
000316	Nobell Communications, Inc.
000317	Merlin Systems, Inc.
000318	Cyras Systems, Inc.
000319	Infineon AG
00031A	Beijing Broad Telecom Ltd., China
00031B	Cellvision Systems, Inc.
00031C	Svenska Hardvarufabriken AB
00031D	Taiwan Commate Computer, Inc.
00031E	Optranet, Inc.
00031F	Condev Ltd.
000320	Xpeed, Inc.
000321	Reco Research Co., Ltd.
000322	IDIS Co., Ltd.
000323	Cornet Technology, Inc.
000324	SANYO Consumer Electronics Co., Ltd.
000325	Arima Computer Corp.
000326	Iwasaki Information Systems Co., Ltd.
000327	ACT'L
000328	Mace Group, Inc.
000329	F3, Inc.
00032A	UniData Communication Systems, Inc.
00032B	GAI Datenfunksysteme GmbH
00032C	ABB Switzerland Ltd
00032D	IBASE Technology, Inc.
00032E	Scope Information Management, Ltd.
00032F	Global Sun Technology, Inc.
000330	Imagenics, Co., Ltd.
000331	Cisco Systems, Inc
000332	Cisco Systems, Inc
000333	Digitel Co., Ltd.
000334	Newport Electronics
000335	Mirae Technology
000336	Zetes Technologies
000337	Vaone, Inc.
000338	Oak Technology
000339	Eurologic Systems, Ltd.
00033A	Silicon Wave, Inc.
00033B	TAMI Tech Co., Ltd.
00033C	Daiden Co., Ltd.
00033D	ILSHin Lab
00033E	Tateyama System Laboratory Co., Ltd.
00033F	BigBand Networks, Ltd.
000340	Floware Wireless Systems, Ltd.
000341	Axon Digital Design
000342	Nortel Networks
000343	Martin Professional A/S
000344	Tietech.Co., Ltd.
000345	Routrek Networks Corporation
000346	Hitachi Kokusai Electric, Inc.
000347	Intel Corporation
000348	Norscan Instruments, Ltd.
000349	Vidicode Datacommunicatie B.V.
00034A	RIAS Corporation
00034B	Nortel Networks
00034C	Shanghai DigiVision Technology Co., Ltd.
00034D	Chiaro Networks, Ltd.
00034E	Pos Data Company, Ltd.
00034F	Sur-Gard Security
000350	BTICINO SPA
000351	Diebold, Inc.
000352	Colubris Networks
000353	Mitac, Inc.
000354	Fiber Logic Communications
000355	TeraBeam Internet Systems
000356	Wincor Nixdorf International GmbH
000357	Intervoice-Brite, Inc.
000358	Hanyang Digitech Co.Ltd
000359	DigitalSis
00035A	Photron Limited
00035B	BridgeWave Communications
00035C	Saint Song Corp.
00035D	Bosung Hi-Net Co., Ltd.
00035E	Metropolitan Area Networks, Inc.
00035F	Prüftechnik Condition Monitoring GmbH & Co. KG
000360	PAC Interactive Technology, Inc.
000361	Widcomm, Inc.
000362	Vodtel Communications, Inc.
000363	Miraesys Co., Ltd.
000364	Scenix Semiconductor, Inc.
000365	Kira Information & Communications, Ltd.
000366	ASM Pacific Technology
000367	Jasmine Networks, Inc.
000368	Embedone Co., Ltd.
000369	Nippon Antenna Co., Ltd.
00036A	Mainnet, Ltd.
00036B	Cisco Systems, Inc
00036C	Cisco Systems, Inc
00036D	Runtop, Inc.
00036E	Nicon Systems (Pty) Limited
00036F	Telsey SPA
000370	NXTV, Inc.
000371	Acomz Networks Corp.
000372	Ulan
000373	Aselsan A.S
000374	Control Microsystems
000375	NetMedia, Inc.
000376	Graphtec Technology, Inc.
000377	Gigabit Wireless
000378	HUMAX Co., Ltd.
000379	Proscend Communications, Inc.
00037A	Taiyo Yuden Co., Ltd.
00037B	IDEC IZUMI Corporation
00037C	Coax Media
00037D	Stellcom
00037E	PORTech Communications, Inc.
00037F	Atheros Communications, Inc.
000380	SSH Communications Security Corp.
000381	Ingenico International
000382	A-One Co., Ltd.
000383	Metera Networks, Inc.
000384	Aeta
000385	Actelis Networks, Inc.
000386	Ho Net, Inc.
000387	Blaze Network Products
000388	Fastfame Technology Co., Ltd.
000389	PLANTRONICS, INC.
00038A	America Online, Inc.
00038B	PLUS-ONE I&T, Inc.
00038C	Total Impact
00038D	PCS Revenue Control Systems, Inc.
00038E	Atoga Systems, Inc.
00038F	Weinschel Corporation
000390	Digital Video Communications, Inc.
000391	Advanced Digital Broadcast, Ltd.
000392	Hyundai Teletek Co., Ltd.
000393	Apple, Inc.
000394	Connect One
000395	California Amplifier
000396	EZ Cast Co., Ltd.
000397	Watchfront Limited
000398	Wisi
000399	Dongju Informations & Communications Co., Ltd.
00039A	SiConnect
00039B	NetChip Technology, Inc.
00039C	OptiMight Communications, Inc.
00039D	Qisda Corporation
00039E	Tera System Co., Ltd.
00039F	Cisco Systems, Inc
0003A0	Cisco Systems, Inc
0003A1	HIPER Information & Communication, Inc.
0003A2	Catapult Communications
0003A3	MAVIX, Ltd.
0003A4	Imation Corp.
0003A5	Medea Corporation
0003A6	Traxit Technology, Inc.
0003A7	Unixtar Technology, Inc.
0003A8	IDOT Computers, Inc.
0003A9	AXCENT Media AG
0003AA	Watlow
0003AB	Bridge Information Systems
0003AC	Fronius Schweissmaschinen
0003AD	Emerson Energy Systems AB
0003AE	Allied Advanced Manufacturing Pte, Ltd.
0003AF	Paragea Communications
0003B0	Xsense Technology Corp.
0003B1	Hospira Inc.
0003B2	Radware
0003B3	IA Link Systems Co., Ltd.
0003B4	Macrotek International Corp.
0003B5	Entra Technology Co.
0003B6	QSI Corporation
0003B7	ZACCESS Systems
0003B8	NetKit Solutions, LLC
0003B9	Hualong Telecom Co., Ltd.
0003BA	Oracle Corporation
0003BB	Signal Communications Limited
0003BC	COT GmbH
0003BD	OmniCluster Technologies, Inc.
0003BE	Netility
0003BF	Centerpoint Broadband Technologies, Inc.
0003C0	RFTNC Co., Ltd.
0003C1	Packet Dynamics Ltd
0003C2	Solphone K.K.
0003C3	Micronik Multimedia
0003C4	Tomra Systems ASA
0003C5	Mobotix AG
0003C6	Morning Star Technologies Inc
0003C7	hopf Elektronik GmbH
0003C8	CML Emergency Services
0003C9	TECOM Co., Ltd.
0003CA	MTS Systems Corp.
0003CB	Nippon Systems Development Co., Ltd.
0003CC	Momentum Computer, Inc.
0003CD	Clovertech, Inc.
0003CE	ETEN Technologies, Inc.
0003CF	Muxcom, Inc.
0003D0	KOANKEISO Co., Ltd.
0003D1	Takaya Corporation
0003D2	Crossbeam Systems, Inc.
0003D3	Internet Energy Systems, Inc.
0003D4	Alloptic, Inc.
0003D5	Advanced Communications Co., Ltd.
0003D6	RADVision, Ltd.
0003D7	NextNet Wireless, Inc.
0003D8	iMPath Networks, Inc.
0003D9	Secheron SA
0003DA	Takamisawa Cybernetics Co., Ltd.
0003DB	Apogee Electronics Corp.
0003DC	Lexar Media, Inc.
0003DD	Comark Interactive Solutions
0003DE	OTC Wireless
0003DF	Desana Systems
0003E0	ARRIS Group, Inc.
0003E1	Winmate Communication, Inc.
0003E2	Comspace Corporation
0003E3	Cisco Systems, Inc
0003E4	Cisco Systems, Inc
0003E5	Hermstedt SG
0003E6	Entone, Inc.
0003E7	Logostek Co. Ltd.
0003E8	Wavelength Digital Limited
0003E9	Akara Canada, Inc.
0003EA	Mega System Technologies, Inc.
0003EB	Atrica
0003EC	ICG Research, Inc.
0003ED	Shinkawa Electric Co., Ltd.
0003EE	MKNet Corporation
0003EF	Oneline AG
0003F0	Redfern Broadband Networks
0003F1	Cicada Semiconductor, Inc.
0003F2	Seneca Networks
0003F3	Dazzle Multimedia, Inc.
0003F4	NetBurner
0003F5	Chip2Chip
0003F6	Allegro Networks, Inc.
0003F7	Plast-Control GmbH
0003F8	SanCastle Technologies, Inc.
0003F9	Pleiades Communications, Inc.
0003FA	TiMetra Networks
0003FB	ENEGATE Co.,Ltd.
0003FC	Intertex Data AB
0003FD	Cisco Systems, Inc
0003FE	Cisco Systems, Inc
0003FF	Microsoft Corporation
000400	Lexmark (Print Server)
000401	Osaki Electric Co., Ltd.
000402	Nexsan Technologies, Ltd.
000403	Nexsi Corporation
000404	Makino Milling Machine Co., Ltd.
000405	ACN Technologies
000406	Fa. Metabox AG
000407	Topcon Positioning Systems, Inc.
000408	Sanko Electronics Co., Ltd.
000409	Cratos Networks
00040A	Sage Systems
00040B	3COM EUROPE LTD.
00040C	Kanno Works, Ltd.
00040D	Avaya Inc
00040E	AVM GmbH
00040F	Asus Network Technologies, Inc.
000410	Spinnaker Networks, Inc.
000411	Inkra Networks, Inc.
000412	WaveSmith Networks, Inc.
000413	SNOM Technology AG
000414	Umezawa Musen Denki Co., Ltd.
000415	Rasteme Systems Co., Ltd.
000416	Parks S/A Comunicacoes Digitais
000417	ELAU AG
000418	Teltronic S.A.U.
000419	Fibercycle Networks, Inc.
00041A	Ines Test and Measurement GmbH & CoKG
00041B	Bridgeworks Ltd.
00041C	ipDialog, Inc.
00041D	Corega of America
00041E	Shikoku Instrumentation Co., Ltd.
00041F	Sony Interactive Entertainment Inc.
000420	Slim Devices, Inc.
000421	Ocular Networks
000422	Studio Technologies, Inc
000423	Intel Corporation
000424	TMC s.r.l.
000425	Atmel Corporation
000426	Autosys
000427	Cisco Systems, Inc
000428	Cisco Systems, Inc
000429	Pixord Corporation
00042A	Wireless Networks, Inc.
00042B	IT Access Co., Ltd.
00042C	Minet, Inc.
00042D	Sarian Systems, Ltd.
00042E	Netous Technologies, Ltd.
00042F	International Communications Products, Inc.
000430	Netgem
000431	GlobalStreams, Inc.
000432	Voyetra Turtle Beach, Inc.
000433	Cyberboard A/S
000434	Accelent Systems, Inc.
000435	InfiNet LLC
000436	ELANsat Technologies, Inc.
000437	Powin Information Technology, Inc.
000438	Nortel Networks
000439	Rosco Entertainment Technology, Inc.
00043A	Intelligent Telecommunications, Inc.
00043B	Lava Computer Mfg., Inc.
00043C	SONOS Co., Ltd.
00043D	INDEL AG
00043E	Telencomm
00043F	ESTeem Wireless Modems, Inc
000440	cyberPIXIE, Inc.
000441	Half Dome Systems, Inc.
000442	Nact
000443	Agilent Technologies, Inc.
000444	Western Multiplex Corporation
000445	LMS Skalar Instruments GmbH
000446	CYZENTECH Co., Ltd.
000447	Acrowave Systems Co., Ltd.
000448	Polaroid Corporation
000449	Mapletree Networks
00044A	iPolicy Networks, Inc.
00044B	Nvidia
00044C	Jenoptik
00044D	Cisco Systems, Inc
00044E	Cisco Systems, Inc
00044F	Schubert System Elektronik Gmbh
000450	DMD Computers SRL
000451	Medrad, Inc.
000452	RocketLogix, Inc.
000453	YottaYotta, Inc.
000454	Quadriga UK
000455	ANTARA.net
000456	Cambium Networks Limited
000457	Universal Access Technology, Inc.
000458	Fusion X Co., Ltd.
000459	Veristar Corporation
00045A	The Linksys Group, Inc.
00045B	Techsan Electronics Co., Ltd.
00045C	Mobiwave Pte Ltd
00045D	BEKA Elektronik
00045E	PolyTrax Information Technology AG
00045F	Avalue Technology, Inc.
000460	Knilink Technology, Inc.
000461	EPOX Computer Co., Ltd.
000462	DAKOS Data & Communication Co., Ltd.
000463	Bosch Security Systems
000464	Pulse-Link Inc
000465	ISTIsdn-               # i.s.t isdn-support technik GmbH
000466	ARMITEL Co.
000467	Wuhan Research Institute of MII
000468	Vivity, Inc.
000469	Innocom, Inc.
00046A	Navini Networks
00046B	Palm Wireless, Inc.
00046C	Cyber Technology Co., Ltd.
00046D	Cisco Systems, Inc
00046E	Cisco Systems, Inc
00046F	Digitel S/A Industria Eletronica
000470	ipUnplugged AB
000471	Iprad
000472	Telelynx, Inc.
000473	Photonex Corporation
000474	Legrand
000475	3 Com Corporation
000476	3 Com Corporation
000477	Scalant Systems, Inc.
000478	G. Star Technology Corporation
000479	Radius Co., Ltd.
00047A	AXXESSIT ASA
00047B	Schlumberger
00047C	Skidata AG
00047D	Pelco
00047E	Siqura B.V.
00047F	Chr. Mayr GmbH & Co. KG
000480	Brocade Communications Systems, Inc.
000481	Econolite Control Products, Inc.
000482	Medialogic Corp.
000483	Deltron Technology, Inc.
000484	Amann GmbH
000485	PicoLight
000486	ITTC, University of Kansas
000487	Cogency Semiconductor, Inc.
000488	Eurotherm Controls
000489	YAFO Networks, Inc.
00048A	Temia Vertriebs GmbH
00048B	Poscon Corporation
00048C	Nayna Networks, Inc.
00048D	Teo Technologies, Inc
00048E	Ohm Tech Labs, Inc.
00048F	TD Systems Corporation
000490	Optical Access
000491	Technovision, Inc.
000492	Hive Internet, Ltd.
000493	Tsinghua Unisplendour Co., Ltd.
000494	Breezecom, Ltd.
000495	Tejas Networks India Limited
000496	Extreme Networks
000497	MacroSystem Digital Video AG
000498	Mahi Networks
000499	Chino Corporation
00049A	Cisco Systems, Inc
00049B	Cisco Systems, Inc
00049C	Surgient Networks, Inc.
00049D	Ipanema Technologies
00049E	Wirelink Co., Ltd.
00049F	Freescale Semiconductor
0004A0	Verity Instruments, Inc.
0004A1	Pathway Connectivity
0004A2	L.S.I. Japan Co., Ltd.
0004A3	Microchip Technology Inc.
0004A4	NetEnabled, Inc.
0004A5	Barco Projection Systems NV
0004A6	SAF Tehnika Ltd.
0004A7	FabiaTech Corporation
0004A8	Broadmax Technologies, Inc.
0004A9	SandStream Technologies, Inc.
0004AA	Jetstream Communications
0004AB	Comverse Network Systems, Inc.
0004AC	IBM				PCMCIA Ethernet adapter.
0004AD	Malibu Networks
0004AE	Sullair Corporation
0004AF	Digital Fountain, Inc.
0004B0	ELESIGN Co., Ltd.
0004B1	Signal Technology, Inc.
0004B2	ESSEGI SRL
0004B3	Videotek, Inc.
0004B4	Ciac
0004B5	Equitrac Corporation
0004B6	Stratex Networks, Inc.
0004B7	AMB i.t. Holding
0004B8	Kumahira Co., Ltd.
0004B9	S.I. Soubou, Inc.
0004BA	KDD Media Will Corporation
0004BB	Bardac Corporation
0004BC	Giantec, Inc.
0004BD	ARRIS Group, Inc.
0004BE	OptXCon, Inc.
0004BF	VersaLogic Corp.
0004C0	Cisco Systems, Inc
0004C1	Cisco Systems, Inc
0004C2	Magnipix, Inc.
0004C3	CASTOR Informatique
0004C4	Allen & Heath Limited
0004C5	ASE Technologies, USA
0004C6	YAMAHA MOTOR CO.,LTD
0004C7	Netmount
0004C8	LIBA Maschinenfabrik GmbH
0004C9	Micro Electron Co., Ltd.
0004CA	FreeMs Corp.
0004CB	Tdsoft Communication, Ltd.
0004CC	Peek Traffic B.V.
0004CD	Extenway Solutions Inc
0004CE	Patria Ailon
0004CF	Seagate Technology
0004D0	Softlink s.r.o.
0004D1	Drew Technologies, Inc.
0004D2	Adcon Telemetry GmbH
0004D3	Toyokeiki Co., Ltd.
0004D4	Proview Electronics Co., Ltd.
0004D5	Hitachi Information & Communication Engineering, Ltd.
0004D6	Takagi Industrial Co., Ltd.
0004D7	Omitec Instrumentation Ltd.
0004D8	IPWireless, Inc.
0004D9	Titan Electronics, Inc.
0004DA	Relax Technology, Inc.
0004DB	Tellus Group Corp.
0004DC	Nortel Networks
0004DD	Cisco Systems, Inc
0004DE	Cisco Systems, Inc
0004DF	Teracom Telematica Ltda.
0004E0	Procket Networks
0004E1	Infinior Microsystems
0004E2	SMC Networks, Inc.
0004E3	Accton Technology Corp
0004E4	Daeryung Ind., Inc.
0004E5	Glonet Systems, Inc.
0004E6	Banyan Network Private Limited
0004E7	Lightpointe Communications, Inc
0004E8	IER, Inc.
0004E9	Infiniswitch Corporation
0004EA	Hewlett Packard
0004EB	Paxonet Communications, Inc.
0004EC	Memobox SA
0004ED	Billion Electric Co., Ltd.
0004EE	Lincoln Electric Company
0004EF	Polestar Corp.
0004F0	International Computers, Ltd
0004F1	Wherenet
0004F2	Polycom
0004F3	FsForth-               # FS FORTH-SYSTEME GmbH
0004F4	Infinite Electronics Inc.
0004F5	SnowShore Networks, Inc.
0004F6	Amphus
0004F7	Omega Band, Inc.
0004F8	QUALICABLE TV Industria E Com., Ltda
0004F9	Xtera Communications, Inc.
0004FA	NBS Technologies Inc.
0004FB	Commtech, Inc.
0004FC	Stratus Computer (DE), Inc.
0004FD	Japan Control Engineering Co., Ltd.
0004FE	Pelago Networks
0004FF	Acronet Co., Ltd.
000500	Cisco Systems, Inc
000501	Cisco Systems, Inc
000502	Apple (PCI bus Macs)
000503	Iconag
000504	Naray Information & Communication Enterprise
000505	Systems Integration Solutions, Inc.
000506	Reddo Networks AB
000507	Fine Appliance Corp.
000508	Inetcam, Inc.
000509	AVOC Nishimura Ltd.
00050A	ICS Spa
00050B	SICOM Systems, Inc.
00050C	Network Photonics, Inc.
00050D	Midstream Technologies, Inc.
00050E	3ware, Inc.
00050F	TanakaS/               # Tanaka S/S Ltd.
000510	Infinite Shanghai Communication Terminals Ltd.
000511	Complementary Technologies Ltd
000512	Zebra Technologies Inc
000513	VTLinx Multimedia Systems, Inc.
000514	KDT Systems Co., Ltd.
000515	Nuark Co., Ltd.
000516	SMART Modular Technologies
000517	Shellcomm, Inc.
000518	Jupiters Technology
000519	Siemens Building Technologies AG,
00051A	3COM EUROPE LTD.
00051B	Magic Control Technology Corporation
00051C	Xnet Technology Corp.
00051D	Airocon, Inc.
00051E	Brocade Communications Systems, Inc.
00051F	Taijin Media Co., Ltd.
000520	Smartronix, Inc.
000521	Control Microsystems
000522	LEA*D Corporation, Inc.
000523	AVL List GmbH
000524	BTL System (HK) Limited
000525	Puretek Industrial Co., Ltd.
000526	IPAS GmbH
000527	SJ Tek Co. Ltd
000528	New Focus, Inc.
000529	Shanghai Broadan Communication Technology Co., Ltd
00052A	Ikegami Tsushinki Co., Ltd.
00052B	HORIBA, Ltd.
00052C	Supreme Magic Corporation
00052D	Zoltrix International Limited
00052E	Cinta Networks
00052F	Leviton Network Solutions
000530	Andiamo Systems, Inc.
000531	Cisco Systems, Inc
000532	Cisco Systems, Inc
000533	Brocade Communications Systems, Inc.
000534	Northstar Engineering Ltd.
000535	Chip PC Ltd.
000536	Danam Communications, Inc.
000537	Nets Technology Co., Ltd.
000538	Merilus, Inc.
000539	A Brand New World in Sweden AB
00053A	Willowglen Services Pte Ltd
00053B	Harbour Networks Ltd., Co. Beijing
00053C	Xircom
00053D	Agere Systems
00053E	KID Systeme GmbH
00053F	VisionTek, Inc.
000540	FAST Corporation
000541	Advanced Systems Co., Ltd.
000542	Otari, Inc.
000543	IQ Wireless GmbH
000544	Valley Technologies, Inc.
000545	Internet Photonics
000546	KDDI Network & Solultions Inc.
000547	Starent Networks
000548	Disco Corporation
000549	Salira Optical Network Systems
00054A	Ario Data Networks, Inc.
00054B	Eaton Automation AG
00054C	RF Innovations Pty Ltd
00054D	Brans Technologies, Inc.
00054E	Philips
00054F	Private
000550	Vcomms Connect Limited
000551	F & S Elektronik Systeme GmbH
000552	Xycotec Computer GmbH
000553	DVC Company, Inc.
000554	Rangestar Wireless
000555	Japan Cash Machine Co., Ltd.
000556	360 Systems
000557	Agile TV Corporation
000558	Synchronous, Inc.
000559	Intracom S.A.
00055A	Power Dsine Ltd.
00055B	Charles Industries, Ltd.
00055C	Kowa Company, Ltd.
00055D	D-LINK SYSTEMS, INC.
00055E	Cisco Systems, Inc
00055F	Cisco Systems, Inc
000560	LEADER COMM.CO., LTD
000561	nac Image Technology, Inc.
000562	Digital View Limited
000563	J-Works, Inc.
000564	Tsinghua Bitway Co., Ltd.
000565	Tailyn Communication Company Ltd.
000566	Secui.com Corporation
000567	Etymonic Design, Inc.
000568	Piltofish Networks AB
000569	VMware, Inc.
00056A	Heuft Systemtechnik GmbH
00056B	C.P. Technology Co., Ltd.
00056C	Hung Chang Co., Ltd.
00056D	Pacific Corporation
00056E	National Enhance Technology, Inc.
00056F	Innomedia Technologies Pvt. Ltd.
000570	Baydel Ltd.
000571	Seiwa Electronics Co.
000572	Deonet Co., Ltd.
000573	Cisco Systems, Inc
000574	Cisco Systems, Inc
000575	CDS-Electronics BV
000576	NSM Technology Ltd.
000577	SM Information & Communication
000578	Private
000579	Universal Control Solution Corp.
00057A	Overture Networks
00057B	Chung Nam Electronic Co., Ltd.
00057C	RCO Security AB
00057D	Sun Communications, Inc.
00057E	Eckelmann Steuerungstechnik GmbH
00057F	Acqis Technology
000580	FibroLAN Ltd.
000581	Snell
000582	ClearCube Technology
000583	ImageCom Limited
000584	AbsoluteValue Systems, Inc.
000585	Juniper Networks
000586	Lucent Technologies
000587	Locus, Incorporated
000588	Sensoria Corp.
000589	National Datacomputer
00058A	Netcom Co., Ltd.
00058B	IPmental, Inc.
00058C	Opentech Inc.
00058D	Lynx Photonic Networks, Inc.
00058E	Flextronics International GmbH & Co. Nfg. KG
00058F	CLCsoft co.
000590	Swissvoice Ltd.
000591	Active Silicon Ltd
000592	Pultek Corp.
000593	Grammar Engine Inc.
000594	HMS Industrial Networks
000595	Alesis Corporation
000596	Genotech Co., Ltd.
000597	Eagle Traffic Control Systems
000598	CRONOS S.r.l.
000599	DRS Test and Energy Management or DRS-TEM
00059A	PowerComputing (Mac clone)
00059B	Cisco Systems, Inc
00059C	Kleinknecht GmbH, Ing. Büro
00059D	Daniel Computing Systems, Inc.
00059E	Zinwell Corporation
00059F	Yotta Networks, Inc.
0005A0	MOBILINE Kft.
0005A1	Zenocom
0005A2	CELOX Networks
0005A3	QEI, Inc.
0005A4	Lucid Voice Ltd.
0005A5	Kott
0005A6	Extron Electronics
0005A7	Hyperchip, Inc.
0005A8	PowerComputing			Mac clones
0005A9	Princeton Networks, Inc.
0005AA	Moore Industries International Inc.
0005AB	Cyber Fone, Inc.
0005AC	Northern Digital, Inc.
0005AD	Topspin Communications, Inc.
0005AE	Mediaport USA
0005AF	InnoScan Computing A/S
0005B0	Korea Computer Technology Co., Ltd.
0005B1	ASB Technology BV
0005B2	Medison Co., Ltd.
0005B3	Asahi-Engineering Co., Ltd.
0005B4	Aceex Corporation
0005B5	Broadcom Technologies
0005B6	INSYS Microelectronics GmbH
0005B7	Arbor Technology Corp.
0005B8	Electronic Design Associates, Inc.
0005B9	Airvana, Inc.
0005BA	Area Netwoeks, Inc.
0005BB	Myspace AB
0005BC	Resource Data Management Ltd
0005BD	ROAX BV
0005BE	Kongsberg Seatex AS
0005BF	JustEzy Technology, Inc.
0005C0	Digital Network Alacarte Co., Ltd.
0005C1	A-Kyung Motion, Inc.
0005C2	Soronti, Inc.
0005C3	Pacific Instruments, Inc.
0005C4	Telect, Inc.
0005C5	Flaga HF
0005C6	Triz Communications
0005C7	I/F-COM A/S
0005C8	Verytech
0005C9	LG Innotek Co., Ltd.
0005CA	Hitron Technology, Inc.
0005CB	ROIS Technologies, Inc.
0005CC	Sumtel Communications, Inc.
0005CD	D&M Holdings Inc.
0005CE	Prolink Microsystems Corporation
0005CF	Thunder River Technologies, Inc.
0005D0	Solinet Systems
0005D1	Metavector Technologies
0005D2	DAP Technologies
0005D3	eProduction Solutions, Inc.
0005D4	FutureSmart Networks, Inc.
0005D5	Speedcom Wireless
0005D6	L-3 Linkabit
0005D7	Vista Imaging, Inc.
0005D8	Arescom, Inc.
0005D9	Techno Valley, Inc.
0005DA	Apex Automationstechnik
0005DB	PSI Nentec GmbH
0005DC	Cisco Systems, Inc
0005DD	Cisco Systems, Inc
0005DE	Gi Fone Korea, Inc.
0005DF	Electronic Innovation, Inc.
0005E0	Empirix Corp.
0005E1	Trellis Photonics, Ltd.
0005E2	Creativ Network Technologies
0005E3	LightSand Communications, Inc.
0005E4	Red Lion Controls Inc.
0005E5	Renishaw PLC
0005E6	Egenera, Inc.
0005E7	Netrake an AudioCodes Company
0005E8	TurboWave, Inc.
0005E9	Unicess Network, Inc.
0005EA	Rednix
0005EB	Blue Ridge Networks, Inc.
0005EC	Mosaic Systems Inc.
0005ED	Technikum Joanneum GmbH
0005EE	Vanderbilt International (SWE) AB
0005EF	ADOIR Digital Technology
0005F0	Satec
0005F1	Vrcom, Inc.
0005F2	Power R, Inc.
0005F3	Webyn
0005F4	System Base Co., Ltd.
0005F5	Geospace Technologies
0005F6	Young Chang Co. Ltd.
0005F7	Analog Devices, Inc.
0005F8	Real Time Access, Inc.
0005F9	TOA Corporation
0005FA	IPOptical, Inc.
0005FB	ShareGate, Inc.
0005FC	Schenck Pegasus Corp.
0005FD	PacketLight Networks Ltd.
0005FE	Traficon N.V.
0005FF	SNS Solutions, Inc.
000600	Toshiba Teli Corporation
000601	Otanikeiki Co., Ltd.
000602	Cirkitech Electronics Co.
000603	Baker Hughes Inc.
000604	@Track Communications, Inc.
000605	Inncom International, Inc.
000606	RapidWAN, Inc.
000607	Omni Directional Control Technology Inc.
000608	At-Sky SAS
000609	Crossport Systems
00060A	Blue2space
00060B	Artesyn Embedded Technologies
00060C	Melco Industries, Inc.
00060D	Hewlett-	# Hewlett-Packard			JetDirect token-ring interfaces
00060E	IGYS Systems, Inc.
00060F	Narad Networks Inc
000610	Abeona Networks Inc
000611	Zeus Wireless, Inc.
000612	Accusys, Inc.
000613	Kawasaki Microelectronics Incorporated
000614	Prism Holdings
000615	Kimoto Electric Co., Ltd.
000616	Tel Net Co., Ltd.
000617	Redswitch Inc.
000618	DigiPower Manufacturing Inc.
000619	Connection Technology Systems
00061A	Zetari Inc.
00061B	Notebook Development Lab.  Lenovo Japan Ltd.
00061C	Hoshino Metal Industries, Ltd.
00061D	MIP Telecom, Inc.
00061E	Maxan Systems
00061F	Vision Components GmbH
000620	Serial System Ltd.
000621	Hinox, Co., Ltd.
000622	Chung Fu Chen Yeh Enterprise Corp.
000623	MGE UPS Systems France
000624	Gentner Communications Corp.
000625	The Linksys Group, Inc.
000626	MWE GmbH
000627	Uniwide Technologies, Inc.
000628	Cisco Systems, Inc
000629	IBM RISC6000 system
00062A	Cisco Systems, Inc
00062B	INTRASERVER TECHNOLOGY
00062C	Bivio Networks
00062D	TouchStar Technologies, L.L.C.
00062E	Aristos Logic Corp.
00062F	Pivotech Systems Inc.
000630	Adtranz Sweden
000631	Calix Inc.
000632	Mesco Engineering GmbH
000633	Cross Match Technologies GmbH
000634	GTE Airfone Inc.
000635	PacketAir Networks, Inc.
000636	Jedai Broadband Networks
000637	Toptrend-Meta Information (ShenZhen) Inc.
000638	Sungjin C&C Co., Ltd.
000639	Newtec
00063A	Dura Micro, Inc.
00063B	Arcturus Networks Inc.
00063C	Intrinsyc Software International Inc.
00063D	Microwave Data Systems Inc.
00063E	Opthos Inc.
00063F	Everex Communications Inc.
000640	White Rock Networks
000641	Itcn
000642	Genetel Systems Inc.
000643	SONO Computer Co., Ltd.
000644	neix,Inc
000645	Meisei Electric Co. Ltd.
000646	ShenZhen XunBao Network Technology Co Ltd
000647	Etrali S.A.
000648	Seedsware, Inc.
000649	3M Deutschland GmbH
00064A	Honeywell Co., Ltd. (KOREA)
00064B	Alexon Co., Ltd.
00064C	Invicta Networks, Inc.
00064D	Sencore
00064E	Broad Net Technology Inc.
00064F	PRO-NETS Technology Corporation
000650	Tiburon Networks, Inc.
000651	Aspen Networks Inc.
000652	Cisco Systems, Inc
000653	Cisco Systems, Inc
000654	Winpresa Building Automation Technologies GmbH
000655	Yipee, Inc.
000656	Tactel AB
000657	Market Central, Inc.
000658	Helmut Fischer GmbH Institut für Elektronik und Messtechnik
000659	EAL (Apeldoorn) B.V.
00065A	Strix Systems
00065B	Dell Inc.
00065C	Malachite Technologies, Inc.
00065D	Heidelberg Web Systems
00065E	Photuris, Inc.
00065F	ECI Telecom Ltd.
000660	NADEX Co., Ltd.
000661	NIA Home Technologies Corp.
000662	MBM Technology Ltd.
000663	Human Technology Co., Ltd.
000664	Fostex Corporation
000665	Sunny Giken, Inc.
000666	Roving Networks
000667	Tripp Lite
000668	Vicon Industries Inc.
000669	Datasound Laboratories Ltd
00066A	InfiniCon Systems, Inc.
00066B	Sysmex Corporation
00066C	Robinson Corporation
00066D	Compuprint S.P.A.
00066E	Delta Electronics, Inc.
00066F	Korea Data Systems
000670	Upponetti Oy
000671	Softing AG
000672	Netezza
000673	TKH Security Solutions USA
000674	Spectrum Control, Inc.
000675	Banderacom, Inc.
000676	Novra Technologies Inc.
000677	SICK AG
000678	D&M Holdings Inc.
000679	Konami Corporation
00067A	JMP Systems
00067B	Toplink C&C Corporation
00067C	Cisco
00067D	Takasago Ltd.
00067E	WinCom Systems, Inc.
00067F	Digeo, Inc.
000680	Card Access, Inc.
000681	Goepel Electronic GmbH
000682	Convedia
000683	Bravara Communications, Inc.
000684	Biacore AB
000685	NetNearU Corporation
000686	ZARDCOM Co., Ltd.
000687	Omnitron Systems Technology, Inc.
000688	Telways Communication Co., Ltd.
000689	yLez Technologies Pte Ltd
00068A	NeuronNet Co. Ltd. R&D Center
00068B	AirRunner Technologies, Inc.
00068C	3COM CORPORATION
00068D	SEPATON, Inc.
00068E	HID Corporation
00068F	Telemonitor, Inc.
000690	Euracom Communication GmbH
000691	PT Inovacao
000692	Intruvert Networks, Inc.
000693	Flexus Computer Technology, Inc.
000694	Mobillian Corporation
000695	Ensure Technologies, Inc.
000696	Advent Networks
000697	R & D Center
000698	egnite GmbH
000699	Vida Design Co.
00069A	e & Tel
00069B	AVT Audio Video Technologies GmbH
00069C	Transmode Systems AB
00069D	Petards Ltd
00069E	UNIQA, Inc.
00069F	Kuokoa Networks
0006A0	Mx Imaging
0006A1	Celsian Technologies, Inc.
0006A2	Microtune, Inc.
0006A3	Bitran Corporation
0006A4	INNOWELL Corp.
0006A5	PINON Corp.
0006A6	Artistic Licence Engineering Ltd
0006A7	Primarion
0006A8	KC Technology, Inc.
0006A9	Universal Instruments Corp.
0006AA	VT Miltope
0006AB	W-Link Systems, Inc.
0006AC	Intersoft Co.
0006AD	KB Electronics Ltd.
0006AE	Himachal Futuristic Communications Ltd
0006AF	Xalted Networks
0006B0	Comtech EF Data Corp.
0006B1	Sonicwall
0006B2	Linxtek Co.
0006B3	Diagraph Corporation
0006B4	Vorne Industries, Inc.
0006B5	Source Photonics, Inc.
0006B6	Nir-Or Israel Ltd.
0006B7	TELEM GmbH
0006B8	Bandspeed Pty Ltd
0006B9	A5TEK Corp.
0006BA	Westwave Communications
0006BB	ATI Technologies Inc.
0006BC	Macrolink, Inc.
0006BD	BNTECHNOLOGY Co., Ltd.
0006BE	Baumer Optronic GmbH
0006BF	Accella Technologies Co., Ltd.
0006C0	United Internetworks, Inc.
0006C1	Cisco
0006C2	Smartmatic Corporation
0006C3	Schindler Elevator Ltd.
0006C4	Piolink Inc.
0006C5	INNOVI Technologies Limited
0006C6	lesswire AG
0006C7	RFNET Technologies Pte Ltd (S)
0006C8	Sumitomo Metal Micro Devices, Inc.
0006C9	Technical Marketing Research, Inc.
0006CA	American Computer & Digital Components, Inc. (ACDC)
0006CB	Jotron Electronics A/S
0006CC	JMI Electronics Co., Ltd.
0006CD	Leaf Imaging Ltd.
0006CE	Dateno
0006CF	Thales Avionics In-Flight Systems, LLC
0006D0	Elgar Electronics Corp.
0006D1	Tahoe Networks, Inc.
0006D2	Tundra Semiconductor Corp.
0006D3	Alpha Telecom, Inc. U.S.A.
0006D4	Interactive Objects, Inc.
0006D5	Diamond Systems Corp.
0006D6	Cisco Systems, Inc
0006D7	Cisco Systems, Inc
0006D8	Maple Optical Systems
0006D9	IPM-Net S.p.A.
0006DA	ITRAN Communications Ltd.
0006DB	ICHIPS Co., Ltd.
0006DC	Syabas Technology (Amquest)
0006DD	AT & T Laboratories - Cambridge Ltd
0006DE	Flash Technology
0006DF	AIDONIC Corporation
0006E0	MAT Co., Ltd.
0006E1	Techno Trade s.a
0006E2	Ceemax Technology Co., Ltd.
0006E3	Quantitative Imaging Corporation
0006E4	Citel Technologies Ltd.
0006E5	Fujian Newland Computer Ltd. Co.
0006E6	DongYang Telecom Co., Ltd.
0006E7	Bit Blitz Communications Inc.
0006E8	Optical Network Testing, Inc.
0006E9	Intime Corp.
0006EA	ELZET80 Mikrocomputer GmbH&Co. KG
0006EB	Global Data
0006EC	Harris Corporation
0006ED	Inara Networks
0006EE	Shenyang Neu-era Information & Technology Stock Co., Ltd
0006EF	Maxxan Systems, Inc.
0006F0	Digeo, Inc.
0006F1	Optillion
0006F2	Platys Communications
0006F3	AcceLight Networks
0006F4	Prime Electronics & Satellitics Inc.
0006F5	ALPS ELECTRIC CO.,LTD.
0006F6	Cisco Systems, Inc
0006F7	ALPS ELECTRIC CO.,LTD.
0006F8	The Boeing Company
0006F9	Mitsui Zosen Systems Research Inc.
0006FA	IP SQUARE Co, Ltd.
0006FB	Hitachi Printing Solutions, Ltd.
0006FC	Fnet Co., Ltd.
0006FD	Comjet Information Systems Corp.
0006FE	Ambrado, Inc
0006FF	Sheba Systems Co., Ltd.
000700	Zettamedia Korea
000701	RACAL-DATACOM
000702	Varian Medical Systems
000703	CSEE Transport
000704	ALPS ELECTRIC CO.,LTD.
000705	Endress & Hauser GmbH & Co
000706	Sanritz Corporation
000707	Interalia Inc.
000708	Bitrage Inc.
000709	Westerstrand Urfabrik AB
00070A	Unicom Automation Co., Ltd.
00070B	Novabase SGPS, SA
00070C	SVA-Intrusion.com Co. Ltd.
00070D	Cisco				2511 Token Ring
00070E	Cisco Systems, Inc
00070F	Fujant, Inc.
000710	Adax, Inc.
000711	Acterna
000712	JAL Information Technology
000713	IP One, Inc.
000714	Brightcom
000715	General Research of Electronics, Inc.
000716	J & S Marine Ltd.
000717	Wieland Electric GmbH
000718	iCanTek Co., Ltd.
000719	Mobiis Co., Ltd.
00071A	Finedigital Inc.
00071B	CDVI Americas Ltd
00071C	At&T
00071D	Satelsa Sistemas Y Aplicaciones De Telecomunicaciones, S.A.
00071E	Tri-M Engineering / Nupak Dev. Corp.
00071F	European Systems Integration
000720	Trutzschler GmbH & Co. KG
000721	Formac Elektronik GmbH
000722	The Nielsen Company
000723	ELCON Systemtechnik GmbH
000724	Telemax Co., Ltd.
000725	Bematech International Corp.
000726	Shenzhen Gongjin Electronics Co., Ltd.
000727	Zi Corporation (HK) Ltd.
000728	Neo Telecom
000729	Kistler Instrumente AG
00072A	Innovance Networks
00072B	Jung Myung Telecom Co., Ltd.
00072C	Fabricom
00072D	CNSystems
00072E	North Node AB
00072F	Intransa, Inc.
000730	Hutchison OPTEL Telecom Technology Co., Ltd.
000731	Ophir-Spiricon LLC
000732	AAEON Technology Inc.
000733	DANCONTROL Engineering
000734	ONStor, Inc.
000735	Flarion Technologies, Inc.
000736	Data Video Technologies Co., Ltd.
000737	Soriya Co. Ltd.
000738	Young Technology Co., Ltd.
000739	Scotty Group Austria Gmbh
00073A	Inventel Systemes
00073B	Tenovis GmbH & Co KG
00073C	Telecom Design
00073D	Nanjing Postel Telecommunications Co., Ltd.
00073E	China Great-Wall Computer Shenzhen Co., Ltd.
00073F	Woojyun Systec Co., Ltd.
000740	BUFFALO.INC
000741	Sierra Automated Systems
000742	Ormazabal
000743	Chelsio Communications
000744	Unico, Inc.
000745	Radlan Computer Communications Ltd.
000746	TURCK, Inc.
000747	Mecalc
000748	The Imaging Source Europe
000749	CENiX Inc.
00074A	Carl Valentin GmbH
00074B	Daihen Corporation
00074C	Beicom Inc.
00074D	Zebra Technologies Corp.
00074E	IPFRONT Inc
00074F	Cisco Systems, Inc
000750	Cisco Systems, Inc
000751	m-u-t AG
000752	Rhythm Watch Co., Ltd.
000753	Beijing Qxcomm Technology Co., Ltd.
000754	Xyterra Computing, Inc.
000755	Lafon
000756	Juyoung Telecom
000757	Topcall International AG
000758	Dragonwave
000759	Boris Manufacturing Corp.
00075A	Air Products and Chemicals, Inc.
00075B	Gibson Guitars
00075C	Eastman Kodak Company
00075D	Celleritas Inc.
00075E	Ametek Power Instruments
00075F	VCS Video Communication Systems AG
000760	TOMIS Information & Telecom Corp.
000761	29530
000762	Group Sense Limited
000763	Sunniwell Cyber Tech. Co., Ltd.
000764	YoungWoo Telecom Co. Ltd.
000765	Jade Quantum Technologies, Inc.
000766	Chou Chin Industrial Co., Ltd.
000767	Yuxing Electronics Company Limited
000768	Danfoss A/S
000769	Italiana Macchi SpA
00076A	NEXTEYE Co., Ltd.
00076B	Stralfors AB
00076C	Daehanet, Inc.
00076D	Flexlight Networks
00076E	Sinetica Corporation Limited
00076F	Synoptics Limited
000770	Ubiquoss Inc
000771	Embedded System Corporation
000772	Alcatel-               # Alcatel-Lucent Shanghai Bell Co., Ltd
000773	Ascom Powerline Communications Ltd.
000774	GuangZhou Thinker Technology Co. Ltd.
000775	Valence Semiconductor, Inc.
000776	Federal APD
000777	Motah Ltd.
000778	GERSTEL GmbH & Co. KG
000779	Sungil Telecom Co., Ltd.
00077A	Infoware System Co., Ltd.
00077B	Millimetrix Broadband Networks
00077C	Westermo Teleindustri AB
00077D	Cisco Systems, Inc
00077E	Elrest GmbH
00077F	J Communications Co., Ltd.
000780	Bluegiga Technologies OY
000781	Itron Inc.
000782	Oracle Corporation
000783	SynCom Network, Inc.
000784	Cisco Systems, Inc
000785	Cisco Systems, Inc
000786	Wireless Networks Inc.
000787	Idea System Co., Ltd.
000788	Clipcomm, Inc.
000789	DONGWON SYSTEMS
00078A	Mentor Data System Inc.
00078B	Wegener Communications, Inc.
00078C	Elektronikspecialisten i Borlange AB
00078D	NetEngines Ltd.
00078E	Garz & Friche GmbH
00078F	Emkay Innovative Products
000790	Tri-M Technologies (s) Limited
000791	International Data Communications, Inc.
000792	Sütron Electronic GmbH
000793	Shin Satellite Public Company Limited
000794	Simple Devices, Inc.
000795	Elitegroup Computer Systems Co.,Ltd.
000796	LSI Systems, Inc.
000797	Netpower Co., Ltd.
000798	Selea SRL
000799	TippingPoint Technologies, Inc.
00079A	Verint Systems Inc
00079B	Aurora Networks
00079C	Golden Electronics Technology Co., Ltd.
00079D	Musashi Co., Ltd.
00079E	Ilinx Co., Ltd.
00079F	Action Digital Inc.
0007A0	e-Watch Inc.
0007A1	VIASYS Healthcare GmbH
0007A2	Opteon Corporation
0007A3	Ositis Software, Inc.
0007A4	GN Netcom Ltd.
0007A5	Y.D.K Co. Ltd.
0007A6	Leviton Manufacturing Co., Inc.
0007A7	A-Z Inc.
0007A8	Haier Group Technologies Ltd.
0007A9	Novasonics
0007AA	Quantum Data Inc.
0007AB	Samsung Electronics Co.,Ltd
0007AC	Eolring
0007AD	Pentacon GmbH Foto-und Feinwerktechnik
0007AE	Britestream Networks, Inc.
0007AF	Red Lion Controls, LP
0007B0	Office Details, Inc.
0007B1	Equator Technologies
0007B2	Transaccess S.A.
0007B3	Cisco Systems, Inc
0007B4	Cisco Systems, Inc
0007B5	Any One Wireless Ltd.
0007B6	Telecom Technology Ltd.
0007B7	Samurai Ind. Prods Eletronicos Ltda
0007B8	Corvalent Corporation
0007B9	Ginganet Corporation
0007BA	UTStarcom Inc
0007BB	Candera Inc.
0007BC	Identix Inc.
0007BD	Radionet Ltd.
0007BE	DataLogic SpA
0007BF	Armillaire Technologies, Inc.
0007C0	NetZerver Inc.
0007C1	Overture Networks, Inc.
0007C2	Netsys Telecom
0007C3	Thomson
0007C4	JEAN Co. Ltd.
0007C5	Gcom, Inc.
0007C6	VDS Vosskuhler GmbH
0007C7	Synectics Systems Limited
0007C8	Brain21, Inc.
0007C9	Technol Seven Co., Ltd.
0007CA	Creatix Polymedia Ges Fur Kommunikaitonssysteme
0007CB	FREEBOX SAS
0007CC	Kaba Benzing GmbH
0007CD	Kumoh Electronic Co, Ltd
0007CE	Cabletime Limited
0007CF	Anoto AB
0007D0	Automat Engenharia de Automação Ltda.
0007D1	Spectrum Signal Processing Inc.
0007D2	Logopak Systeme GmbH & Co. KG
0007D3	SPGPrints B.V.
0007D4	Zhejiang Yutong Network Communication Co Ltd.
0007D5	3e Technologies Int;., Inc.
0007D6	Commil Ltd.
0007D7	Caporis Networks AG
0007D8	Hitron Technologies. Inc
0007D9	Splicecom
0007DA	Neuro Telecom Co., Ltd.
0007DB	Kirana Networks, Inc.
0007DC	Atek Co, Ltd.
0007DD	Cradle Technologies
0007DE	eCopilt AB
0007DF	Vbrick Systems Inc.
0007E0	Palm Inc.
0007E1	WIS Communications Co. Ltd.
0007E2	Bitworks, Inc.
0007E3	Navcom Technology, Inc.
0007E4	SoftRadio Co., Ltd.
0007E5	Coup Corporation
0007E6	edgeflow Canada Inc.
0007E7	FreeWave Technologies
0007E8	Edgewave
0007E9	Intel Corporation
0007EA	Massana, Inc.
0007EB	Cisco Systems, Inc
0007EC	Cisco Systems, Inc
0007ED	Altera Corporation
0007EE	telco Informationssysteme GmbH
0007EF	Lockheed Martin Tactical Systems
0007F0	LogiSync LLC
0007F1	TeraBurst Networks Inc.
0007F2	IOA Corporation
0007F3	Thinkengine Networks
0007F4	Eletex Co., Ltd.
0007F5	Bridgeco Co AG
0007F6	Qqest Software Systems
0007F7	Galtronics
0007F8	ITDevices, Inc.
0007F9	Sensaphone
0007FA	ITT Co., Ltd.
0007FB	Giga Stream UMTS Technologies GmbH
0007FC	Adept Systems Inc.
0007FD	LANergy Ltd.
0007FE	Rigaku Corporation
0007FF	Gluon Networks
000800	MULTITECH SYSTEMS, INC.
000801	HighSpeed Surfing Inc.
000802	Hewlett Packard
000803	Cos Tron
000804	ICA Inc.
000805	Techno-Holon Corporation
000806	Raonet Systems, Inc.
000807	Access Devices Limited
000808	PPT Vision, Inc.
000809	Systemonic AG
00080A	Espera-Werke GmbH
00080B	Birka BPA Informationssystem AB
00080C	VDA Elettronica spa
00080D	Toshiba
00080E	ARRIS Group, Inc.
00080F	Proximion Fiber Optics AB
000810	Key Technology, Inc.
000811	VOIX Corporation
000812	GM-2 Corporation
000813	Diskbank, Inc.
000814	TIL Technologies
000815	CATS Co., Ltd.
000816	Bluelon ApS
000817	EmergeCore Networks LLC
000818	Pixelworks, Inc.
000819	Banksys
00081A	Sanrad Intelligence Storage Communications (2000) Ltd.
00081B	Windigo Systems
00081C	@pos.com
00081D	Ipsil, Incorporated
00081E	Repeatit AB
00081F	Pou Yuen Tech Corp. Ltd.
000820	Cisco Systems, Inc
000821	Cisco Systems, Inc
000822	InPro Comm
000823	Texa Corp.
000824	Nuance Document Imaging
000825	Acme Packet
000826	Colorado Med Tech
000827	ADB Broadband Italia
000828	Koei Engineering Ltd.
000829	Aval Nagasaki Corporation
00082A	Powerwallz Network Security
00082B	Wooksung Electronics, Inc.
00082C	Homag AG
00082D	Indus Teqsite Private Limited
00082E	Multitone Electronics PLC
00082F	Cisco Systems, Inc
000830	Cisco Systems, Inc
000831	Cisco Systems, Inc
000832	Cisco Systems, Inc
00084E	DivergeNet, Inc.
00084F	Qualstar Corporation
000850	Arizona Instrument Corp.
000851	Canadian Bank Note Company, Ltd.
000852	Technically Elite Concepts
000853	Schleicher GmbH & Co. Relaiswerke KG
000854	Netronix, Inc.
000855	Fermilab
000856	Gamatronic Electronic Industries Ltd.
000857	Polaris Networks, Inc.
000858	Novatechnology Inc.
000859	ShenZhen Unitone Electronics Co., Ltd.
00085A	IntiGate Inc.
00085B	Hanbit Electronics Co., Ltd.
00085C	Shanghai Dare Technologies Co. Ltd.
00085D	Aastra
00085E	PCO AG
00085F	Picanol N.V.
000860	LodgeNet Entertainment Corp.
000861	SoftEnergy Co., Ltd.
000862	NEC Eluminant Technologies, Inc.
000863	Entrisphere Inc.
000864	Fasy S.p.A.
000865	JASCOM CO., LTD
000866	DSX Access Systems, Inc.
000867	Uptime Devices
000868	Puroptix
000869	Command-               # Command-e Technology Co.,Ltd.
00086A	Securiton Gmbh
00086B	Mipsys
00086C	Plasmon LMS
00086D	Missouri FreeNet
00086E	Hyglo AB
00086F	Resources Computer Network Ltd.
000870	Rasvia Systems, Inc.
000871	NORTHDATA Co., Ltd.
000872	Sorenson Communications
000873	DapTechnology B.V.
000874	Dell Inc.
000875	Acorp Electronics Corp.
000876	Sdsystem
000877	Liebert-               # Liebert-Hiross Spa
000878	Benchmark Storage Innovations
000879	CEM Corporation
00087A	Wipotec GmbH
00087B	RTX Telecom A/S
00087C	Cisco Systems, Inc
00087D	Cisco Systems, Inc
00087E	Bon Electro-Telecom Inc.
00087F	SPAUN electronic GmbH & Co. KG
000880	BroadTel Canada Communications inc.
000881	DIGITAL HANDS CO.,LTD.
000882	SIGMA CORPORATION
000883	Hewlett Packard
000884	Index Braille AB
000885	EMS Dr. Thomas Wünsche
000886	Hansung Teliann, Inc.
000887	Maschinenfabrik Reinhausen GmbH
000888	OULLIM Information Technology Inc,.
000889	Echostar Technologies Corp
00088A	Minds@Work
00088B	Tropic Networks Inc.
00088C	Quanta Network Systems Inc.
00088D	Sigma-Links Inc.
00088E	Nihon Computer Co., Ltd.
00088F	ADVANCED DIGITAL TECHNOLOGY
000890	AVILINKS SA
000891	Lyan Inc.
000892	EM Solutions
000893	LE INFORMATION COMMUNICATION INC.
000894	InnoVISION Multimedia Ltd.
000895	DIRC Technologie GmbH & Co.KG
000896	Printronix, Inc.
000897	Quake Technologies
000898	Gigabit Optics Corporation
000899	Netbind, Inc.
00089A	Alcatel Microelectronics
00089B	ICP Electronics Inc.
00089C	Elecs Industry Co., Ltd.
00089D	UHD-Elektronik
00089E	Beijing Enter-Net co.LTD
00089F	EFM Networks
0008A0	Stotz Feinmesstechnik GmbH
0008A1	CNet Technology Inc.
0008A2	ADI Engineering, Inc.
0008A3	Cisco Systems, Inc
0008A4	Cisco Systems, Inc
0008A5	Peninsula Systems Inc.
0008A6	Multiware & Image Co., Ltd.
0008A7	iLogic Inc.
0008A8	Systec Co., Ltd.
0008A9	SangSang Technology, Inc.
0008AA	Karam
0008AB	EnerLinx.com, Inc.
0008AC	Eltromat GmbH
0008AD	Toyo-Linx Co., Ltd.
0008AE	PacketFront Network Products AB
0008AF	Novatec Corporation
0008B0	BKtel communications GmbH
0008B1	ProQuent Systems
0008B2	SHENZHEN COMPASS TECHNOLOGY DEVELOPMENT CO.,LTD
0008B3	Fastwel
0008B4	Syspol
0008B5	TAI GUEN ENTERPRISE CO., LTD
0008B6	RouteFree, Inc.
0008B7	HIT Incorporated
0008B8	E.F. Johnson
0008B9	Kaonmedia CO., LTD.
0008BA	Erskine Systems Ltd
0008BB	NetExcell
0008BC	Ilevo AB
0008BD	Tepg-Us
0008BE	XENPAK MSA Group
0008BF	Aptus Elektronik AB
0008C0	ASA SYSTEMS
0008C1	Avistar Communications Corporation
0008C2	Cisco Systems, Inc
0008C3	Contex A/S
0008C4	Hikari Co.,Ltd.
0008C5	Liontech Co., Ltd.
0008C6	Philips Consumer Communications
0008C7	Compaq
0008C8	Soneticom, Inc.
0008C9	TechniSat Digital GmbH
0008CA	TwinHan Technology Co.,Ltd
0008CB	Zeta Broadband Inc.
0008CC	Remotec, Inc.
0008CD	With-Net Inc
0008CE	IPMobileNet Inc.
0008CF	Nippon Koei Power Systems Co., Ltd.
0008D0	Musashi Engineering Co., LTD.
0008D1	KAREL INC.
0008D2	ZOOM Networks Inc.
0008D3	Hercules Technologies S.A.S.
0008D4	IneoQuest Technologies, Inc
0008D5	Vanguard Networks Solutions, LLC
0008D6	HASSNET Inc.
0008D7	HOW CORPORATION
0008D8	Dowkey Microwave
0008D9	Mitadenshi Co.,LTD
0008DA	SofaWare Technologies Ltd.
0008DB	Corrigent Systems
0008DC	Wiznet
0008DD	Telena Communications, Inc.
0008DE	3UP Systems
0008DF	Alistel Inc.
0008E0	ATO Technology Ltd.
0008E1	Barix AG
0008E2	Cisco Systems, Inc
0008E3	Cisco Systems, Inc
0008E4	Envenergy Inc
0008E5	IDK Corporation
0008E6	Littlefeet
0008E7	SHI ControlSystems,Ltd.
0008E8	Excel Master Ltd.
0008E9	Nextgig
0008EA	Motion Control Engineering, Inc
0008EB	ROMWin Co.,Ltd.
0008EC	Optical Zonu Corporation
0008ED	ST&T Instrument Corp.
0008EE	Logic Product Development
0008EF	DIBAL,S.A.
0008F0	Next Generation Systems, Inc.
0008F1	Voltaire
0008F2	C&S Technology
0008F3	Wany
0008F4	Bluetake Technology Co., Ltd.
0008F5	YESTECHNOLOGY Co.,Ltd.
0008F6	Sumitomo Electric Industries,Ltd
0008F7	Hitachi Ltd, Semiconductor & Integrated Circuits Gr
0008F8	UTC CCS
0008F9	Artesyn Embedded Technologies
0008FA	Karl E.Brinkmann GmbH
0008FB	SonoSite, Inc.
0008FC	Gigaphoton Inc.
0008FD	BlueKorea Co., Ltd.
0008FE	UNIK C&C Co.,Ltd.
0008FF	Trilogy Communications Ltd
000900	Tmt
000901	Shenzhen Shixuntong Information & Technoligy Co
000902	Redline Communications Inc.
000903	Panasas, Inc
000904	MONDIAL electronic
000905	iTEC Technologies Ltd.
000906	Esteem Networks
000907	Chrysalis Development
000908	VTech Technology Corp.
000909	Telenor Connect A/S
00090A	SnedFar Technology Co., Ltd.
00090B	MTL  Instruments PLC
00090C	Mayekawa Mfg. Co. Ltd.
00090D	LEADER ELECTRONICS CORP.
00090E	Helix Technology Inc.
00090F	Fortinet Inc.
000910	Simple Access Inc.
000911	Cisco Systems, Inc
000912	Cisco Systems, Inc
000913	SystemK Corporation
000914	COMPUTROLS INC.
000915	CAS Corp.
000916	Listman Home Technologies, Inc.
000917	WEM Technology Inc
000918	SAMSUNG TECHWIN CO.,LTD
000919	MDS Gateways
00091A	Macat Optics & Electronics Co., Ltd.
00091B	Digital Generation Inc.
00091C	CacheVision, Inc
00091D	Proteam Computer Corporation
00091E	Firstech Technology Corp.
00091F	A&D Co., Ltd.
000920	EpoX COMPUTER CO.,LTD.
000921	Planmeca Oy
000922	TST Biometrics GmbH
000923	Heaman System Co., Ltd
000924	Telebau GmbH
000925	VSN Systemen BV
000926	YODA COMMUNICATIONS, INC.
000927	TOYOKEIKI CO.,LTD.
000928	Telecore
000929	Sanyo Industries (UK) Limited
00092A	MYTECS Co.,Ltd.
00092B	iQstor Networks, Inc.
00092C	Hitpoint Inc.
00092D	HTC Corporation
00092E	B&Tech System Inc.
00092F	Akom Technology Corporation
000930	AeroConcierge Inc.
000931	Future Internet, Inc.
000932	Omnilux
000933	Ophit Co.Ltd.
000934	Dream-Multimedia-Tv GmbH
000935	Sandvine Incorporated
000936	Ipetronik GmbH & Co. KG
000937	Inventec Appliance Corp
000938	Allot Communications
000939	ShibaSoku Co.,Ltd.
00093A	Molex
00093B	HYUNDAI NETWORKS INC.
00093C	Jacques Technologies P/L
00093D	Newisys,Inc.
00093E	C&I Technologies
00093F	Double-Win Enterpirse CO., LTD
000940	AGFEO GmbH & Co. KG
000941	Allied Telesis R&D Center K.K.
000942	Wireless Technologies, Inc
000943	Cisco Systems, Inc
000944	Cisco Systems, Inc
000945	Palmmicro Communications Inc
000946	Cluster Labs GmbH
000947	Aztek, Inc.
000948	Vista Control Systems, Corp.
000949	Glyph Technologies Inc.
00094A	Homenet Communications
00094B	FillFactory NV
00094C	Communication Weaver Co.,Ltd.
00094D	Braintree Communications Pty Ltd
00094E	BARTECH SYSTEMS INTERNATIONAL, INC
00094F	elmegt GmbH & Co. KG
000950	Independent Storage Corporation
000951	Apogee Imaging Systems
000952	Auerswald GmbH & Co. KG
000953	Linkage System Integration Co.Ltd.
000954	AMiT spol. s. r. o.
000955	Young Generation International Corp.
000956	Network Systems Group, Ltd. (NSG)
000957	Supercaller, Inc.
000958	INTELNET S.A.
000959	Sitecsoft
00095A	RACEWOOD TECHNOLOGY
00095B	Netgear
00095C	Philips Medical Systems - Cardiac and Monitoring Systems (CM
00095D	Dialogue Technology Corp.
00095E	Masstech Group Inc.
00095F	Telebyte, Inc.
000960	YOZAN Inc.
000961	Switchgear and Instrumentation Ltd
000962	Sonitor Technologies AS
000963	Dominion Lasercom Inc.
000964	Hi-Techniques, Inc.
000965	HyunJu Computer Co., Ltd.
000966	Thales Navigation
000967	Tachyon, Inc
000968	TECHNOVENTURE, INC.
000969	Meret Optical Communications
00096A	Cloverleaf Communications Inc.
00096B	IBM Corp
00096C	Imedia Semiconductor Corp.
00096D	Powernet Technologies Corp.
00096E	GIANT ELECTRONICS LTD.
00096F	Beijing Zhongqing Elegant Tech. Corp.,Limited
000970	Vibration Research Corporation
000971	Time Management, Inc.
000972	Securebase,Inc
000973	Lenten Technology Co., Ltd.
000974	Innopia Technologies, Inc.
000975	fSONA Communications Corporation
000976	Datasoft ISDN Systems GmbH
000977	Brunner Elektronik AG
000978	AIJI System Co., Ltd.
000979	Advanced Television Systems Committee, Inc.
00097A	Louis Design Labs.
00097B	Cisco Systems, Inc
00097C	Cisco Systems, Inc
00097D	SecWell Networks Oy
00097E	IMI TECHNOLOGY CO., LTD
00097F	Vsecure 2000 LTD.
000980	Power Zenith Inc.
000981	Newport Networks
000982	Loewe Opta GmbH
000983	GlobalTop Technology, Inc.
000984	MyCasa Network Inc.
000985	Auto Telecom Company
000986	Metalink LTD.
000987	NISHI NIPPON ELECTRIC WIRE & CABLE CO.,LTD.
000988	Nudian Electron Co., Ltd.
000989	VividLogic Inc.
00098A	EqualLogic Inc
00098B	Entropic Communications, Inc.
00098C	Option Wireless Sweden
00098D	Velocity Semiconductor
00098E	ipcas GmbH
00098F	Cetacean Networks
000990	ACKSYS Communications & systems
000991	GE Fanuc Automation Manufacturing, Inc.
000992	InterEpoch Technology,INC.
000993	Visteon Corporation
000994	Cronyx Engineering
000995	Castle Technology Ltd
000996	Rdi
000997	Nortel Networks
000998	Capinfo Company Limited
000999	CP GEORGES RENAULT
00099A	ELMO COMPANY, LIMITED
00099B	Western Telematic Inc.
00099C	Naval Research Laboratory
00099D	Haliplex Communications
00099E	Testech, Inc.
00099F	VIDEX INC.
0009A0	Microtechno Corporation
0009A1	Telewise Communications, Inc.
0009A2	Interface Co., Ltd.
0009A3	Leadfly Techologies Corp. Ltd.
0009A4	HARTEC Corporation
0009A5	HANSUNG ELETRONIC INDUSTRIES DEVELOPMENT CO., LTD
0009A6	Ignis Optics, Inc.
0009A7	Bang & Olufsen A/S
0009A8	Eastmode Pte Ltd
0009A9	Ikanos Communications
0009AA	Data Comm for Business, Inc.
0009AB	Netcontrol Oy
0009AC	Lanvoice
0009AD	HYUNDAI SYSCOMM, INC.
0009AE	OKANO ELECTRIC CO.,LTD
0009AF	e-generis
0009B0	Onkyo Corporation
0009B1	Kanematsu Electronics, Ltd.
0009B2	L&F Inc.
0009B3	MCM Systems Ltd
0009B4	KISAN TELECOM CO., LTD.
0009B5	3J Tech. Co., Ltd.
0009B6	Cisco Systems, Inc
0009B7	Cisco Systems, Inc
0009B8	Entise Systems
0009B9	Action Imaging Solutions
0009BA	MAKU Informationstechik GmbH
0009BB	MathStar, Inc.
0009BC	Digital Safety Technologies, Inc
0009BD	Epygi Technologies, Ltd.
0009BE	Mamiya-OP Co.,Ltd.
0009BF	Nintendo Co., Ltd.
0009C0	6wind
0009C1	PROCES-DATA A/S
0009C2	Onity, Inc.
0009C3	Netas
0009C4	Medicore Co., Ltd
0009C5	KINGENE Technology Corporation
0009C6	Visionics Corporation
0009C7	Movistec
0009C8	SINAGAWA TSUSHIN KEISOU SERVICE
0009C9	BlueWINC Co., Ltd.
0009CA	iMaxNetworks(Shenzhen)Limited.
0009CB	Hbrain
0009CC	Moog GmbH
0009CD	HUDSON SOFT CO.,LTD.
0009CE	SpaceBridge Semiconductor Corp.
0009CF	iAd GmbH
0009D0	Solacom Technologies Inc.
0009D1	SERANOA NETWORKS INC
0009D2	Mai Logic Inc.
0009D3	Western DataCom Co., Inc.
0009D4	Transtech Networks
0009D5	Signal Communication, Inc.
0009D6	KNC One GmbH
0009D7	DC Security Products
0009D8	Fält Communications AB
0009D9	Neoscale Systems, Inc
0009DA	Control Module Inc.
0009DB	Espace
0009DC	Galaxis Technology AG
0009DD	Mavin Technology Inc.
0009DE	Samjin Information & Communications Co., Ltd.
0009DF	Vestel Komunikasyon Sanayi ve Ticaret A.S.
0009E0	XEMICS S.A.
0009E1	Gemtek Technology Co., Ltd.
0009E2	Sinbon Electronics Co., Ltd.
0009E3	Angel Iglesias S.A.
0009E4	K Tech Infosystem Inc.
0009E5	Hottinger Baldwin Messtechnik GmbH
0009E6	Cyber Switching Inc.
0009E7	ADC Techonology
0009E8	Cisco Systems, Inc
0009E9	Cisco Systems, Inc
0009EA	YEM Inc.
0009EB	HuMANDATA LTD.
0009EC	Daktronics, Inc.
0009ED	CipherOptics
0009EE	MEIKYO ELECTRIC CO.,LTD
0009EF	Vocera Communications
0009F0	Shimizu Technology Inc.
0009F1	Yamaki Electric Corporation
0009F2	Cohu, Inc., Electronics Division
0009F3	WELL Communication Corp.
0009F4	Alcon Laboratories, Inc.
0009F5	Emerson Network Power Co.,Ltd
0009F6	Shenzhen Eastern Digital Tech Ltd.
0009F7	SED, a division of Calian
0009F8	UNIMO TECHNOLOGY CO., LTD.
0009F9	ART JAPAN CO., LTD.
0009FB	Philips Patient Monitoring
0009FC	IPFLEX Inc.
0009FD	Ubinetics Limited
0009FE	Daisy Technologies, Inc.
0009FF	X.net 2000 GmbH
000A00	Mediatek Corp.
000A01	SOHOware, Inc.
000A02	ANNSO CO., LTD.
000A03	ENDESA SERVICIOS, S.L.
000A04	3Com Ltd
000A05	Widax Corp.
000A06	Teledex LLC
000A07	WebWayOne Ltd
000A08	Alpine Electronics, Inc.
000A09	TaraCom Integrated Products, Inc.
000A0A	SUNIX Co., Ltd.
000A0B	Sealevel Systems, Inc.
000A0C	Scientific Research Corporation
000A0D	FCI Deutschland GmbH
000A0E	Invivo Research Inc.
000A0F	Ilryung Telesys, Inc
000A10	FAST media integrations AG
000A11	ExPet Technologies, Inc
000A12	Azylex Technology, Inc
000A13	Honeywell Video Systems
000A14	TECO a.s.
000A15	Silicon Data, Inc
000A16	Lassen Research
000A17	NESTAR COMMUNICATIONS, INC
000A18	Vichel Inc.
000A19	Valere Power, Inc.
000A1A	Imerge Ltd
000A1B	Stream Labs
000A1C	Bridge Information Co., Ltd.
000A1D	Optical Communications Products Inc.
000A1E	Red-M Products Limited
000A1F	ART WARE Telecommunication Co., Ltd.
000A20	SVA Networks, Inc.
000A21	Integra Telecom Co. Ltd
000A22	Amperion Inc
000A23	Parama Networks Inc
000A24	Octave Communications
000A25	CERAGON NETWORKS
000A26	CEIA S.p.A.
000A27	Apple, Inc.
000A28	Motorola
000A29	Pan Dacom Networking AG
000A2A	QSI Systems Inc.
000A2B	Etherstuff
000A2C	Active Tchnology Corporation
000A2D	Cabot Communications Limited
000A2E	MAPLE NETWORKS CO., LTD
000A2F	Artnix Inc.
000A30	Visteon Corporation
000A31	HCV Consulting
000A32	Xsido Corporation
000A33	Emulex Corporation
000A34	Identicard Systems Incorporated
000A35	Xilinx
000A36	Synelec Telecom Multimedia
000A37	Procera Networks, Inc.
000A38	Apani Networks
000A39	LoPA Information Technology
000A3A	J-THREE INTERNATIONAL Holding Co., Ltd.
000A3B	GCT Semiconductor, Inc
000A3C	Enerpoint Ltd.
000A3D	Elo Sistemas Eletronicos S.A.
000A3E	EADS Telecom
000A3F	Data East Corporation
000A40	Crown Audio -- Harmanm International
000A41	Cisco Systems, Inc
000A42	Cisco Systems, Inc
000A43	Chunghwa Telecom Co., Ltd.
000A44	Avery Dennison Deutschland GmbH
000A45	Audio-Technica Corp.
000A46	ARO WELDING TECHNOLOGIES SAS
000A47	Allied Vision Technologies
000A48	Albatron Technology
000A49	F5 Networks, Inc.
000A4A	Targa Systems Ltd.
000A4B	DataPower Technology, Inc.
000A4C	Molecular Devices Corporation
000A4D	Noritz Corporation
000A4E	UNITEK Electronics INC.
000A4F	Brain Boxes Limited
000A50	REMOTEK CORPORATION
000A51	GyroSignal Technology Co., Ltd.
000A52	AsiaRF Ltd.
000A53	Intronics, Incorporated
000A54	Laguna Hills, Inc.
000A55	MARKEM Corporation
000A56	HITACHI Maxell Ltd.
000A57	Hewlett Packard
000A58	Freyer & Siegel Elektronik GmbH & Co. KG
000A59	HW server
000A5A	GreenNET Technologies Co.,Ltd.
000A5B	Power-One as
000A5C	Carel s.p.a.
000A5D	FingerTec Worldwide Sdn Bhd
000A5E	3COM Corporation
000A5F	almedio inc.
000A60	Autostar Technology Pte Ltd
000A61	Cellinx Systems Inc.
000A62	Crinis Networks, Inc.
000A63	DHD GmbH
000A64	Eracom Technologies
000A65	GentechMedia.co.,ltd.
000A66	MITSUBISHI ELECTRIC SYSTEM & SERVICE CO.,LTD.
000A67	Ongcorp
000A68	Solarflare Communications Inc
000A69	SUNNY bell Technology Co., Ltd.
000A6A	SVM Microwaves s.r.o.
000A6B	Tadiran Telecom Business Systems LTD
000A6C	Walchem Corporation
000A6D	EKS Elektronikservice GmbH
000A6E	Harmonic, Inc
000A6F	ZyFLEX Technologies Inc
000A70	MPLS Forum
000A71	Avrio Technologies, Inc
000A72	STEC, INC.
000A73	Scientific Atlanta
000A74	Manticom Networks Inc.
000A75	Caterpillar, Inc
000A76	Beida Jade Bird Huaguang Technology Co.,Ltd
000A77	Bluewire Technologies LLC
000A78	Olitec
000A79	corega K.K
000A7A	Kyoritsu Electric Co., Ltd.
000A7B	Cornelius Consult
000A7C	Tecton Ltd
000A7D	Valo, Inc.
000A7E	The Advantage Group
000A7F	Teradon Industries, Inc
000A80	Telkonet Inc.
000A81	TEIMA Audiotex S.L.
000A82	TATSUTA SYSTEM ELECTRONICS CO.,LTD.
000A83	SALTO SYSTEMS S.L.
000A84	Rainsun Enterprise Co., Ltd.
000A85	PLAT'C2,Inc
000A86	Lenze
000A87	Integrated Micromachines Inc.
000A88	InCypher S.A.
000A89	Creval Systems, Inc.
000A8A	Cisco Systems, Inc
000A8B	Cisco Systems, Inc
000A8C	Guardware Systems Ltd.
000A8D	EUROTHERM LIMITED
000A8E	Invacom Ltd
000A8F	Aska International Inc.
000A90	Bayside Interactive, Inc.
000A91	HemoCue AB
000A92	Presonus Corporation
000A93	W2 Networks, Inc.
000A94	ShangHai cellink CO., LTD
000A95	Apple, Inc.
000A96	MEWTEL TECHNOLOGY INC.
000A97	SONICblue, Inc.
000A98	M+F Gwinner GmbH & Co
000A99	Calamp Wireless Networks Inc
000A9A	Aiptek International Inc
000A9B	TB Group Inc
000A9C	Server Technology, Inc.
000A9D	King Young Technology Co. Ltd.
000A9E	BroadWeb Corportation
000A9F	Pannaway Technologies, Inc.
000AA0	Cedar Point Communications
000AA1	V V S Limited
000AA2	SYSTEK INC.
000AA3	SHIMAFUJI ELECTRIC CO.,LTD.
000AA4	SHANGHAI SURVEILLANCE TECHNOLOGY CO,LTD
000AA5	MAXLINK INDUSTRIES LIMITED
000AA6	Hochiki Corporation
000AA7	FEI Electron Optics
000AA8	ePipe Pty. Ltd.
000AA9	Brooks Automation GmbH
000AAA	AltiGen Communications Inc.
000AAB	Toyota Technical Development Corporation
000AAC	TerraTec Electronic GmbH
000AAD	Stargames Corporation
000AAE	Rosemount Process Analytical
000AAF	Pipal Systems
000AB0	LOYTEC electronics GmbH
000AB1	GENETEC Corporation
000AB2	Fresnel Wireless Systems
000AB3	Fa. GIRA
000AB4	ETIC Telecommunications
000AB5	Digital Electronic Network
000AB6	COMPUNETIX, INC
000AB7	Cisco Systems, Inc
000AB8	Cisco Systems, Inc
000AB9	Astera Technologies Corp.
000ABA	Arcon Technology Limited
000ABB	Taiwan Secom Co,. Ltd
000ABC	Seabridge Ltd.
000ABD	Rupprecht & Patashnick Co.
000ABE	OPNET Technologies CO., LTD.
000ABF	HIROTA SS
000AC0	Fuyoh Video Industry CO., LTD.
000AC1	Futuretel
000AC2	Wuhan FiberHome Digital Technology Co.,Ltd.
000AC3	eM Technics Co., Ltd.
000AC4	Daewoo Teletech Co., Ltd
000AC5	Color Kinetics
000AC6	Overture Networks.
000AC7	Unication Group
000AC8	ZPSYS CO.,LTD. (Planning&Management)
000AC9	Zambeel Inc
000ACA	YOKOYAMA SHOKAI CO.,Ltd.
000ACB	XPAK MSA Group
000ACC	Winnow Networks, Inc.
000ACD	Sunrich Technology Limited
000ACE	RADIANTECH, INC.
000ACF	PROVIDEO Multimedia Co. Ltd.
000AD0	Niigata Develoment Center,  F.I.T. Co., Ltd.
000AD1	Mws
000AD2	JEPICO Corporation
000AD3	INITECH Co., Ltd
000AD4	CoreBell Systems Inc.
000AD5	Brainchild Electronic Co., Ltd.
000AD6	BeamReach Networks
000AD7	Origin ELECTRIC CO.,LTD.
000AD8	IPCserv Technology Corp.
000AD9	Sony Mobile Communications AB
000ADA	Vindicator Technologies
000ADB	SkyPilot Network, Inc
000ADC	RuggedCom Inc.
000ADD	Allworx Corp.
000ADE	Happy Communication Co., Ltd.
000ADF	Gennum Corporation
000AE0	Fujitsu Softek
000AE1	EG Technology
000AE2	Binatone Electronics International, Ltd
000AE3	YANG MEI TECHNOLOGY CO., LTD
000AE4	Wistron Corporation
000AE5	ScottCare Corporation
000AE6	Elitegroup Computer Systems Co.,Ltd.
000AE7	ELIOP S.A.
000AE8	Cathay Roxus Information Technology Co. LTD
000AE9	AirVast Technology Inc.
000AEA	ADAM ELEKTRONIK LTD. ŞTI
000AEB	TP-LINK TECHNOLOGIES CO.,LTD.
000AEC	Koatsu Gas Kogyo Co., Ltd.
000AED	HARTING Electronics GmbH
000AEE	GcdHard-               # GCD Hard- & Software GmbH
000AEF	OTRUM ASA
000AF0	SHIN-OH ELECTRONICS CO., LTD. R&D
000AF1	Clarity Design, Inc.
000AF2	NeoAxiom Corp.
000AF3	Cisco Systems, Inc
000AF4	Cisco Systems, Inc
000AF5	Airgo Networks, Inc.
000AF6	Emerson Climate Technologies Retail Solutions, Inc.
000AF7	Broadcom
000AF8	American Telecare Inc.
000AF9	HiConnect, Inc.
000AFA	Traverse Technologies Australia
000AFB	Ambri Limited
000AFC	Core Tec Communications, LLC
000AFD	Kentec Electronics
000AFE	NovaPal Ltd
000AFF	Kilchherr Elektronik AG
000B00	FUJIAN START COMPUTER EQUIPMENT CO.,LTD
000B01	DAIICHI ELECTRONICS CO., LTD.
000B02	Dallmeier electronic
000B03	Taekwang Industrial Co., Ltd
000B04	Volktek Corporation
000B05	Pacific Broadband Networks
000B06	ARRIS Group, Inc.
000B07	Voxpath Networks
000B08	Pillar Data Systems
000B09	Ifoundry Systems Singapore
000B0A	dBm Optics
000B0B	Corrent Corporation
000B0C	Agile Systems Inc.
000B0D	Air2U, Inc.
000B0E	Trapeze Networks
000B0F	Bosch Rexroth
000B10	11wave Technonlogy Co.,Ltd
000B11	HIMEJI ABC TRADING CO.,LTD.
000B12	NURI Telecom Co., Ltd.
000B13	ZETRON INC
000B14	ViewSonic Corporation
000B15	Platypus Technology
000B16	Communication Machinery Corporation
000B17	MKS Instruments
000B18	Private
000B19	Vernier Networks, Inc.
000B1A	Industrial Defender, Inc.
000B1B	Systronix, Inc.
000B1C	SIBCO bv
000B1D	LayerZero Power Systems, Inc.
000B1E	KAPPA opto-electronics GmbH
000B1F	I CON Computer Co.
000B20	Hirata corporation
000B21	G-Star Communications Inc.
000B22	Environmental Systems and Services
000B23	Siemens Subscriber Networks
000B24	Airlogic
000B25	Aeluros
000B26	Wetek Corporation
000B27	Scion Corporation
000B28	Quatech Inc.
000B29	LS(LG) Industrial Systems co.,Ltd
000B2A	HOWTEL Co., Ltd.
000B2B	HOSTNET CORPORATION
000B2C	Eiki Industrial Co. Ltd.
000B2D	Danfoss Inc.
000B2E	Cal-Comp Electronics & Communications Company Ltd.
000B2F	bplan GmbH
000B30	Beijing Gongye Science & Technology Co.,Ltd
000B31	Yantai ZhiYang Scientific and technology industry CO., LTD
000B32	VORMETRIC, INC.
000B33	Vivato Technologies
000B34	ShangHai Broadband Technologies CO.LTD
000B35	Quad Bit System co., Ltd.
000B36	Productivity Systems, Inc.
000B37	MANUFACTURE DES MONTRES ROLEX SA
000B38	Knürr GmbH
000B39	Keisoku Giken Co.,Ltd.
000B3A	QuStream Corporation
000B3B	devolo AG
000B3C	Cygnal Integrated Products, Inc.
000B3D	CONTAL OK Ltd.
000B3E	BittWare, Inc
000B3F	Anthology Solutions Inc.
000B40	Oclaro
000B41	Ing. Büro Dr. Beutlhauser
000B42	commax Co., Ltd.
000B43	Microscan Systems, Inc.
000B44	Concord IDea Corp.
000B45	Cisco Systems, Inc
000B46	Cisco Systems, Inc
000B47	Advanced Energy
000B48	Sofrel
000B49	RF-Link System Inc.
000B4A	Visimetrics (UK) Ltd
000B4B	VISIOWAVE SA
000B4C	Clarion (M) Sdn Bhd
000B4D	Emuzed
000B4E	VertexRSI, General Dynamics SatCOM Technologies, Inc.
000B4F	Verifone
000B50	Oxygnet
000B51	Micetek International Inc.
000B52	JOYMAX ELECTRONICS CO. LTD.
000B53	INITIUM Co., Ltd.
000B54	BiTMICRO Networks, Inc.
000B55	ADInstruments
000B56	Cybernetics
000B57	Silicon Laboratories
000B58	Astronautics C.A  LTD
000B59	ScriptPro, LLC
000B5A	HyperEdge
000B5B	Rincon Research Corporation
000B5C	Newtech Co.,Ltd
000B5D	FUJITSU LIMITED
000B5E	Audio Engineering Society Inc.
000B5F	Cisco Systems, Inc
000B60	Cisco Systems, Inc
000B61	Friedrich Lütze GmbH & Co. KG
000B62	ib-mohnen KG
000B63	Kaleidescape
000B64	Kieback & Peter GmbH & Co KG
000B65	Sy.A.C. srl
000B66	Teralink Communications
000B67	Topview Technology Corporation
000B68	Addvalue Communications Pte Ltd
000B69	Franke Finland Oy
000B6A	Asiarock Technology Limited
000B6B	Wistron Neweb Corporation
000B6C	Sychip Inc.
000B6D	SOLECTRON JAPAN NAKANIIDA
000B6E	Neff Instrument Corp.
000B6F	Media Streaming Networks Inc
000B70	Load Technology, Inc.
000B71	Litchfield Communications Inc.
000B72	Lawo AG
000B73	Kodeos Communications
000B74	Kingwave Technology Co., Ltd.
000B75	Iosoft Ltd.
000B76	ET&T Technology Co. Ltd.
000B77	Cogent Systems, Inc.
000B78	TAIFATECH INC.
000B79	X-COM, Inc.
000B7A	L-3 Linkabit
000B7B	Test-Um Inc.
000B7C	Telex Communications
000B7D	SOLOMON EXTREME INTERNATIONAL LTD.
000B7E	SAGINOMIYA Seisakusho Inc.
000B7F	Align Engineering LLC
000B80	Lycium Networks
000B81	Kaparel Corporation
000B82	Grandstream Networks, Inc.
000B83	DATAWATT B.V.
000B84	Bodet
000B85	Cisco Systems, Inc
000B86	Aruba Networks
000B87	American Reliance Inc.
000B88	Vidisco ltd.
000B89	Top Global Technology, Ltd.
000B8A	MITEQ Inc.
000B8B	KERAJET, S.A.
000B8C	Flextronics
000B8D	Avvio Networks
000B8E	Ascent Corporation
000B8F	AKITA ELECTRONICS SYSTEMS CO.,LTD.
000B90	ADVA Optical Networking Ltd.
000B91	Aglaia Gesellschaft für Bildverarbeitung und Kommunikation mbH
000B92	Ascom Danmark A/S
000B93	Ritter Elektronik
000B94	Digital Monitoring Products, Inc.
000B95	eBet Gaming Systems Pty Ltd
000B96	Innotrac Diagnostics Oy
000B97	Matsushita Electric Industrial Co.,Ltd.
000B98	NiceTechVision
000B99	SensAble Technologies, Inc.
000B9A	Shanghai Ulink Telecom Equipment Co. Ltd.
000B9B	Sirius System Co, Ltd.
000B9C	TriBeam Technologies, Inc.
000B9D	TwinMOS Technologies Inc.
000B9E	Yasing Technology Corp.
000B9F	Neue ELSA GmbH
000BA0	T&L Information Inc.
000BA1	Fujikura Solutions Ltd.
000BA2	Sumitomo Electric Industries,Ltd
000BA3	Siemens AG, I&S
000BA4	Shiron Satellite Communications Ltd. (1996)
000BA5	Quasar Cipta Mandiri, PT
000BA6	Miyakawa Electric Works Ltd.
000BA7	Maranti Networks
000BA8	HANBACK ELECTRONICS CO., LTD.
000BA9	CloudShield Technologies, Inc.
000BAA	Aiphone co.,Ltd
000BAB	Advantech Technology (CHINA) Co., Ltd.
000BAC	3Com Ltd
000BAD	PC-PoS Inc.
000BAE	Vitals System Inc.
000BAF	WOOJU COMMUNICATIONS Co,.Ltd
000BB0	Sysnet Telematica srl
000BB1	Super Star Technology Co., Ltd.
000BB2	SMALLBIG TECHNOLOGY
000BB3	RiT technologies Ltd.
000BB4	RDC Semiconductor Inc.,
000BB5	nStor Technologies, Inc.
000BB6	Metalligence Technology Corp.
000BB7	Micro Systems Co.,Ltd.
000BB8	Kihoku Electronic Co.
000BB9	Imsys AB
000BBA	Harmonic, Inc
000BBB	Etin Systems Co., Ltd
000BBC	En Garde Systems, Inc.
000BBD	Connexionz Limited
000BBE	Cisco Systems, Inc
000BBF	Cisco Systems, Inc
000BC0	China IWNComm Co., Ltd.
000BC1	Bay Microsystems, Inc.
000BC2	Corinex Communication Corp.
000BC3	Multiplex, Inc.
000BC4	BIOTRONIK GmbH & Co
000BC5	SMC Networks, Inc.
000BC6	ISAC, Inc.
000BC7	ICET S.p.A.
000BC8	AirFlow Networks
000BC9	Electroline Equipment
000BCA	DATAVAN TC
000BCB	Fagor Automation , S. Coop
000BCC	JUSAN, S.A.
000BCD	Hewlett Packard
000BCE	Free2move AB
000BCF	AGFA NDT INC.
000BD0	XiMeta Technology Americas Inc.
000BD1	Aeronix, Inc.
000BD2	Remopro Technology Inc.
000BD3	Cd3o
000BD4	Beijing Wise Technology & Science Development Co.Ltd
000BD5	Nvergence, Inc.
000BD6	Paxton Access Ltd
000BD7	DORMA Time + Access GmbH
000BD8	Industrial Scientific Corp.
000BD9	General Hydrogen
000BDA	EyeCross Co.,Inc.
000BDB	Dell Inc.
000BDC	Akcp
000BDD	TOHOKU RICOH Co., LTD.
000BDE	TELDIX GmbH
000BDF	Shenzhen RouterD Networks Limited
000BE0	SercoNet Ltd.
000BE1	Nokia NET Product Operations
000BE2	Lumenera Corporation
000BE3	Key Stream Co., Ltd.
000BE4	Hosiden Corporation
000BE5	HIMS International Corporation
000BE6	Datel Electronics
000BE7	COMFLUX TECHNOLOGY INC.
000BE8	Aoip
000BE9	Actel Corporation
000BEA	Zultys Technologies
000BEB	Systegra AG
000BEC	NIPPON ELECTRIC INSTRUMENT, INC.
000BED	ELM Inc.
000BEE	inc.jet, Incorporated
000BEF	Code Corporation
000BF0	MoTEX Products Co., Ltd.
000BF1	LAP Laser Applikations
000BF2	Chih-Kan Technology Co., Ltd.
000BF3	BAE SYSTEMS
000BF4	Private
000BF5	Shanghai Sibo Telecom Technology Co.,Ltd
000BF6	Nitgen Co., Ltd
000BF7	NIDEK CO.,LTD
000BF8	Infinera
000BF9	Gemstone Communications, Inc.
000BFA	EXEMYS SRL
000BFB	D-NET International Corporation
000BFC	Cisco Systems, Inc
000BFD	Cisco Systems, Inc
000BFE	CASTEL Broadband Limited
000BFF	Berkeley Camera Engineering
000C00	BEB Industrie-Elektronik AG
000C01	Abatron AG
000C02	ABB Oy
000C03	HDMI Licensing, LLC
000C04	Tecnova
000C05	RPA Reserch Co., Ltd.
000C06	Nixvue Systems  Pte Ltd
000C07	Iftest AG
000C08	HUMEX Technologies Corp.
000C09	Hitachi IE Systems Co., Ltd
000C0A	Guangdong Province Electronic Technology Research Institute
000C0B	Broadbus Technologies
000C0C	APPRO TECHNOLOGY INC.
000C0D	Communications & Power Industries / Satcom Division
000C0E	XtremeSpectrum, Inc.
000C0F	Techno-One Co., Ltd
000C10	PNI Corporation
000C11	NIPPON DEMPA CO.,LTD.
000C12	Micro-Optronic-Messtechnik GmbH
000C13	Mediaq
000C14	Diagnostic Instruments, Inc.
000C15	CyberPower Systems, Inc.
000C16	Concorde Microsystems Inc.
000C17	AJA Video Systems Inc
000C18	Zenisu Keisoku Inc.
000C19	Telio Communications GmbH
000C1A	Quest Technical Solutions Inc.
000C1B	ORACOM Co, Ltd.
000C1C	MicroWeb Co., Ltd.
000C1D	Mettler & Fuchs AG
000C1E	Global Cache
000C1F	Glimmerglass Networks
000C20	Fi WIn, Inc.
000C21	Faculty of Science and Technology, Keio University
000C22	Double D Electronics Ltd
000C23	Beijing Lanchuan Tech. Co., Ltd.
000C24	Anator
000C25	Allied Telesis Labs, Inc.
000C26	Weintek Labs. Inc.
000C27	Sammy Corporation
000C28	Rifatron
000C29	VMware, Inc.
000C2A	OCTTEL Communication Co., Ltd.
000C2B	ELIAS Technology, Inc.
000C2C	Enwiser Inc.
000C2D	FullWave Technology Co., Ltd.
000C2E	Openet information technology(shenzhen) Co., Ltd.
000C2F	SeorimTechnology Co.,Ltd.
000C30	Cisco Systems, Inc
000C31	Cisco Systems, Inc
000C32	Avionic Design Development GmbH
000C33	Compucase Enterprise Co. Ltd.
000C34	Vixen Co., Ltd.
000C35	KaVo Dental GmbH & Co. KG
000C36	SHARP TAKAYA ELECTRONICS INDUSTRY CO.,LTD.
000C37	Geomation, Inc.
000C38	TelcoBridges Inc.
000C39	Sentinel Wireless Inc.
000C3A	Oxance
000C3B	Orion Electric Co., Ltd.
000C3C	MediaChorus, Inc.
000C3D	Glsystech Co., Ltd.
000C3E	Crest Audio
000C3F	Cogent Defence & Security Networks,
000C40	Altech Controls
000C41	Cisco-Linksys, LLC
000C42	Routerboard.com
000C43	Ralink Technology, Corp.
000C44	Automated Interfaces, Inc.
000C45	Animation Technologies Inc.
000C46	Allied Telesyn Inc.
000C47	SK Teletech(R&D Planning Team)
000C48	QoStek Corporation
000C49	Dangaard Telecom Denmark A/S
000C4A	Cygnus Microsystems (P) Limited
000C4B	Cheops Elektronik
000C4C	ArcorAg&               # Arcor AG&Co.
000C4D	Curtiss-               # Curtiss-Wright Controls Avionics & Electronics
000C4E	Winbest Technology CO,LT
000C4F	UDTech Japan Corporation
000C50	Seagate Technology
000C51	Scientific Technologies Inc.
000C52	Roll Systems Inc.
000C53	Private
000C54	Pedestal Networks, Inc
000C55	Microlink Communications Inc.
000C56	Megatel Computer (1986) Corp.
000C57	MACKIE Engineering Services Belgium BVBA
000C58	M&S Systems
000C59	Indyme Electronics, Inc.
000C5A	IBSmm Embedded Electronics Consulting
000C5B	HANWANG TECHNOLOGY CO.,LTD
000C5C	GTN Systems B.V.
000C5D	CHIC TECHNOLOGY (CHINA) CORP.
000C5E	Calypso Medical
000C5F	Avtec, Inc.
000C60	ACM Systems
000C61	AC Tech corporation DBA Advanced Digital
000C62	AbbCewe-               # ABB AB, Cewe-Control
000C63	Zenith Electronics Corporation
000C64	X2 MSA Group
000C65	Sunin Telecom
000C66	Pronto Networks Inc
000C67	OYO ELECTRIC CO.,LTD
000C68	SigmaTel, Inc.
000C69	National Radio Astronomy Observatory
000C6A	Mbari
000C6B	Kurz Industrie-Elektronik GmbH
000C6C	Elgato Systems LLC
000C6D	Edwards Ltd.
000C6E	ASUSTek COMPUTER INC.
000C6F	Amtek system co.,LTD.
000C70	ACC GmbH
000C71	Wybron, Inc
000C72	Tempearl Industrial Co., Ltd.
000C73	TELSON ELECTRONICS CO., LTD
000C74	RIVERTEC CORPORATION
000C75	Oriental integrated electronics. LTD
000C76	MICRO-STAR INTERNATIONAL CO., LTD.
000C77	Life Racing Ltd
000C78	In-Tech Electronics Limited
000C79	Extel Communications P/L
000C7A	DaTARIUS Technologies GmbH
000C7B	ALPHA PROJECT Co.,Ltd.
000C7C	Internet Information Image Inc.
000C7D	TEIKOKU ELECTRIC MFG. CO., LTD
000C7E	Tellium Incorporated
000C7F	synertronixx GmbH
000C80	Opelcomm Inc.
000C81	Schneider Electric (Australia)
000C82	NETWORK TECHNOLOGIES INC
000C83	Logical Solutions
000C84	Eazix, Inc.
000C85	Cisco Systems, Inc
000C86	Cisco Systems, Inc
000C87	Amd
000C88	Apache Micro Peripherals, Inc.
000C89	AC Electric Vehicles, Ltd.
000C8A	Bose Corporation
000C8B	Connect Tech Inc
000C8C	KODICOM CO.,LTD.
000C8D	MATRIX VISION GmbH
000C8E	Mentor Engineering Inc
000C8F	Nergal s.r.l.
000C90	Octasic Inc.
000C91	Riverhead Networks Inc.
000C92	WolfVision Gmbh
000C93	Xeline Co., Ltd.
000C94	United Electronic Industries, Inc. (EUI)
000C95	Primenet
000C96	OQO, Inc.
000C97	NV ADB TTV Technologies SA
000C98	LETEK Communications Inc.
000C99	HITEL LINK Co.,Ltd
000C9A	Hitech Electronics Corp.
000C9B	EE Solutions, Inc
000C9C	Chongho information & communications
000C9D	UbeeAirWalk, Inc.
000C9E	MemoryLink Corp.
000C9F	NKE Corporation
000CA0	StorCase Technology, Inc.
000CA1	SIGMACOM Co., LTD.
000CA2	Harmonic Video Network
000CA3	Rancho Technology, Inc.
000CA4	Prompttec Product Management GmbH
000CA5	Naman NZ LTd
000CA6	Mintera Corporation
000CA7	Metro (Suzhou) Technologies Co., Ltd.
000CA8	Garuda Networks Corporation
000CA9	Ebtron Inc.
000CAA	Cubic Transportation Systems Inc
000CAB	COMMEND International
000CAC	Citizen Watch Co., Ltd.
000CAD	BTU International
000CAE	Ailocom Oy
000CAF	TRI TERM CO.,LTD.
000CB0	Star Semiconductor Corporation
000CB1	Salland Engineering (Europe) BV
000CB2	UNION co., ltd.
000CB3	ROUND Co.,Ltd.
000CB4	AutoCell Laboratories, Inc.
000CB5	Premier Technolgies, Inc
000CB6	NANJING SEU MOBILE & INTERNET TECHNOLOGY CO.,LTD
000CB7	Nanjing Huazhuo Electronics Co., Ltd.
000CB8	MEDION AG
000CB9	Lea
000CBA	Jamex, Inc.
000CBB	ISKRAEMECO
000CBC	Iscutum
000CBD	Interface Masters, Inc
000CBE	Innominate Security Technologies AG
000CBF	Holy Stone Ent. Co., Ltd.
000CC0	Genera Oy
000CC1	Eaton Corporation
000CC2	ControlNet (India) Private Limited
000CC3	BeWAN systems
000CC4	Tiptel AG
000CC5	Nextlink Co., Ltd.
000CC6	Ka-Ro electronics GmbH
000CC7	Intelligent Computer Solutions Inc.
000CC8	Xytronix Research & Design, Inc.
000CC9	ILWOO DATA & TECHNOLOGY CO.,LTD
000CCA	HGST a Western Digital Company
000CCB	Design Combus Ltd
000CCC	Aeroscout Ltd.
000CCD	IEC - TC57
000CCE	Cisco Systems, Inc
000CCF	Cisco Systems, Inc
000CD0	Symetrix
000CD1	SFOM Technology Corp.
000CD2	Schaffner EMV AG
000CD3	Prettl Elektronik Radeberg GmbH
000CD4	Positron Public Safety Systems inc.
000CD5	Passave Inc.
000CD6	PARTNER TECH
000CD7	Nallatech Ltd
000CD8	M. K. Juchheim GmbH & Co
000CD9	Itcare Co., Ltd
000CDA	FreeHand Systems, Inc.
000CDB	Brocade Communications Systems, Inc.
000CDC	BECS Technology, Inc
000CDD	AOS technologies AG
000CDE	ABB STOTZ-KONTAKT GmbH
000CDF	PULNiX America, Inc
000CE0	Trek Diagnostics Inc.
000CE1	The Open Group
000CE2	Rolls-Royce
000CE3	Option International N.V.
000CE4	NeuroCom International, Inc.
000CE5	ARRIS Group, Inc.
000CE6	Meru Networks Inc
000CE7	MediaTek Inc.
000CE8	GuangZhou AnJuBao Co., Ltd
000CE9	BLOOMBERG L.P.
000CEA	aphona Kommunikationssysteme
000CEB	CNMP Networks, Inc.
000CEC	Spectracom Corp.
000CED	Real Digital Media
000CEE	jp-embedded
000CEF	Open Networks Engineering Ltd
000CF0	M & N GmbH
000CF1	Intel Corporation
000CF2	GAMESA Eólica
000CF3	CALL IMAGE SA
000CF4	AKATSUKI ELECTRIC MFG.CO.,LTD.
000CF5	InfoExpress
000CF6	Sitecom Europe BV
000CF7	Nortel Networks
000CF8	Nortel Networks
000CF9	Xylem Water Solutions
000CFA	Digital Systems Corp
000CFB	Korea Network Systems
000CFC	S2io Technologies Corp
000CFD	Hyundai ImageQuest Co.,Ltd.
000CFE	Grand Electronic Co., Ltd
000CFF	MRO-TEK LIMITED
000D00	Seaway Networks Inc.
000D01	P&E Microcomputer Systems, Inc.
000D02	NEC Platforms, Ltd.
000D03	Matrics, Inc.
000D04	Foxboro Eckardt Development GmbH
000D05	cybernet manufacturing inc.
000D06	Compulogic Limited
000D07	Calrec Audio Ltd
000D08	AboveCable, Inc.
000D09	Yuehua(Zhuhai) Electronic CO. LTD
000D0A	Projectiondesign as
000D0B	BUFFALO.INC
000D0C	MDI Security Systems
000D0D	ITSupported, LLC
000D0E	Inqnet Systems, Inc.
000D0F	Finlux Ltd
000D10	Embedtronics Oy
000D11	DENTSPLY - Gendex
000D12	AXELL Corporation
000D13	Wilhelm Rutenbeck GmbH&Co.KG
000D14	Vtech Innovation LP dba Advanced American Telephones
000D15	Voipac s.r.o.
000D16	UHS Systems Pty Ltd
000D17	Turbo Networks Co.Ltd
000D18	Mega-Trend Electronics CO., LTD.
000D19	ROBE Show lighting
000D1A	Mustek System Inc.
000D1B	Kyoto Electronics Manufacturing Co., Ltd.
000D1C	Amesys Defense
000D1D	HIGH-TEK HARNESS ENT. CO., LTD.
000D1E	Control Techniques
000D1F	AV Digital
000D20	ASAHIKASEI TECHNOSYSTEM CO.,LTD.
000D21	WISCORE Inc.
000D22	Unitronics LTD
000D23	Smart Solution, Inc
000D24	SentecE&               # SENTEC E&E CO., LTD.
000D25	SANDEN CORPORATION
000D26	Primagraphics Limited
000D27	MICROPLEX Printware AG
000D28	Cisco Systems, Inc
000D29	Cisco Systems, Inc
000D2A	Scanmatic AS
000D2B	Racal Instruments
000D2C	Net2Edge Limited
000D2D	NCT Deutschland GmbH
000D2E	Matsushita Avionics Systems Corporation
000D2F	AIN Comm.Tech.Co., LTD
000D30	IceFyre Semiconductor
000D31	Compellent Technologies, Inc.
000D32	DispenseSource, Inc.
000D33	Prediwave Corp.
000D34	Shell International Exploration and Production, Inc.
000D35	PAC International Ltd
000D36	Wu Han Routon Electronic Co., Ltd
000D37	Wiplug
000D38	NISSIN INC.
000D39	Network Electronics
000D3A	Microsoft Corp.
000D3B	Microelectronics Technology Inc.
000D3C	i.Tech Dynamic Ltd
000D3D	Hammerhead Systems, Inc.
000D3E	APLUX Communications Ltd.
000D3F	VTI Instruments Corporation
000D40	Verint Loronix Video Solutions
000D41	Siemens AG ICM MP UC RD IT KLF1
000D42	Newbest Development Limited
000D43	DRS Tactical Systems Inc.
000D44	AudioBu-               # Audio BU - Logitech
000D45	Tottori SANYO Electric Co., Ltd.
000D46	Parker SSD Drives
000D47	Collex
000D48	AEWIN Technologies Co., Ltd.
000D49	Triton Systems of Delaware, Inc.
000D4A	Steag ETA-Optik
000D4B	Roku, Inc.
000D4C	Outline Electronics Ltd.
000D4D	Ninelanes
000D4E	NDR Co.,LTD.
000D4F	Kenwood Corporation
000D50	Galazar Networks
000D51	DIVR Systems, Inc.
000D52	Comart system
000D53	Beijing 5w Communication Corp.
000D54	3Com Ltd
000D55	SANYCOM Technology Co.,Ltd
000D56	Dell Inc.
000D57	Fujitsu I-Network Systems Limited.
000D58	Private
000D59	Amity Systems, Inc.
000D5A	Tiesse SpA
000D5B	Smart Empire Investments Limited
000D5C	Robert Bosch GmbH, VT-ATMO
000D5D	Raritan Computer, Inc
000D5E	NEC Personal Products
000D5F	Minds Inc
000D60	IBM Corp
000D61	Giga-Byte Technology Co., Ltd.
000D62	Funkwerk Dabendorf GmbH
000D63	DENT Instruments, Inc.
000D64	COMAG Handels AG
000D65	Cisco Systems, Inc
000D66	Cisco Systems, Inc
000D67	Ericsson
000D68	Vinci Systems, Inc.
000D69	TMT&D Corporation
000D6A	Redwood Technologies LTD
000D6B	Mita-Teknik A/S
000D6C	M-Audio
000D6D	K-Tech Devices Corp.
000D6E	K-Patents Oy
000D6F	Ember Corporation
000D70	Datamax Corporation
000D71	boca systems
000D72	2Wire Inc
000D73	Technical Support, Inc.
000D74	Sand Network Systems, Inc.
000D75	Kobian Pte Ltd - Taiwan Branch
000D76	Hokuto Denshi Co,. Ltd.
000D77	FalconStor Software
000D78	Engineering & Security
000D79	Dynamic Solutions Co,.Ltd.
000D7A	DiGATTO Asia Pacific Pte Ltd
000D7B	Consensys Computers Inc.
000D7C	Codian Ltd
000D7D	Afco Systems
000D7E	Axiowave Networks, Inc.
000D7F	MIDAS  COMMUNICATION TECHNOLOGIES PTE LTD ( Foreign Branch)
000D80	Online Development Inc
000D81	Pepperl+               # Pepperl+Fuchs GmbH
000D82	PHS srl
000D83	Sanmina-               # Sanmina-SCI Hungary  Ltd.
000D84	Makus Inc.
000D85	Tapwave, Inc.
000D86	Huber + Suhner AG
000D87	Elitegroup Computer Systems Co.,Ltd.
000D88	D-Link Corporation
000D89	Bils Technology Inc
000D8A	Winners Electronics Co., Ltd.
000D8B	T&D Corporation
000D8C	Shanghai Wedone Digital Ltd. CO.
000D8D	Prosoft Technology, Inc
000D8E	Koden Electronics Co., Ltd.
000D8F	King Tsushin Kogyo Co., LTD.
000D90	Factum Electronics AB
000D91	Eclipse (HQ Espana) S.L.
000D92	ARIMA Communications Corp.
000D93	Apple, Inc.
000D94	AFAR Communications,Inc
000D95	Opti-cell, Inc.
000D96	Vtera Technology Inc.
000D97	ABB Inc./Tropos
000D98	S.W.A.C. Schmitt-Walter Automation Consult GmbH
000D99	Orbital Sciences Corp.; Launch Systems Group
000D9A	INFOTEC LTD
000D9B	Heraeus Electro-Nite International N.V.
000D9C	Elan GmbH & Co KG
000D9D	Hewlett Packard
000D9E	TOKUDEN OHIZUMI SEISAKUSYO Co.,Ltd.
000D9F	RF Micro Devices
000DA0	NEDAP N.V.
000DA1	MIRAE ITS Co.,LTD.
000DA2	Infrant Technologies, Inc.
000DA3	Emerging Technologies Limited
000DA4	DOSCH & AMAND SYSTEMS AG
000DA5	Fabric7 Systems, Inc
000DA6	Universal Switching Corporation
000DA7	Private
000DA8	Teletronics Technology Corporation
000DA9	T.E.A.M. S.L.
000DAA	S.A.Tehnology co.,Ltd.
000DAB	Parker Hannifin GmbH Electromechanical Division Europe
000DAC	Japan CBM Corporation
000DAD	Dataprobe, Inc.
000DAE	SAMSUNG HEAVY INDUSTRIES CO., LTD.
000DAF	Plexus Corp (UK) Ltd
000DB0	Olym-tech Co.,Ltd.
000DB1	Japan Network Service Co., Ltd.
000DB2	Ammasso, Inc.
000DB3	SDO Communication Corperation
000DB4	Netasq
000DB5	GLOBALSAT TECHNOLOGY CORPORATION
000DB6	Broadcom
000DB7	SANKO ELECTRIC CO,.LTD
000DB8	SCHILLER AG
000DB9	PC Engines GmbH
000DBA	Océ Document Technologies GmbH
000DBB	Nippon Dentsu Co.,Ltd.
000DBC	Cisco Systems, Inc
000DBD	Cisco Systems, Inc
000DBE	Bel Fuse Europe Ltd.,UK
000DBF	TekTone Sound & Signal Mfg., Inc.
000DC0	Spagat AS
000DC1	SafeWeb Inc
000DC2	Private
000DC3	First Communication, Inc.
000DC4	Emcore Corporation
000DC5	EchoStar Global B.V.
000DC6	DigiRose Technology Co., Ltd.
000DC7	COSMIC ENGINEERING INC.
000DC8	AirMagnet, Inc
000DC9	THALES Elektronik Systeme GmbH
000DCA	Tait Electronics
000DCB	Petcomkorea Co., Ltd.
000DCC	NEOSMART Corp.
000DCD	GROUPE TXCOM
000DCE	Dynavac Technology Pte Ltd
000DCF	Cidra Corp.
000DD0	TetraTec Instruments GmbH
000DD1	Stryker Corporation
000DD2	Simrad Optronics ASA
000DD3	SAMWOO Telecommunication Co.,Ltd.
000DD4	Symantec Corporation
000DD5	O'RITE TECHNOLOGY CO.,LTD
000DD6	ITI    LTD
000DD7	Bright
000DD8	Bbn
000DD9	Anton Paar GmbH
000DDA	ALLIED TELESIS K.K.
000DDB	AIRWAVE TECHNOLOGIES INC.
000DDC	Vac
000DDD	Profilo Telra Elektronik Sanayi ve Ticaret. A.Ş
000DDE	Joyteck Co., Ltd.
000DDF	Japan Image & Network Inc.
000DE0	ICPDAS Co.,LTD
000DE1	Control Products, Inc.
000DE2	CMZ Sistemi Elettronici
000DE3	AT Sweden AB
000DE4	DIGINICS, Inc.
000DE5	Samsung Thales
000DE6	YOUNGBO ENGINEERING CO.,LTD
000DE7	Snap-on OEM Group
000DE8	Nasaco Electronics Pte. Ltd
000DE9	Napatech Aps
000DEA	Kingtel Telecommunication Corp.
000DEB	CompXs Limited
000DEC	Cisco Systems, Inc
000DED	Cisco Systems, Inc
000DEE	Andrew RF Power Amplifier Group
000DEF	Soc. Coop. Bilanciai
000DF0	QCOM TECHNOLOGY INC.
000DF1	IONIX INC.
000DF2	Private
000DF3	Asmax Solutions
000DF4	Watertek Co.
000DF5	Teletronics International Inc.
000DF6	Technology Thesaurus Corp.
000DF7	Space Dynamics Lab
000DF8	ORGA Kartensysteme GmbH
000DF9	NDS Limited
000DFA	Micro Control Systems Ltd.
000DFB	Komax AG
000DFC	ITFOR Inc.
000DFD	HugesHi-               # Huges Hi-Tech Inc.,
000DFE	Hauppauge Computer Works, Inc.
000DFF	CHENMING MOLD INDUSTRY CORP.
000E00	Atrie
000E01	ASIP Technologies Inc.
000E02	Advantech AMT Inc.
000E03	Emulex Corporation
000E04	CMA/Microdialysis AB
000E05	WIRELESS MATRIX CORP.
000E06	Team Simoco Ltd
000E07	Sony Mobile Communications AB
000E08	Cisco-Linksys, LLC
000E09	Shenzhen Coship Software Co.,LTD.
000E0A	SAKUMA DESIGN OFFICE
000E0B	Netac Technology Co., Ltd.
000E0C	Intel Corporation
000E0D	Hesch Schröder GmbH
000E0E	ESA elettronica S.P.A.
000E0F	Ermme
000E10	C-guys, Inc.
000E11	BDT Büro und Datentechnik GmbH & Co.KG
000E12	Adaptive Micro Systems Inc.
000E13	Accu-Sort Systems inc.
000E14	Visionary Solutions, Inc.
000E15	Tadlys LTD
000E16	SouthWing S.L.
000E17	Private
000E18	MyA Technology
000E19	LogicaCMG Pty Ltd
000E1A	JPS Communications
000E1B	IAV GmbH
000E1C	Hach Company
000E1D	ARION Technology Inc.
000E1E	QLogic Corporation
000E1F	TCL Networks Equipment Co., Ltd.
000E20	ACCESS Systems Americas, Inc.
000E21	MTU Friedrichshafen GmbH
000E22	Private
000E23	Incipient, Inc.
000E24	Huwell Technology Inc.
000E25	Hannae Technology Co., Ltd
000E26	Gincom Technology Corp.
000E27	Crere Networks, Inc.
000E28	Dynamic Ratings P/L
000E29	Shester Communications Inc
000E2A	Private
000E2B	Safari Technologies
000E2C	Netcodec co.
000E2D	Hyundai Digital Technology Co.,Ltd.
000E2E	Edimax Technology Co. Ltd.
000E2F	Roche Diagnostics GmbH
000E30	AERAS Networks, Inc.
000E31	Olympus Soft Imaging Solutions GmbH
000E32	Kontron Medical
000E33	Shuko Electronics Co.,Ltd
000E34	NexGen City, LP
000E35	Intel Corporation
000E36	HEINESYS, Inc.
000E37	Harms & Wende GmbH & Co.KG
000E38	Cisco Systems, Inc
000E39	Cisco Systems, Inc
000E3A	Cirrus Logic
000E3B	Hawking Technologies, Inc.
000E3C	Transact Technologies Inc
000E3D	Televic N.V.
000E3E	Sun Optronics Inc
000E3F	Soronti, Inc.
000E40	Nortel Networks
000E41	NIHON MECHATRONICS CO.,LTD.
000E42	Motic Incoporation Ltd.
000E43	G-Tek Electronics Sdn. Bhd.
000E44	Digital 5, Inc.
000E45	Beijing Newtry Electronic Technology Ltd
000E46	Niigata Seimitsu Co.,Ltd.
000E47	NCI System Co.,Ltd.
000E48	Lipman TransAction Solutions
000E49	Forsway Scandinavia AB
000E4A	Changchun Huayu WEBPAD Co.,LTD
000E4B	atrium c and i
000E4C	Bermai Inc.
000E4D	Numesa Inc.
000E4E	Waveplus Technology Co., Ltd.
000E4F	Trajet GmbH
000E50	Thomson Telecom Belgium
000E51	tecna elettronica srl
000E52	Optium Corporation
000E53	AV TECH CORPORATION
000E54	AlphaCell Wireless Ltd.
000E55	Auvitran
000E56	4G Systems GmbH & Co. KG
000E57	Iworld Networking, Inc.
000E58	Sonos, Inc.
000E59	Sagemcom Broadband SAS
000E5A	TELEFIELD inc.
000E5B	ParkerVision - Direct2Data
000E5C	ARRIS Group, Inc.
000E5D	Triple Play Technologies A/S
000E5E	Raisecom Technology
000E5F	activ-net GmbH & Co. KG
000E60	360SUN Digital Broadband Corporation
000E61	MICROTROL LIMITED
000E62	Nortel Networks
000E63	Lemke Diagnostics GmbH
000E64	Elphel, Inc
000E65	TransCore
000E66	Hitachi Industry & Control Solutions, Ltd.
000E67	Eltis Microelectronics Ltd.
000E68	E-TOP Network Technology Inc.
000E69	China Electric Power Research Institute
000E6A	3Com Ltd
000E6B	Janitza electronics GmbH
000E6C	Device Drivers Limited
000E6D	Murata Manufacturing Co., Ltd.
000E6E	MAT S.A. (Mircrelec Advanced Technology)
000E6F	IRIS Corporation Berhad
000E70	in2 Networks
000E71	Gemstar Technology Development Ltd.
000E72	CTS electronics
000E73	Tpack A/S
000E74	Solar Telecom. Tech
000E75	New York Air Brake Corp.
000E76	GEMSOC INNOVISION INC.
000E77	Decru, Inc.
000E78	Amtelco
000E79	Ample Communications Inc.
000E7A	GemWon Communications Co., Ltd.
000E7B	Toshiba
000E7C	Televes S.A.
000E7D	Electronics Line 3000 Ltd.
000E7E	ionSign Oy
000E7F	Hewlett Packard
000E80	Thomson Technology Inc
000E81	Devicescape Software, Inc.
000E82	Commtech Wireless
000E83	Cisco Systems, Inc
000E84	Cisco Systems, Inc
000E85	Catalyst Enterprises, Inc.
000E86	Alcatel North America
000E87	adp Gauselmann GmbH
000E88	VIDEOTRON CORP.
000E89	Clematic
000E8A	Avara Technologies Pty. Ltd.
000E8B	Astarte Technology Co, Ltd.
000E8C	Siemens AG A&D ET
000E8D	Systems in Progress Holding GmbH
000E8E	SparkLAN Communications, Inc.
000E8F	Sercomm Corp.
000E90	PONICO CORP.
000E91	Navico Auckland Ltd
000E92	Open Telecom
000E93	Milénio 3 Sistemas Electrónicos, Lda.
000E94	Maas International BV
000E95	Fujiya Denki Seisakusho Co.,Ltd.
000E96	Cubic Defense Applications, Inc.
000E97	Ultracker Technology CO., Inc
000E98	HME Clear-Com LTD.
000E99	Spectrum Digital, Inc
000E9A	BOE TECHNOLOGY GROUP CO.,LTD
000E9B	Ambit Microsystems Corporation
000E9C	Benchmark Electronics
000E9D	Tiscali UK Ltd
000E9E	Topfield Co., Ltd
000E9F	TEMIC SDS GmbH
000EA0	NetKlass Technology Inc.
000EA1	Formosa Teletek Corporation
000EA2	McAfee, Inc
000EA3	CNCR-IT CO.,LTD,HangZhou P.R.CHINA
000EA4	Certance Inc.
000EA5	BLIP Systems
000EA6	ASUSTek COMPUTER INC.
000EA7	Endace Technology
000EA8	United Technologists Europe Limited
000EA9	Shanghai Xun Shi Communications Equipment Ltd. Co.
000EAA	Scalent Systems, Inc.
000EAB	Cray Inc
000EAC	MINTRON ENTERPRISE CO., LTD.
000EAD	Metanoia Technologies, Inc.
000EAE	GAWELL TECHNOLOGIES CORP.
000EAF	Castel
000EB0	Solutions Radio BV
000EB1	Newcotech,Ltd
000EB2	Micro-Research Finland Oy
000EB3	Hewlett Packard
000EB4	GUANGZHOU GAOKE COMMUNICATIONS TECHNOLOGY CO.LTD.
000EB5	Ecastle Electronics Co., Ltd.
000EB6	Riverbed Technology, Inc.
000EB7	Knovative, Inc.
000EB8	Iiga co.,Ltd
000EB9	HASHIMOTO Electronics Industry Co.,Ltd.
000EBA	HANMI SEMICONDUCTOR CO., LTD.
000EBB	Everbee Networks
000EBC	Paragon Fidelity GmbH
000EBD	Burdick, a Quinton Compny
000EBE	B&B Electronics Manufacturing Co.
000EBF	Remsdaq Limited
000EC0	Nortel Networks
000EC1	MYNAH Technologies
000EC2	Lowrance Electronics, Inc.
000EC3	Logic Controls, Inc.
000EC4	Iskra Transmission d.d.
000EC5	Digital Multitools Inc
000EC6	ASIX ELECTRONICS CORP.
000EC7	Motorola Korea
000EC8	Zoran Corporation
000EC9	YOKO Technology Corp.
000ECA	WTSS Inc
000ECB	VineSys Technology
000ECC	Tableau, LLC
000ECD	SKOV A/S
000ECE	S.I.T.T.I. S.p.A.
000ECF	PROFIBUS Nutzerorganisation e.V.
000ED0	Privaris, Inc.
000ED1	Osaka Micro Computer.
000ED2	Filtronic plc
000ED3	Epicenter, Inc.
000ED4	CRESITT INDUSTRIE
000ED5	COPAN Systems Inc.
000ED6	Cisco Systems, Inc
000ED7	Cisco Systems, Inc
000ED8	Positron Access Solutions Corp
000ED9	Aksys, Ltd.
000EDA	C-TECH UNITED CORP.
000EDB	XiNCOM Corp.
000EDC	Tellion INC.
000EDD	SHURE INCORPORATED
000EDE	REMEC, Inc.
000EDF	PLX Technology
000EE0	Mcharge
000EE1	ExtremeSpeed Inc.
000EE2	Custom Engineering
000EE3	Chiyu Technology Co.,Ltd
000EE4	BOE TECHNOLOGY GROUP CO.,LTD
000EE5	bitWallet, Inc.
000EE6	Adimos Systems LTD
000EE7	AAC ELECTRONICS CORP.
000EE8	Zioncom Electronics (Shenzhen) Ltd.
000EE9	WayTech Development, Inc.
000EEA	Shadong Luneng Jicheng Electronics,Co.,Ltd
000EEB	Sandmartin(zhong shan)Electronics Co.,Ltd
000EEC	Orban
000EED	Nokia Danmark A/S
000EEE	Muco Industrie BV
000EEF	Private
000EF0	Festo AG & Co. KG
000EF1	EZQUEST INC.
000EF2	Infinico Corporation
000EF3	Smarthome
000EF4	Kasda Networks Inc
000EF5	iPAC Technology Co., Ltd.
000EF6	E-TEN Information Systems Co., Ltd.
000EF7	Vulcan Portals Inc
000EF8	SBC ASI
000EF9	REA Elektronik GmbH
000EFA	Optoway Technology Incorporation
000EFB	Macey Enterprises
000EFC	JTAG Technologies B.V.
000EFD	FUJINON CORPORATION
000EFE	EndRun Technologies LLC
000EFF	Megasolution,Inc.
000F00	Legra Systems, Inc.
000F01	DIGITALKS INC
000F02	Digicube Technology Co., Ltd
000F03	COM&C CO., LTD
000F04	cim-usa inc
000F05	3B SYSTEM INC.
000F06	Nortel Networks
000F07	Mangrove Systems, Inc.
000F08	Indagon Oy
000F09	Private
000F0A	Clear Edge Networks
000F0B	Kentima Technologies AB
000F0C	SYNCHRONIC ENGINEERING
000F0D	Hunt Electronic Co., Ltd.
000F0E	WaveSplitter Technologies, Inc.
000F0F	Real ID Technology Co., Ltd.
000F10	RDM Corporation
000F11	Prodrive B.V.
000F12	Panasonic Europe Ltd.
000F13	Nisca corporation
000F14	Mindray Co., Ltd.
000F15	Kjaerulff1 A/S
000F16	JAY HOW TECHNOLOGY CO.,
000F17	Insta Elektro GmbH
000F18	Industrial Control Systems
000F19	Boston Scientific
000F1A	Gaming Support B.V.
000F1B	Ego Systems Inc.
000F1C	DigitAll World Co., Ltd
000F1D	Cosmo Techs Co., Ltd.
000F1E	Chengdu KT Electric Co.of High & New Technology
000F1F	Dell Inc.
000F20	Hewlett Packard
000F21	Scientific Atlanta, Inc
000F22	Helius, Inc.
000F23	Cisco Systems, Inc
000F24	Cisco Systems, Inc
000F25	AimValley B.V.
000F26	WorldAccxx  LLC
000F27	TEAL Electronics, Inc.
000F28	Itronix Corporation
000F29	Augmentix Corporation
000F2A	Cableware Electronics
000F2B	GREENBELL SYSTEMS
000F2C	Uplogix, Inc.
000F2D	CHUNG-HSIN ELECTRIC & MACHINERY MFG.CORP.
000F2E	Megapower International Corp.
000F2F	W-LINX TECHNOLOGY CO., LTD.
000F30	Raza Microelectronics Inc
000F31	Allied Vision Technologies Canada Inc
000F32	Lootom Telcovideo Network Wuxi Co Ltd
000F33	DUALi Inc.
000F34	Cisco Systems, Inc
000F35	Cisco Systems, Inc
000F36	Accurate Techhnologies, Inc.
000F37	Xambala Incorporated
000F38	Netstar
000F39	IRIS SENSORS
000F3A	Hisharp
000F3B	Fuji System Machines Co., Ltd.
000F3C	Endeleo Limited
000F3D	D-Link Corporation
000F3E	CardioNet, Inc
000F3F	Big Bear Networks
000F40	Optical Internetworking Forum
000F41	Zipher Ltd
000F42	Xalyo Systems
000F43	Wasabi Systems Inc.
000F44	Tivella Inc.
000F45	Stretch, Inc.
000F46	SINAR AG
000F47	ROBOX SPA
000F48	Polypix Inc.
000F49	Northover Solutions Limited
000F4A	Kyushu-kyohan co.,ltd
000F4B	Oracle Corporation
000F4C	Elextech INC
000F4D	TalkSwitch
000F4E	Cellink
000F4F	PCS Systemtechnik GmbH
000F50	StreamScale Limited
000F51	Azul Systems, Inc.
000F52	YORK Refrigeration, Marine & Controls
000F53	Solarflare Communications Inc
000F54	Entrelogic Corporation
000F55	Datawire Communication Networks Inc.
000F56	Continuum Photonics Inc
000F57	CABLELOGIC Co., Ltd.
000F58	Adder Technology Limited
000F59	Phonak AG
000F5A	Peribit Networks
000F5B	Delta Information Systems, Inc.
000F5C	Day One Digital Media Limited
000F5D	Genexis BV
000F5E	Veo
000F5F	Nicety Technologies Inc. (NTS)
000F60	Lifetron Co.,Ltd
000F61	Hewlett Packard
000F62	Alcatel Bell Space N.V.
000F63	Obzerv Technologies
000F64	D&R Electronica Weesp BV
000F65	icube Corp.
000F66	Cisco-Linksys, LLC
000F67	West Instruments
000F68	Vavic Network Technology, Inc.
000F69	SEW Eurodrive GmbH & Co. KG
000F6A	Nortel Networks
000F6B	GateWare Communications GmbH
000F6C	ADDI-DATA GmbH
000F6D	Midas Engineering
000F6E	Bbox
000F6F	FTA Communication Technologies
000F70	Wintec Industries, inc.
000F71	Sanmei Electronics Co.,Ltd
000F72	Sandburst
000F73	RS Automation Co., Ltd
000F74	Qamcom Technology AB
000F75	First Silicon Solutions
000F76	Digital Keystone, Inc.
000F77	DENTUM CO.,LTD
000F78	Datacap Systems Inc
000F79	Bluetooth Interest Group Inc.
000F7A	BeiJing NuQX Technology CO.,LTD
000F7B	Arce Sistemas, S.A.
000F7C	ACTi Corporation
000F7D	Xirrus
000F7E	Ablerex Electronics Co., LTD
000F7F	UBSTORAGE Co.,Ltd.
000F80	Trinity Security Systems,Inc.
000F81	PAL Pacific Inc.
000F82	Mortara Instrument, Inc.
000F83	Brainium Technologies Inc.
000F84	Astute Networks, Inc.
000F85	ADDO-Japan Corporation
000F86	BlackBerry RTS
000F87	Maxcess International
000F88	AMETEK, Inc.
000F89	Winnertec System Co., Ltd.
000F8A	Wideview
000F8B	Orion MultiSystems Inc
000F8C	Gigawavetech Pte Ltd
000F8D	FAST TV-Server AG
000F8E	DONGYANG TELECOM CO.,LTD.
000F8F	Cisco Systems, Inc
000F90	Cisco Systems, Inc
000F91	Aerotelecom Co.,Ltd.
000F92	Microhard Systems Inc.
000F93	Landis+Gyr Ltd.
000F94	Genexis BV
000F95	ELECOM Co.,LTD Laneed Division
000F96	Telco Systems, Inc.
000F97	Avanex Corporation
000F98	Avamax Co. Ltd.
000F99	APAC opto Electronics Inc.
000F9A	Synchrony, Inc.
000F9B	Ross Video Limited
000F9C	Panduit Corp
000F9D	DisplayLink (UK) Ltd
000F9E	Murrelektronik GmbH
000F9F	ARRIS Group, Inc.
000FA0	CANON KOREA BUSINESS SOLUTIONS INC.
000FA1	Gigabit Systems Inc.
000FA2	2xWireless
000FA3	Alpha Networks Inc.
000FA4	Sprecher Automation GmbH
000FA5	BWA Technology GmbH
000FA6	S2 Security Corporation
000FA7	Raptor Networks Technology
000FA8	Photometrics, Inc.
000FA9	PC Fabrik
000FAA	Nexus Technologies
000FAB	Kyushu Electronics Systems Inc.
000FAC	IEEE 802.11
000FAD	FMN communications GmbH
000FAE	E2O Communications
000FAF	Dialog Inc.
000FB0	COMPAL ELECTRONICS, INC.
000FB1	Cognio Inc.
000FB2	Broadband Pacenet (India) Pvt. Ltd.
000FB3	Actiontec Electronics, Inc
000FB4	Timespace Technology
000FB5	Netgear
000FB6	Europlex Technologies
000FB7	Cavium
000FB8	CallURL Inc.
000FB9	Adaptive Instruments
000FBA	Tevebox AB
000FBB	Nokia Siemens Networks GmbH & Co. KG.
000FBC	Onkey Technologies, Inc.
000FBD	MRV Communications (Networks) LTD
000FBE	e-w/you Inc.
000FBF	DGT Sp. z o.o.
000FC0	Delcomp
000FC1	WAVE Corporation
000FC2	Uniwell Corporation
000FC3	PalmPalm Technology, Inc.
000FC4	NST co.,LTD.
000FC5	KeyMed Ltd
000FC6	Eurocom Industries A/S
000FC7	Dionica R&D Ltd.
000FC8	Chantry Networks
000FC9	Allnet GmbH
000FCA	A-JIN TECHLINE CO, LTD
000FCB	3Com Ltd
000FCC	ARRIS Group, Inc.
000FCD	Nortel Networks
000FCE	Kikusui Electronics Corp.
000FCF	DataWind Research
000FD0	Astri
000FD1	Applied Wireless Identifications Group, Inc.
000FD2	EWA Technologies, Inc.
000FD3	Digium
000FD4	Soundcraft
000FD5	Schwechat - RISE
000FD6	Sarotech Co., Ltd
000FD7	Harman Music Group
000FD8	Force, Inc.
000FD9	FlexDSL Telecommunications AG
000FDA	YAZAKI CORPORATION
000FDB	Westell Technologies Inc.
000FDC	Ueda Japan  Radio Co., Ltd.
000FDD	SORDIN AB
000FDE	Sony Mobile Communications AB
000FDF	SOLOMON Technology Corp.
000FE0	NComputing Co.,Ltd.
000FE1	ID DIGITAL CORPORATION
000FE2	Hangzhou H3C Technologies Co., Limited
000FE3	Damm Cellular Systems A/S
000FE4	Pantech Co.,Ltd
000FE5	MERCURY SECURITY CORPORATION
000FE6	MBTech Systems, Inc.
000FE7	Lutron Electronics Co., Inc.
000FE8	Lobos, Inc.
000FE9	GW TECHNOLOGIES CO.,LTD.
000FEA	Giga-Byte Technology Co.,LTD.
000FEB	Cylon Controls
000FEC	ARKUS Inc.
000FED	Anam Electronics Co., Ltd
000FEE	XTec, Incorporated
000FEF	ThalesE-               # Thales e-Transactions GmbH
000FF0	Sunray Co. Ltd.
000FF1	nex-G Systems Pte.Ltd
000FF2	Loud Technologies Inc.
000FF3	Jung Myoung Communications&Technology
000FF4	Guntermann & Drunck GmbH
000FF5	GN&S company
000FF6	DARFON LIGHTING CORP
000FF7	Cisco Systems, Inc
000FF8	Cisco Systems, Inc
000FF9	Valcretec, Inc.
000FFA	Optinel Systems, Inc.
000FFB	Nippon Denso Industry Co., Ltd.
000FFC	MeritLi-               # Merit Li-Lin Ent.
000FFD	Glorytek Network Inc.
000FFE	G-PRO COMPUTER
000FFF	Control4
001000	CableLabs
001001	Citel
001002	Actia
001003	IMATRON, INC.
001004	THE BRANTLEY COILE COMPANY,INC
001005	UEC COMMERCIAL
001006	Thales Contact Solutions Ltd.
001007	Cisco Systems			Catalyst 1900
001008	VIENNA SYSTEMS CORPORATION
001009	HORO QUARTZ
00100A	WILLIAMS COMMUNICATIONS GROUP
00100B	Cisco Systems
00100C	ITO CO., LTD.
00100D	Cisco Systems			Catalyst 2924-XL
00100E	MICRO LINEAR COPORATION
00100F	INDUSTRIAL CPU SYSTEMS
001010	INITIO CORPORATION
001011	Cisco Systems			Cisco 75xx
001012	PROCESSOR SYSTEMS (I) PVT LTD
001013	Kontron America, Inc.
001014	Cisco Systems, Inc
001015	OOmon Inc.
001016	T.SQWARE
001017	Bosch Access Systems GmbH
001018	Broadcom
001019	SIRONA DENTAL SYSTEMS GmbH & Co. KG
00101A	PictureTel Corp.
00101B	CORNET TECHNOLOGY, INC.
00101C	OHM TECHNOLOGIES INTL, LLC
00101D	WINBOND ELECTRONICS CORP.
00101E	MATSUSHITA ELECTRONIC INSTRUMENTS CORP.
00101F	Cisco Systems			Catalyst 2901
001020	Hand Held Products Inc
001021	ENCANTO NETWORKS, INC.
001022	SatCom Media Corporation
001023	Network Equipment Technologies
001024	NAGOYA ELECTRIC WORKS CO., LTD
001025	Grayhill, Inc
001026	ACCELERATED NETWORKS, INC.
001027	L-3 COMMUNICATIONS EAST
001028	COMPUTER TECHNICA, INC.
001029	Cisco Systems			Catalyst 5000
00102A	ZF MICROSYSTEMS, INC.
00102B	UMAX DATA SYSTEMS, INC.
00102C	Lasat Networks A/S
00102D	HITACHI SOFTWARE ENGINEERING
00102E	NETWORK SYSTEMS & TECHNOLOGIES PVT. LTD.
00102F	Cisco Systems			Cisco 5000
001030	EION Inc.
001031	OBJECTIVE COMMUNICATIONS, INC.
001032	ALTA TECHNOLOGY
001033	ACCESSLAN COMMUNICATIONS, INC.
001034	GNP Computers
001035	Elitegroup Computer Systems Co.,Ltd.
001036	INTER-TEL INTEGRATED SYSTEMS
001037	CYQ've Technology Co., Ltd.
001038	MICRO RESEARCH INSTITUTE, INC.
001039	Vectron Systems AG
00103A	DIAMOND NETWORK TECH
00103B	HIPPI NETWORKING FORUM
00103C	IC ENSEMBLE, INC.
00103D	PHASECOM, LTD.
00103E	NETSCHOOLS CORPORATION
00103F	TOLLGRADE COMMUNICATIONS, INC.
001040	INTERMEC CORPORATION
001041	BRISTOL BABCOCK, INC.
001042	Alacritech, Inc.
001043	A2 CORPORATION
001044	InnoLabs Corporation
001045	Nortel Networks
001046	ALCORN MCBRIDE INC.
001047	ECHO ELETRIC CO. LTD.
001048	HTRC AUTOMATION, INC.
001049	ShoreTel, Inc
00104A	The Parvus Corporation
00104B	3Com				3C905-TX PCI
00104C	Teledyne LeCroy, Inc
00104D	SURTEC INDUSTRIES, INC.
00104E	Ceologic
00104F	Oracle Corporation
001050	RION CO., LTD.
001051	CMICRO CORPORATION
001052	Mettler-               # METTLER-TOLEDO (ALBSTADT) GMBH
001053	COMPUTER TECHNOLOGY CORP.
001054	Cisco Systems, Inc
001055	FUJITSU MICROELECTRONICS, INC.
001056	SODICK CO., LTD.
001057	Rebel.com, Inc.
001058	ArrowPoint Communications
001059	DIABLO RESEARCH CO. LLC
00105A	3Com				Fast Etherlink XL in a Gateway 2000
00105B	NET INSIGHT AB
00105C	QUANTUM DESIGNS (H.K.) LTD.
00105D	Draeger Medical
00105E	Spirent plc, Service Assurance Broadband
00105F	ZODIAC DATA SYSTEMS
001060	Billington			Novell NE200 Compatible
001061	HOSTLINK CORP.
001062	NX SERVER, ILNC.
001063	STARGUIDE DIGITAL NETWORKS
001064	DNPG, LLC
001065	RADYNE CORPORATION
001066	ADVANCED CONTROL SYSTEMS, INC.
001067	Ericsson
001068	COMOS TELECOM
001069	HELIOSS COMMUNICATIONS, INC.
00106A	DIGITAL MICROWAVE CORPORATION
00106B	SONUS NETWORKS, INC.
00106C	EDNT GmbH
00106D	Axxcelera Broadband Wireless
00106E	TADIRAN COM. LTD.
00106F	TRENTON TECHNOLOGY INC.
001070	CARADON TREND LTD.
001071	ADVANET INC.
001072	GVN TECHNOLOGIES, INC.
001073	TECHNOBOX, INC.
001074	ATEN INTERNATIONAL CO., LTD.
001075	Segate Technology LLC
001076	EUREM GmbH
001077	SAF DRIVE SYSTEMS, LTD.
001078	NUERA COMMUNICATIONS, INC.
001079	Cisco				5500 Router
00107A	Ambicom (was Tandy?)
00107B	Cisco Systems
00107C	P-COM, INC.
00107D	AURORA COMMUNICATIONS, LTD.
00107E	BACHMANN ELECTRONIC GmbH
00107F	CRESTRON ELECTRONICS, INC.
001080	METAWAVE COMMUNICATIONS
001081	DPS, INC.
001082	JNA TELECOMMUNICATIONS LIMITED
001083	HP-UX E 9000/889
001084	K-BOT COMMUNICATIONS
001085	POLARIS COMMUNICATIONS, INC.
001086	ATTO Technology, Inc.
001087	XSTREAMIS PLC
001088	AMERICAN NETWORKS INC.
001089	Websonic
00108A	TeraLogic, Inc.
00108B	LASERANIMATION SOLLINGER GMBH
00108C	Fujitsu Services Ltd
00108D	Johnson Controls, Inc.
00108E	HUGH SYMONS CONCEPT Technologies Ltd.
00108F	RAPTOR SYSTEMS
001090	CIMETRICS, INC.
001091	NO WIRES NEEDED BV
001092	NETCORE INC.
001093	CMS COMPUTERS, LTD.
001094	Performance Analysis Broadband, Spirent plc
001095	Thomson Inc.
001096	TRACEWELL SYSTEMS, INC.
001097	WinNet Metropolitan Communications Systems, Inc.
001098	STARNET TECHNOLOGIES, INC.
001099	InnoMedia, Inc.
00109A	Netline
00109B	Emulex Corporation
00109C	M-SYSTEM CO., LTD.
00109D	CLARINET SYSTEMS, INC.
00109E	AWARE, INC.
00109F	PAVO, INC.
0010A0	INNOVEX TECHNOLOGIES, INC.
0010A1	KENDIN SEMICONDUCTOR, INC.
0010A2	Tns
0010A3	OMNITRONIX, INC.
0010A4	Xircom				RealPort 10/100 PC Card
0010A5	OXFORD INSTRUMENTS
0010A6	Cisco
0010A7	UNEX TECHNOLOGY CORPORATION
0010A8	RELIANCE COMPUTER CORP.
0010A9	ADHOC TECHNOLOGIES
0010AA	MEDIA4, INC.
0010AB	KOITO ELECTRIC INDUSTRIES, LTD.
0010AC	IMCI TECHNOLOGIES
0010AD	SOFTRONICS USB, INC.
0010AE	SHINKO ELECTRIC INDUSTRIES CO.
0010AF	TAC SYSTEMS, INC.
0010B0	MERIDIAN TECHNOLOGY CORP.
0010B1	FOR-A CO., LTD.
0010B2	COACTIVE AESTHETICS
0010B3	NOKIA MULTIMEDIA TERMINALS
0010B4	ATMOSPHERE NETWORKS
0010B5	Accton Technology Corp
0010B6	ENTRATA COMMUNICATIONS CORP.
0010B7	COYOTE TECHNOLOGIES, LLC
0010B8	ISHIGAKI COMPUTER SYSTEM CO.
0010B9	MAXTOR CORP.
0010BA	MARTINHO-DAVIS SYSTEMS, INC.
0010BB	DATA & INFORMATION TECHNOLOGY
0010BC	Aastra Telecom
0010BD	THE TELECOMMUNICATION TECHNOLOGY COMMITTEE (TTC)
0010BE	MARCH NETWORKS CORPORATION
0010BF	InterAir Wireless
0010C0	ARMA, Inc.
0010C1	OI ELECTRIC CO.,LTD
0010C2	WILLNET, INC.
0010C3	CSI-CONTROL SYSTEMS
0010C4	MEDIA GLOBAL LINKS CO., LTD.
0010C5	PROTOCOL TECHNOLOGIES, INC.
0010C6	Universal Global Scientific Industrial Co., Ltd.
0010C7	DATA TRANSMISSION NETWORK
0010C8	COMMUNICATIONS ELECTRONICS SECURITY GROUP
0010C9	MITSUBISHI ELECTRONICS LOGISTIC SUPPORT CO.
0010CA	Telco Systems, Inc.
0010CB	FACIT K.K.
0010CC	CLP COMPUTER LOGISTIK PLANUNG GmbH
0010CD	INTERFACE CONCEPT
0010CE	VOLAMP, LTD.
0010CF	FIBERLANE COMMUNICATIONS
0010D0	WITCOM, LTD.
0010D1	Top Layer Networks, Inc.
0010D2	NITTO TSUSHINKI CO., LTD
0010D3	GRIPS ELECTRONIC GMBH
0010D4	STORAGE COMPUTER CORPORATION
0010D5	IMASDE CANARIAS, S.A.
0010D6	Exelis
0010D7	Argosy				EN 220 Fast Ethernet PCMCIA
0010D8	Calista
0010D9	IBM JAPAN, FUJISAWA MT+D
0010DA	Kollmorgen Corp
0010DB	Now part of Juniper Networks
0010DC	MICRO-STAR INTERNATIONAL CO., LTD.
0010DD	ENABLE SEMICONDUCTOR, INC.
0010DE	INTERNATIONAL DATACASTING CORPORATION
0010DF	RISE COMPUTER INC.
0010E0	Oracle Corporation
0010E1	S.I. TECH, INC.
0010E2	ArrayComm, Inc.
0010E3	Hewlett Packard
0010E4	NSI CORPORATION
0010E5	SOLECTRON TEXAS
0010E6	APPLIED INTELLIGENT SYSTEMS, INC.
0010E7	Breezecom, Ltd.
0010E8	TELOCITY, INCORPORATED
0010E9	RAIDTEC LTD.
0010EA	ADEPT TECHNOLOGY
0010EB	SELSIUS SYSTEMS, INC.
0010EC	RPCG, LLC
0010ED	SUNDANCE TECHNOLOGY, INC.
0010EE	CTI PRODUCTS, INC.
0010EF	DBTEL INCORPORATED
0010F0	RITTAL-WERK RUDOLF LOH GmbH & Co.
0010F1	I-O CORPORATION
0010F2	Antec
0010F3	Nexcom International Co., Ltd.
0010F4	Vertical Communications
0010F5	AMHERST SYSTEMS, INC.
0010F6	Cisco
0010F7	IRIICHI TECHNOLOGIES Inc.
0010F8	TEXIO TECHNOLOGY CORPORATION
0010F9	UNIQUE SYSTEMS, INC.
0010FA	Apple, Inc.
0010FB	ZIDA TECHNOLOGIES LIMITED
0010FC	BROADBAND NETWORKS, INC.
0010FD	COCOM A/S
0010FE	DIGITAL EQUIPMENT CORPORATION
0010FF	Cisco Systems, Inc
001100	Schneider Electric
001101	CET Technologies Pte Ltd
001102	Aurora Multimedia Corp.
001103	kawamura electric inc.
001104	Telexy
001105	Sunplus Technology Co., Ltd.
001106	Siemens NV (Belgium)
001107	RGB Networks Inc.
001108	Orbital Data Corporation
001109	Micro-Star International
00110A	Hewlett Packard
00110B	Franklin Technology Systems
00110C	Atmark Techno, Inc.
00110D	SANBlaze Technology, Inc.
00110E	Tsurusaki Sealand Transportation Co. Ltd.
00110F	netplat,Inc.
001110	Maxanna Technology Co., Ltd.
001111	Intel Corporation
001112	Honeywell CMSS
001113	Fraunhofer FOKUS
001114	EverFocus Electronics Corp.
001115	EPIN Technologies, Inc.
001116	COTEAU VERT CO., LTD.
001117	Cesnet
001118	BLX IC Design Corp., Ltd.
001119	Solteras, Inc.
00111A	ARRIS Group, Inc.
00111B	Targa Systems Div L-3 Communications
00111C	Pleora Technologies Inc.
00111D	Hectrix Limited
00111E	EPSG (Ethernet Powerlink Standardization Group)
00111F	Doremi Labs, Inc.
001120	Cisco Systems, Inc
001121	Cisco Systems, Inc
001122	CIMSYS Inc
001123	Appointech, Inc.
001124	Apple, Inc.
001125	IBM Corp
001126	Venstar Inc.
001127	TASI, Inc
001128	Streamit
001129	Paradise Datacom Ltd.
00112A	Niko NV
00112B	NetModule AG
00112C	IZT GmbH
00112D	iPulse Systems
00112E	Ceicom
00112F	ASUSTek COMPUTER INC.
001130	Allied Telesis (Hong Kong) Ltd.
001131	UNATECH. CO.,LTD
001132	Synology Incorporated
001133	Siemens Austria SIMEA
001134	MediaCell, Inc.
001135	Grandeye Ltd
001136	Goodrich Sensor Systems
001137	AICHI ELECTRIC CO., LTD.
001138	TAISHIN CO., LTD.
001139	STOEBER ANTRIEBSTECHNIK GmbH + Co. KG.
00113A	SHINBORAM
00113B	Micronet Communications Inc.
00113C	Micronas GmbH
00113D	KN SOLTEC CO.,LTD.
00113E	JL Corporation
00113F	Alcatel DI
001140	Nanometrics Inc.
001141	GoodMan Corporation
001142	e-SMARTCOM  INC.
001143	Dell Inc.
001144	Assurance Technology Corp
001145	ValuePoint Networks
001146	Telecard-Pribor Ltd
001147	Secom-Industry co.LTD.
001148	Prolon Control Systems
001149	Proliphix Inc.
00114A	KAYABA INDUSTRY Co,.Ltd.
00114B	Francotyp-Postalia GmbH
00114C	caffeina applied research ltd.
00114D	Atsumi Electric Co.,LTD.
00114E	690885 Ontario Inc.
00114F	US Digital Television, Inc
001150	Belkin Corporation
001151	Mykotronx
001152	Eidsvoll Electronics AS
001153	Trident Tek, Inc.
001154	Webpro Technologies Inc.
001155	Sevis Systems
001156	Pharos Systems NZ
001157	Oki Electric Industry Co., Ltd.
001158	Nortel Networks
001159	MATISSE NETWORKS INC
00115A	Ivoclar Vivadent AG
00115B	Elitegroup Computer Systems Co.,Ltd.
00115C	Cisco Systems, Inc
00115D	Cisco Systems, Inc
00115E	ProMinent Dosiertechnik GmbH
00115F	ITX Security Co., Ltd.
001160	ARTDIO Company Co., LTD
001161	NetStreams, LLC
001162	STAR MICRONICS CO.,LTD.
001163	SYSTEM SPA DEPT. ELECTRONICS
001164	ACARD Technology Corp.
001165	ZNYX Networks, Inc.
001166	Taelim Electronics Co., Ltd.
001167	Integrated System Solution Corp.
001168	HomeLogic LLC
001169	EMS Satcom
00116A	Domo Ltd
00116B	Digital Data Communications Asia Co.,Ltd
00116C	Nanwang Multimedia Inc.,Ltd
00116D	American Time and Signal
00116E	Peplink International Ltd.
00116F	Netforyou Co., LTD.
001170	GSC SRL
001171	DEXTER Communications, Inc.
001172	COTRON CORPORATION
001173	SMART Storage Systems
001174	Mojo Networks, Inc.
001175	Intel Corporation
001176	Intellambda Systems, Inc.
001177	Coaxial Networks, Inc.
001178	Chiron Technology Ltd
001179	Singular Technology Co. Ltd.
00117A	Singim International Corp.
00117B	Büchi  Labortechnik AG
00117C	e-zy.net
00117D	ZMD America, Inc.
00117E	Midmark Corp
00117F	Neotune Information Technology Corporation,.LTD
001180	ARRIS Group, Inc.
001181	InterEnergy Co.Ltd,
001182	IMI Norgren Ltd
001183	Datalogic ADC, Inc.
001184	Humo Laboratory,Ltd.
001185	Hewlett Packard
001186	Prime Systems, Inc.
001187	Category Solutions, Inc
001188	Enterasys
001189	Aerotech Inc
00118A	Viewtran Technology Limited
00118B	Alcatel-               # Alcatel-Lucent Enterprise
00118C	Missouri Department of Transportation
00118D	Hanchang System Corp.
00118E	Halytech Mace
00118F	EUTECH INSTRUMENTS PTE. LTD.
001190	Digital Design Corporation
001191	CTS-Clima Temperatur Systeme GmbH
001192	Cisco Systems, Inc
001193	Cisco Systems, Inc
001194	Chi Mei Communication Systems, Inc.
001195	D-Link Corporation
001196	Actuality Systems, Inc.
001197	Monitoring Technologies Limited
001198	Prism Media Products Limited
001199	2wcom Systems GmbH
00119A	Alkeria srl
00119B	Telesynergy Research Inc.
00119C	EP&T Energy
00119D	Diginfo Technology Corporation
00119E	Solectron Brazil
00119F	Nokia Danmark A/S
0011A0	Vtech Engineering Canada Ltd
0011A1	VISION NETWARE CO.,LTD
0011A2	Manufacturing Technology Inc
0011A3	LanReady Technologies Inc.
0011A4	JStream Technologies Inc.
0011A5	Fortuna Electronic Corp.
0011A6	Sypixx Networks
0011A7	Infilco Degremont Inc.
0011A8	Quest Technologies
0011A9	MOIMSTONE Co., LTD
0011AA	Uniclass Technology, Co., LTD
0011AB	TRUSTABLE TECHNOLOGY CO.,LTD.
0011AC	Simtec Electronics
0011AD	Shanghai Ruijie Technology
0011AE	ARRIS Group, Inc.
0011AF	Medialink-i,Inc
0011B0	Fortelink Inc.
0011B1	BlueExpert Technology Corp.
0011B2	2001 Technology Inc.
0011B3	YOSHIMIYA CO.,LTD.
0011B4	Westermo Teleindustri AB
0011B5	Shenzhen Powercom Co.,Ltd
0011B6	Open Systems International
0011B7	Octalix B.V.
0011B8	Liebherr - Elektronik GmbH
0011B9	Inner Range Pty. Ltd.
0011BA	Elexol Pty Ltd
0011BB	Cisco Systems, Inc
0011BC	Cisco Systems, Inc
0011BD	Bombardier Transportation
0011BE	AGP Telecom Co. Ltd
0011BF	AESYS S.p.A.
0011C0	Aday Technology Inc
0011C1	4P MOBILE DATA PROCESSING
0011C2	United Fiber Optic Communication
0011C3	Transceiving System Technology Corporation
0011C4	Terminales de Telecomunicacion Terrestre, S.L.
0011C5	TEN Technology
0011C6	Seagate Technology
0011C7	Raymarine UK Ltd
0011C8	Powercom Co., Ltd.
0011C9	MTT Corporation
0011CA	Long Range Systems, Inc.
0011CB	Jacobsons AB
0011CC	Guangzhou Jinpeng Group Co.,Ltd.
0011CD	Axsun Technologies
0011CE	Ubisense Limited
0011CF	Thrane & Thrane A/S
0011D0	Tandberg Data ASA
0011D1	Soft Imaging System GmbH
0011D2	Perception Digital Ltd
0011D3	NextGenTel Holding ASA
0011D4	NetEnrich, Inc
0011D5	Hangzhou Sunyard System Engineering Co.,Ltd.
0011D6	HandEra, Inc.
0011D7	eWerks Inc
0011D8	ASUSTek COMPUTER INC.
0011D9	Tivo
0011DA	Vivaas Technology Inc.
0011DB	Land-Cellular Corporation
0011DC	Glunz & Jensen
0011DD	FROMUS TEC. Co., Ltd.
0011DE	EURILOGIC
0011DF	Current Energy
0011E0	U-MEDIA Communications, Inc.
0011E1	Arcelik A.S
0011E2	Hua Jung Components Co., Ltd.
0011E3	Thomson, Inc.
0011E4	Danelec Electronics A/S
0011E5	KCodes Corporation
0011E6	Scientific Atlanta
0011E7	WORLDSAT - Texas de France
0011E8	Tixi.Com
0011E9	STARNEX CO., LTD.
0011EA	IWICS Inc.
0011EB	Innovative Integration
0011EC	AVIX INC.
0011ED	802 Global
0011EE	Estari, Inc.
0011EF	Conitec Datensysteme GmbH
0011F0	Wideful Limited
0011F1	QinetiQ Ltd
0011F2	Institute of Network Technologies
0011F3	NeoMedia Europe AG
0011F4	woori-net
0011F5	ASKEY COMPUTER CORP
0011F6	Asia Pacific Microsystems , Inc.
0011F7	Shenzhen Forward Industry Co., Ltd
0011F8	AIRAYA Corp
0011F9	Nortel Networks
0011FA	Rane Corporation
0011FB	Heidelberg Engineering GmbH
0011FC	HARTING Electronics GmbH
0011FD	KORG INC.
0011FE	Keiyo System Research, Inc.
0011FF	Digitro Tecnologia Ltda
001200	Cisco Systems, Inc
001201	Cisco Systems, Inc
001202	Decrane Aerospace - Audio International Inc.
001203	ActivNetworks
001204	u10 Networks, Inc.
001205	Terrasat Communications, Inc.
001206	iQuest (NZ) Ltd
001207	Head Strong International Limited
001208	Gantner Instruments GmbH
001209	Fastrax Ltd
00120A	Emerson Climate Technologies GmbH
00120B	Chinasys Technologies Limited
00120C	CE-Infosys Pte Ltd
00120D	Advanced Telecommunication Technologies, Inc.
00120E	Abocom
00120F	IEEE 802.3
001210	WideRay Corp
001211	Protechna Herbst GmbH & Co. KG
001212	PLUS  Corporation
001213	Metrohm AG
001214	Koenig & Bauer AG
001215	iStor Networks, Inc.
001216	ICP Internet Communication Payment AG
001217	Cisco-Linksys, LLC
001218	ARUZE Corporation
001219	Ahead Communication Systems Inc
00121A	Techno Soft Systemnics Inc.
00121B	Sound Devices, LLC
00121C	PARROT SA
00121D	Netfabric Corporation
00121E	Juniper Networks
00121F	Harding Instruments
001220	Cadco Systems
001221	B.Braun Melsungen AG
001222	Skardin (UK) Ltd
001223	Pixim
001224	NexQL Corporation
001225	ARRIS Group, Inc.
001226	Japan Direx Corporation
001227	Franklin Electric Co., Inc.
001228	Data Ltd.
001229	BroadEasy Technologies Co.,Ltd
00122A	VTech Telecommunications Ltd.
00122B	Virbiage Pty Ltd
00122C	Soenen Controls N.V.
00122D	SiNett Corporation
00122E	Signal Technology - AISD
00122F	Sanei Electric Inc.
001230	Picaso Infocommunication CO., LTD.
001231	Motion Control Systems, Inc.
001232	LeWiz Communications Inc.
001233	JRC TOKKI Co.,Ltd.
001234	Camille Bauer
001235	Andrew Corporation
001236	ConSentry Networks
001237	Texas Instruments
001238	SetaBox Technology Co., Ltd.
001239	S Net Systems Inc.
00123A	Posystech Inc., Co.
00123B	KeRo Systems ApS
00123C	Second Rule LLC
00123D	GES Co, Ltd
00123E	ERUNE technology Co., Ltd.
00123F	Dell Inc.
001240	AMOI ELECTRONICS CO.,LTD
001241	a2i marketing center
001242	Millennial Net
001243	Cisco Systems, Inc
001244	Cisco Systems, Inc
001245	Zellweger Analytics, Inc.
001246	T.O.M TECHNOLOGY INC..
001247	Samsung Electronics Co.,Ltd
001248	EMC Corporation (Kashya)
001249	Delta Elettronica S.p.A.
00124A	Dedicated Devices, Inc.
00124B	Texas Instruments
00124C	BBWM Corporation
00124D	Inducon BV
00124E	XAC AUTOMATION CORP.
00124F	Pentair Thermal Management
001250	Tokyo Aircaft Instrument Co., Ltd.
001251	Silink
001252	Citronix, LLC
001253	AudioDev AB
001254	Spectra Technologies Holdings Company Ltd
001255	NetEffect Incorporated
001256	LG INFORMATION & COMM.
001257	LeapComm Communication Technologies Inc.
001258	Activis Polska
001259	THERMO ELECTRON KARLSRUHE
00125A	Microsoft Corporation
00125B	KAIMEI ELECTRONI
00125C	Green Hills Software, Inc.
00125D	CyberNet Inc.
00125E	Caen
00125F	AWIND Inc.
001260	Stanton Magnetics,inc.
001261	Adaptix, Inc
001262	Nokia Danmark A/S
001263	Data Voice Technologies GmbH
001264	daum electronic gmbh
001265	Enerdyne Technologies, Inc.
001266	Swisscom Hospitality Services SA
001267	Panasonic Corporation
001268	IPS d.o.o.
001269	Value Electronics
00126A	OPTOELECTRONICS Co., Ltd.
00126B	Ascalade Communications Limited
00126C	Visonic Technologies 1993 Ltd.
00126D	University of California, Berkeley
00126E	Seidel Elektronik GmbH Nfg.KG
00126F	Rayson Technology Co., Ltd.
001270	NGES Denro Systems
001271	Measurement Computing Corp
001272	Redux Communications Ltd.
001273	Stoke Inc
001274	NIT lab
001275	Sentilla Corporation
001276	CG Power Systems Ireland Limited
001277	Korenix Technologies Co., Ltd.
001278	International Bar Code
001279	Hewlett Packard
00127A	Sanyu Industry Co.,Ltd.
00127B	VIA Networking Technologies, Inc.
00127C	SWEGON AB
00127D	MobileAria
00127E	Digital Lifestyles Group, Inc.
00127F	Cisco Systems, Inc
001280	Cisco Systems, Inc
001281	March Networks S.p.A.
001282	Qovia
001283	Nortel Networks
001284	Lab33 Srl
001285	Gizmondo Europe Ltd
001286	ENDEVCO CORP
001287	Digital Everywhere Unterhaltungselektronik GmbH
001288	2Wire Inc
001289	Advance Sterilization Products
00128A	ARRIS Group, Inc.
00128B	Sensory Networks Inc
00128C	Woodward Governor
00128D	STB Datenservice GmbH
00128E	Q-Free ASA
00128F	Montilio
001290	KYOWA Electric & Machinery Corp.
001291	KWS Computersysteme GmbH
001292	Griffin Technology
001293	GE Energy
001294	SUMITOMO ELECTRIC DEVICE INNOVATIONS, INC
001295	Aiware Inc.
001296	Addlogix
001297	O2Micro, Inc.
001298	MICO ELECTRIC(SHENZHEN) LIMITED
001299	Ktech Telecommunications Inc
00129A	IRT Electronics Pty Ltd
00129B	E2S Electronic Engineering Solutions, S.L.
00129C	Yulinet
00129D	First International Computer do Brasil
00129E	Surf Communications Inc.
00129F	RAE Systems
0012A0	NeoMeridian Sdn Bhd
0012A1	BluePacket Communications Co., Ltd.
0012A2	Vita
0012A3	Trust International B.V.
0012A4	ThingMagic, LLC
0012A5	Stargen, Inc.
0012A6	Dolby Australia
0012A7	ISR TECHNOLOGIES Inc
0012A8	intec GmbH
0012A9	3Com Ltd
0012AA	IEE, Inc.
0012AB	WiLife, Inc.
0012AC	ONTIMETEK INC.
0012AD	IDS GmbH
0012AE	HlsHard-               # HLS HARD-LINE Solutions Inc.
0012AF	ELPRO Technologies
0012B0	Efore Oyj   (Plc)
0012B1	Dai Nippon Printing Co., Ltd
0012B2	AVOLITES LTD.
0012B3	Advance Wireless Technology Corp.
0012B4	Work Microwave GmbH
0012B5	Vialta, Inc.
0012B6	Santa Barbara Infrared, Inc.
0012B7	PTW Freiburg
0012B8	G2 Microsystems
0012B9	Fusion Digital Technology
0012BA	FSI Systems, Inc.
0012BB	Telecommunications Industry Association TR-41 Committee
0012BC	Echolab LLC
0012BD	Avantec Manufacturing Limited
0012BE	Astek Corporation
0012BF	Arcadyan Technology Corporation
0012C0	HotLava Systems, Inc.
0012C1	Check Point Software Technologies
0012C2	Apex Electronics Factory
0012C3	WIT S.A.
0012C4	Viseon, Inc.
0012C5	V-Show  Technology (China) Co.,Ltd
0012C6	TGC America, Inc
0012C7	SECURAY Technologies Ltd.Co.
0012C8	Perfect tech
0012C9	ARRIS Group, Inc.
0012CA	Mechatronic Brick Aps
0012CB	CSS Inc.
0012CC	Bitatek CO., LTD
0012CD	ASEM SpA
0012CE	Advanced Cybernetics Group
0012CF	Accton Technology Corp
0012D0	Gossen-Metrawatt-GmbH
0012D1	Texas Instruments
0012D2	Texas Instruments
0012D3	Zetta Systems, Inc.
0012D4	Princeton Technology, Ltd
0012D5	Motion Reality Inc.
0012D6	Jiangsu Yitong High-Tech Co.,Ltd
0012D7	Invento Networks, Inc.
0012D8	International Games System Co., Ltd.
0012D9	Cisco Systems, Inc
0012DA	Cisco Systems, Inc
0012DB	ZIEHL industrie-elektronik GmbH + Co KG
0012DC	SunCorp Industrial Limited
0012DD	Shengqu Information Technology (Shanghai) Co., Ltd.
0012DE	Radio Components Sweden AB
0012DF	Novomatic AG
0012E0	Codan Limited
0012E1	Alliant Networks, Inc
0012E2	ALAXALA Networks Corporation
0012E3	Agat-RT, Ltd.
0012E4	ZIEHL industrie-electronik GmbH + Co KG
0012E5	Time America, Inc.
0012E6	SPECTEC COMPUTER CO., LTD.
0012E7	Projectek Networking Electronics Corp.
0012E8	Fraunhofer IMS
0012E9	Abbey Systems Ltd
0012EA	Trane
0012EB	PDH Solutions, LLC
0012EC	Movacolor b.v.
0012ED	AVG Advanced Technologies
0012EE	Sony Mobile Communications AB
0012EF	OneAccess SA
0012F0	Intel Corporate
0012F1	Ifotec
0012F2	Brocade Communications Systems, Inc.
0012F3	connectBlue AB
0012F4	Belco International Co.,Ltd.
0012F5	Imarda New Zealand Limited
0012F6	MDK CO.,LTD.
0012F7	Xiamen Xinglian Electronics Co., Ltd.
0012F8	WNI Resources, LLC
0012F9	URYU SEISAKU, LTD.
0012FA	THX LTD
0012FB	Samsung Electronics Co.,Ltd
0012FC	PLANET System Co.,LTD
0012FD	OPTIMUS IC S.A.
0012FE	Lenovo Mobile Communication Technology Ltd.
0012FF	Lely Industries N.V.
001300	IT-FACTORY, INC.
001301	IronGate S.L.
001302	Intel Corporate
001303	GateConnect
001304	Flaircomm Technologies Co. LTD
001305	Epicom, Inc.
001306	Always On Wireless
001307	Paravirtual Corporation
001308	Nuvera Fuel Cells
001309	Ocean Broadband Networks
00130A	Nortel Networks
00130B	Mextal B.V.
00130C	HF System Corporation
00130D	GALILEO AVIONICA
00130E	Focusrite Audio Engineering Limited
00130F	EGEMEN Bilgisayar Muh San ve Tic LTD STI
001310	Cisco-Linksys, LLC
001311	ARRIS Group, Inc.
001312	Amedia Networks Inc.
001313	GuangZhou Post & Telecom Equipment ltd
001314	Asiamajor Inc.
001315	Sony Interactive Entertainment Inc.
001316	L-S-B Broadcast Technologies GmbH
001317	GN Netcom A/S
001318	DGSTATION Co., Ltd.
001319	Cisco Systems, Inc
00131A	Cisco Systems, Inc
00131B	BeCell Innovations Corp.
00131C	LiteTouch, Inc.
00131D	Scanvaegt International A/S
00131E	Peiker acustic GmbH & Co. KG
00131F	NxtPhase T&D, Corp.
001320	Intel Corporate
001321	Hewlett Packard
001322	DAQ Electronics, Inc.
001323	Cap Co., Ltd.
001324	Schneider Electric Ultra Terminal
001325	Cortina Systems Inc
001326	ECM Systems Ltd
001327	Data Acquisitions limited
001328	Westech Korea Inc.,
001329	VSST Co., LTD
00132A	Sitronics Telecom Solutions
00132B	Phoenix Digital
00132C	MAZ Brandenburg GmbH
00132D	iWise Communications
00132E	ITian Coporation
00132F	Interactek
001330	EURO PROTECTION SURVEILLANCE
001331	CellPoint Connect
001332	Beijing Topsec Network Security Technology Co., Ltd.
001333	BaudTec Corporation
001334	Arkados, Inc.
001335	VS Industry Berhad
001336	Tianjin 712 Communication Broadcasting co., ltd.
001337	Orient Power Home Network Ltd.
001338	FRESENIUS-VIAL
001339	CCV Deutschland GmbH
00133A	VadaTech Inc.
00133B	Speed Dragon Multimedia Limited
00133C	QUINTRON SYSTEMS INC.
00133D	Micro Memory Curtiss Wright Co
00133E	MetaSwitch
00133F	Eppendorf Instrumente GmbH
001340	AD.EL s.r.l.
001341	Shandong New Beiyang Information Technology Co.,Ltd
001342	Vision Research, Inc.
001343	Matsushita Electronic Components (Europe) GmbH
001344	Fargo Electronics Inc.
001345	Eaton Corporation
001346	D-Link Corporation
001347	Red Lion Controls, LP
001348	Artila Electronics Co., Ltd.
001349	ZyXEL Communications Corporation
00134A	Engim, Inc.
00134B	ToGoldenNet Technology Inc.
00134C	YDT Technology International
00134D	Inepro BV
00134E	Valox Systems, Inc.
00134F	Tranzeo Wireless Technologies Inc.
001350	Silver Spring Networks, Inc
001351	Niles Audio Corporation
001352	Naztec, Inc.
001353	HYDAC Filtertechnik GMBH
001354	Zcomax Technologies, Inc.
001355	TOMEN Cyber-business Solutions, Inc.
001356	FLIR Radiation Inc
001357	Soyal Technology Co., Ltd.
001358	Realm Systems, Inc.
001359	ProTelevision Technologies A/S
00135A	Project T&E Limited
00135B	PanelLink Cinema, LLC
00135C	OnSite Systems, Inc.
00135D	NTTPC Communications, Inc.
00135E	Eab/Rwi/               # EAB/RWI/K
00135F	Cisco Systems, Inc
001360	Cisco Systems, Inc
001361	Biospace Co., Ltd.
001362	ShinHeung Precision Co., Ltd.
001363	Verascape, Inc.
001364	Paradigm Technology Inc..
001365	Nortel Networks
001366	Neturity Technologies Inc.
001367	Narayon. Co., Ltd.
001368	Saab Danmark A/S
001369	Honda Electron Co., LED.
00136A	Hach Lange Sarl
00136B	E-Tec
00136C	Tomtom
00136D	Tentaculus AB
00136E	Techmetro Corp.
00136F	PacketMotion, Inc.
001370	Nokia Danmark A/S
001371	ARRIS Group, Inc.
001372	Dell Inc.
001373	BLwave Electronics Co., Ltd
001374	Atheros Communications, Inc.
001375	American Security Products Co.
001376	Tabor Electronics Ltd.
001377	Samsung Electronics Co.,Ltd
001378	Qsan Technology, Inc.
001379	PONDER INFORMATION INDUSTRIES LTD.
00137A	Netvox Technology Co., Ltd.
00137B	Movon Corporation
00137C	Kaicom co., Ltd.
00137D	Dynalab, Inc.
00137E	CorEdge Networks, Inc.
00137F	Cisco Systems, Inc
001380	Cisco Systems, Inc
001381	CHIPS & Systems, Inc.
001382	Cetacea Networks Corporation
001383	Application Technologies and Engineering Research Laboratory
001384	Advanced Motion Controls
001385	Add-On Technology Co., LTD.
001386	ABB Inc./Totalflow
001387	27M Technologies AB
001388	WiMedia Alliance
001389	Redes de Telefonía Móvil S.A.
00138A	QINGDAO GOERTEK ELECTRONICS CO.,LTD.
00138B	Phantom Technologies LLC
00138C	Kumyoung.Co.Ltd
00138D	Kinghold
00138E	FOAB Elektronik AB
00138F	Asiarock Technology Limited
001390	Termtek Computer Co., Ltd
001391	OUEN CO.,LTD.
001392	Ruckus Wireless
001393	Panta Systems, Inc.
001394	Infohand Co.,Ltd
001395	congatec AG
001396	Acbel Polytech Inc.
001397	Oracle Corporation
001398	TrafficSim Co.,Ltd
001399	STAC Corporation.
00139A	K-ubique ID Corp.
00139B	ioIMAGE Ltd.
00139C	Exavera Technologies, Inc.
00139D	Marvell Hispana S.L.
00139E	Ciara Technologies Inc.
00139F	Electronics Design Services, Co., Ltd.
0013A0	ALGOSYSTEM Co., Ltd.
0013A1	Crow Electronic Engeneering
0013A2	MaxStream, Inc
0013A3	Siemens Com CPE Devices
0013A4	KeyEye Communications
0013A5	General Solutions, LTD.
0013A6	Extricom Ltd
0013A7	BATTELLE MEMORIAL INSTITUTE
0013A8	Tanisys Technology
0013A9	Sony Corporation
0013AA	ALS  & TEC Ltd.
0013AB	Telemotive AG
0013AC	Sunmyung Electronics Co., LTD
0013AD	Sendo Ltd
0013AE	Radiance Technologies, Inc.
0013AF	NUMA Technology,Inc.
0013B0	Jablotron
0013B1	Intelligent Control Systems (Asia) Pte Ltd
0013B2	Carallon Limited
0013B3	Ecom Communications Technology Co., Ltd.
0013B4	Appear TV
0013B5	Wavesat
0013B6	Sling Media, Inc.
0013B7	Scantech ID
0013B8	RyCo Electronic Systems Limited
0013B9	BM SPA
0013BA	ReadyLinks Inc
0013BB	Smartvue Corporation
0013BC	Artimi Ltd
0013BD	HYMATOM SA
0013BE	Virtual Conexions
0013BF	Media System Planning Corp.
0013C0	Trix Tecnologia Ltda.
0013C1	Asoka USA Corporation
0013C2	WACOM Co.,Ltd
0013C3	Cisco Systems, Inc
0013C4	Cisco Systems, Inc
0013C5	LIGHTRON FIBER-OPTIC DEVICES INC.
0013C6	OpenGear, Inc
0013C7	IONOS Co.,Ltd.
0013C8	ADB Broadband Italia
0013C9	Beyond Achieve Enterprises Ltd.
0013CA	Pico Digital
0013CB	Zenitel Norway AS
0013CC	Tall Maple Systems
0013CD	MTI co. LTD
0013CE	Intel Corporate
0013CF	4Access Communications
0013D0	t+ Medical Ltd
0013D1	KIRK telecom A/S
0013D2	PAGE IBERICA, S.A.
0013D3	MICRO-STAR INTERNATIONAL CO., LTD.
0013D4	ASUSTek COMPUTER INC.
0013D5	RuggedCom
0013D6	TII NETWORK TECHNOLOGIES, INC.
0013D7	SPIDCOM Technologies SA
0013D8	Princeton Instruments
0013D9	Matrix Product Development, Inc.
0013DA	Diskware Co., Ltd
0013DB	SHOEI Electric Co.,Ltd
0013DC	IBTEK INC.
0013DD	Abbott Diagnostics
0013DE	Adapt4, LLC
0013DF	Ryvor Corp.
0013E0	Murata Manufacturing Co., Ltd.
0013E1	Iprobe AB
0013E2	GeoVision Inc.
0013E3	CoVi Technologies, Inc.
0013E4	YANGJAE SYSTEMS CORP.
0013E5	TENOSYS, INC.
0013E6	Technolution
0013E7	Halcro
0013E8	Intel Corporate
0013E9	VeriWave, Inc.
0013EA	Kamstrup A/S
0013EB	Sysmaster Corporation
0013EC	Netsnapper Technologies SARL
0013ED	Psia
0013EE	JBX Designs Inc.
0013EF	Kingjon Digital Technology Co.,Ltd
0013F0	Wavefront Semiconductor
0013F1	AMOD Technology Co., Ltd.
0013F2	Klas Ltd
0013F3	Giga-byte Communications Inc.
0013F4	Psitek (Pty) Ltd
0013F5	Akimbi Systems
0013F6	Cintech
0013F7	SMC Networks, Inc.
0013F8	Dex Security Solutions
0013F9	Cavera Systems
0013FA	LifeSize Communications, Inc
0013FB	RKC INSTRUMENT INC.
0013FC	SiCortex, Inc
0013FD	Nokia Danmark A/S
0013FE	GRANDTEC ELECTRONIC CORP.
0013FF	Dage-MTI of MC, Inc.
001400	MINERVA KOREA CO., LTD
001401	Rivertree Networks Corp.
001402	kk-electronic a/s
001403	Renasis, LLC
001404	ARRIS Group, Inc.
001405	OpenIB, Inc.
001406	Go Networks
001407	Sperian Protection Instrumentation
001408	Eka Systems Inc.
001409	MAGNETI MARELLI   S.E. S.p.A.
00140A	WEPIO Co., Ltd.
00140B	FIRST INTERNATIONAL COMPUTER, INC.
00140C	GKB CCTV CO., LTD.
00140D	Nortel Networks
00140E	Nortel Networks
00140F	Federal State Unitary Enterprise Leningrad R&D Institute of
001410	Suzhou Keda Technology CO.,Ltd
001411	Deutschmann Automation GmbH & Co. KG
001412	S-TEC electronics AG
001413	Trebing & Himstedt Prozeßautomation GmbH & Co. KG
001414	Jumpnode Systems LLC.
001415	Intec Automation inc.
001416	Scosche Industries, Inc.
001417	RSE Informations Technologie GmbH
001418	C4line
001419	Sidsa
00141A	DEICY CORPORATION
00141B	Cisco Systems, Inc
00141C	Cisco Systems, Inc
00141D	LTi DRIVES GmbH
00141E	P.A. Semi, Inc.
00141F	SunKwang Electronics Co., Ltd
001420	G-Links networking company
001421	Total Wireless Technologies Pte. Ltd.
001422	Dell Inc.
001423	J-S Co. NEUROCOM
001424	Merry Electrics CO., LTD.
001425	Galactic Computing Corp.
001426	NL Technology
001427	JazzMutant
001428	Vocollect Inc
001429	V Center Technologies Co., Ltd.
00142A	Elitegroup Computer Systems Co.,Ltd.
00142B	Edata Communication Inc.
00142C	Koncept International, Inc.
00142D	Toradex AG
00142E	77 Elektronika Kft.
00142F	Savvius
001430	ViPowER, Inc
001431	PDL Electronics Ltd
001432	Tarallax Wireless, Inc.
001433	Empower Technologies(Canada) Inc.
001434	Keri Systems, Inc
001435	CityCom Corp.
001436	Qwerty Elektronik AB
001437	GSTeletech Co.,Ltd.
001438	Hewlett Packard Enterprise
001439	Blonder Tongue Laboratories, Inc.
00143A	RAYTALK INTERNATIONAL SRL
00143B	Sensovation AG
00143C	Rheinmetall Canada Inc.
00143D	Aevoe Inc.
00143E	AirLink Communications, Inc.
00143F	Hotway Technology Corporation
001440	ATOMIC Corporation
001441	Innovation Sound Technology Co., LTD.
001442	ATTO CORPORATION
001443	Consultronics Europe Ltd
001444	Grundfos Holding
001445	Telefon-               # Telefon-Gradnja d.o.o.
001446	SuperVision Solutions LLC
001447	BOAZ Inc.
001448	Inventec Multimedia & Telecom Corporation
001449	Sichuan Changhong Electric Ltd.
00144A	Taiwan Thick-Film Ind. Corp.
00144B	Hifn, Inc.
00144C	General Meters Corp.
00144D	Intelligent Systems
00144E	Srisa
00144F	Oracle Corporation
001450	Heim Systems GmbH
001451	Apple, Inc.
001452	CALCULEX,INC.
001453	ADVANTECH TECHNOLOGIES CO.,LTD
001454	Symwave
001455	Coder Electronics Corporation
001456	Edge Products
001457	T-VIPS AS
001458	HS Automatic ApS
001459	Moram Co., Ltd.
00145A	Neratec Solutions AG
00145B	SeekerNet Inc.
00145C	Intronics B.V.
00145D	WJ Communications, Inc.
00145E	IBM Corp
00145F	ADITEC CO. LTD
001460	Kyocera Wireless Corp.
001461	CORONA CORPORATION
001462	Digiwell Technology, inc
001463	IDCS N.V.
001464	Cryptosoft
001465	Novo Nordisk A/S
001466	Kleinhenz Elektronik GmbH
001467	ArrowSpan Inc.
001468	CelPlan International, Inc.
001469	Cisco Systems, Inc
00146A	Cisco Systems, Inc
00146B	Anagran, Inc.
00146C	Netgear
00146D	RF Technologies
00146E	H. Stoll GmbH & Co. KG
00146F	Kohler Co
001470	Prokom Software SA
001471	Eastern Asia Technology Limited
001472	China Broadband Wireless IP Standard Group
001473	Bookham Inc
001474	K40 Electronics
001475	Wiline Networks, Inc.
001476	MultiCom Industries Limited
001477	Nertec  Inc.
001478	TP-LINK TECHNOLOGIES CO.,LTD.
001479	NEC Magnus Communications,Ltd.
00147A	Eubus GmbH
00147B	Iteris, Inc.
00147C	3Com Ltd
00147D	Aeon Digital International
00147E	InnerWireless
00147F	Thomson Telecom Belgium
001480	Hitachi-               # Hitachi-LG Data Storage Korea, Inc
001481	Multilink Inc
001482	Aurora Networks
001483	eXS Inc.
001484	Cermate Technologies Inc.
001485	Giga-Byte
001486	Echo Digital Audio Corporation
001487	American Technology Integrators
001488	Akorri
001489	B15402100 - JANDEI, S.L.
00148A	Elin Ebg Traction Gmbh
00148B	Globo Electronic GmbH & Co. KG
00148C	General Dynamics Mission Systems
00148D	Cubic Defense Simulation Systems
00148E	Tele Power Inc.
00148F	Protronic (Far East) Ltd.
001490	ASP Corporation
001491	Daniels Electronics Ltd. dbo Codan Rado Communications
001492	Liteon, Mobile Media Solution SBU
001493	Systimax Solutions
001494	ESU AG
001495	2Wire Inc
001496	Phonic Corp.
001497	ZHIYUAN Eletronics co.,ltd.
001498	Viking Design Technology
001499	Helicomm Inc
00149A	ARRIS Group, Inc.
00149B	Nokota Communications, LLC
00149C	HF Company
00149D	Sound ID Inc.
00149E	UbONE Co., Ltd
00149F	System and Chips, Inc.
0014A0	Accsense, Inc.
0014A1	Synchronous Communication Corp
0014A2	Core Micro Systems Inc.
0014A3	Vitelec BV
0014A4	Hon Hai Precision Ind. Co.,Ltd.
0014A5	Gemtek Technology Co., Ltd.
0014A6	Teranetics, Inc.
0014A7	Nokia Danmark A/S
0014A8	Cisco Systems, Inc
0014A9	Cisco Systems, Inc
0014AA	Ashly Audio, Inc.
0014AB	Senhai Electronic Technology Co., Ltd.
0014AC	Bountiful WiFi
0014AD	Gassner Wiege- und Meßtechnik GmbH
0014AE	Wizlogics Co., Ltd.
0014AF	Datasym POS Inc.
0014B0	Naeil Community
0014B1	Axell Wireless Limited
0014B2	mCubelogics Corporation
0014B3	CoreStar International Corp
0014B4	General Dynamics United Kingdom Ltd
0014B5	PHYSIOMETRIX,INC
0014B6	Enswer Technology Inc.
0014B7	AR Infotek Inc.
0014B8	Hill-Rom
0014B9	MSTAR SEMICONDUCTOR
0014BA	Carvers SA de CV
0014BB	Open Interface North America
0014BC	SYNECTIC TELECOM EXPORTS PVT. LTD.
0014BD	incNETWORKS, Inc
0014BE	Wink communication technology CO.LTD
0014BF	Cisco-Linksys, LLC
0014C0	Symstream Technology Group Ltd
0014C1	U.S. Robotics Corporation
0014C2	Hewlett Packard
0014C3	Seagate Technology
0014C4	Vitelcom Mobile Technology
0014C5	Alive Technologies Pty Ltd
0014C6	Quixant Ltd
0014C7	Nortel Networks
0014C8	Contemporary Research Corp
0014C9	Brocade Communications Systems, Inc.
0014CA	Key Radio Systems Limited
0014CB	LifeSync Corporation
0014CC	Zetec, Inc.
0014CD	DigitalZone Co., Ltd.
0014CE	NF CORPORATION
0014CF	INVISIO Communications
0014D0	BTI Systems Inc.
0014D1	TRENDnet, Inc.
0014D2	Kyuden Technosystems Corporation
0014D3	Sepsa
0014D4	K Technology Corporation
0014D5	Datang Telecom Technology CO. , LCD,Optical Communication Br
0014D6	Jeongmin Electronics Co.,Ltd.
0014D7	Datastore Technology Corp
0014D8	bio-logic SA
0014D9	IP Fabrics, Inc.
0014DA	Huntleigh Healthcare
0014DB	Elma Trenew Electronic GmbH
0014DC	Communication System Design & Manufacturing (CSDM)
0014DD	Covergence Inc.
0014DE	Sage Instruments Inc.
0014DF	HI-P Tech Corporation
0014E0	LET'S Corporation
0014E1	Data Display AG
0014E2	datacom systems inc.
0014E3	mm-lab GmbH
0014E4	infinias, LLC
0014E5	Alticast
0014E6	AIM Infrarotmodule GmbH
0014E7	Stolinx,. Inc
0014E8	ARRIS Group, Inc.
0014E9	Nortech International
0014EA	S Digm Inc. (Safe Paradigm Inc.)
0014EB	AwarePoint Corporation
0014EC	Acro Telecom
0014ED	Airak, Inc.
0014EE	Western Digital Technologies, Inc.
0014EF	TZero Technologies, Inc.
0014F0	Business Security OL AB
0014F1	Cisco Systems, Inc
0014F2	Cisco Systems, Inc
0014F3	ViXS Systems Inc
0014F4	DekTec Digital Video B.V.
0014F5	OSI Security Devices
0014F6	Juniper Networks
0014F7	CREVIS Co., LTD
0014F8	Scientific Atlanta
0014F9	Vantage Controls
0014FA	AsGa S.A.
0014FB	Technical Solutions Inc.
0014FC	Extandon, Inc.
0014FD	Thecus Technology Corp.
0014FE	Artech Electronics
0014FF	Precise Automation, Inc.
001500	Intel Corporate
001501	Lexbox
001502	BETA tech
001503	PROFIcomms s.r.o.
001504	GAME PLUS CO., LTD.
001505	Actiontec Electronics, Inc
001506	Neo Photonics
001507	Renaissance Learning Inc
001508	Global Target Enterprise Inc
001509	Plus Technology Co., Ltd
00150A	Sonoa Systems, Inc
00150B	SAGE INFOTECH LTD.
00150C	AVM GmbH
00150D	Hoana Medical, Inc.
00150E	OPENBRAIN TECHNOLOGIES CO., LTD.
00150F	Mingjong
001510	Techsphere Co., Ltd
001511	Data Center Systems
001512	Zurich University of Applied Sciences
001513	EFS sas
001514	Hu Zhou NAVA Networks&Electronics Ltd.
001515	Leipold+               # Leipold+Co.GmbH
001516	URIEL SYSTEMS INC.
001517	Intel Corporate
001518	Shenzhen 10MOONS Technology Development CO.,Ltd
001519	StoreAge Networking Technologies
00151A	Hunter Engineering Company
00151B	Isilon Systems Inc.
00151C	Leneco
00151D	M2I CORPORATION
00151E	Ethernet Powerlink Standardization Group (EPSG)
00151F	Multivision Intelligent Surveillance (Hong Kong) Ltd
001520	Radiocrafts AS
001521	Horoquartz
001522	Dea Security
001523	Meteor Communications Corporation
001524	Numatics, Inc.
001525	Chamberlain Access Solutions
001526	Remote Technologies Inc
001527	Balboa Instruments
001528	Beacon Medical Products LLC d.b.a. BeaconMedaes
001529	N3 Corporation
00152A	Nokia GmbH
00152B	Cisco Systems, Inc
00152C	Cisco Systems, Inc
00152D	TenX Networks, LLC
00152E	PacketHop, Inc.
00152F	ARRIS Group, Inc.
001530	EMC Corporation
001531	Kocom
001532	Consumer Technologies Group, LLC
001533	NADAM.CO.,LTD
001534	A Beltrónica-Companhia de Comunicações, Lda
001535	OTE Spa
001536	Powertech co.,Ltd
001537	Ventus Networks
001538	RFID, Inc.
001539	Technodrive srl
00153A	Shenzhen Syscan Technology Co.,Ltd.
00153B	EMH metering GmbH & Co. KG
00153C	Kprotech Co., Ltd.
00153D	ELIM PRODUCT CO.
00153E	Q-Matic Sweden AB
00153F	Alcatel Alenia Space Italia
001540	Nortel Networks
001541	StrataLight Communications, Inc.
001542	MICROHARD S.R.L.
001543	Aberdeen Test Center
001544	coM.s.a.t. AG
001545	SEECODE Co., Ltd.
001546	ITG Worldwide Sdn Bhd
001547	AiZen Solutions Inc.
001548	CUBE TECHNOLOGIES
001549	Dixtal Biomedica Ind. Com. Ltda
00154A	WANSHIH ELECTRONIC CO., LTD
00154B	Wonde Proud Technology Co., Ltd
00154C	Saunders Electronics
00154D	Netronome Systems, Inc.
00154E	Iec
00154F	one RF Technology
001550	Nits Technology Inc
001551	RadioPulse Inc.
001552	Wi-Gear Inc.
001553	Cytyc Corporation
001554	Atalum Wireless S.A.
001555	DFM GmbH
001556	Sagemcom Broadband SAS
001557	Olivetti
001558	Foxconn
001559	Securaplane Technologies, Inc.
00155A	DAINIPPON PHARMACEUTICAL CO., LTD.
00155B	Sampo Corporation
00155C	Dresser Wayne
00155D	Microsoft Corporation
00155E	Morgan Stanley
00155F	GreenPeak Technologies
001560	Hewlett Packard
001561	JJPlus Corporation
001562	Cisco Systems, Inc
001563	Cisco Systems, Inc
001564	BEHRINGER Spezielle Studiotechnik GmbH
001565	XIAMEN YEALINK NETWORK TECHNOLOGY CO.,LTD
001566	A-First Technology Co., Ltd.
001567	RADWIN Inc.
001568	Dilithium Networks
001569	PECO II, Inc.
00156A	DG2L Technologies Pvt. Ltd.
00156B	Perfisans Networks Corp.
00156C	SANE SYSTEM CO., LTD
00156D	Ubiquiti Networks Inc.
00156E	A. W. Communication Systems Ltd
00156F	Xiranet Communications GmbH
001570	Zebra Technologies Inc
001571	Nolan Systems
001572	Red-Lemon
001573	NewSoft  Technology Corporation
001574	Horizon Semiconductors Ltd.
001575	Nevis Networks Inc.
001576	Labitec-               # LABiTec - Labor Biomedical Technologies GmbH
001577	Allied Telesis, Inc.
001578	Audio / Video Innovations
001579	Lunatone Industrielle Elektronik GmbH
00157A	Telefin S.p.A.
00157B	Leuze electronic GmbH + Co. KG
00157C	Dave Networks, Inc.
00157D	Posdata
00157E	Weidmüller Interface GmbH & Co. KG
00157F	ChuanG International Holding CO.,LTD.
001580	U-WAY CORPORATION
001581	MAKUS Inc.
001582	Pulse Eight Limited
001583	IVT corporation
001584	Schenck Process GmbH
001585	Aonvision Technolopy Corp.
001586	Xiamen Overseas Chinese Electronic Co., Ltd.
001587	Takenaka Seisakusho Co.,Ltd
001588	Salutica Allied Solutions Sdn Bhd
001589	D-MAX Technology Co.,Ltd
00158A	SURECOM Technology Corp.
00158B	Park Air Systems Ltd
00158C	Liab ApS
00158D	Jennic Ltd
00158E	Plustek.INC
00158F	NTT Advanced Technology Corporation
001590	Hectronic GmbH
001591	RLW Inc.
001592	Facom UK Ltd (Melksham)
001593	U4EA Technologies Inc.
001594	BIXOLON CO.,LTD
001595	Quester Tangent Corporation
001596	ARRIS Group, Inc.
001597	AETA AUDIO SYSTEMS
001598	Kolektor group
001599	Samsung Electronics Co.,Ltd
00159A	ARRIS Group, Inc.
00159B	Nortel Networks
00159C	B-KYUNG SYSTEM Co.,Ltd.
00159D	Tripp Lite
00159E	Mad Catz Interactive Inc
00159F	Terascala, Inc.
0015A0	Nokia Danmark A/S
0015A1	ECA-SINTERS
0015A2	ARRIS Group, Inc.
0015A3	ARRIS Group, Inc.
0015A4	ARRIS Group, Inc.
0015A5	DCI Co., Ltd.
0015A6	Digital Electronics Products Ltd.
0015A7	Robatech AG
0015A8	ARRIS Group, Inc.
0015A9	KWANG WOO I&C CO.,LTD
0015AA	Rextechnik International Co.,
0015AB	PRO CO SOUND INC
0015AC	Capelon AB
0015AD	Accedian Networks
0015AE	kyung il
0015AF	AzureWave Technology Inc.
0015B0	AUTOTELENET CO.,LTD
0015B1	Ambient Corporation
0015B2	Advanced Industrial Computer, Inc.
0015B3	Caretech AB
0015B4	Polymap  Wireless LLC
0015B5	CI Network Corp.
0015B6	ShinMaywa Industries, Ltd.
0015B7	Toshiba
0015B8	Tahoe
0015B9	Samsung Electronics Co.,Ltd
0015BA	iba AG
0015BB	SMA Solar Technology AG
0015BC	Develco
0015BD	Group 4 Technology Ltd
0015BE	Iqua Ltd.
0015BF	technicob
0015C0	DIGITAL TELEMEDIA CO.,LTD.
0015C1	Sony Interactive Entertainment Inc.
0015C2	3M Germany
0015C3	Ruf Telematik AG
0015C4	FLOVEL CO., LTD.
0015C5	Dell Inc.
0015C6	Cisco Systems, Inc
0015C7	Cisco Systems, Inc
0015C8	FlexiPanel Ltd
0015C9	Gumstix, Inc
0015CA	TeraRecon, Inc.
0015CB	Surf Communication Solutions Ltd.
0015CC	UQUEST, LTD.
0015CD	Exartech International Corp.
0015CE	ARRIS Group, Inc.
0015CF	ARRIS Group, Inc.
0015D0	ARRIS Group, Inc.
0015D1	ARRIS Group, Inc.
0015D2	Xantech Corporation
0015D3	Pantech&               # Pantech&Curitel Communications, Inc.
0015D4	Emitor AB
0015D5	Nicevt
0015D6	OSLiNK Sp. z o.o.
0015D7	Reti Corporation
0015D8	Interlink Electronics
0015D9	PKC Electronics Oy
0015DA	IRITEL A.D.
0015DB	Canesta Inc.
0015DC	KT&C Co., Ltd.
0015DD	IP Control Systems Ltd.
0015DE	Nokia Danmark A/S
0015DF	Clivet S.p.A.
0015E0	Ericsson
0015E1	Picochip Ltd
0015E2	Dr.Ing. Herbert Knauer GmbH
0015E3	Dream Technologies Corporation
0015E4	Zimmer Elektromedizin
0015E5	Cheertek Inc.
0015E6	MOBILE TECHNIKA Inc.
0015E7	Quantec Tontechnik
0015E8	Nortel Networks
0015E9	D-Link Corporation
0015EA	Tellumat (Pty) Ltd
0015EB	zte corporation
0015EC	Boca Devices LLC
0015ED	Fulcrum Microsystems, Inc.
0015EE	Omnex Control Systems
0015EF	NEC TOKIN Corporation
0015F0	EGO BV
0015F1	KYLINK Communications Corp.
0015F2	ASUSTek COMPUTER INC.
0015F3	PELTOR AB
0015F4	Eventide
0015F5	Sustainable Energy Systems
0015F6	SCIENCE AND ENGINEERING SERVICES, INC.
0015F7	Wintecronics Ltd.
0015F8	Kingtronics Industrial Co. Ltd.
0015F9	Cisco Systems, Inc
0015FA	Cisco Systems, Inc
0015FB	setex schermuly textile computer gmbh
0015FC	Littelfuse Startco
0015FD	Complete Media Systems
0015FE	SCHILLING ROBOTICS LLC
0015FF	Novatel Wireless Solutions, Inc.
001600	CelleBrite Mobile Synchronization
001601	BUFFALO.INC
001602	CEYON TECHNOLOGY CO.,LTD.
001603	COOLKSKY Co., LTD
001604	Sigpro
001605	YORKVILLE SOUND INC.
001606	Ideal Industries
001607	Curves International Inc.
001608	Sequans Communications
001609	Unitech electronics co., ltd.
00160A	SWEEX Europe BV
00160B	TVWorks LLC
00160C	LPL  DEVELOPMENT S.A. DE C.V
00160D	Be Here Corporation
00160E	Optica Technologies Inc.
00160F	BADGER METER INC
001610	Carina Technology
001611	Altecon Srl
001612	Otsuka Electronics Co., Ltd.
001613	LibreStream Technologies Inc.
001614	Picosecond Pulse Labs
001615	Nittan Company, Limited
001616	BROWAN COMMUNICATION INC.
001617	Msi
001618	HIVION Co., Ltd.
001619	Lancelan Technologies S.L.
00161A	Dametric AB
00161B	Micronet Corporation
00161C	ECue
00161D	Innovative Wireless Technologies, Inc.
00161E	Woojinnet
00161F	SUNWAVETEC Co., Ltd.
001620	Sony Mobile Communications AB
001621	Colorado Vnet
001622	BBH SYSTEMS GMBH
001623	Interval Media
001624	Teneros, Inc.
001625	Impinj, Inc.
001626	ARRIS Group, Inc.
001627	embedded-logic DESIGN AND MORE GmbH
001628	Magicard Ltd
001629	Nivus GmbH
00162A	Antik computers & communications s.r.o.
00162B	Togami Electric Mfg.co.,Ltd.
00162C	Xanboo
00162D	STNet Co., Ltd.
00162E	Space Shuttle Hi-Tech Co., Ltd.
00162F	Geutebrück GmbH
001630	Vativ Technologies
001631	Xteam
001632	Samsung Electronics Co.,Ltd
001633	Oxford Diagnostics Ltd.
001634	Mathtech, Inc.
001635	Hewlett Packard
001636	QUANTA COMPUTER INC.
001637	CITEL SpA
001638	TECOM Co., Ltd.
001639	Ubiquam Co., Ltd.
00163A	YVES TECHNOLOGY CO., LTD.
00163B	VertexRSI/General Dynamics
00163C	Rebox B.V.
00163D	Tsinghua Tongfang Legend Silicon Tech. Co., Ltd.
00163E	Xensource, Inc.
00163F	CReTE SYSTEMS Inc.
001640	Asmobile Communication Inc.
001641	Universal Global Scientific Industrial Co., Ltd.
001642	Pangolin
001643	Sunhillo Corporation
001644	LITE-ON Technology Corp.
001645	Power Distribution, Inc.
001646	Cisco Systems, Inc
001647	Cisco Systems, Inc
001648	SSD Company Limited
001649	SetOne GmbH
00164A	Vibration Technology Limited
00164B	Quorion Data Systems GmbH
00164C	PLANET INT Co., Ltd
00164D	Alcatel-               # Alcatel-Lucent IPD
00164E	Nokia Danmark A/S
00164F	World Ethnic Broadcastin Inc.
001650	Kratos EPD
001651	Exeo Systems
001652	Hoatech Technologies, Inc.
001653	LEGO System A/S IE Electronics Division
001654	Flex-P Industries Sdn. Bhd.
001655	FUHO TECHNOLOGY Co., LTD
001656	Nintendo Co., Ltd.
001657	Aegate Ltd
001658	Fusiontech Technologies Inc.
001659	Z.M.P. RADWAG
00165A	Harman Specialty Group
00165B	Grip Audio
00165C	Trackflow Ltd
00165D	AirDefense, Inc.
00165E	Precision I/O
00165F	Fairmount Automation
001660	Nortel Networks
001661	Novatium Solutions (P) Ltd
001662	Liyuh Technology Ltd.
001663	KBT Mobile
001664	Prod-El SpA
001665	Cellon France
001666	Quantier Communication Inc.
001667	A-TEC Subsystem INC.
001668	Eishin Electronics
001669	MRV Communication (Networks) LTD
00166A	Tps
00166B	Samsung Electronics Co.,Ltd
00166C	Samsung Electronics Co.,Ltd
00166D	Yulong Computer Telecommunication Scientific (Shenzhen) Co.,Ltd
00166E	Arbitron Inc.
00166F	Intel Corporate
001670	SKNET Corporation
001671	Symphox Information Co.
001672	Zenway enterprise ltd
001673	Bury GmbH & Co. KG
001674	EuroCB (Phils.), Inc.
001675	ARRIS Group, Inc.
001676	Intel Corporate
001677	Bihl + Wiedemann GmbH
001678	SHENZHEN BAOAN GAOKE ELECTRONICS CO., LTD
001679	eOn Communications
00167A	Skyworth Overseas Development Ltd.
00167B	Haver&Boecker
00167C	iRex Technologies BV
00167D	Sky-Line Information Co., Ltd.
00167E	DIBOSS.CO.,LTD
00167F	Bluebird Soft Inc.
001680	Bally Gaming + Systems
001681	Vector Informatik GmbH
001682	Pro Dex, Inc
001683	WEBIO International Co.,.Ltd.
001684	Donjin Co.,Ltd.
001685	Elisa Oyj
001686	Karl Storz Imaging
001687	Chubb CSC-Vendor AP
001688	ServerEngines LLC
001689	Pilkor Electronics Co., Ltd
00168A	id-Confirm Inc
00168B	Paralan Corporation
00168C	DSL Partner AS
00168D	KORWIN CO., Ltd.
00168E	Vimicro corporation
00168F	GN Netcom A/S
001690	J-TEK INCORPORATION
001691	Moser-Baer AG
001692	Scientific-Atlanta, Inc.
001693	PowerLink Technology Inc.
001694	Sennheiser Communications A/S
001695	AVC Technology (International) Limited
001696	QDI Technology (H.K.) Limited
001697	NEC Corporation
001698	T&A Mobile Phones
001699	Tonic DVB Marketing Ltd
00169A	Quadrics Ltd
00169B	Alstom Transport
00169C	Cisco Systems, Inc
00169D	Cisco Systems, Inc
00169E	TV One Ltd
00169F	Vimtron Electronics Co., Ltd.
0016A0	Auto-Maskin
0016A1	3Leaf Networks
0016A2	CentraLite Systems, Inc.
0016A3	Ingeteam Transmission&Distribution, S.A.
0016A4	Ezurio Ltd
0016A5	Tandberg Storage ASA
0016A6	Dovado FZ-LLC
0016A7	AWETA G&P
0016A8	CWT CO., LTD.
0016A9	2ei
0016AA	Kei Communication Technology Inc.
0016AB	Dansensor A/S
0016AC	Toho Technology Corp.
0016AD	BT-Links Company Limited
0016AE	Inventel
0016AF	Shenzhen Union Networks Equipment Co.,Ltd.
0016B0	VK Corporation
0016B1	Kbs
0016B2	DriveCam Inc
0016B3	Photonicbridges (China) Co., Ltd.
0016B4	Private
0016B5	ARRIS Group, Inc.
0016B6	Cisco-Linksys, LLC
0016B7	Seoul Commtech
0016B8	Sony Mobile Communications AB
0016B9	ProCurve Networking by HP
0016BA	WEATHERNEWS INC.
0016BB	Law-Chain Computer Technology Co Ltd
0016BC	Nokia Danmark A/S
0016BD	ATI Industrial Automation
0016BE	INFRANET, Inc.
0016BF	PaloDEx Group Oy
0016C0	Semtech Corporation
0016C1	Eleksen Ltd
0016C2	Avtec Systems Inc
0016C3	BA Systems Inc
0016C4	SiRF Technology, Inc.
0016C5	Shenzhen Xing Feng Industry Co.,Ltd
0016C6	North Atlantic Industries
0016C7	Cisco Systems, Inc
0016C8	Cisco Systems, Inc
0016C9	NAT Seattle, Inc.
0016CA	Nortel Networks
0016CB	Apple, Inc.
0016CC	Xcute Mobile Corp.
0016CD	HIJI HIGH-TECH CO., LTD.
0016CE	Hon Hai Precision Ind. Co.,Ltd.
0016CF	Hon Hai Precision Ind. Co.,Ltd.
0016D0	ATech elektronika d.o.o.
0016D1	ZAT a.s.
0016D2	Caspian
0016D3	Wistron Corporation
0016D4	Compal Communications, Inc.
0016D5	Synccom Co., Ltd
0016D6	TDA Tech Pty Ltd
0016D7	Sunways AG
0016D8	Senea AB
0016D9	NINGBO BIRD CO.,LTD.
0016DA	Futronic Technology Co. Ltd.
0016DB	Samsung Electronics Co.,Ltd
0016DC	Archos
0016DD	Gigabeam Corporation
0016DE	FAST Inc
0016DF	Lundinova AB
0016E0	3Com Ltd
0016E1	SiliconStor, Inc.
0016E2	American Fibertek, Inc.
0016E3	ASKEY COMPUTER CORP
0016E4	VANGUARD SECURITY ENGINEERING CORP.
0016E5	FORDLEY DEVELOPMENT LIMITED
0016E6	GIGA-BYTE TECHNOLOGY CO.,LTD.
0016E7	Dynamix Promotions Limited
0016E8	Sigma Designs, Inc.
0016E9	Tiba Medical Inc
0016EA	Intel Corporate
0016EB	Intel Corporate
0016EC	Elitegroup Computer Systems Co.,Ltd.
0016ED	Digital Safety Technologies, Inc
0016EE	Royaldigital Inc.
0016EF	Koko Fitness, Inc.
0016F0	Dell
0016F1	OmniSense, LLC
0016F2	Dmobile System Co., Ltd.
0016F3	CAST Information Co., Ltd
0016F4	Eidicom Co., Ltd.
0016F5	Dalian Golden Hualu Digital Technology Co.,Ltd
0016F6	Video Products Group
0016F7	L-3 Communications, Aviation Recorders
0016F8	AVIQTECH TECHNOLOGY CO., LTD.
0016F9	CETRTA POT, d.o.o., Kranj
0016FA	ECI Telecom Ltd.
0016FB	SHENZHEN MTC CO LTD
0016FC	TOHKEN CO.,LTD.
0016FD	Jaty Electronics
0016FE	ALPS ELECTRIC CO.,LTD.
0016FF	Wamin Optocomm Mfg Corp
001700	Kabel
001701	KDE, Inc.
001702	Osung Midicom Co., Ltd
001703	MOSDAN Internation Co.,Ltd
001704	Shinco Electronics Group Co.,Ltd
001705	Methode Electronics
001706	Techfaithwireless Communication Technology Limited.
001707	InGrid, Inc
001708	Hewlett Packard
001709	Exalt Communications
00170A	INEW DIGITAL COMPANY
00170B	Contela, Inc.
00170C	Twig Com Ltd.
00170D	Dust Networks Inc.
00170E	Cisco Systems, Inc
00170F	Cisco Systems, Inc
001710	Casa Systems Inc.
001711	GE Healthcare Bio-Sciences AB
001712	ISCO International
001713	Tiger NetCom
001714	BR Controls Nederland bv
001715	Qstik
001716	Qno Technology Inc.
001717	Leica Geosystems AG
001718	Vansco Electronics Oy
001719	Audiocodes USA, Inc
00171A	Winegard Company
00171B	Innovation Lab Corp.
00171C	NT MicroSystems, Inc.
00171D	Digit
00171E	Theo Benning GmbH & Co. KG
00171F	IMV Corporation
001720	Image Sensing Systems, Inc.
001721	FITRE S.p.A.
001722	Hanazeder Electronic GmbH
001723	Summit Data Communications
001724	Studer Professional Audio GmbH
001725	Liquid Computing
001726	m2c Electronic Technology Ltd.
001727	Thermo Ramsey Italia s.r.l.
001728	Selex Communications
001729	Ubicod Co.LTD
00172A	Proware Technology Corp.(By Unifosa)
00172B	Global Technologies Inc.
00172C	TAEJIN INFOTECH
00172D	Axcen Photonics Corporation
00172E	FXC Inc.
00172F	NeuLion Incorporated
001730	Automation Electronics
001731	ASUSTek COMPUTER INC.
001732	Science-               # Science-Technical Center RISSA
001733	Sfr
001734	ADC Telecommunications
001735	Intel Wireless Network Group
001736	iiTron Inc.
001737	Industrie Dial Face S.p.A.
001738	International Business Machines
001739	Bright Headphone Electronics Company
00173A	Reach Systems Inc.
00173B	Cisco Systems, Inc
00173C	Extreme Engineering Solutions
00173D	Neology
00173E	LeucotronEquipamentos Ltda.
00173F	Belkin International Inc.
001740	Bluberi Gaming Technologies Inc
001741	Defidev
001742	FUJITSU LIMITED
001743	Deck Srl
001744	Araneo Ltd.
001745	INNOTZ CO., Ltd
001746	Freedom9 Inc.
001747	Trimble
001748	Neokoros Brasil Ltda
001749	HYUNDAE YONG-O-SA CO.,LTD
00174A	Socomec
00174B	Nokia Danmark A/S
00174C	Millipore
00174D	DYNAMIC NETWORK FACTORY, INC.
00174E	Parama-tech Co.,Ltd.
00174F	iCatch Inc.
001750	GSI Group, MicroE Systems
001751	Online Corporation
001752	DAGS, Inc
001753	nFore Technology Inc.
001754	Arkino HiTOP Corporation Limited
001755	GE Security
001756	Vinci Labs Oy
001757	RIX TECHNOLOGY LIMITED
001758	ThruVision Ltd
001759	Cisco Systems, Inc
00175A	Cisco Systems, Inc
00175B	ACS Solutions Switzerland Ltd.
00175C	SHARP CORPORATION
00175D	Dongseo system.
00175E	Zed-3
00175F	XENOLINK Communications Co., Ltd.
001760	Naito Densei Machida MFG.CO.,LTD
001761	Private
001762	Solar Technology, Inc.
001763	Essentia S.p.A.
001764	ATMedia GmbH
001765	Nortel Networks
001766	Accense Technology, Inc.
001767	Earforce AS
001768	Zinwave Ltd
001769	Cymphonix Corp
00176A	Avago Technologies
00176B	Kiyon, Inc.
00176C	Pivot3, Inc.
00176D	CORE CORPORATION
00176E	DUCATI SISTEMI
00176F	PAX Computer Technology(Shenzhen) Ltd.
001770	Arti Industrial Electronics Ltd.
001771	APD Communications Ltd
001772	ASTRO Strobel Kommunikationssysteme GmbH
001773	Laketune Technologies Co. Ltd
001774	Elesta GmbH
001775	TTE Germany GmbH
001776	Meso Scale Diagnostics, LLC
001777	Obsidian Research Corporation
001778	Central Music Co.
001779	Quicktel
00177A	ASSA ABLOY AB
00177B	Azalea Networks inc
00177C	Smartlink Network Systems Limited
00177D	IDT Technology Limited
00177E	Meshcom Technologies Inc.
00177F	Worldsmart Retech
001780	Applied Biosystems B.V.
001781	Greystone Data System, Inc.
001782	LoBenn Inc.
001783	Texas Instruments
001784	ARRIS Group, Inc.
001785	Sparr Electronics Ltd
001786	Wisembed
001787	Brother, Brother & Sons ApS
001788	Philips Lighting BV
001789	Zenitron Corporation
00178A	DARTS TECHNOLOGIES CORP.
00178B	Teledyne Technologies Incorporated
00178C	Independent Witness, Inc
00178D	Checkpoint Systems, Inc.
00178E	Gunnebo Cash Automation AB
00178F	NINGBO YIDONG ELECTRONIC CO.,LTD.
001790	HYUNDAI DIGITECH Co, Ltd.
001791	LinTech GmbH
001792	Falcom Wireless Comunications Gmbh
001793	Tigi Corporation
001794	Cisco Systems, Inc
001795	Cisco Systems, Inc
001796	Rittmeyer AG
001797	Telsy Elettronica S.p.A.
001798	Azonic Technology Co., LTD
001799	SmarTire Systems Inc.
00179A	D-Link Corporation
00179B	CHANT SINCERE CO.,LTD
00179C	DEPRAG SCHULZ GMBH u. CO.
00179D	Kelman Limited
00179E	Sirit Inc
00179F	Apricorn
0017A0	RoboTech srl
0017A1	3soft inc.
0017A2	Camrivox Ltd.
0017A3	MIX s.r.l.
0017A4	Hewlett Packard
0017A5	Ralink Technology Corp
0017A6	YOSIN ELECTRONICS CO., LTD.
0017A7	Mobile Computing Promotion Consortium
0017A8	EDM Corporation
0017A9	Sentivision
0017AA	elab-experience inc.
0017AB	Nintendo Co., Ltd.
0017AC	O'Neil Product Development Inc.
0017AD	AceNet Corporation
0017AE	GAI-Tronics
0017AF	Enermet
0017B0	Nokia Danmark A/S
0017B1	ACIST Medical Systems, Inc.
0017B2	SK Telesys
0017B3	Aftek Infosys Limited
0017B4	Remote Security Systems, LLC
0017B5	Peerless Systems Corporation
0017B6	Aquantia
0017B7	Tonze Technology Co.
0017B8	NOVATRON CO., LTD.
0017B9	Gambro Lundia AB
0017BA	SEDO CO., LTD.
0017BB	Syrinx Industrial Electronics
0017BC	Touchtunes Music Corporation
0017BD	Tibetsystem
0017BE	Tratec Telecom B.V.
0017BF	Coherent Research Limited
0017C0	PureTech Systems, Inc.
0017C1	CM Precision Technology LTD.
0017C2	ADB Broadband Italia
0017C3	KTF Technologies Inc.
0017C4	Quanta Microsystems, INC.
0017C5	SonicWALL
0017C6	Cross Match Technologies Inc
0017C7	MARA Systems Consulting AB
0017C8	KYOCERA Document Solutions Inc.
0017C9	Samsung Electronics Co.,Ltd
0017CA	Qisda Corporation
0017CB	Juniper Networks
0017CC	Alcatel-               # Alcatel-Lucent
0017CD	CEC Wireless R&D Ltd.
0017CE	Screen Service Spa
0017CF	iMCA-GmbH
0017D0	Opticom Communications, LLC
0017D1	Nortel Networks
0017D2	THINLINX PTY LTD
0017D3	Etymotic Research, Inc.
0017D4	Monsoon Multimedia, Inc
0017D5	Samsung Electronics Co.,Ltd
0017D6	Bluechips Microhouse Co.,Ltd.
0017D7	ION Geophysical Corporation Inc.
0017D8	Magnum Semiconductor, Inc.
0017D9	AAI Corporation
0017DA	Spans Logic
0017DB	CANKO TECHNOLOGIES INC.
0017DC	DAEMYUNG ZERO1
0017DD	Clipsal Australia
0017DE	Advantage Six Ltd
0017DF	Cisco Systems, Inc
0017E0	Cisco Systems, Inc
0017E1	DACOS Technologies Co., Ltd.
0017E2	ARRIS Group, Inc.
0017E3	Texas Instruments
0017E4	Texas Instruments
0017E5	Texas Instruments
0017E6	Texas Instruments
0017E7	Texas Instruments
0017E8	Texas Instruments
0017E9	Texas Instruments
0017EA	Texas Instruments
0017EB	Texas Instruments
0017EC	Texas Instruments
0017ED	WooJooIT Ltd.
0017EE	ARRIS Group, Inc.
0017EF	IBM Corp
0017F0	SZCOM Broadband Network Technology Co.,Ltd
0017F1	Renu Electronics Pvt Ltd
0017F2	Apple, Inc.
0017F3	Harris Corparation
0017F4	ZERON ALLIANCE
0017F5	LIG NEOPTEK
0017F6	Pyramid Meriden Inc.
0017F7	CEM Solutions Pvt Ltd
0017F8	Motech Industries Inc.
0017F9	Forcom Sp. z o.o.
0017FA	Microsoft Corporation
0017FB	Fa
0017FC	Suprema Inc.
0017FD	Amulet Hotkey
0017FE	TALOS SYSTEM INC.
0017FF	PLAYLINE Co.,Ltd.
001800	UNIGRAND LTD
001801	Actiontec Electronics, Inc
001802	Alpha Networks Inc.
001803	ArcSoft Shanghai Co. LTD
001804	E-TEK DIGITAL TECHNOLOGY LIMITED
001805	Beijing InHand Networking Technology Co.,Ltd.
001806	Hokkei Industries Co., Ltd.
001807	Fanstel Corp.
001808	SightLogix, Inc.
001809	Cresyn
00180A	Cisco Meraki
00180B	Brilliant Telecommunications
00180C	Optelian Access Networks
00180D	Terabytes Server Storage Tech Corp
00180E	Avega Systems
00180F	Nokia Danmark A/S
001810	IPTrade S.A.
001811	Neuros Technology International, LLC.
001812	Beijing Xinwei Telecom Technology Co., Ltd.
001813	Sony Mobile Communications AB
001814	Mitutoyo Corporation
001815	GZ Technologies, Inc.
001816	Ubixon Co., Ltd.
001817	D. E. Shaw Research, LLC
001818	Cisco Systems, Inc
001819	Cisco Systems, Inc
00181A	AVerMedia Information Inc.
00181B	TaiJin Metal Co., Ltd.
00181C	Exterity Limited
00181D	ASIA ELECTRONICS CO.,LTD
00181E	GDX Technologies Ltd.
00181F	Palmmicro Communications
001820	w5networks
001821	SINDORICOH
001822	CEC TELECOM CO.,LTD.
001823	Delta Electronics, Inc.
001824	Kimaldi Electronics, S.L.
001825	Private
001826	Cale Access AB
001827	NEC UNIFIED SOLUTIONS NEDERLAND B.V.
001828	e2v technologies (UK) ltd.
001829	Gatsometer
00182A	Taiwan Video & Monitor
00182B	Softier
00182C	Ascend Networks, Inc.
00182D	Artec Design
00182E	XStreamHD
00182F	Texas Instruments
001830	Texas Instruments
001831	Texas Instruments
001832	Texas Instruments
001833	Texas Instruments
001834	Texas Instruments
001835	Thoratec / ITC
001836	Reliance Electric Limited
001837	Universal ABIT Co., Ltd.
001838	PanAccess Communications,Inc.
001839	Cisco-Linksys, LLC
00183A	Westell Technologies Inc.
00183B	CENITS Co., Ltd.
00183C	Encore Software Limited
00183D	Vertex Link Corporation
00183E	Digilent, Inc
00183F	2Wire Inc
001840	3 Phoenix, Inc.
001841	High Tech Computer Corp
001842	Nokia Danmark A/S
001843	Dawevision Ltd
001844	Heads Up Technologies, Inc.
001845	Pulsar-Telecom LLC.
001846	Crypto S.A.
001847	AceNet Technology Inc.
001848	Vecima Networks Inc.
001849	Pigeon Point Systems LLC
00184A	Catcher, Inc.
00184B	Las Vegas Gaming, Inc.
00184C	Bogen Communications
00184D	Netgear
00184E	Lianhe Technologies, Inc.
00184F	8 Ways Technology Corp.
001850	Secfone Kft
001851	Swsoft
001852	StorLink Semiconductors, Inc.
001853	Atera Networks LTD.
001854	Argard Co., Ltd
001855	Aeromaritime Systembau GmbH
001856	EyeFi, Inc
001857	Unilever R&D
001858	TagMaster AB
001859	Strawberry Linux Co.,Ltd.
00185A	uControl, Inc.
00185B	Network Chemistry, Inc
00185C	EDSLAB Technologies
00185D	TAIGUEN TECHNOLOGY (SHEN-ZHEN) CO., LTD.
00185E	Nexterm Inc.
00185F	TAC Inc.
001860	SIM Technology Group Shanghai Simcom Ltd.,
001861	Ooma, Inc.
001862	Seagate Technology
001863	Veritech Electronics Limited
001864	Eaton Corporation
001865	Siemens Healthcare Diagnostics Manufacturing Ltd
001866	Leutron Vision
001867	Datalogic ADC
001868	Cisco SPVTG
001869	Kingjim
00186A	Global Link Digital Technology Co,.LTD
00186B	Sambu Communics CO., LTD.
00186C	Neonode AB
00186D	Zhenjiang Sapphire Electronic Industry CO.
00186E	3Com Ltd
00186F	Setha Industria Eletronica LTDA
001870	E28 Shanghai Limited
001871	Hewlett Packard
001872	Expertise Engineering
001873	Cisco Systems, Inc
001874	Cisco Systems, Inc
001875	AnaCise Testnology Pte Ltd
001876	WowWee Ltd.
001877	Amplex A/S
001878	Mackware GmbH
001879	Dsys
00187A	Wiremold
00187B	4NSYS Co. Ltd.
00187C	INTERCROSS, LLC
00187D	Armorlink shanghai Co. Ltd
00187E	RGB Spectrum
00187F	Zodianet
001880	Maxim Integrated Products
001881	Buyang Electronics Industrial Co., Ltd
001882	HUAWEI TECHNOLOGIES CO.,LTD
001883	FORMOSA21 INC.
001884	Fon Technology S.L.
001885	Avigilon Corporation
001886	EL-TECH, INC.
001887	Metasystem SpA
001888	GOTIVE a.s.
001889	WinNet Solutions Limited
00188A	Infinova LLC
00188B	Dell Inc.
00188C	Mobile Action Technology Inc.
00188D	Nokia Danmark A/S
00188E	Ekahau, Inc.
00188F	Montgomery Technology, Inc.
001890	RadioCOM, s.r.o.
001891	Zhongshan General K-mate Electronics Co., Ltd
001892	ads-tec GmbH
001893	SHENZHEN PHOTON BROADBAND TECHNOLOGY CO.,LTD
001894	NPCore, Inc.
001895	Hansun Technologies Inc.
001896	Great Well Electronic LTD
001897	JESS-LINK PRODUCTS Co., LTD
001898	KINGSTATE ELECTRONICS CORPORATION
001899	ShenZhen jieshun Science&Technology Industry CO,LTD.
00189A	HANA Micron Inc.
00189B	Thomson Inc.
00189C	Weldex Corporation
00189D	Navcast Inc.
00189E	OMNIKEY GmbH.
00189F	Lenntek Corporation
0018A0	Cierma Ascenseurs
0018A1	Tiqit Computers, Inc.
0018A2	XIP Technology AB
0018A3	ZIPPY TECHNOLOGY CORP.
0018A4	ARRIS Group, Inc.
0018A5	ADigit Technologies Corp.
0018A6	Persistent Systems, LLC
0018A7	Yoggie Security Systems LTD.
0018A8	AnNeal Technology Inc.
0018A9	Ethernet Direct Corporation
0018AA	Protec Fire Detection plc
0018AB	BEIJING LHWT MICROELECTRONICS INC.
0018AC	Shanghai Jiao Da HISYS Technology Co. Ltd.
0018AD	NIDEC SANKYO CORPORATION
0018AE	TVT CO.,LTD
0018AF	Samsung Electronics Co.,Ltd
0018B0	Nortel Networks
0018B1	IBM Corp
0018B2	ADEUNIS RF
0018B3	TEC WizHome Co., Ltd.
0018B4	Dawon Media Inc.
0018B5	Magna Carta
0018B6	S3C, Inc.
0018B7	D3 LED, LLC
0018B8	New Voice International AG
0018B9	Cisco Systems, Inc
0018BA	Cisco Systems, Inc
0018BB	Eliwell Controls srl
0018BC	ZAO NVP Bolid
0018BD	SHENZHEN DVBWORLD TECHNOLOGY CO., LTD.
0018BE	ANSA Corporation
0018BF	Essence Technology Solution, Inc.
0018C0	ARRIS Group, Inc.
0018C1	Almitec Informática e Comércio
0018C2	Firetide, Inc
0018C3	CS Corporation
0018C4	Raba Technologies LLC
0018C5	Nokia Danmark A/S
0018C6	OPW Fuel Management Systems
0018C7	Real Time Automation
0018C8	ISONAS Inc.
0018C9	EOps Technology Limited
0018CA	Viprinet GmbH
0018CB	Tecobest Technology Limited
0018CC	AXIOHM SAS
0018CD	Erae Electronics Industry Co., Ltd
0018CE	Dreamtech Co., Ltd
0018CF	Baldor Electric Company
0018D0	AtRoad,  A Trimble Company
0018D1	Siemens Home & Office Comm. Devices
0018D2	High-Gain Antennas LLC
0018D3	Teamcast
0018D4	Unified Display Interface SIG
0018D5	Reigncom
0018D6	Swirlnet A/S
0018D7	JAVAD GNSS, Inc.
0018D8	ARCH METER Corporation
0018D9	Santosha Internatonal, Inc
0018DA	AMBER wireless GmbH
0018DB	EPL Technology Ltd
0018DC	Prostar Co., Ltd.
0018DD	Silicondust Engineering Ltd
0018DE	Intel Corporate
0018DF	The Morey Corporation
0018E0	Anaveo
0018E1	Verkerk Service Systemen
0018E2	Topdata Sistemas de Automacao Ltda
0018E3	Visualgate Systems, Inc.
0018E4	Yiguang
0018E5	Adhoco AG
0018E6	Computer Hardware Design SIA
0018E7	Cameo Communications, INC.
0018E8	Hacetron Corporation
0018E9	Numata Corporation
0018EA	Alltec GmbH
0018EB	Blue Zen Enterprises Private Limited
0018EC	Welding Technology Corporation
0018ED	Accutech Ultrasystems Co., Ltd.
0018EE	Videology Imaging Solutions, Inc.
0018EF	Escape Communications, Inc.
0018F0	JOYTOTO Co., Ltd.
0018F1	Chunichi Denshi Co.,LTD.
0018F2	Beijing Tianyu Communication Equipment Co., Ltd
0018F3	ASUSTek COMPUTER INC.
0018F4	EO TECHNICS Co., Ltd.
0018F5	Shenzhen Streaming Video Technology Company Limited
0018F6	Thomson Telecom Belgium
0018F7	Kameleon Technologies
0018F8	Cisco-Linksys, LLC
0018F9	VVOND, Inc.
0018FA	Yushin Precision Equipment Co.,Ltd.
0018FB	Compro Technology
0018FC	Altec Electronic AG
0018FD	Optimal Technologies International Inc.
0018FE	Hewlett Packard
0018FF	PowerQuattro Co.
001900	Intelliverese - DBA Voicecom
001901	F1media
001902	Cambridge Consultants Ltd
001903	Bigfoot Networks Inc
001904	WB Electronics Sp. z o.o.
001905	SCHRACK Seconet AG
001906	Cisco Systems, Inc
001907	Cisco Systems, Inc
001908	Duaxes Corporation
001909	DEVI - Danfoss A/S
00190A	HASWARE INC.
00190B	Southern Vision Systems, Inc.
00190C	Encore Electronics, Inc.
00190D	IEEE 1394c
00190E	Atech Technology Co., Ltd.
00190F	Advansus Corp.
001910	Knick Elektronische Messgeraete GmbH & Co. KG
001911	Just In Mobile Information Technologies (Shanghai) Co., Ltd.
001912	Welcat Inc
001913	Chuang-Yi Network Equipment Co.Ltd.
001914	Winix Co., Ltd
001915	TECOM Co., Ltd.
001916	PayTec AG
001917	Posiflex Inc.
001918	Interactive Wear AG
001919	ASTEL Inc.
00191A	Irlink
00191B	Sputnik Engineering AG
00191C	Sensicast Systems
00191D	Nintendo Co., Ltd.
00191E	Beyondwiz Co., Ltd.
00191F	Microlink communications Inc.
001920	KUME electric Co.,Ltd.
001921	Elitegroup Computer Systems Co.,Ltd.
001922	CM Comandos Lineares
001923	Phonex Korea Co., LTD.
001924	LBNL  Engineering
001925	Intelicis Corporation
001926	BitsGen Co., Ltd.
001927	ImCoSys Ltd
001928	Siemens AG, Transportation Systems
001929	2M2B Montadora de Maquinas Bahia Brasil LTDA
00192A	Antiope Associates
00192B	Aclara RF Systems Inc.
00192C	ARRIS Group, Inc.
00192D	Nokia Corporation
00192E	Spectral Instruments, Inc.
00192F	Cisco Systems, Inc
001930	Cisco Systems, Inc
001931	Balluff GmbH
001932	Gude Analog- und Digialsysteme GmbH
001933	Strix Systems, Inc.
001934	TRENDON TOUCH TECHNOLOGY CORP.
001935	DUERR DENTAL AG
001936	STERLITE OPTICAL TECHNOLOGIES LIMITED
001937	CommerceGuard AB
001938	UMB Communications Co., Ltd.
001939	Gigamips
00193A	OESOLUTIONS
00193B	Wilibox Deliberant Group LLC
00193C	HighPoint Technologies Incorporated
00193D	GMC Guardian Mobility Corp.
00193E	ADB Broadband Italia
00193F	RDI technology(Shenzhen) Co.,LTD
001940	Rackable Systems
001941	Pitney Bowes, Inc
001942	ON SOFTWARE INTERNATIONAL LIMITED
001943	Belden
001944	Fossil Partners, L.P.
001945	RF COncepts, LLC
001946	Cianet Industria e Comercio S/A
001947	Cisco SPVTG
001948	AireSpider Networks
001949	TENTEL  COMTECH CO., LTD.
00194A	TESTO AG
00194B	Sagemcom Broadband SAS
00194C	Fujian Stelcom information & Technology CO.,Ltd
00194D	Avago Technologies Sdn Bhd
00194E	Ultra Electronics - TCS (Tactical Communication Systems)
00194F	Nokia Danmark A/S
001950	Harman Multimedia
001951	NETCONS, s.r.o.
001952	ACOGITO Co., Ltd
001953	Chainleader Communications Corp.
001954	Leaf Corporation.
001955	Cisco Systems, Inc
001956	Cisco Systems, Inc
001957	Saafnet Canada Inc.
001958	Bluetooth SIG, Inc.
001959	Staccato Communications Inc.
00195A	Jenaer Antriebstechnik GmbH
00195B	D-Link Corporation
00195C	Innotech Corporation
00195D	ShenZhen XinHuaTong Opto Electronics Co.,Ltd
00195E	ARRIS Group, Inc.
00195F	Valemount Networks Corporation
001960	DoCoMo Systems, Inc.
001961	Blaupunkt  Embedded Systems GmbH
001962	Commerciant, LP
001963	Sony Mobile Communications AB
001964	Doorking Inc.
001965	YuHua TelTech (ShangHai) Co., Ltd.
001966	Asiarock Technology Limited
001967	TELDAT Sp.J.
001968	Digital Video Networks(Shanghai) CO. LTD.
001969	Nortel Networks
00196A	MikroM GmbH
00196B	Danpex Corporation
00196C	ETROVISION TECHNOLOGY
00196D	Raybit Systems Korea, Inc
00196E	Metacom (Pty) Ltd.
00196F	SensoPart GmbH
001970	Z-Com, Inc.
001971	Guangzhou Unicomp Technology Co.,Ltd
001972	Plexus (Xiamen) Co.,ltd.
001973	Zeugma Systems
001974	16063
001975	Beijing Huisen networks technology Inc
001976	Xipher Technologies, LLC
001977	Aerohive Networks Inc.
001978	Datum Systems, Inc.
001979	Nokia Danmark A/S
00197A	MAZeT GmbH
00197B	Picotest Corp.
00197C	Riedel Communications GmbH
00197D	Hon Hai Precision Ind. Co.,Ltd.
00197E	Hon Hai Precision Ind. Co.,Ltd.
00197F	PLANTRONICS, INC.
001980	Gridpoint Systems
001981	Vivox Inc
001982	Smardtv
001983	CCT R&D Limited
001984	ESTIC Corporation
001985	IT Watchdogs, Inc
001986	Cheng Hongjian
001987	Panasonic Mobile Communications Co., Ltd.
001988	Wi2Wi, Inc
001989	Sonitrol Corporation
00198A	Northrop Grumman Systems Corp.
00198B	Novera Optics Korea, Inc.
00198C	Ixsea
00198D	Ocean Optics, Inc.
00198E	Oticon A/S
00198F	Alcatel Bell N.V.
001990	ELM DATA Co., Ltd.
001991	Avinfo
001992	Adtran Inc
001993	Changshu Switchgear MFG. Co.,Ltd. (Former Changshu Switchgea
001994	Jorjin Technologies Inc.
001995	Jurong Hi-Tech (Suzhou)Co.ltd
001996	TurboChef Technologies Inc.
001997	Soft Device Sdn Bhd
001998	SATO CORPORATION
001999	Fujitsu Technology Solutions GmbH
00199A	Edo-Evi
00199B	Diversified Technical Systems, Inc.
00199C	Ctring
00199D	Vizio, Inc
00199E	Nifty
00199F	DKT A/S
0019A0	NIHON DATA SYSTENS, INC.
0019A1	LG INFORMATION & COMM.
0019A2	ORDYN TECHNOLOGIES
0019A3	asteel electronique atlantique
0019A4	Austar Technology (hang zhou) Co.,Ltd
0019A5	RadarFind Corporation
0019A6	ARRIS Group, Inc.
0019A7	Itu-T
0019A8	WiQuest Communications
0019A9	Cisco Systems, Inc
0019AA	Cisco Systems, Inc
0019AB	Raycom CO ., LTD
0019AC	GSP SYSTEMS Inc.
0019AD	BOBST SA
0019AE	Hopling Technologies b.v.
0019AF	Rigol Technologies, Inc.
0019B0	HanYang System
0019B1	Arrow7 Corporation
0019B2	XYnetsoft Co.,Ltd
0019B3	Stanford Research Systems
0019B4	Intellio Ltd
0019B5	Famar Fueguina S.A.
0019B6	Euro Emme s.r.l.
0019B7	Nokia Danmark A/S
0019B8	Boundary Devices
0019B9	Dell Inc.
0019BA	Paradox Security Systems Ltd
0019BB	Hewlett Packard
0019BC	ELECTRO CHANCE SRL
0019BD	New Media Life
0019BE	Altai Technologies Limited
0019BF	Citiway technology Co.,ltd
0019C0	ARRIS Group, Inc.
0019C1	ALPS ELECTRIC CO.,LTD.
0019C2	Equustek Solutions, Inc.
0019C3	Qualitrol
0019C4	Infocrypt Inc.
0019C5	Sony Interactive Entertainment Inc.
0019C6	zte corporation
0019C7	Cambridge Industries(Group) Co.,Ltd.
0019C8	AnyDATA Corporation
0019C9	S&C ELECTRIC COMPANY
0019CA	Broadata Communications, Inc
0019CB	ZyXEL Communications Corporation
0019CC	RCG (HK) Ltd
0019CD	Chengdu ethercom information technology Ltd.
0019CE	Progressive Gaming International
0019CF	SALICRU, S.A.
0019D0	Cathexis
0019D1	Intel Corporate
0019D2	Intel Corporate
0019D3	TRAK Microwave
0019D4	ICX Technologies
0019D5	IP Innovations, Inc.
0019D6	LS Cable and System Ltd.
0019D7	FORTUNETEK CO., LTD
0019D8	Maxfor
0019D9	Zeutschel GmbH
0019DA	Welltrans O&E Technology Co. , Ltd.
0019DB	MICRO-STAR INTERNATIONAL CO., LTD.
0019DC	ENENSYS Technologies
0019DD	FEI-Zyfer, Inc.
0019DE	Mobitek
0019DF	Thomson Inc.
0019E0	TP-LINK TECHNOLOGIES CO.,LTD.
0019E1	Nortel Networks
0019E2	Juniper Networks
0019E3	Apple, Inc.
0019E4	2Wire Inc
0019E5	Lynx Studio Technology, Inc.
0019E6	TOYO MEDIC CO.,LTD.
0019E7	Cisco Systems, Inc
0019E8	Cisco Systems, Inc
0019E9	S-Information Technolgy, Co., Ltd.
0019EA	TeraMage Technologies Co., Ltd.
0019EB	Pyronix Ltd
0019EC	Sagamore Systems, Inc.
0019ED	Axesstel Inc.
0019EE	CARLO GAVAZZI CONTROLS SPA-Controls Division
0019EF	SHENZHEN LINNKING ELECTRONICS CO.,LTD
0019F0	UNIONMAN TECHNOLOGY CO.,LTD
0019F1	Star Communication Network Technology Co.,Ltd
0019F2	Teradyne K.K.
0019F3	Cetis, Inc
0019F4	Convergens Oy Ltd
0019F5	Imagination Technologies Ltd
0019F6	Acconet (PTE) Ltd
0019F7	Onset Computer Corporation
0019F8	Embedded Systems Design, Inc.
0019F9	TDK-Lambda
0019FA	Cable Vision Electronics CO., LTD.
0019FB	BSkyB Ltd
0019FC	PT. Ufoakses Sukses Luarbiasa
0019FD	Nintendo Co., Ltd.
0019FE	SHENZHEN SEECOMM TECHNOLOGY CO.,LTD.
0019FF	Finnzymes
001A00	MATRIX INC.
001A01	Smiths Medical
001A02	SECURE CARE PRODUCTS, INC
001A03	Angel Electronics Co., Ltd.
001A04	Interay Solutions BV
001A05	OPTIBASE LTD
001A06	OpVista, Inc.
001A07	Arecont Vision
001A08	Simoco Ltd.
001A09	Wayfarer Transit Systems Ltd
001A0A	Adaptive Micro-Ware Inc.
001A0B	BONA TECHNOLOGY INC.
001A0C	Swe-Dish Satellite Systems AB
001A0D	HandHeld entertainment, Inc.
001A0E	Cheng Uei Precision Industry Co.,Ltd
001A0F	Sistemas Avanzados de Control, S.A.
001A10	LUCENT TRANS ELECTRONICS CO.,LTD
001A11	Google, Inc.
001A12	Essilor
001A13	Wanlida Group Co., LTD
001A14	Xin Hua Control Engineering Co.,Ltd.
001A15	gemalto e-Payment
001A16	Nokia Danmark A/S
001A17	Teak Technologies, Inc.
001A18	Advanced Simulation Technology inc.
001A19	Computer Engineering Limited
001A1A	Gentex Corporation/Electro-Acoustic Products
001A1B	ARRIS Group, Inc.
001A1C	GT&T Engineering Pte Ltd
001A1D	PChome Online Inc.
001A1E	Aruba Networks
001A1F	Coastal Environmental Systems
001A20	CMOTECH Co. Ltd.
001A21	Brookhuis Applied Technologies BV
001A22	eQ-3 Entwicklung GmbH
001A23	Ice Qube, Inc
001A24	Galaxy Telecom Technologies Ltd
001A25	DELTA DORE
001A26	Deltanode Solutions AB
001A27	Ubistar
001A28	ASWT Co., LTD. Taiwan Branch H.K.
001A29	Johnson Outdoors Marine Electronics d/b/a Minnkota
001A2A	Arcadyan Technology Corporation
001A2B	Ayecom Technology Co., Ltd.
001A2C	SATEC Co.,LTD
001A2D	The Navvo Group
001A2E	Ziova Coporation
001A2F	Cisco Systems, Inc
001A30	Cisco Systems, Inc
001A31	SCAN COIN Industries AB
001A32	ACTIVA MULTIMEDIA
001A33	ASI Communications, Inc.
001A34	Konka Group Co., Ltd.
001A35	BARTEC GmbH
001A36	Aipermon GmbH & Co. KG
001A37	Lear Corporation
001A38	Sanmina-               # Sanmina-SCI
001A39	Merten GmbH&CoKG
001A3A	Dongahelecomm
001A3B	Doah Elecom Inc.
001A3C	Technowave Ltd.
001A3D	Ajin Vision Co.,Ltd
001A3E	Faster Technology LLC
001A3F	intelbras
001A40	A-FOUR TECH CO., LTD.
001A41	INOCOVA Co.,Ltd
001A42	Techcity Technology co., Ltd.
001A43	Logical Link Communications
001A44	JWTrading Co., Ltd
001A45	GN Netcom A/S
001A46	Digital Multimedia Technology Co., Ltd
001A47	Agami Systems, Inc.
001A48	Takacom Corporation
001A49	Micro Vision Co.,LTD
001A4A	Qumranet Inc.
001A4B	Hewlett Packard
001A4C	Crossbow Technology, Inc
001A4D	GIGA-BYTE TECHNOLOGY CO.,LTD.
001A4E	NTI AG / LinMot
001A4F	AVM GmbH
001A50	PheeNet Technology Corp.
001A51	Alfred Mann Foundation
001A52	Meshlinx Wireless Inc.
001A53	Zylaya
001A54	Hip Shing Electronics Ltd.
001A55	ACA-Digital Corporation
001A56	ViewTel Co,. Ltd.
001A57	Matrix Design Group, LLC
001A58	CCV Deutschland GmbH - Celectronic eHealth Div.
001A59	Ircona
001A5A	Korea Electric Power Data Network  (KDN) Co., Ltd
001A5B	NetCare Service Co., Ltd.
001A5C	Euchner GmbH+Co. KG
001A5D	Mobinnova Corp.
001A5E	Thincom Technology Co.,Ltd
001A5F	KitWorks.fi Ltd.
001A60	Wave Electronics Co.,Ltd.
001A61	PacStar Corp.
001A62	Data Robotics, Incorporated
001A63	Elster Solutions, LLC,
001A64	IBM Corp
001A65	Seluxit
001A66	ARRIS Group, Inc.
001A67	Infinite QL Sdn Bhd
001A68	Weltec Enterprise Co., Ltd.
001A69	Wuhan Yangtze Optical Technology CO.,Ltd.
001A6A	Tranzas, Inc.
001A6B	Universal Global Scientific Industrial Co., Ltd.
001A6C	Cisco Systems, Inc
001A6D	Cisco Systems, Inc
001A6E	Impro Technologies
001A6F	MI.TEL s.r.l.
001A70	Cisco-Linksys, LLC
001A71	Diostech Co., Ltd.
001A72	Mosart Semiconductor Corp.
001A73	Gemtek Technology Co., Ltd.
001A74	Procare International Co
001A75	Sony Mobile Communications AB
001A76	SDT information Technology Co.,LTD.
001A77	ARRIS Group, Inc.
001A78	Ubtos
001A79	TELECOMUNICATION TECHNOLOGIES LTD.
001A7A	Lismore Instruments Limited
001A7B	Teleco, Inc.
001A7C	Hirschmann Multimedia B.V.
001A7D	cyber-blue(HK)Ltd
001A7E	LN Srithai Comm Ltd.
001A7F	GCI Science & Technology Co.,LTD
001A80	Sony Corporation
001A81	Zelax
001A82	PROBA Building Automation Co.,LTD
001A83	Pegasus Technologies Inc.
001A84	V One Multimedia Pte Ltd
001A85	NV Michel Van de Wiele
001A86	AdvancedIO Systems Inc
001A87	Canhold International Limited
001A88	Venergy,Co,Ltd
001A89	Nokia Danmark A/S
001A8A	Samsung Electronics Co.,Ltd
001A8B	CHUNIL ELECTRIC IND., CO.
001A8C	Sophos Ltd
001A8D	AVECS Bergen GmbH
001A8E	3Way Networks Ltd
001A8F	Nortel Networks
001A90	Trópico Sistemas e Telecomunicações da Amazônia LTDA.
001A91	FusionDynamic Ltd.
001A92	ASUSTek COMPUTER INC.
001A93	ERCO Leuchten GmbH
001A94	Votronic GmbH
001A95	Hisense Mobile Communications Technoligy Co.,Ltd.
001A96	ECLER S.A.
001A97	fitivision technology Inc.
001A98	Asotel Communication Limited Taiwan Branch
001A99	Smarty (HZ) Information Electronics Co., Ltd
001A9A	Skyworth Digital Technology(Shenzhen) Co.,Ltd
001A9B	ADEC & Parter AG
001A9C	RightHand Technologies, Inc.
001A9D	Skipper Wireless, Inc.
001A9E	ICON Digital International Limited
001A9F	A-Link Ltd
001AA0	Dell Inc.
001AA1	Cisco Systems, Inc
001AA2	Cisco Systems, Inc
001AA3	Delorme
001AA4	Future University-Hakodate
001AA5	BRN Phoenix
001AA6	Telefunken Radio Communication Systems GmbH &CO.KG
001AA7	Torian Wireless
001AA8	Mamiya Digital Imaging Co., Ltd.
001AA9	FUJIAN STAR-NET COMMUNICATION CO.,LTD
001AAA	Analogic Corp.
001AAB	eWings s.r.l.
001AAC	Corelatus AB
001AAD	ARRIS Group, Inc.
001AAE	Savant Systems LLC
001AAF	BLUSENS TECHNOLOGY
001AB0	Signal Networks Pvt. Ltd.,
001AB1	Asia Pacific Satellite Industries Co., Ltd.
001AB2	Cyber Solutions Inc.
001AB3	VISIONITE INC.
001AB4	FFEI Ltd.
001AB5	Home Network System
001AB6	Texas Instruments
001AB7	Ethos Networks LTD.
001AB8	Anseri Corporation
001AB9	Pmc
001ABA	Caton Overseas Limited
001ABB	Fontal Technology Incorporation
001ABC	U4EA Technologies Ltd
001ABD	Impatica Inc.
001ABE	COMPUTER HI-TECH INC.
001ABF	TRUMPF Laser Marking Systems AG
001AC0	JOYBIEN TECHNOLOGIES CO., LTD.
001AC1	3Com Ltd
001AC2	YEC Co.,Ltd.
001AC3	Scientific-Atlanta, Inc
001AC4	2Wire Inc
001AC5	BreakingPoint Systems, Inc.
001AC6	Micro Control Designs
001AC7	Unipoint
001AC8	ISL (Instrumentation Scientifique de Laboratoire)
001AC9	SUZUKEN CO.,LTD
001ACA	Tilera Corporation
001ACB	Autocom Products Ltd
001ACC	Celestial Semiconductor, Ltd
001ACD	Tidel Engineering LP
001ACE	YUPITERU CORPORATION
001ACF	C.T. ELETTRONICA
001AD0	Albis Technologies AG
001AD1	FARGO CO., LTD.
001AD2	Eletronica Nitron Ltda
001AD3	Vamp Ltd.
001AD4	iPOX Technology Co., Ltd.
001AD5	KMC CHAIN INDUSTRIAL CO., LTD.
001AD6	JIAGNSU AETNA ELECTRIC CO.,LTD
001AD7	Christie Digital Systems, Inc.
001AD8	AlsterAero GmbH
001AD9	International Broadband Electric Communications, Inc.
001ADA	Biz-2-Me Inc.
001ADB	ARRIS Group, Inc.
001ADC	Nokia Danmark A/S
001ADD	PePWave Ltd
001ADE	ARRIS Group, Inc.
001ADF	Interactivetv Pty Limited
001AE0	Mythology Tech Express Inc.
001AE1	EDGE ACCESS INC
001AE2	Cisco Systems, Inc
001AE3	Cisco Systems, Inc
001AE4	Medicis Technologies Corporation
001AE5	Mvox Technologies Inc.
001AE6	Atlanta Advanced Communications Holdings Limited
001AE7	Aztek Networks, Inc.
001AE8	Unify Software and Solutions GmbH & Co. KG
001AE9	Nintendo Co., Ltd.
001AEA	Radio Terminal Systems Pty Ltd
001AEB	Allied Telesis R&D Center K.K.
001AEC	Keumbee Electronics Co.,Ltd.
001AED	INCOTEC GmbH
001AEE	Shenztech Ltd
001AEF	Loopcomm Technology, Inc.
001AF0	Alcatel-               # Alcatel-Lucent IPD
001AF1	Embedded Artists AB
001AF2	Dynavisions Schweiz AG
001AF3	Samyoung Electronics
001AF4	Handreamnet
001AF5	PENTAONE. CO., LTD.
001AF6	Woven Systems, Inc.
001AF7	dataschalt e+a GmbH
001AF8	Copley Controls Corporation
001AF9	AeroVIronment (AV Inc)
001AFA	Welch Allyn, Inc.
001AFB	Joby Inc.
001AFC	ModusLink Corporation
001AFD	Evolis
001AFE	SOFACREAL
001AFF	Wizyoung Tech.
001B00	Neopost Technologies
001B01	Applied Radio Technologies
001B02	ED Co.Ltd
001B03	Action Technology (SZ) Co., Ltd
001B04	Affinity International S.p.a
001B05	YMC AG
001B06	Ateliers R. LAUMONIER
001B07	Mendocino Software
001B08	Danfoss Drives A/S
001B09	Matrix Telecom Pvt. Ltd.
001B0A	Intelligent Distributed Controls Ltd
001B0B	Phidgets Inc.
001B0C	Cisco Systems, Inc
001B0D	Cisco Systems, Inc
001B0E	InoTec GmbH Organisationssysteme
001B0F	Petratec
001B10	ShenZhen Kang Hui Technology Co.,ltd
001B11	D-Link Corporation
001B12	Apprion
001B13	Icron Technologies Corporation
001B14	Carex Lighting Equipment Factory
001B15	Voxtel, Inc.
001B16	Celtro Ltd.
001B17	Palo Alto Networks
001B18	Tsuken Electric Ind. Co.,Ltd
001B19	IEEE I&M Society TC9
001B1A	e-trees Japan, Inc.
001B1B	Siemens AG,
001B1C	Coherent
001B1D	Phoenix International Co., Ltd
001B1E	HART Communication Foundation
001B1F	DELTA - Danish Electronics, Light & Acoustics
001B20	TPine Technology
001B21	Intel Corporate
001B22	Palit Microsystems ( H.K.) Ltd.
001B23	SimpleComTools
001B24	QUANTA COMPUTER INC.
001B25	Nortel Networks
001B26	RON-Telecom ZAO
001B27	Merlin CSI
001B28	POLYGON, JSC
001B29	Avantis.Co.,Ltd
001B2A	Cisco Systems, Inc
001B2B	Cisco Systems, Inc
001B2C	ATRON electronic GmbH
001B2D	Med-Eng Systems Inc.
001B2E	Sinkyo Electron Inc
001B2F	Netgear
001B30	Solitech Inc.
001B31	Neural Image. Co. Ltd.
001B32	QLogic Corporation
001B33	Nokia Danmark A/S
001B34	Focus System Inc.
001B35	ChongQing JINOU Science & Technology Development CO.,Ltd
001B36	Tsubata Engineering Co.,Ltd. (Head Office)
001B37	Computec Oy
001B38	COMPAL INFORMATION (KUNSHAN) CO., LTD.
001B39	Proxicast
001B3A	SIMS Corp.
001B3B	Yi-Qing CO., LTD
001B3C	Software Technologies Group,Inc.
001B3D	EuroTel Spa
001B3E	Curtis, Inc.
001B3F	ProCurve Networking by HP
001B40	Network Automation mxc AB
001B41	General Infinity Co.,Ltd.
001B42	Wise & Blue
001B43	Beijing DG Telecommunications equipment Co.,Ltd
001B44	SanDisk Corporation
001B45	ABB AS, Division Automation Products
001B46	Blueone Technology Co.,Ltd
001B47	Futarque A/S
001B48	Shenzhen Lantech Electronics Co., Ltd.
001B49	Roberts Radio limited
001B4A	W&W Communications, Inc.
001B4B	SANION Co., Ltd.
001B4C	Signtech
001B4D	Areca Technology Corporation
001B4E	Navman New Zealand
001B4F	Avaya Inc
001B50	Nizhny Novgorod Factory named after M.Frunze, FSUE (NZiF)
001B51	Vector Technology Corp.
001B52	ARRIS Group, Inc.
001B53	Cisco Systems, Inc
001B54	Cisco Systems, Inc
001B55	Hurco Automation Ltd.
001B56	Tehuti Networks Ltd.
001B57	SEMINDIA SYSTEMS PRIVATE LIMITED
001B58	ACE CAD Enterprise Co., Ltd.
001B59	Sony Mobile Communications AB
001B5A	Apollo Imaging Technologies, Inc.
001B5B	2Wire Inc
001B5C	Azuretec Co., Ltd.
001B5D	Vololink Pty Ltd
001B5E	BPL Limited
001B5F	Alien Technology
001B60	NAVIGON AG
001B61	Digital Acoustics, LLC
001B62	JHT Optoelectronics Co.,Ltd.
001B63	Apple, Inc.
001B64	IsaacLandKorea Co., Ltd,
001B65	China Gridcom Co., Ltd
001B66	Sennheiser electronic GmbH & Co. KG
001B67	Cisco Systems Inc
001B68	Modnnet Co., Ltd
001B69	Equaline Corporation
001B6A	Powerwave Technologies Sweden AB
001B6B	Swyx Solutions AG
001B6C	LookX Digital Media BV
001B6D	Midtronics, Inc.
001B6E	Anue Systems, Inc.
001B6F	Teletrak Ltd
001B70	IRI Ubiteq, INC.
001B71	Telular Corp.
001B72	Sicep s.p.a.
001B73	DTL Broadcast Ltd
001B74	MiraLink Corporation
001B75	Hypermedia Systems
001B76	Ripcode, Inc.
001B77	Intel Corporate
001B78	Hewlett Packard
001B79	FAIVELEY TRANSPORT
001B7A	Nintendo Co., Ltd.
001B7B	The Tintometer Ltd
001B7C	A & R Cambridge
001B7D	CXR Anderson Jacobson
001B7E	Beckmann GmbH
001B7F	TMN Technologies Telecomunicacoes Ltda
001B80	LORD Corporation
001B81	DATAQ Instruments, Inc.
001B82	Taiwan Semiconductor Co., Ltd.
001B83	Finsoft Ltd
001B84	Scan Engineering Telecom
001B85	MAN Diesel SE
001B86	Bosch Access Systems GmbH
001B87	Deepsound Tech. Co., Ltd
001B88	Divinet Access Technologies Ltd
001B89	EMZA Visual Sense Ltd.
001B8A	2M Electronic A/S
001B8B	NEC Platforms, Ltd.
001B8C	JMicron Technology Corp.
001B8D	Electronic Computer Systems, Inc.
001B8E	Hulu Sweden AB
001B8F	Cisco Systems, Inc
001B90	Cisco Systems, Inc
001B91	EFKON AG
001B92	l-acoustics
001B93	JC Decaux SA DNT
001B94	T.E.M.A. S.p.A.
001B95	VIDEO SYSTEMS SRL
001B96	General Sensing
001B97	Violin Technologies
001B98	Samsung Electronics Co.,Ltd
001B99	KS System GmbH
001B9A	Apollo Fire Detectors Ltd
001B9B	Hose-McCann Communications
001B9C	SATEL sp. z o.o.
001B9D	Novus Security Sp. z o.o.
001B9E	ASKEY COMPUTER CORP
001B9F	Calyptech Pty Ltd
001BA0	Awox
001BA1	Åmic AB
001BA2	IDS Imaging Development Systems GmbH
001BA3	Flexit Group GmbH
001BA4	S.A.E Afikim
001BA5	MyungMin Systems, Inc.
001BA6	intotech inc.
001BA7	Lorica Solutions
001BA8	UBI&MOBI,.Inc
001BA9	Brother industries, LTD.
001BAA	XenICs nv
001BAB	Telchemy, Incorporated
001BAC	Curtiss Wright Controls Embedded Computing
001BAD	iControl Incorporated
001BAE	Micro Control Systems, Inc
001BAF	Nokia Danmark A/S
001BB0	BHARAT ELECTRONICS
001BB1	Wistron Neweb Corporation
001BB2	Intellect International NV
001BB3	Condalo GmbH
001BB4	Airvod Limited
001BB5	Cherry GmbH
001BB6	Bird Electronic Corp.
001BB7	Alta Heights Technology Corp.
001BB8	BLUEWAY ELECTRONIC CO;LTD
001BB9	Elitegroup Computer Systems Co.,Ltd.
001BBA	Nortel Networks
001BBB	RFTech Co.,Ltd
001BBC	Silver Peak Systems, Inc.
001BBD	FMC Kongsberg Subsea AS
001BBE	ICOP Digital
001BBF	Sagemcom Broadband SAS
001BC0	Juniper Networks
001BC1	HOLUX Technology, Inc.
001BC2	Integrated Control Technology Limitied
001BC3	Mobisolution Co.,Ltd
001BC4	Ultratec, Inc.
001BC5	IEEE Registration Authority
001BC6	Strato Rechenzentrum AG
001BC7	StarVedia Technology Inc.
001BC8	MIURA CO.,LTD
001BC9	FSN DISPLAY INC
001BCA	Beijing Run Technology LTD. Company
001BCB	PEMPEK SYSTEMS PTY LTD
001BCC	KINGTEK CCTV ALLIANCE CO., LTD.
001BCD	DAVISCOMMS (S) PTE LTD
001BCE	Measurement Devices Ltd
001BCF	Dataupia Corporation
001BD0	IDENTEC SOLUTIONS
001BD1	SOGESTMATIC
001BD2	ULTRA-X ASIA PACIFIC Inc.
001BD3	Panasonic Corp. AVC Company
001BD4	Cisco Systems, Inc
001BD5	Cisco Systems, Inc
001BD6	Kelvin Hughes Ltd
001BD7	Cisco SPVTG
001BD8	DVTel LTD
001BD9	Edgewater Computer Systems
001BDA	UTStarcom Inc
001BDB	Valeo VECS
001BDC	Vencer Co., Ltd.
001BDD	ARRIS Group, Inc.
001BDE	Renkus-Heinz, Inc.
001BDF	Iskra Sistemi d.d.
001BE0	TELENOT ELECTRONIC GmbH
001BE1	Vialogy
001BE2	AhnLab,Inc.
001BE3	Health Hero Network, Inc.
001BE4	TOWNET SRL
001BE5	802automation Limited
001BE6	VR AG
001BE7	Postek Electronics Co., Ltd.
001BE8	Ultratronik GmbH
001BE9	Broadcom
001BEA	Nintendo Co., Ltd.
001BEB	DMP Electronics INC.
001BEC	Netio Technologies Co., Ltd
001BED	Brocade Communications Systems, Inc.
001BEE	Nokia Danmark A/S
001BEF	Blossoms Digital Technology Co.,Ltd.
001BF0	Value Platforms Limited
001BF1	Nanjing SilverNet Software Co., Ltd.
001BF2	KWORLD COMPUTER CO., LTD
001BF3	TRANSRADIO SenderSysteme Berlin AG
001BF4	KENWIN INDUSTRIAL(HK) LTD.
001BF5	Tellink Sistemas de Telecomunicación S.L.
001BF6	CONWISE Technology Corporation Ltd.
001BF7	Lund IP Products AB
001BF8	Digitrax Inc.
001BF9	Intellitect Water Ltd
001BFA	G.i.N. mbH
001BFB	ALPS ELECTRIC CO.,LTD.
001BFC	ASUSTek COMPUTER INC.
001BFD	Dignsys Inc.
001BFE	Zavio Inc.
001BFF	Millennia Media inc.
001C00	Entry Point, LLC
001C01	ABB Oy Drives
001C02	Pano Logic
001C03	Betty TV Technology AG
001C04	Airgain, Inc.
001C05	Nonin Medical Inc.
001C06	Siemens Numerical Control Ltd., Nanjing
001C07	Cwlinux Limited
001C08	Echo360, Inc.
001C09	SAE Electronic Co.,Ltd.
001C0A	Shenzhen AEE Technology Co.,Ltd.
001C0B	SmartAnt Telecom
001C0C	TANITA Corporation
001C0D	G-Technology, Inc.
001C0E	Cisco Systems, Inc
001C0F	Cisco Systems, Inc
001C10	Cisco-Linksys, LLC
001C11	ARRIS Group, Inc.
001C12	ARRIS Group, Inc.
001C13	OPTSYS TECHNOLOGY CO., LTD.
001C14	VMware, Inc.
001C15	iPhotonix LLC
001C16	ThyssenKrupp Elevator
001C17	Nortel Networks
001C18	Sicert S.r.L.
001C19	secunet Security Networks AG
001C1A	Thomas Instrumentation, Inc
001C1B	Hyperstone GmbH
001C1C	Center Communication Systems GmbH
001C1D	CHENZHOU GOSPELL DIGITAL TECHNOLOGY CO.,LTD
001C1E	emtrion GmbH
001C1F	Quest Retail Technology Pty Ltd
001C20	CLB Benelux
001C21	Nucsafe Inc.
001C22	Aeris Elettronica s.r.l.
001C23	Dell Inc.
001C24	Formosa Wireless Systems Corp.
001C25	Hon Hai Precision Ind. Co.,Ltd.
001C26	Hon Hai Precision Ind. Co.,Ltd.
001C27	Sunell Electronics Co.
001C28	Sphairon Technologies GmbH
001C29	CORE DIGITAL ELECTRONICS CO., LTD
001C2A	Envisacor Technologies Inc.
001C2B	Alertme.com Limited
001C2C	Synapse
001C2D	FlexRadio Systems
001C2E	HPN Supply Chain
001C2F	Pfister GmbH
001C30	Mode Lighting (UK ) Ltd.
001C31	Mobile XP Technology Co., LTD
001C32	Telian Corporation
001C33	Sutron
001C34	HUEY CHIAO INTERNATIONAL CO., LTD.
001C35	Nokia Danmark A/S
001C36	iNEWiT NV
001C37	Callpod, Inc.
001C38	Bio-Rad Laboratories, Inc.
001C39	S Netsystems Inc.
001C3A	Element Labs, Inc.
001C3B	AmRoad Technology Inc.
001C3C	Seon Design Inc.
001C3D	WaveStorm
001C3E	ECKey Corporation
001C3F	International Police Technologies, Inc.
001C40	VDG-Security bv
001C41	scemtec Transponder Technology GmbH
001C42	Parallels, Inc.
001C43	Samsung Electronics Co.,Ltd
001C44	Bosch Security Systems BV
001C45	Chenbro Micom Co., Ltd.
001C46	Qtum
001C47	Hangzhou Hollysys Automation Co., Ltd
001C48	WiDeFi, Inc.
001C49	Zoltan Technology Inc.
001C4A	AVM GmbH
001C4B	Gener8, Inc.
001C4C	Petrotest Instruments
001C4D	Aplix IP Holdings Corporation
001C4E	TASA International Limited
001C4F	MACAB AB
001C50	TCL Technoly Electronics (Huizhou) Co., Ltd.
001C51	Celeno Communications
001C52	VISIONEE SRL
001C53	Synergy Lighting Controls
001C54	Hillstone Networks Inc
001C55	Shenzhen Kaifa Technology Co.
001C56	Pado Systems, Inc.
001C57	Cisco Systems, Inc
001C58	Cisco Systems, Inc
001C59	DEVON IT
001C5A	Advanced Relay Corporation
001C5B	Chubb Electronic Security Systems Ltd
001C5C	Integrated Medical Systems, Inc.
001C5D	Leica Microsystems
001C5E	ASTON France
001C5F	Winland Electronics, Inc.
001C60	CSP Frontier Technologies,Inc.
001C61	Galaxy  Microsystems LImited
001C62	LG Electronics (Mobile Communications)
001C63	Truen
001C64	Landis+Gyr
001C65	JoeScan, Inc.
001C66	UCAMP CO.,LTD
001C67	Pumpkin Networks, Inc.
001C68	Anhui Sun Create Electronics Co., Ltd
001C69	Packet Vision Ltd
001C6A	Weiss Engineering Ltd.
001C6B	COVAX  Co. Ltd
001C6C	30805
001C6D	KYOHRITSU ELECTRONIC INDUSTRY CO., LTD.
001C6E	Newbury Networks, Inc.
001C6F	Emfit Ltd
001C70	NOVACOMM LTDA
001C71	Emergent Electronics
001C72	Mayer & Cie GmbH & Co KG
001C73	Arista Networks, Inc.
001C74	Syswan Technologies Inc.
001C75	Segnet Ltd.
001C76	The Wandsworth Group Ltd
001C77	Prodys
001C78	WYPLAY SAS
001C79	Cohesive Financial Technologies LLC
001C7A	Perfectone Netware Company Ltd
001C7B	Castlenet Technology Inc.
001C7C	PERQ SYSTEMS CORPORATION
001C7D	Excelpoint Manufacturing Pte Ltd
001C7E	Toshiba
001C7F	Check Point Software Technologies
001C80	New Business Division/Rhea-Information CO., LTD.
001C81	NextGen Venturi LTD
001C82	Genew Technologies
001C83	New Level Telecom Co., Ltd.
001C84	STL Solution Co.,Ltd.
001C85	Eunicorn
001C86	Cranite Systems, Inc.
001C87	Uriver Inc.
001C88	TRANSYSTEM INC.
001C89	Force Communications, Inc.
001C8A	Cirrascale Corporation
001C8B	MJ Innovations Ltd.
001C8C	DIAL TECHNOLOGY LTD.
001C8D	Mesa Imaging
001C8E	Alcatel-               # Alcatel-Lucent IPD
001C8F	Advanced Electronic Design, Inc.
001C90	Empacket Corporation
001C91	Gefen Inc.
001C92	Tervela
001C93	ExaDigm Inc
001C94	LI-COR Biosciences
001C95	Opticomm Corporation
001C96	Linkwise Technology Pte Ltd
001C97	Enzytek Technology Inc.,
001C98	LUCKY TECHNOLOGY (HK) COMPANY LIMITED
001C99	Shunra Software Ltd.
001C9A	Nokia Danmark A/S
001C9B	FEIG ELECTRONIC GmbH
001C9C	Nortel Networks
001C9D	Liecthi AG
001C9E	Dualtech IT AB
001C9F	Razorstream, LLC
001CA0	Production Resource Group, LLC
001CA1	AKAMAI TECHNOLOGIES, INC.
001CA2	ADB Broadband Italia
001CA3	Terra
001CA4	Sony Mobile Communications AB
001CA5	Zygo Corporation
001CA6	Win4net
001CA7	International Quartz Limited
001CA8	AirTies Wireless Networks
001CA9	Audiomatica Srl
001CAA	Bellon Pty Ltd
001CAB	Meyer Sound Laboratories, Inc.
001CAC	Qniq Technology Corp.
001CAD	Wuhan Telecommunication Devices Co.,Ltd
001CAE	WiChorus, Inc.
001CAF	Plato Networks Inc.
001CB0	Cisco Systems, Inc
001CB1	Cisco Systems, Inc
001CB2	BPT SPA
001CB3	Apple, Inc.
001CB4	Iridium Satellite LLC
001CB5	Neihua Network Technology Co.,LTD.(NHN)
001CB6	Duzon CNT Co., Ltd.
001CB7	USC DigiArk Corporation
001CB8	CBC Co., Ltd
001CB9	KWANG SUNG ELECTRONICS CO., LTD.
001CBA	VerScient, Inc.
001CBB	MusicianLink
001CBC	CastGrabber, LLC
001CBD	Ezze Mobile Tech., Inc.
001CBE	Nintendo Co., Ltd.
001CBF	Intel Corporate
001CC0	Intel Corporate
001CC1	ARRIS Group, Inc.
001CC2	Part II Research, Inc.
001CC3	ARRIS Group, Inc.
001CC4	Hewlett Packard
001CC5	3Com Ltd
001CC6	ProStor Systems
001CC7	Rembrandt Technologies, LLC d/b/a REMSTREAM
001CC8	INDUSTRONIC Industrie-Electronic GmbH & Co. KG
001CC9	Kaise Electronic Technology Co., Ltd.
001CCA	Shanghai Gaozhi Science & Technology Development Co.
001CCB	Forth Corporation Public Company Limited
001CCC	BlackBerry RTS
001CCD	Alektrona Corporation
001CCE	By Techdesign
001CCF	Limetek
001CD0	Circleone Co.,Ltd.
001CD1	Waves Audio LTD
001CD2	King Champion (Hong Kong) Limited
001CD3	ZP Engineering SEL
001CD4	Nokia Danmark A/S
001CD5	ZeeVee, Inc.
001CD6	Nokia Danmark A/S
001CD7	Harman/Becker Automotive Systems GmbH
001CD8	BlueAnt Wireless
001CD9	GlobalTop Technology Inc.
001CDA	Exegin Technologies Limited
001CDB	CARPOINT CO.,LTD
001CDC	Custom Computer Services, Inc.
001CDD	COWBELL ENGINEERING CO., LTD.
001CDE	Interactive Multimedia eXchange Inc.
001CDF	Belkin International Inc.
001CE0	DASAN TPS
001CE1	INDRA SISTEMAS, S.A.
001CE2	Attero Tech, LLC.
001CE3	Optimedical Systems
001CE4	EleSy JSC
001CE5	MBS Electronic Systems GmbH
001CE6	Innes
001CE7	Rocon PLC Research Centre
001CE8	Cummins Inc
001CE9	Galaxy Technology Limited
001CEA	Scientific-Atlanta, Inc
001CEB	Nortel Networks
001CEC	Mobilesoft (Aust.) Pty Ltd
001CED	ENVIRONNEMENT SA
001CEE	SHARP Corporation
001CEF	Primax Electronics Ltd.
001CF0	D-Link Corporation
001CF1	SUPoX Technology Co. , LTD.
001CF2	Tenlon Technology Co.,Ltd.
001CF3	EVS BROADCAST EQUIPMENT
001CF4	Media Technology Systems Inc
001CF5	Wiseblue Technology Limited
001CF6	Cisco Systems, Inc
001CF7	AudioScience
001CF8	Parade Technologies, Ltd.
001CF9	Cisco Systems, Inc
001CFA	Alarm.com
001CFB	ARRIS Group, Inc.
001CFC	Sumitomo Electric Industries,Ltd
001CFD	Universal Electronics, Inc.
001CFE	Quartics Inc
001CFF	Napera Networks Inc
001D00	Brivo Systems, LLC
001D01	Neptune Digital
001D02	Cybertech Telecom Development
001D03	Design Solutions Inc.
001D04	Zipit Wireless, Inc.
001D05	Eaton Corporation
001D06	HM Electronics, Inc.
001D07	Shenzhen Sang Fei Consumer Communications Co.,Ltd
001D08	Jiangsu Yinhe  Electronics Co.,Ltd.
001D09	Dell Inc.
001D0A	Davis Instruments, Inc.
001D0B	Power Standards Lab
001D0C	MobileCompia
001D0D	Sony Interactive Entertainment Inc.
001D0E	Agapha Technology co., Ltd.
001D0F	TP-LINK TECHNOLOGIES CO.,LTD.
001D10	LightHaus Logic, Inc.
001D11	Analogue & Micro Ltd
001D12	ROHM CO., LTD.
001D13	Nextgtv
001D14	SPERADTONE INFORMATION TECHNOLOGY LIMITED
001D15	Shenzhen Dolphin Electronic Co., Ltd
001D16	Sfr
001D17	Digital Sky Corporation
001D18	Power Innovation GmbH
001D19	Arcadyan Technology Corporation
001D1A	OvisLink S.A.
001D1B	Sangean Electronics Inc.
001D1C	Gennet s.a.
001D1D	Inter-M Corporation
001D1E	KYUSHU TEN CO.,LTD
001D1F	Siauliu Tauro Televizoriai, JSC
001D20	Comtrend Corporation
001D21	Alcad SL
001D22	Foss Analytical A/S
001D23	Sensus
001D24	Aclara Power-Line Systems Inc.
001D25	Samsung Electronics Co.,Ltd
001D26	Rockridgesound Technology Co.
001D27	NAC-INTERCOM
001D28	Sony Mobile Communications AB
001D29	Doro AB
001D2A	SHENZHEN BUL-TECH CO.,LTD.
001D2B	Wuhan Pont Technology CO. , LTD
001D2C	Wavetrend Technologies (Pty) Limited
001D2D	Pylone, Inc.
001D2E	Ruckus Wireless
001D2F	QuantumVision Corporation
001D30	YX Wireless S.A.
001D31	HIGHPRO INTERNATIONAL R&D CO,.LTD.
001D32	Longkay Communication & Technology (Shanghai) Co. Ltd
001D33	Maverick Systems Inc.
001D34	SYRIS Technology Corp
001D35	Viconics Electronics Inc.
001D36	ELECTRONICS CORPORATION OF INDIA LIMITED
001D37	Thales-Panda Transportation System
001D38	Seagate Technology
001D39	MOOHADIGITAL CO., LTD
001D3A	mh acoustics LLC
001D3B	Nokia Danmark A/S
001D3C	Muscle Corporation
001D3D	Avidyne Corporation
001D3E	SAKA TECHNO SCIENCE CO.,LTD
001D3F	Mitron Pty Ltd
001D40	Intel – GE Care Innovations LLC
001D41	Hardy Instruments
001D42	Nortel Networks
001D43	Shenzhen G-link Digital Technology Co., Ltd.
001D44	Krohne
001D45	Cisco Systems, Inc
001D46	Cisco Systems, Inc
001D47	Covote GmbH & Co KG
001D48	Sensor-Technik Wiedemann GmbH
001D49	Innovation Wireless Inc.
001D4A	Carestream Health, Inc.
001D4B	Grid Connect Inc.
001D4C	Alcatel-               # Alcatel-Lucent
001D4D	Adaptive Recognition Hungary, Inc
001D4E	TCM Mobile LLC
001D4F	Apple, Inc.
001D50	SPINETIX SA
001D51	Babcock & Wilcox Power Generation Group, Inc
001D52	Defzone B.V.
001D53	S&O Electronics (Malaysia) Sdn. Bhd.
001D54	Sunnic Technology & Merchandise INC.
001D55	ZANTAZ, Inc
001D56	Kramer Electronics Ltd.
001D57	CAETEC Messtechnik
001D58	CQ Inc
001D59	Mitra Energy & Infrastructure
001D5A	2Wire Inc
001D5B	Tecvan Informática Ltda
001D5C	Tom Communication Industrial Co.,Ltd.
001D5D	Control Dynamics Pty. Ltd.
001D5E	COMING MEDIA CORP.
001D5F	OverSpeed SARL
001D60	ASUSTek COMPUTER INC.
001D61	BIJ Corporation
001D62	InPhase Technologies
001D63	Miele & Cie. KG
001D64	Adam Communications Systems Int Ltd
001D65	Microwave Radio Communications
001D66	Hyundai Telecom
001D67	Amec
001D68	Thomson Telecom Belgium
001D69	Knorr-Bremse IT-Services GmbH
001D6A	Alpha Networks Inc.
001D6B	ARRIS Group, Inc.
001D6C	ClariPhy Communications, Inc.
001D6D	Confidant International LLC
001D6E	Nokia Danmark A/S
001D6F	Chainzone Technology Co., Ltd
001D70	Cisco Systems, Inc
001D71	Cisco Systems, Inc
001D72	Wistron Corporation
001D73	BUFFALO.INC
001D74	Tianjin China-Silicon Microelectronics Co., Ltd.
001D75	Radioscape PLC
001D76	Eyeheight Ltd.
001D77	Nsgate
001D78	Invengo Information Technology Co.,Ltd
001D79	SIGNAMAX LLC
001D7A	Wideband Semiconductor, Inc.
001D7B	Ice Energy, Inc.
001D7C	ABE Elettronica S.p.A.
001D7D	GIGA-BYTE TECHNOLOGY CO.,LTD.
001D7E	Cisco-Linksys, LLC
001D7F	Tekron International Ltd
001D80	Beijing Huahuan Eletronics Co.,Ltd
001D81	GUANGZHOU GATEWAY ELECTRONICS CO., LTD
001D82	GN Netcom A/S
001D83	Emitech Corporation
001D84	Gateway, Inc.
001D85	Call Direct Cellular Solutions
001D86	Shinwa Industries(China) Ltd.
001D87	VigTech Labs Sdn Bhd
001D88	Clearwire
001D89	VaultStor Corporation
001D8A	TechTrex Inc
001D8B	ADB Broadband Italia
001D8C	La Crosse Technology LTD
001D8D	Raytek GmbH
001D8E	Alereon, Inc.
001D8F	PureWave Networks
001D90	EMCO Flow Systems
001D91	Digitize, Inc
001D92	MICRO-STAR INT'L CO.,LTD.
001D93	Modacom
001D94	Climax Technology Co., Ltd
001D95	Flash, Inc.
001D96	WatchGuard Video
001D97	Alertus Technologies LLC
001D98	Nokia Danmark A/S
001D99	Cyan Optic, Inc.
001D9A	GODEX INTERNATIONAL CO., LTD
001D9B	Hokuyo Automatic Co., Ltd.
001D9C	Rockwell Automation
001D9D	ARTJOY INTERNATIONAL LIMITED
001D9E	AXION TECHNOLOGIES
001D9F	MATT   R.P.Traczynscy Sp.J.
001DA0	Heng Yu Electronic Manufacturing Company Limited
001DA1	Cisco Systems, Inc
001DA2	Cisco Systems, Inc
001DA3	Sabioso
001DA4	Hangzhou System Technology CO., LTD
001DA5	WB Electronics
001DA6	Media Numerics Limited
001DA7	Seamless Internet
001DA8	Takahata Electronics Co.,Ltd
001DA9	Castles Technology, Co., LTD
001DAA	DrayTek Corp.
001DAB	SwissQual License AG
001DAC	Gigamon Systems LLC
001DAD	Sinotech Engineering Consultants, Inc.  Geotechnical Enginee
001DAE	CHANG TSENG TECHNOLOGY CO., LTD
001DAF	Nortel Networks
001DB0	FuJian HengTong Information Technology Co.,Ltd
001DB1	Crescendo Networks
001DB2	HOKKAIDO ELECTRIC ENGINEERING CO.,LTD.
001DB3	HPN Supply Chain
001DB4	KUMHO ENG CO.,LTD
001DB5	Juniper Networks
001DB6	BestComm Networks, Inc.
001DB7	Tendril Networks, Inc.
001DB8	Intoto Inc.
001DB9	Wellspring Wireless
001DBA	Sony Corporation
001DBB	Dynamic System Electronics Corp.
001DBC	Nintendo Co., Ltd.
001DBD	Versamed Inc.
001DBE	ARRIS Group, Inc.
001DBF	Radiient Technologies, Inc.
001DC0	Enphase Energy
001DC1	Audinate Pty L
001DC2	XORTEC OY
001DC3	RIKOR TV, Ltd
001DC4	AIOI Systems Co., Ltd.
001DC5	Beijing Jiaxun Feihong Electricial Co., Ltd.
001DC6	SNR Inc.
001DC7	L-3 Communications Geneva Aerospace
001DC8	Navionics Research Inc., dba SCADAmetrics
001DC9	GainSpan Corp.
001DCA	PAV Electronics Limited
001DCB	Exéns Development Oy
001DCC	Hetra Secure Solutions
001DCD	ARRIS Group, Inc.
001DCE	ARRIS Group, Inc.
001DCF	ARRIS Group, Inc.
001DD0	ARRIS Group, Inc.
001DD1	ARRIS Group, Inc.
001DD2	ARRIS Group, Inc.
001DD3	ARRIS Group, Inc.
001DD4	ARRIS Group, Inc.
001DD5	ARRIS Group, Inc.
001DD6	ARRIS Group, Inc.
001DD7	Algolith
001DD8	Microsoft Corporation
001DD9	Hon Hai Precision Ind. Co.,Ltd.
001DDA	Mikroelektronika spol. s r. o.
001DDB	C-BEL Corporation
001DDC	HangZhou DeChangLong Tech&Info Co.,Ltd
001DDD	DAT H.K. LIMITED
001DDE	Zhejiang Broadcast&Television Technology Co.,Ltd.
001DDF	Sunitec Enterprise Co., Ltd.
001DE0	Intel Corporate
001DE1	Intel Corporate
001DE2	Radionor Communications
001DE3	Intuicom
001DE4	Visioneered Image Systems
001DE5	Cisco Systems, Inc
001DE6	Cisco Systems, Inc
001DE7	Marine Sonic Technology, Ltd.
001DE8	Nikko Denki Tsushin Corporation(NDTC)
001DE9	Nokia Danmark A/S
001DEA	Commtest Instruments Ltd
001DEB	DINEC International
001DEC	Marusys
001DED	Grid Net, Inc.
001DEE	NEXTVISION SISTEMAS DIGITAIS DE TELEVISÃO LTDA.
001DEF	TRIMM, INC.
001DF0	Vidient Systems, Inc.
001DF1	Intego Systems, Inc.
001DF2	Netflix, Inc.
001DF3	SBS Science & Technology Co., Ltd
001DF4	Magellan Technology Pty Limited
001DF5	Sunshine Co,LTD
001DF6	Samsung Electronics Co.,Ltd
001DF7	R. STAHL Schaltgeräte GmbH
001DF8	Webpro Vision Technology Corporation
001DF9	Cybiotronics (Far East) Limited
001DFA	Fujian LANDI Commercial Equipment Co.,Ltd
001DFB	NETCLEUS Systems Corporation
001DFC	Ksic
001DFD	Nokia Danmark A/S
001DFE	Palm, Inc
001DFF	Network Critical Solutions Ltd
001E00	Shantou Institute of Ultrasonic Instruments
001E01	Renesas Technology Sales Co., Ltd.
001E02	Sougou Keikaku Kougyou Co.,Ltd.
001E03	LiComm Co., Ltd.
001E04	Hanson Research Corporation
001E05	Xseed Technologies & Computing
001E06	Wibrain
001E07	Winy Technology Co., Ltd.
001E08	Centec Networks Inc
001E09	ZEFATEK Co.,LTD
001E0A	Syba Tech Limited
001E0B	Hewlett Packard
001E0C	Sherwood Information Partners, Inc.
001E0D	Micran Ltd.
001E0E	MAXI VIEW HOLDINGS LIMITED
001E0F	Briot International
001E10	HUAWEI TECHNOLOGIES CO.,LTD
001E11	ELELUX INTERNATIONAL LTD
001E12	Ecolab
001E13	Cisco Systems, Inc
001E14	Cisco Systems, Inc
001E15	Beech Hill Electronics
001E16	Keytronix
001E17	STN BV
001E18	Radio Activity srl
001E19	Gtri
001E1A	Best Source Taiwan Inc.
001E1B	Digital Stream Technology, Inc.
001E1C	SWS Australia Pty Limited
001E1D	East Coast Datacom, Inc.
001E1E	Honeywell Life Safety
001E1F	Nortel Networks
001E20	Intertain Inc.
001E21	Qisda Corporation
001E22	ARVOO Imaging Products BV
001E23	Electronic Educational Devices, Inc
001E24	Zhejiang Bell Technology Co.,ltd
001E25	INTEK DIGITAL
001E26	Digifriends Co. Ltd
001E27	SBN TECH Co.,Ltd.
001E28	Lumexis Corporation
001E29	Hypertherm Inc
001E2A	Netgear
001E2B	Radio Systems Design, Inc.
001E2C	CyVerse Corporation
001E2D	Stim
001E2E	SIRTI S.p.A.
001E2F	DiMoto Pty Ltd
001E30	Shireen Inc
001E31	INFOMARK CO.,LTD.
001E32	Zensys
001E33	INVENTEC Corporation
001E34	CryptoMetrics
001E35	Nintendo Co., Ltd.
001E36	Ipte
001E37	Universal Global Scientific Industrial Co., Ltd.
001E38	Bluecard Software Technology Co., Ltd.
001E39	Comsys Communication Ltd.
001E3A	Nokia Danmark A/S
001E3B	Nokia Danmark A/S
001E3C	Lyngbox Media AB
001E3D	ALPS ELECTRIC CO.,LTD.
001E3E	KMW Inc.
001E3F	TrellisWare Technologies, Inc.
001E40	Shanghai DareGlobal Technologies Co.,Ltd
001E41	Microwave Communication & Component, Inc.
001E42	Teltonika
001E43	AISIN AW CO.,LTD.
001E44	Santec
001E45	Sony Mobile Communications AB
001E46	ARRIS Group, Inc.
001E47	PT. Hariff Daya Tunggal Engineering
001E48	Wi-Links
001E49	Cisco Systems, Inc
001E4A	Cisco Systems, Inc
001E4B	City Theatrical
001E4C	Hon Hai Precision Ind. Co.,Ltd.
001E4D	Welkin Sciences, LLC
001E4E	DakoEdv-               # DAKO EDV-Ingenieur- und Systemhaus GmbH
001E4F	Dell Inc.
001E50	BATTISTONI RESEARCH
001E51	Converter Industry Srl
001E52	Apple, Inc.
001E53	Further Tech Co., LTD
001E54	TOYO ELECTRIC Corporation
001E55	COWON SYSTEMS,Inc.
001E56	Bally Wulff Entertainment GmbH
001E57	ALCOMA, spol. s r.o.
001E58	D-Link Corporation
001E59	Silicon Turnkey Express, LLC
001E5A	ARRIS Group, Inc.
001E5B	Unitron Company, Inc.
001E5C	RB GeneralEkonomik
001E5D	Holosys d.o.o.
001E5E	COmputime Ltd.
001E5F	KwikByte, LLC
001E60	Digital Lighting Systems, Inc
001E61	ITEC GmbH
001E62	Siemon
001E63	Vibro-Meter SA
001E64	Intel Corporate
001E65	Intel Corporate
001E66	RESOL Elektronische Regelungen GmbH
001E67	Intel Corporate
001E68	QUANTA COMPUTER INC.
001E69	Thomson Inc.
001E6A	Beijing Bluexon Technology Co.,Ltd
001E6B	Cisco SPVTG
001E6C	Opaque Systems
001E6D	IT R&D Center
001E6E	Shenzhen First Mile Communications Ltd
001E6F	Magna-Power Electronics, Inc.
001E70	Cobham Defence Communications Ltd
001E71	MIrcom Group of Companies
001E72	Pcs
001E73	zte corporation
001E74	Sagemcom Broadband SAS
001E75	LG Electronics (Mobile Communications)
001E76	Thermo Fisher Scientific
001E77	Air2app
001E78	Owitek Technology Ltd.,
001E79	Cisco Systems, Inc
001E7A	Cisco Systems, Inc
001E7B	R.I.CO. S.r.l.
001E7C	Taiwick Limited
001E7D	Samsung Electronics Co.,Ltd
001E7E	Nortel Networks
001E7F	CBM of America
001E80	Last Mile Ltd.
001E81	CNB Technology Inc.
001E82	SanDisk Corporation
001E83	LAN/MAN Standards Association (LMSC)
001E84	Pika Technologies Inc.
001E85	Lagotek Corporation
001E86	MEL Co.,Ltd.
001E87	Realease Limited
001E88	ANDOR SYSTEM SUPPORT CO., LTD.
001E89	CRFS Limited
001E8A	eCopy, Inc
001E8B	Infra Access Korea Co., Ltd.
001E8C	ASUSTek COMPUTER INC.
001E8D	ARRIS Group, Inc.
001E8E	Hunkeler AG
001E8F	CANON INC.
001E90	Elitegroup Computer Systems Co.,Ltd.
001E91	KIMIN Electronic Co., Ltd.
001E92	JEULIN S.A.
001E93	CiriTech Systems Inc
001E94	SUPERCOM TECHNOLOGY CORPORATION
001E95	SIGMALINK
001E96	Sepura Plc
001E97	Medium Link System Technology CO., LTD,
001E98	GreenLine Communications
001E99	Vantanol Industrial Corporation
001E9A	HAMILTON Bonaduz AG
001E9B	San-Eisha, Ltd.
001E9C	Fidustron INC
001E9D	Recall Technologies, Inc.
001E9E	DdmHopt+               # ddm hopt + schuler Gmbh + Co. KG
001E9F	Visioneering Systems, Inc.
001EA0	Xln-T
001EA1	Brunata a/s
001EA2	Symx Systems, Inc.
001EA3	Nokia Danmark A/S
001EA4	Nokia Danmark A/S
001EA5	ROBOTOUS, Inc.
001EA6	Best IT World (India) Pvt. Ltd.
001EA7	Actiontec Electronics, Inc
001EA8	Datang Mobile Communications Equipment CO.,LTD
001EA9	Nintendo Co., Ltd.
001EAA	E-Senza Technologies GmbH
001EAB	TeleWell Oy
001EAC	Armadeus Systems
001EAD	Wingtech Group Limited
001EAE	Continental Automotive Systems Inc.
001EAF	Ophir Optronics Ltd
001EB0	ImesD Electronica S.L.
001EB1	Cryptsoft Pty Ltd
001EB2	LG innotek
001EB3	Primex Wireless
001EB4	UNIFAT TECHNOLOGY LTD.
001EB5	Ever Sparkle Technologies Ltd
001EB6	TAG Heuer SA
001EB7	TBTech, Co., Ltd.
001EB8	Fortis, Inc.
001EB9	Sing Fai Technology Limited
001EBA	High Density Devices AS
001EBB	BLUELIGHT TECHNOLOGY INC.
001EBC	WINTECH AUTOMATION CO.,LTD.
001EBD	Cisco Systems, Inc
001EBE	Cisco Systems, Inc
001EBF	Haas Automation Inc.
001EC0	Microchip Technology Inc.
001EC1	3COM EUROPE LTD
001EC2	Apple, Inc.
001EC3	Kozio, Inc.
001EC4	Celio Corp
001EC5	Middle Atlantic Products Inc
001EC6	Obvius Holdings LLC
001EC7	2Wire Inc
001EC8	Rapid Mobile (Pty) Ltd
001EC9	Dell Inc.
001ECA	Nortel Networks
001ECB	RPC Energoautomatika Ltd
001ECC	Cdvi
001ECD	KYLAND Technology Co. LTD
001ECE	BISA Technologies (Hong Kong) Limited
001ECF	PHILIPS ELECTRONICS UK LTD
001ED0	Ingespace
001ED1	Keyprocessor B.V.
001ED2	Ray Shine Video Technology Inc
001ED3	Dot Technology Int'l Co., Ltd.
001ED4	Doble Engineering
001ED5	Tekon-Automatics
001ED6	Alentec & Orion AB
001ED7	H-Stream Wireless, Inc.
001ED8	Digital United Inc.
001ED9	Mitsubishi Precision Co.,LTd.
001EDA	Wesemann Elektrotechniek B.V.
001EDB	Giken Trastem Co., Ltd.
001EDC	Sony Mobile Communications AB
001EDD	WASKO S.A.
001EDE	BYD COMPANY LIMITED
001EDF	Master Industrialization Center Kista
001EE0	Urmet Domus SpA
001EE1	Samsung Electronics Co.,Ltd
001EE2	Samsung Electronics Co.,Ltd
001EE3	T&W Electronics (ShenZhen) Co.,Ltd
001EE4	ACS Solutions France
001EE5	Cisco-Linksys, LLC
001EE6	Shenzhen Advanced Video Info-Tech Co., Ltd.
001EE7	Epic Systems Inc
001EE8	Mytek
001EE9	Stoneridge Electronics AB
001EEA	Sensor Switch, Inc.
001EEB	Talk-A-Phone Co.
001EEC	COMPAL INFORMATION (KUNSHAN) CO., LTD.
001EED	Adventiq Ltd.
001EEE	ETL Systems Ltd
001EEF	Cantronic International Limited
001EF0	Gigafin Networks
001EF1	Servimat
001EF2	Micro Motion Inc
001EF3	From2
001EF4	L-3 Communications Display Systems
001EF5	Hitek Automated Inc.
001EF6	Cisco Systems, Inc
001EF7	Cisco Systems, Inc
001EF8	Emfinity Inc.
001EF9	Pascom Kommunikations systeme GmbH.
001EFA	PROTEI Ltd.
001EFB	Trio Motion Technology Ltd
001EFC	JSC MASSA-K
001EFD	Microbit 2.0 AB
001EFE	LEVEL s.r.o.
001EFF	Mueller-               # Mueller-Elektronik GmbH & Co. KG
001F00	Nokia Danmark A/S
001F01	Nokia Danmark A/S
001F02	Pixelmetrix Corporation Pte Ltd
001F03	NUM AG
001F04	Granch Ltd.
001F05	iTAS Technology Corp.
001F06	Integrated Dispatch Solutions
001F07	AZTEQ Mobile
001F08	RISCO LTD
001F09	Jastec
001F0A	Nortel Networks
001F0B	Federal State Unitary Enterprise Industrial UnionElectropribor
001F0C	Intelligent Digital Services GmbH
001F0D	L3 Communications - Telemetry West
001F0E	Japan Kyastem Co., Ltd
001F0F	Select Engineered Systems
001F10	TOLEDO DO BRASIL INDUSTRIA DE BALANCAS  LTDA
001F11	OPENMOKO, INC.
001F12	Juniper Networks
001F13	S.& A.S. Ltd.
001F14	Nexg
001F15	Bioscrypt Inc
001F16	Wistron Corporation
001F17	IDX Company, Ltd.
001F18	Hakusan.Mfg.Co,.Ltd
001F19	BEN-RI ELECTRONICA S.A.
001F1A	Prominvest
001F1B	RoyalTek Company Ltd.
001F1C	KOBISHI ELECTRIC Co.,Ltd.
001F1D	Atlas Material Testing Technology LLC
001F1E	Astec Technology Co., Ltd
001F1F	Edimax Technology Co. Ltd.
001F20	Logitech Europe SA
001F21	Inner Mongolia Yin An Science & Technology Development Co.,L
001F22	Source Photonics, Inc.
001F23	Interacoustics
001F24	DIGITVIEW TECHNOLOGY CO., LTD.
001F25	MBS GmbH
001F26	Cisco Systems, Inc
001F27	Cisco Systems, Inc
001F28	HPN Supply Chain
001F29	Hewlett Packard
001F2A	Accm
001F2B	Orange Logic
001F2C	Starbridge Networks
001F2D	Electro-               # Electro-Optical Imaging, Inc.
001F2E	Triangle Research Int'l Pte Ltd
001F2F	Berker GmbH & Co. KG
001F30	Travelping
001F31	Radiocomp
001F32	Nintendo Co., Ltd.
001F33	Netgear
001F34	Lung Hwa Electronics Co., Ltd.
001F35	AIR802 LLC
001F36	Bellwin Information Co. Ltd.,
001F37	Genesis I&C
001F38	Positron
001F39	Construcciones y Auxiliar de Ferrocarriles, S.A.
001F3A	Hon Hai Precision Ind. Co.,Ltd.
001F3B	Intel Corporate
001F3C	Intel Corporate
001F3D	Qbit GmbH
001F3E	RP-Technik e.K.
001F3F	AVM GmbH
001F40	Speakercraft Inc.
001F41	Ruckus Wireless
001F42	Etherstack plc
001F43	ENTES ELEKTRONIK
001F44	GE Transportation Systems
001F45	Enterasys
001F46	Nortel Networks
001F47	MCS Logic Inc.
001F48	Mojix Inc.
001F49	Manhattan TV Ltd
001F4A	Albentia Systems S.A.
001F4B	Lineage Power
001F4C	Roseman Engineering Ltd
001F4D	Segnetics LLC
001F4E	ConMed Linvatec
001F4F	Thinkware Co. Ltd.
001F50	Swissdis AG
001F51	HD Communications Corp
001F52	UVT Unternehmensberatung fur Verkehr und Technik GmbH
001F53	GEMAC Gesellschaft für Mikroelektronikanwendung Chemnitz mbH
001F54	Lorex Technology Inc.
001F55	Honeywell Security (China) Co., Ltd.
001F56	DIGITAL FORECAST
001F57	Phonik Innovation Co.,LTD
001F58	EMH Energiemesstechnik GmbH
001F59	Kronback Tracers
001F5A	Beckwith Electric Co.
001F5B	Apple, Inc.
001F5C	Nokia Danmark A/S
001F5D	Nokia Danmark A/S
001F5E	Dyna Technology Co.,Ltd.
001F5F	Blatand GmbH
001F60	COMPASS SYSTEMS CORP.
001F61	Talent Communication Networks Inc.
001F62	JSC Stilsoft
001F63	JSC Goodwin-Europa
001F64	Beijing Autelan Technology Inc.
001F65	KOREA ELECTRIC TERMINAL CO., LTD.
001F66	PLANAR LLC
001F67	Hitachi,Ltd.
001F68	Martinsson Elektronik AB
001F69	Pingood Technology Co., Ltd.
001F6A	PacketFlux Technologies, Inc.
001F6B	LG Electronics (Mobile Communications)
001F6C	Cisco Systems, Inc
001F6D	Cisco Systems, Inc
001F6E	Vtech Engineering Corporation
001F6F	Fujian Sunnada Communication Co.,Ltd.
001F70	Botik Technologies LTD
001F71	xG Technology, Inc.
001F72	QingDao Hiphone Technology Co,.Ltd
001F73	Teraview Technology Co., Ltd.
001F74	Eigen Development
001F75	GiBahn Media
001F76	AirLogic Systems Inc.
001F77	HEOL DESIGN
001F78	Blue Fox Porini Textile
001F79	Lodam Electronics A/S
001F7A	WiWide Inc.
001F7B	TechNexion Ltd.
001F7C	Witelcom AS
001F7D	embedded wireless GmbH
001F7E	ARRIS Group, Inc.
001F7F	Phabrix Limited
001F80	Lucas Holding bv
001F81	Accel Semiconductor Corp
001F82	Cal-Comp Electronics & Communications Company Ltd.
001F83	Teleplan Technology Services Sdn Bhd
001F84	Gigle Semiconductor
001F85	Apriva ISS, LLC
001F86	Digecor
001F87	Skydigital Inc.
001F88	FMS Force Measuring Systems AG
001F89	Signalion GmbH
001F8A	Ellion Digital Inc.
001F8B	Cache IQ
001F8C	CCS Inc.
001F8D	Ingenieurbuero Stark GmbH und Ko. KG
001F8E	Metris USA Inc.
001F8F	Shanghai Bellmann Digital Source Co.,Ltd.
001F90	Actiontec Electronics, Inc
001F91	DBS Lodging Technologies, LLC
001F92	VideoIQ, Inc.
001F93	Xiotech Corporation
001F94	Lascar Electronics Ltd
001F95	Sagemcom Broadband SAS
001F96	APROTECH CO.LTD
001F97	BERTANA srl
001F98	Daiichi-               # DAIICHI-DENTSU LTD.
001F99	SERONICS co.ltd
001F9A	Nortel Networks
001F9B	Posbro
001F9C	Ledco
001F9D	Cisco Systems, Inc
001F9E	Cisco Systems, Inc
001F9F	Thomson Telecom Belgium
001FA0	A10 Networks
001FA1	Gtran Inc
001FA2	Datron World Communications, Inc.
001FA3	T&W Electronics(Shenzhen)Co.,Ltd.
001FA4	SHENZHEN GONGJIN ELECTRONICS CO.,LT
001FA5	Blue-White Industries
001FA6	Stilo srl
001FA7	Sony Interactive Entertainment Inc.
001FA8	Smart Energy Instruments Inc.
001FA9	Atlanta DTH, Inc.
001FAA	Taseon, Inc.
001FAB	I.S HIGH TECH.INC
001FAC	Goodmill Systems Ltd
001FAD	Brown Innovations, Inc
001FAE	Blick South Africa (Pty) Ltd
001FAF	NextIO, Inc.
001FB0	TimeIPS, Inc.
001FB1	Cybertech Inc.
001FB2	Sontheim Industrie Elektronik GmbH
001FB3	2Wire Inc
001FB4	SmartShare Systems
001FB5	I/O Interconnect Inc.
001FB6	Chi Lin Technology Co., Ltd.
001FB7	WiMate Technologies Corp.
001FB8	Universal Remote Control, Inc.
001FB9	Paltronics
001FBA	Boyoung Tech
001FBB	Xenatech Co.,LTD
001FBC	EVGA Corporation
001FBD	Kyocera Wireless Corp.
001FBE	Shenzhen Mopnet Industrial Co.,Ltd
001FBF	Fulhua Microelectronics Corp. Taiwan Branch
001FC0	Control Express Finland Oy
001FC1	Hanlong Technology Co.,LTD
001FC2	Jow Tong Technology Co Ltd
001FC3	SmartSynch, Inc
001FC4	ARRIS Group, Inc.
001FC5	Nintendo Co., Ltd.
001FC6	ASUSTek COMPUTER INC.
001FC7	Casio Hitachi Mobile Communications Co., Ltd.
001FC8	Up-Today Industrial Co., Ltd.
001FC9	Cisco Systems, Inc
001FCA	Cisco Systems, Inc
001FCB	NIW Solutions
001FCC	Samsung Electronics Co.,Ltd
001FCD	Samsung Electronics Co.,Ltd
001FCE	QTECH LLC
001FCF	MSI Technology GmbH
001FD0	GIGA-BYTE TECHNOLOGY CO.,LTD.
001FD1	OPTEX CO.,LTD.
001FD2	COMMTECH TECHNOLOGY MACAO COMMERCIAL OFFSHORE LTD.
001FD3	RIVA Networks Inc.
001FD4	4IPNET, INC.
001FD5	MICRORISC s.r.o.
001FD6	Shenzhen Allywll
001FD7	TELERAD SA
001FD8	A-TRUST COMPUTER CORPORATION
001FD9	RSD Communications Ltd
001FDA	Nortel Networks
001FDB	Network Supply Corp.,
001FDC	Mobile Safe Track Ltd
001FDD	GDI LLC
001FDE	Nokia Danmark A/S
001FDF	Nokia Danmark A/S
001FE0	EdgeVelocity Corp
001FE1	Hon Hai Precision Ind. Co.,Ltd.
001FE2	Hon Hai Precision Ind. Co.,Ltd.
001FE3	LG Electronics (Mobile Communications)
001FE4	Sony Mobile Communications AB
001FE5	In-Circuit GmbH
001FE6	Alphion Corporation
001FE7	Simet
001FE8	KURUSUGAWA Electronics Industry Inc,.
001FE9	Printrex, Inc.
001FEA	Applied Media Technologies Corporation
001FEB	Trio Datacom Pty Ltd
001FEC	Synapse Électronique
001FED	Tecan Systems Inc.
001FEE	ubisys technologies GmbH
001FEF	SHINSEI INDUSTRIES CO.,LTD
001FF0	Audio Partnership
001FF1	Paradox Hellas S.A.
001FF2	VIA Technologies, Inc.
001FF3	Apple, Inc.
001FF4	Power Monitors, Inc.
001FF5	Kongsberg Defence & Aerospace
001FF6	PS Audio International
001FF7	Nakajima All Precision Co., Ltd.
001FF8	Siemens AG, Sector Industry, Drive Technologies, Motion Control Systems
001FF9	Advanced Knowledge Associates
001FFA	Coretree, Co, Ltd
001FFB	Green Packet Bhd
001FFC	Riccius+               # Riccius+Sohn GmbH
001FFD	Indigo Mobile Technologies Corp.
001FFE	HPN Supply Chain
001FFF	Respironics, Inc.
002000	Lexmark (Print Server)
002001	DSP SOLUTIONS, INC.
002002	SERITECH ENTERPRISE CO., LTD.
002003	PIXEL POWER LTD.
002004	YAMATAKE-HONEYWELL CO., LTD.
002005	simpletech
002006	GARRETT COMMUNICATIONS, INC.
002007	SFA, INC.
002008	Cable & Computer Technology
002009	PACKARD BELL ELEC., INC.
00200A	SOURCE-COMM CORP.
00200B	OCTAGON SYSTEMS CORP.
00200C	Adastra Systems Corp
00200D	CARL ZEISS
00200E	SATELLITE TECHNOLOGY MGMT, INC
00200F	EBRAINS Inc
002010	JEOL SYSTEM TECHNOLOGY CO. LTD
002011	Canopus Co Ltd
002012	CAMTRONICS MEDICAL SYSTEMS
002013	DIVERSIFIED TECHNOLOGY, INC.
002014	GLOBAL VIEW CO., LTD.
002015	ACTIS COMPUTER SA
002016	SHOWA ELECTRIC WIRE & CABLE CO
002017	Orbotech
002018	Realtek
002019	OHLER GMBH
00201A	Nbase
00201B	NORTHERN TELECOM/NETWORK
00201C	EXCEL, INC.
00201D	KATANA PRODUCTS
00201E	NETQUEST CORPORATION
00201F	BEST POWER TECHNOLOGY, INC.
002020	MEGATRON COMPUTER INDUSTRIES PTY, LTD.
002021	ALGORITHMS SOFTWARE PVT. LTD.
002022	NMS Communications
002023	T.C. TECHNOLOGIES PTY. LTD
002024	PACIFIC COMMUNICATION SCIENCES
002025	Control Technology Inc (Industrial Controls and Network Interfaces)
002026	AMKLY SYSTEMS, INC.
002027	MING FORTUNE INDUSTRY CO., LTD
002028	Bloomberg
002029	TeleProcessing CSU/DSU (now owned by ADC/Kentrox)
00202A	N.V. DZINE
00202B	ATML (Advanced Telecommunications Modules, Ltd.)
00202C	WELLTRONIX CO., LTD.
00202D	TAIYO CORPORATION
00202E	DAYSTAR DIGITAL
00202F	ZETA COMMUNICATIONS, LTD.
002030	ANALOG & DIGITAL SYSTEMS
002031	Tattile SRL
002032	ALCATEL TAISEL
002033	SYNAPSE TECHNOLOGIES, INC.
002034	ROTEC INDUSTRIEAUTOMATION GMBH
002035	IBM (International Business Machines)	mainframes, Etherjet printers
002036	BMC Software
002037	SEAGATE TECHNOLOGY
002038	VME MICROSYSTEMS INTERNATIONAL CORPORATION
002039	Scinets
00203A	DIGITAL BI0METRICS INC.
00203B	WISDM LTD.
00203C	EUROTIME AB
00203D	Honeywell ECC
00203E	LogiCan Technologies, Inc.
00203F	JUKI CORPORATION
002040	ARRIS Group, Inc.
002041	DATA NET
002042	Datametrics Corp
002043	NEURON COMPANY LIMITED
002044	GENITECH PTY LTD
002045	SolCom Systems Limited
002046	CIPRICO, INC.
002047	STEINBRECHER CORP.
002048	Fore Systems Inc
002049	COMTRON, INC.
00204A	PRONET GMBH
00204B	Autocomputer Co Ltd
00204C	Mitron Computer Pte Ltd
00204D	INOVIS GMBH
00204E	NETWORK SECURITY SYSTEMS, INC.
00204F	DEUTSCHE AEROSPACE AG
002050	KOREA COMPUTER INC.
002051	Verilink Corporation
002052	RAGULA SYSTEMS
002053	HUNTSVILLE MICROSYSTEMS, INC.
002054	Sycamore Networks
002055	ALTECH CO., LTD.
002056	Neoproducts
002057	TITZE DATENTECHNIK GmbH
002058	ALLIED SIGNAL INC.
002059	MIRO COMPUTER PRODUCTS AG
00205A	COMPUTER IDENTICS
00205B	Kentrox, LLC
00205C	InterNet Systems of Florida, Inc.
00205D	NANOMATIC OY
00205E	CASTLE ROCK, INC.
00205F	GAMMADATA COMPUTER GMBH
002060	ALCATEL ITALIA S.p.A.
002061	Dynatech Communications Inc
002062	SCORPION LOGIC, LTD.
002063	Wipro Infotech Ltd
002064	PROTEC MICROSYSTEMS, INC.
002065	SUPERNET NETWORKING INC.
002066	General Magic Inc
002067	Node Runner Inc
002068	Isdyne
002069	ISDN SYSTEMS CORPORATION
00206A	OSAKA COMPUTER CORP.
00206B	Minolta Co., Ltd		Network printers
00206C	EVERGREEN TECHNOLOGY CORP.
00206D	DATA RACE, INC.
00206E	XACT, INC.
00206F	FLOWPOINT CORPORATION
002070	HYNET, LTD.
002071	IBR GMBH
002072	WORKLINK INNOVATIONS
002073	FUSION SYSTEMS CORPORATION
002074	SUNGWOON SYSTEMS
002075	MOTOROLA COMMUNICATION ISRAEL
002076	REUDO CORPORATION
002077	KARDIOS SYSTEMS CORP.
002078	Runtop Inc
002079	MIKRON GMBH
00207A	WiSE Communications, Inc.
00207B	Intel Corporation
00207C	AUTEC GMBH
00207D	ADVANCED COMPUTER APPLICATIONS
00207E	FINECOM CO., LTD.
00207F	KYOEI SANGYO CO., LTD.
002080	SYNERGY (UK) LTD.
002081	TITAN ELECTRONICS
002082	ONEAC CORPORATION
002083	PRESTICOM INCORPORATED
002084	OCE PRINTING SYSTEMS, GMBH
002085	3Com
002086	MICROTECH ELECTRONICS LIMITED
002087	MEMOTEC, INC.
002088	GLOBAL VILLAGE COMMUNICATION
002089	T3PLUS NETWORKING, INC.
00208A	Sonix Communications Ltd
00208B	Focus Enhancements
00208C	Galaxy Networks Inc
00208D	CMD TECHNOLOGY
00208E	CHEVIN SOFTWARE ENG. LTD.
00208F	ECI Telecom Ltd.
002090	ADVANCED COMPRESSION TECHNOLOGY, INC.
002091	J125, NATIONAL SECURITY AGENCY
002092	CHESS ENGINEERING B.V.
002093	LANDINGS TECHNOLOGY CORP.
002094	Cubix Corporation
002095	RIVA ELECTRONICS
002096	Invensys
002097	APPLIED SIGNAL TECHNOLOGY
002098	HECTRONIC AB
002099	BON ELECTRIC CO., LTD.
00209A	THE 3DO COMPANY
00209B	ERSAT ELECTRONIC GMBH
00209C	PRIMARY ACCESS CORP.
00209D	LIPPERT AUTOMATIONSTECHNIK
00209E	BROWN'S OPERATING SYSTEM SERVICES, LTD.
00209F	MERCURY COMPUTER SYSTEMS, INC.
0020A0	OA LABORATORY CO., LTD.
0020A1	Dovatron
0020A2	GALCOM NETWORKING LTD.
0020A3	Harmonic, Inc
0020A4	MULTIPOINT NETWORKS
0020A5	Newer Technology
0020A6	Proxim Inc
0020A7	Pairgain Technologies, Inc.
0020A8	SAST TECHNOLOGY CORP.
0020A9	WHITE HORSE INDUSTRIAL
0020AA	Ericsson Television Limited
0020AB	MICRO INDUSTRIES CORP.
0020AC	INTERFLEX DATENSYSTEME GMBH
0020AD	LINQ SYSTEMS
0020AE	ORNET DATA COMMUNICATION TECH.
0020AF	3COM Corporation
0020B0	GATEWAY DEVICES, INC.
0020B1	COMTECH RESEARCH INC.
0020B2	CSP (Printline Multiconnectivity converter)
0020B3	Tattile SRL
0020B4	TERMA ELEKTRONIK AS
0020B5	YASKAWA ELECTRIC CORPORATION
0020B6	Agile Networks Inc
0020B7	NAMAQUA COMPUTERWARE
0020B8	PRIME OPTION, INC.
0020B9	Metricom, Inc.
0020BA	CENTER FOR HIGH PERFORMANCE
0020BB	ZAX CORPORATION
0020BC	Long Reach Networks Pty Ltd
0020BD	NIOBRARA R & D CORPORATION
0020BE	LAN ACCESS CORP.
0020BF	AEHR TEST SYSTEMS
0020C0	PULSE ELECTRONICS, INC.
0020C1	SAXA, Inc.
0020C2	TEXAS MEMORY SYSTEMS, INC.
0020C3	COUNTER SOLUTIONS LTD.
0020C4	INET,INC.
0020C5	Eagle NE2000
0020C6	Nectec
0020C7	AKAI Professional M.I. Corp.
0020C8	LARSCOM INCORPORATED
0020C9	VICTRON BV
0020CA	DIGITAL OCEAN
0020CB	PRETEC ELECTRONICS CORP.
0020CC	DIGITAL SERVICES, LTD.
0020CD	HYBRID NETWORKS, INC.
0020CE	LOGICAL DESIGN GROUP, INC.
0020CF	TEST & MEASUREMENT SYSTEMS INC
0020D0	Versalynx Corp.			"The One Port" terminal server
0020D1	MICROCOMPUTER SYSTEMS (M) SDN.
0020D2	RAD Data Communications Ltd
0020D3	OST (Ouet Standard Telematique)
0020D4	Cabletron Systems, Inc.
0020D5	VIPA GMBH
0020D6	Breezecom, Ltd.
0020D7	JAPAN MINICOMPUTER SYSTEMS CO., Ltd.
0020D8	Netwave
0020D9	PANASONIC TECHNOLOGIES, INC./MIECO-US
0020DA	Xylan
0020DB	XNET TECHNOLOGY, INC.
0020DC	Densitron Taiwan Ltd
0020DD	Cybertec Pty Ltd
0020DE	JAPAN DIGITAL LABORAT'Y CO.LTD
0020DF	KYOSAN ELECTRIC MFG. CO., LTD.
0020E0	PreMax PE-200 (PCMCIA NE2000-clone card, sold by InfoExpress)
0020E1	ALAMAR ELECTRONICS
0020E2	INFORMATION RESOURCE ENGINEERING
0020E3	MCD KENCOM CORPORATION
0020E4	HSING TECH ENTERPRISE CO., LTD
0020E5	Apex Data
0020E6	LIDKOPING MACHINE TOOLS AB
0020E7	B&W NUCLEAR SERVICE COMPANY
0020E8	DATATREK CORPORATION
0020E9	Dantel
0020EA	EFFICIENT NETWORKS, INC.
0020EB	CINCINNATI MICROWAVE, INC.
0020EC	TECHWARE SYSTEMS CORP.
0020ED	GIGA-BYTE TECHNOLOGY CO., LTD.
0020EE	Gtech Corporation
0020EF	USC CORPORATION
0020F0	UNIVERSAL MICROELECTRONICS CO.
0020F1	ALTOS INDIA LIMITED
0020F2	Oracle Corporation
0020F3	RAYNET CORPORATION
0020F4	SPECTRIX CORPORATION
0020F5	PANDATEL AG
0020F6	Net Tek & Karlnet Inc
0020F7	CYBERDATA CORPORATION
0020F8	Carrera Computers Inc
0020F9	PARALINK NETWORKS, INC.
0020FA	GDE SYSTEMS, INC.
0020FB	OCTEL COMMUNICATIONS CORP.
0020FC	Matrox
0020FD	ITV TECHNOLOGIES, INC.
0020FE	Topware/               # TOPWARE INC. / GRAND COMPUTER
0020FF	SYMMETRICAL TECHNOLOGIES
002100	Gemtek Technology Co., Ltd.
002101	Aplicaciones Electronicas Quasar (AEQ)
002102	UpdateLogic Inc.
002103	GHI Electronics, LLC
002104	Gigaset Communications GmbH
002105	Alcatel-               # Alcatel-Lucent IPD
002106	RIM Testing Services
002107	Seowonintech Co Ltd.
002108	Nokia Danmark A/S
002109	Nokia Danmark A/S
00210A	bydsign Corporation
00210B	GEMINI TRAZE RFID PVT. LTD.
00210C	Cymtec Systems, Inc.
00210D	SAMSIN INNOTEC
00210E	Orpak Systems L.T.D.
00210F	Cernium Corp
002110	Clearbox Systems
002111	Uniphone Inc.
002112	WISCOM SYSTEM CO.,LTD
002113	Padtec S/A
002114	Hylab Technology Inc.
002115	PHYWE Systeme GmbH & Co. KG
002116	Transcon Electronic Systems, spol. s r. o.
002117	Tellord
002118	Athena Tech, Inc.
002119	SAMSUNG ELECTRO MECHANICS CO., LTD.
00211A	LInTech Corporation
00211B	Cisco Systems, Inc
00211C	Cisco Systems, Inc
00211D	Dataline AB
00211E	ARRIS Group, Inc.
00211F	SHINSUNG DELTATECH CO.,LTD.
002120	Sequel Technologies
002121	VRmagic GmbH
002122	Chip-pro Ltd.
002123	Aerosat Avionics
002124	Optos Plc
002125	KUK JE TONG SHIN Co.,LTD
002126	Shenzhen Torch Equipment Co., Ltd.
002127	TP-LINK TECHNOLOGIES CO.,LTD.
002128	Oracle Corporation
002129	Cisco-Linksys, LLC
00212A	Audiovox Corporation
00212B	MSA Auer
00212C	SemIndia System Private Limited
00212D	SCIMOLEX CORPORATION
00212E	Dresden-               # dresden-elektronik
00212F	Phoebe Micro Inc.
002130	Keico Hightech Inc.
002131	Blynke Inc.
002132	Masterclock, Inc.
002133	Building B, Inc
002134	Brandywine Communications
002135	Alcatel-               # ALCATEL-LUCENT
002136	ARRIS Group, Inc.
002137	Bay Controls, LLC
002138	Cepheid
002139	Escherlogic Inc.
00213A	Winchester Systems Inc.
00213B	Berkshire Products, Inc
00213C	Aliphcom
00213D	Cermetek Microelectronics, Inc.
00213E	Tomtom
00213F	A-Team Technology Ltd.
002140	EN Technologies Inc.
002141	Radlive
002142	Advanced Control Systems doo
002143	ARRIS Group, Inc.
002144	SS Telecoms
002145	Semptian Technologies Ltd.
002146	Sanmina-               # Sanmina-SCI
002147	Nintendo Co., Ltd.
002148	Kaco Solar Korea
002149	China Daheng Group ,Inc.
00214A	Pixel Velocity, Inc
00214B	Shenzhen HAMP Science & Technology Co.,Ltd
00214C	Samsung Electronics Co.,Ltd
00214D	Guangzhou Skytone Transmission Technology Com. Ltd.
00214E	GS Yuasa Power Supply Ltd.
00214F	ALPS ELECTRIC CO.,LTD.
002150	EYEVIEW ELECTRONICS
002151	Millinet Co., Ltd.
002152	General Satellite Research & Development Limited
002153	SeaMicro Inc.
002154	D-TACQ Solutions Ltd
002155	Cisco Systems, Inc
002156	Cisco Systems, Inc
002157	National Datacast, Inc.
002158	Style Flying Technology Co.
002159	Juniper Networks
00215A	Hewlett Packard
00215B	SenseAnywhere
00215C	Intel Corporate
00215D	Intel Corporate
00215E	IBM Corp
00215F	IHSE GmbH
002160	Hidea Solutions Co. Ltd.
002161	Yournet Inc.
002162	Nortel Networks
002163	ASKEY COMPUTER CORP
002164	Special Design Bureau for Seismic Instrumentation
002165	Presstek Inc.
002166	NovAtel Inc.
002167	HwaJinT&               # HWA JIN T&I Corp.
002168	iVeia, LLC
002169	Prologix, LLC.
00216A	Intel Corporate
00216B	Intel Corporate
00216C	Odva
00216D	Soltech Co., Ltd.
00216E	Function ATI (Huizhou) Telecommunications Co., Ltd.
00216F	SymCom, Inc.
002170	Dell Inc.
002171	Wesung TNC Co., Ltd.
002172	Seoultek Valley
002173	Ion Torrent Systems, Inc.
002174	AvaLAN Wireless
002175	Pacific Satellite International Ltd.
002176	YMax Telecom Ltd.
002177	W. L. Gore & Associates
002178	Matuschek Messtechnik GmbH
002179	IOGEAR, Inc.
00217A	Sejin Electron, Inc.
00217B	Bastec AB
00217C	2Wire Inc
00217D	PYXIS S.R.L.
00217E	Telit Communication s.p.a
00217F	Intraco Technology Pte Ltd
002180	ARRIS Group, Inc.
002181	Si2 Microsystems Limited
002182	SandLinks Systems, Ltd.
002183	ANDRITZ HYDRO GmbH
002184	POWERSOFT SRL
002185	MICRO-STAR INT'L CO.,LTD.
002186	Universal Global Scientific Industrial Co., Ltd.
002187	Imacs GmbH
002188	EMC Corporation
002189	AppTech, Inc.
00218A	Electronic Design and Manufacturing Company
00218B	Wescon Technology, Inc.
00218C	TopControl GMBH
00218D	AP Router Ind. Eletronica LTDA
00218E	MEKICS CO., LTD.
00218F	Avantgarde Acoustic Lautsprechersysteme GmbH
002190	Goliath Solutions
002191	D-Link Corporation
002192	Baoding Galaxy Electronic Technology  Co.,Ltd
002193	Videofon MV
002194	Ping Communication
002195	GWD Media Limited
002196	Telsey  S.p.A.
002197	Elitegroup Computer Systems Co.,Ltd.
002198	Thai Radio Co, LTD
002199	Vacon Plc
00219A	Cambridge Visual Networks Ltd
00219B	Dell Inc.
00219C	Honeywld Technology Corp.
00219D	Adesys BV
00219E	Sony Mobile Communications AB
00219F	SATEL OY
0021A0	Cisco Systems, Inc
0021A1	Cisco Systems, Inc
0021A2	EKE-Electronics Ltd.
0021A3	Micromint
0021A4	Dbii Networks
0021A5	ERLPhase Power Technologies Ltd.
0021A6	Videotec Spa
0021A7	Hantle System Co., Ltd.
0021A8	Telephonics Corporation
0021A9	Mobilink Telecom Co.,Ltd
0021AA	Nokia Danmark A/S
0021AB	Nokia Danmark A/S
0021AC	Infrared Integrated Systems Ltd
0021AD	Nordic ID Oy
0021AE	Alcatel-               # ALCATEL-LUCENT FRANCE - WTD
0021AF	Radio Frequency Systems
0021B0	Tyco Telecommunications
0021B1	DIGITAL SOLUTIONS LTD
0021B2	Fiberblaze A/S
0021B3	Ross Controls
0021B4	APRO MEDIA CO., LTD
0021B5	Galvanic Ltd
0021B6	Triacta Power Technologies Inc.
0021B7	Lexmark International Inc.
0021B8	Inphi Corporation
0021B9	Universal Devices Inc.
0021BA	Texas Instruments
0021BB	Riken Keiki Co., Ltd.
0021BC	ZALA COMPUTER
0021BD	Nintendo Co., Ltd.
0021BE	Cisco SPVTG
0021BF	Hitachi High-Tech Control Systems Corporation
0021C0	Mobile Appliance, Inc.
0021C1	ABB Oy / Medium Voltage Products
0021C2	GL Communications Inc
0021C3	CORNELL Communications, Inc.
0021C4	Consilium AB
0021C5	3DSP Corp
0021C6	CSJ Global, Inc.
0021C7	Russound
0021C8	LOHUIS Networks
0021C9	Wavecom Asia Pacific Limited
0021CA	ART System Co., Ltd.
0021CB	SMS TECNOLOGIA ELETRONICA LTDA
0021CC	Flextronics International
0021CD	Livetv
0021CE	NTC-Metrotek
0021CF	The Crypto Group
0021D0	Global Display Solutions Spa
0021D1	Samsung Electronics Co.,Ltd
0021D2	Samsung Electronics Co.,Ltd
0021D3	BOCOM SECURITY(ASIA PACIFIC) LIMITED
0021D4	Vollmer Werke GmbH
0021D5	X2E GmbH
0021D6	LXI Consortium
0021D7	Cisco Systems, Inc
0021D8	Cisco Systems, Inc
0021D9	SEKONIC CORPORATION
0021DA	Automation Products Group Inc.
0021DB	Santachi Video Technology (Shenzhen) Co., Ltd.
0021DC	TECNOALARM S.r.l.
0021DD	Northstar Systems Corp
0021DE	Firepro Wireless
0021DF	Martin Christ GmbH
0021E0	CommAgility Ltd
0021E1	Nortel Networks
0021E2	visago Systems & Controls GmbH & Co. KG
0021E3	SerialTek LLC
0021E4	I-Win
0021E5	Display Solution AG
0021E6	Starlight Video Limited
0021E7	Informatics Services Corporation
0021E8	Murata Manufacturing Co., Ltd.
0021E9	Apple, Inc.
0021EA	Bystronic Laser AG
0021EB	ESP SYSTEMS, LLC
0021EC	Solutronic GmbH
0021ED	Telegesis
0021EE	Full Spectrum Inc.
0021EF	Kapsys
0021F0	EW3 Technologies LLC
0021F1	Tutus Data AB
0021F2	EASY3CALL Technology Limited
0021F3	Si14 SpA
0021F4	INRange Systems, Inc
0021F5	Western Engravers Supply, Inc.
0021F6	Oracle Corporation
0021F7	HPN Supply Chain
0021F8	Enseo, Inc.
0021F9	WIRECOM Technologies
0021FA	A4SP Technologies Ltd.
0021FB	LG Electronics (Mobile Communications)
0021FC	Nokia Danmark A/S
0021FD	LACROIX TRAFFIC S.A.U
0021FE	Nokia Danmark A/S
0021FF	Cyfrowy Polsat SA
002200	IBM Corp
002201	Aksys Networks Inc
002202	Excito Elektronik i Skåne AB
002203	Glensound Electronics Ltd
002204	Koratek
002205	WeLink Solutions, Inc.
002206	Cyberdyne Inc.
002207	Inteno Broadband Technology AB
002208	Certicom Corp
002209	Omron Healthcare Co., Ltd
00220A	OnLive, Inc
00220B	National Source Coding Center
00220C	Cisco Systems, Inc
00220D	Cisco Systems, Inc
00220E	Indigo Security Co., Ltd.
00220F	MoCA (Multimedia over Coax Alliance)
002210	ARRIS Group, Inc.
002211	Rohati Systems
002212	CAI Networks, Inc.
002213	PCI CORPORATION
002214	RINNAI KOREA
002215	ASUSTek COMPUTER INC.
002216	SHIBAURA VENDING MACHINE CORPORATION
002217	Neat Electronics
002218	Verivue Inc.
002219	Dell Inc.
00221A	Audio Precision
00221B	Morega Systems
00221C	Private
00221D	Freegene Technology LTD
00221E	Media Devices Co., Ltd.
00221F	eSang Technologies Co., Ltd.
002220	Mitac Technology Corp
002221	ITOH DENKI CO,LTD.
002222	Schaffner Deutschland GmbH
002223	TimeKeeping Systems, Inc.
002224	Good Will Instrument Co., Ltd.
002225	Thales Avionics Ltd
002226	Avaak, Inc.
002227	uv-electronic GmbH
002228	Breeze Innovations Ltd.
002229	Compumedics Ltd
00222A	SoundEar A/S
00222B	Nucomm, Inc.
00222C	Ceton Corp
00222D	SMC Networks Inc.
00222E	maintech GmbH
00222F	Open Grid Computing, Inc.
002230	FutureLogic Inc.
002231	SMT&C Co., Ltd.
002232	Design Design Technology Ltd
002233	ADB Broadband Italia
002234	Corventis Inc.
002235	Strukton Systems bv
002236	VECTOR SP. Z O.O.
002237	Shinhint Group
002238	Logiplus
002239	Indiana Life Sciences Incorporated
00223A	Cisco SPVTG
00223B	Communication Networks, LLC
00223C	RATIO Entwicklungen GmbH
00223D	JumpGen Systems, LLC
00223E	IRTrans GmbH
00223F	Netgear
002240	Universal Telecom S/A
002241	Apple, Inc.
002242	Alacron Inc.
002243	AzureWave Technology Inc.
002244	Chengdu Linkon Communications Device Co., Ltd
002245	Leine & Linde AB
002246	Evoc Intelligent Technology Co.,Ltd.
002247	DAC ENGINEERING CO., LTD.
002248	Microsoft Corporation
002249	HOME MULTIENERGY SL
00224A	RAYLASE AG
00224B	AIRTECH TECHNOLOGIES, INC.
00224C	Nintendo Co., Ltd.
00224D	MITAC INTERNATIONAL CORP.
00224E	SEEnergy Corp.
00224F	Byzoro Networks Ltd.
002250	Point Six Wireless, LLC
002251	Lumasense Technologies
002252	ZOLL Lifecor Corporation
002253	Entorian Technologies
002254	Bigelow Aerospace
002255	Cisco Systems, Inc
002256	Cisco Systems, Inc
002257	3COM EUROPE LTD
002258	Taiyo Yuden Co., Ltd.
002259	Guangzhou New Postcom Equipment Co.,Ltd.
00225A	Garde Security AB
00225B	Teradici Corporation
00225C	Multimedia & Communication Technology
00225D	Digicable Network India Pvt. Ltd.
00225E	Uwin Technologies Co.,LTD
00225F	Liteon Technology Corporation
002260	AFREEY Inc.
002261	Frontier Silicon Ltd
002262	BEP Marine
002263	Koos Technical Services, Inc.
002264	Hewlett Packard
002265	Nokia Danmark A/S
002266	Nokia Danmark A/S
002267	Nortel Networks
002268	Hon Hai Precision Ind. Co.,Ltd.
002269	Hon Hai Precision Ind. Co.,Ltd.
00226A	Honeywell
00226B	Cisco-Linksys, LLC
00226C	LinkSprite Technologies, Inc.
00226D	Shenzhen GIEC Electronics Co., Ltd.
00226E	Gowell Electronic Limited
00226F	3onedata Technology Co. Ltd.
002270	ABK North America, LLC
002271	Jäger Computergesteuerte Meßtechnik GmbH.
002272	American Micro-Fuel Device Corp.
002273	Techway
002274	FamilyPhone AB
002275	Belkin International Inc.
002276	Triple EYE B.V.
002277	NEC Australia Pty Ltd
002278	Shenzhen  Tongfang Multimedia  Technology Co.,Ltd.
002279	Nippon Conlux Co., Ltd.
00227A	Telecom Design
00227B	Apogee Labs, Inc.
00227C	Woori SMT Co.,ltd
00227D	YE DATA INC.
00227E	Chengdu 30Kaitian Communication Industry Co.Ltd
00227F	Ruckus Wireless
002280	A2B Electronics AB
002281	Daintree Networks Pty
002282	8086 Consultancy
002283	Juniper Networks
002284	DESAY A&V SCIENCE AND TECHNOLOGY CO.,LTD
002285	NOMUS COMM SYSTEMS
002286	Astron
002287	Titan Wireless LLC
002288	Sagrad, Inc.
002289	Optosecurity Inc.
00228A	Teratronik elektronische systeme gmbh
00228B	Kensington Computer Products Group
00228C	Photon Europe GmbH
00228D	GBS Laboratories LLC
00228E	TV-NUMERIC
00228F	Cnrs
002290	Cisco Systems, Inc
002291	Cisco Systems, Inc
002292	Cinetal
002293	zte corporation
002294	Kyocera Corporation
002295	SGM Technology for lighting spa
002296	LinoWave Corporation
002297	XMOS Semiconductor
002298	Sony Mobile Communications AB
002299	SeaMicro Inc.
00229A	Lastar, Inc.
00229B	AverLogic Technologies, Inc.
00229C	Verismo Networks Inc
00229D	PYUNG-HWA IND.CO.,LTD
00229E	Social Aid Research Co., Ltd.
00229F	Sensys Traffic AB
0022A0	Delphi Corporation
0022A1	Huawei Symantec Technologies Co.,Ltd.
0022A2	Xtramus Technologies
0022A3	California Eastern Laboratories
0022A4	2Wire Inc
0022A5	Texas Instruments
0022A6	Sony Computer Entertainment America
0022A7	Tyco Electronics AMP GmbH
0022A8	Ouman Oy
0022A9	LG Electronics (Mobile Communications)
0022AA	Nintendo Co., Ltd.
0022AB	Shenzhen Turbosight Technology Ltd
0022AC	Hangzhou Siyuan Tech. Co., Ltd
0022AD	TELESIS TECHNOLOGIES, INC.
0022AE	Mattel Inc.
0022AF	Safety Vision
0022B0	D-Link Corporation
0022B1	Elbit Systems Ltd.
0022B2	4RF Communications Ltd
0022B3	Sei S.p.A.
0022B4	ARRIS Group, Inc.
0022B5	Novita
0022B6	Superflow Technologies Group
0022B7	GSS Grundig SAT-Systems GmbH
0022B8	Norcott
0022B9	Analogix Seminconductor, Inc
0022BA	HUTH Elektronik Systeme GmbH
0022BB	beyerdynamic GmbH & Co. KG
0022BC	JDSU France SAS
0022BD	Cisco Systems, Inc
0022BE	Cisco Systems, Inc
0022BF	SieAmp Group of Companies
0022C0	Shenzhen Forcelink Electronic Co, Ltd
0022C1	Active Storage Inc.
0022C2	Proview Eletrônica do Brasil LTDA
0022C3	Zeeport Technology Inc.
0022C4	epro GmbH
0022C5	INFORSON Co,Ltd.
0022C6	Sutus Inc
0022C7	SEGGER Microcontroller GmbH & Co. KG
0022C8	Applied Instruments B.V.
0022C9	Lenord, Bauer & Co GmbH
0022CA	Anviz Biometric Tech. Co., Ltd.
0022CB	IONODES Inc.
0022CC	SciLog, Inc.
0022CD	Ared Technology Co., Ltd.
0022CE	Cisco SPVTG
0022CF	PLANEX COMMUNICATIONS INC.
0022D0	Polar Electro Oy
0022D1	Albrecht Jung GmbH & Co. KG
0022D2	All Earth Comércio de Eletrônicos LTDA.
0022D3	Hub-Tech
0022D4	ComWorth Co., Ltd.
0022D5	Eaton Corp. Electrical Group Data Center Solutions - Pulizzi
0022D6	Cypak AB
0022D7	Nintendo Co., Ltd.
0022D8	Shenzhen GST Security and Safety Technology Limited
0022D9	Fortex Industrial Ltd.
0022DA	ANATEK, LLC
0022DB	Translogic Corporation
0022DC	Vigil Health Solutions Inc.
0022DD	Protecta Electronics Ltd
0022DE	OPPO Digital, Inc.
0022DF	TAMUZ Monitors
0022E0	Atlantic Software Technologies S.r.L.
0022E1	ZORT Labs, LLC.
0022E2	WABTEC Transit Division
0022E3	Amerigon
0022E4	APASS TECHNOLOGY CO., LTD.
0022E5	Fisher-Rosemount Systems Inc.
0022E6	Intelligent Data
0022E7	WPS Parking Systems
0022E8	Applition Co., Ltd.
0022E9	ProVision Communications
0022EA	Rustelcom Inc.
0022EB	Data Respons A/S
0022EC	IDEALBT TECHNOLOGY CORPORATION
0022ED	TSI Power Corporation
0022EE	Algo Communication Products Ltd
0022EF	iWDL Technologies
0022F0	3 Greens Aviation Limited
0022F1	Private
0022F2	SunPower Corp
0022F3	SHARP Corporation
0022F4	AMPAK Technology, Inc.
0022F5	Advanced Realtime Tracking GmbH
0022F6	Syracuse Research Corporation
0022F7	Conceptronic
0022F8	PIMA Electronic Systems Ltd.
0022F9	Pollin Electronic GmbH
0022FA	Intel Corporate
0022FB	Intel Corporate
0022FC	Nokia Danmark A/S
0022FD	Nokia Danmark A/S
0022FE	Advanced Illumination
0022FF	NIVIS LLC
002300	Cayee Computer Ltd.
002301	Witron Technology Limited
002302	Cobalt Digital, Inc.
002303	LITE-ON IT Corporation
002304	Cisco Systems, Inc
002305	Cisco Systems, Inc
002306	ALPS ELECTRIC CO.,LTD.
002307	FUTURE INNOVATION TECH CO.,LTD
002308	Arcadyan Technology Corporation
002309	Janam Technologies LLC
00230A	ARBURG GmbH & Co KG
00230B	ARRIS Group, Inc.
00230C	CLOVER ELECTRONICS CO.,LTD.
00230D	Nortel Networks
00230E	Gorba AG
00230F	Hirsch Electronics Corporation
002310	LNC Technology Co., Ltd.
002311	Gloscom Co., Ltd.
002312	Apple, Inc.
002313	Qool Technologies Ltd.
002314	Intel Corporate
002315	Intel Corporate
002316	KISAN ELECTRONICS CO
002317	Lasercraft Inc
002318	Toshiba
002319	Sielox LLC
00231A	ITF Co., Ltd.
00231B	Danaher Motion - Kollmorgen
00231C	Fourier Systems Ltd.
00231D	Deltacom Electronics Ltd
00231E	Cezzer Multimedia Technologies
00231F	Guangda Electronic & Telecommunication Technology Development Co., Ltd.
002320	Nicira Networks
002321	Avitech International Corp
002322	KISS Teknical Solutions, Inc.
002323	Zylin AS
002324	G-PRO COMPUTER
002325	IOLAN Holding
002326	FUJITSU LIMITED
002327	Shouyo Electronics CO., LTD
002328	ALCON TELECOMMUNICATIONS CO., LTD.
002329	DDRdrive LLC
00232A	EonasIt-               # eonas IT-Beratung und -Entwicklung GmbH
00232B	IRD A/S
00232C	Senticare
00232D	SandForce
00232E	Kedah Electronics Engineering, LLC
00232F	Advanced Card Systems Ltd.
002330	DIZIPIA, INC.
002331	Nintendo Co., Ltd.
002332	Apple, Inc.
002333	Cisco Systems, Inc
002334	Cisco Systems, Inc
002335	Linkflex Co.,Ltd
002336	METEL s.r.o.
002337	Global Star Solutions ULC
002338	OJ-Electronics A/S
002339	Samsung Electronics Co.,Ltd
00233A	Samsung Electronics Co.,Ltd
00233B	C-Matic Systems Ltd
00233C	Alflex
00233D	Novero holding B.V.
00233E	Alcatel-               # Alcatel-Lucent IPD
00233F	Purechoice Inc
002340	MiXTelematics
002341	Vanderbilt International (SWE) AB
002342	Coffee Equipment Company
002343	TEM AG
002344	Objective Interface Systems, Inc.
002345	Sony Mobile Communications AB
002346	Vestac
002347	ProCurve Networking by HP
002348	Sagemcom Broadband SAS
002349	Helmholtz Centre Berlin for Material and Energy
00234A	Private
00234B	Inyuan Technology Inc.
00234C	KTC AB
00234D	Hon Hai Precision Ind. Co.,Ltd.
00234E	Hon Hai Precision Ind. Co.,Ltd.
00234F	Luminous Power Technologies Pvt. Ltd.
002350	Lyntec
002351	2Wire Inc
002352	DATASENSOR S.p.A.
002353	F E T Elettronica snc
002354	ASUSTek COMPUTER INC.
002355	Kinco Automation(Shanghai) Ltd.
002356	Packet Forensics LLC
002357	Pitronot Technologies and Engineering P.T.E. Ltd.
002358	SYSTEL SA
002359	Benchmark Electronics ( Thailand ) Public Company Limited
00235A	COMPAL INFORMATION (KUNSHAN) CO., LTD.
00235B	Gulfstream
00235C	Aprius, Inc.
00235D	Cisco Systems, Inc
00235E	Cisco Systems, Inc
00235F	Silicon Micro Sensors GmbH
002360	Lookit Technology Co., Ltd
002361	Unigen Corporation
002362	Goldline Controls
002363	Zhuhai Raysharp Technology Co.,Ltd
002364	Power Instruments Pte Ltd
002365	Insta Elektro GmbH
002366	Beijing Siasun Electronic System Co.,Ltd.
002367	UniControls a.s.
002368	Zebra Technologies Inc
002369	Cisco-Linksys, LLC
00236A	SmartRG Inc
00236B	Xembedded, Inc.
00236C	Apple, Inc.
00236D	ResMed Ltd
00236E	Burster GmbH & Co KG
00236F	DAQ System
002370	Snell
002371	SOAM Systel
002372	MORE STAR INDUSTRIAL GROUP LIMITED
002373	GridIron Systems, Inc.
002374	ARRIS Group, Inc.
002375	ARRIS Group, Inc.
002376	HTC Corporation
002377	Isotek Electronics Ltd
002378	GN Netcom A/S
002379	Union Business Machines Co. Ltd.
00237A	Rim
00237B	WHDI LLC
00237C	Neotion
00237D	Hewlett Packard
00237E	ELSTER GMBH
00237F	PLANTRONICS, INC.
002380	Nanoteq
002381	Lengda Technology(Xiamen) Co.,Ltd.
002382	Lih Rong electronic Enterprise Co., Ltd.
002383	InMage Systems Inc
002384	GGH Engineering s.r.l.
002385	Antipode
002386	Tour & Andersson AB
002387	ThinkFlood, Inc.
002388	V.T. Telematica S.p.a.
002389	Hangzhou H3C Technologies Co., Limited
00238A	Ciena Corporation
00238B	QUANTA COMPUTER INC.
00238C	Private
00238D	Techno Design Co., Ltd.
00238E	ADB Broadband Italia
00238F	NIDEC COPAL CORPORATION
002390	Algolware Corporation
002391	Maxian
002392	Proteus Industries Inc.
002393	AJINEXTEK
002394	Samjeon
002395	ARRIS Group, Inc.
002396	ANDES TECHNOLOGY CORPORATION
002397	Westell Technologies Inc.
002398	Vutlan sro
002399	Samsung Electronics Co.,Ltd
00239A	EasyData Hardware GmbH
00239B	Elster Solutions, LLC
00239C	Juniper Networks
00239D	Mapower Electronics Co., Ltd
00239E	Jiangsu Lemote Technology Corporation Limited
00239F	Institut für Prüftechnik
0023A0	Hana CNS Co., LTD.
0023A1	Trend Electronics Ltd
0023A2	ARRIS Group, Inc.
0023A3	ARRIS Group, Inc.
0023A4	New Concepts Development Corp.
0023A5	SageTV, LLC
0023A6	E-Mon
0023A7	Redpine Signals, Inc.
0023A8	Marshall Electronics
0023A9	Beijing Detianquan Electromechanical Equipment Co., Ltd
0023AA	HFR, Inc.
0023AB	Cisco Systems, Inc
0023AC	Cisco Systems, Inc
0023AD	Xmark Corporation
0023AE	Dell Inc.
0023AF	ARRIS Group, Inc.
0023B0	COMXION Technology Inc.
0023B1	Longcheer Technology (Singapore) Pte Ltd
0023B2	Intelligent Mechatronic Systems Inc
0023B3	Lyyn AB
0023B4	Nokia Danmark A/S
0023B5	ORTANA LTD
0023B6	SECURITE COMMUNICATIONS / HONEYWELL
0023B7	Q-Light Co., Ltd.
0023B8	Sichuan Jiuzhou Electronic Technology Co.,Ltd
0023B9	Airbus Defence and Space Deutschland GmbH
0023BA	Chroma
0023BB	Schmitt Industries
0023BC	EQ-SYS GmbH
0023BD	Digital Ally, Inc.
0023BE	Cisco SPVTG
0023BF	Mainpine, Inc.
0023C0	Broadway Networks
0023C1	Securitas Direct AB
0023C2	SAMSUNG Electronics. Co. LTD
0023C3	LogMeIn, Inc.
0023C4	Lux Lumen
0023C5	Radiation Safety and Control Services Inc
0023C6	SMC Corporation
0023C7	Avsystem
0023C8	Team-R
0023C9	Sichuan Tianyi Information Science & Technology Stock CO.,LTD
0023CA	Behind The Set, LLC
0023CB	Shenzhen Full-join Technology Co.,Ltd
0023CC	Nintendo Co., Ltd.
0023CD	TP-LINK TECHNOLOGIES CO.,LTD.
0023CE	KITA DENSHI CORPORATION
0023CF	Cummins-               # CUMMINS-ALLISON CORP.
0023D0	Uniloc USA Inc.
0023D1	Trg
0023D2	Inhand Electronics, Inc.
0023D3	AirLink WiFi Networking Corp.
0023D4	Texas Instruments
0023D5	WAREMA electronic GmbH
0023D6	Samsung Electronics Co.,Ltd
0023D7	Samsung Electronics Co.,Ltd
0023D8	Ball-It Oy
0023D9	Banner Engineering
0023DA	Industrial Computer Source (Deutschland)GmbH
0023DB	saxnet gmbh
0023DC	Benein, Inc
0023DD	ELGIN S.A.
0023DE	Ansync Inc.
0023DF	Apple, Inc.
0023E0	INO Therapeutics LLC
0023E1	Cavena Image Products AB
0023E2	SEA Signalisation
0023E3	Microtronic AG
0023E4	IPnect co. ltd.
0023E5	IPaXiom Networks
0023E6	Pirkus, Inc.
0023E7	Hinke A/S
0023E8	Demco Corp.
0023E9	F5 Networks, Inc.
0023EA	Cisco Systems, Inc
0023EB	Cisco Systems, Inc
0023EC	Algorithmix GmbH
0023ED	ARRIS Group, Inc.
0023EE	ARRIS Group, Inc.
0023EF	Zuend Systemtechnik AG
0023F0	Shanghai Jinghan Weighing Apparatus Co. Ltd.
0023F1	Sony Mobile Communications AB
0023F2	Tvlogic
0023F3	Glocom, Inc.
0023F4	Masternaut
0023F5	WILO SE
0023F6	Softwell Technology Co., Ltd.
0023F7	Private
0023F8	ZyXEL Communications Corporation
0023F9	Double-Take Software, INC.
0023FA	RG Nets, Inc.
0023FB	IP Datatel, LLC.
0023FC	Ultra Stereo Labs, Inc
0023FD	AFT Atlas Fahrzeugtechnik GmbH
0023FE	Biodevices, SA
0023FF	Beijing HTTC Technology Ltd.
002400	Nortel Networks
002401	D-Link Corporation
002402	Op-Tection GmbH
002403	Nokia Danmark A/S
002404	Nokia Danmark A/S
002405	Dilog Nordic AB
002406	Pointmobile
002407	TELEM SAS
002408	Pacific Biosciences
002409	The Toro Company
00240A	US Beverage Net
00240B	Virtual Computer Inc.
00240C	DELEC GmbH
00240D	OnePath Networks LTD.
00240E	Inventec Besta Co., Ltd.
00240F	Ishii Tool & Engineering Corporation
002410	NUETEQ Technology,Inc.
002411	PharmaSmart LLC
002412	Benign Technologies Co, Ltd.
002413	Cisco Systems, Inc
002414	Cisco Systems, Inc
002415	Magnetic Autocontrol GmbH
002416	Any Use
002417	Thomson Telecom Belgium
002418	Nextwave Semiconductor
002419	Private
00241A	Red Beetle Inc.
00241B	iWOW Communications Pte Ltd
00241C	FuGang Electronic (DG) Co.,Ltd
00241D	GIGA-BYTE TECHNOLOGY CO.,LTD.
00241E	Nintendo Co., Ltd.
00241F	DCT-Delta GmbH
002420	NetUP Inc.
002421	MICRO-STAR INT'L CO., LTD.
002422	Knapp Logistik Automation GmbH
002423	AzureWave Technologies (Shanghai) Inc.
002424	Axis Network Technology
002425	Shenzhenshi chuangzhicheng Technology Co.,Ltd
002426	NOHMI BOSAI LTD.
002427	SSI COMPUTER CORP
002428	EnergyICT
002429	MK MASTER INC.
00242A	Hittite Microwave Corporation
00242B	Hon Hai Precision Ind. Co.,Ltd.
00242C	Hon Hai Precision Ind. Co.,Ltd.
00242E	Datastrip Inc.
00242F	Micron
002430	Ruby Tech Corp.
002431	Uni-v co.,ltd
002432	Neostar Technology Co.,LTD
002433	ALPS ELECTRIC CO.,LTD.
002434	Lectrosonics, Inc.
002435	WIDE CORPORATION
002436	Apple, Inc.
002437	Motorola - BSG
002438	Brocade Communications Systems, Inc.
002439	Digital Barriers Advanced Technologies
00243A	Ludl Electronic Products
00243B	CSSI (S) Pte Ltd
00243C	S.A.A.A.
00243D	Emerson Appliance Motors and Controls
00243F	Storwize, Inc.
002440	Halo Monitoring, Inc.
002441	Wanzl Metallwarenfabrik GmbH
002442	Axona Limited
002443	Nortel Networks
002444	Nintendo Co., Ltd.
002445	Adtran Inc
002446	MMB Research Inc.
002447	Kaztek Systems
002448	SpiderCloud Wireless, Inc
002449	Shen Zhen Lite Star Electronics Technology Co., Ltd
00244A	Voyant International
00244B	PERCEPTRON INC
00244C	Solartron Metrology Ltd
00244D	Hokkaido Electronics Corporation
00244E	RadChips, Inc.
00244F	Asantron Technologies Ltd.
002450	Cisco Systems, Inc
002451	Cisco Systems, Inc
002452	Silicon Software GmbH
002453	Initra d.o.o.
002454	Samsung Electronics Co.,Ltd
002455	MuLogic BV
002456	2Wire Inc
002458	PA Bastion CC
002459	ABB Automation products GmbH
00245A	Nanjing Panda Electronics Company Limited
00245B	RAIDON TECHNOLOGY, INC.
00245C	Design-Com Technologies Pty. Ltd.
00245D	Terberg besturingstechniek B.V.
00245E	Hivision Co.,ltd
00245F	Vine Telecom CO.,Ltd.
002460	Giaval Science Development Co. Ltd.
002461	Shin Wang Tech.
002462	Rayzone Corporation
002463	Phybridge Inc
002464	Bridge Technologies Co AS
002465	Elentec
002466	Unitron nv
002467	AOC International (Europe) GmbH
002468	Sumavision Technologies Co.,Ltd
002469	Smart Doorphones
00246A	Solid Year Co., Ltd.
00246B	Covia, Inc.
00246C	Aruba Networks
00246D	Weinzierl Engineering GmbH
00246E	Phihong USA Corp.
00246F	Onda Communication spa
002470	AUROTECH ultrasound AS.
002471	Fusion MultiSystems dba Fusion-io
002472	ReDriven Power Inc.
002473	3COM EUROPE LTD
002474	Autronica Fire And Securirty
002475	Compass System(Embedded Dept.)
002476	TAP.tv
002477	Tibbo Technology
002478	Mag Tech Electronics Co Limited
002479	Optec Displays, Inc.
00247A	FU YI CHENG Technology Co., Ltd.
00247B	Actiontec Electronics, Inc
00247C	Nokia Danmark A/S
00247D	Nokia Danmark A/S
00247E	Universal Global Scientific Industrial Co., Ltd.
00247F	Nortel Networks
002480	Meteocontrol GmbH
002481	Hewlett Packard
002482	Ruckus Wireless
002483	LG Electronics (Mobile Communications)
002484	Bang and Olufsen Medicom a/s
002485	ConteXtream Ltd
002486	DesignArt Networks
002487	Blackboard Inc.
002488	Centre For Development Of Telematics
002489	Vodafone Omnitel N.V.
00248A	Kaga Electronics Co., Ltd.
00248B	HYBUS CO., LTD.
00248C	ASUSTek COMPUTER INC.
00248D	Sony Interactive Entertainment Inc.
00248E	Infoware ZRt.
00248F	Do-Monix
002490	Samsung Electronics Co.,Ltd
002491	Samsung Electronics Co.,Ltd
002492	Motorola, Broadband Solutions Group
002493	ARRIS Group, Inc.
002494	Shenzhen Baoxin Tech CO., Ltd.
002495	ARRIS Group, Inc.
002496	Ginzinger electronic systems
002497	Cisco Systems, Inc
002498	Cisco Systems, Inc
002499	Aquila Technologies
00249A	Beijing Zhongchuang Telecommunication Test Co., Ltd.
00249B	Action Star Enterprise Co., Ltd.
00249C	Bimeng Comunication System Co. Ltd
00249D	NES Technology Inc.
00249E	ADC-Elektronik GmbH
00249F	RIM Testing Services
0024A0	ARRIS Group, Inc.
0024A1	ARRIS Group, Inc.
0024A2	Hong Kong Middleware Technology Limited
0024A3	Sonim Technologies Inc
0024A4	Siklu Communication
0024A5	BUFFALO.INC
0024A6	TELESTAR DIGITAL GmbH
0024A7	Advanced Video Communications Inc.
0024A8	ProCurve Networking by HP
0024A9	Ag Leader Technology
0024AA	Dycor Technologies Ltd.
0024AB	A7 Engineering, Inc.
0024AC	Hangzhou DPtech Technologies Co., Ltd.
0024AD	Adolf Thies Gmbh & Co. KG
0024AE	Morpho
0024AF	Echostar Technologies Corp
0024B0	ESAB AB
0024B1	Coulomb Technologies
0024B2	Netgear
0024B3	Graf-Syteco GmbH & Co. KG
0024B4	ESCATRONIC GmbH
0024B5	Nortel Networks
0024B6	Seagate Technology
0024B7	GridPoint, Inc.
0024B8	free alliance sdn bhd
0024B9	Wuhan Higheasy Electronic Technology Development Co.Ltd
0024BA	Texas Instruments
0024BB	CENTRAL Corporation
0024BC	HuRob Co.,Ltd
0024BD	Hainzl Industriesysteme GmbH
0024BE	Sony Corporation
0024BF	Ciat
0024C0	NTI COMODO INC
0024C1	ARRIS Group, Inc.
0024C2	Asumo Co.,Ltd.
0024C3	Cisco Systems, Inc
0024C4	Cisco Systems, Inc
0024C5	Meridian Audio Limited
0024C6	Hager Electro SAS
0024C7	Mobilarm Ltd
0024C8	Broadband Solutions Group
0024C9	Broadband Solutions Group
0024CA	Tobii Technology AB
0024CB	Autonet Mobile
0024CC	Fascinations Toys and Gifts, Inc.
0024CD	Willow Garage, Inc.
0024CE	Exeltech Inc
0024CF	Inscape Data Corporation
0024D0	Shenzhen SOGOOD Industry CO.,LTD.
0024D1	Thomson Inc.
0024D2	ASKEY COMPUTER CORP
0024D3	QUALICA Inc.
0024D4	FREEBOX SAS
0024D5	Winward Industrial Limited
0024D6	Intel Corporate
0024D7	Intel Corporate
0024D8	IlSung Precision
0024D9	BICOM, Inc.
0024DA	Innovar Systems Limited
0024DB	Alcohol Monitoring Systems
0024DC	Juniper Networks
0024DD	Centrak, Inc.
0024DE	GLOBAL Technology Inc.
0024DF	Digitalbox Europe GmbH
0024E0	DS Tech, LLC
0024E1	Convey Computer Corp.
0024E2	HASEGAWA ELECTRIC CO.,LTD.
0024E3	CAO Group
0024E4	Withings
0024E5	Seer Technology, Inc
0024E6	In Motion Technology Inc.
0024E7	Plaster Networks
0024E8	Dell Inc.
0024E9	Samsung Electronics Co.,Ltd
0024EA	iris-GmbH infrared & intelligent sensors
0024EB	ClearPath Networks, Inc.
0024EC	United Information Technology Co.,Ltd.
0024ED	YT Elec. Co,.Ltd.
0024EE	Wynmax Inc.
0024EF	Sony Mobile Communications AB
0024F0	Seanodes
0024F1	Shenzhen Fanhai Sanjiang Electronics Co., Ltd.
0024F2	Uniphone Telecommunication Co., Ltd.
0024F3	Nintendo Co., Ltd.
0024F4	Kaminario, Ltd.
0024F5	NDS Surgical Imaging
0024F6	MIYOSHI ELECTRONICS CORPORATION
0024F7	Cisco Systems, Inc
0024F8	Technical Solutions Company Ltd.
0024F9	Cisco Systems, Inc
0024FA	Hilger u. Kern GMBH
0024FB	Private
0024FC	QuoPin Co., Ltd.
0024FD	Accedian Networks Inc
0024FE	AVM GmbH
0024FF	QLogic Corporation
002500	Apple, Inc.
002501	JSC Supertel
002502	NaturalPoint
002503	IBM Corp
002504	Valiant Communications Limited
002505	eks Engel GmbH & Co. KG
002506	A.I. ANTITACCHEGGIO ITALIA SRL
002507	ASTAK Inc.
002508	Maquet Cardiopulmonary AG
002509	SHARETRONIC Group LTD
00250A	Security Expert Co. Ltd
00250B	CENTROFACTOR  INC
00250C	Enertrac
00250D	GZT Telkom-Telmor sp. z o.o.
00250E	gt german telematics gmbh
00250F	On-Ramp Wireless, Inc.
002510	Pico-Tesla Magnetic Therapies
002511	Elitegroup Computer Systems Co.,Ltd.
002512	zte corporation
002513	CXP DIGITAL BV
002514	PC Worth Int'l Co., Ltd.
002515	Sfr
002516	Integrated Design Tools, Inc.
002517	Venntis, LLC
002518	Power PLUS Communications AG
002519	Viaas Inc
00251A	Psiber Data Systems Inc.
00251B	Philips CareServant
00251C	Edt
00251D	DSA Encore, LLC
00251E	ROTEL TECHNOLOGIES
00251F	ZYNUS VISION INC.
002520	SMA Railway Technology GmbH
002521	Logitek Electronic Systems, Inc.
002522	ASRock Incorporation
002523	OCP Inc.
002524	Lightcomm Technology Co., Ltd
002525	CTERA Networks Ltd.
002526	Genuine Technologies Co., Ltd.
002527	Bitrode Corp.
002528	Daido Signal Co., Ltd.
002529	COMELIT GROUP S.P.A
00252A	Chengdu GeeYa Technology Co.,LTD
00252B	Stirling Energy Systems
00252C	Entourage Systems, Inc.
00252D	Kiryung Electronics
00252E	Cisco SPVTG
00252F	Energy, Inc.
002530	Aetas Systems Inc.
002531	Cloud Engines, Inc.
002532	Digital Recorders
002533	WITTENSTEIN AG
002535	Minimax GmbH & Co KG
002536	Oki Electric Industry Co., Ltd.
002537	Runcom Technologies Ltd.
002538	Samsung Electronics Co., Ltd., Memory Division
002539	IfTA GmbH
00253A	CEVA, Ltd.
00253B	din Dietmar Nocker Facilitymanagement GmbH
00253C	2Wire Inc
00253D	DRS Consolidated Controls
00253E	Sensus Metering Systems
002540	Quasar Technologies, Inc.
002541	Maquet Critical Care AB
002542	Pittasoft
002543	MONEYTECH
002544	LoJack Corporation
002545	Cisco Systems, Inc
002546	Cisco Systems, Inc
002547	Nokia Danmark A/S
002548	Nokia Danmark A/S
002549	Jeorich Tech. Co.,Ltd.
00254A	RingCube Technologies, Inc.
00254B	Apple, Inc.
00254C	Videon Central, Inc.
00254D	Singapore Technologies Electronics Limited
00254E	Vertex Wireless Co., Ltd.
00254F	ELETTROLAB Srl
002550	Riverbed Technology, Inc.
002551	SE-Elektronic GmbH
002552	VXi Corporation
002553	ADB Broadband Italia
002554	Pixel8 Networks
002555	Visonic Technologies 1993 Ltd.
002556	Hon Hai Precision Ind. Co.,Ltd.
002557	BlackBerry RTS
002558	Mpedia
002559	Syphan Technologies Ltd
00255A	Tantalus Systems Corp.
00255B	CoachComm, LLC
00255C	NEC Corporation
00255D	Morningstar Corporation
00255E	Shanghai Dare Technologies Co.,Ltd.
00255F	SenTec AG
002560	Ibridge Networks & Communications Ltd.
002561	ProCurve Networking by HP
002562	interbro Co. Ltd.
002563	Luxtera Inc
002564	Dell Inc.
002565	Vizimax Inc.
002566	Samsung Electronics Co.,Ltd
002567	Samsung Electronics Co.,Ltd
002568	HUAWEI TECHNOLOGIES CO.,LTD
002569	Sagemcom Broadband SAS
00256A	inIT - Institut Industrial IT
00256B	ATENIX E.E. s.r.l.
00256C	Azimut Production Association JSC
00256D	Broadband Forum
00256E	Van Breda B.V.
00256F	Dantherm Power
002570	Eastern Communications Company Limited
002571	Zhejiang Tianle Digital Electric Co.,Ltd
002572	Nemo-Q International AB
002573	ST Electronics (Info-Security) Pte Ltd
002574	KUNIMI MEDIA DEVICE Co., Ltd.
002575	FiberPlex Technologies, LLC
002576	NELI TECHNOLOGIES
002577	D-BOX Technologies
002578	JSC Concern Sozvezdie
002579	J & F Labs
00257A	CAMCO Produktions- und Vertriebs-GmbH für  Beschallungs- und Beleuchtungsanlagen
00257B	STJ  ELECTRONICS  PVT  LTD
00257C	Huachentel Technology Development Co., Ltd
00257D	PointRed Telecom Private Ltd.
00257E	NEW POS Technology Limited
00257F	CallTechSolution Co.,Ltd
002580	Equipson S.A.
002581	x-star networks Inc.
002582	Maksat Technologies (P) Ltd
002583	Cisco Systems, Inc
002584	Cisco Systems, Inc
002585	KokuyoS&               # KOKUYO S&T Co., Ltd.
002586	TP-LINK TECHNOLOGIES CO.,LTD.
002587	Vitality, Inc.
002588	Genie Industries, Inc.
002589	Hills Industries Limited
00258A	Pole/Zero Corporation
00258B	Mellanox Technologies, Inc.
00258C	ESUS ELEKTRONIK SAN. VE DIS. TIC. LTD. STI.
00258D	Haier
00258E	The Weather Channel
00258F	Trident Microsystems, Inc.
002590	Super Micro Computer, Inc.
002591	NEXTEK, Inc.
002592	Guangzhou Shirui Electronic Co., Ltd
002593	DatNet Informatikai Kft.
002594	Eurodesign BG LTD
002595	Northwest Signal Supply, Inc
002596	GIGAVISION srl
002597	Kalki Communication Technologies
002598	Zhong Shan City Litai Electronic Industrial Co. Ltd
002599	Hedon e.d. B.V.
00259A	CEStronics GmbH
00259B	Beijing PKUNITY Microsystems Technology Co., Ltd
00259C	Cisco-Linksys, LLC
00259D	Private
00259E	HUAWEI TECHNOLOGIES CO.,LTD
00259F	TechnoDigital Technologies GmbH
0025A0	Nintendo Co., Ltd.
0025A1	Enalasys
0025A2	Alta Definicion LINCEO S.L.
0025A3	Trimax Wireless, Inc.
0025A4	EuroDesign embedded technologies GmbH
0025A5	Walnut Media Network
0025A6	Central Network Solution Co., Ltd.
0025A7	Comverge, Inc.
0025A8	Kontron (BeiJing) Technology Co.,Ltd
0025A9	Shanghai Embedway Information Technologies Co.,Ltd
0025AA	Beijing Soul Technology Co.,Ltd.
0025AB	AIO LCD PC BU / TPV
0025AC	I-Tech corporation
0025AD	Manufacturing Resources International
0025AE	Microsoft Corporation
0025AF	COMFILE Technology
0025B0	Schmartz Inc
0025B1	Maya-Creation Corporation
0025B2	MBDA Deutschland GmbH
0025B3	Hewlett Packard
0025B4	Cisco Systems, Inc
0025B5	Cisco Systems, Inc
0025B6	Telecom FM
0025B7	Costar  electronics, inc.,
0025B8	Agile Communications, Inc.
0025B9	Cypress Solutions Inc
0025BA	Alcatel-               # Alcatel-Lucent IPD
0025BB	INNERINT Co., Ltd.
0025BC	Apple, Inc.
0025BD	Italdata Ingegneria dell'Idea S.p.A.
0025BE	Tektrap Systems Inc.
0025BF	Wireless Cables Inc.
0025C0	ZillionTV Corporation
0025C1	Nawoo Korea Corp.
0025C2	RingBell Co.,Ltd.
0025C3	21168
0025C4	Ruckus Wireless
0025C5	Star Link Communication Pvt. Ltd.
0025C6	kasercorp, ltd
0025C7	altek Corporation
0025C8	S-Access GmbH
0025C9	SHENZHEN HUAPU DIGITAL CO., LTD
0025CA	LS Research, LLC
0025CB	Reiner SCT
0025CC	Mobile Communications Korea Incorporated
0025CD	Skylane Optics
0025CE	InnerSpace
0025CF	Nokia Danmark A/S
0025D0	Nokia Danmark A/S
0025D1	Eastern Asia Technology Limited
0025D2	InpegVision Co., Ltd
0025D3	AzureWave Technology Inc.
0025D4	General Dynamics Mission Systems
0025D5	Robonica (Pty) Ltd
0025D6	The Kroger Co.
0025D7	Cedo
0025D8	KOREA MAINTENANCE
0025D9	DataFab Systems Inc.
0025DA	Secura Key
0025DB	ATI Electronics(Shenzhen) Co., LTD
0025DC	Sumitomo Electric Industries,Ltd
0025DD	SUNNYTEK INFORMATION CO., LTD.
0025DE	Probits Co., LTD.
0025DF	Private
0025E0	CeedTec Sdn Bhd
0025E1	SHANGHAI SEEYOO ELECTRONIC & TECHNOLOGY CO., LTD
0025E2	Everspring Industry Co., Ltd.
0025E3	Hanshinit Inc.
0025E4	OMNI-WiFi, LLC
0025E5	LG Electronics (Mobile Communications)
0025E6	Belgian Monitoring Systems bvba
0025E7	Sony Mobile Communications AB
0025E8	Idaho Technology
0025E9	i-mate Development, Inc.
0025EA	Iphion BV
0025EB	Reutech Radar Systems (PTY) Ltd
0025EC	Humanware
0025ED	NuVo Technologies LLC
0025EE	Avtex Ltd
0025EF	I-TEC Co., Ltd.
0025F0	Suga Electronics Limited
0025F1	ARRIS Group, Inc.
0025F2	ARRIS Group, Inc.
0025F3	Nordwestdeutsche Zählerrevision
0025F4	KoCo Connector AG
0025F5	DVS Korea, Co., Ltd
0025F6	netTALK.com, Inc.
0025F7	Ansaldo STS USA
0025F9	GMK electronic design GmbH
0025FA	J&M Analytik AG
0025FB	Tunstall Healthcare A/S
0025FC	ENDA ENDUSTRIYEL ELEKTRONIK LTD. STI.
0025FD	OBR Centrum Techniki Morskiej S.A.
0025FE	Pilot Electronics Corporation
0025FF	CreNova Multimedia Co., Ltd
002600	TEAC Australia Pty Ltd.
002601	Cutera Inc
002602	SMART Temps LLC
002603	Shenzhen Wistar Technology Co., Ltd
002604	Audio Processing Technology Ltd
002605	CC Systems AB
002606	RAUMFELD GmbH
002607	Enabling Technology Pty Ltd
002608	Apple, Inc.
002609	Phyllis Co., Ltd.
00260A	Cisco Systems, Inc
00260B	Cisco Systems, Inc
00260C	Dataram
00260D	Mercury Systems, Inc.
00260E	Ablaze Systems, LLC
00260F	Linn Products Ltd
002610	Apacewave Technologies
002611	Licera AB
002612	Space Exploration Technologies
002613	Engel Axil S.L.
002614	Ktnf
002615	Teracom Limited
002616	Rosemount Inc.
002617	OEM Worldwide
002618	ASUSTek COMPUTER INC.
002619	Frc
00261A	Femtocomm System Technology Corp.
00261B	LAUREL BANK MACHINES CO., LTD.
00261C	NEOVIA INC.
00261D	COP SECURITY SYSTEM CORP.
00261E	QINGBANG ELEC(SZ) CO., LTD
00261F	SAE Magnetics (H.K.) Ltd.
002620	ISGUS GmbH
002621	InteliCloud Technology Inc.
002622	COMPAL INFORMATION (KUNSHAN) CO., LTD.
002623	JRD Communication Inc
002624	Thomson Inc.
002625	MediaSputnik
002626	Geophysical Survey Systems, Inc.
002627	Truesell
002628	companytec automação e controle ltda.
002629	Juphoon System Software Inc.
00262A	Proxense, LLC
00262B	Wongs Electronics Co. Ltd.
00262C	IKT Advanced Technologies s.r.o.
00262D	Wistron Corporation
00262E	Chengdu Jiuzhou Electronic Technology Inc
00262F	HAMAMATSU TOA ELECTRONICS
002630	ACOREL S.A.S
002631	COMMTACT LTD
002632	Instrumentation Technologies d.d.
002633	MIR - Medical International Research
002634	Infineta Systems, Inc
002635	Bluetechnix GmbH
002636	ARRIS Group, Inc.
002637	SAMSUNG ELECTRO MECHANICS CO., LTD.
002638	Xia Men Joyatech Co., Ltd.
002639	T.M. Electronics, Inc.
00263A	Digitec Systems
00263B	Onbnetech
00263C	Bachmann Technology GmbH & Co. KG
00263D	MIA Corporation
00263E	Trapeze Networks
00263F	LIOS Technology GmbH
002640	Baustem Broadband Technologies, Ltd.
002641	ARRIS Group, Inc.
002642	ARRIS Group, Inc.
002643	ALPS ELECTRIC CO.,LTD.
002644	Thomson Telecom Belgium
002645	Circontrol S.A.
002646	SHENYANG TONGFANG MULTIMEDIA TECHNOLOGY COMPANY LIMITED
002647	WFE TECHNOLOGY CORP.
002648	Emitech Corp.
00264A	Apple, Inc.
00264C	Shanghai DigiVision Technology Co., Ltd.
00264D	Arcadyan Technology Corporation
00264E	Rail & Road Protec GmbH
00264F	Krüger &Gothe GmbH
002650	2Wire Inc
002651	Cisco Systems, Inc
002652	Cisco Systems, Inc
002653	DaySequerra Corporation
002654	3Com Corporation
002655	Hewlett Packard
002656	Sansonic Electronics USA
002657	OOO NPP EKRA
002658	T-Platforms (Cyprus) Limited
002659	Nintendo Co., Ltd.
00265A	D-Link Corporation
00265B	Hitron Technologies. Inc
00265C	Hon Hai Precision Ind. Co.,Ltd.
00265D	Samsung Electronics Co.,Ltd
00265E	Hon Hai Precision Ind. Co.,Ltd.
00265F	Samsung Electronics Co.,Ltd
002660	Logiways
002661	Irumtek Co., Ltd.
002662	Actiontec Electronics, Inc
002663	Shenzhen Huitaiwei Tech. Ltd, co.
002664	Core System Japan
002665	ProtectedLogic Corporation
002666	EFM Networks
002667	CARECOM CO.,LTD.
002668	Nokia Danmark A/S
002669	Nokia Danmark A/S
00266A	ESSENSIUM NV
00266B	SHINE UNION ENTERPRISE LIMITED
00266C	INVENTEC Corporation
00266D	MobileAccess Networks
00266E	Nissho-denki Co.,LTD.
00266F	Coordiwise Technology Corp.
002670	Cinch Connectors
002671	AUTOVISION Co., Ltd
002672	AAMP of America
002673	RICOH COMPANY,LTD.
002674	Electronic Solutions, Inc.
002675	Aztech Electronics Pte Ltd
002676	COMMidt AS
002677	DEIF A/S
002678	Logic Instrument SA
002679	Euphonic Technologies, Inc.
00267A	wuhan hongxin telecommunication technologies co.,ltd
00267B	GSI Helmholtzzentrum für Schwerionenforschung GmbH
00267C	Metz-Werke GmbH & Co KG
00267D	A-Max Technology Macao Commercial Offshore Company Limited
00267E	PARROT SA
00267F	Zenterio AB
002680	SIL3 Pty.Ltd
002681	Interspiro AB
002682	Gemtek Technology Co., Ltd.
002683	Ajoho Enterprise Co., Ltd.
002684	KISAN SYSTEM
002685	Digital Innovation
002686	Quantenna Communcations, Inc.
002687	corega K.K
002688	Juniper Networks
002689	General Dynamics Robotic Systems
00268A	Terrier SC Ltd
00268B	Guangzhou Escene Computer Technology Limited
00268C	StarLeaf Ltd.
00268D	CellTel S.p.A.
00268E	Alta Solutions, Inc.
00268F	MTA SpA
002690	I DO IT
002691	Sagemcom Broadband SAS
002692	Mitsubishi Electric Co.
002693	QVidium Technologies, Inc.
002694	Senscient Ltd
002695	ZT Group Int'l Inc
002696	NOOLIX Co., Ltd
002697	Alpha  Technologies Inc.
002698	Cisco Systems, Inc
002699	Cisco Systems, Inc
00269A	Carina System Co., Ltd.
00269B	SOKRAT Ltd.
00269C	ITUS JAPAN CO. LTD
00269D	M2Mnet Co., Ltd.
00269E	QUANTA COMPUTER INC.
00269F	Private
0026A0	Moblic
0026A1	Megger
0026A2	Instrumentation Technology Systems
0026A3	FQ Ingenieria Electronica S.A.
0026A4	Novus Produtos Eletronicos Ltda
0026A5	MICROROBOT.CO.,LTD
0026A6	Trixell
0026A7	CONNECT SRL
0026A8	DAEHAP HYPER-TECH
0026A9	Strong Technologies Pty Ltd
0026AA	Kenmec Mechanical Engineering Co., Ltd.
0026AB	Seiko Epson Corporation
0026AC	Shanghai LUSTER Teraband photonic Co., Ltd.
0026AD	Arada Systems, Inc.
0026AE	Wireless Measurement Ltd
0026AF	Duelco A/S
0026B0	Apple, Inc.
0026B1	Navis Auto Motive Systems, Inc.
0026B2	Setrix GmbH
0026B3	Thales Communications Inc
0026B4	Ford Motor Company
0026B5	ICOMM Tele Ltd
0026B6	ASKEY COMPUTER CORP
0026B7	Kingston Technology Company, Inc.
0026B8	Actiontec Electronics, Inc
0026B9	Dell Inc.
0026BA	ARRIS Group, Inc.
0026BB	Apple, Inc.
0026BC	General Jack Technology Ltd.
0026BD	JTEC Card & Communication Co., Ltd.
0026BE	Schoonderbeek Elektronica Systemen B.V.
0026BF	ShenZhen Temobi Science&Tech Development Co.,Ltd
0026C0	EnergyHub
0026C1	ARTRAY CO., LTD.
0026C2	SCDI Co. LTD
0026C3	Insightek Corp.
0026C4	Cadmos microsystems S.r.l.
0026C5	Guangdong Gosun Telecommunications Co.,Ltd
0026C6	Intel Corporate
0026C7	Intel Corporate
0026C8	System Sensor
0026C9	Proventix Systems, Inc.
0026CA	Cisco Systems, Inc
0026CB	Cisco Systems, Inc
0026CC	Nokia Danmark A/S
0026CD	PurpleComm, Inc.
0026CE	Kozumi USA Corp.
0026CF	DEKA R&D
0026D0	Semihalf
0026D1	S Squared Innovations Inc.
0026D2	Pcube Systems, Inc.
0026D3	Zeno Information System
0026D4	IRCA SpA
0026D5	Ory Solucoes em Comercio de Informatica Ltda.
0026D6	Ningbo Andy Optoelectronic Co., Ltd.
0026D7	KM Electornic Technology Co., Ltd.
0026D8	Magic Point Inc.
0026D9	ARRIS Group, Inc.
0026DA	Universal Media Corporation /Slovakia/ s.r.o.
0026DB	Ionics EMS Inc.
0026DC	Optical Systems Design
0026DD	Fival Science & Technology Co.,Ltd.
0026DE	FDI MATELEC
0026DF	TaiDoc Technology Corp.
0026E0	Asiteq
0026E1	Stanford University, OpenFlow Group
0026E2	LG Electronics (Mobile Communications)
0026E3	Dti
0026E4	Canal+                 # Canal +
0026E5	AEG Power Solutions
0026E6	Visionhitech Co., Ltd.
0026E7	Shanghai ONLAN Communication Tech. Co., Ltd.
0026E8	Murata Manufacturing Co., Ltd.
0026E9	SP Corp
0026EA	Cheerchip Electronic Technology (ShangHai) Co., Ltd.
0026EB	Advanced Spectrum Technology Co., Ltd.
0026EC	Legrand Home Systems, Inc
0026ED	zte corporation
0026EE	TKM GmbH
0026EF	Technology Advancement Group, Inc.
0026F0	cTrixs International GmbH.
0026F1	ProCurve Networking by HP
0026F2	Netgear
0026F3	SMC Networks
0026F4	Nesslab
0026F5	XRPLUS Inc.
0026F6	Military Communication Institute
0026F7	Nivetti Systems Pvt. Ltd.
0026F8	Golden Highway Industry Development Co., Ltd.
0026F9	S.E.M. srl
0026FA	BandRich Inc.
0026FB	AirDio Wireless, Inc.
0026FC	AcSiP Technology Corp.
0026FD	Interactive Intelligence
0026FE	MKD Technology Inc.
0026FF	BlackBerry RTS
002700	Shenzhen Siglent Technology Co., Ltd.
002701	INCOstartec GmbH
002702	SolarEdge Technologies
002703	Testech Electronics Pte Ltd
002704	Accelerated Concepts, Inc
002705	Sectronic
002706	Yoisys
002707	Lift Complex DS, JSC
002708	Nordiag ASA
002709	Nintendo Co., Ltd.
00270A	IEE S.A.
00270B	Adura Technologies
00270C	Cisco Systems, Inc
00270D	Cisco Systems, Inc
00270E	Intel Corporate
00270F	Envisionnovation Inc
002710	Intel Corporate
002711	LanPro Inc
002712	MaxVision LLC
002713	Universal Global Scientific Industrial Co., Ltd.
002714	Grainmustards, Co,ltd.
002715	Rebound Telecom. Co., Ltd
002716	Adachi-Syokai Co., Ltd.
002717	CE Digital(Zhenjiang)Co.,Ltd
002718	Suzhou NEW SEAUNION Video Technology Co.,Ltd
002719	TP-LINK TECHNOLOGIES CO.,LTD.
00271A	Geenovo Technology Ltd.
00271B	Alec Sicherheitssysteme GmbH
00271C	MERCURY CORPORATION
00271D	Comba Telecom Systems (China) Ltd.
00271E	Xagyl Communications
00271F	MIPRO Electronics Co., Ltd
002720	NEW-SOL COM
002721	Shenzhen Baoan Fenda Industrial Co., Ltd
002722	Ubiquiti Networks Inc.
0027F8	Brocade Communications Systems, Inc.
0028F8	Intel Corporate
002926	Applied Optoelectronics, Inc Taiwan Branch
002A10	Cisco Systems, Inc
002A6A	Cisco Systems, Inc
002AAF	LARsys-Automation GmbH
002CC8	Cisco Systems, Inc
002D76	TITECH GmbH
003000	ALLWELL TECHNOLOGY CORP.
003001	Smp
003002	Expand Networks
003003	Phasys Ltd.
003004	LEADTEK RESEARCH INC.
003005	Fujitsu Siemens Computers
003006	SUPERPOWER COMPUTER
003007	OPTI, INC.
003008	AVIO DIGITAL, INC.
003009	Tachion Networks, Inc.
00300A	Aztech Electronics Pte Ltd
00300B	mPHASE Technologies, Inc.
00300C	CONGRUENCY, LTD.
00300D	MMC Technology, Inc.
00300E	Klotz Digital AG
00300F	IMT - Information Management T
003010	VISIONETICS INTERNATIONAL
003011	HMS Industrial Networks
003012	DIGITAL ENGINEERING LTD.
003013	NEC Corporation
003014	DIVIO, INC.
003015	CP CLARE CORP.
003016	ISHIDA CO., LTD.
003017	BlueArc UK Ltd
003018	Jetway Information Co., Ltd.
003019	Cisco Systems, Inc
00301A	SMARTBRIDGES PTE. LTD.
00301B	SHUTTLE, INC.
00301C	ALTVATER AIRDATA SYSTEMS
00301D	SKYSTREAM, INC.
00301E	3COM EUROPE LTD.
00301F	OPTICAL NETWORKS, INC.
003020	TSI, Inc..
003021	HSING TECH. ENTERPRISE CO.,LTD
003022	Fong Kai Industrial Co., Ltd.
003023	COGENT COMPUTER SYSTEMS, INC.
003024	Cisco Systems, Inc
003025	CHECKOUT COMPUTER SYSTEMS, LTD
003026	HeiTel Digital Video GmbH
003027	KERBANGO, INC.
003028	FASE Saldatura srl
003029	Opicom
00302A	SOUTHERN INFORMATION
00302B	INALP NETWORKS, INC.
00302C	SYLANTRO SYSTEMS CORPORATION
00302D	QUANTUM BRIDGE COMMUNICATIONS
00302E	Hoft & Wessel AG
00302F	GE Aviation System
003030	HARMONIX CORPORATION
003031	LIGHTWAVE COMMUNICATIONS, INC.
003032	MagicRam, Inc.
003033	ORIENT TELECOM CO., LTD.
003034	SET ENGINEERING
003035	Corning Incorporated
003036	RMP ELEKTRONIKSYSTEME GMBH
003037	Packard Bell Nec Services
003038	XCP, INC.
003039	SOFTBOOK PRESS
00303A	Maatel
00303B	PowerCom Technology
00303C	ONNTO CORP.
00303D	IVA CORPORATION
00303E	Radcom Ltd.
00303F	TurboComm Tech Inc.
003040	Cisco Systems, Inc
003041	SAEJIN T & M CO., LTD.
003042	DeTeWe-Deutsche Telephonwerke
003043	IDREAM TECHNOLOGIES, PTE. LTD.
003044	CradlePoint, Inc
003045	Village Networks, Inc. (VNI)
003046	Controlled Electronic Manageme
003047	NISSEI ELECTRIC CO., LTD.
003048	Super Micro Computer, Inc.
003049	BRYANT TECHNOLOGY, LTD.
00304A	Fraunhofer IPMS
00304B	ORBACOM SYSTEMS, INC.
00304C	APPIAN COMMUNICATIONS, INC.
00304D	Esi
00304E	BUSTEC PRODUCTION LTD.
00304F	PLANET Technology Corporation
003050	Versa Technology
003051	ORBIT AVIONIC & COMMUNICATION
003052	ELASTIC NETWORKS
003053	Basler AG
003054	CASTLENET TECHNOLOGY, INC.
003055	Renesas Technology America, Inc.
003056	Beck IPC GmbH
003057	QTelNet, Inc.
003058	API MOTION
003059	KONTRON COMPACT COMPUTERS AG
00305A	TELGEN CORPORATION
00305B	Toko Inc.
00305C	SMAR Laboratories Corp.
00305D	DIGITRA SYSTEMS, INC.
00305E	Abelko Innovation
00305F	Hasselblad
003060	Powerfile, Inc.
003061	Mobytel
003062	IP Video Networks Inc
003063	SANTERA SYSTEMS, INC.
003064	ADLINK TECHNOLOGY, INC.
003065	Apple, Inc.
003066	Rfm
003067	BIOSTAR Microtech Int'l Corp.
003068	CYBERNETICS TECH. CO., LTD.
003069	IMPACCT TECHNOLOGY CORP.
00306A	PENTA MEDIA CO., LTD.
00306B	CMOS SYSTEMS, INC.
00306C	Hitex Holding GmbH
00306D	LUCENT TECHNOLOGIES
00306E	Hewlett Packard
00306F	SEYEON TECH. CO., LTD.
003070	1Net Corporation
003071	Cisco Systems, Inc
003072	Intellibyte Inc.
003073	International Microsystems, In
003074	EQUIINET LTD.
003075	Adtech
003076	Akamba Corporation
003077	ONPREM NETWORKS
003078	Cisco Systems, Inc
003079	CQOS, INC.
00307A	Advanced Technology & Systems
00307B	Cisco Systems, Inc
00307C	ADID SA
00307D	GRE AMERICA, INC.
00307E	Redflex Communication Systems
00307F	IRLAN LTD.
003080	Cisco Systems, Inc
003081	ALTOS C&C
003082	TAIHAN ELECTRIC WIRE CO., LTD.
003083	Ivron Systems
003084	ALLIED TELESYN INTERNAIONAL
003085	Cisco Systems, Inc
003086	Transistor Devices, Inc.
003087	VEGA GRIESHABER KG
003088	Ericsson
003089	Spectrapoint Wireless, LLC
00308A	NICOTRA SISTEMI S.P.A
00308B	Brix Networks
00308C	Quantum Corporation
00308D	Pinnacle Systems, Inc.
00308E	CROSS MATCH TECHNOLOGIES, INC.
00308F	MICRILOR, Inc.
003090	CYRA TECHNOLOGIES, INC.
003091	TAIWAN FIRST LINE ELEC. CORP.
003092	ModuNORM GmbH
003093	Sonnet Technologies, Inc
003094	Cisco Systems, Inc
003095	Procomp Informatics, Ltd.
003096	Cisco Systems, Inc
003097	AB Regin
003098	Global Converging Technologies
003099	BOENIG UND KALLENBACH OHG
00309A	ASTRO TERRA CORP.
00309B	Smartware
00309C	Timing Applications, Inc.
00309D	Nimble Microsystems, Inc.
00309E	WORKBIT CORPORATION.
00309F	AMBER NETWORKS
0030A0	TYCO SUBMARINE SYSTEMS, LTD.
0030A1	WEBGATE Inc.
0030A2	Lightner Engineering
0030A3	Cisco Systems, Inc
0030A4	Woodwind Communications System
0030A5	ACTIVE POWER
0030A6	VIANET TECHNOLOGIES, LTD.
0030A7	SCHWEITZER ENGINEERING
0030A8	OL'E COMMUNICATIONS, INC.
0030A9	Netiverse, Inc.
0030AA	AXUS MICROSYSTEMS, INC.
0030AB	DELTA NETWORKS, INC.
0030AC	Systeme Lauer GmbH & Co., Ltd.
0030AD	SHANGHAI COMMUNICATION
0030AE	Times N System, Inc.
0030AF	Honeywell GmbH
0030B0	Convergenet Technologies
0030B1	Trunknet
0030B2	L-3 Sonoma EO
0030B3	San Valley Systems, Inc.
0030B4	INTERSIL CORP.
0030B5	Tadiran Microwave Networks
0030B6	Cisco Systems, Inc
0030B7	Teletrol Systems, Inc.
0030B8	RiverDelta Networks
0030B9	Ectel
0030BA	AC&T SYSTEM CO., LTD.
0030BB	CacheFlow, Inc.
0030BC	Optronic AG
0030BD	BELKIN COMPONENTS
0030BE	City-Net Technology, Inc.
0030BF	MULTIDATA GMBH
0030C0	Lara Technology, Inc.
0030C1	Hewlett Packard
0030C2	Comone
0030C3	FLUECKIGER ELEKTRONIK AG
0030C4	Canon Imaging Systems Inc.
0030C5	CADENCE DESIGN SYSTEMS, INC.
0030C6	CONTROL SOLUTIONS, INC.
0030C7	Macromate Corp.
0030C8	GAD LINE, LTD.
0030C9	LuxN, N
0030CA	Discovery Com
0030CB	OMNI FLOW COMPUTERS, INC.
0030CC	Tenor Networks, Inc.
0030CD	CONEXANT SYSTEMS, INC.
0030CE	Zaffire
0030CF	TWO TECHNOLOGIES, INC.
0030D0	Tellabs
0030D1	INOVA CORPORATION
0030D2	WIN TECHNOLOGIES, CO., LTD.
0030D3	Agilent Technologies, Inc.
0030D4	AAE Systems, Inc.
0030D5	DResearch GmbH
0030D6	MSC VERTRIEBS GMBH
0030D7	Innovative Systems, L.L.C.
0030D8	Sitek
0030D9	DATACORE SOFTWARE CORP.
0030DA	Comtrend Corporation
0030DB	Mindready Solutions, Inc.
0030DC	RIGHTECH CORPORATION
0030DD	INDIGITA CORPORATION
0030DE	WAGO Kontakttechnik GmbH
0030DF	KB/TEL TELECOMUNICACIONES
0030E0	OXFORD SEMICONDUCTOR LTD.
0030E1	Network Equipment Technologies, Inc.
0030E2	GARNET SYSTEMS CO., LTD.
0030E3	SEDONA NETWORKS CORP.
0030E4	CHIYODA SYSTEM RIKEN
0030E5	Amper Datos S.A.
0030E6	Draeger Medical Systems, Inc.
0030E7	CNF MOBILE SOLUTIONS, INC.
0030E8	ENSIM CORP.
0030E9	GMA COMMUNICATION MANUFACT'G
0030EA	TeraForce Technology Corporation
0030EB	TURBONET COMMUNICATIONS, INC.
0030EC	Borgardt
0030ED	Expert Magnetics Corp.
0030EE	DSG Technology, Inc.
0030EF	NEON TECHNOLOGY, INC.
0030F0	Uniform Industrial Corp.
0030F1	Accton Technology Corp
0030F2	Cisco Systems, Inc
0030F3	At Work Computers
0030F4	STARDOT TECHNOLOGIES
0030F5	Wild Lab. Ltd.
0030F6	SECURELOGIX CORPORATION
0030F7	RAMIX INC.
0030F8	Dynapro Systems, Inc.
0030F9	Sollae Systems Co., Ltd.
0030FA	TELICA, INC.
0030FB	AZS Technology AG
0030FC	Terawave Communications, Inc.
0030FD	INTEGRATED SYSTEMS DESIGN
0030FE	DSA GmbH
0030FF	DataFab Systems Inc.
003146	Juniper Networks
00323A	So-Logic
00336C	SynapSense Corporation
0034DA	LG Electronics (Mobile Communications)
0034F1	Radicom Research, Inc.
0034FE	HUAWEI TECHNOLOGIES CO.,LTD
00351A	Cisco Systems, Inc
003532	Electro-               # Electro-Metrics Corporation
003560	Rosen Aviation
003676	ARRIS Group, Inc.
0036F8	Conti Temic microelectronic GmbH
0036FE	SuperVision
00376D	Murata Manufacturing Co., Ltd.
0037B7	Sagemcom Broadband SAS
0038DF	Cisco Systems, Inc
003A7D	Cisco Systems, Inc
003A98	Cisco Systems, Inc
003A99	Cisco Systems, Inc
003A9A	Cisco Systems, Inc
003A9B	Cisco Systems, Inc
003A9C	Cisco Systems, Inc
003A9D	NEC Platforms, Ltd.
003AAF	BlueBit Ltd.
003CC5	WONWOO Engineering Co., Ltd
003D41	Hatteland Computer AS
003EE1	Apple, Inc.
004000	PCI COMPONENTES DA AMZONIA LTD
004001	Zero One Technology Co Ltd (ZyXEL?)
004002	PERLE SYSTEMS LIMITED
004003	Emerson Process Management Power & Water Solutions, Inc.
004004	ICM CO. LTD.
004005	TRENDware International Inc.; Linksys; Simple Net; all three reported
004006	SAMPO TECHNOLOGY CORPORATION
004007	TELMAT INFORMATIQUE
004008	A PLUS INFO CORPORATION
004009	Tachibana Tectron Co Ltd
00400A	PIVOTAL TECHNOLOGIES, INC.
00400B	Cresc
00400C	General Micro Systems, Inc.
00400D	LANNET Data Communications
00400E	MEMOTEC, INC.
00400F	DATACOM TECHNOLOGIES
004010	Sonic				Mac Ethernet interfaces
004011	Facilities Andover Environmental Controllers
004012	WINDATA, INC.
004013	NTT Data Communication Systems Corp
004014	Comsoft Gmbh
004015	Ascom
004016	ADC - Global Connectivity Solutions Division
004017	XcdXjet-	# XCd XJet - HP printer server card
004018	ADOBE SYSTEMS, INC.
004019	AEON SYSTEMS, INC.
00401A	FUJI ELECTRIC CO., LTD.
00401B	PRINTER SYSTEMS CORP.
00401C	AST				Pentium/90 PC (emulating AMD EISA card)
00401D	INVISIBLE SOFTWARE, INC.
00401E	Icc
00401F	Colorgraph Ltd
004020	Pilkington Communication
004021	RASTER GRAPHICS
004022	KLEVER COMPUTERS, INC.
004023	Logic Corporation
004024	COMPAC INC.
004025	Molecular Dynamics
004026	Melco Inc
004027	SMC Massachusetts		[HadSigma (?), maybe the "S"?]
004028	Netcomm
004029	Compex
00402A	Canoga-Perkins
00402B	Trigem
00402C	ISIS DISTRIBUTED SYSTEMS, INC.
00402D	HARRIS ADACOM CORPORATION
00402E	PRECISION SOFTWARE, INC.
00402F	Xlnt Designs Inc (XDI)
004030	GK Computer
004031	KOKUSAI ELECTRIC CO., LTD
004032	Digital Communications
004033	Addtron Technology Co., Ltd.
004034	BUSTEK CORPORATION
004035	Opcom
004036	TribeStar
004037	SEA-ILAN, INC.
004038	TALENT ELECTRIC INCORPORATED
004039	Optec Daiichi Denko Co Ltd
00403A	IMPACT TECHNOLOGIES
00403B	SYNERJET INTERNATIONAL CORP.
00403C	Forks, Inc.
00403D	Teradata Corporation
00403E	RASTER OPS CORPORATION
00403F	SSANGYONG COMPUTER SYSTEMS
004040	RING ACCESS, INC.
004041	Fujikura Ltd.
004042	N.A.T. GMBH
004043	Nokia Data Communications
004044	QNIX COMPUTER CO., LTD.
004045	TWINHEAD CORPORATION
004046	UDC RESEARCH LIMITED
004047	WIND RIVER SYSTEMS
004048	SMD Informatica S.A.
004049	Roche Diagnostics International Ltd.
00404A	WEST AUSTRALIAN DEPARTMENT
00404B	MAPLE COMPUTER SYSTEMS
00404C	Hypertec Pty Ltd.
00404D	Telecomm Techniques
00404E	FLUENT, INC.
00404F	Space & Naval Warfare Systems
004050	Ironics, Incorporated
004051	GRACILIS, INC.
004052	Star Technologies Inc
004053	Datum [Bancomm Division]	TymServe 2000
004054	Thinking Machines Corporation
004055	METRONIX GMBH
004056	MCM JAPAN LTD.
004057	Lockheed-Sanders
004058	KRONOS, INC.
004059	Yoshida Kogyo K.K.
00405A	GOLDSTAR INFORMATION & COMM.
00405B	Funasset Limited
00405C	FUTURE SYSTEMS, INC.
00405D	Star-Tek Inc
00405E	NORTH HILLS ISRAEL
00405F	AFE COMPUTERS LTD.
004060	COMENDEC LTD
004061	DATATECH ENTERPRISES CO., LTD.
004062	E-SYSTEMS, INC./GARLAND DIV.
004063	VIA TECHNOLOGIES, INC.
004064	KLA INSTRUMENTS CORPORATION
004065	GTE SPACENET
004066	Hitachi Cable, Ltd.
004067	Omnibyte Corporation
004068	Extended Systems
004069	Lemcom Systems Inc
00406A	Kentek Information Systems Inc
00406B	Sysgen
00406C	COPERNIQUE
00406D	LANCO, INC.
00406E	Corollary, Inc.
00406F	Sync Research Inc
004070	INTERWARE CO., LTD.
004071	ATM COMPUTER GMBH
004072	Applied Innovation
004073	BASS ASSOCIATES
004074	Cable and Wireless
004075	Tattile SRL
004076	AMP Incorporated
004077	MAXTON TECHNOLOGY CORPORATION
004078	Wearnes Automation Pte Ltd
004079	JUKO MANUFACTURE COMPANY, LTD.
00407A	SOCIETE D'EXPLOITATION DU CNIT
00407B	SCIENTIFIC ATLANTA
00407C	QUME CORPORATION
00407D	EXTENSION TECHNOLOGY CORP.
00407E	EVERGREEN SYSTEMS, INC.
00407F	Agema Infrared Systems AB
004080	ATHENIX CORPORATION
004081	MANNESMANN SCANGRAPHIC GMBH
004082	Laboratory Equipment Corp
004083	TDA INDUSTRIA DE PRODUTOS
004084	HONEYWELL ACS
004085	SAAB Instruments AB
004086	Michels & Kleberhoff Computer
004087	Ubitrex Corporation
004088	Mobuis			NuBus (Mac) combination video/EtherTalk
004089	MEIDENSHA CORPORATION
00408A	TPS Teleprocessing Sys. Gmbh
00408B	RAYLAN CORPORATION
00408C	Axis Communications AB
00408D	THE GOODYEAR TIRE & RUBBER CO.
00408E	CXR/Digilog
00408F	WM-Data Minfo AB
004090	Ansel Communications	PC NE2000 compatible twisted-pair ethernet cards
004091	Procomp Industria Eletronica
004092	ASP Computer Products, Inc.
004093	PAXDATA NETWORKS LTD.
004094	Shographics Inc
004095	Eagle Technologies	[UMC also reported]
004096	Cisco Systems, Inc.
004097	DATEX DIVISION OF
004098	DRESSLER GMBH & CO.
004099	NEWGEN SYSTEMS CORP.
00409A	Network Express Inc
00409B	HAL COMPUTER SYSTEMS INC.
00409C	Transware
00409D	DigiBoard		Ethernet-ISDN bridges
00409E	Concurrent Technologies Ltd.
00409F	Lancast/	# Lancast/Casat Technology Inc
0040A0	GOLDSTAR CO., LTD.
0040A1	ERGO COMPUTING
0040A2	KINGSTAR TECHNOLOGY INC.
0040A3	MICROUNITY SYSTEMS ENGINEERING
0040A4	Rose Electronics
0040A5	CLINICOMP INTL.
0040A6	Cray Research Inc.
0040A7	ITAUTEC PHILCO S.A.
0040A8	IMF INTERNATIONAL LTD.
0040A9	DATACOM INC.
0040AA	Valmet Automation Inc
0040AB	ROLAND DG CORPORATION
0040AC	SUPER WORKSTATION, INC.
0040AD	SMA Regelsysteme Gmbh
0040AE	Delta Controls, Inc.
0040AF	Digital Products, Inc. (DPI).
0040B0	BYTEX CORPORATION, ENGINEERING
0040B1	CODONICS INC.
0040B2	SYSTEMFORSCHUNG
0040B3	ParTech Inc.
0040B4	3COM K.K.
0040B5	Video Technology Computers Ltd
0040B6	Computerm Corporation
0040B7	STEALTH COMPUTER SYSTEMS
0040B8	IDEA ASSOCIATES
0040B9	MACQ Electronique SA
0040BA	ALLIANT COMPUTER SYSTEMS CORP.
0040BB	GOLDSTAR CABLE CO., LTD.
0040BC	ALGORITHMICS LTD.
0040BD	Starlight Networks Inc
0040BE	BOEING DEFENSE & SPACE
0040BF	CHANNEL SYSTEMS INTERN'L INC.
0040C0	VISTA CONTROLS CORPORATION
0040C1	Bizerba-	# Bizerba-Werke Wilheim Kraut
0040C2	Applied Computing Devices
0040C3	Fischer and Porter Co.
0040C4	KINKEI SYSTEM CORPORATION
0040C5	Micom Communications Corp.
0040C6	Fibernet Research, Inc.
0040C7	Danpex Corporation
0040C8	Milan Technology Corp.
0040C9	Ncube
0040CA	FIRST INTERNAT'L COMPUTER, INC
0040CB	LANWAN TECHNOLOGIES
0040CC	Silcom Manufacturing Technology Inc
0040CD	TERA MICROSYSTEMS, INC.
0040CE	NET-SOURCE, INC.
0040CF	Strawberry Tree Inc
0040D0	DEC/Compaq
0040D1	FUKUDA DENSHI CO., LTD.
0040D2	Pagine Corporation
0040D3	KIMPSION INTERNATIONAL CORP.
0040D4	Gage Talker Corp.
0040D5	Sartorius Mechatronics T&H GmbH
0040D6	LOCAMATION B.V.
0040D7	Studio Gen Inc
0040D8	Ocean Office Automation Ltd
0040D9	AMERICAN MEGATRENDS INC.
0040DA	TELSPEC LTD
0040DB	ADVANCED TECHNICAL SOLUTIONS
0040DC	Tritec Electronic Gmbh
0040DD	HONG TECHNOLOGIES
0040DE	Elsag Datamat spa
0040DF	Digalog Systems, Inc.
0040E0	ATOMWIDE LTD.
0040E1	Marner International Inc
0040E2	Mesa Ridge Technologies Inc
0040E3	Quin Systems Ltd
0040E4	E-M TECHNOLOGY, INC.
0040E5	Sybus Corporation
0040E6	C.A.E.N.
0040E7	Arnos Instruments & Computer
0040E8	CHARLES RIVER DATA SYSTEMS,INC
0040E9	Accord Systems, Inc.
0040EA	PlainTree Systems Inc
0040EB	MARTIN MARIETTA CORPORATION
0040EC	MIKASA SYSTEM ENGINEERING
0040ED	Network Controls International Inc
0040EE	Optimem
0040EF	HYPERCOM, INC.
0040F0	Micro Systems Inc
0040F1	Chuo Electronics Co., Ltd.
0040F2	JANICH & KLASS COMPUTERTECHNIK
0040F3	Netcor
0040F4	Cameo Communications, Inc.
0040F5	OEM Engines
0040F6	Katron Computers Inc
0040F7	Polaroid Corporation
0040F8	SYSTEMHAUS DISCOM
0040F9	Combinet
0040FA	Microboards Inc
0040FB	Cascade Communications Corp.
0040FC	IBR COMPUTER TECHNIK GMBH
0040FD	Lxe
0040FE	SYMPLEX COMMUNICATIONS
0040FF	Telebit Corporation		Personal NetBlazer
0041B4	Wuxi Zhongxing Optoelectronics Technology Co.,Ltd.
0041D2	Cisco Systems, Inc
004252	RLX Technologies
00425A	Cisco Systems, Inc
004268	Cisco Systems, Inc
0043FF	KETRON S.R.L.
004501	Versus Technology, Inc.
00464B	HUAWEI TECHNOLOGIES CO.,LTD
004854	Digital SemiConductor		21143/2 based 10/100
004A77	zte corporation
004BF3	SHENZHEN MERCURY COMMUNICATION TECHNOLOGIES CO.,LTD.
004D32	Andon Health Co.,Ltd.
004F49	Realtek
004F4B	Pine Technology Ltd.
005000	NEXO COMMUNICATIONS, INC.
005001	YAMASHITA SYSTEMS CORP.
005002	OMNISEC AG
005003	Xrite Inc
005004	3com				3C90X
005006	TAC AB
005007	SIEMENS TELECOMMUNICATION SYSTEMS LIMITED
005008	TIVA MICROCOMPUTER CORP. (TMC)
005009	PHILIPS BROADBAND NETWORKS
00500A	IRIS TECHNOLOGIES, INC.
00500B	Cisco Systems, Inc
00500C	e-Tek Labs, Inc.
00500D	SATORI ELECTORIC CO., LTD.
00500E	CHROMATIS NETWORKS, INC.
00500F	Cisco
005010	NovaNET Learning, Inc.
005012	Cbl-                   # CBL - GMBH
005013	Chaparral Network Storage
005014	Cisco Systems, Inc
005015	BRIGHT STAR ENGINEERING
005016	Molex Canada Ltd
005017	RSR S.R.L.
005018	AMIT, Inc.
005019	SPRING TIDE NETWORKS, INC.
00501A	IQinVision
00501B	ABL CANADA, INC.
00501C	JATOM SYSTEMS, INC.
00501E	Grass Valley, A Belden Brand
00501F	MRG SYSTEMS, LTD.
005020	MEDIASTAR CO., LTD.
005021	EIS INTERNATIONAL, INC.
005022	ZONET TECHNOLOGY, INC.
005023	PG DESIGN ELECTRONICS, INC.
005024	NAVIC SYSTEMS, INC.
005026	COSYSTEMS, INC.
005027	GENICOM CORPORATION
005028	AVAL COMMUNICATIONS
005029	1394 PRINTER WORKING GROUP
00502A	Cisco Systems, Inc
00502B	GENRAD LTD.
00502C	SOYO COMPUTER, INC.
00502D	ACCEL, INC.
00502E	CAMBEX CORPORATION
00502F	TollBridge Technologies, Inc.
005030	FUTURE PLUS SYSTEMS
005031	AEROFLEX LABORATORIES, INC.
005032	PICAZO COMMUNICATIONS, INC.
005033	MAYAN NETWORKS
005036	NETCAM, LTD.
005037	KOGA ELECTRONICS CO.
005038	DAIN TELECOM CO., LTD.
005039	MARINER NETWORKS
00503A	DATONG ELECTRONICS LTD.
00503B	MEDIAFIRE CORPORATION
00503C	TSINGHUA NOVEL ELECTRONICS
00503E	Cisco Systems, Inc
00503F	ANCHOR GAMES
005040	Panasonic Electric Works Co., Ltd.
005041	Coretronic Corporation
005042	SCI MANUFACTURING SINGAPORE PTE, LTD.
005043	MARVELL SEMICONDUCTOR, INC.
005044	ASACA CORPORATION
005045	RIOWORKS SOLUTIONS, INC.
005046	MENICX INTERNATIONAL CO., LTD.
005047	Private
005048	INFOLIBRIA
005049	Arbor Networks Inc
00504A	ELTECO A.S.
00504B	BARCONET N.V.
00504C	Galil Motion Control
00504D	Repotec Group
00504E	UMC				UM9008 NE2000-compatible ISA Card for PC
00504F	OLENCOM ELECTRONICS
005050	Cisco
005051	IWATSU ELECTRIC CO., LTD.
005052	TIARA NETWORKS, INC.
005053	Cisco Systems, Inc
005054	Cisco Systems, Inc
005055	DOMS A/S
005056	VMware, Inc.
005057	BROADBAND ACCESS SYSTEMS
005058	Sangoma Technologies
005059	Ibahn
00505A	NETWORK ALCHEMY, INC.
00505B	KAWASAKI LSI U.S.A., INC.
00505C	TUNDO CORPORATION
00505E	DIGITEK MICROLOGIC S.A.
00505F	BRAND INNOVATORS
005060	TANDBERG TELECOM AS
005062	KOUWELL ELECTRONICS CORP.  **
005063	OY COMSEL SYSTEM AB
005064	CAE ELECTRONICS
005065	TDK-Lambda Corporation
005066	AtecoM GmbH advanced telecomunication modules
005067	AEROCOMM, INC.
005068	ELECTRONIC INDUSTRIES ASSOCIATION
005069	PixStream Incorporated
00506A	EDEVA, INC.
00506B	Spx-Ateg
00506C	Beijer Electronics Products AB
00506D	VIDEOJET SYSTEMS
00506E	CORDER ENGINEERING CORPORATION
00506F	G-CONNECT
005070	CHAINTECH COMPUTER CO., LTD.
005071	AIWA CO., LTD.
005072	CORVIS CORPORATION
005073	Cisco Systems, Inc
005074	ADVANCED HI-TECH CORP.
005075	KESTREL SOLUTIONS
005076	IBM Corp
005077	PROLIFIC TECHNOLOGY, INC.
005078	MEGATON HOUSE, LTD.
005079	Private
00507A	XPEED, INC.
00507B	MERLOT COMMUNICATIONS
00507C	VIDEOCON AG
00507D	Ifp
00507E	NEWER TECHNOLOGY
00507F	DrayTek Corp.
005080	Cisco Systems, Inc
005081	MURATA MACHINERY, LTD.
005082	FORESSON CORPORATION
005083	GILBARCO, INC.
005084	ATL PRODUCTS
005086	TELKOM SA, LTD.
005087	TERASAKI ELECTRIC CO., LTD.
005088	AMANO CORPORATION
005089	SAFETY MANAGEMENT SYSTEMS
00508B	Hewlett Packard
00508C	RSI SYSTEMS
00508D	ABIT COMPUTER CORPORATION
00508E	OPTIMATION, INC.
00508F	ASITA TECHNOLOGIES INT'L LTD.
005090	Dctri
005091	NETACCESS, INC.
005092	Rigaku Corporation Osaka Plant
005093	Boeing
005094	ARRIS Group, Inc.
005095	PERACOM NETWORKS
005096	SALIX TECHNOLOGIES, INC.
005097	MMC-EMBEDDED COMPUTERTECHNIK GmbH
005098	GLOBALOOP, LTD.
005099	3COM EUROPE, LTD.
00509A	TAG ELECTRONIC SYSTEMS
00509B	SWITCHCORE AB
00509C	BETA RESEARCH
00509D	THE INDUSTREE B.V.
00509E	Les Technologies SoftAcoustik Inc.
00509F	HORIZON COMPUTER
0050A0	DELTA COMPUTER SYSTEMS, INC.
0050A1	CARLO GAVAZZI, INC.
0050A2	Cisco Systems, Inc
0050A3	TransMedia Communications, Inc.
0050A4	IO TECH, INC.
0050A5	CAPITOL BUSINESS SYSTEMS, LTD.
0050A6	OPTRONICS
0050A7	Cisco Systems, Inc
0050A8	OpenCon Systems, Inc.
0050A9	MOLDAT WIRELESS TECHNOLGIES
0050AA	KONICA MINOLTA HOLDINGS, INC.
0050AB	NALTEC, Inc.
0050AC	MAPLE COMPUTER CORPORATION
0050AD	CommUnique Wireless Corp.
0050AE	FDK Co., Ltd
0050AF	INTERGON, INC.
0050B0	TECHNOLOGY ATLANTA CORPORATION
0050B1	GIDDINGS & LEWIS
0050B2	BRODEL GmbH
0050B3	VOICEBOARD CORPORATION
0050B4	SATCHWELL CONTROL SYSTEMS, LTD
0050B5	FICHET-BAUCHE
0050B6	GOOD WAY IND. CO., LTD.
0050B7	BOSER TECHNOLOGY CO., LTD.
0050B8	INOVA COMPUTERS GMBH & CO. KG
0050B9	XITRON TECHNOLOGIES, INC.
0050BA	D-Link Corporation
0050BB	CMS TECHNOLOGIES
0050BC	HAMMER STORAGE SOLUTIONS
0050BD	Cisco
0050BE	FAST MULTIMEDIA AG
0050BF	Metalligence Technology Corp.
0050C0	GATAN, INC.
0050C1	GEMFLEX NETWORKS, LTD.
0050C2	IEEE Registration Authority
0050C4	Imd
0050C5	ADS Technologies, Inc
0050C6	LOOP TELECOMMUNICATION INTERNATIONAL, INC.
0050C7	Private
0050C8	Addonics Technologies, Inc.
0050C9	MASPRO DENKOH CORP.
0050CA	NET TO NET TECHNOLOGIES
0050CB	Jetter
0050CC	Xyratex
0050CD	DIGIANSWER A/S
0050CE	LG INTERNATIONAL CORP.
0050CF	VANLINK COMMUNICATION TECHNOLOGY RESEARCH INSTITUTE
0050D0	MINERVA SYSTEMS
0050D1	Cisco Systems, Inc
0050D2	CMC Electronics Inc
0050D3	DIGITAL AUDIO PROCESSING PTY. LTD.
0050D4	JOOHONG INFORMATION &
0050D5	AD SYSTEMS CORP.
0050D6	ATLAS COPCO TOOLS AB
0050D7	Telstrat
0050D8	UNICORN COMPUTER CORP.
0050D9	ENGETRON-ENGENHARIA ELETRONICA IND. e COM. LTDA
0050DA	3COM CORPORATION
0050DB	CONTEMPORARY CONTROL
0050DC	TAS TELEFONBAU A. SCHWABE GMBH & CO. KG
0050DD	SERRA SOLDADURA, S.A.
0050DE	SIGNUM SYSTEMS CORP.
0050DF	AirFiber, Inc.
0050E1	NS TECH ELECTRONICS SDN BHD
0050E2	Cisco
0050E3	ARRIS Group, Inc.
0050E4	Apple, Inc.
0050E6	HAKUSAN CORPORATION
0050E7	PARADISE INNOVATIONS (ASIA)
0050E8	NOMADIX INC.
0050EA	XEL COMMUNICATIONS, INC.
0050EB	ALPHA-TOP CORPORATION
0050EC	OLICOM A/S
0050ED	ANDA NETWORKS
0050EE	TEK DIGITEL CORPORATION
0050EF	SPE Systemhaus GmbH
0050F0	Cisco Systems, Inc
0050F1	Intel Corporation
0050F2	MICROSOFT CORP.
0050F3	GLOBAL NET INFORMATION CO., Ltd.
0050F4	SIGMATEK GMBH & CO. KG
0050F6	PAN-INTERNATIONAL INDUSTRIAL CORP.
0050F7	VENTURE MANUFACTURING (SINGAPORE) LTD.
0050F8	ENTREGA TECHNOLOGIES, INC.
0050F9	Sensormatic Electronics LLC
0050FA	OXTEL, LTD.
0050FB	VSK ELECTRONICS
0050FC	Edimax Technology Co. Ltd.
0050FD	VISIONCOMM CO., LTD.
0050FE	PCTVnet ASA
0050FF	HAKKO ELECTRONICS CO., LTD.
005218	Wuxi Keboda Electron Co.Ltd
00549F	Avaya Inc
0054AF	Continental Automotive Systems Inc.
0054BD	Swelaser AB
005500	Xerox
0055DA	IEEE Registration Authority
00562B	Cisco Systems, Inc
0056CD	Apple, Inc.
0057D2	Cisco Systems, Inc
005907	LenovoEMC Products USA, LLC
005979	Networked Energy Services
0059AC	KPN. B.V.
0059DC	Cisco Systems, Inc
005A13	HUAWEI TECHNOLOGIES CO.,LTD
005A39	SHENZHEN FAST TECHNOLOGIES CO.,LTD
005BA1	shanghai huayuan chuangxin software CO., LTD.
005CB1	Gospell DIGITAL TECHNOLOGY CO., LTD
005D03	Xilinx, Inc
005F86	Cisco Systems, Inc
006000	XYCOM INC.
006001	InnoSys, Inc.
006002	SCREEN SUBTITLING SYSTEMS, LTD
006003	TERAOKA WEIGH SYSTEM PTE, LTD.
006004	COMPUTADORES MODULARES SA
006005	FEEDBACK DATA LTD.
006006	SOTEC CO., LTD
006007	ACRES GAMING, INC.
006008	3Com				3Com PCI form factor 3C905 TX board
006009	Cisco				Catalyst 5000 Ethernet switch
00600A	SORD COMPUTER CORPORATION
00600B	LOGWARE GmbH
00600C	Eurotech Inc.
00600D	Digital Logic GmbH
00600E	WAVENET INTERNATIONAL, INC.
00600F	Westell Technologies Inc.
006010	NETWORK MACHINES, INC.
006011	CRYSTAL SEMICONDUCTOR CORP.
006012	POWER COMPUTING CORPORATION
006013	NETSTAL MASCHINEN AG
006014	EDEC CO., LTD.
006015	NET2NET CORPORATION
006016	Clariion
006017	TOKIMEC INC.
006018	STELLAR ONE CORPORATION
006019	Roche Diagnostics
00601A	KEITHLEY INSTRUMENTS
00601B	MESA ELECTRONICS
00601C	TELXON CORPORATION
00601D	LUCENT TECHNOLOGIES
00601E	SOFTLAB, INC.
00601F	STALLION TECHNOLOGIES
006020	PIVOTAL NETWORKING, INC.
006021	DSC CORPORATION
006022	VICOM SYSTEMS, INC.
006023	PERICOM SEMICONDUCTOR CORP.
006024	GRADIENT TECHNOLOGIES, INC.
006025	Active Imaging Inc.
006026	VIKING Modular Solutions
006027	Superior Modular Products
006028	MACROVISION CORPORATION
006029	CARY PERIPHERALS INC.
00602A	SYMICRON COMPUTER COMMUNICATIONS, LTD.
00602B	PEAK AUDIO
00602C	LINX Data Terminals, Inc.
00602D	ALERTON TECHNOLOGIES, INC.
00602E	CYCLADES CORPORATION
00602F	Cisco
006030	VillageTronic			used on Amiga
006031	HRK SYSTEMS
006032	I-CUBE, INC.
006033	ACUITY IMAGING, INC.
006034	ROBERT BOSCH GmbH
006035	DALLAS SEMICONDUCTOR, INC.
006036	AIT Austrian Institute of Technology GmbH
006037	NXP Semiconductors
006038	Nortel Networks
006039	SanCom Technology, Inc.
00603A	QUICK CONTROLS LTD.
00603B	AMTEC spa
00603C	HAGIWARA SYS-COM CO., LTD.
00603D	3cx
00603E	Cisco				100Mbps interface
00603F	PATAPSCO DESIGNS
006040	NETRO CORP.
006041	Yokogawa Digital Computer Corporation
006042	TKS (USA), INC.
006043	iDirect, INC.
006044	LITTON/POLY-SCIENTIFIC
006045	PATHLIGHT TECHNOLOGIES
006046	VMETRO, INC.
006047	Cisco
006048	EMC CORPORATION
006049	VINA TECHNOLOGIES
00604A	SAIC IDEAS GROUP
00604B	Safe-com GmbH & Co. KG
00604C	Sagemcom Broadband SAS
00604D	MMC NETWORKS, INC.
00604E	Cycle Computer (Sun MotherBoard Replacements)
00604F	Tattile SRL
006050	INTERNIX INC.
006051	QUALITY SEMICONDUCTOR
006052	Realtek				(RTL 8029 == PCI NE2000)
006053	TOYODA MACHINE WORKS, LTD.
006054	CONTROLWARE GMBH
006055	CORNELL UNIVERSITY
006056	NETWORK TOOLS, INC.
006057	Murata Manufacturing Co., Ltd.
006058	COPPER MOUNTAIN COMMUNICATIONS, INC.
006059	TECHNICAL COMMUNICATIONS CORP.
00605A	CELCORE, INC.
00605B	IntraServer Technology, Inc.
00605C	Cisco
00605D	SCANIVALVE CORP.
00605E	LIBERTY TECHNOLOGY NETWORKING
00605F	NIPPON UNISOFT CORPORATION
006060	Data Innovations North America
006061	WHISTLE COMMUNICATIONS CORP.
006062	TELESYNC, INC.
006063	PSION DACOM PLC.
006064	NETCOMM LIMITED
006065	BERNECKER & RAINER INDUSTRIE-ELEKTRONIC GmbH
006066	LACROIX Trafic
006067	Acer Lan
006068	Dialogic Corporation
006069	Brocade Communications Systems, Inc.
00606A	MITSUBISHI WIRELESS COMMUNICATIONS. INC.
00606B	Synclayer Inc.
00606C	Arescom
00606D	DIGITAL EQUIPMENT CORP.
00606E	DAVICOM SEMICONDUCTOR, INC.
00606F	CLARION CORPORATION OF AMERICA
006070	Cisco				routers (2524 and 4500)
006071	MIDAS LAB, INC.
006072	VXL INSTRUMENTS, LIMITED
006073	REDCREEK COMMUNICATIONS, INC.
006074	QSC LLC
006075	PENTEK, INC.
006076	SCHLUMBERGER TECHNOLOGIES RETAIL PETROLEUM SYSTEMS
006077	PRISA NETWORKS
006078	POWER MEASUREMENT LTD.
006079	Mainstream Data, Inc.
00607A	DVS GMBH
00607B	FORE SYSTEMS, INC.
00607C	WaveAccess, Ltd.
00607D	SENTIENT NETWORKS INC.
00607E	GIGALABS, INC.
00607F	AURORA TECHNOLOGIES, INC.
006080	MICROTRONIX DATACOM LTD.
006081	TV/COM INTERNATIONAL
006082	NOVALINK TECHNOLOGIES, INC.
006083	Cisco Systems, Inc.		3620/3640 routers
006084	DIGITAL VIDEO
006085	Storage Concepts
006086	LOGIC REPLACEMENT TECH. LTD.
006087	KANSAI ELECTRIC CO., LTD.
006088	WHITE MOUNTAIN DSP, INC.
006089	Xata
00608A	CITADEL COMPUTER
00608B	ConferTech International
00608C	3Com (1990 onwards)
00608D	UNIPULSE CORP.
00608E	HE ELECTRONICS, TECHNOLOGIE & SYSTEMTECHNIK GmbH
00608F	TEKRAM TECHNOLOGY CO., LTD.
006090	Artiza Networks Inc
006091	FIRST PACIFIC NETWORKS, INC.
006092	MICRO/SYS, INC.
006093	Varian
006094	AMD PCNET PCI
006095	ACCU-TIME SYSTEMS, INC.
006096	T.S. MICROTECH INC.
006097	3com
006098	HT COMMUNICATIONS
006099	SBE, Inc.
00609A	NJK TECHNO CO.
00609B	AstroNova, Inc
00609C	Perkin-Elmer Incorporated
00609D	PMI FOOD EQUIPMENT GROUP
00609E	ASC X3 - INFORMATION TECHNOLOGY STANDARDS SECRETARIATS
00609F	PHAST CORPORATION
0060A0	SWITCHED NETWORK TECHNOLOGIES, INC.
0060A1	VPNet, Inc.
0060A2	NIHON UNISYS LIMITED CO.
0060A3	CONTINUUM TECHNOLOGY CORP.
0060A4	GEW Technologies (PTY)Ltd
0060A5	PERFORMANCE TELECOM CORP.
0060A6	PARTICLE MEASURING SYSTEMS
0060A7	MICROSENS GmbH & CO. KG
0060A8	TIDOMAT AB
0060A9	GESYTEC MBH
0060AA	INTELLIGENT DEVICES INC. (IDI)
0060AB	LARSCOM INCORPORATED
0060AC	RESILIENCE CORPORATION
0060AD	MegaChips Corporation
0060AE	TRIO INFORMATION SYSTEMS AB
0060AF	PACIFIC MICRO DATA, INC.
0060B0	HP
0060B1	Input/Output, Inc.
0060B2	PROCESS CONTROL CORP.
0060B3	Z-COM, INC.
0060B4	GLENAYRE R&D INC.
0060B5	KEBA GmbH
0060B6	LAND COMPUTER CO., LTD.
0060B7	CHANNELMATIC, INC.
0060B8	CORELIS Inc.
0060B9	NEC Platforms, Ltd
0060BA	SAHARA NETWORKS, INC.
0060BB	Cabletron Systems, Inc.
0060BC	KeunYoung Electronics & Communication Co., Ltd.
0060BD	Enginuity Communications
0060BE	WEBTRONICS
0060BF	MACRAIGOR SYSTEMS, INC.
0060C0	Nera Networks AS
0060C1	WaveSpan Corporation
0060C2	MPL AG
0060C3	NETVISION CORPORATION
0060C4	SOLITON SYSTEMS K.K.
0060C5	ANCOT CORP.
0060C6	DCS AG
0060C7	AMATI COMMUNICATIONS CORP.
0060C8	KUKA WELDING SYSTEMS & ROBOTS
0060C9	ControlNet, Inc.
0060CA	HARMONIC SYSTEMS INCORPORATED
0060CB	HITACHI ZOSEN CORPORATION
0060CC	EMTRAK, INCORPORATED
0060CD	VideoServer, Inc.
0060CE	ACCLAIM COMMUNICATIONS
0060CF	ALTEON NETWORKS, INC.
0060D0	SNMP RESEARCH INCORPORATED
0060D1	CASCADE COMMUNICATIONS
0060D2	LUCENT TECHNOLOGIES TAIWAN TELECOMMUNICATIONS CO., LTD.
0060D3	At&T
0060D4	ELDAT COMMUNICATION LTD.
0060D5	AMADA MIYACHI Co., Ltd
0060D6	NovAtel Inc.
0060D7	ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE (EPFL)
0060D8	ELMIC SYSTEMS, INC.
0060D9	TRANSYS NETWORKS INC.
0060DA	Red Lion Controls, LP
0060DB	NTP ELEKTRONIK A/S
0060DC	NEC Magnus Communications,Ltd.
0060DD	MYRICOM, INC.
0060DE	Kayser-Threde GmbH
0060DF	Brocade Communications Systems, Inc.
0060E0	AXIOM TECHNOLOGY CO., LTD.
0060E1	ORCKIT COMMUNICATIONS LTD.
0060E2	QUEST ENGINEERING & DEVELOPMENT
0060E3	ARBIN INSTRUMENTS
0060E4	COMPUSERVE, INC.
0060E5	FUJI AUTOMATION CO., LTD.
0060E6	SHOMITI SYSTEMS INCORPORATED
0060E7	Randata
0060E8	HITACHI COMPUTER PRODUCTS (AMERICA), INC.
0060E9	ATOP TECHNOLOGIES, INC.
0060EA	StreamLogic
0060EB	FOURTHTRACK SYSTEMS
0060EC	HERMARY OPTO ELECTRONICS INC.
0060ED	RICARDO TEST AUTOMATION LTD.
0060EE	Apollo
0060EF	FLYTECH TECHNOLOGY CO., LTD.
0060F0	JOHNSON & JOHNSON MEDICAL, INC
0060F1	EXP COMPUTER, INC.
0060F2	LASERGRAPHICS, INC.
0060F3	Performance Analysis Broadband, Spirent plc
0060F4	ADVANCED COMPUTER SOLUTIONS, Inc.
0060F5	Phobos FastEthernet for Unix WS
0060F6	NEXTEST COMMUNICATIONS PRODUCTS, INC.
0060F7	DATAFUSION SYSTEMS
0060F8	Loran International Technologies Inc.
0060F9	DIAMOND LANE COMMUNICATIONS
0060FA	EDUCATIONAL TECHNOLOGY RESOURCES, INC.
0060FB	PACKETEER, INC.
0060FC	CONSERVATION THROUGH INNOVATION LTD.
0060FD	NetICs, Inc.
0060FE	LYNX SYSTEM DEVELOPERS, INC.
0060FF	QuVis, Inc.
006171	Apple, Inc.
0062EC	Cisco Systems, Inc
006440	Cisco Systems, Inc
0064A6	Maquet CardioVascular
00664B	HUAWEI TECHNOLOGIES CO.,LTD
006B8E	Shanghai Feixun Communication Co.,Ltd.
006B9E	Vizio, Inc
006BA0	SHENZHEN UNIVERSAL INTELLISYS PTE LTD
006BF1	Cisco Systems, Inc
006CBC	Cisco Systems, Inc
006CFD	Sichuan Changhong Electric Ltd.
006D52	Apple, Inc.
006DFB	Vutrix Technologies Ltd
006F64	Samsung Electronics Co.,Ltd
0070B0	M/A-COM INC. COMPANIES
0070B3	DATA RECALL LTD.
0071C2	PEGATRON CORPORATION
0071CC	Hon Hai Precision Ind. Co.,Ltd.
00738D	Shenzhen TINNO Mobile Technology Corp.
0073E0	Samsung Electronics Co.,Ltd
00749C	Ruijie Networks Co.,LTD
007532	INID BV
0075E1	Ampt, LLC
007686	Cisco Systems, Inc
007888	Cisco Systems, Inc
00789E	Sagemcom Broadband SAS
0078CD	Ignition Design Labs
007B18	SENTRY Co., LTD.
007DFA	Volkswagen Group of America
007E56	China Dragon Technology Limited
007F28	Actiontec Electronics, Inc
008000	Multitech Systems Inc
008001	Periphonics Corporation
008002	SATELCOM (UK) LTD
008003	HYTEC ELECTRONICS LTD.
008004	Antlow Computers, Ltd.
008005	Cactus Computer Inc.
008006	Compuadd Corporation
008007	Dlog NC-Systeme
008008	DYNATECH COMPUTER SYSTEMS
008009	Jupiter Systems (older MX-600 series machines)
00800A	JAPAN COMPUTER CORP.
00800B	CSK CORPORATION
00800C	VIDECOM LIMITED
00800D	Vosswinkel FU
00800E	ATLANTIX CORPORATION
00800F	SMC
008010	Commodore
008011	DIGITAL SYSTEMS INT'L. INC.
008012	IMS Corp.			IMS failure analysis tester
008013	Thomas Conrad Corp.
008014	ESPRIT SYSTEMS
008015	Seiko Systems Inc
008016	Wandel & Goltermann
008017	Pfu
008018	KOBE STEEL, LTD.
008019	Dayna Communications		"Etherprint" product
00801A	Bell Atlantic
00801B	Kodiak Technology
00801C	NEWPORT SYSTEMS SOLUTIONS
00801D	INTEGRATED INFERENCE MACHINES
00801E	XINETRON, INC.
00801F	KRUPP ATLAS ELECTRONIK GMBH
008020	NETWORK PRODUCTS
008021	Newbridge Networks Corporation
008022	SCAN-OPTICS
008023	Integrated Business Networks
008024	Kalpana
008025	Telit Wireless Solutions GmbH
008026	Network Products Corporation
008027	ADAPTIVE SYSTEMS, INC.
008028	TRADPOST (HK) LTD
008029	Microdyne Corporation
00802A	Test Systems & Simulations Inc
00802B	INTEGRATED MARKETING CO
00802C	The Sage Group PLC
00802D	Xylogics, Inc.			Annex terminal servers
00802E	Plexcom, Inc.
00802F	NATIONAL INSTRUMENTS CORP.
008030	NEXUS ELECTRONICS
008031	BASYS, CORP.
008032	ACCESS CO., LTD.
008033	Formation (?)
008034	SMT-Goupil
008035	Technology Works
008036	REFLEX MANUFACTURING SYSTEMS
008037	Ericsson Business Comm.
008038	Data Research & Applications
008039	ALCATEL STC AUSTRALIA
00803A	VARITYPER, INC.
00803B	APT Communications, Inc.
00803C	TVS ELECTRONICS LTD
00803D	Surigiken Co Ltd
00803E	Synernetics
00803F	Hyundai Electronics
008040	JOHN FLUKE MANUFACTURING CO.
008041	VEB KOMBINAT ROBOTRON
008042	Force Computers
008043	Networld Inc
008044	SYSTECH COMPUTER CORP.
008045	Matsushita Electric Ind Co
008046	University of Toronto
008047	IN-NET CORP.
008048	Compex, used by Commodore and DEC at least
008049	Nissin Electric Co Ltd
00804A	Pro-Log
00804B	EAGLE TECHNOLOGIES PTY.LTD.
00804C	Contec Co., Ltd.
00804D	Cyclone Microsystems, Inc.
00804E	APEX COMPUTER COMPANY
00804F	DAIKIN INDUSTRIES, LTD.
008050	ZIATECH CORPORATION
008051	ADC Fibermux
008052	Network Professor
008053	INTELLICOM, INC.
008054	FRONTIER TECHNOLOGIES CORP.
008055	Fermilab
008056	SPHINX Electronics GmbH & Co KG
008057	Adsoft Ltd
008058	PRINTER SYSTEMS CORP.
008059	STANLEY ELECTRIC CO., LTD
00805A	Tulip Computers International BV
00805B	Condor Systems, Inc.
00805C	Agilis?		# Agilis(?)
00805D	Canstar
00805E	LSI LOGIC CORPORATION
00805F	Compaq Computer Corporation
008060	Network Interface Corporation
008061	LITTON SYSTEMS, INC.
008062	Interface Co.
008063	Richard Hirschmann Gmbh & Co
008064	Wyse
008065	CYBERGRAPHIC SYSTEMS PTY LTD.
008066	ARCOM CONTROL SYSTEMS, LTD.
008067	Square D Company
008068	YAMATECH SCIENTIFIC LTD.
008069	Computone Systems
00806A	ERI (Empac Research Inc.)
00806B	Schmid Telecommunication
00806C	Cegelec Projects Ltd
00806D	Century Systems Corp.
00806E	Nippon Steel Corporation
00806F	Onelan Ltd
008070	COMPUTADORAS MICRON
008071	SAI Technology
008072	Microplex Systems Ltd
008073	DWB ASSOCIATES
008074	Fisher Controls
008075	PARSYTEC GMBH
008076	Mcnc
008077	Brother industries, LTD.
008078	PRACTICAL PERIPHERALS, INC.
008079	Microbus Designs Ltd
00807A	AITECH SYSTEMS LTD.
00807B	Artel Communications Corp.
00807C	Fibercom
00807D	Equinox Systems Inc
00807E	SOUTHERN PACIFIC LTD.
00807F	DY-4 INCORPORATED
008080	DATAMEDIA CORPORATION
008081	KENDALL SQUARE RESEARCH CORP.
008082	PEP Modular Computers Gmbh
008083	Amdahl
008084	THE CLOUD INC.
008085	H-THREE SYSTEMS CORPORATION
008086	Computer Generation Inc.
008087	Okidata
008088	VICTOR COMPANY OF JAPAN, LTD.
008089	TECNETICS (PTY) LTD.
00808A	Summit?		# Summit (?)
00808B	Dacoll Limited
00808C	Netscout Systems (formerly Frontier Software Development)
00808D	Westcove Technology BV
00808E	Radstone Technology
00808F	C. ITOH ELECTRONICS, INC.
008090	Microtek International Inc
008091	TOKYO ELECTRIC CO.,LTD
008092	Japan Computer Industry, Inc.
008093	Xyron Corporation
008094	Sattcontrol AB
008095	BASIC MERTON HANDELSGES.M.B.H.
008096	HDS
008097	CENTRALP AUTOMATISMES
008098	TDK Corporation
008099	Eaton Industries GmbH
00809A	Novus Networks Ltd
00809B	Justsystem Corporation
00809C	LUXCOM, INC.
00809D	Datacraft Manufactur'g Pty Ltd
00809E	DATUS GMBH
00809F	Alcatel Business Systems
0080A0	Hewlett Packard
0080A1	Microtest
0080A2	CREATIVE ELECTRONIC SYSTEMS
0080A3	Lantronix	(see also 0800A3)
0080A4	LIBERTY ELECTRONICS
0080A5	SPEED INTERNATIONAL
0080A6	Republic Technology Inc
0080A7	Measurex Corp
0080A8	VITACOM CORPORATION
0080A9	CLEARPOINT RESEARCH
0080AA	Maxpeed
0080AB	DUKANE NETWORK INTEGRATION
0080AC	IMLOGIX, DIVISION OF GENESYS
0080AD	Telebit
0080AE	Hughes Network Systems
0080AF	Allumer Co., Ltd.
0080B0	ADVANCED INFORMATION
0080B1	Softcom A/S
0080B2	NET (Network Equipment Technologies)
0080B3	AVAL DATA CORPORATION
0080B4	SOPHIA SYSTEMS
0080B5	UNITED NETWORKS INC.
0080B6	Themis corporation
0080B7	STELLAR COMPUTER
0080B8	DMG MORI B.U.G. CO., LTD.
0080B9	ARCHE TECHNOLIGIES INC.
0080BA	Specialix (Asia) Pte Ltd
0080BB	HUGHES LAN SYSTEMS
0080BC	HITACHI ENGINEERING CO., LTD
0080BD	THE FURUKAWA ELECTRIC CO., LTD
0080BE	ARIES RESEARCH
0080BF	TAKAOKA ELECTRIC MFG. CO. LTD.
0080C0	Penril Datability Networks
0080C1	LANEX CORPORATION
0080C2	IEEE				802.1 Committee
0080C3	BICC INFORMATION SYSTEMS & SVC
0080C4	DOCUMENT TECHNOLOGIES, INC.
0080C5	NOVELLCO DE MEXICO
0080C6	Soho
0080C7	Xircom, Inc.
0080C8	D-Link	(also Solectek Pocket Adapters, and LinkSys PCMCIA)
0080C9	Alberta Microelectronic Centre
0080CA	NETCOM RESEARCH INCORPORATED
0080CB	FALCO DATA PRODUCTS
0080CC	MICROWAVE BYPASS SYSTEMS
0080CD	MICRONICS COMPUTER, INC.
0080CE	Broadcast Television Systems
0080CF	EMBEDDED PERFORMANCE INC.
0080D0	Computer Products International
0080D1	KIMTRON CORPORATION
0080D2	SHINNIHONDENKO CO., LTD.
0080D3	Shiva				Appletalk-Ethernet interface
0080D4	Chase Limited
0080D5	CADRE TECHNOLOGIES
0080D6	Apple Mac Portable(?)
0080D7	Fantum Electronics
0080D8	Network Peripherals
0080D9	EMK Elektronik GmbH & Co. KG
0080DA	Bruel & Kjaer
0080DB	GRAPHON CORPORATION
0080DC	PICKER INTERNATIONAL
0080DD	GMX INC/GIMIX
0080DE	GIPSI S.A.
0080DF	ADC CODENOLL TECHNOLOGY CORP.
0080E0	XTP Systems Inc
0080E1	STMicroelectronics SRL
0080E2	T.D.I. CO., LTD.
0080E3	Coral?		# Coral (?)
0080E4	NORTHWEST DIGITAL SYSTEMS, INC
0080E5	Netapp
0080E6	PEER NETWORKS, INC.
0080E7	Lynwood Scientific Dev Ltd
0080E8	CUMULUS CORPORATIION
0080E9	Madge Ltd.
0080EA	The Fiber Company
0080EB	COMPCONTROL B.V.
0080EC	SUPERCOMPUTING SOLUTIONS, INC.
0080ED	IQ TECHNOLOGIES, INC.
0080EE	THOMSON CSF
0080EF	Rational
0080F0	Kyushu Matsushita Electric Co
0080F1	Opus
0080F2	RAYCOM SYSTEMS INC
0080F3	Sun Electronics Corp
0080F4	Telemechanique Electrique
0080F5	Quantel Ltd
0080F6	SYNERGY MICROSYSTEMS
0080F7	Zenith Communications Products
0080F8	MIZAR, INC.
0080F9	HEURIKON CORPORATION
0080FA	RWT GMBH
0080FB	BVM Limited
0080FC	AVATAR CORPORATION
0080FD	EXSCEED CORPRATION
0080FE	Azure Technologies Inc
0080FF	SOC. DE TELEINFORMATIQUE RTC
0081C4	Cisco Systems, Inc
0084ED	Private
0086A0	Private
008701	Samsung Electronics Co.,Ltd
008731	Cisco Systems, Inc
008865	Apple, Inc.
008A96	Cisco Systems, Inc
008B43	Rftech
008C10	Black Box Corp.
008C54	ADB Broadband Italia
008CFA	INVENTEC Corporation
008D4E	CJSC NII STT
008DDA	Link One Co., Ltd.
008E73	Cisco Systems, Inc
008EF2	Netgear
009000	DIAMOND MULTIMEDIA
009001	NISHIMU ELECTRONICS INDUSTRIES CO., LTD.
009002	ALLGON AB
009003	Aplio
009004	3com
009005	PROTECH SYSTEMS CO., LTD.
009006	Hamamatsu Photonics K.K.
009007	DOMEX TECHNOLOGY CORP.
009008	HanA Systems Inc.
009009	I Controls, Inc.
00900A	PROTON ELECTRONIC INDUSTRIAL CO., LTD.
00900B	LANNER ELECTRONICS, INC.
00900C	Cisco Systems, Inc
00900D	Overland Storage Inc.
00900E	HANDLINK TECHNOLOGIES, INC.
00900F	KAWASAKI HEAVY INDUSTRIES, LTD
009010	SIMULATION LABORATORIES, INC.
009011	WAVTrace, Inc.
009012	GLOBESPAN SEMICONDUCTOR, INC.
009013	SAMSAN CORP.
009014	ROTORK INSTRUMENTS, LTD.
009015	CENTIGRAM COMMUNICATIONS CORP.
009016	Zac
009017	Zypcom, Inc
009018	ITO ELECTRIC INDUSTRY CO, LTD.
009019	HERMES ELECTRONICS CO., LTD.
00901A	UNISPHERE SOLUTIONS
00901B	DIGITAL CONTROLS
00901C	mps Software Gmbh
00901D	PEC (NZ) LTD.
00901E	Selesta Ingegneria S.p.A.
00901F	ADTEC PRODUCTIONS, INC.
009020	PHILIPS ANALYTICAL X-RAY B.V.
009021	Cisco Systems, Inc
009022	Ivex
009023	ZILOG INC.
009024	PIPELINKS, INC.
009025	BAE Systems Australia (Electronic Systems) Pty Ltd
009026	ADVANCED SWITCHING COMMUNICATIONS, INC.
009027	Intel
009028	NIPPON SIGNAL CO., LTD.
009029	CRYPTO AG
00902A	COMMUNICATION DEVICES, INC.
00902B	Cisco				Ethernet Switches and Light Streams
00902C	DATA & CONTROL EQUIPMENT LTD.
00902D	DATA ELECTRONICS (AUST.) PTY, LTD.
00902E	NAMCO LIMITED
00902F	NETCORE SYSTEMS, INC.
009030	HONEYWELL-DATING
009031	MYSTICOM, LTD.
009032	PELCOMBE GROUP LTD.
009033	INNOVAPHONE AG
009034	IMAGIC, INC.
009035	ALPHA TELECOM, INC.
009036	ens, inc.
009037	ACUCOMM, INC.
009038	FOUNTAIN TECHNOLOGIES, INC.
009039	SHASTA NETWORKS
00903A	NIHON MEDIA TOOL INC.
00903B	TriEMS Research Lab, Inc.
00903C	ATLANTIC NETWORK SYSTEMS
00903D	BIOPAC SYSTEMS, INC.
00903E	N.V. PHILIPS INDUSTRIAL ACTIVITIES
00903F	AZTEC RADIOMEDIA
009040	Siemens Network Convergence LLC
009041	APPLIED DIGITAL ACCESS
009042	ECCS, Inc.
009043	Tattile SRL
009044	ASSURED DIGITAL, INC.
009045	Marconi Communications
009046	DEXDYNE, LTD.
009047	GIGA FAST E. LTD.
009048	ZEAL CORPORATION
009049	ENTRIDIA CORPORATION
00904A	CONCUR SYSTEM TECHNOLOGIES
00904B	Gemtek Technology Co., Ltd.
00904C	Epigram, Inc.
00904D	SPEC S.A.
00904E	DELEM BV
00904F	ABB POWER T&D COMPANY, INC.
009050	Teleste Corporation
009051	ULTIMATE TECHNOLOGY CORP.
009052	SELCOM ELETTRONICA S.R.L.
009053	DAEWOO ELECTRONICS CO., LTD.
009054	INNOVATIVE SEMICONDUCTORS, INC
009055	PARKER HANNIFIN CORPORATION COMPUMOTOR DIVISION
009056	TELESTREAM, INC.
009057	AANetcom, Inc.
009058	Ultra Electronics Command & Control Systems
009059	TELECOM DEVICE K.K.
00905A	DEARBORN GROUP, INC.
00905B	RAYMOND AND LAE ENGINEERING
00905C	Edmi
00905D	NETCOM SICHERHEITSTECHNIK GMBH
00905E	Rauland-               # RAULAND-BORG CORPORATION
00905F	Cisco Systems, Inc
009060	SYSTEM CREATE CORP.
009061	PACIFIC RESEARCH & ENGINEERING CORPORATION
009062	ICP VORTEX COMPUTERSYSTEME GmbH
009063	COHERENT COMMUNICATIONS SYSTEMS CORPORATION
009064	Thomson Inc.
009065	FINISAR CORPORATION
009066	Troika Networks, Inc.
009067	WalkAbout Computers, Inc.
009068	DVT CORP.
009069	Juniper Networks
00906A	TURNSTONE SYSTEMS, INC.
00906B	APPLIED RESOURCES, INC.
00906C	Sartorius Hamburg GmbH
00906D	Cisco Systems, Inc
00906E	PRAXON, INC.
00906F	Cisco Systems, Inc
009070	NEO NETWORKS, INC.
009071	Applied Innovation Inc.
009072	SIMRAD AS
009073	GAIO TECHNOLOGY
009074	ARGON NETWORKS, INC.
009075	NEC DO BRASIL S.A.
009076	FMT AIRCRAFT GATE SUPPORT SYSTEMS AB
009077	ADVANCED FIBRE COMMUNICATIONS
009078	MER TELEMANAGEMENT SOLUTIONS, LTD.
009079	ClearOne, Inc.
00907A	Spectralink, Inc
00907B	E-TECH, INC.
00907C	DIGITALCAST, INC.
00907D	Lake Communications
00907E	VETRONIX CORP.
00907F	WatchGuard Technologies, Inc.
009080	NOT LIMITED, INC.
009081	ALOHA NETWORKS, INC.
009082	FORCE INSTITUTE
009083	TURBO COMMUNICATION, INC.
009084	ATECH SYSTEM
009085	GOLDEN ENTERPRISES, INC.
009086	Cisco
009087	Itis
009088	BAXALL SECURITY LTD.
009089	SOFTCOM MICROSYSTEMS, INC.
00908A	BAYLY COMMUNICATIONS, INC.
00908B	Tattile SRL
00908C	ETREND ELECTRONICS, INC.
00908D	VICKERS ELECTRONICS SYSTEMS
00908E	Nortel Networks Broadband Access
00908F	AUDIO CODES LTD.
009090	I-Bus
009091	DigitalScape, Inc.
009092	Cisco
009093	NANAO CORPORATION
009094	OSPREY TECHNOLOGIES, INC.
009095	UNIVERSAL AVIONICS
009096	ASKEY COMPUTER CORP
009097	Sycamore Networks
009098	SBC DESIGNS, INC.
009099	ALLIED TELESIS, K.K.
00909A	ONE WORLD SYSTEMS, INC.
00909B	MARKEM-IMAJE
00909C	ARRIS Group, Inc.
00909D	NovaTech Process Solutions, LLC
00909E	Critical IO, LLC
00909F	DIGI-DATA CORPORATION
0090A0	8X8 INC.
0090A1	Flying Pig Systems/High End Systems Inc.
0090A2	CyberTAN Technology Inc.
0090A3	Corecess Inc.
0090A4	ALTIGA NETWORKS
0090A5	SPECTRA LOGIC
0090A6	Cisco Systems, Inc
0090A7	CLIENTEC CORPORATION
0090A8	NineTiles Networks, Ltd.
0090A9	WESTERN DIGITAL
0090AA	INDIGO ACTIVE VISION SYSTEMS LIMITED
0090AB	Cisco
0090AC	OPTIVISION, INC.
0090AD	ASPECT ELECTRONICS, INC.
0090AE	ITALTEL S.p.A/RF-UP-I
0090AF	J. MORITA MFG. CORP.
0090B0	Vadem
0090B1	Cisco
0090B2	AVICI SYSTEMS INC.
0090B3	AGRANAT SYSTEMS
0090B4	WILLOWBROOK TECHNOLOGIES
0090B5	NIKON CORPORATION
0090B6	FIBEX SYSTEMS
0090B7	DIGITAL LIGHTWAVE, INC.
0090B8	ROHDE & SCHWARZ GMBH & CO. KG
0090B9	BERAN INSTRUMENTS LTD.
0090BA	VALID NETWORKS, INC.
0090BB	TAINET COMMUNICATION SYSTEM Corp.
0090BC	TELEMANN CO., LTD.
0090BD	OMNIA COMMUNICATIONS, INC.
0090BE	IBC/INTEGRATED BUSINESS COMPUTERS
0090BF	Cisco Systems, Inc
0090C0	K.J. LAW ENGINEERS, INC.
0090C1	Peco II, Inc.
0090C2	JK microsystems, Inc.
0090C3	TOPIC SEMICONDUCTOR CORP.
0090C4	JAVELIN SYSTEMS, INC.
0090C5	INTERNET MAGIC, INC.
0090C6	OPTIM SYSTEMS, INC.
0090C7	ICOM INC.
0090C8	WAVERIDER COMMUNICATIONS (CANADA) INC.
0090C9	DPAC Technologies
0090CA	ACCORD VIDEO TELECOMMUNICATIONS, LTD.
0090CB	Wireless OnLine, Inc.
0090CC	PLANEX COMMUNICATIONS INC.
0090CD	ENT-EMPRESA NACIONAL DE TELECOMMUNICACOES, S.A.
0090CE	TETRA GmbH
0090CF	Nortel
0090D0	Thomson Telecom Belgium
0090D1	LEICHU ENTERPRISE CO., LTD.
0090D2	ARTEL VIDEO SYSTEMS
0090D3	GIESECKE & DEVRIENT GmbH
0090D4	BindView Development Corp.
0090D5	EUPHONIX, INC.
0090D6	Crystal Group, Inc.
0090D7	NetBoost Corp.
0090D8	WHITECROSS SYSTEMS
0090D9	Cisco Systems, Inc
0090DA	DYNARC, INC.
0090DB	NEXT LEVEL COMMUNICATIONS
0090DC	TECO INFORMATION SYSTEMS
0090DD	MIHARU COMMUNICATIONS Inc
0090DE	CARDKEY SYSTEMS, INC.
0090DF	MITSUBISHI CHEMICAL AMERICA, INC.
0090E0	SYSTRAN CORP.
0090E1	TELENA S.P.A.
0090E2	DISTRIBUTED PROCESSING TECHNOLOGY
0090E3	AVEX ELECTRONICS INC.
0090E4	NEC AMERICA, INC.
0090E5	TEKNEMA, INC.
0090E6	ALi Corporation
0090E7	HORSCH ELEKTRONIK AG
0090E8	MOXA TECHNOLOGIES CORP., LTD.
0090E9	JANZ COMPUTER AG
0090EA	ALPHA TECHNOLOGIES, INC.
0090EB	SENTRY TELECOM SYSTEMS
0090EC	Pyrescom
0090ED	CENTRAL SYSTEM RESEARCH CO., LTD.
0090EE	PERSONAL COMMUNICATIONS TECHNOLOGIES
0090EF	INTEGRIX, INC.
0090F0	Harmonic Video Systems Ltd.
0090F1	DOT HILL SYSTEMS CORPORATION
0090F2	Cisco				Ethernet Switches and Light Streams
0090F3	ASPECT COMMUNICATIONS
0090F4	LIGHTNING INSTRUMENTATION
0090F5	CLEVO CO.
0090F6	ESCALATE NETWORKS, INC.
0090F7	NBASE COMMUNICATIONS LTD.
0090F8	MEDIATRIX TELECOM
0090F9	Imagine Communications
0090FA	Emulex Corporation
0090FB	PORTWELL, INC.
0090FC	NETWORK COMPUTING DEVICES
0090FD	CopperCom, Inc.
0090FE	ELECOM CO., LTD.  (LANEED DIV.)
0090FF	TELLUS TECHNOLOGY INC.
0091D6	Crystal Group, Inc.
0091FA	Synapse Product Development
0092FA	SHENZHEN WISKY TECHNOLOGY CO.,LTD
009363	Uni-Link Technology Co., Ltd.
009569	LSD Science and Technology Co.,Ltd.
0097FF	Heimann Sensor GmbH
009ACD	HUAWEI TECHNOLOGIES CO.,LTD
009C02	Hewlett Packard
009D8E	CARDIAC RECORDERS, INC.
009E1E	Cisco Systems, Inc
009EC8	Xiaomi Communications Co Ltd
00A000	Bay Networks			Ethernet switch
00A001	DRS Signal Solutions
00A002	LEEDS & NORTHRUP AUSTRALIA PTY LTD
00A003	Siemens Switzerland Ltd., I B T HVP
00A004	NETPOWER, INC.
00A005	DANIEL INSTRUMENTS, LTD.
00A006	IMAGE DATA PROCESSING SYSTEM GROUP
00A007	APEXX TECHNOLOGY, INC.
00A008	Netcorp
00A009	WHITETREE NETWORK
00A00A	Airspan
00A00B	COMPUTEX CO., LTD.
00A00C	Kingmax Technology Inc.		PCMCIA card
00A00D	THE PANDA PROJECT
00A00E	NetScout Systems, Inc.
00A00F	Broadband Technologies
00A010	SYSLOGIC DATENTECHNIK AG
00A011	MUTOH INDUSTRIES LTD.
00A012	Telco Systems, Inc.
00A013	TELTREND LTD.
00A014	Csir
00A015	Wyle
00A016	MICROPOLIS CORP.
00A017	J B M CORPORATION
00A018	CREATIVE CONTROLLERS, INC.
00A019	NEBULA CONSULTANTS, INC.
00A01A	BINAR ELEKTRONIK AB
00A01B	PREMISYS COMMUNICATIONS, INC.
00A01C	NASCENT NETWORKS CORPORATION
00A01D	Red Lion Controls, LP
00A01E	EST CORPORATION
00A01F	TRICORD SYSTEMS, INC.
00A020	CITICORP/TTI
00A021	General Dynamics
00A022	CENTRE FOR DEVELOPMENT OF ADVANCED COMPUTING
00A023	APPLIED CREATIVE TECHNOLOGY, INC.
00A024	3com
00A025	REDCOM LABS INC.
00A026	TELDAT, S.A.
00A027	FIREPOWER SYSTEMS, INC.
00A028	CONNER PERIPHERALS
00A029	COULTER CORPORATION
00A02A	TRANCELL SYSTEMS
00A02B	TRANSITIONS RESEARCH CORP.
00A02C	interWAVE Communications
00A02D	1394 Trade Association
00A02E	BRAND COMMUNICATIONS, LTD.
00A02F	ADB Broadband Italia
00A030	CAPTOR NV/SA
00A031	HAZELTINE CORPORATION, MS 1-17
00A032	GES SINGAPORE PTE. LTD.
00A033	imc MeBsysteme GmbH
00A034	Axel
00A035	CYLINK CORPORATION
00A036	APPLIED NETWORK TECHNOLOGY
00A037	Mindray DS USA, Inc.
00A038	EMAIL ELECTRONICS
00A039	ROSS TECHNOLOGY, INC.
00A03A	KUBOTEK CORPORATION
00A03B	TOSHIN ELECTRIC CO., LTD.
00A03C	EG&G NUCLEAR INSTRUMENTS
00A03D	Opto-22
00A03E	ATM FORUM
00A03F	COMPUTER SOCIETY MICROPROCESSOR & MICROPROCESSOR STANDARDS C
00A040	Apple (PCI Mac)
00A041	Inficon
00A042	SPUR PRODUCTS CORP.
00A043	AMERICAN TECHNOLOGY LABS, INC.
00A044	NTT IT CO., LTD.
00A045	PHOENIX CONTACT Electronics GmbH
00A046	SCITEX CORP. LTD.
00A047	INTEGRATED FITNESS CORP.
00A048	QUESTECH, LTD.
00A049	DIGITECH INDUSTRIES, INC.
00A04A	NISSHIN ELECTRIC CO., LTD.
00A04B	Sonic Systems Inc.		EtherFE 10/100 PCI for Mac or PC
00A04C	INNOVATIVE SYSTEMS & TECHNOLOGIES, INC.
00A04D	EDA INSTRUMENTS, INC.
00A04E	VOELKER TECHNOLOGIES, INC.
00A04F	AMERITEC CORP.
00A050	CYPRESS SEMICONDUCTOR
00A051	ANGIA COMMUNICATIONS. INC.
00A052	STANILITE ELECTRONICS PTY. LTD
00A053	COMPACT DEVICES, INC.
00A054	Private
00A055	Data Device Corporation
00A056	MICROPROSS
00A057	LANCOM Systems GmbH
00A058	GLORY, LTD.
00A059	HAMILTON HALLMARK
00A05A	KOFAX IMAGE PRODUCTS
00A05B	MARQUIP, INC.
00A05C	INVENTORY CONVERSION, INC./
00A05D	CS COMPUTER SYSTEME GmbH
00A05E	MYRIAD LOGIC INC.
00A05F	BTG Electronics Design BV
00A060	ACER PERIPHERALS, INC.
00A061	PURITAN BENNETT
00A062	AES PRODATA
00A063	JRL SYSTEMS, INC.
00A064	KVB/ANALECT
00A065	Symantec Corporation
00A066	ISA CO., LTD.
00A067	NETWORK SERVICES GROUP
00A068	BHP LIMITED
00A069	Symmetricom, Inc.
00A06A	Verilink Corporation
00A06B	DMS DORSCH MIKROSYSTEM GMBH
00A06C	SHINDENGEN ELECTRIC MFG. CO., LTD.
00A06D	MANNESMANN TALLY CORPORATION
00A06E	AUSTRON, INC.
00A06F	Color Sentinel Systems, LLC
00A070	Coastcom
00A071	VIDEO LOTTERY TECHNOLOGIES,INC
00A072	OVATION SYSTEMS LTD.
00A073	Com21
00A074	PERCEPTION TECHNOLOGY
00A075	MICRON TECHNOLOGY, INC.
00A076	CARDWARE LAB, INC.
00A077	FUJITSU NEXION, INC.
00A078	Marconi Communications
00A079	ALPS ELECTRIC (USA), INC.
00A07A	ADVANCED PERIPHERALS TECHNOLOGIES, INC.
00A07B	DAWN COMPUTER INCORPORATION
00A07C	TONYANG NYLON CO., LTD.
00A07D	SEEQ TECHNOLOGY, INC.
00A07E	AVID TECHNOLOGY, INC.
00A07F	GSM-SYNTEL, LTD.
00A080	Tattile SRL
00A081	ALCATEL DATA NETWORKS
00A082	NKT ELEKTRONIK A/S
00A083	Intel
00A084	Dataplex Pty Ltd
00A085	Private
00A086	AMBER WAVE SYSTEMS, INC.
00A087	Microsemi Corporation
00A088	ESSENTIAL COMMUNICATIONS
00A089	XPOINT TECHNOLOGIES, INC.
00A08A	BROOKTROUT TECHNOLOGY, INC.
00A08B	ASTON ELECTRONIC DESIGNS LTD.
00A08C	MultiMedia LANs, Inc.
00A08D	JACOMO CORPORATION
00A08E	Check Point Software Technologies
00A08F	DESKNET SYSTEMS, INC.
00A090	TimeStep Corporation
00A091	APPLICOM INTERNATIONAL
00A092	Intermate International		[LAN printer interfaces]
00A093	B/E AEROSPACE, Inc.
00A094	COMSAT CORPORATION
00A095	ACACIA NETWORKS, INC.
00A096	MITSUMI ELECTRIC CO., LTD.
00A097	JC INFORMATION SYSTEMS
00A098	Netapp
00A099	K-NET LTD.
00A09A	NIHON KOHDEN AMERICA
00A09B	QPSX COMMUNICATIONS, LTD.
00A09C	Xyplex, Inc.
00A09D	JOHNATHON FREEMAN TECHNOLOGIES
00A09E	Ictv
00A09F	COMMVISION CORP.
00A0A0	COMPACT DATA, LTD.
00A0A1	EPIC DATA INC.
00A0A2	DIGICOM S.P.A.
00A0A3	RELIABLE POWER METERS
00A0A4	Oracle Corporation
00A0A5	TEKNOR MICROSYSTEME, INC.
00A0A6	M.I. SYSTEMS, K.K.
00A0A7	VORAX CORPORATION
00A0A8	RENEX CORPORATION
00A0A9	NAVTEL COMMUNICATIONS INC.
00A0AA	SPACELABS MEDICAL
00A0AB	NETCS INFORMATIONSTECHNIK GMBH
00A0AC	GILAT SATELLITE NETWORKS, LTD.
00A0AD	MARCONI SPA
00A0AE	Network Peripherals, Inc.
00A0AF	WMS INDUSTRIES
00A0B0	I-O DATA DEVICE, INC.
00A0B1	FIRST VIRTUAL CORPORATION
00A0B2	SHIMA SEIKI
00A0B3	Zykronix
00A0B4	TEXAS MICROSYSTEMS, INC.
00A0B5	3H TECHNOLOGY
00A0B6	SANRITZ AUTOMATION CO., LTD.
00A0B7	CORDANT, INC.
00A0B8	Netapp
00A0B9	EAGLE TECHNOLOGY, INC.
00A0BA	PATTON ELECTRONICS CO.
00A0BB	HILAN GMBH
00A0BC	VIASAT, INCORPORATED
00A0BD	I-TECH CORP.
00A0BE	INTEGRATED CIRCUIT SYSTEMS, INC. COMMUNICATIONS GROUP
00A0BF	WIRELESS DATA GROUP MOTOROLA
00A0C0	DIGITAL LINK CORP.
00A0C1	ORTIVUS MEDICAL AB
00A0C2	R.A. SYSTEMS CO., LTD.
00A0C3	UNICOMPUTER GMBH
00A0C4	CRISTIE ELECTRONICS LTD.
00A0C5	ZyXEL Communications Corporation
00A0C6	Qualcomm Inc.
00A0C7	TADIRAN TELECOMMUNICATIONS
00A0C8	Adtran, Inc.
00A0C9	Intel (PRO100B and PRO100+)	[used on Cisco PIX firewall among others]
00A0CA	FUJITSU DENSO LTD.
00A0CB	ARK TELECOMMUNICATIONS, INC.
00A0CC	Lite-On		(used by MacSense in Adapter for Mac, also seen in PCs)
00A0CD	DR. JOHANNES HEIDENHAIN GmbH
00A0CE	Ecessa
00A0CF	SOTAS, INC.
00A0D0	TEN X TECHNOLOGY, INC.
00A0D1	National Semiconductor		[COMPAQ Docking Station]
00A0D2	Allied Telesyn
00A0D3	INSTEM COMPUTER SYSTEMS, LTD.
00A0D4	RADIOLAN,  INC.
00A0D5	SIERRA WIRELESS INC.
00A0D6	SBE, Inc.
00A0D7	KASTEN CHASE APPLIED RESEARCH
00A0D8	Spectra-               # SPECTRA - TEK
00A0D9	CONVEX COMPUTER CORPORATION
00A0DA	INTEGRATED SYSTEMS Technology, Inc.
00A0DB	FISHER & PAYKEL PRODUCTION
00A0DC	O.N. ELECTRONIC CO., LTD.
00A0DD	AZONIX CORPORATION
00A0DE	YAMAHA CORPORATION
00A0DF	STS TECHNOLOGIES, INC.
00A0E0	TENNYSON TECHNOLOGIES PTY LTD
00A0E1	WESTPORT RESEARCH ASSOCIATES, INC.
00A0E2	Keisokugiken Corporation
00A0E3	XKL SYSTEMS CORP.
00A0E4	OPTIQUEST
00A0E5	NHC COMMUNICATIONS
00A0E6	DIALOGIC CORPORATION
00A0E7	CENTRAL DATA CORPORATION
00A0E8	REUTERS HOLDINGS PLC
00A0E9	ELECTRONIC RETAILING SYSTEMS INTERNATIONAL
00A0EA	ETHERCOM CORP.
00A0EB	Encore Networks, Inc.
00A0EC	TRANSMITTON LTD.
00A0ED	Brooks Automation, Inc.
00A0EE	NASHOBA NETWORKS
00A0EF	LUCIDATA LTD.
00A0F0	TORONTO MICROELECTRONICS INC.
00A0F1	Mti
00A0F2	INFOTEK COMMUNICATIONS, INC.
00A0F3	Staubli
00A0F4	Ge
00A0F5	RADGUARD LTD.
00A0F6	AutoGas Systems Inc.
00A0F7	V.I COMPUTER CORP.
00A0F8	Zebra Technologies Inc
00A0F9	BINTEC COMMUNICATIONS GMBH
00A0FA	Marconi Communication GmbH
00A0FB	TORAY ENGINEERING CO., LTD.
00A0FC	IMAGE SCIENCES, INC.
00A0FD	SCITEX DIGITAL PRINTING, INC.
00A0FE	BOSTON TECHNOLOGY, INC.
00A0FF	TELLABS OPERATIONS, INC.
00A1DE	ShenZhen ShiHua Technology CO.,LTD
00A289	Cisco Systems, Inc
00A2DA	INAT GmbH
00A2EE	Cisco Systems, Inc
00A2F5	Guangzhou Yuanyun Network Technology Co.,Ltd
00A2FF	abatec group AG
00A509	WigWag Inc.
00A6CA	Cisco Systems, Inc
00A742	Cisco Systems, Inc
00A784	ITX security
00AA00	Intel
00AA01	Intel Corporation
00AA02	Intel Corporation
00AA3C	OLIVETTI TELECOM SPA (OLTECO)
00AA70	LG Electronics (Mobile Communications)
00ACE0	ARRIS Group, Inc.
00AEFA	Murata Manufacturing Co., Ltd.
00AF1F	Cisco Systems, Inc
00B009	Grass Valley, A Belden Brand
00B017	InfoGear Technology Corp.
00B019	UTC CCS
00B01C	Westport Technologies
00B01E	Rantic Labs, Inc.
00B02A	ORSYS GmbH
00B02D	ViaGate Technologies, Inc.
00B033	OAO Izhevskiy radiozavod
00B03B	HiQ Networks
00B048	Marconi Communications Inc.
00B04A	Cisco Systems, Inc
00B052	Atheros Communications
00B064	Cisco Systems, Inc
00B069	Honewell Oy
00B06D	Jones Futurex Inc.
00B080	Mannesmann Ipulsys B.V.
00B086	LocSoft Limited
00B08E	Cisco Systems, Inc
00B091	Transmeta Corp.
00B094	Alaris, Inc.
00B09A	Morrow Technologies Corp.
00B09D	Point Grey Research Inc.
00B0AC	SIAE-Microelettronica S.p.A.
00B0AE	Symmetricom
00B0B3	XSTREAMIS PLC
00B0C2	Cisco Systems, Inc
00B0C7	Tellabs Operations, Inc.
00B0CE	Viveris Technologies
00B0D0	Computer Products International
00B0DB	Nextcell, Inc.
00B0DF	Starboard Storage Systems
00B0E1	Cisco Systems, Inc
00B0E7	British Federal Ltd.
00B0EC	Eacem
00B0EE	Ajile Systems, Inc.
00B0F0	CALY NETWORKS
00B0F5	NetWorth Technologies, Inc.
00B338	Kontron Design Manufacturing Services (M) Sdn. Bhd
00B342	MacroSAN Technologies Co., Ltd.
00B362	Apple, Inc.
00B56D	David Electronics Co., LTD.
00B5D6	Omnibit Inc.
00B78D	Nanjing Shining Electric Automation Co., Ltd
00B9F6	Shenzhen Super Rich Electronics Co.,Ltd
00BAC0	Biometric Access Company
00BB01	OCTOTHORPE CORP.
00BB3A	Private
00BB8E	HME Co., Ltd.
00BBC1	CANON INC.
00BBF0	UNGERMANN-BASS INC.
00BD27	Exar Corp.
00BD3A	Nokia Corporation
00BD82	Shenzhen YOUHUA Technology Co., Ltd
00BF15	Genetec Inc.
00C000	Lanoptics Ltd
00C001	Diatek Patient Managment
00C002	Sercomm Corporation
00C003	Globalnet Communications
00C004	Japan Business Computer Co.Ltd
00C005	Livingston Enterprises Inc	Portmaster (OEMed by Cayman)
00C006	Nippon Avionics Co Ltd
00C007	Pinnacle Data Systems Inc
00C008	Seco SRL
00C009	KT Technology (s) Pte Inc
00C00A	Micro Craft
00C00B	Norcontrol A.S.
00C00C	ARK PC Technology, Inc.
00C00D	Advanced Logic Research Inc
00C00E	Psitech Inc
00C00F	QNX Software Systems Ltd.	[also Quantum Software Systems Ltd]
00C010	HIRAKAWA HEWTECH CORP.
00C011	Interactive Computing Devices
00C012	Netspan Corp
00C013	Netrix
00C014	Telematics Calabasas
00C015	New Media Corp
00C016	Electronic Theatre Controls
00C017	Fluke
00C018	Lanart Corp
00C019	LEAP TECHNOLOGY, INC.
00C01A	Corometrics Medical Systems
00C01B	Socket Communications
00C01C	Interlink Communications Ltd.
00C01D	Grand Junction Networks, Inc.	(Cisco Catalyst also reported)
00C01E	LA FRANCAISE DES JEUX
00C01F	S.E.R.C.E.L.
00C020	Arco Electronic, Control Ltd.
00C021	Netexpress
00C022	LASERMASTER TECHNOLOGIES, INC.
00C023	Tutankhamon Electronics
00C024	Eden Sistemas De Computacao SA
00C025	Dataproducts Corporation
00C026	LANS TECHNOLOGY CO., LTD.
00C027	Cipher Systems, Inc.
00C028	Jasco Corporation
00C029	Kabel Rheydt AG
00C02A	Ohkura Electric Co
00C02B	Gerloff Gesellschaft Fur
00C02C	Centrum Communications, Inc.
00C02D	Fuji Photo Film Co., Ltd.
00C02E	Netwiz
00C02F	Okuma Corp
00C030	Integrated Engineering B. V.
00C031	Design Research Systems, Inc.
00C032	I-Cubed Limited
00C033	Telebit Corporation
00C034	Dale Computer Corporation
00C035	Quintar Company
00C036	Raytech Electronic Corp
00C037	Dynatem
00C038	RASTER IMAGE PROCESSING SYSTEM
00C039	Silicon Systems
00C03A	MEN-MIKRO ELEKTRONIK GMBH
00C03B	Multiaccess Computing Corp
00C03C	Tower Tech S.R.L.
00C03D	Wiesemann & Theis Gmbh
00C03E	Fa. Gebr. Heller Gmbh
00C03F	Stores Automated Systems Inc
00C040	Ecci
00C041	Digital Transmission Systems
00C042	Datalux Corp.
00C043	Stratacom
00C044	Emcom Corporation
00C045	Isolation Systems Inc
00C046	Kemitron Ltd
00C047	Unimicro Systems Inc
00C048	Bay Technical Associates
00C049	US Robotics Total Control (tm) NETServer Card
00C04A	GROUP 2000 AG
00C04B	CREATIVE MICROSYSTEMS
00C04C	DEPARTMENT OF FOREIGN AFFAIRS
00C04D	Mitec Ltd
00C04E	Comtrol Corporation
00C04F	Dell
00C050	Toyo Denki Seizo K.K.
00C051	Advanced Integration Research
00C052	BURR-BROWN
00C053	Aspect Software Inc.
00C054	NETWORK PERIPHERALS, LTD.
00C055	Modular Computing Technologies
00C056	Somelec
00C057	Myco Electronics
00C058	Dataexpert Corp
00C059	Nippondenso Corp
00C05A	SEMAPHORE COMMUNICATIONS CORP.
00C05B	Networks Northwest Inc
00C05C	Elonex PLC
00C05D	L&N Technologies
00C05E	Vari-Lite Inc
00C05F	FINE-PAL COMPANY LIMITED
00C060	ID Scandinavia A/S
00C061	Solectek Corporation
00C062	IMPULSE TECHNOLOGY
00C063	Morning Star Technologies Inc	May be miswrite of 0003C6
00C064	General Datacomm Ind Inc
00C065	Scope Communications Inc
00C066	Docupoint, Inc.
00C067	United Barcode Industries
00C068	Philp Drake Electronics Ltd
00C069	California Microwave Inc
00C06A	Zahner-Elektrik Gmbh & Co KG
00C06B	OSI Plus Corporation
00C06C	SVEC Computer Corp
00C06D	Boca Research, Inc.
00C06E	HAFT TECHNOLOGY, INC.
00C06F	Komatsu Ltd
00C070	Sectra Secure-Transmission AB
00C071	Areanex Communications, Inc.
00C072	KNX Ltd
00C073	Xedia Corporation
00C074	Toyoda Automatic Loom Works Ltd
00C075	Xante Corporation
00C076	I-Data International A-S
00C077	Daewoo Telecom Ltd
00C078	Computer Systems Engineering
00C079	Fonsys Co Ltd
00C07A	Priva BV
00C07B	Ascend Communications		ISDN bridges/routers
00C07C	HIGHTECH INFORMATION
00C07D	RISC Developments Ltd
00C07E	KUBOTA CORPORATION ELECTRONIC
00C07F	Nupon Computing Corp
00C080	Netstar Inc
00C081	Metrodata Ltd
00C082	Moore Products Co
00C083	TRACE MOUNTAIN PRODUCTS, INC.
00C084	Data Link Corp Ltd
00C085	Canon
00C086	The Lynk Corporation
00C087	UUNET Technologies Inc
00C088	EKF ELEKTRONIK GMBH
00C089	Telindus Distribution
00C08A	Lauterbach Datentechnik Gmbh
00C08B	RISQ Modular Systems Inc
00C08C	Performance Technologies Inc
00C08D	Tronix Product Development
00C08E	Network Information Technology
00C08F	Matsushita Electric Works, Ltd.
00C090	Praim S.R.L.
00C091	Jabil Circuit, Inc.
00C092	Mennen Medical Inc
00C093	Alta Research Corp.
00C094	VMX INC.
00C095	Znyx (Network Appliance); Jupiter Systems (MX-700); Apple (G3)  all seen
00C096	Tamura Corporation
00C097	Archipel SA
00C098	Chuntex Electronic Co., Ltd.
00C099	YOSHIKI INDUSTRIAL CO.,LTD.
00C09A	PHOTONICS CORPORATION
00C09B	Reliance Comm/Tec, R-Tec Systems Inc
00C09C	TOA Electronic Ltd
00C09D	Distributed Systems Int'l, Inc.
00C09E	CACHE COMPUTERS, INC.
00C09F	Quanta Computer Inc
00C0A0	Advance Micro Research, Inc.
00C0A1	Tokyo Denshi Sekei Co
00C0A2	Intermedium A/S
00C0A3	Dual Enterprises Corporation
00C0A4	Unigraf OY
00C0A5	DICKENS DATA SYSTEMS
00C0A6	EXICOM AUSTRALIA PTY. LTD
00C0A7	SEEL Ltd
00C0A8	GVC Corporation
00C0A9	Barron McCann Ltd
00C0AA	Silicon Valley Computer
00C0AB	Jupiter Technology Inc
00C0AC	Gambit Computer Communications
00C0AD	Computer Communication Systems
00C0AE	Towercom Co Inc DBA PC House
00C0AF	TEKLOGIX INC.
00C0B0	GCC Technologies,Inc.
00C0B1	GENIUS NET CO.
00C0B2	Norand Corporation
00C0B3	Comstat Datacomm Corporation
00C0B4	Myson Technology Inc
00C0B5	Corporate Network Systems Inc
00C0B6	Meridian Data Inc
00C0B7	American Power Conversion Corp
00C0B8	Fraser's Hill Ltd.
00C0B9	Funk Software Inc
00C0BA	Netvantage
00C0BB	Forval Creative Inc
00C0BC	TELECOM AUSTRALIA/CSSC
00C0BD	Inex Technologies, Inc.
00C0BE	Alcatel-	# Alcatel - Sel
00C0BF	Technology Concepts Ltd
00C0C0	Shore Microsystems Inc
00C0C1	Quad/Graphics Inc
00C0C2	Infinite Networks Ltd.
00C0C3	Acuson Computed Sonography
00C0C4	Computer Operational
00C0C5	SID Informatica
00C0C6	Personal Media Corp
00C0C7	SPARKTRUM MICROSYSTEMS, INC.
00C0C8	Micro Byte Pty Ltd
00C0C9	Bailey Controls Co
00C0CA	Alfa, Inc.
00C0CB	Control Technology Corporation
00C0CC	TELESCIENCES CO SYSTEMS, INC.
00C0CD	Comelta S.A.
00C0CE	CEI SYSTEMS & ENGINEERING PTE
00C0CF	IMATRAN VOIMA OY
00C0D0	Ratoc System Inc
00C0D1	Comtree Technology Corporation (EFA also reported)
00C0D2	Syntellect Inc
00C0D3	OLYMPUS IMAGE SYSTEMS, INC.
00C0D4	Axon Networks Inc
00C0D5	Quancom Electronic Gmbh
00C0D6	J1 Systems, Inc.
00C0D7	TAIWAN TRADING CENTER DBA
00C0D8	UNIVERSAL DATA SYSTEMS
00C0D9	Quinte Network Confidentiality Equipment Inc
00C0DA	NICE SYSTEMS LTD.
00C0DB	IPC Corporation (Pte) Ltd
00C0DC	EOS Technologies, Inc.
00C0DD	QLogic Corporation
00C0DE	ZComm Inc
00C0DF	Kye Systems Corp
00C0E0	DSC COMMUNICATION CORP.
00C0E1	Sonic Solutions
00C0E2	Calcomp, Inc.
00C0E3	Ositech Communications Inc
00C0E4	Landis & Gyr Powers Inc
00C0E5	GESPAC S.A.
00C0E6	Txport
00C0E7	Fiberdata AB
00C0E8	Plexcom Inc
00C0E9	Oak Solutions Ltd
00C0EA	Array Technology Ltd.
00C0EB	SEH COMPUTERTECHNIK GMBH
00C0EC	Dauphin Technology
00C0ED	US Army Electronic Proving Ground
00C0EE	Kyocera Corporation
00C0EF	Abit Corporation
00C0F0	Kingston Technology Corporation
00C0F1	Shinko Electric Co Ltd
00C0F2	Transition Engineering Inc
00C0F3	Network Communications Corp
00C0F4	Interlink System Co., Ltd.
00C0F5	Metacomp Inc
00C0F6	Celan Technology Inc.
00C0F7	Engage Communication, Inc.
00C0F8	About Computing Inc.
00C0F9	Artesyn Embedded Technologies
00C0FA	Canary Communications Inc
00C0FB	Advanced Technology Labs
00C0FC	ASDG Incorporated
00C0FD	Prosum
00C0FE	APTEC COMPUTER SYSTEMS, INC.
00C0FF	Box Hill Systems Corporation
00C14F	DDL Co,.ltd.
00C164	Cisco Systems, Inc
00C1B1	Cisco Systems, Inc
00C2C6	Intel Corporate
00C5DB	Datatech Sistemas Digitales Avanzados SL
00C610	Apple, Inc.
00C88B	Cisco Systems, Inc
00CAE5	Cisco Systems, Inc
00CB00	Private
00CBBD	Cambridge Broadband Networks Ltd.
00CCFC	Cisco Systems, Inc
00CD90	MAS Elektronik AG
00CDFE	Apple, Inc.
00CF1C	Communication Machinery Corporation
00D000	FERRAN SCIENTIFIC, INC.
00D001	VST TECHNOLOGIES, INC.
00D002	DITECH CORPORATION
00D003	COMDA ENTERPRISES CORP.
00D004	PENTACOM LTD.
00D005	ZHS ZEITMANAGEMENTSYSTEME
00D006	Cisco Systems, Inc
00D007	MIC ASSOCIATES, INC.
00D008	MACTELL CORPORATION
00D009	HSING TECH. ENTERPRISE CO. LTD
00D00A	LANACCESS TELECOM S.A.
00D00B	RHK TECHNOLOGY, INC.
00D00C	SNIJDER MICRO SYSTEMS
00D00D	MICROMERITICS INSTRUMENT
00D00E	PLURIS, INC.
00D00F	SPEECH DESIGN GMBH
00D010	CONVERGENT NETWORKS, INC.
00D011	PRISM VIDEO, INC.
00D012	GATEWORKS CORP.
00D013	PRIMEX AEROSPACE COMPANY
00D014	ROOT, INC.
00D015	UNIVEX MICROTECHNOLOGY CORP.
00D016	SCM MICROSYSTEMS, INC.
00D017	SYNTECH INFORMATION CO., LTD.
00D018	QWES. COM, INC.
00D019	DAINIPPON SCREEN CORPORATE
00D01A	URMET  TLC S.P.A.
00D01B	MIMAKI ENGINEERING CO., LTD.
00D01C	SBS TECHNOLOGIES,
00D01D	FURUNO ELECTRIC CO., LTD.
00D01E	PINGTEL CORP.
00D01F	Senetas Security
00D020	AIM SYSTEM, INC.
00D021	REGENT ELECTRONICS CORP.
00D022	INCREDIBLE TECHNOLOGIES, INC.
00D023	INFORTREND TECHNOLOGY, INC.
00D024	Cognex Corporation
00D025	XROSSTECH, INC.
00D026	HIRSCHMANN AUSTRIA GMBH
00D027	APPLIED AUTOMATION, INC.
00D028	Harmonic, Inc
00D029	WAKEFERN FOOD CORPORATION
00D02A	Voxent Systems Ltd.
00D02B	JETCELL, INC.
00D02C	CAMPBELL SCIENTIFIC, INC.
00D02D	Ademco
00D02E	COMMUNICATION AUTOMATION CORP.
00D02F	VLSI TECHNOLOGY INC.
00D030	Safetran Systems Corp
00D031	INDUSTRIAL LOGIC CORPORATION
00D032	YANO ELECTRIC CO., LTD.
00D033	DALIAN DAXIAN NETWORK
00D034	ORMEC SYSTEMS CORP.
00D035	BEHAVIOR TECH. COMPUTER CORP.
00D036	TECHNOLOGY ATLANTA CORP.
00D037	ARRIS Group, Inc.
00D038	FIVEMERE, LTD.
00D039	UTILICOM, INC.
00D03A	ZONEWORX, INC.
00D03B	VISION PRODUCTS PTY. LTD.
00D03C	Vieo, Inc.
00D03D	GALILEO TECHNOLOGY, LTD.
00D03E	ROCKETCHIPS, INC.
00D03F	AMERICAN COMMUNICATION
00D040	SYSMATE CO., LTD.
00D041	AMIGO TECHNOLOGY CO., LTD.
00D042	MAHLO GMBH & CO. UG
00D043	ZONAL RETAIL DATA SYSTEMS
00D044	ALIDIAN NETWORKS, INC.
00D045	KVASER AB
00D046	DOLBY LABORATORIES, INC.
00D047	XN TECHNOLOGIES
00D048	ECTON, INC.
00D049	IMPRESSTEK CO., LTD.
00D04A	PRESENCE TECHNOLOGY GMBH
00D04B	LA CIE GROUP S.A.
00D04C	EUROTEL TELECOM LTD.
00D04D	DIV OF RESEARCH & STATISTICS
00D04E	Logibag
00D04F	BITRONICS, INC.
00D050	Iskratel
00D051	O2 MICRO, INC.
00D052	ASCEND COMMUNICATIONS, INC.
00D053	CONNECTED SYSTEMS
00D054	SAS INSTITUTE INC.
00D055	KATHREIN-WERKE KG
00D056	SOMAT CORPORATION
00D057	ULTRAK, INC.
00D058	Cisco Systems, Inc
00D059	AMBIT MICROSYSTEMS CORP.
00D05A	SYMBIONICS, LTD.
00D05B	ACROLOOP MOTION CONTROL
00D05C	KATHREIN TechnoTrend GmbH
00D05D	INTELLIWORXX, INC.
00D05E	STRATABEAM TECHNOLOGY, INC.
00D05F	VALCOM, INC.
00D060	Panasonic Europe Ltd.
00D061	TREMON ENTERPRISES CO., LTD.
00D062	Digigram
00D063	Cisco Systems, Inc
00D064	Multitel
00D065	TOKO ELECTRIC
00D066	WINTRISS ENGINEERING CORP.
00D067	CAMPIO COMMUNICATIONS
00D068	IWILL CORPORATION
00D069	TECHNOLOGIC SYSTEMS
00D06A	LINKUP SYSTEMS CORPORATION
00D06B	SR TELECOM INC.
00D06C	SHAREWAVE, INC.
00D06D	ACRISON, INC.
00D06E	TRENDVIEW RECORDERS LTD.
00D06F	KMC CONTROLS
00D070	LONG WELL ELECTRONICS CORP.
00D071	ECHELON CORP.
00D072	BROADLOGIC
00D073	ACN ADVANCED COMMUNICATIONS
00D074	TAQUA SYSTEMS, INC.
00D075	ALARIS MEDICAL SYSTEMS, INC.
00D076	Bank of America
00D077	LUCENT TECHNOLOGIES
00D078	Eltex of Sweden AB
00D079	Cisco Systems, Inc
00D07A	AMAQUEST COMPUTER CORP.
00D07B	COMCAM INTERNATIONAL INC
00D07C	KOYO ELECTRONICS INC. CO.,LTD.
00D07D	COSINE COMMUNICATIONS
00D07E	KEYCORP LTD.
00D07F	STRATEGY & TECHNOLOGY, LIMITED
00D080	EXABYTE CORPORATION
00D081	RTD Embedded Technologies, Inc.
00D082	IOWAVE INC.
00D083	INVERTEX, INC.
00D084	NEXCOMM SYSTEMS, INC.
00D085	OTIS ELEVATOR COMPANY
00D086	FOVEON, INC.
00D087	MICROFIRST INC.
00D088	ARRIS Group, Inc.
00D089	DYNACOLOR, INC.
00D08A	PHOTRON USA
00D08B	ADVA Optical Networking Ltd.
00D08C	GENOA TECHNOLOGY, INC.
00D08D	PHOENIX GROUP, INC.
00D08E	Grass Valley, A Belden Brand
00D08F	ARDENT TECHNOLOGIES, INC.
00D090	Cisco Systems, Inc
00D091	SMARTSAN SYSTEMS, INC.
00D092	GLENAYRE WESTERN MULTIPLEX
00D093	TQ - COMPONENTS GMBH
00D094	Seeion Control LLC
00D095	Alcatel-               # Alcatel-Lucent Enterprise
00D096	3COM EUROPE LTD.
00D097	Cisco Systems, Inc
00D098	Photon Dynamics Canada Inc.
00D099	Elcard Wireless Systems Oy
00D09A	FILANET CORPORATION
00D09B	SPECTEL LTD.
00D09C	KAPADIA COMMUNICATIONS
00D09D	VERIS INDUSTRIES
00D09E	2Wire Inc
00D09F	NOVTEK TEST SYSTEMS
00D0A0	MIPS DENMARK
00D0A1	OSKAR VIERLING GMBH + CO. KG
00D0A2	INTEGRATED DEVICE
00D0A3	VOCAL DATA, INC.
00D0A4	ALANTRO COMMUNICATIONS
00D0A5	AMERICAN ARIUM
00D0A6	LANBIRD TECHNOLOGY CO., LTD.
00D0A7	TOKYO SOKKI KENKYUJO CO., LTD.
00D0A8	NETWORK ENGINES, INC.
00D0A9	SHINANO KENSHI CO., LTD.
00D0AA	CHASE COMMUNICATIONS
00D0AB	DELTAKABEL TELECOM CV
00D0AC	Commscope, Inc
00D0AD	TL INDUSTRIES
00D0AE	ORESIS COMMUNICATIONS, INC.
00D0AF	CUTLER-HAMMER, INC.
00D0B0	BITSWITCH LTD.
00D0B1	OMEGA ELECTRONICS SA
00D0B2	Xiotech Corporation
00D0B3	DRS Technologies Canada Ltd
00D0B4	KATSUJIMA CO., LTD.
00D0B5	IPricot formerly DotCom
00D0B6	CRESCENT NETWORKS, INC.
00D0B7	Intel Corporation
00D0B8	Iomega Corporation
00D0B9	MICROTEK INTERNATIONAL, INC.
00D0BA	Cisco Systems, Inc
00D0BB	Cisco Systems, Inc
00D0BC	Cisco Systems, Inc
00D0BD	Lattice Semiconductor Corp. (LPA)
00D0BE	EMUTEC INC.
00D0BF	PIVOTAL TECHNOLOGIES
00D0C0	Cisco Systems, Inc
00D0C1	HARMONIC DATA SYSTEMS, LTD.
00D0C2	BALTHAZAR TECHNOLOGY AB
00D0C3	VIVID TECHNOLOGY PTE, LTD.
00D0C4	TERATECH CORPORATION
00D0C5	COMPUTATIONAL SYSTEMS, INC.
00D0C6	THOMAS & BETTS CORP.
00D0C7	PATHWAY, INC.
00D0C8	Prevas A/S
00D0C9	ADVANTECH CO., LTD.
00D0CA	Intrinsyc Software International Inc.
00D0CB	DASAN CO., LTD.
00D0CC	TECHNOLOGIES LYRE INC.
00D0CD	ATAN TECHNOLOGY INC.
00D0CE	ASYST ELECTRONIC
00D0CF	MORETON BAY
00D0D0	ZHONGXING TELECOM LTD.
00D0D1	Sycamore Networks
00D0D2	EPILOG CORPORATION
00D0D3	Cisco Systems, Inc
00D0D4	V-BITS, INC.
00D0D5	GRUNDIG AG
00D0D6	AETHRA TELECOMUNICAZIONI
00D0D7	B2C2, INC.
00D0D8	3Com Corporation
00D0D9	DEDICATED MICROCOMPUTERS
00D0DA	TAICOM DATA SYSTEMS CO., LTD.
00D0DB	MCQUAY INTERNATIONAL
00D0DC	MODULAR MINING SYSTEMS, INC.
00D0DD	SUNRISE TELECOM, INC.
00D0DE	PHILIPS MULTIMEDIA NETWORK
00D0DF	KUZUMI ELECTRONICS, INC.
00D0E0	DOOIN ELECTRONICS CO.
00D0E1	AVIONITEK ISRAEL INC.
00D0E2	MRT MICRO, INC.
00D0E3	ELE-CHEM ENGINEERING CO., LTD.
00D0E4	Cisco Systems, Inc
00D0E5	SOLIDUM SYSTEMS CORP.
00D0E6	IBOND INC.
00D0E7	VCON TELECOMMUNICATION LTD.
00D0E8	MAC SYSTEM CO., LTD.
00D0E9	Advantage Century Telecommunication Corp.
00D0EA	NEXTONE COMMUNICATIONS, INC.
00D0EB	LIGHTERA NETWORKS, INC.
00D0EC	NAKAYO Inc
00D0ED	Xiox
00D0EE	DICTAPHONE CORPORATION
00D0EF	Igt
00D0F0	CONVISION TECHNOLOGY GMBH
00D0F1	SEGA ENTERPRISES, LTD.
00D0F2	MONTEREY NETWORKS
00D0F3	SOLARI DI UDINE SPA
00D0F4	CARINTHIAN TECH INSTITUTE
00D0F5	ORANGE MICRO, INC.
00D0F6	Nokia
00D0F7	NEXT NETS CORPORATION
00D0F8	FUJIAN STAR TERMINAL
00D0F9	ACUTE COMMUNICATIONS CORP.
00D0FA	ThalesE-               # Thales e-Security Ltd.
00D0FB	TEK MICROSYSTEMS, INCORPORATED
00D0FC	GRANITE MICROSYSTEMS
00D0FD	OPTIMA TELE.COM, INC.
00D0FE	ASTRAL POINT
00D0FF	Cisco Systems, Inc
00D11C	Acetel
00D318	SPG Controls
00D38D	Hotel Technology Next Generation
00D632	GE Energy
00D78F	Cisco Systems, Inc
00D9D1	Sony Interactive Entertainment Inc.
00DA55	Cisco Systems, Inc
00DB1E	Albedo Telecom SL
00DB45	THAMWAY CO.,LTD.
00DBDF	Intel Corporate
00DD00	Ungermann-Bass			IBM RT
00DD01	Ungermann-Bass
00DD02	UNGERMANN-BASS INC.
00DD03	UNGERMANN-BASS INC.
00DD04	UNGERMANN-BASS INC.
00DD05	UNGERMANN-BASS INC.
00DD06	UNGERMANN-BASS INC.
00DD07	UNGERMANN-BASS INC.
00DD08	Ungermann-Bass
00DD09	UNGERMANN-BASS INC.
00DD0A	UNGERMANN-BASS INC.
00DD0B	UNGERMANN-BASS INC.
00DD0C	UNGERMANN-BASS INC.
00DD0D	UNGERMANN-BASS INC.
00DD0E	UNGERMANN-BASS INC.
00DD0F	UNGERMANN-BASS INC.
00DEFB	Cisco Systems, Inc
00E000	FUJITSU LIMITED
00E001	STRAND LIGHTING LIMITED
00E002	CROSSROADS SYSTEMS, INC.
00E003	NOKIA WIRELESS BUSINESS COMMUN
00E004	PMC-SIERRA, INC.
00E005	TECHNICAL CORP.
00E006	SILICON INTEGRATED SYS. CORP.
00E007	Avaya ECS Ltd
00E008	AMAZING CONTROLS! INC.
00E009	MARATHON TECHNOLOGIES CORP.
00E00A	DIBA, INC.
00E00B	ROOFTOP COMMUNICATIONS CORP.
00E00C	Motorola
00E00D	RADIANT SYSTEMS
00E00E	AVALON IMAGING SYSTEMS, INC.
00E00F	Shanghai Baud Data Communication Co.,Ltd.
00E010	HESS SB-AUTOMATENBAU GmbH
00E011	Uniden Corporation
00E012	PLUTO TECHNOLOGIES INTERNATIONAL INC.
00E013	EASTERN ELECTRONIC CO., LTD.
00E014	Cisco
00E015	HEIWA CORPORATION
00E016	rapid-city (now a part of bay networks)
00E017	EXXACT GmbH
00E018	Asustek		Intel 82558-based Integrated Fast Ethernet for WIM
00E019	ING. GIORDANO ELETTRONICA
00E01A	COMTEC SYSTEMS. CO., LTD.
00E01B	SPHERE COMMUNICATIONS, INC.
00E01C	Cradlepoint, Inc
00E01D	WebTV NETWORKS, INC.
00E01E	Cisco
00E01F	AVIDIA Systems, Inc.
00E020	TECNOMEN OY
00E021	FREEGATE CORP.
00E022	Analog Devices, Inc.
00E023	Telrad
00E024	GADZOOX NETWORKS
00E025	dit Co., Ltd.
00E026	Redlake MASD LLC
00E027	DUX, INC.
00E028	APTIX CORPORATION
00E029	SMC EtherPower II 10/100
00E02A	TANDBERG TELEVISION AS
00E02B	Extreme Networks
00E02C	AST - built into 5166M PC motherboard (win95 id's as Intel)
00E02D	InnoMediaLogic, Inc.
00E02E	SPC ELECTRONICS CORPORATION
00E02F	MCNS HOLDINGS, L.P.
00E030	MELITA INTERNATIONAL CORP.
00E031	HAGIWARA ELECTRIC CO., LTD.
00E032	MISYS FINANCIAL SYSTEMS, LTD.
00E033	E.E.P.D. GmbH
00E034	Cisco
00E035	Artesyn Embedded Technologies
00E036	PIONEER CORPORATION
00E037	CENTURY CORPORATION
00E038	PROXIMA CORPORATION
00E039	Paradyne 7112 T1 DSU/CSU
00E03A	Cabletron Systems, Inc.
00E03B	PROMINET CORPORATION
00E03C	Advansys
00E03D	FOCON ELECTRONIC SYSTEMS A/S
00E03E	ALFATECH, INC.
00E03F	JATON CORPORATION
00E040	DeskStation Technology, Inc.
00E041	Cspi
00E042	Pacom Systems Ltd.
00E043	Vitalcom
00E044	LSICS CORPORATION
00E045	TOUCHWAVE, INC.
00E046	BENTLY NEVADA CORP.
00E047	InFocus Corporation
00E048	SDL COMMUNICATIONS, INC.
00E049	MICROWI ELECTRONIC GmbH
00E04A	ZX Technologies, Inc
00E04B	JUMP INDUSTRIELLE COMPUTERTECHNIK GmbH
00E04C	REALTEK SEMICONDUCTOR CORP.
00E04D	INTERNET INITIATIVE JAPAN, INC
00E04E	SANYO DENKI CO., LTD.
00E04F	Cisco
00E050	EXECUTONE INFORMATION SYSTEMS, INC.
00E051	TALX CORPORATION
00E052	Brocade Communications Systems, Inc.
00E053	CELLPORT LABS, INC.
00E054	KODAI HITEC CO., LTD.
00E055	INGENIERIA ELECTRONICA COMERCIAL INELCOM S.A.
00E056	HOLONTECH CORPORATION
00E057	HAN MICROTELECOM. CO., LTD.
00E058	PHASE ONE DENMARK A/S
00E059	CONTROLLED ENVIRONMENTS, LTD.
00E05A	GALEA NETWORK SECURITY
00E05B	WEST END SYSTEMS CORP.
00E05C	Panasonic Healthcare Co., Ltd.
00E05D	UNITEC CO., LTD.
00E05E	JAPAN AVIATION ELECTRONICS INDUSTRY, LTD.
00E05F	e-Net, Inc.
00E060	Sherwood
00E061	EdgePoint Networks, Inc.
00E062	HOST ENGINEERING
00E063	Cabletron Systems, Inc.
00E064	SAMSUNG ELECTRONICS
00E065	OPTICAL ACCESS INTERNATIONAL
00E066	ProMax Systems, Inc.
00E067	eac AUTOMATION-CONSULTING GmbH
00E068	MERRIMAC SYSTEMS INC.
00E069	Jaycor
00E06A	KAPSCH AG
00E06B	W&G SPECIAL PRODUCTS
00E06C	Ultra Electronics Command & Control Systems
00E06D	COMPUWARE CORPORATION
00E06E	FAR SYSTEMS S.p.A.
00E06F	ARRIS Group, Inc.
00E070	DH TECHNOLOGY
00E071	EPIS MICROCOMPUTER
00E072	Lynk
00E073	NATIONAL AMUSEMENT NETWORK, INC.
00E074	TIERNAN COMMUNICATIONS, INC.
00E075	Verilink Corporation
00E076	DEVELOPMENT CONCEPTS, INC.
00E077	WEBGEAR, INC.
00E078	BERKELEY NETWORKS
00E079	A.T.N.R.
00E07A	MIKRODIDAKT AB
00E07B	BAY NETWORKS
00E07C	Mettler-               # METTLER-TOLEDO, INC.
00E07D	Encore (Netronix?)		10/100 PCI Fast ethernet card
00E07E	WALT DISNEY IMAGINEERING
00E07F	LOGISTISTEM s.r.l.
00E080	CONTROL RESOURCES CORPORATION
00E081	Tyan Computer Corp.		Onboard Intel 82558 10/100
00E082	Anerma
00E083	Jato Technologies, Inc.
00E084	COMPULITE R&D
00E085	GLOBAL MAINTECH, INC.
00E086	Emerson Network Power, Avocent Division
00E087	LeCroy - Networking Productions Division
00E088	LTX-Credence CORPORATION
00E089	ION Networks, Inc.
00E08A	GEC AVERY, LTD.
00E08B	QLogic Corporation
00E08C	NEOPARADIGM LABS, INC.
00E08D	PRESSURE SYSTEMS, INC.
00E08E	UTSTARCOM
00E08F	Cisco Systems			Catalyst 2900 series
00E090	BECKMAN LAB. AUTOMATION DIV.
00E091	LG Electronics
00E092	ADMTEK INCORPORATED
00E093	ACKFIN NETWORKS
00E094	OSAI SRL
00E095	ADVANCED-VISION TECHNOLGIES CORP.
00E096	SHIMADZU CORPORATION
00E097	CARRIER ACCESS CORPORATION
00E098	Trend
00E099	SAMSON AG
00E09A	Positron Inc.
00E09B	ENGAGE NETWORKS, INC.
00E09C	Mii
00E09D	SARNOFF CORPORATION
00E09E	Quantum Corporation
00E09F	PIXEL VISION
00E0A0	WILTRON CO.
00E0A1	HIMA PAUL HILDEBRANDT GmbH Co. KG
00E0A2	MICROSLATE INC.
00E0A3	Cisco Systems			Catalyst 1924
00E0A4	ESAOTE S.p.A.
00E0A5	ComCore Semiconductor, Inc.
00E0A6	TELOGY NETWORKS, INC.
00E0A7	IPC INFORMATION SYSTEMS, INC.
00E0A8	SAT GmbH & Co.
00E0A9	FUNAI ELECTRIC CO., LTD.
00E0AA	ELECTROSONIC LTD.
00E0AB	DIMAT S.A.
00E0AC	MIDSCO, INC.
00E0AD	EES TECHNOLOGY, LTD.
00E0AE	XAQTI CORPORATION
00E0AF	GENERAL DYNAMICS INFORMATION SYSTEMS
00E0B0	Cisco Systems			Various systems reported
00E0B1	Alcatel-               # Alcatel-Lucent Enterprise
00E0B2	TELMAX COMMUNICATIONS CORP.
00E0B3	EtherWAN Systems, Inc.
00E0B4	TECHNO SCOPE CO., LTD.
00E0B5	ARDENT COMMUNICATIONS CORP.
00E0B6	Entrada Networks
00E0B7	PI GROUP, LTD.
00E0B8	AMD PCNet			in a Gateway 2000
00E0B9	BYAS SYSTEMS
00E0BA	BERGHOF AUTOMATIONSTECHNIK GmbH
00E0BB	NBX CORPORATION
00E0BC	SYMON COMMUNICATIONS, INC.
00E0BD	INTERFACE SYSTEMS, INC.
00E0BE	GENROCO INTERNATIONAL, INC.
00E0BF	TORRENT NETWORKING TECHNOLOGIES CORP.
00E0C0	SEIWA ELECTRIC MFG. CO., LTD.
00E0C1	MEMOREX TELEX JAPAN, LTD.
00E0C2	NECSY S.p.A.
00E0C3	SAKAI SYSTEM DEVELOPMENT CORP.
00E0C4	HORNER ELECTRIC, INC.
00E0C5	BCOM Electronics Inc.
00E0C6	LINK2IT, L.L.C.
00E0C7	EUROTECH SRL
00E0C8	VIRTUAL ACCESS, LTD.
00E0C9	AutomatedLogic Corporation
00E0CA	BEST DATA PRODUCTS
00E0CB	RESON, INC.
00E0CC	HERO SYSTEMS, LTD.
00E0CD	SAAB SENSIS CORPORATION
00E0CE	Arn
00E0CF	INTEGRATED DEVICE
00E0D0	NETSPEED, INC.
00E0D1	TELSIS LIMITED
00E0D2	VERSANET COMMUNICATIONS, INC.
00E0D3	DATENTECHNIK GmbH
00E0D4	EXCELLENT COMPUTER
00E0D5	Emulex Corporation
00E0D6	COMPUTER & COMMUNICATION RESEARCH LAB.
00E0D7	SUNSHINE ELECTRONICS, INC.
00E0D8	LANBit Computer, Inc.
00E0D9	TAZMO CO., LTD.
00E0DA	Alcatel-               # Alcatel-Lucent Enterprise
00E0DB	ViaVideo Communications, Inc.
00E0DC	NEXWARE CORP.
00E0DD	Zenith Electronics Corporation
00E0DE	DATAX NV
00E0DF	KEYMILE GmbH
00E0E0	SI ELECTRONICS, LTD.
00E0E1	G2 NETWORKS, INC.
00E0E2	INNOVA CORP.
00E0E3	SK-ELEKTRONIK GMBH
00E0E4	FANUC ROBOTICS NORTH AMERICA, Inc.
00E0E5	CINCO NETWORKS, INC.
00E0E6	INCAA Computers
00E0E7	RAYTHEON E-SYSTEMS, INC.
00E0E8	GRETACODER Data Systems AG
00E0E9	DATA LABS, INC.
00E0EA	INNOVAT COMMUNICATIONS, INC.
00E0EB	DIGICOM SYSTEMS, INCORPORATED
00E0EC	CELESTICA INC.
00E0ED	New Link
00E0EE	MAREL HF
00E0EF	Dionex
00E0F0	ABLER TECHNOLOGY, INC.
00E0F1	THAT CORPORATION
00E0F2	ARLOTTO COMNET, INC.
00E0F3	WebSprint Communications, Inc.
00E0F4	INSIDE Technology A/S
00E0F5	TELES AG
00E0F6	DECISION EUROPE
00E0F7	Cisco
00E0F8	DICNA CONTROL AB
00E0F9	Cisco
00E0FA	TRL TECHNOLOGY, LTD.
00E0FB	LEIGHTRONIX, INC.
00E0FC	HUAWEI TECHNOLOGIES CO.,LTD
00E0FD	A-TREND TECHNOLOGY CO., LTD.
00E0FE	Cisco
00E0FF	SECURITY DYNAMICS TECHNOLOGIES, Inc.
00E16D	Cisco Systems, Inc
00E175	AK-Systems Ltd
00E3B2	Samsung Electronics Co.,Ltd
00E400	Sichuan Changhong Electric Ltd.
00E666	ARIMA Communications Corp.
00E6D3	NIXDORF COMPUTER CORP.
00E6E8	Netzin Technology Corporation,.Ltd.
00E8AB	Meggitt Training Systems, Inc.
00EB2D	Sony Mobile Communications AB
00EBD5	Cisco Systems, Inc
00EEBD	HTC Corporation
00F051	KWB Gmbh
00F22C	Shanghai B-star Technology Co.,Ltd.
00F28B	Cisco Systems, Inc
00F3DB	WOO Sports
00F403	Orbis Systems Oy
00F46F	Samsung Electronics Co.,Ltd
00F4B9	Apple, Inc.
00F663	Cisco Systems, Inc
00F76F	Apple, Inc.
00F81C	HUAWEI TECHNOLOGIES CO.,LTD
00F82C	Cisco Systems, Inc
00F860	PT. Panggung Electric Citrabuana
00F871	DGS Denmark A/S
00FA3B	CLOOS ELECTRONIC GMBH
00FC58	WebSilicon Ltd.
00FC70	Intrepid Control Systems, Inc.
00FC8D	Hitron Technologies. Inc
00FD45	Hewlett Packard Enterprise
00FD4C	Nevatec
00FEC8	Cisco Systems, Inc
010ECF	PROFINET Multicast
020406	BBN				internal usage (not registered)
020701	Interlan [now Racal-InterLAN]	DEC (UNIBUS or QBUS), Apollo, Cisco
021C7C	PERQ SYSTEMS CORPORATION
022048	At least some 2810 send with locally assigned flag set
026060	3com
026086	Satelcom MegaPac (UK)
02608C	3Com				IBM PC; Imagen; Valid; Cisco; Macintosh
027001	RACAL-DATACOM
0270B0	M/A-COM INC. COMPANIES
0270B3	DATA RECALL LTD.
029D8E	CARDIAC RECORDERS, INC.
02A0C9	Intel
02AA3C	Olivetti
02BB01	OCTOTHORPE CORP.
02C08C	3COM CORPORATION
02CF1C	Communication Machinery Corporation
02CF1F	CMC
02E03B	Prominet Corporation		Gigabit Ethernet Switch
02E6D3	BTI (Bus-Tech, Inc.)		IBM Mainframes
04021F	HUAWEI TECHNOLOGIES CO.,LTD
0404EA	Valens Semiconductor Ltd.
040A83	Alcatel-               # Alcatel-Lucent
040AE0	XMIT AG COMPUTER NETWORKS
040CCE	Apple, Inc.
040EC2	ViewSonic Mobile China Limited
041552	Apple, Inc.
04180F	Samsung Electronics Co.,Ltd
0418B6	Private
0418D6	Ubiquiti Networks Inc.
041A04	Waveip
041B94	Host Mobility AB
041BBA	Samsung Electronics Co.,Ltd
041D10	Dream Ware Inc.
041E64	Apple, Inc.
041E7A	Dspworks
04209A	Panasonic AVC Networks Company
04214C	Insight Energy Ventures LLC
042234	Wireless Standard Extensions
0425C5	HUAWEI TECHNOLOGIES CO.,LTD
042605	GFR Gesellschaft für Regelungstechnik und Energieeinsparung mbH
042665	Apple, Inc.
042758	HUAWEI TECHNOLOGIES CO.,LTD
042AE2	Cisco Systems, Inc
042BBB	PicoCELA, Inc.
042DB4	First Property (Beijing) Co., Ltd Modern MOMA Branch
042F56	ATOCS (Shenzhen) LTD
043110	Inspur Group Co., Ltd.
0432F4	Partron
043389	HUAWEI TECHNOLOGIES CO.,LTD
043604	Gyeyoung I&T
043D98	ChongQing QingJia Electronics CO.,LTD
044169	Gopro
0444A1	TELECON GALICIA,S.A.
044665	Murata Manufacturing Co., Ltd.
04489A	Apple, Inc.
044A50	Ramaxel Technology (Shenzhen) limited company
044BED	Apple, Inc.
044BFF	GuangZhou Hedy Digital Technology Co., Ltd
044CEF	Fujian Sanao Technology Co.,Ltd
044E06	Ericsson AB
044E5A	ARRIS Group, Inc.
044F8B	Adapteva, Inc.
044FAA	Ruckus Wireless
0452C7	Bose Corporation
0452F3	Apple, Inc.
0453D5	Sysorex Global Holdings
045453	Apple, Inc.
0455CA	BriView (Xiamen) Corp.
045604	Gionee Communication Equipment Co.,Ltd.
04572F	Sertel Electronics UK Ltd
04586F	Sichuan Whayer information industry Co.,LTD
045A95	Nokia Corporation
045C06	Zmodo Technology Corporation
045C8E	gosund GROUP CO.,LTD
045D4B	Sony Corporation
045D56	camtron industrial inc.
045FA7	Shenzhen Yichen Technology Development Co.,LTD
046169	MEDIA GLOBAL LINKS CO., LTD.
046273	Cisco Systems, Inc
0462D7	ALSTOM HYDRO FRANCE
0463E0	Nome Oy
046565	Testop
046785	scemtec Hard- und Software fuer Mess- und Steuerungstechnik GmbH
0469F8	Apple, Inc.
046C9D	Cisco Systems, Inc
046D42	Bryston Ltd.
046E02	OpenRTLS Group
046E49	TaiYear Electronic Technology (Suzhou) Co., Ltd
0470BC	Globalstar Inc.
0474A1	Aligera Equipamentos Digitais Ltda
047503	HUAWEI TECHNOLOGIES CO.,LTD
0475F5	Csst
04766E	ALPS ELECTRIC CO.,LTD.
047863	Shanghai MXCHIP Information Technology Co., Ltd.
047D50	Shenzhen Kang Ying Technology Co.Ltd.
047D7B	QUANTA COMPUTER INC.
047E4A	moobox CO., Ltd.
0481AE	Clack Corporation
04848A	7INOVA TECHNOLOGY LIMITED
048845	Bay Networks			token ring line card
04888C	Eifelwerk Butler Systeme GmbH
0488E2	Beats Electronics LLC
048A15	Avaya Inc
048B42	Skspruce Technology Limited
048C03	ThinPAD Technology (Shenzhen)CO.,LTD
048D38	Netcore Technology Inc.
0492EE	iway AG
04946B	TECNO MOBILE LIMITED
0494A1	CATCH THE WIND INC
049573	zte corporation
0495E6	Tenda Technology Co.,Ltd.Dongguan branch
049645	WUXI SKY CHIP INTERCONNECTION TECHNOLOGY CO.,LTD.
049790	Lartech telecom LLC
0498F3	ALPS ELECTRIC CO.,LTD.
0499E6	Shenzhen Yoostar Technology Co., Ltd
049B9C	Eadingcore  Intelligent Technology Co., Ltd.
049C62	BMT Medical Technology s.r.o.
049F06	Smobile Co., Ltd.
049F81	NetScout Systems, Inc.
049FCA	HUAWEI TECHNOLOGIES CO.,LTD
04A151	Netgear
04A316	Texas Instruments
04A3F3	Emicon
04A82A	Nokia Corporation
04B0E7	HUAWEI TECHNOLOGIES CO.,LTD
04B3B6	Seamap (UK) Ltd
04B466	BSP Co., Ltd.
04B648	Zenner
04BA36	Li Seng Technology Ltd
04BBF9	Pavilion Data Systems Inc
04BD70	HUAWEI TECHNOLOGIES CO.,LTD
04BD88	Aruba Networks
04BF6D	ZyXEL Communications Corporation
04BFA8	ISB Corporation
04C05B	Tigo Energy
04C06F	HUAWEI TECHNOLOGIES CO.,LTD
04C09C	Tellabs Inc.
04C103	Clover Network, Inc.
04C1B9	Fiberhome Telecommunication Technologies Co.,LTD
04C23E	HTC Corporation
04C5A4	Cisco Systems, Inc
04C880	Samtec Inc
04C991	Phistek INC.
04C9D9	Echostar Technologies Corp
04CB1D	Traka plc
04CE14	Wilocity LTD.
04CF25	MANYCOLORS, INC.
04D3CF	Apple, Inc.
04D437	Znv
04D783	Y&H E&C Co.,LTD.
04DAD2	Cisco Systems, Inc
04DB56	Apple, Inc.
04DB8A	Suntech International Ltd.
04DD4C	Velocytech
04DEDB	Rockport Networks Inc
04DEF2	Shenzhen ECOM Technology Co. Ltd
04DF69	Car Connectivity Consortium
04E0C4	Triumph-               # TRIUMPH-ADLER AG
04E1C8	IMS Soluções em Energia Ltda.
04E2F8	AEP Ticketing solutions srl
04E451	Texas Instruments
04E536	Apple, Inc.
04E548	Cohda Wireless Pty Ltd
04E662	Acroname Inc.
04E676	AMPAK Technology, Inc.
04E9E5	PJRC.COM, LLC
04EE91	x-fabric GmbH
04F021	Compex Systems Pte Ltd
04F13E	Apple, Inc.
04F17D	Tarana Wireless
04F4BC	Xena Networks
04F7E4	Apple, Inc.
04F8C2	Flaircomm Microelectronics, Inc.
04F938	HUAWEI TECHNOLOGIES CO.,LTD
04FE31	Samsung Electronics Co.,Ltd
04FE7F	Cisco Systems, Inc
04FE8D	HUAWEI TECHNOLOGIES CO.,LTD
04FEA1	Fihonest communication co.,Ltd
04FF51	NOVAMEDIA INNOVISION SP. Z O.O.
080001	Computer Vision
080002	3Com
080003	ACC
080004	CROMEMCO INCORPORATED
080005	Symbolics			Symbolics LISP machines
080006	Siemens Nixdorf			PC clone
080007	Apple
080008	BBN
080009	HP
08000A	Nestar Systems
08000B	Unisys also Ascom-Timeplex (former Unisys subsidiary)
08000C	MIKLYN DEVELOPMENT CO.
08000D	ICL (International Computers, Ltd.)
08000E	Ncr/At&T
08000F	SMC (Standard Microsystems Corp.)
080010	AT&T [misrepresentation of 800010?]
080011	Tektronix, Inc.
080012	BELL ATLANTIC INTEGRATED SYST.
080013	Exxon
080014	Excelan				BBN Butterfly, Masscomp, Silicon Graphics
080015	STC BUSINESS SYSTEMS
080016	BARRISTER INFO SYS CORP
080017	National Semiconductor Corp. (used to have Network System Corp., wrong NSC)
080018	PIRELLI FOCOM NETWORKS
080019	GENERAL ELECTRIC CORPORATION
08001A	Data General
08001B	Data General
08001C	KDD-KOKUSAI DEBNSIN DENWA CO.
08001D	ABLE COMMUNICATIONS INC.
08001E	Apollo
08001F	Sharp
080020	Sun
080021	3M COMPANY
080022	NBI (Nothing But Initials)
080023	Matsushita Denso
080024	10NET COMMUNICATIONS/DCA
080025	Cdc
080026	Norsk Data (Nord)
080027	PCS Computer Systems GmbH
080028	TI				Explorer
080029	Megatek Corporation
08002A	MOSAIC TECHNOLOGIES INC.
08002B	Dec
08002C	BRITTON LEE INC.
08002D	LAN-TEC INC.
08002E	Metaphor
08002F	Prime Computer			Prime 50-Series LHC300
080030	Cern
080031	LITTLE MACHINES INC.
080032	Tigan
080033	BAUSCH & LOMB
080034	FILENET CORPORATION
080035	MICROFIVE CORPORATION
080036	Intergraph			CAE stations
080037	Fuji Xerox
080038	Bull
080039	Spider Systems
08003A	ORCATECH INC.
08003B	Torus Systems
08003C	SCHLUMBERGER WELL SERVICES
08003D	Cadnetix
08003E	Motorola
08003F	FRED KOSCHARA ENTERPRISES
080040	FERRANTI COMPUTER SYS. LIMITED
080041	DCA (Digital Comm. Assoc.)
080042	JAPAN MACNICS CORP.
080043	PIXEL COMPUTER INC.
080044	DSI (DAVID Systems, Inc.)
080045	???? (maybe Xylogics, but they claim not to know this number)
080046	Sony
080047	Sequent
080048	Eurotherm Gauging Systems
080049	Univation
08004A	BANYAN SYSTEMS INC.
08004B	Planning Research Corp.
08004C	Encore
08004D	CORVUS SYSTEMS INC.
08004E	BICC	[3com bought BICC, so may appear on 3com equipment as well]
08004F	CYGNET SYSTEMS
080050	DAISY SYSTEMS CORP.
080051	Experdata
080052	Insystec
080053	MIDDLE EAST TECH. UNIVERSITY
080055	STANFORD TELECOMM. INC.
080056	Stanford University
080057	Evans & Sutherland (?)
080058	???				DECsystem-20
080059	A/S MYCRON
08005A	Ibm
08005B	VTA TECHNOLOGIES INC.
08005C	FOUR PHASE SYSTEMS
08005D	GOULD INC.
08005E	COUNTERPOINT COMPUTER INC.
08005F	SABER TECHNOLOGY CORP.
080060	INDUSTRIAL NETWORKING INC.
080061	JAROGATE LTD.
080062	General Dynamics
080063	Plessey
080064	Sitasys AG
080065	GENRAD INC.
080066	AGFA				printers, phototypesetters etc.
080067	Comdesign
080068	Ridge
080069	SGI
08006A	Attst?		# ATTst (?)
08006B	ACCEL TECHNOLOGIES INC.
08006C	SUNTEK TECHNOLOGY INT'L
08006D	WHITECHAPEL COMPUTER WORKS
08006E	Excelan
08006F	PHILIPS APELDOORN B.V.
080070	Mitsubishi
080071	MATRA (DSIE)
080072	XEROX CORP UNIV GRANT PROGRAM
080073	TECMAR INC.
080074	Casio
080075	DDE (Danish Data Elektronik A/S)
080076	PC LAN TECHNOLOGIES
080077	TSL (now Retix)
080078	ACCELL CORPORATION
080079	SGI
08007A	Indata
08007B	SANYO ELECTRIC CO. LTD.
08007C	Vitalink			TransLAN III
08007E	AMALGAMATED WIRELESS(AUS) LTD
08007F	CARNEGIE-MELLON UNIVERSITY
080080	Xios
080081	Crosfield Electronics
080082	VERITAS SOFTWARE
080083	Seiko Denshi
080084	TOMEN ELECTRONICS CORP.
080085	Elxsi
080086	Imagen/QMS
080087	Xyplex				terminal servers
080088	McDATA Corporation
080089	Kinetics			AppleTalk-Ethernet interface
08008A	PerfTech, Inc.
08008B	Pyramid
08008C	NETWORK RESEARCH CORPORATION
08008D	XyVision			XyVision machines
08008E	Tandem / Solbourne Computer ?
08008F	Chipcom Corp.
080090	Retix
08010F	SICHUAN TIANYI COMHEART TELECOMCO.,LTD
08028E	Netgear
080371	KRG CORPORATE
080581	Roku, Inc.
0805CD	DongGuang EnMai Electronic Product Co.Ltd.
0808C2	Samsung Electronics Co.,Ltd
0808EA	Amsc
0809B6	Masimo Corp
080A4E	Planet Bingo® — 3rd Rock Gaming®
080C0B	SysMik GmbH Dresden
080CC9	Mission Technology Group, dba Magma
080D84	GECO, Inc.
080EA8	Velex s.r.l.
080FFA	KSP INC.
08115E	Bitel Co., Ltd.
081196	Intel Corporate
081443	UNIBRAIN S.A.
081651	SHENZHEN SEA STAR TECHNOLOGY CO.,LTD
081735	Cisco Systems, Inc
0817F4	IBM Corp
08181A	zte corporation
08184C	A. S. Thomas, Inc.
0819A6	HUAWEI TECHNOLOGIES CO.,LTD
081DFB	Shanghai Mexon Communication Technology Co.,Ltd
081F3F	WondaLink Inc.
081F71	TP-LINK TECHNOLOGIES CO.,LTD.
081FEB	Bincube
081FF3	Cisco Systems, Inc
0821EF	Samsung Electronics Co.,Ltd
0823B2	vivo Mobile Communication Co., Ltd.
082522	Advansee
082719	APS systems/electronic AG
0827CE	NAGANO KEIKI CO., LTD.
082AD0	SRD Innovations Inc.
082CB0	Network Instruments
082E5F	Hewlett Packard
083571	CASwell INC.
08373D	Samsung Electronics Co.,Ltd
08379C	Topaz Co. LTD.
0838A5	Funkwerk plettac electronic GmbH
083A5C	Junilab, Inc.
083AB8	Shinoda Plasma Co., Ltd.
083D88	Samsung Electronics Co.,Ltd
083E0C	ARRIS Group, Inc.
083E5D	Sagemcom Broadband SAS
083E8E	Hon Hai Precision Ind. Co.,Ltd.
083F3E	WSH GmbH
083F76	Intellian Technologies, Inc.
083FBC	zte corporation
084027	Gridstore Inc.
084656	Veo-Labs
08482C	Raycore Taiwan Co., LTD.
084E1C	H2A Systems, LLC
084EBF	Broad Net Mux Corporation
08512E	Orion Diagnostica Oy
085240	EbV Elektronikbau- und Vertriebs GmbH
085700	TP-LINK TECHNOLOGIES CO.,LTD.
085AE0	Recovision Technology Co., Ltd.
085B0E	Fortinet, Inc.
085BDA	CliniCare LTD
085DDD	MERCURY CORPORATION
08606E	ASUSTek COMPUTER INC.
086266	ASUSTek COMPUTER INC.
086361	HUAWEI TECHNOLOGIES CO.,LTD
086698	Apple, Inc.
0868D0	Japan System Design
0868EA	EITO ELECTRONICS CO., LTD.
086A0A	ASKEY COMPUTER CORP
086D41	Apple, Inc.
086DF2	Shenzhen MIMOWAVE Technology Co.,Ltd
087045	Apple, Inc.
087402	Apple, Inc.
0874F6	Winterhalter Gastronom GmbH
087572	Obelux Oy
087618	ViE Technologies Sdn. Bhd.
087695	Auto Industrial Co., Ltd.
0876FF	Thomson Telecom Belgium
087999	AIM GmbH
087A4C	HUAWEI TECHNOLOGIES CO.,LTD
087BAA	SVYAZKOMPLEKTSERVICE, LLC
087CBE	Quintic Corp.
087D21	Altasec technology corporation
088039	Cisco SPVTG
0881BC	HongKong Ipro Technology Co., Limited
0881F4	Juniper Networks
088620	TECNO MOBILE LIMITED
08863B	Belkin International Inc.
088C2C	Samsung Electronics Co.,Ltd
088DC8	Ryowa Electronics Co.,Ltd
088E4F	SF Software Solutions
088F2C	Hills Sound Vision & Lighting
0894EF	Wistron Infocomm (Zhongshan) Corporation
08952A	Technicolor CH USA Inc.
0896AD	Cisco Systems, Inc
0896D7	AVM GmbH
089758	Shenzhen Strong Rising Electronics Co.,Ltd DongGuan Subsidiary
089B4B	iKuai Networks
089E01	QUANTA COMPUTER INC.
089E08	Google, Inc.
089F97	LEROY AUTOMATION
08A12B	ShenZhen EZL Technology Co., Ltd
08A5C8	Sunnovo International Limited
08A95A	AzureWave Technology Inc.
08ACA5	Benu Video, Inc.
08AF78	Totus Solutions, Inc.
08B258	Juniper Networks
08B2A3	Cynny Italia S.r.L.
08B4CF	Abicom International
08B738	Lite-On Technogy Corp.
08B7EC	Wireless Seismic
08BBCC	AK-NORD EDV VERTRIEBSGES. mbH
08BD43	Netgear
08BE09	Astrol Electronic AG
08BE77	Green Electronics
08C021	HUAWEI TECHNOLOGIES CO.,LTD
08C6B3	QTECH LLC
08CA45	Toyou Feiji Electronics Co., Ltd.
08CC68	Cisco Systems, Inc
08CCA7	Cisco Systems, Inc
08CD9B	samtec automotive electronics & software GmbH
08D09F	Cisco Systems, Inc
08D0B7	Qingdao Hisense Communications Co.,Ltd.
08D29A	Proformatique
08D34B	Techman Electronics (Changshu) Co., Ltd.
08D40C	Intel Corporate
08D42B	Samsung Electronics Co.,Ltd
08D5C0	Seers Technology Co., Ltd
08D833	Shenzhen RF Technology Co., Ltd
08DF1F	Bose Corporation
08E5DA	NANJING FUJITSU COMPUTER PRODUCTS CO.,LTD.
08E672	JEBSEE ELECTRONICS CO.,LTD.
08E84F	HUAWEI TECHNOLOGIES CO.,LTD
08EA40	SHENZHEN BILIAN ELECTRONIC CO.，LTD
08EA44	Aerohive Networks Inc.
08EB29	Jiangsu Huitong Group Co.,Ltd.
08EB74	HUMAX Co., Ltd.
08EBED	World Elite Technology Co.,LTD
08ECA9	Samsung Electronics Co.,Ltd
08ED02	IEEE Registration Authority
08EDB9	Hon Hai Precision Ind. Co.,Ltd.
08EE8B	Samsung Electronics Co.,Ltd
08EF3B	MCS Logic Inc.
08EFAB	SAYME WIRELESS SENSOR NETWORK
08F1B7	Towerstream Corpration
08F2F4	Net One Partners Co.,Ltd.
08F6F8	GET Engineering
08F728	GLOBO Multimedia Sp. z o.o. Sp.k.
08FAE0	Fohhn Audio AG
08FC52	OpenXS BV
08FC88	Samsung Electronics Co.,Ltd
08FD0E	Samsung Electronics Co.,Ltd
09006A	AT&T
0C0227	Technicolor CH USA Inc.
0C0400	Jantar d.o.o.
0C0535	Juniper Systems
0C1105	Ringslink (Xiamen) Network Communication Technologies Co., Ltd
0C1167	Cisco Systems, Inc
0C1262	zte corporation
0C130B	Uniqoteq Ltd.
0C1420	Samsung Electronics Co.,Ltd
0C1539	Apple, Inc.
0C15C5	SDTEC Co., Ltd.
0C17F1	Telecsys
0C191F	Inform Electronik
0C1A10	Acoustic Stream
0C1DAF	Xiaomi Communications Co Ltd
0C1DC2	SeAH Networks
0C2026	noax Technologies AG
0C2576	LONGCHEER TELECOMMUNICATION LIMITED
0C2724	Cisco Systems, Inc
0C2755	Valuable Techologies Limited
0C2A69	electric imp, incorporated
0C2AE7	Beijing General Research Institute of Mining and Metallurgy
0C2D89	QiiQ Communications Inc.
0C3021	Apple, Inc.
0C37DC	HUAWEI TECHNOLOGIES CO.,LTD
0C383E	Fanvil Technology Co., Ltd.
0C3956	Observator instruments
0C3C65	Dome Imaging Inc
0C3CCD	Universal Global Scientific Industrial Co., Ltd.
0C3E9F	Apple, Inc.
0C413E	Microsoft Corporation
0C45BA	HUAWEI TECHNOLOGIES CO.,LTD
0C469D	MS Sedco
0C473D	Hitron Technologies. Inc
0C47C9	Amazon Technologies Inc.
0C4885	LG Electronics (Mobile Communications)
0C4933	Sichuan Jiuzhou Electronic Technology Co., Ltd.
0C4C39	MitraStar Technology Corp.
0C4DE9	Apple, Inc.
0C4F5A	ASA-RT s.r.l.
0C5101	Apple, Inc.
0C51F7	CHAUVIN ARNOUX
0C54A5	PEGATRON CORPORATION
0C54B9	Nokia
0C5521	Axiros GmbH
0C565C	HyBroad Vision (Hong Kong) Technology Co Ltd
0C57EB	Mueller Systems
0C5A19	Axtion Sdn Bhd
0C5A9E	Wi-SUN Alliance
0C5CD8	DOLI Elektronik GmbH
0C5F35	Niagara Video Corporation
0C6076	Hon Hai Precision Ind. Co.,Ltd.
0C6127	Actiontec Electronics, Inc
0C61CF	Texas Instruments
0C63FC	Nanjing Signway Technology Co., Ltd
0C6803	Cisco Systems, Inc
0C6AE6	Stanley Security Solutions
0C6E4F	PrimeVOLT Co., Ltd.
0C6F9C	Shaw Communications Inc.
0C715D	Samsung Electronics Co.,Ltd
0C722C	TP-LINK TECHNOLOGIES CO.,LTD.
0C73BE	Dongguan Haimai Electronie Technology Co.,Ltd
0C74C2	Apple, Inc.
0C7523	BEIJING GEHUA CATV NETWORK CO.,LTD
0C756C	Anaren Microwave, Inc.
0C75BD	Cisco Systems, Inc
0C771A	Apple, Inc.
0C7D7C	Kexiang Information Technology Co, Ltd.
0C8112	Private
0C8230	SHENZHEN MAGNUS TECHNOLOGIES CO.,LTD
0C8268	TP-LINK TECHNOLOGIES CO.,LTD.
0C826A	Wuhan Huagong Genuine Optics Technology Co., Ltd
0C8411	A.O. Smith Water Products
0C8484	Zenovia Electronics Inc.
0C84DC	Hon Hai Precision Ind. Co.,Ltd.
0C8525	Cisco Systems, Inc
0C8610	Juniper Networks
0C8910	Samsung Electronics Co.,Ltd
0C8A87	AgLogica Holdings, Inc
0C8BFD	Intel Corporate
0C8C8F	Kamo Technology Limited
0C8CDC	Suunto Oy
0C8D98	TOP EIGHT IND CORP
0C8DDB	Cisco Meraki
0C9160	Hui Zhou Gaoshengda Technology Co.,LTD
0C924E	Rice Lake Weighing Systems
0C9301	PT. Prasimax Inovasi Teknologi
0C93FB	BNS Solutions
0C96BF	HUAWEI TECHNOLOGIES CO.,LTD
0C9B13	Shanghai Magic Mobile Telecommunication Co.Ltd.
0C9D56	Consort Controls Ltd
0C9E91	Sankosha Corporation
0CA138	Blinq Wireless Inc.
0CA2F4	Chameleon Technology (UK) Limited
0CA402	Alcatel-               # Alcatel-Lucent IPD
0CA42A	OB Telecom Electronic Technology Co., Ltd
0CA694	Sunitec Enterprise Co.,Ltd
0CAC05	Unitend Technologies Inc.
0CAF5A	GENUS POWER INFRASTRUCTURES LIMITED
0CB319	Samsung Electronics Co.,Ltd
0CB4EF	Digience Co.,Ltd.
0CB5DE	Alcatel Lucent
0CB912	JM-DATA GmbH
0CBC9F	Apple, Inc.
0CBD51	TCT mobile ltd
0CBF15	Genetec Inc.
0CBF3F	Shenzhen Lencotion Technology Co.,Ltd
0CC0C0	MAGNETI MARELLI SISTEMAS ELECTRONICOS MEXICO
0CC3A7	Meritec
0CC47A	Super Micro Computer, Inc.
0CC47E	EUCAST Co., Ltd.
0CC655	Wuxi YSTen Technology Co.,Ltd.
0CC66A	Nokia Corporation
0CC6AC	Dags
0CC731	Currant, Inc.
0CC81F	Summer Infant, Inc.
0CC9C6	Samwin Hong Kong Limited
0CCB8D	ASCO Numatics GmbH
0CCC26	Airenetworks
0CCDD3	EASTRIVER TECHNOLOGY CO., LTD.
0CCDFB	EDIC Systems Inc.
0CCFD1	SPRINGWAVE Co., Ltd
0CD292	Intel Corporate
0CD2B5	Binatone Telecommunication Pvt. Ltd
0CD502	Westell Technologies Inc.
0CD696	Amimon Ltd
0CD6BD	HUAWEI TECHNOLOGIES CO.,LTD
0CD746	Apple, Inc.
0CD7C2	Axium Technologies, Inc.
0CD86C	SHENZHEN FAST TECHNOLOGIES CO.,LTD
0CD996	Cisco Systems, Inc
0CD9C1	Visteon Corporation
0CDA41	Hangzhou H3C Technologies Co., Limited
0CDCCC	Inala Technologies
0CDDEF	Nokia Corporation
0CDFA4	Samsung Electronics Co.,Ltd
0CE0E4	PLANTRONICS, INC.
0CE5D3	DH electronics GmbH
0CE709	Fox Crypto B.V.
0CE725	Microsoft Corporation
0CE82F	Bonfiglioli Vectron GmbH
0CE936	ELIMOS srl
0CEEE6	Hon Hai Precision Ind. Co.,Ltd.
0CEF7C	AnaCom Inc
0CEFAF	IEEE Registration Authority
0CF019	Malgn Technology Co., Ltd.
0CF0B4	Globalsat International Technology Ltd
0CF361	Java Information
0CF3EE	EM Microelectronic
0CF405	Beijing Signalway Technologies Co.,Ltd
0CF4D5	Ruckus Wireless
0CF5A4	Cisco Systems, Inc
0CF893	ARRIS Group, Inc.
0CF9C0	BSkyB Ltd
0CFC83	Airoha Technology Corp.,
0CFD37	SUSE Linux GmbH
0CFE45	Sony Interactive Entertainment Inc.
100000	Private
10005A	Ibm
100090	HP
1000D4	DEC
1000E0	Apple A/UX			(modified addresses for licensing)
1000E8	NATIONAL SEMICONDUCTOR
1000FD	LaonPeople
1001CA	Ashley Butterworth
1002B5	Intel Corporate
100501	PEGATRON CORPORATION
1005B1	ARRIS Group, Inc.
1005CA	Cisco Systems, Inc
100723	IEEE Registration Authority
1008B1	Hon Hai Precision Ind. Co.,Ltd.
10090C	Janome Sewing Machine Co., Ltd.
100BA9	Intel Corporate
100C24	pomdevices, LLC
100D2F	Online Security Pty. Ltd.
100D32	Embedian, Inc.
100D7F	Netgear
100E2B	NEC CASIO Mobile Communications
100E7E	Juniper Networks
100F18	Fu Gang Electronic(KunShan)CO.,LTD
1010B6	McCain Inc
101212	Vivo International Corporation Pty Ltd
101218	Korins Inc.
101248	ITG, Inc.
101250	Integrated Device Technology (Malaysia) Sdn. Bhd.
101331	Technicolor
1013EE	Justec International Technology INC.
10189E	Elmo Motion Control
101B54	HUAWEI TECHNOLOGIES CO.,LTD
101C0C	Apple, Inc.
101D51	ON-Q LLC dba ON-Q Mesh Networks
101DC0	Samsung Electronics Co.,Ltd
101F74	Hewlett Packard
102279	ZeroDesktop, Inc.
1027BE	Tvip
102831	Morion Inc.
102AB3	Xiaomi Communications Co Ltd
102C83	Ximea
102D96	Looxcie Inc.
102EAF	Texas Instruments
102F6B	Microsoft Corporation
103047	Samsung Electronics Co.,Ltd
103378	FLECTRON Co., LTD
103711	Simlink AS
103B59	Samsung Electronics Co.,Ltd
103DEA	HFC Technology (Beijing) Ltd. Co.
1040F3	Apple, Inc.
10417F	Apple, Inc.
104369	Soundmax Electronic Limited
10445A	Shaanxi Hitech Electronic Co., LTD
1045BE	Norphonic AS
1045F8	LNT-Automation GmbH
104780	HUAWEI TECHNOLOGIES CO.,LTD
1048B1	Beijing Duokan Technology Limited
104A7D	Intel Corporate
104B46	Mitsubishi Electric Corporation
104D77	Innovative Computer Engineering
104E07	Shanghai Genvision Industries Co.,Ltd
104FA8	Sony Corporation
105172	HUAWEI TECHNOLOGIES CO.,LTD
105611	ARRIS Group, Inc.
1056CA	Peplink International Ltd.
105887	Fiberhome Telecommunication Technologies Co.,LTD
105AF7	ADB Italia
105C3B	Perma-Pipe, Inc.
105CBF	DuroByte Inc
105F06	Actiontec Electronics, Inc
105F49	Cisco SPVTG
10604B	Hewlett Packard
1062C9	Adatis GmbH & Co. KG
1062EB	D-Link International
1064E2	ADFweb.com s.r.l.
1065A3	Core Brands LLC
1065CF	Iqsim
106682	NEC Platforms, Ltd.
10683F	LG Electronics (Mobile Communications)
106F3F	BUFFALO.INC
106FEF	Ad-Sol Nissin Corp
1071F9	Cloud Telecomputers, LLC
107223	TELLESCOM INDUSTRIA E COMERCIO EM TELECOMUNICACAO
10768A	Eocell
1077B0	Fiberhome Telecommunication Technologies Co.,LTD
1077B1	Samsung Electronics Co.,Ltd
10785B	Actiontec Electronics, Inc
107873	Shenzhen Jinkeyi Communication Co., Ltd.
1078CE	Hanvit SI, Inc.
1078D2	Elitegroup Computer Systems Co.,Ltd.
107A86	U&U ENGINEERING INC.
107BEF	ZyXEL Communications Corporation
107D1A	Dell Inc.
1083D2	Microseven Systems, LLC
10868C	ARRIS Group, Inc.
10880F	Daruma Telecomunicações e Informática S.A.
1088CE	Fiberhome Telecommunication Technologies Co.,LTD
108A1B	RAONIX Inc.
108CCF	Cisco Systems, Inc
109266	Samsung Electronics Co.,Ltd
1093E9	Apple, Inc.
10954B	Megabyte Ltd.
109836	Dell Inc.
109AB9	Tosibox Oy
109ADD	Apple, Inc.
109FA9	Actiontec Electronics, Inc
10A13B	FUJIKURA RUBBER LTD.
10A5D0	Murata Manufacturing Co., Ltd.
10A659	Mobile Create Co.,Ltd.
10A743	SK Mtek Limited
10A932	Beijing Cyber Cloud Technology Co. ,Ltd.
10AE60	Private
10AF78	Shenzhen ATUE Technology Co., Ltd
10B1F8	HUAWEI TECHNOLOGIES CO.,LTD
10B26B	base Co.,Ltd.
10B713	Private
10B7F6	Plastoform Industries Ltd.
10B9FE	Lika srl
10BAA5	GANA I&C CO., LTD
10BD18	Cisco Systems, Inc
10BD55	Q-Lab Corporation
10BEF5	D-Link International
10BF48	ASUSTek COMPUTER INC.
10C07C	Blu-ray Disc Association
10C2BA	UTT Co., Ltd.
10C37B	ASUSTek COMPUTER INC.
10C586	BIO SOUND LAB CO., LTD.
10C60C	Domino UK Ltd
10C61F	HUAWEI TECHNOLOGIES CO.,LTD
10C67E	SHENZHEN JUCHIN TECHNOLOGY CO., LTD
10C6FC	Garmin International
10C73F	Midas Klark Teknik Ltd
10CA81	Precia
10CC1B	Liverock technologies,INC
10CCDB	AXIMUM PRODUITS ELECTRONIQUES
10CDAE	Avaya Inc
10D07A	AMPAK Technology, Inc.
10D0AB	zte corporation
10D1DC	INSTAR Deutschland GmbH
10D38A	Samsung Electronics Co.,Ltd
10D542	Samsung Electronics Co.,Ltd
10DA43	Netgear
10DDB1	Apple, Inc.
10DDF4	Maxway Electronics CO.,LTD
10DEE4	automationNEXT GmbH
10DF8B	Shenzhen CareDear Communication Technology Co.,Ltd
10E2D5	Qi Hardware Inc.
10E3C7	Seohwa Telecom
10E4AF	APR, LLC
10E68F	KWANGSUNG ELECTRONICS KOREA CO.,LTD.
10E6AE	Source Technologies, LLC
10E878	Nokia
10E8EE	PhaseSpace
10EA59	Cisco SPVTG
10EED9	Canoga Perkins Corporation
10F005	Intel Corporate
10F311	Cisco Systems, Inc
10F3DB	Gridco Systems, Inc.
10F49A	T3 Innovation
10F681	vivo Mobile Communication Co., Ltd.
10F96F	LG Electronics (Mobile Communications)
10F9EE	Nokia Corporation
10FACE	Reacheng Communication Technology Co.,Ltd
10FBF0	KangSheng LTD.
10FC54	Shany Electronic Co., Ltd.
10FEED	TP-LINK TECHNOLOGIES CO.,LTD.
1100AA	Private
111111	Private
1402EC	Hewlett Packard Enterprise
140467	SNK Technologies Co.,Ltd.
140708	Private
1407E0	Abrantix AG
140C5B	PLNetworks
140C76	FREEBOX SAS
140D4F	Flextronics International
14109F	Apple, Inc.
141330	Anakreon UK LLP
141357	ATP Electronics, Inc.
14144B	FUJIAN STAR-NET COMMUNICATION CO.,LTD
1414E6	Ningbo Sanhe Digital Co.,Ltd
14157C	TOKYO COSMOS ELECTRIC CO.,LTD.
141877	Dell Inc.
141A51	Treetech Sistemas Digitais
141AA3	Motorola Mobility LLC, a Lenovo Company
141BBD	Volex Inc.
141BF0	Intellimedia Systems Ltd
141F78	Samsung Electronics Co.,Ltd
141FBA	IEEE Registration Authority
1422DB	eero inc.
1423D7	EUTRONIX CO., LTD.
142971	NEMOA ELECTRONICS (HK) CO. LTD
142BD2	Armtel Ltd.
142BD6	Guangdong Appscomm Co.,Ltd
142D27	Hon Hai Precision Ind. Co.,Ltd.
142D8B	Incipio Technologies, Inc
142DF5	Amphitech
142FFD	LT SECURITY INC
143004	HUAWEI TECHNOLOGIES CO.,LTD
14307A	Avermetrics
1430C6	Motorola Mobility LLC, a Lenovo Company
1432D1	Samsung Electronics Co.,Ltd
143365	TEM Mobile Limited
14358B	Mediabridge Products, LLC.
1435B3	Future Designs, Inc.
143605	Nokia Corporation
1436C6	Lenovo Mobile Communication Technology Ltd.
14373B	PROCOM Systems
143AEA	Dynapower Company LLC
143DF2	Beijing Shidai Hongyuan Network Communication Co.,Ltd
143E60	Nokia
143EBF	zte corporation
143F27	Noccela Oy
144146	Honeywell (China) Co., LTD
1441E2	Monaco Enterprises, Inc.
144319	Creative&Link Technology Limited
1446E4	Avistel
14488B	Shenzhen Doov Technology Co.,Ltd
144978	Digital Control Incorporated
1449E0	SAMSUNG ELECTRO-MECHANICS(THAILAND)
144C1A	Max Communication GmbH
144D67	Zioncom Electronics (Shenzhen) Ltd.
144FD7	IEEE Registration Authority
145412	Entis Co., Ltd.
145645	Savitech Corp.
14568E	Samsung Electronics Co.,Ltd
1458D0	Hewlett Packard
145A05	Apple, Inc.
145A83	Logi-D inc
145BD1	ARRIS Group, Inc.
145F94	HUAWEI TECHNOLOGIES CO.,LTD
146080	zte corporation
146102	Alpine Electronics, Inc.
14612F	Avaya Inc
146308	JABIL CIRCUIT (SHANGHAI) LTD.
146A0B	Cypress Electronics Limited
146B72	Shenzhen Fortune Ship Technology Co., Ltd.
146E0A	Private
147373	TUBITAK UEKAE
147411	Rim
147590	TP-LINK TECHNOLOGIES CO.,LTD.
147DB3	JOA TELECOM.CO.,LTD
147DC5	Murata Manufacturing Co., Ltd.
14825B	Hefei Radio Communication Technology Co., Ltd
148692	TP-LINK TECHNOLOGIES CO.,LTD.
14893E	VIXTEL TECHNOLOGIES LIMTED
148951	LCFC(HeFei) Electronics Technology co., ltd
1489FD	Samsung Electronics Co.,Ltd
148A70	ADS GmbH
148F21	Garmin International
148FC6	Apple, Inc.
149090	KongTop industrial(shen zhen)CO.,LTD
149182	Belkin International Inc.
149448	BLU CASTLE S.A.
14987D	Technicolor CH USA Inc.
1499E2	Apple, Inc.
149A10	Microsoft Corporation
149D09	HUAWEI TECHNOLOGIES CO.,LTD
149ECF	Dell Inc.
149FE8	Lenovo Mobile Communication Technology Ltd.
14A0F8	HUAWEI TECHNOLOGIES CO.,LTD
14A364	Samsung Electronics Co.,Ltd
14A51A	HUAWEI TECHNOLOGIES CO.,LTD
14A62C	S.M. Dezac S.A.
14A78B	Zhejiang Dahua Technology Co., Ltd.
14A86B	ShenZhen Telacom Science&Technology Co., Ltd
14A9E3	MST CORPORATION
14ABC5	Intel Corporate
14ABF0	ARRIS Group, Inc.
14AEDB	VTech Telecommunications Ltd.
14B126	Industrial Software Co
14B1C8	InfiniWing, Inc.
14B31F	Dell Inc.
14B370	Gigaset Digital Technology (Shenzhen) Co., Ltd.
14B484	Samsung Electronics Co.,Ltd
14B73D	ARCHEAN Technologies
14B7F8	Technicolor CH USA Inc.
14B837	Shenzhen YOUHUA Technology Co., Ltd
14B968	HUAWEI TECHNOLOGIES CO.,LTD
14BB6E	Samsung Electronics Co.,Ltd
14BD61	Apple, Inc.
14C089	DUNE HD LTD
14C126	Nokia Corporation
14C1FF	ShenZhen QianHai Comlan communication Co.,LTD
14C21D	Sabtech Industries
14C3C2	K.A. Schmersal GmbH & Co. KG
14C913	LG Electronics
14CC20	TP-LINK TECHNOLOGIES CO.,LTD.
14CF8D	OHSUNG ELECTRONICS CO., LTD.
14CF92	TP-LINK TECHNOLOGIES CO.,LTD.
14CFE2	ARRIS Group, Inc.
14D11F	HUAWEI TECHNOLOGIES CO.,LTD
14D4FE	ARRIS Group, Inc.
14D64D	D-Link International
14D76E	CONCH ELECTRONIC Co.,Ltd
14DAE9	ASUSTek COMPUTER INC.
14DB85	S NET MEDIA
14DDA9	ASUSTek COMPUTER INC.
14DDE5	Mpmkvvcl
14E4EC	mLogic LLC
14E6E4	TP-LINK TECHNOLOGIES CO.,LTD.
14E7C8	Integrated Device Technology (Malaysia) Sdn. Bhd.
14EB33	BSMediasoft Co., Ltd.
14EDA5	Wächter GmbH Sicherheitssysteme
14EDBB	2Wire Inc
14EDE4	Kaiam Corporation
14EE9D	AirNav Systems LLC
14F0C5	Xtremio Ltd.
14F28E	ShenYang ZhongKe-Allwin Technology Co.LTD
14F42A	Samsung Electronics Co.,Ltd
14F65A	Xiaomi Communications Co Ltd
14F893	Wuhan FiberHome Digital Technology Co.,Ltd.
14FEAF	SAGITTAR LIMITED
14FEB5	Dell Inc.
18002D	Sony Mobile Communications AB
1800DB	Fitbit Inc.
18017D	Harbin Arteor technology co., LTD
1801E3	Bittium Wireless Ltd
180373	Dell Inc.
1803FA	IBT Interfaces
180675	Dilax Intelcom GmbH
180B52	Nanotron Technologies GmbH
180C14	iSonea Limited
180C77	Westinghouse Electric Company, LLC
180CAC	CANON INC.
18104E	CEDINT-UPM
181212	Cepton Technologies
181420	TEB SAS
181456	Nokia Corporation
1816C9	Samsung Electronics Co.,Ltd
181714	Daewoois
181725	Cameo Communications, Inc.
18193F	Tamtron Oy
181BEB	Actiontec Electronics, Inc
181E78	Sagemcom Broadband SAS
181EB0	Samsung Electronics Co.,Ltd
182012	Aztech Associates Inc.
182032	Apple, Inc.
1820A6	Sage Co., Ltd.
182195	Samsung Electronics Co.,Ltd
18227E	Samsung Electronics Co.,Ltd
182666	Samsung Electronics Co.,Ltd
182861	AirTies Wireless Networks
182A7B	Nintendo Co., Ltd.
182B05	8D Technologies
182C91	Concept Development, Inc.
183009	Woojin Industrial Systems Co., Ltd.
1832A2	LAON TECHNOLOGY CO., LTD.
18339D	Cisco Systems, Inc
183451	Apple, Inc.
1836FC	Elecsys International Corporation
183825	Wuhan Lingjiu High-tech Co.,Ltd.
183864	CAP-TECH INTERNATIONAL CO., LTD.
183919	Unicoi Systems
183A2D	Samsung Electronics Co.,Ltd
183BD2	BYD Precision Manufacture Company Ltd.
183DA2	Intel Corporate
183F47	Samsung Electronics Co.,Ltd
1840A4	Shenzhen Trylong Smart Science and Technology Co., Ltd.
18421D	Private
18422F	Alcatel Lucent
184462	Riava Networks, Inc.
1844E6	zte corporation
184617	Samsung Electronics Co.,Ltd
1848D8	Fastback Networks
184A6F	Alcatel-               # Alcatel-Lucent Shanghai Bell Co., Ltd
184E94	MESSOA TECHNOLOGIES INC.
184F32	Hon Hai Precision Ind. Co.,Ltd.
185207	SICHUAN TIANYI COMHEART TELECOMCO., LTD
185253	Pixord Corporation
1853E0	Hanyang Digitech Co.Ltd
18550F	Cisco SPVTG
185933	Cisco SPVTG
185936	Xiaomi Communications Co Ltd
185AE8	Zenotech.Co.,Ltd
185D9A	BobjGear LLC
185E0F	Intel Corporate
1861C7	lemonbeat GmbH
18622C	Sagemcom Broadband SAS
186472	Aruba Networks
186571	Top Victory Electronics (Taiwan) Co., Ltd.
186590	Apple, Inc.
1866DA	Dell Inc.
1866E3	Veros Systems, Inc.
18673F	Hanover Displays Limited
186751	KOMEG Industrielle Messtechnik GmbH
1867B0	Samsung Electronics Co.,Ltd
18686A	zte corporation
186882	BewardR&               # Beward R&D Co., Ltd.
1868CB	Hangzhou Hikvision Digital Technology Co.,Ltd.
186D99	Adanis Inc.
187117	eta plus electronic gmbh
187532	SICHUAN TIANYI COMHEART TELECOMCO., LTD
1879A2	GMJ ELECTRIC LIMITED
187A93	AMICCOM Electronics Corporation
187C81	Valeo Vision Systems
187ED5	shenzhen kaism technology Co. Ltd
1880CE	Barberry Solutions Ltd
1880F5	Alcatel-               # Alcatel-Lucent Shanghai Bell Co., Ltd
188219	Alibaba Cloud Computing Ltd.
188331	Samsung Electronics Co.,Ltd
1883BF	Arcadyan Technology Corporation
188410	CoreTrust Inc.
18863A	DIGITAL ART SYSTEM
1886AC	Nokia Danmark A/S
188796	HTC Corporation
188857	Beijing Jinhong Xi-Dian Information Technology Corp.
18895B	Samsung Electronics Co.,Ltd
1889DF	CerebrEX Inc.
188B15	ShenZhen ZhongRuiJing Technology co.,LTD
188B45	Cisco Systems, Inc
188B9D	Cisco Systems, Inc
188ED5	TP Vision Belgium N.V. - innovation site Brugge
188EF9	G2C Co. Ltd.
18922C	Virtual Instruments
1893D7	Texas Instruments
1897FF	TechFaith Wireless Technology Limited
1899F5	Sichuan Changhong Electric Ltd.
189A67	CSE-Servelec Limited
189C5D	Cisco Systems, Inc
189EFC	Apple, Inc.
18A3E8	Fiberhome Telecommunication Technologies Co.,LTD
18A6F7	TP-LINK TECHNOLOGIES CO.,LTD.
18A905	Hewlett Packard
18A958	PROVISION THAI CO., LTD.
18A99B	Dell Inc.
18AA45	Fon Technology
18ABF5	Ultra Electronics Electrics
18AD4D	Polostar Technology Corporation
18AEBB	Siemens Convergence Creators GmbH&Co.KG
18AF61	Apple, Inc.
18AF8F	Apple, Inc.
18AF9F	DIGITRONIC Automationsanlagen GmbH
18B169	Sonicwall
18B209	Torrey Pines Logic, Inc
18B3BA	Netlogic AB
18B430	Nest Labs Inc.
18B591	I-Storm
18B79E	Invoxia
18BDAD	L-TECH CORPORATION
18C086	Broadcom
18C451	Tucson Embedded Systems
18C501	SHENZHEN GONGJIN ELECTRONICS CO.,LT
18C58A	HUAWEI TECHNOLOGIES CO.,LTD
18C8E7	Shenzhen Hualistone Technology Co.,Ltd
18CC23	Philio Technology Corporation
18CF5E	Liteon Technology Corporation
18D071	DASAN CO., LTD.
18D276	HUAWEI TECHNOLOGIES CO.,LTD
18D5B6	SMG Holdings LLC
18D66A	Inmarsat
18D6C7	TP-LINK TECHNOLOGIES CO.,LTD.
18D6CF	Kurth Electronic GmbH
18D949	Qvis Labs, LLC
18DBF2	Dell Inc.
18DC56	Yulong Computer Telecommunication Scientific (Shenzhen) Co.,Ltd
18DED7	HUAWEI TECHNOLOGIES CO.,LTD
18E288	STT Condigi
18E29F	vivo Mobile Communication Co., Ltd.
18E2C2	Samsung Electronics Co.,Ltd
18E3BC	TCT mobile ltd
18E728	Cisco Systems, Inc
18E7F4	Apple, Inc.
18E80F	Viking Electronics Inc.
18E8DD	MODULETEK
18EE69	Apple, Inc.
18EF63	Cisco Systems, Inc
18F145	NetComm Wireless Limited
18F292	Shannon Systems
18F46A	Hon Hai Precision Ind. Co.,Ltd.
18F643	Apple, Inc.
18F650	Multimedia Pacific Limited
18F76B	Zhejiang Winsight Technology CO.,LTD
18F87A	i3 International Inc.
18FA6F	ISC applied systems corp
18FB7B	Dell Inc.
18FC9F	Changhe Electronics Co., Ltd.
18FE34	Espressif Inc.
18FF0F	Intel Corporate
18FF2E	Shenzhen Rui Ying Da Technology Co., Ltd
1C0656	IDY Corporation
1C08C1	Lg Innotek
1C0B52	EPICOM S.A
1C0FCF	Sypro Optics GmbH
1C11E1	Wartsila Finland Oy
1C129D	IEEE PES PSRC/SUB
1C1448	ARRIS Group, Inc.
1C14B3	Airwire Technologies
1C17D3	Cisco Systems, Inc
1C184A	ShenZhen RicherLink Technologies Co.,LTD
1C19DE	eyevis GmbH
1C1AC0	Apple, Inc.
1C1B0D	GIGA-BYTE TECHNOLOGY CO.,LTD.
1C1B68	ARRIS Group, Inc.
1C1CFD	Dalian Hi-Think Computer Technology, Corp
1C1D67	HUAWEI TECHNOLOGIES CO.,LTD
1C1D86	Cisco Systems, Inc
1C1EE3	Hui Zhou Gaoshengda Technology Co.,LTD
1C21D1	IEEE Registration Authority
1C232C	Samsung Electronics Co.,Ltd
1C234F	EDMI  Europe Ltd
1C25E1	China Mobile IOT Company Limited
1C330E	PernixData
1C334D	ITS Telecom
1C3477	Innovation Wireless
1C35F1	NEW Lift Neue Elektronische Wege Steuerungsbau GmbH
1C37BF	Cloudium Systems Ltd.
1C3947	COMPAL INFORMATION (KUNSHAN) CO., LTD.
1C398A	Fiberhome Telecommunication Technologies Co.,LTD
1C3A4F	AccuSpec Electronics, LLC
1C3ADE	Samsung Electronics Co.,Ltd
1C3DE7	Sigma Koki Co.,Ltd.
1C3E84	Hon Hai Precision Ind. Co.,Ltd.
1C4024	Dell Inc.
1C40E8	SHENZHEN PROGRESS&WIN TECHNOLOGY CO.,LTD
1C4158	Gemalto M2M GmbH
1C43EC	JAPAN CIRCUIT CO.,LTD
1C4419	TP-LINK TECHNOLOGIES CO.,LTD.
1C4593	Texas Instruments
1C4840	IMS Messsysteme GmbH
1C48CE	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
1C48F9	GN Netcom A/S
1C497B	Gemtek Technology Co., Ltd.
1C4AF7	AMON INC
1C4BB9	SMG ENTERPRISE, LLC
1C4BD6	AzureWave Technology Inc.
1C51B5	Techaya LTD
1C5216	DONGGUAN HELE ELECTRONICS CO., LTD
1C52D6	FLAT DISPLAY TECHNOLOGY CORPORATION
1C553A	QianGua Corp.
1C56FE	Motorola Mobility LLC, a Lenovo Company
1C57D8	Kraftway Corporation PLC
1C5A0B	Tegile Systems
1C5A3E	Samsung Electronics Co.,Ltd
1C5A6B	Philips Electronics Nederland BV
1C5C55	PRIMA Cinema, Inc
1C5C60	Shenzhen Belzon Technology Co.,LTD.
1C5CF2	Apple, Inc.
1C5F2B	D-Link International
1C5FFF	Beijing Ereneben Information Technology Co.,Ltd Shenzhen Branch
1C60DE	SHENZHEN MERCURY COMMUNICATION TECHNOLOGIES CO.,LTD.
1C62B8	Samsung Electronics Co.,Ltd
1C63B7	OpenProducts 237 AB
1C659D	Liteon Technology Corporation
1C666D	Hon Hai Precision Ind. Co.,Ltd.
1C66AA	Samsung Electronics Co.,Ltd
1C6758	HUAWEI TECHNOLOGIES CO.,LTD
1C69A5	BlackBerry RTS
1C6A7A	Cisco Systems, Inc
1C6BCA	Mitsunami Co., Ltd.
1C6E4C	Logistic Service & Engineering Co.,Ltd
1C6E76	Quarion Technology Inc
1C6F65	GIGA-BYTE TECHNOLOGY CO.,LTD.
1C7370	Neotech
1C740D	ZyXEL Communications Corporation
1C7508	COMPAL INFORMATION (KUNSHAN) CO., LTD.
1C76CA	Terasic Technologies Inc.
1C77F6	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
1C7839	Shenzhen Tencent Computer System Co., Ltd.
1C7B21	Sony Mobile Communications AB
1C7B23	Qingdao Hisense Communications Co.,Ltd.
1C7C11	Eid
1C7C45	Vitek Industrial Video Products, Inc.
1C7CC7	Coriant GmbH
1C7D22	Fuji Xerox Co., Ltd.
1C7E51	3bumen.com
1C7EE5	D-Link International
1C8341	Hefei Bitland Information Technology Co.Ltd
1C83B0	Linked IP GmbH
1C8464	FORMOSA WIRELESS COMMUNICATION CORP.
1C86AD	MCT CO., LTD.
1C872C	ASUSTek COMPUTER INC.
1C8E5C	HUAWEI TECHNOLOGIES CO.,LTD
1C8E8E	DB Communication & Systems Co., ltd.
1C8F8A	Phase Motion Control SpA
1C9148	Apple, Inc.
1C9179	Integrated System Technologies Ltd
1C9492	RUAG Schweiz AG
1C955D	I-LAX ELECTRONICS INC.
1C959F	Veethree Electronics And Marine LLC
1C965A	Weifang goertek Electronics CO.,LTD
1C973D	PRICOM Design
1C98EC	Hewlett Packard Enterprise
1C994C	Murata Manufacturing Co., Ltd.
1C9C26	Zoovel Technologies
1C9D3E	Integrated Device Technology (Malaysia) Sdn. Bhd.
1C9E46	Apple, Inc.
1C9ECB	Beijing Nari Smartchip Microelectronics Company Limited
1CA0D3	IEEE Registration Authority
1CA2B1	ruwido austria gmbh
1CA532	Shenzhen Gongjin Electronics Co.,Ltd
1CA770	SHENZHEN CHUANGWEI-RGB ELECTRONICS CO.,LTD
1CAA07	Cisco Systems, Inc
1CAB01	Innovolt
1CABA7	Apple, Inc.
1CABC0	Hitron Technologies. Inc
1CADD1	Bosung Electronics Co., Ltd.
1CAF05	Samsung Electronics Co.,Ltd
1CAFF7	D-Link International
1CB094	HTC Corporation
1CB17F	NEC Platforms, Ltd.
1CB243	TDC A/S
1CB72C	ASUSTek COMPUTER INC.
1CB857	Becon Technologies Co,.Ltd.
1CB9C4	Ruckus Wireless
1CBA8C	Texas Instruments
1CBBA8	OJSC Ufimskiy Zavod Promsvyaz
1CBD0E	Amplified Engineering Pty Ltd
1CBDB9	D-Link International
1CC035	PLANEX COMMUNICATIONS INC.
1CC0E1	IEEE Registration Authority
1CC11A	Wavetronix
1CC1DE	Hewlett Packard
1CC316	MileSight Technology Co., Ltd.
1CC586	Absolute Acoustics
1CC63C	Arcadyan Technology Corporation
1CC72D	Shenzhen Huapu Digital CO.,Ltd
1CCAE3	IEEE Registration Authority
1CCB99	TCT mobile ltd
1CCDE5	Shanghai Wind Technologies Co.,Ltd
1CD40C	Kriwan Industrie-Elektronik GmbH
1CD6BD	LEEDARSON LIGHTING CO., LTD.
1CDA27	vivo Mobile Communication Co., Ltd.
1CDEA7	Cisco Systems, Inc
1CDF0F	Cisco Systems, Inc
1CE165	Marshal Corporation
1CE192	Qisda Corporation
1CE2CC	Texas Instruments
1CE62B	Apple, Inc.
1CE6C7	Cisco Systems, Inc
1CE85D	Cisco Systems, Inc
1CEA1B	Nokia
1CEEC9	Elo touch solutions
1CEEE8	Ilshin Elecom
1CEFCE	bebro electronic GmbH
1CF03E	Wearhaus Inc.
1CF061	SCAPS GmbH
1CF4CA	Private
1CF5E7	Turtle Industry Co., Ltd.
1CFA68	TP-LINK TECHNOLOGIES CO.,LTD.
1CFCBB	Realfiction ApS
1CFEA7	IDentytech Solutins Ltd.
20014F	Linea Research Ltd
2002AF	Murata Manufacturing Co., Ltd.
200505	RADMAX COMMUNICATION PRIVATE LIMITED
2005E8	OOO InProMedia
2008ED	HUAWEI TECHNOLOGIES CO.,LTD
200A5E	Xiangshan Giant Eagle Technology Developing Co., Ltd.
200BC7	HUAWEI TECHNOLOGIES CO.,LTD
200CC8	Netgear
200E95	IEC – TC9 WG43
20107A	Gemtek Technology Co., Ltd.
201257	Most Lucky Trading Ltd
2012D5	Scientech Materials Corporation
2013E0	Samsung Electronics Co.,Ltd
2016D8	Liteon Technology Corporation
20180E	Shenzhen Sunchip Technology Co., Ltd
201A06	COMPAL INFORMATION (KUNSHAN) CO., LTD.
201D03	Elatec GmbH
2021A5	LG Electronics (Mobile Communications)
202564	PEGATRON CORPORATION
202598	Teleview
2028BC	Visionscape Co,. Ltd.
202BC1	HUAWEI TECHNOLOGIES CO.,LTD
202CB7	Kong Yue Electronics & Information Industry (Xinhui) Ltd.
202D07	Samsung Electronics Co.,Ltd
202DF8	Digital Media Cartridge Ltd.
2031EB	Hdsn
203706	Cisco Systems, Inc
2037BC	Kuipers Electronic Engineering BV
203A07	Cisco Systems, Inc
203AEF	Sivantos GmbH
203CAE	Apple, Inc.
203D66	ARRIS Group, Inc.
203DB2	HUAWEI TECHNOLOGIES CO.,LTD
204005	feno GmbH
20415A	Smarteh d.o.o.
20443A	Schneider Electric Asia Pacific Ltd
2046A1	VECOW Co., Ltd
2046F9	Advanced Network Devices (dbaAND)
204747	Dell Inc.
2047ED	BSkyB Ltd
204AAA	Hanscan Spain S.A.
204C03	Aruba Networks
204C6D	Hugo Brennenstuhl Gmbh & Co. KG.
204C9E	Cisco Systems, Inc
204E6B	Axxana(israel) ltd
204E71	Juniper Networks
204E7F	Netgear
2053CA	Risk Technology Ltd
205476	Sony Mobile Communications AB
205531	Samsung Electronics Co.,Ltd
205532	Gotech International Technology Limited
205721	Salix Technology CO., Ltd.
2057AF	Shenzhen FH-NET OPTOELECTRONICS CO.,LTD
2059A0	Paragon Technologies Inc.
205A00	Coval
205B2A	Private
205B5E	Shenzhen Wonhe Technology Co., Ltd
205CFA	Yangzhou ChangLian Network Technology Co,ltd.
205D47	vivo Mobile Communication Co., Ltd.
205EF7	Samsung Electronics Co.,Ltd
206274	Microsoft Corporation
20635F	Abeeway
206432	SAMSUNG ELECTRO MECHANICS CO., LTD.
2067B1	Pluto inc.
20689D	Liteon Technology Corporation
206A8A	Wistron Infocomm (Zhongshan) Corporation
206AFF	Atlas Elektronik UK Limited
206C8A	Aerohive Networks Inc.
206E9C	Samsung Electronics Co.,Ltd
206FEC	Braemac CA LLC
20719E	SF Technology Co.,Ltd
207355	ARRIS Group, Inc.
2074CF	Shenzhen Voxtech Co.,Ltd
207600	Actiontec Electronics, Inc
20768F	Apple, Inc.
207693	Lenovo (Beijing) Limited.
20780B	Delta Faucet Company
2078F0	Apple, Inc.
207C8F	Quanta Microsystems,Inc.
207D74	Apple, Inc.
2082C0	Xiaomi Communications Co Ltd
20858C	Assa
208756	SIEMENS AG
2087AC	AES motomation
20896F	Fiberhome Telecommunication Technologies Co.,LTD
208984	COMPAL INFORMATION (KUNSHAN) CO., LTD.
208986	zte corporation
208B37	Skyworth Digital Technology(Shenzhen) Co.,Ltd
20906F	Shenzhen Tencent Computer System Co., Ltd.
209148	Texas Instruments
20918A	Profalux
2091D9	I'M SPA
20934D	FUJIAN STAR-NET COMMUNICATION CO.,LTD
209AE9	Volacomm Co., Ltd
209BA5	JIAXING GLEAD Electronics Co.,Ltd
209BCD	Apple, Inc.
20A2E4	Apple, Inc.
20A2E7	Lee-Dickens Ltd
20A680	HUAWEI TECHNOLOGIES CO.,LTD
20A783	miControl GmbH
20A787	Bointec Taiwan Corporation Limited
20A8B9	Siemens
20A90E	TCT mobile ltd
20A99B	Microsoft Corporation
20AA25	IP-NET LLC
20AA4B	Cisco-Linksys, LLC
20AB37	Apple, Inc.
20B0F7	Enclustra GmbH
20B399	Enterasys
20B5C6	Mimosa Networks
20B7C0	OMICRON electronics GmbH
20BB76	COL GIOVANNI PAOLO SpA
20BBC0	Cisco Systems, Inc
20BBC6	Jabil Circuit Hungary Ltd.
20BFDB	Dvl
20C047	Verizon
20C06D	SHENZHEN SPACETEK TECHNOLOGY CO.,LTD
20C1AF	i Wit Digital Co., Limited
20C38F	Texas Instruments
20C3A4	RetailNext
20C60D	Shanghai annijie Information technology Co.,LTD
20C6EB	Panasonic Corporation AVC Networks Company
20C8B3	SHENZHEN BUL-TECH CO.,LTD.
20C9D0	Apple, Inc.
20CD39	Texas Instruments
20CEC4	Peraso Technologies
20CF30	ASUSTek COMPUTER INC.
20D160	Private
20D21F	Wincal Technology Corp.
20D25F	SmartCap Technologies
20D390	Samsung Electronics Co.,Ltd
20D5AB	Korea Infocom Co.,Ltd.
20D5BF	Samsung Electronics Co.,Ltd
20D607	Nokia Corporation
20D75A	Posh Mobile Limited
20D906	Iota, Inc.
20DBAB	Samsung Electronics Co., Ltd.
20DC93	Cheetah Hi-Tech, Inc.
20DCE6	TP-LINK TECHNOLOGIES CO.,LTD.
20DF3F	Nanjing SAC Power Grid Automation Co., Ltd.
20E407	Spark srl
20E52A	Netgear
20E564	ARRIS Group, Inc.
20E791	Siemens Healthcare Diagnostics, Inc
20EAC7	SHENZHEN RIOPINE ELECTRONICS CO., LTD
20ED74	Ability enterprise co.,Ltd.
20EEC6	Elefirst Science & Tech Co ., ltd
20F002	MTData Developments Pty. Ltd.
20F17C	HUAWEI TECHNOLOGIES CO.,LTD
20F3A3	HUAWEI TECHNOLOGIES CO.,LTD
20F41B	Shenzhen Bilian electronic CO.,LTD
20F452	Shanghai IUV Software Development Co. Ltd
20F510	Codex Digital Limited
20F543	Hui Zhou Gaoshengda Technology Co.,LTD
20F85E	Delta Electronics
20FABB	Cambridge Executive Limited
20FDF1	3COM EUROPE LTD
20FECD	System In Frontier Inc.
20FEDB	M2M Solution S.A.S.
2400BA	HUAWEI TECHNOLOGIES CO.,LTD
2401C7	Cisco Systems, Inc
24050F	MTN Electronic Co. Ltd
2405F5	Integrated Device Technology (Malaysia) Sdn. Bhd.
240917	Devlin Electronics Limited
240995	HUAWEI TECHNOLOGIES CO.,LTD
240A11	TCT mobile ltd
240A64	AzureWave Technology Inc.
240AC4	Espressif Inc.
240B0A	Palo Alto Networks
240B2A	Viettel Group
240BB1	KOSTAL Industrie Elektrik GmbH
240D65	Shenzhen Vsun Communication Technology Co., Ltd.
240DC2	TCT mobile ltd
241064	Shenzhen Ecsino Tecnical Co. Ltd
241125	Hutek Co., Ltd.
241148	Entropix, LLC
2411D0	Chongqing Ehs Science and Technology Development Co.,Ltd.
241A8C	Squarehead Technology AS
241B13	Shanghai Nutshell Electronic Co., Ltd.
241B44	Hangzhou Tuners Electronics Co., Ltd
241C04	SHENZHEN JEHE TECHNOLOGY DEVELOPMENT CO., LTD.
241EEB	Apple, Inc.
241F2C	Calsys, Inc.
241FA0	HUAWEI TECHNOLOGIES CO.,LTD
2420C7	Sagemcom Broadband SAS
2421AB	Sony Mobile Communications AB
24240E	Apple, Inc.
242642	SHARP Corporation.
242FFA	Toshiba Global Commerce Solutions
243184	SHARP Corporation
24336C	Private
2435CC	Zhongshan Scinan Internet of Things Co.,Ltd.
24374C	Cisco SPVTG
2437EF	EMC Electronic Media Communication SA
243C20	Dynamode Group
2442BC	Alinco,incorporated
244427	HUAWEI TECHNOLOGIES CO.,LTD
244597	GEMUE Gebr. Mueller Apparatebau
24470E	PentronicAB
24497B	Innovative Converged Devices Inc
244B03	Samsung Electronics Co.,Ltd
244B81	Samsung Electronics Co.,Ltd
244C07	HUAWEI TECHNOLOGIES CO.,LTD
244E7B	IEEE Registration Authority
244F1D	iRule LLC
24590B	White Sky Inc. Limited
245BA7	Apple, Inc.
245BF0	Liteon, Inc.
245CBF	Ncse
245EBE	QNAP Systems, Inc.
245FDF	KYOCERA Corporation
246081	razberi technologies
24615A	China Mobile Group Device Co.,Ltd.
246278	sysmocom - systems for mobile communications GmbH
2464EF	CYG SUNRI CO.,LTD.
246511	AVM GmbH
24693E	innodisk Corporation
24694A	Jasmine Systems Inc.
246968	TP-LINK TECHNOLOGIES CO.,LTD.
2469A5	HUAWEI TECHNOLOGIES CO.,LTD
246AAB	IT-IS International
246C8A	YUKAI Engineering
246E96	Dell Inc.
247189	Texas Instruments
247260	IOTTECH Corp
247656	Shanghai Net Miles Fiber Optics Technology Co., LTD.
24767D	Cisco SPVTG
247703	Intel Corporate
24792A	Ruckus Wireless
247C4C	Herman Miller
247F20	Sagemcom Broadband SAS
247F3C	HUAWEI TECHNOLOGIES CO.,LTD
248000	Westcontrol AS
2481AA	KSH International Co., Ltd.
24828A	Prowave Technologies Ltd.
2486F4	Ctek, Inc.
248707	SEnergy Corporation
248894	shenzhen lensun Communication Technology LTD
248A07	Mellanox Technologies, Inc.
24920E	Samsung Electronics Co.,Ltd
2493CA	Voxtronic Technology Computer-Systeme GmbH
249442	OPEN ROAD SOLUTIONS , INC.
249504	Sfr
2497ED	Techvision Intelligent Technology Limited
249EAB	HUAWEI TECHNOLOGIES CO.,LTD
24A074	Apple, Inc.
24A2E1	Apple, Inc.
24A42C	KOUKAAM a.s.
24A43C	Ubiquiti Networks Inc.
24A495	Thales Canada Inc.
24A7DC	BSkyB Ltd
24A87D	Panasonic Automotive Systems Asia Pacific(Thailand)Co.,Ltd.
24A937	PURE Storage
24AB81	Apple, Inc.
24AF4A	Alcatel-               # Alcatel-Lucent IPD
24AF54	NEXGEN Mediatech Inc.
24B0A9	Shanghai Mobiletek Communication Ltd.
24B657	Cisco Systems, Inc
24B6B8	FRIEM SPA
24B6FD	Dell Inc.
24B88C	Crenus Co.,Ltd.
24B8D2	Opzoon Technology Co.,Ltd.
24BA13	RISO KAGAKU CORPORATION
24BA30	Technical Consumer Products, Inc.
24BBC1	Absolute Analysis
24BC82	Dali Wireless, Inc.
24BCF8	HUAWEI TECHNOLOGIES CO.,LTD
24BE05	Hewlett Packard
24BF74	Private
24C0B3	Rsf
24C1BD	CRRC DALIAN R&D CO.,LTD.
24C3F9	Securitas Direct AB
24C44A	zte corporation
24C696	Samsung Electronics Co.,Ltd
24C848	mywerk system GmbH
24C86E	Chaney Instrument Co.
24C9A1	Ruckus Wireless
24C9DE	Genoray
24CBE7	MYK, Inc.
24CF21	Shenzhen State Micro Technology Co., Ltd
24D13F	MEXUS CO.,LTD
24D2CC	SmartDrive Systems Inc.
24D51C	Zhongtian broadband technology co., LTD
24D921	Avaya Inc
24DA11	NO NDA Inc
24DA9B	Motorola Mobility LLC, a Lenovo Company
24DAB6	Sistemas de Gestión Energética S.A. de C.V
24DBAC	HUAWEI TECHNOLOGIES CO.,LTD
24DBAD	ShopperTrak RCT Corporation
24DBED	Samsung Electronics Co.,Ltd
24DEC6	Aruba Networks
24DF6A	HUAWEI TECHNOLOGIES CO.,LTD
24E271	Qingdao Hisense Communications Co.,Ltd.
24E314	Apple, Inc.
24E43F	Wenzhou Kunmei Communication Technology Co.,Ltd.
24E5AA	Philips Oral Healthcare, Inc.
24E6BA	JSC Zavod im. Kozitsky
24E9B3	Cisco Systems, Inc
24EA40	Helmholz GmbH & Co. KG
24EB65	SAET I.S. S.r.l.
24EC99	ASKEY COMPUTER CORP
24ECD6	CSG Science & Technology Co.,Ltd.Hefei
24EE3A	Chengdu Yingji Electronic Hi-tech Co Ltd
24F094	Apple, Inc.
24F0FF	GHT Co., Ltd.
24F2DD	Radiant Zemax LLC
24F57E	HWH CO., LTD.
24F5AA	Samsung Electronics Co.,Ltd
24FD52	Liteon Technology Corporation
24FD5B	SmartThings, Inc.
2804E0	FERMAX ELECTRONICA S.A.U.
28061E	NINGBO GLOBAL USEFUL ELECTRIC CO.,LTD
28068D	ITL, LLC
280B5C	Apple, Inc.
280C28	Unigen DataStorage Corporation
280CB8	Mikrosay Yazilim ve Elektronik A.S.
280DFC	Sony Interactive Entertainment Inc.
280E8B	Beijing Spirit Technology Development Co., Ltd.
28101B	Magnacom
28107B	D-Link International
281471	Lantis co., LTD.
28162E	2Wire Inc
2816AD	Intel Corporate
2817CE	Omnisense Ltd
281878	Microsoft Corporation
2818FD	Aditya Infotech Ltd.
282246	Beijing Sinoix Communication Co., LTD
2824FF	Wistron Neweb Corporation
282536	SHENZHEN HOLATEK CO.,LTD
2826A6	PBR electronics GmbH
2827BF	Samsung Electronics Co.,Ltd
28285D	ZyXEL Communications Corporation
2829CC	Corsa Technology Incorporated
2829D9	GlobalBeiMing technology (Beijing)Co. Ltd
282CB2	TP-LINK TECHNOLOGIES CO.,LTD.
283152	HUAWEI TECHNOLOGIES CO.,LTD
2832C5	HUMAX Co., Ltd.
283410	Enigma Diagnostics Limited
2834A2	Cisco Systems, Inc
283638	IEEE Registration Authority
283713	Shenzhen 3Nod Digital Technology Co., Ltd.
283737	Apple, Inc.
2838CF	Gen2wave
28395E	Samsung Electronics Co.,Ltd
2839E7	Preceno Technology Pte.Ltd.
283B96	Cool Control LTD
283CE4	HUAWEI TECHNOLOGIES CO.,LTD
283F69	Sony Mobile Communications AB
28401A	C8 MediSensors, Inc.
284121	OptiSense Network, LLC
284430	GenesisTechnical Systems (UK) Ltd
2847AA	Nokia Corporation
284846	GridCentric Inc.
284C53	Intune Networks
284D92	Luminator
284ED7	OutSmart Power Systems, Inc.
284FCE	Liaoning Wontel Science and Technology Development Co.,Ltd.
285132	Shenzhen Prayfly Technology Co.,Ltd
285261	Cisco Systems, Inc
2852E0	Layon international Electronic & Telecom Co.,Ltd
28565A	Hon Hai Precision Ind. Co.,Ltd.
285767	Echostar Technologies Corp
2857BE	Hangzhou Hikvision Digital Technology Co.,Ltd.
285AEB	Apple, Inc.
285F2F	RNware Co.,Ltd.
285FDB	HUAWEI TECHNOLOGIES CO.,LTD
286046	Lantech Communications Global, Inc.
286094	Capelec
286336	Siemens-               # Siemens AG - Industrial Automation - EWA
28656B	Keystone Microtech Corporation
286AB8	Apple, Inc.
286ABA	Apple, Inc.
286C07	XIAOMI Electronics,CO.,LTD
286D97	SAMJIN Co., Ltd.
286ED4	HUAWEI TECHNOLOGIES CO.,LTD
286F7F	Cisco Systems, Inc
287184	Spire Payments
2872C5	Smartmatic Corp
2872F0	Athena
287610	IgniteNet
2876CD	Funshion Online Technologies Co.,Ltd
287994	Realplay Digital Technology(Shenzhen) Co.,Ltd
287AEE	ARRIS Group, Inc.
287CDB	Hefei  Toycloud Technology Co.,ltd
288023	Hewlett Packard
288335	Samsung Electronics Co.,Ltd
2884FA	SHARP Corporation
28852D	Touch Networks
288915	CashGuard Sverige AB
288A1C	Juniper Networks
2891D0	Stage Tec Entwicklungsgesellschaft für professionelle Audiotechnik mbH
28924A	Hewlett Packard
2893FE	Cisco Systems, Inc
28940F	Cisco Systems, Inc
2894AF	Samhwa Telecom
28987B	Samsung Electronics Co.,Ltd
28993A	Arista Networks
289A4B	SteelSeries ApS
289AFA	TCT mobile ltd
289EDF	Danfoss Turbocor Compressors, Inc
28A02B	Apple, Inc.
28A183	ALPS ELECTRIC CO.,LTD.
28A186	Enblink
28A192	GERP Solution
28A1EB	ETEK TECHNOLOGY (SHENZHEN) CO.,LTD
28A241	exlar corp
28A24B	Juniper Networks
28A574	Miller Electric Mfg. Co.
28A5EE	Shenzhen SDGI CATV Co., Ltd
28A6DB	HUAWEI TECHNOLOGIES CO.,LTD
28AC67	Mach Power, Rappresentanze Internazionali s.r.l.
28AF0A	Sirius XM Radio Inc
28B0CC	Xenya d.o.o.
28B2BD	Intel Corporate
28B3AB	Genmark Automation
28B448	HUAWEI TECHNOLOGIES CO.,LTD
28B9D9	Radisys Corporation
28BA18	NextNav, LLC
28BAB5	Samsung Electronics Co.,Ltd
28BB59	RNET Technologies, Inc.
28BC18	SourcingOverseas Co. Ltd
28BC56	EMAC, Inc.
28BE03	TCT mobile ltd
28BE9B	Technicolor CH USA Inc.
28C0DA	Juniper Networks
28C2DD	AzureWave Technology Inc.
28C63F	Intel Corporate
28C671	Yota Devices OY
28C68E	Netgear
28C718	Altierre
28C7CE	Cisco Systems, Inc
28C825	DellKing Industrial Co., Ltd
28C87A	ARRIS Group, Inc.
28C914	Taimag Corporation
28CA09	ThyssenKrupp Elevators (Shanghai) Co.,Ltd
28CBEB	One
28CC01	Samsung Electronics Co.,Ltd
28CCFF	Corporacion Empresarial Altra SL
28CD1C	Espotel Oy
28CD4C	Individual Computers GmbH
28CD9C	Shenzhen Dynamax Software Development Co.,Ltd.
28CFDA	Apple, Inc.
28CFE9	Apple, Inc.
28D1AF	Nokia Corporation
28D244	LCFC(HeFei) Electronics Technology Co., Ltd.
28D576	Premier Wireless, Inc.
28D93E	Telecor Inc.
28D98A	Hangzhou Konke Technology Co.,Ltd.
28D997	Yuduan Mobile Co., Ltd.
28DB81	Shanghai Guao Electronic Technology Co., Ltd
28DEF6	bioMerieux Inc.
28E02C	Apple, Inc.
28E14C	Apple, Inc.
28E297	Shanghai InfoTM Microelectronics Co.,Ltd.
28E31F	Xiaomi Communications Co Ltd
28E347	Liteon Technology Corporation
28E476	Pi-Coral
28E608	Tokheim
28E6E9	SIS Sat Internet Services GmbH
28E794	Microtime Computer Inc.
28E7CF	Apple, Inc.
28ED58	JAG Jakob AG
28ED6A	Apple, Inc.
28EE2C	Frontline Test Equipment
28EE52	TP-LINK TECHNOLOGIES CO.,LTD.
28EED3	Shenzhen Super D Technology Co., Ltd
28EF01	Private
28F076	Apple, Inc.
28F10E	Dell Inc.
28F358	2C - Trifonov & Co
28F366	Shenzhen Bilian electronic CO.,LTD
28F532	ADD-Engineering BV
28F606	Syes srl
28FAA0	vivo Mobile Communication Co., Ltd.
28FBD3	Ragentek Technology Group
28FC51	The Electric Controller and Manufacturing Co., LLC
28FCF6	Shenzhen Xin KingBrand enterprises Co.,Ltd
28FD80	IEEE Registration Authority
28FECD	Lemobile Information Technology (Beijing) Co., Ltd.
28FF3E	zte corporation
2C002C	Unowhy
2C0033	EControls, LLC
2C00F7	Xos
2C010B	NASCENT Technology, LLC - RemKon
2C029F	3alogics
2C0623	Win Leader Inc.
2C073C	DEVLINE LIMITED
2C081C	Ovh
2C088C	HUMAX Co., Ltd.
2C094D	Raptor Engineering, LLC
2C09CB	COBS AB
2C0BE9	Cisco Systems, Inc
2C0E3D	SAMSUNG ELECTRO-MECHANICS(THAILAND)
2C10C1	Nintendo Co., Ltd.
2C18AE	Trend Electronics Co., Ltd.
2C1984	IDN Telecom, Inc.
2C1A31	Electronics Company Limited
2C1BC8	Hunan Topview Network System CO.,LTD
2C1DB8	ARRIS Group, Inc.
2C1EEA	Aerodev
2C1F23	Apple, Inc.
2C200B	Apple, Inc.
2C2131	Juniper Networks
2C2172	Juniper Networks
2C21D7	IMAX Corporation
2C228B	CTR SRL
2C233A	Hewlett Packard
2C245F	Babolat VS
2C265F	IEEE Registration Authority
2C26C5	zte corporation
2C27D7	Hewlett Packard
2C282D	BBK EDUCATIONAL ELECTRONICS CORP.,LTD.
2C2997	Microsoft Corporation
2C2D48	bct electronic GesmbH
2C3033	Netgear
2C3068	Pantech Co.,Ltd
2C3124	Cisco Systems, Inc
2C3311	Cisco Systems, Inc
2C3361	Apple, Inc.
2C337A	Hon Hai Precision Ind. Co.,Ltd.
2C3427	ERCO & GENER
2C3557	ELLIY Power CO..Ltd
2C36A0	Capisco Limited
2C36F8	Cisco Systems, Inc
2C3731	SHENZHEN YIFANG DIGITAL TECHNOLOGY CO.,LTD.
2C3796	CYBO CO.,LTD.
2C3996	Sagemcom Broadband SAS
2C39C1	Ciena Corporation
2C3A28	Fagor Electrónica
2C3BFD	Netstor Technology Co., Ltd.
2C3ECF	Cisco Systems, Inc
2C3F38	Cisco Systems, Inc
2C3F3E	Alge-Timing GmbH
2C402B	Smart iBlue Technology Limited
2C4138	Hewlett Packard
2C4401	Samsung Electronics Co.,Ltd
2C441B	Spectrum Medical Limited
2C44FD	Hewlett Packard
2C4D54	ASUSTek COMPUTER INC.
2C4D79	GoerTek Inc.
2C5089	Shenzhen Kaixuan Visual Technology Co.,Limited
2C534A	Shenzhen Winyao Electronic Limited
2C542D	Cisco Systems, Inc
2C54CF	LG Electronics (Mobile Communications)
2C553C	Gainspeed, Inc.
2C55D3	HUAWEI TECHNOLOGIES CO.,LTD
2C56DC	ASUSTek COMPUTER INC.
2C598A	LG Electronics (Mobile Communications)
2C59E5	Hewlett Packard
2C5A05	Nokia Corporation
2C5A0F	Cisco Systems, Inc
2C5A8D	SYSTRONIK Elektronik u. Systemtechnik GmbH
2C5AA3	PROMATE ELECTRONIC CO.LTD
2C5BB8	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
2C5BE1	Centripetal Networks, Inc
2C5D93	Ruckus Wireless
2C5FF3	Pertronic Industries
2C600C	QUANTA COMPUTER INC.
2C625A	Finest Security Systems Co., Ltd
2C6289	Regenersis (Glenrothes) Ltd
2C6373	SICHUAN TIANYI COMHEART TELECOMCO., LTD
2C6798	InTalTech Ltd.
2C67FB	ShenZhen Zhengjili Electronics Co., LTD
2C69BA	RF Controls, LLC
2C6A6F	IEEE Registration Authority
2C6BF5	Juniper Networks
2C6E85	Intel Corporate
2C6FC9	Hon Hai Precision Ind. Co.,Ltd.
2C7155	HiveMotion
2C72C3	Soundmatters
2C750F	Shanghai Dongzhou-Lawton Communication Technology Co. Ltd.
2C768A	Hewlett Packard
2C7B5A	Milper Ltd
2C7B84	OOO Petr Telegin
2C7E81	ARRIS Group, Inc.
2C7ECF	Onzo Ltd
2C8065	HARTING Inc. of North America
2C8158	Hon Hai Precision Ind. Co.,Ltd.
2C86D2	Cisco Systems, Inc
2C8A72	HTC Corporation
2C8BF2	Hitachi Metals America Ltd
2C9127	Eintechno Corporation
2C922C	Kishu Giken Kogyou Company Ltd,.
2C9464	Cincoze Co., Ltd.
2C957F	zte corporation
2C9662	Invenit BV
2C9717	I.C.Y. B.V.
2C9924	ARRIS Group, Inc.
2C9AA4	Eolo SpA
2C9D1E	HUAWEI TECHNOLOGIES CO.,LTD
2C9E5F	ARRIS Group, Inc.
2C9EFC	CANON INC.
2CA157	acromate, Inc.
2CA17D	ARRIS Group, Inc.
2CA2B4	Fortify Technologies, LLC
2CA30E	POWER DRAGON DEVELOPMENT LIMITED
2CA539	Parallel Wireless, Inc
2CA780	True Technologies Inc.
2CA835	Rim
2CAB00	HUAWEI TECHNOLOGIES CO.,LTD
2CAB25	Shenzhen Gongjin Electronics Co.,Ltd
2CABA4	Cisco SPVTG
2CABEB	Cisco Systems, Inc
2CAC44	Conextop
2CAD13	SHENZHEN ZHILU TECHNOLOGY CO.,LTD
2CAE2B	Samsung Electronics Co.,Ltd
2CB05D	Netgear
2CB0DF	Soliton Technologies Pvt Ltd
2CB115	Integrated Device Technology (Malaysia) Sdn. Bhd.
2CB43A	Apple, Inc.
2CB693	Radware
2CB69D	RED Digital Cinema
2CBABA	Samsung Electronics Co.,Ltd
2CBE08	Apple, Inc.
2CBE97	Ingenieurbuero Bickele und Buehler GmbH
2CC260	Oracle Corporation
2CC548	IAdea Corporation
2CC5D3	Ruckus Wireless
2CCC15	Nokia Corporation
2CCD27	Precor Inc
2CCD43	Summit Technology Group
2CCD69	Aqavi.com
2CCF58	HUAWEI TECHNOLOGIES CO.,LTD
2CD02D	Cisco Systems, Inc
2CD05A	Liteon Technology Corporation
2CD141	IEEE Registration Authority
2CD1DA	Sanjole, Inc.
2CD2E7	Nokia Corporation
2CD444	FUJITSU LIMITED
2CDCAD	Wistron Neweb Corporation
2CDD0C	Discovergy GmbH
2CDD95	Taicang T&W Electronics
2CDDA3	Point Grey Research Inc.
2CE2A8	DeviceDesign
2CE412	Sagemcom Broadband SAS
2CE6CC	Ruckus Wireless
2CE871	Alert Metalguard ApS
2CEDEB	Alpheus Digital Company Limited
2CEE26	Petroleum Geo-Services
2CF0A2	Apple, Inc.
2CF0EE	Apple, Inc.
2CF203	EMKO ELEKTRONIK SAN VE TIC AS
2CF4C5	Avaya Inc
2CF7F1	Seeed Technology Inc.
2CFAA2	Alcatel-               # Alcatel-Lucent Enterprise
2CFCE4	CTEK Sweden AB
2CFD37	Blue Calypso, Inc.
2CFF65	Oki Electric Industry Co., Ltd.
2E2E2E	LAA (Locally Administered Address) for Meditech Systems
30055C	Brother industries, LTD.
300B9C	Delta Mobile Systems, Inc.
300C23	zte corporation
300D2A	Zhejiang Wellcom Technology Co.,Ltd.
300D43	Microsoft Mobile Oy
300ED5	Hon Hai Precision Ind. Co.,Ltd.
300EE3	Aquantia Corporation
3010B3	Liteon Technology Corporation
3010E4	Apple, Inc.
30142D	Piciorgros GmbH
30144A	Wistron Neweb Corporation
301518	Ubiquitous Communication Co. ltd.
30168D	Prolon
3017C8	Sony Mobile Communications AB
3018CF	DEOS control systems GmbH
301966	Samsung Electronics Co.,Ltd
301A28	Mako Networks Ltd
30215B	Shenzhen Ostar Display Electronic Co.,Ltd
3029BE	Shanghai MRDcom Co.,Ltd
302DE8	JDA, LLC (JDA Systems)
303294	W-Ie-Ne-               # W-IE-NE-R Plein & Baus GmbH
3032D4	Hanilstm Co., Ltd.
303335	Boosty
3034D2	Availink, Inc.
3037A6	Cisco Systems, Inc
303855	Nokia Corporation
303926	Sony Mobile Communications AB
303955	Shenzhen Jinhengjia Electronic Co., Ltd.
3039F2	ADB Broadband Italia
303A64	Intel Corporate
303D08	GLINTT TES S.A.
303EAD	Sonavox Canada Inc
304174	ALTEC LANSING LLC
304225	BURG-WÄCHTER KG
304449	PLATH GmbH
304487	Hefei Radio Communication Technology Co., Ltd
3044A1	Shanghai Nanchao Information Technology
30469A	Netgear
30493B	Nanjing Z-Com Wireless Co.,Ltd
304C7E	Panasonic Electric Works Automation Controls Techno Co.,Ltd.
304EC3	Tianjin Techua Technology Co., Ltd.
3051F8	BYK-Gardner GmbH
30525A	NST Co., LTD
3052CB	Liteon Technology Corporation
3055ED	Trex Network LLC
3057AC	IRLAB LTD.
305890	Frontier Silicon Ltd
30595B	streamnow AG
3059B7	Microsoft
305A3A	ASUSTek COMPUTER INC.
305D38	Beissbarth
306023	ARRIS Group, Inc.
306112	PAV GmbH
306118	Paradom Inc.
30636B	Apple, Inc.
3065EC	Wistron (ChongQing)
30688C	Reach Technology Inc.
30694B	Rim
306CBE	Skymotion Technology (HK) Limited
306E5C	Validus Technologies
3071B2	Hangzhou Prevail Optoelectronic Equipment Co.,LTD.
307350	Inpeco SA
307496	HUAWEI TECHNOLOGIES CO.,LTD
307512	Sony Mobile Communications AB
30766F	LG Electronics (Mobile Communications)
3077CB	Maike Industry(Shenzhen)CO.,LTD
30785C	Partow Tamas Novin (Parman)
30786B	TIANJIN Golden Pentagon Electronics Co., Ltd.
3078C2	Innowireless, Co. Ltd.
307C30	Rim
307C5E	Juniper Networks
307CB2	ANOV FRANCE
307ECB	Sfr
3085A9	ASUSTek COMPUTER INC.
308730	HUAWEI TECHNOLOGIES CO.,LTD
3087D9	Ruckus Wireless
308999	Guangdong East Power Co.,
3089D3	HONGKONG UCLOUDLINK NETWORK TECHNOLOGY LIMITED
308CFB	Dropcam
308D99	Hewlett Packard
3090AB	Apple, Inc.
30918F	Technicolor
3092F6	SHANGHAI SUNMON COMMUNICATION TECHNOGY CO.,LTD
3095E3	SHANGHAI SIMCOM LIMITED
3096FB	Samsung Electronics Co.,Ltd
309BAD	BBK EDUCATIONAL ELECTRONICS CORP.,LTD.
30A220	ARG Telecom
30A243	Shenzhen Prifox Innovation Technology Co., Ltd.
30A8DB	Sony Mobile Communications AB
30A9DE	LG Innotek
30AABD	Shanghai Reallytek Information Technology Co.,Ltd
30AE7B	Deqing Dusun Electron CO., LTD
30AEA4	Espressif Inc.
30AEF6	Radio Mobile Access
30B216	Hytec Geraetebau GmbH
30B3A2	Shenzhen Heguang Measurement & Control Technology Co.,Ltd
30B49E	TP-LINK TECHNOLOGIES CO.,LTD.
30B5C2	TP-LINK TECHNOLOGIES CO.,LTD.
30B5F1	Aitexin Technology Co., Ltd
30B64F	Juniper Networks
30C750	MIC Technology Group
30C7AE	Samsung Electronics Co.,Ltd
30C82A	WI-BIZ srl
30CBF8	Samsung Electronics Co.,Ltd
30CDA7	Samsung Electronics Co.,Ltd
30D17E	HUAWEI TECHNOLOGIES CO.,LTD
30D32D	devolo AG
30D357	Logosol, Inc.
30D386	zte corporation
30D46A	Autosales Incorporated
30D587	Samsung Electronics Co.,Ltd
30D6C9	Samsung Electronics Co.,Ltd
30DE86	Cedac Software S.r.l.
30E090	Linctronix Ltd,
30E171	Hewlett Packard
30E37A	Intel Corporate
30E48E	Vodafone UK
30E4DB	Cisco Systems, Inc
30EB25	INTEK DIGITAL
30EFD1	Alstom Strongwish (Shenzhen) Co., Ltd.
30F31D	zte corporation
30F335	HUAWEI TECHNOLOGIES CO.,LTD
30F33A	+plugg srl
30F42F	Esp
30F6B9	Ecocentric Energy
30F70D	Cisco Systems, Inc
30F772	Hon Hai Precision Ind. Co.,Ltd.
30F7C5	Apple, Inc.
30F7D7	Thread Technology Co., Ltd
30F9ED	Sony Corporation
30FAB7	Tunai Creative
30FC68	TP-LINK TECHNOLOGIES CO.,LTD.
30FD11	MACROTECH (USA) INC.
30FFF6	HangZhou KuoHeng Technology Co.,ltd
3400A3	HUAWEI TECHNOLOGIES CO.,LTD
340286	Intel Corporate
34029B	CloudBerry Technologies Private Limited
34049E	IEEE Registration Authority
34074F	AccelStor, Inc.
3407FB	Ericsson AB
340804	D-Link Corporation
340A22	TOP-ACCESS ELECTRONICS CO LTD
340AFF	Qingdao Hisense Communications Co.,Ltd.
340B40	MIOS ELETTRONICA SRL
340CED	Moduel AB
341290	Treeview Co.,Ltd.
341298	Apple, Inc.
3413A8	Mediplan Limited
3413E8	Intel Corporate
34145F	Samsung Electronics Co.,Ltd
34159E	Apple, Inc.
3417EB	Dell Inc.
341A35	Fiberhome Telecommunication Technologies Co.,LTD
341A4C	SHENZHEN WEIBU ELECTRONICS CO.,LTD.
341B22	Grandbeing Technology Co., Ltd
341E6B	HUAWEI TECHNOLOGIES CO.,LTD
341FE4	ARRIS Group, Inc.
342109	Jensen Scandinavia AS
342387	Hon Hai Precision Ind. Co.,Ltd.
3423BA	SAMSUNG ELECTRO-MECHANICS(THAILAND)
34255D	Shenzhen Loadcom Technology Co.,Ltd
342606	CarePredict, Inc.
3428F0	ATN International Limited
3429EA	MCD ELECTRONICS SP. Z O.O.
342F6E	Anywire corporation
343111	Samsung Electronics Co.,Ltd
3431C4	AVM GmbH
34363B	Apple, Inc.
343759	zte corporation
3438AF	Inlab Software GmbH
343D98	JinQianMao Technology Co.,Ltd.
343DC4	BUFFALO.INC
3440B5	Ibm
34466F	HiTEM Engineering
344B3D	Fiberhome Telecommunication Technologies Co.,LTD
344B50	zte corporation
344CA4	amazipoint technology Ltd.
344CC8	Echodyne Corp
344DEA	zte corporation
344DF7	LG Electronics (Mobile Communications)
344F3F	IO-Power Technology Co., Ltd.
344F5C	R&amp;M AG
344F69	EKINOPS SAS
3451AA	JID GLOBAL
3451C9	Apple, Inc.
34543C	TAKAOKA TOKO CO.,LTD.
345760	MitraStar Technology Corp.
345B11	EVI HEAT AB
345BBB	GD Midea Air-Conditioning Equipment Co.,Ltd.
345C40	Cargt Holdings LLC
345D10	Wytek
346178	The Boeing Company
346288	Cisco Systems, Inc
3464A9	Hewlett Packard
34684A	Teraworks Co., Ltd.
346895	Hon Hai Precision Ind. Co.,Ltd.
346987	zte corporation
346AC2	HUAWEI TECHNOLOGIES CO.,LTD
346BD3	HUAWEI TECHNOLOGIES CO.,LTD
346C0F	Pramod Telecom Pvt. Ltd
346E8A	Ecosense
346E9D	Ericsson AB
346F90	Cisco Systems, Inc
346F92	White Rodgers Division
3475C7	Avaya Inc
3476C5	I-O DATA DEVICE, INC.
347877	O-Net Communications (Shenzhen) Limited
3478D7	Gionee Communication Equipment Co.,Ltd.
347A60	ARRIS Group, Inc.
347E39	Nokia Danmark A/S
3480B3	Xiaomi Communications Co Ltd
348137	UNICARD SA
3481C4	AVM GmbH
3481F4	SST Taiwan Ltd.
3482DE	Kiio Inc
348302	iFORCOM Co., Ltd
348446	Ericsson AB
34862A	Heinz Lackmann GmbH & Co KG
34873D	Quectel Wireless Solution Co.,Ltd.
34885D	Logitech Far East
348A7B	Samsung Electronics Co.,Ltd
348AAE	Sagemcom Broadband SAS
3495DB	Logitec Corporation
349672	TP-LINK TECHNOLOGIES CO.,LTD.
3497F6	ASUSTek COMPUTER INC.
3497FB	ADVANCED RF TECHNOLOGIES INC
34996F	VPI Engineering
349971	Quanta Storage Inc.
3499D7	Universal Flow Monitors, Inc.
349A0D	ZBD Displays Ltd
349B5B	Maquet GmbH
349D90	Heinzmann GmbH & CO. KG
349E34	Evervictory Electronic Co.Ltd
34A183	AWare, Inc
34A2A2	HUAWEI TECHNOLOGIES CO.,LTD
34A395	Apple, Inc.
34A3BF	Terewave. Inc.
34A55D	TECHNOSOFT INTERNATIONAL SRL
34A5E1	Sensorist ApS
34A68C	Shine Profit Development Limited
34A709	Trevil srl
34A7BA	Fischer International Systems Corporation
34A843	KYOCERA Display Corporation
34A84E	Cisco Systems, Inc
34AA8B	Samsung Electronics Co.,Ltd
34AA99	Nokia
34AAEE	Mikrovisatos Servisas UAB
34AB37	Apple, Inc.
34ADE4	Shanghai Chint Power Systems Co., Ltd.
34AF2C	Nintendo Co., Ltd.
34B1F7	Texas Instruments
34B354	HUAWEI TECHNOLOGIES CO.,LTD
34B571	Plds
34B7FD	Guangzhou Younghead Electronic Technology Co.,Ltd
34BA51	Se-Kure Controls, Inc.
34BA75	Tembo Systems, Inc.
34BA9A	Asiatelco Technologies Co.
34BB1F	BlackBerry RTS
34BB26	Motorola Mobility LLC, a Lenovo Company
34BCA6	Beijing Ding Qing Technology, Ltd.
34BDC8	Cisco Systems, Inc
34BDF9	Shanghai WDK Industrial Co.,Ltd.
34BDFA	Cisco SPVTG
34BE00	Samsung Electronics Co.,Ltd
34BF90	Fiberhome Telecommunication Technologies Co.,LTD
34C059	Apple, Inc.
34C0F9	Rockwell Automation
34C3AC	Samsung Electronics Co.,Ltd
34C3D2	FN-LINK TECHNOLOGY LIMITED
34C5D0	Hagleitner Hygiene International GmbH
34C69A	Enecsys Ltd
34C731	ALPS ELECTRIC CO.,LTD.
34C803	Nokia Corporation
34C99D	EIDOLON COMMUNICATIONS TECHNOLOGY CO. LTD.
34C9F0	LM Technologies Ltd
34CC28	Nexpring Co. LTD.,
34CD6D	CommSky Technologies
34CDBE	HUAWEI TECHNOLOGIES CO.,LTD
34CE00	XIAOMI Electronics,CO.,LTD
34CE94	Parsec (Pty) Ltd
34D09B	MobilMAX Technology Inc.
34D270	Amazon Technologies Inc.
34D2C4	RENA GmbH Print Systeme
34D7B4	Tributary Systems, Inc.
34DBFD	Cisco Systems, Inc
34DE1A	Intel Corporate
34DE34	zte corporation
34DF2A	Fujikon Industrial Co.,Limited
34E0CF	zte corporation
34E0D7	DONGGUAN QISHENG ELECTRONICS INDUSTRIAL CO., LTD
34E2FD	Apple, Inc.
34E42A	Automatic Bar Controls Inc.
34E6AD	Intel Corporate
34E6D7	Dell Inc.
34E70B	HAN Networks Co., Ltd
34E71C	Shenzhen YOUHUA Technology Co., Ltd
34EA34	HangZhou Gubei Electronics Technology Co.,Ltd
34ED0B	Shanghai XZ-COM.CO.,Ltd.
34EF44	2Wire Inc
34EF8B	NTT Communications Corporation
34F0CA	Shenzhen Linghangyuan Digital Technology Co.,Ltd.
34F39A	Intel Corporate
34F39B	WizLAN Ltd.
34F62D	SHARP Corporation
34F6D2	Panasonic Taiwan Co.,Ltd.
34F968	ATEK Products, LLC
34FA40	Guangzhou Robustel Technologies Co., Limited
34FC6F	Alcea
34FCB9	Hewlett Packard Enterprise
34FCEF	LG Electronics (Mobile Communications)
380195	Samsung Electronics Co.,Ltd
380197	TSST Global,Inc
380546	Foctek Photonics, Inc.
3805AC	Piller Group GmbH
3806B4	A.D.C. GmbH
3808FD	Silca Spa
3809A4	Firefly Integrations
380A0A	Sky-City Communication and Electronics Limited Company
380A94	Samsung Electronics Co.,Ltd
380AAB	Formlabs
380B40	Samsung Electronics Co.,Ltd
380DD4	Primax Electronics Ltd.
380E7B	V.P.S. Thai Co., Ltd
380F4A	Apple, Inc.
380FE4	Dedicated Network Partners Oy
3810D5	AVM Audiovisuelles Marketing und Computersysteme GmbH
3816D1	Samsung Electronics Co.,Ltd
381766	PROMZAKAZ LTD.
38192F	Nokia Corporation
381C1A	Cisco Systems, Inc
381C23	Hilan Technology CO.,LTD
381C4A	SIMCom Wireless Solutions Co.,Ltd.
381DD9	FN-LINK TECHNOLOGY LIMITED
382056	Cisco Systems, Inc
382187	Midea Group Co., Ltd.
38229D	ADB Broadband Italia
3822D6	Hangzhou H3C Technologies Co., Limited
38256B	Microsoft Mobile Oy
38262B	UTran Technology
3826CD	Andtek
3828EA	Fujian Netcom Technology Co., LTD
38295A	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
3829DD	ONvocal Inc
382B78	ECO PLUGS ENTERPRISE CO., LTD
382C4A	ASUSTek COMPUTER INC.
382DD1	Samsung Electronics Co.,Ltd
382DE8	Samsung Electronics Co.,Ltd
3831AC	Weg
383A21	IEEE Registration Authority
383BC8	2Wire Inc
383F10	DBL Technology Ltd.
384233	Wildeboer Bauteile GmbH
3842A6	Ingenieurbuero Stahlkopf
384369	Patrol Products Consortium LLC
38454C	Light Labs, Inc.
38458C	MyCloud Technology corporation
384608	zte corporation
38484C	Apple, Inc.
384B76	AIRTAME ApS
384C4F	HUAWEI TECHNOLOGIES CO.,LTD
384C90	ARRIS Group, Inc.
384FF0	AzureWave Technology Inc.
38521A	Nokia
385610	CANDY HOUSE, Inc.
38580C	Panaccess Systems GmbH
3859F8	MindMade Sp. z o.o.
3859F9	Hon Hai Precision Ind. Co.,Ltd.
385AA8	Beijing Zhongdun Security Technology Development Co.
385F66	Cisco SPVTG
385FC3	Yu Jeong System, Co.Ltd
386077	PEGATRON CORPORATION
3863BB	Hewlett Packard
3863F6	3NOD MULTIMEDIA(SHENZHEN)CO.,LTD
386645	OOSIC Technology CO.,Ltd
386793	Asia Optical Co., Inc.
386BBB	ARRIS Group, Inc.
386C9B	Ivy Biomedical
386E21	Wasion Group Ltd.
38700C	ARRIS Group, Inc.
3871DE	Apple, Inc.
3872C0	Comtrend Corporation
3876CA	Shenzhen Smart Intelligent Technology Co.Ltd
3876D1	Euronda SpA
387B47	AKELA, Inc.
388345	TP-LINK TECHNOLOGIES CO.,LTD.
388602	Flexoptix GmbH
3889DC	Opticon Sensors Europe B.V.
388AB7	ITC Networks
388C50	LG Electronics
388EE7	Fanhattan LLC
3891D5	Hangzhou H3C Technologies Co., Limited
3891FB	Xenox Holding BV
389496	Samsung Electronics Co.,Ltd
389592	Beijing Tendyron Corporation
3897D6	Hangzhou H3C Technologies Co., Limited
3898D8	MERITECH CO.,LTD
389F83	OTN Systems N.V.
38A28C	SHENZHEN RF-LINK TECHNOLOGY CO.,LTD.
38A4ED	Xiaomi Communications Co Ltd
38A53C	COMECER Netherlands
38A5B6	SHENZHEN MEGMEET ELECTRICAL CO.,LTD
38A851	Moog, Ing
38A86B	Orga BV
38A95F	Actifio Inc
38AA3C	SAMSUNG ELECTRO MECHANICS CO., LTD.
38AC3D	Nephos Inc
38AFD7	FUJITSU LIMITED
38B12D	Sonotronic Nagel GmbH
38B1DB	Hon Hai Precision Ind. Co.,Ltd.
38B54D	Apple, Inc.
38B5BD	E.G.O. Elektro-Ger
38B725	Wistron Infocomm (Zhongshan) Corporation
38B74D	Fijowave Limited
38B8EB	IEEE Registration Authority
38BB23	OzVision America LLC
38BB3C	Avaya Inc
38BC01	HUAWEI TECHNOLOGIES CO.,LTD
38BC1A	MEIZU Technology Co., Ltd.
38BF2F	Espec Corp.
38BF33	NEC CASIO Mobile Communications
38C096	ALPS ELECTRIC CO.,LTD.
38C70A	Wifisong
38C7BA	CS Services Co.,Ltd.
38C85C	Cisco SPVTG
38C986	Apple, Inc.
38C9A9	SMART High Reliability Solutions, Inc.
38CA97	Contour Design LLC
38CADA	Apple, Inc.
38D135	EasyIO Corporation Sdn. Bhd.
38D269	Texas Instruments
38D40B	Samsung Electronics Co.,Ltd
38D547	ASUSTek COMPUTER INC.
38D82F	zte corporation
38DBBB	Sunbow Telecom Co., Ltd.
38DE60	Mohlenhoff GmbH
38E08E	Mitsubishi Electric Corporation
38E3C5	Taicang T&W Electronics
38E595	Shenzhen Gongjin Electronics Co.,Ltd
38E7D8	HTC Corporation
38E8DF	BMedien+               # b gmbh medien + datenbanken
38E98C	Reco S.p.A.
38EAA7	Hewlett Packard
38EC11	Novatek Microelectronics Corp.
38ECE4	Samsung Electronics Co.,Ltd
38ED18	Cisco Systems, Inc
38EE9D	Anedo Ltd.
38F098	Vapor Stone Rail Systems
38F0C8	Livestream
38F135	SensorTec-Canada
38F23E	Microsoft Mobile Oy
38F33F	TATSUNO CORPORATION
38F557	JOLATA, INC.
38F597	home2net GmbH
38F708	National Resource Management, Inc.
38F7B2	SEOJUN ELECTRIC
38F889	HUAWEI TECHNOLOGIES CO.,LTD
38F8B7	V2COM PARTICIPACOES S.A.
38F8CA	OWIN Inc.
38FACA	Skyworth Digital Technology(Shenzhen) Co.,Ltd
38FDFE	IEEE Registration Authority
38FEC5	Ellips B.V.
38FF36	Ruckus Wireless
3C0000	3Com
3C02B1	Creation Technologies LP
3C04BF	PRAVIS SYSTEMS Co.Ltd.,
3C0518	Samsung Electronics Co.,Ltd
3C05AB	Product Creation Studio
3C0754	Apple, Inc.
3C0771	Sony Corporation
3C081E	Beijing Yupont Electric Power Technology Co.,Ltd
3C08F6	Cisco Systems, Inc
3C096D	Powerhouse Dynamics
3C0C48	Servergy, Inc.
3C0E23	Cisco Systems, Inc
3C0FC1	KBC Networks
3C1040	daesung network
3C106F	ALBAHITH TECHNOLOGIES
3C15C2	Apple, Inc.
3C15EA	TESCOM CO., LTD.
3C189F	Nokia Corporation
3C18A0	Luxshare Precision Industry Co.,Ltd.
3C1915	GFI Chrono Time
3C197D	Ericsson AB
3C1A0F	ClearSky Data
3C1A57	Cardiopulmonary Corp
3C1A79	Huayuan Technology CO.,LTD
3C1CBE	JADAK LLC
3C1E04	D-Link International
3C1E13	HANGZHOU SUNRISE TECHNOLOGY CO., LTD
3C25D7	Nokia Corporation
3C26D5	Sotera Wireless
3C2763	SLE quality engineering GmbH & Co. KG
3C2AF4	Brother Industries, LTD.
3C2C94	杭州德澜科技有限公司（HangZhou Delan Technology Co.,Ltd）
3C2DB7	Texas Instruments
3C2F3A	SFORZATO Corp.
3C300C	Dewar Electronics Pty Ltd
3C3178	Qolsys Inc.
3C3300	Shenzhen Bilian electronic CO.,LTD
3C3556	Cognitec Systems GmbH
3C363D	Nokia Corporation
3C36E4	ARRIS Group, Inc.
3C3888	ConnectQuest, llc
3C39C3	JW Electronics Co., Ltd.
3C39E7	IEEE Registration Authority
3C3A73	Avaya Inc
3C3F51	2crsi
3C404F	GUANGDONG PISEN ELECTRONICS CO.,LTD
3C438E	ARRIS Group, Inc.
3C46D8	TP-LINK TECHNOLOGIES CO.,LTD.
3C4711	HUAWEI TECHNOLOGIES CO.,LTD
3C4937	ASSMANN Electronic GmbH
3C4A92	Hewlett Packard
3C4C69	Infinity System S.L.
3C4E47	Etronic A/S
3C5282	Hewlett Packard
3C57BD	Kessler Crane Inc.
3C57D5	Fiveco
3C591E	TCL King Electrical Appliances (Huizhou) Co., Ltd
3C5A37	Samsung Electronics Co.,Ltd
3C5AB4	Google, Inc.
3C5CC3	Shenzhen First Blue Chip Technology Ltd
3C5EC3	Cisco Systems, Inc
3C5F01	Synerchip Co., Ltd.
3C6104	Juniper Networks
3C6200	Samsung Electronics Co.,Ltd
3C6278	SHENZHEN JETNET TECHNOLOGY CO.,LTD.
3C6716	Lily Robotics
3C672C	Sciovid Inc.
3C678C	HUAWEI TECHNOLOGIES CO.,LTD
3C6816	VXi Corporation
3C6A7D	Niigata Power Systems Co., Ltd.
3C6A9D	Dexatek Technology LTD.
3C6E63	Mitron OY
3C6F45	Fiberpro Inc.
3C6FEA	Panasonic India Pvt. Ltd.
3C6FF7	EnTek Systems, Inc.
3C7059	MakerBot Industries
3C7437	Rim
3C754A	ARRIS Group, Inc.
3C77E6	Hon Hai Precision Ind. Co.,Ltd.
3C7873	Airsonics
3C7A8A	ARRIS Group, Inc.
3C7DB1	Texas Instruments
3C7F6F	Telechips, Inc.
3C80AA	Ransnet Singapore Pte Ltd
3C81D8	Sagemcom Broadband SAS
3C831E	CKD Corporation
3C8375	Microsoft Corporation
3C83B5	Advance Vision Electronics Co. Ltd.
3C86A8	Sangshin elecom .co,, LTD
3C8970	Neosfar
3C89A6	Kapelse
3C8AB0	Juniper Networks
3C8AE5	Tensun Information Technology(Hangzhou) Co.,LTD
3C8BCD	Alcatel-               # Alcatel-Lucent Shanghai Bell Co., Ltd
3C8BFE	Samsung Electronics Co.,Ltd
3C8C40	Hangzhou H3C Technologies Co., Limited
3C8CF8	TRENDnet, Inc.
3C9066	SmartRG, Inc.
3C912B	Vexata Inc
3C9157	Yulong Computer Telecommunication Scientific (Shenzhen) Co.,Ltd
3C9174	ALONG COMMUNICATION TECHNOLOGY
3C92DC	Octopod Technology Co. Ltd.
3C94D5	Juniper Networks
3C9509	Liteon Technology Corporation
3C970E	Wistron InfoComm(Kunshan)Co.,Ltd.
3C977E	IPS Technology Limited
3C98BF	Quest Controls, Inc.
3C99F7	Lansentechnology AB
3C9F81	Shenzhen CATIC Bit Communications Technology Co.,Ltd
3CA067	Liteon Technology Corporation
3CA10D	Samsung Electronics Co.,Ltd
3CA308	Texas Instruments
3CA315	Bless Information & Communications Co., Ltd
3CA31A	Oilfind International LLC
3CA348	vivo Mobile Communication Co., Ltd.
3CA72B	MRV Communications (Networks) LTD
3CA82A	Hewlett Packard
3CA9F4	Intel Corporate
3CAA3F	iKey, Ltd.
3CAB8E	Apple, Inc.
3CAE69	ESA Elektroschaltanlagen Grimma GmbH
3CB15B	Avaya Inc
3CB17F	Wattwatchers Pty Ld
3CB6B7	vivo Mobile Communication Co., Ltd.
3CB72B	PLUMgrid Inc
3CB792	Hitachi Maxell, Ltd., Optronics Division
3CB87A	Private
3CB9A6	Belden Deutschland GmbH
3CBB73	Shenzhen Xinguodu Technology Co., Ltd.
3CBBFD	Samsung Electronics Co.,Ltd
3CBD3E	Beijing Xiaomi Electronics Co., Ltd.
3CBDD8	LG ELECTRONICS INC
3CBEE1	NIKON CORPORATION
3CC0C6	d&b audiotechnik GmbH
3CC12C	AES Corporation
3CC1F6	Melange Systems Pvt. Ltd.
3CC243	Nokia Corporation
3CC2E1	XINHUA CONTROL ENGINEERING CO.,LTD
3CC99E	Huiyang Technology Co., Ltd
3CCA87	Iders Incorporated
3CCB7C	TCT mobile ltd
3CCD5A	Technische Alternative GmbH
3CCD93	LG ELECTRONICS INC
3CCE15	Mercedes-Benz USA, LLC
3CCE73	Cisco Systems, Inc
3CCF5B	ICOMM HK LIMITED
3CD0F8	Apple, Inc.
3CD16E	Telepower Communication Co., Ltd
3CD4D6	WirelessWERX, Inc
3CD7DA	SK Mtek microelectronics(shenzhen)limited
3CD92B	Hewlett Packard
3CD9CE	Eclipse WiFi
3CDA2A	zte corporation
3CDD89	SOMO HOLDINGS & TECH. CO.,LTD.
3CDF1E	Cisco Systems, Inc
3CDFA9	ARRIS Group, Inc.
3CDFBD	HUAWEI TECHNOLOGIES CO.,LTD
3CE072	Apple, Inc.
3CE5A6	Hangzhou H3C Technologies Co., Limited
3CE5B4	KIDASEN INDUSTRIA E COMERCIO DE ANTENAS LTDA
3CE624	LG Display
3CEA4F	2Wire Inc
3CEAFB	NSE AG
3CEF8C	Zhejiang Dahua Technology Co., Ltd.
3CF392	Virtualtek. Co. Ltd
3CF52C	DSPECIALISTS GmbH
3CF72A	Nokia Corporation
3CF748	Shenzhen Linsn Technology Development Co.,Ltd
3CF808	HUAWEI TECHNOLOGIES CO.,LTD
3CF862	Intel Corporate
3CFA43	HUAWEI TECHNOLOGIES CO.,LTD
3CFB96	Emcraft Systems LLC
3CFDFE	Intel Corporate
400003	NetWare?	# Net Ware (?)
4000E0	Derek(Shaoguan)Limited
400107	Arista Corp
4001C6	3COM EUROPE LTD
40040C	A&T
4007C0	Railtec Systems GmbH
400D10	ARRIS Group, Inc.
400E67	Tremol Ltd.
400E85	SAMSUNG ELECTRO-MECHANICS(THAILAND)
4011DC	Sonance
4012E4	Compass-               # Compass-EOS
4013D9	Global ES
401597	Protect America, Inc.
40163B	Samsung Electronics Co.,Ltd
40167E	ASUSTek COMPUTER INC.
40169F	TP-LINK TECHNOLOGIES CO.,LTD.
4016FA	EKM Metering
4018B1	Aerohive Networks Inc.
4018D7	Smartronix, Inc.
401B5F	Weifang GoerTek Electronics Co., Ltd.
401D59	Biometric Associates, LP
4022ED	Digital Projection Ltd
4025C2	Intel Corporate
40270B	Mobileeco Co., Ltd
402814	RFI Engineering
402BA1	Sony Mobile Communications AB
402CF4	Universal Global Scientific Industrial Co., Ltd.
402E28	MiXTelematics
403004	Apple, Inc.
403067	Conlog (Pty) Ltd
40331A	Apple, Inc.
40336C	Godrej & Boyce Mfg. co. ltd
4037AD	Macro Image Technology, Inc.
403CFC	Apple, Inc.
403DEC	HUMAX Co., Ltd.
403F8C	TP-LINK TECHNOLOGIES CO.,LTD.
404022	Ziv
40406B	Icomera
4040A7	Sony Mobile Communications AB
4045DA	Spreadtrum Communications (Shanghai) Co., Ltd.
40476A	AG Acquisition Corp. d.b.a. ASTRO Gaming
40490F	Hon Hai Precision Ind. Co.,Ltd.
404A03	ZyXEL Communications Corporation
404A18	Addrek Smart Solutions
404AD4	Widex A/S
404D7F	Apple, Inc.
404D8E	HUAWEI TECHNOLOGIES CO.,LTD
404E36	HTC Corporation
404EEB	Higher Way Electronic Co., Ltd.
4050E0	Milton Security Group LLC
40516C	Grandex International Corporation
40520D	Pico Technology
4054E4	Wearsafe Labs Inc
405539	Cisco Systems, Inc
40560C	In Home Displays Ltd
40562D	Smartron India Pvt ltd
405A9B	Anovo
405CFD	Dell Inc.
405D82	Netgear
405EE1	Shenzhen H&T Intelligent Control Co.,Ltd.
405FBE	Rim
405FC2	Texas Instruments
40605A	Hawkeye Tech Co. Ltd
406186	MICRO-STAR INT'L CO.,LTD
40618E	Stella-Green Co
4062B6	Tele system communication
4065A3	Sagemcom Broadband SAS
40667A	Mediola-               # mediola - connected living AG
406826	Thales UK Limited
406AAB	Rim
406C8F	Apple, Inc.
406F2A	BlackBerry RTS
407009	ARRIS Group, Inc.
40704A	Power Idea Technology Limited
407074	Life Technology (China) Co., Ltd
407183	Juniper Networks
407496	aFUN TECHNOLOGY INC.
40786A	Motorola Mobility LLC, a Lenovo Company
407875	IMBEL - Industria de Material Belico do Brasil
407A80	Nokia Corporation
407B1B	Mettle Networks Inc.
407C7D	Nokia
407D0F	HUAWEI TECHNOLOGIES CO.,LTD
407FE0	Glory Star Technics (ShenZhen) Limited
408256	Continental Automotive GmbH
4083DE	Zebra Technologies Inc
408493	Clavister AB
40862E	JDM MOBILE INTERNET SOLUTION CO., LTD.
408805	Motorola Mobility LLC, a Lenovo Company
4088E0	Beijing Ereneben Information Technology Limited Shenzhen Branch
408A9A	TITENG CO., Ltd.
408B07	Actiontec Electronics, Inc
408BF6	Shenzhen TCL New Technology Co; Ltd.
408D5C	GIGA-BYTE TECHNOLOGY CO.,LTD.
409558	Aisino Corporation
4095BD	NTmore.Co.,Ltd
4097D1	BK Electronics cc
40984C	Casacom Solutions AG
40984E	Texas Instruments
40987B	Aisino Corporation
409B0D	Shenzhen Yourf Kwan Industrial Co., Ltd
409F38	AzureWave Technology Inc.
409F87	Jide Technology (Hong Kong) Limited
409FC7	BAEKCHUN I&C Co., Ltd.
40A5EF	Shenzhen Four Seas Global Link Network Technology Co., Ltd.
40A677	Juniper Networks
40A6A4	PassivSystems Ltd
40A6D9	Apple, Inc.
40A6E8	Cisco Systems, Inc
40A8F0	Hewlett Packard
40AC8D	Data Management, Inc.
40B034	Hewlett Packard
40B0FA	LG Electronics (Mobile Communications)
40B2C8	Nortel Networks
40B395	Apple, Inc.
40B3CD	Chiyoda Electronics Co.,Ltd.
40B3FC	Logital Co. Limited
40B4CD	Amazon Technologies Inc.
40B4F0	Juniper Networks
40B688	LEGIC Identsystems AG
40B6B1	SUNGSAM CO,.Ltd
40B7F3	ARRIS Group, Inc.
40B837	Sony Mobile Communications AB
40B89A	Hon Hai Precision Ind. Co.,Ltd.
40B93C	Hewlett Packard Enterprise
40BA61	ARIMA Communications Corp.
40BC73	Cronoplast  S.L.
40BC8B	itelio GmbH
40BD9E	Physio-Control, Inc
40BF17	Digistar Telecom. SA
40C245	Shenzhen Hexicom Technology Co., Ltd.
40C4D6	ChongQing Camyu Technology Development Co.,Ltd.
40C62A	Shanghai Jing Ren Electronic Technology Co., Ltd.
40C729	Sagemcom Broadband SAS
40C7C9	Naviit Inc.
40C8CB	AM Telecom co., Ltd.
40CBA8	HUAWEI TECHNOLOGIES CO.,LTD
40CD3A	Z3 Technology
40D28A	Nintendo Co., Ltd.
40D32D	Apple, Inc.
40D357	Ison Technology Co., Ltd.
40D3AE	Samsung Electronics Co.,Ltd
40D40E	Biodata Ltd
40D559	MICRO S.E.R.I.
40D855	IEEE Registration Authority
40E230	AzureWave Technology Inc.
40E3D6	Aruba Networks
40E730	DEY Storage Systems, Inc.
40E793	Shenzhen Siviton Technology Co.,Ltd
40EACE	FOUNDER BROADBAND NETWORK SERVICE CO.,LTD
40ECF8	Siemens AG
40ED98	IEEE Registration Authority
40EF4C	Fihonest communication co.,Ltd
40F02F	Liteon Technology Corporation
40F14C	ISE Europe SPRL
40F201	Sagemcom Broadband SAS
40F2E9	Ibm
40F308	Murata Manufacturing Co., Ltd.
40F385	IEEE Registration Authority
40F407	Nintendo Co., Ltd.
40F413	Rubezh
40F420	SICHUAN TIANYI COMHEART TELECOMCO.,LTD
40F4EC	Cisco Systems, Inc
40F52E	Leica Microsystems (Schweiz) AG
40FA7F	Preh Car Connect GmbH
40FC89	ARRIS Group, Inc.
40FE0D	Maxio
440010	Apple, Inc.
44032C	Intel Corporate
4403A7	Cisco Systems, Inc
440444	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
4409B8	Salcomp (Shenzhen) CO., LTD.
440CFD	NetMan Co., Ltd.
441102	EDMI  Europe Ltd
4411C2	Telegartner Karl Gartner GmbH
441319	WKK TECHNOLOGY LTD.
441441	AudioControl Inc.
44184F	Fitview
4419B6	Hangzhou Hikvision Digital Technology Co.,Ltd.
441CA8	Hon Hai Precision Ind. Co.,Ltd.
441E91	ARVIDA Intelligent Electronics Technology  Co.,Ltd.
441EA1	Hewlett Packard
4423AA	Farmage Co., Ltd.
4425BB	Bamboo Entertainment Corporation
442938	NietZsche enterprise Co.Ltd.
442A60	Apple, Inc.
442AFF	E3 Technology, Inc.
442B03	Cisco Systems, Inc
442C05	AMPAK Technology, Inc.
443192	Hewlett Packard
44322A	Avaya Inc
4432C8	Technicolor CH USA Inc.
44334C	Shenzhen Bilian electronic CO.,LTD
44348F	MXT INDUSTRIAL LTDA
44356F	Neterix
443708	MRV Comunications
443719	2 Save Energy Ltd
44376F	Young Electric Sign Co
4437E6	Hon Hai Precision Ind. Co.,Ltd.
443839	Cumulus Networks, inc
4439C4	Universal Global Scientific Industrial Co., Ltd.
443C9C	Pintsch Tiefenbach GmbH
443D21	Nuvolt
443EB2	DEOTRON Co., LTD.
444450	Ottoq
444553	Microsoft
444649	DFI (Diamond Flower Industries)
444891	HDMI Licensing, LLC
4448C1	Hewlett Packard Enterprise
444A65	Silverflare Ltd.
444C0C	Apple, Inc.
444CA8	Arista Networks
444E1A	Samsung Electronics Co.,Ltd
444F5E	Pan Studios Co.,Ltd.
4451DB	Raytheon BBN Technologies
4454C0	Thompson Aerospace
4455B1	HUAWEI TECHNOLOGIES CO.,LTD
44568D	PNC Technologies  Co., Ltd.
4456B7	Spawn Labs, Inc
445829	Cisco SPVTG
44599F	Criticare Systems, Inc
445ECD	Razer Inc
445EF3	Tonalite Holding B.V.
445F7A	Shihlin Electric & Engineering Corp.
445F8C	Intercel Group Limited
446132	ecobee inc
44619C	FONsystem co. ltd.
446246	Comat AG
44650D	Amazon Technologies Inc.
44656A	Mega Video Electronic(HK) Industry Co., Ltd
44666E	Ip-Line
446755	Orbit Irrigation
4468AB	JUIN COMPANY, LIMITED
446A2E	HUAWEI TECHNOLOGIES CO.,LTD
446AB7	ARRIS Group, Inc.
446C24	Reallin Electronic Co.,Ltd
446D57	Liteon Technology Corporation
446D6C	Samsung Electronics Co.,Ltd
446EE5	HUAWEI TECHNOLOGIES CO.,LTD
44700B	Iffu
447098	MING HONG TECHNOLOGY (SHEN ZHEN) LIMITED
4473D6	Logitech
44746C	Sony Mobile Communications AB
44783E	Samsung Electronics Co.,Ltd
447BC4	DualShine Technology(SZ)Co.,Ltd
447C7F	Innolight Technology Corporation
447DA5	VTION INFORMATION TECHNOLOGY (FUJIAN) CO.,LTD
447E76	Trek Technology (S) Pte Ltd
447E95	Alpha and Omega, Inc
4480EB	Motorola Mobility LLC, a Lenovo Company
4482E5	HUAWEI TECHNOLOGIES CO.,LTD
448312	Star-Net
448500	Intel Corporate
4486C1	Siemens Low Voltage & Products
448723	HOYA SERVICE CORPORATION
4487FC	Elitegroup Computer Systems Co.,Ltd.
4488CB	Camco Technologies NV
448A5B	Micro-Star INT'L CO., LTD.
448C52	KTIS CO., Ltd
448E12	DT Research, Inc.
448E81	Vig
4491DB	Shanghai Huaqin Telecom Technology Co.,Ltd
4494FC	Netgear
4495FA	Qingdao Santong Digital Technology Co.Ltd
44962B	Aidon Oy
44975A	SHENZHEN FAST TECHNOLOGIES CO.,LTD
449B78	The Now Factory
449CB5	Alcomp, Inc
449F7F	DataCore Software Corporation
44A42D	TCT mobile ltd
44A689	PROMAX ELECTRONICA SA
44A6E5	THINKING TECHNOLOGY CO.,LTD
44A7CF	Murata Manufacturing Co., Ltd.
44A842	Dell Inc.
44A8C2	SEWOO TECH CO., LTD
44AA27	udworks Co., Ltd.
44AA50	Juniper Networks
44AAE8	Nanotec Electronic GmbH & Co. KG
44AAF5	ARRIS Group, Inc.
44ADD9	Cisco Systems, Inc
44B32D	TP-LINK TECHNOLOGIES CO.,LTD.
44B382	Kuang-chi Institute of Advanced Technology
44B412	SIUS AG
44BA46	SICHUAN TIANYI COMHEART TELECOMCO.,LTD
44BFE3	Shenzhen Longtech Electronics Co.,Ltd
44C15C	Texas Instruments
44C233	Guangzhou Comet Technology Development Co.Ltd
44C306	SIFROM Inc.
44C346	HUAWEI TECHNOLOGIES CO.,LTD
44C39B	OOO RUBEZH NPO
44C4A9	Opticom Communication, LLC
44C56F	NGN Easy Satfinder (Tianjin) Electronic Co., Ltd
44C69B	Wuhan Feng Tian Information Network CO.,LTD
44C9A2	Greenwald Industries
44CE7D	Sfr
44D15E	Shanghai Kingto Information Technology Ltd
44D1FA	Shenzhen Yunlink Technology Co., Ltd
44D244	Seiko Epson Corporation
44D2CA	Anvia TV Oy
44D3CA	Cisco Systems, Inc
44D437	Inteno Broadband Technology AB
44D4E0	Sony Mobile Communications AB
44D63D	Talari Networks
44D6E1	Snuza International Pty. Ltd.
44D832	AzureWave Technology Inc.
44D884	Apple, Inc.
44D9E7	Ubiquiti Networks Inc.
44DC91	PLANEX COMMUNICATIONS INC.
44DCCB	SEMINDIA SYSTEMS PVT LTD
44E08E	Cisco SPVTG
44E137	ARRIS Group, Inc.
44E49A	OMNITRONICS PTY LTD
44E4D9	Cisco Systems, Inc
44E8A5	Myreka Technologies Sdn. Bhd.
44E9DD	Sagemcom Broadband SAS
44ED57	Longicorn, inc.
44EE02	MTI Ltd.
44EE30	Budelmann Elektronik GmbH
44F436	zte corporation
44F459	Samsung Electronics Co.,Ltd
44F477	Juniper Networks
44F849	Union Pacific Railroad
44FB42	Apple, Inc.
44FDA3	Everysight LTD.
475443	GTC (Not registered!)		(This number is a multicast!)
480031	HUAWEI TECHNOLOGIES CO.,LTD
480033	Technicolor CH USA Inc.
48022A	B-Link Electronic Limited
480362	DESAY ELECTRONICS(HUIZHOU)CO.,LTD
48066A	Tempered Networks, Inc.
480C49	NAKAYO Inc
480FCF	Hewlett Packard
481063	NTT Innovation Institute, Inc.
481249	Luxcom Technologies Inc.
48137E	Samsung Electronics Co.,Ltd
4813F3	BBK EDUCATIONAL ELECTRONICS CORP.,LTD.
48174C	MicroPower technologies
481842	Shanghai Winaas Co. Equipment Co. Ltd.
481A84	Pointer Telocation Ltd
481BD2	Intron Scientific co., ltd.
481D70	Cisco SPVTG
4826E8	Tek-Air Systems, Inc.
4827EA	Samsung Electronics Co.,Ltd
48282F	zte corporation
482CEA	Motorola Inc Business Light Radios
4833DD	ZENNIO AVANCE Y TECNOLOGIA, S.L.
48343D	IEP GmbH
48365F	Wintecronics Ltd.
483974	Proware Technologies Co., Ltd.
483B38	Apple, Inc.
483C0C	HUAWEI TECHNOLOGIES CO.,LTD
483D32	Syscor Controls &amp; Automation
48435A	HUAWEI TECHNOLOGIES CO.,LTD
48437C	Apple, Inc.
484453	Hds???		# HDS ???
484487	Cisco SPVTG
4844F7	Samsung Electronics Co.,Ltd
484520	Intel Corporate
4846F1	Uros Oy
4846FB	HUAWEI TECHNOLOGIES CO.,LTD
4849C7	Samsung Electronics Co.,Ltd
484BAA	Apple, Inc.
484C00	Network Solutions
484D7E	Dell Inc.
485073	Microsoft Corporation
4851B7	Intel Corporate
485261	Soreel
485415	NET RULES TECNOLOGIA EIRELI
4854E8	Winbond?
48555F	Fiberhome Telecommunication Technologies Co.,LTD
4857DD	Facebook
485929	LG Electronics (Mobile Communications)
485A3F	Wisol
485AB6	Hon Hai Precision Ind. Co.,Ltd.
485B39	ASUSTek COMPUTER INC.
485D36	Verizon
485D60	AzureWave Technology Inc.
4860BC	Apple, Inc.
4861A3	Concern Axion JSC
486276	HUAWEI TECHNOLOGIES CO.,LTD
4865EE	IEEE Registration Authority
486B2C	BBK EDUCATIONAL ELECTRONICS CORP.,LTD.
486B91	Fleetwood Group Inc.
486DBB	Vestel Elektronik San ve Tic. A.Ş.
486E73	Pica8, Inc.
486EFB	Davit System Technology Co., Ltd.
486FD2	StorSimple Inc
487119	SGB GROUP LTD.
48746E	Apple, Inc.
487604	Private
487A55	ALE International
487ADA	Hangzhou H3C Technologies Co., Limited
487B6B	HUAWEI TECHNOLOGIES CO.,LTD
488244	Life Fitness / Div. of Brunswick
4882F2	Appel Elektronik GmbH
4883C7	Sagemcom Broadband SAS
4886E8	Microsoft Corporation
488803	ManTechnology Inc.
4888CA	Motorola (Wuhan) Mobility Technologies Communication Co., Ltd.
488AD2	SHENZHEN MERCURY COMMUNICATION TECHNOLOGIES CO.,LTD.
488E42	DIGALOG GmbH
489153	Weinmann Geräte für Medizin GmbH + Co. KG
4891F6	Shenzhen Reach software technology CO.,LTD
489A42	Technomate Ltd
489BE2	SCI Innovations Ltd
489D18	Flashbay Limited
489D24	BlackBerry RTS
48A195	Apple, Inc.
48A22D	Shenzhen Huaxuchang Telecom Technology Co.,Ltd
48A2B7	Kodofon JSC
48A380	Gionee Communication Equipment Co.,Ltd.
48A6D2	GJsun Optical Science and Tech Co.,Ltd.
48A74E	zte corporation
48A9D2	Wistron Neweb Corporation
48AA5D	Store Electronic Systems
48AD08	HUAWEI TECHNOLOGIES CO.,LTD
48B253	Marketaxess Corporation
48B5A7	Glory Horse Industries Ltd.
48B620	ROLI Ltd.
48B8DE	HOMEWINS TECHNOLOGY CO.,LTD.
48B977	PulseOn Oy
48B9C2	Teletics Inc.
48BE2D	Symanitron
48BF6B	Apple, Inc.
48BF74	Baicells Technologies Co.,LTD
48C049	Broad Telecom SA
48C093	Xirrus, Inc.
48C1AC	PLANTRONICS, INC.
48C663	GTO Access Systems LLC
48C862	Simo Wireless,Inc.
48C8B6	SysTec GmbH
48CB6E	Cello Electronics (UK) Ltd
48D0CF	Universal Electronics, Inc.
48D18E	Metis Communication Co.,Ltd
48D224	Liteon Technology Corporation
48D343	ARRIS Group, Inc.
48D539	HUAWEI TECHNOLOGIES CO.,LTD
48D54C	Jeda Networks
48D705	Apple, Inc.
48D7FF	BLANKOM Antennentechnik GmbH
48D855	Telvent
48D8FE	ClarIDy Solutions, Inc.
48DA96	Eddy Smart Home Solutions Inc.
48DB50	HUAWEI TECHNOLOGIES CO.,LTD
48DCFB	Nokia Corporation
48DF1C	Wuhan NEC Fibre Optic Communications industry Co. Ltd
48DF37	Hewlett Packard Enterprise
48E1AF	Vity
48E244	Hon Hai Precision Ind. Co.,Ltd.
48E9F1	Apple, Inc.
48EA63	Zhejiang Uniview Technologies Co., Ltd.
48EB30	ETERNA TECHNOLOGY, INC.
48ED80	daesung eltec
48EE07	Silver Palm Technologies LLC
48EE0C	D-Link International
48EE86	UTStarcom (China) Co.,Ltd
48F07B	ALPS ELECTRIC CO.,LTD.
48F230	Ubizcore Co.,LTD
48F317	Private
48F47D	TechVision Holding  Internation Limited
48F7C0	Technicolor CH USA Inc.
48F7F1	Nokia
48F8B3	Cisco-Linksys, LLC
48F8E1	Nokia
48F925	Maestronic
48F97C	Fiberhome Telecommunication Technologies Co.,LTD
48FCB6	LAVA INTERNATIONAL(H.K) LIMITED
48FCB8	Woodstream Corporation
48FD8E	HUAWEI TECHNOLOGIES CO.,LTD
48FEEA	HOMA B.V.
4C0082	Cisco Systems, Inc
4C022E	CMR KOREA CO., LTD
4C0289	LEX COMPUTECH CO., LTD
4C068A	Basler Electric Company
4C07C9	COMPUTER OFFICE Co.,Ltd.
4C09B4	zte corporation
4C09D4	Arcadyan Technology Corporation
4C0B3A	TCT mobile ltd
4C0BBE	Microsoft
4C0DEE	JABIL CIRCUIT (SHANGHAI) LTD.
4C0F6E	Hon Hai Precision Ind. Co.,Ltd.
4C0FC7	Earda Electronics Co.,Ltd
4C11BF	Zhejiang Dahua Technology Co., Ltd.
4C1480	NOREGON SYSTEMS, INC
4C14A3	TCL Technoly Electronics (Huizhou) Co., Ltd.
4C1694	shenzhen sibituo Technology Co., Ltd
4C16F1	zte corporation
4C17EB	Sagemcom Broadband SAS
4C1A3A	PRIMA Research And Production Enterprise Ltd.
4C1A3D	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
4C1A95	Novakon Co., Ltd.
4C1FCC	HUAWEI TECHNOLOGIES CO.,LTD
4C21D0	Sony Mobile Communications AB
4C2258	cozybit, Inc.
4C2578	Nokia Corporation
4C26E7	Welgate Co., Ltd.
4C2C80	Beijing Skyway Technologies Co.,Ltd
4C2C83	Zhejiang KaNong Network Technology Co.,Ltd.
4C2F9D	ICM Controls
4C3089	Thales Transportation Systems GmbH
4C322D	TELEDATA NETWORKS
4C3275	Apple, Inc.
4C32D9	M Rutty Holdings Pty. Ltd.
4C334E	Hightech
4C3488	Intel Corporate
4C38D5	MITAC COMPUTING TECHNOLOGY CORPORATION
4C3909	HPL Electric & Power Private Limited
4C3910	Newtek Electronics co., Ltd.
4C3B74	VOGTEC(H.K.) Co., Ltd
4C3C16	Samsung Electronics Co.,Ltd
4C424C	Information Modes software modified addresses (not registered?)
4C48DA	Beijing Autelan Technology Co.,Ltd
4C4B68	Mobile Device, Inc.
4C4E03	TCT mobile ltd
4C4E35	Cisco Systems, Inc
4C5427	Linepro Sp. z o.o.
4C5499	HUAWEI TECHNOLOGIES CO.,LTD
4C5585	Hamilton Systems
4C55B8	Turkcell Teknoloji
4C55CC	Zentri Pty Ltd
4C57CA	Apple, Inc.
4C5DCD	Oy Finnish Electric Vehicle Technologies Ltd
4C5E0C	Routerboard.com
4C5FD2	Alcatel-               # Alcatel-Lucent
4C60D5	airPointe of New Hampshire
4C60DE	Netgear
4C6255	Sanmina-               # SANMINA-SCI SYSTEM DE MEXICO S.A. DE C.V.
4C63EB	Application Solutions (Electronics and Vision) Ltd
4C64D9	Guangdong Leawin Group Co., Ltd
4C6641	SAMSUNG ELECTRO-MECHANICS(THAILAND)
4C6E6E	Comnect Technology CO.,LTD
4C72B9	PEGATRON CORPORATION
4C7367	Genius Bytes Software Solutions GmbH
4C73A5	Kove
4C7403	Bq
4C7487	Leader Phone Communication Technology Co., Ltd.
4C74BF	Apple, Inc.
4C7625	Dell Inc.
4C774F	Embedded Wireless Labs
4C7872	Cav. Uff. Giacomo Cimberio S.p.A.
4C7897	Arrowhead Alarm Products Ltd
4C79BA	Intel Corporate
4C7C5F	Apple, Inc.
4C7F62	Nokia Corporation
4C804F	Armstrong Monitoring Corp
4C8093	Intel Corporate
4C8120	Taicang T&W Electronics
4C82CF	Echostar Technologies Corp
4C83DE	Cisco SPVTG
4C8B30	Actiontec Electronics, Inc
4C8B55	Grupo Digicon
4C8BEF	HUAWEI TECHNOLOGIES CO.,LTD
4C8D79	Apple, Inc.
4C8ECC	SILKAN SA
4C8FA5	Jastec
4C9614	Juniper Networks
4C98EF	Zeo
4C9E80	KYOKKO ELECTRIC Co., Ltd.
4C9EE4	Hanyang Navicom Co.,Ltd.
4C9EFF	ZyXEL Communications Corporation
4CA003	T-21 Technologies LLC
4CA161	Rain Bird Corporation
4CA515	Baikal Electronics JSC
4CA56D	Samsung Electronics Co.,Ltd
4CA74B	Alcatel Lucent
4CA928	Insensi
4CAA16	AzureWave Technologies (Shanghai) Inc.
4CAB33	KST technology
4CAC0A	zte corporation
4CAE31	ShengHai Electronics (Shenzhen) Ltd
4CB0E8	Beijing RongZhi xinghua technology co., LTD
4CB16C	HUAWEI TECHNOLOGIES CO.,LTD
4CB199	Apple, Inc.
4CB21C	Maxphotonics Co.,Ltd
4CB44A	NANOWAVE Technologies Inc.
4CB4EA	HRD (S) PTE., LTD.
4CB76D	Novi Security
4CB81C	SAM Electronics GmbH
4CB82C	Cambridge Mobile Telematics, Inc.
4CB8B5	Shenzhen YOUHUA Technology Co., Ltd
4CB9C8	CONET CO., LTD.
4CBAA3	Bison Electronics Inc.
4CBB58	Chicony Electronics Co., Ltd.
4CBC42	Shenzhen Hangsheng Electronics Co.,Ltd.
4CBCA5	Samsung Electronics Co.,Ltd
4CC452	Shang Hai Tyd. Electon Technology Ltd.
4CC602	Radios, Inc.
4CC681	Shenzhen Aisat Electronic Co., Ltd.
4CC94F	Nokia
4CCA53	Skyera, Inc.
4CCBF5	zte corporation
4CCC34	Motorola Solutions Inc.
4CCC6A	Micro-Star INTL CO., LTD.
4CD08A	HUMAX Co., Ltd.
4CD637	Qsono Electronics Co., Ltd
4CD7B6	Helmer Scientific
4CD9C4	Magneti Marelli Automotive Electronics (Guangzhou) Co. Ltd
4CDF3D	TEAM ENGINEERS ADVANCE TECHNOLOGIES INDIA PVT LTD
4CE173	IEEE Registration Authority
4CE1BB	Zhuhai HiFocus Technology Co., Ltd.
4CE2F1	sclak srl
4CE676	BUFFALO.INC
4CE933	RailComm, LLC
4CEB42	Intel Corporate
4CECEF	Soraa, Inc.
4CEDDE	ASKEY COMPUTER CORP
4CEEB0	SHC Netzwerktechnik GmbH
4CF02E	Vifa Denmark A/S
4CF2BF	Cambridge Industries(Group) Co.,Ltd.
4CF45B	Blue Clover Devices
4CF5A0	Scalable Network Technologies Inc
4CF737	SamJi Electronics Co., Ltd
4CF95D	HUAWEI TECHNOLOGIES CO.,LTD
4CFACA	Cambridge Industries(Group) Co.,Ltd.
4CFB45	HUAWEI TECHNOLOGIES CO.,LTD
4CFF12	Fuze Entertainment Co., ltd
50008C	Hong Kong Telecommunications (HKT) Limited
50016B	HUAWEI TECHNOLOGIES CO.,LTD
5001BB	Samsung Electronics Co.,Ltd
5001D9	HUAWEI TECHNOLOGIES CO.,LTD
5004B8	HUAWEI TECHNOLOGIES CO.,LTD
50053D	CyWee Group Ltd
500604	Cisco Systems, Inc
5006AB	Cisco Systems, Inc
500959	Technicolor CH USA Inc.
500B32	Foxda Technology Industrial(ShenZhen)Co.,LTD
500B91	IEEE Registration Authority
500E6D	TrafficCast International
500FF5	Tenda Technology Co.,Ltd.Dongguan branch
5011EB	SilverNet Ltd
5014B5	Richfit Information Technology Co., Ltd
5017FF	Cisco Systems, Inc
501AA5	GN Netcom A/S
501AC5	Microsoft
501CBF	Cisco Systems, Inc
501E2D	StreamUnlimited Engineering GmbH
50206B	Emerson Climate Technologies Transportation Solutions
502267	Pixelink
50252B	Nethra Imaging Incorporated
502690	FUJITSU LIMITED
5027C7	TECHNART Co.,Ltd
50294D	NANJING IOT SENSOR TECHNOLOGY CO,LTD
502A7E	Smart electronic GmbH
502A8B	Telekom Research and Development Sdn Bhd
502B73	Tenda Technology Co.,Ltd.Dongguan branch
502D1D	Nokia Corporation
502DA2	Intel Corporate
502DF4	Phytec Messtechnik GmbH
502E5C	HTC Corporation
502ECE	Asahi Electronics Co.,Ltd
5031AD	ABB Global Industries and Services Private Limited
503237	Apple, Inc.
503275	Samsung Electronics Co.,Ltd
50338B	Texas Instruments
503955	Cisco SPVTG
503A7D	AlphaTech PLC Int’l Co., Ltd.
503AA0	SHENZHEN MERCURY COMMUNICATION TECHNOLOGIES CO.,LTD.
503CC4	Lenovo Mobile Communication Technology Ltd.
503DA1	Samsung Electronics Co.,Ltd
503DE5	Cisco Systems, Inc
503F56	Syncmold Enterprise Corp
503F98	Cmitech
504061	Nokia
5045F7	Liuhe Intelligence Technology Ltd.
50465D	ASUSTek COMPUTER INC.
5048EB	BEIJING HAIHEJINSHENG NETWORK TECHNOLOGY CO. LTD.
504A5E	Masimo Corporation
504A6E	Netgear
504B5B	CONTROLtronic GmbH
504F94	Loxone Electronics GmbH
50502A	Egardia
505065	TAKT Corporation
5052D2	Hangzhou Telin Technologies Co., Limited
505527	LG Electronics (Mobile Communications)
505663	Texas Instruments
5056A8	Jolla Ltd
5056BF	Samsung Electronics Co.,Ltd
5057A8	Cisco Systems, Inc
505800	WyTec International, Inc.
50584F	waytotec,Inc.
505AC6	GUANGDONG SUPER TELECOM CO.,LTD.
506028	Xirrus Inc.
506184	Avaya Inc
5061D6	Indu-Sol GmbH
506313	Hon Hai Precision Ind. Co.,Ltd.
506441	Greenlee
506583	Texas Instruments
5065F3	Hewlett Packard
506787	Planet Networks
5067AE	Cisco Systems, Inc
5067F0	ZyXEL Communications Corporation
50680A	HUAWEI TECHNOLOGIES CO.,LTD
506A03	Netgear
506B8D	Nutanix
506F9A	Wi-Fi Alliance
5070E5	He Shan World Fair Electronics Technology Limited
507224	Texas Instruments
50724D	BEG Brueck Electronic GmbH
507691	Tekpea, Inc.
5076A6	Ecil Informatica Ind. Com. Ltda
50795B	Interexport Telecomunicaciones S.A.
507A55	Apple, Inc.
507B9D	LCFC(HeFei) Electronics Technology co., ltd
507D02	Biodit
507E5D	Arcadyan Technology Corporation
5082D5	Apple, Inc.
508569	Samsung Electronics Co.,Ltd
508789	Cisco Systems, Inc
5087B8	Nuvyyo Inc
508965	SHENZHEN MERCURY COMMUNICATION TECHNOLOGIES CO.,LTD.
508A0F	SHENZHEN FISE TECHNOLOGY HOLDING CO.,LTD.
508A42	Uptmate Technology Co., LTD
508ACB	SHENZHEN MAXMADE TECHNOLOGY CO., LTD.
508C77	DIRMEIER Schanktechnik GmbH &Co KG
508CB1	Texas Instruments
508D6F	CHAHOO Limited
50934F	Gradual Tecnologia Ltda.
509772	Westinghouse Digital
509871	Inventum Technologies Private Limited
5098F3	Rheem Australia Pty Ltd
509A4C	Dell Inc.
509EA7	Samsung Electronics Co.,Ltd
509F27	HUAWEI TECHNOLOGIES CO.,LTD
509F3B	OI ELECTRIC CO.,LTD
50A054	Actineon
50A0BF	Alba Fiber Systems Inc.
50A4C8	Samsung Electronics Co.,Ltd
50A4D0	IEEE Registration Authority
50A6E3	David Clark Company
50A715	Aboundi, Inc.
50A72B	HUAWEI TECHNOLOGIES CO.,LTD
50A733	Ruckus Wireless
50A9DE	Smartcom - Bulgaria AD
50AB3E	Qibixx AG
50ABBF	Hoseo Telecom
50ADD5	Dynalec Corporation
50AF73	Shenzhen Bitland Information Technology Co., Ltd.
50B363	Digitron da Amazonia S/A
50B695	Micropoint Biotechnologies,Inc.
50B7C3	Samsung Electronics Co.,Ltd
50B888	wi2be Tecnologia S/A
50B8A2	ImTech Technologies LLC,
50BD5F	TP-LINK TECHNOLOGIES CO.,LTD.
50C006	Carmanah Signs
50C271	SECURETECH INC
50C58D	Juniper Networks
50C7BF	TP-LINK TECHNOLOGIES CO.,LTD.
50C8E5	Samsung Electronics Co.,Ltd
50C971	GN Netcom A/S
50C9A0	SKIPPER Electronics AS
50CCF8	SAMSUNG ELECTRO MECHANICS CO., LTD.
50CD22	Avaya Inc
50CD32	NanJing Chaoran Science & Technology Co.,Ltd.
50CE75	Measy Electronics Co., Ltd.
50D213	CviLux Corporation
50D274	Steffes Corporation
50D37F	Yu Fly Mikly Way Science and Technology Co., Ltd.
50D59C	Thai Habel Industrial Co., Ltd.
50D6D7	Takahata Precision
50D753	CONELCOM GmbH
50DA00	Hangzhou H3C Technologies Co., Limited
50DD4F	Automation Components, Inc
50DF95	Lytx
50E0C7	TurControlSystme AG
50E14A	Private
50E549	GIGA-BYTE TECHNOLOGY CO.,LTD.
50E666	Shenzhen Techtion Electronics Co., Ltd.
50EAD6	Apple, Inc.
50EB1A	Brocade Communications Systems, Inc.
50ED78	Changzhou Yongse Infotech Co.,Ltd
50ED94	EGATEL SL
50F003	Open Stack, Inc.
50F0D3	Samsung Electronics Co.,Ltd
50F14A	Texas Instruments
50F43C	Leeo Inc
50F520	Samsung Electronics Co.,Ltd
50F5DA	Amazon Technologies Inc.
50F61A	Kunshan JADE Technologies co., Ltd.
50FA84	TP-LINK TECHNOLOGIES CO.,LTD.
50FAAB	L-tek d.o.o.
50FC30	Treehouse Labs
50FC9F	Samsung Electronics Co.,Ltd
50FEF2	Sify Technologies Ltd
50FF20	Keenetic Limited
50FF99	IEEE Registration Authority
525400	Realtek (UpTech? also reported)
52544C	Novell 2000
5254AB	REALTEK (a Realtek 8029 based PCI Card)
540384	Hangkong Nano IC Technologies Co., Ltd
5403F5	EBN Technology Corp.
540496	Gigawave LTD
5404A6	ASUSTek COMPUTER INC.
540536	Vivago Oy
54055F	Alcatel Lucent
540593	WOORI ELEC Co.,Ltd
540955	zte corporation
54098D	deister electronic GmbH
5410EC	Microchip Technology Inc.
54112F	Sulzer Pump Solutions Finland Oy
54115F	Atamo Pty Ltd
541379	Hon Hai Precision Ind. Co.,Ltd.
541473	Wingtech Group (HongKong）Limited
5414FD	Orbbec 3D Technology International
5419C8	vivo Mobile Communication Co., Ltd.
541B5D	Techno-Innov
541DFB	Freestyle Energy Ltd
541E56	Juniper Networks
541FD5	Advantage Electronics
542018	Tely Labs
542160	Resolution Products
5422F8	zte corporation
5425EA	HUAWEI TECHNOLOGIES CO.,LTD
542696	Apple, Inc.
54271E	AzureWave Technology Inc.
542758	Motorola (Wuhan) Mobility Technologies Communication Co., Ltd.
54276C	Jiangsu Houge Technology Corp.
542A9C	LSY Defense, LLC.
542AA2	Alpha Networks Inc.
542B57	Night Owl SP
542CEA	PROTECTRON
542F89	Euclid Laboratories, Inc.
542F8A	TELLESCOM INDUSTRIA E COMERCIO EM TELECOMUNICACAO
543131	Raster Vision Ltd
543530	Hon Hai Precision Ind. Co.,Ltd.
5435DF	Symeo GmbH
54369B	1Verge Internet Technology (Beijing) Co., Ltd.
543968	Edgewater Networks Inc
5439DF	HUAWEI TECHNOLOGIES CO.,LTD
543B30	duagon AG
543D37	Ruckus Wireless
5440AD	Samsung Electronics Co.,Ltd
544249	Sony Corporation
544408	Nokia Corporation
54466B	Shenzhen CZTIC Electronic Technology Co., Ltd
54489C	CDOUBLES ELECTRONICS CO. LTD.
544A00	Cisco Systems, Inc
544A05	wenglor sensoric gmbh
544A16	Texas Instruments
544B8C	Juniper Networks
544E45	Private
544E90	Apple, Inc.
54511B	HUAWEI TECHNOLOGIES CO.,LTD
545146	AMG Systems Ltd.
5453ED	Sony Corporation
545414	Digital RF Corea, Inc
5454CF	PROBEDIGITAL CO.,LTD
545AA6	Espressif Inc.
545EBD	NL Technologies
545FA9	Teracom Limited
546009	Google, Inc.
546172	ZODIAC AEROSPACE SAS
5461EA	Zaplox AB
5464D9	Sagemcom Broadband SAS
5465DE	ARRIS Group, Inc.
546751	Compal Broadband Networks, Inc.
546C0E	Texas Instruments
546D52	TOPVIEW OPTRONICS CORP.
54724F	Apple, Inc.
547398	Toyo Electronics Corporation
5474E6	Webtech Wireless
5475D0	Cisco Systems, Inc
54781A	Cisco Systems, Inc
547975	Nokia Corporation
547C69	Cisco Systems, Inc
547F54	Ingenico
547FA8	TELCO systems, s.r.o.
547FEE	Cisco Systems, Inc
5481AD	Eagle Research Corporation
54847B	Digital Devices GmbH
54880E	SAMSUNG ELECTRO-MECHANICS(THAILAND)
548922	Zelfy Inc
548998	HUAWEI TECHNOLOGIES CO.,LTD
548CA0	Liteon Technology Corporation
5492BE	Samsung Electronics Co.,Ltd
549359	SHENZHEN TWOWING TECHNOLOGIES CO.,LTD.
549478	Silvershore Technology Partners
549A11	IEEE Registration Authority
549A16	Uzushio Electric Co.,Ltd.
549B12	Samsung Electronics Co.,Ltd
549D85	EnerAccess inc
549F13	Apple, Inc.
549F35	Dell Inc.
54A04F	t-mac Technologies Ltd
54A050	ASUSTek COMPUTER INC.
54A274	Cisco Systems, Inc
54A31B	Shenzhen Linkworld Technology Co,.LTD
54A3FA	BQT Solutions (Australia)Pty Ltd
54A51B	HUAWEI TECHNOLOGIES CO.,LTD
54A54B	NSC Communications Siberia Ltd
54A619	Alcatel-               # Alcatel-Lucent Shanghai Bell Co., Ltd
54A9D4	Minibar Systems
54AB3A	QUANTA COMPUTER INC.
54AE27	Apple, Inc.
54B56C	Xi'an NovaStar Tech Co., Ltd
54B620	SuhdolE&               # SUHDOL E&C Co.Ltd.
54B753	Hunan Fenghui Yinjia Science And Technology Co.,Ltd
54B80A	D-Link International
54BE53	zte corporation
54BEF7	PEGATRON CORPORATION
54C415	Hangzhou Hikvision Digital Technology Co.,Ltd.
54C80F	TP-LINK TECHNOLOGIES CO.,LTD.
54CD10	Panasonic Mobile Communications Co.,Ltd.
54CDA7	Fujian Shenzhou Electronic Co.,Ltd
54CDEE	ShenZhen Apexis Electronic Co.,Ltd
54D0B4	Xiamen Four-Faith Communication Technology Co.,Ltd
54D0ED	AXIM Communications
54D163	MAX-TECH,INC
54D1B0	Universal Laser Systems, Inc
54D272	Nuki Home Solutions GmbH
54D46F	Cisco SPVTG
54D9E4	BRILLIANTTS CO., LTD
54DC1D	Yulong Computer Telecommunication Scientific (Shenzhen) Co.,Ltd
54DF00	Ulterius Technologies, LLC
54DF63	Intrakey technologies GmbH
54E032	Juniper Networks
54E061	SICHUAN TIANYI COMHEART TELECOMCO., LTD
54E140	Ingenico
54E1AD	LCFC(HeFei) Electronics Technology co., ltd
54E2C8	Dongguan Aoyuan Electronics Technology Co., Ltd
54E2E0	ARRIS Group, Inc.
54E3B0	JVL Industri Elektronik
54E3F6	Alcatel-               # Alcatel-Lucent
54E43A	Apple, Inc.
54E4BD	FN-LINK TECHNOLOGY LIMITED
54E63F	ShenZhen LingKeWeiEr Technology Co., Ltd.
54E6FC	TP-LINK TECHNOLOGIES CO.,LTD.
54EAA8	Apple, Inc.
54EDA3	Navdy, Inc.
54EE75	Wistron InfoComm(Kunshan)Co.,Ltd.
54EF92	Shenzhen Elink Technology Co., LTD
54EFFE	Fullpower Technologies, Inc.
54F201	Samsung Electronics Co.,Ltd
54F5B6	ORIENTAL PACIFIC INTERNATIONAL LIMITED
54F666	Berthold Technologies GmbH and Co.KG
54F6C5	FUJIAN STAR-NET COMMUNICATION CO.,LTD
54F876	ABB AG
54FA3E	Samsung Electronics Co.,Ltd
54FA96	Nokia
54FB58	WISEWARE, Lda
54FDBF	Scheidt & Bachmann GmbH
54FF82	Davit Solution co.
54FFCF	Mopria Alliance
565857	Aculab plc			audio bridges
5800E3	Liteon Technology Corporation
5804CB	Tianjin Huisun Technology Co.,Ltd.
580528	LABRIS NETWORKS
580556	Elettronica GF S.r.L.
5808FA	Fiber Optic & telecommunication INC.
580943	Private
5809E5	Kivic Inc.
580A20	Cisco Systems, Inc
58108C	Intelbras
581243	AcSiP Technology Corp.
581626	Avaya Inc
58170C	Sony Mobile Communications AB
581CBD	Affinegy
581D91	Advanced Mobile Telecom co.,ltd.
581F28	HUAWEI TECHNOLOGIES CO.,LTD
581F67	Open-m technology limited
581FAA	Apple, Inc.
581FEF	Tuttnaer LTD
5820B1	Hewlett Packard
582136	KMB systems, s.r.o.
58238C	Technicolor CH USA Inc.
582AF7	HUAWEI TECHNOLOGIES CO.,LTD
582BDB	Pax AB
582EFE	Lighting Science Group
582F42	Universal Electric Corporation
583112	Drust
583277	Reliance Communications LLC
58343B	Glovast Technology Ltd.
5835D9	Cisco Systems, Inc
583CC6	Omneality Ltd.
583F54	LG Electronics (Mobile Communications)
58404E	Apple, Inc.
5842E4	Baxter International Inc
584498	Xiaomi Communications Co Ltd
58468F	Koncar Electronics and Informatics
5846E1	Baxter International Inc
584704	Shenzhen Webridge Technology Co.,Ltd
584822	Sony Mobile Communications AB
5848C0	Coflec
584925	E3 Enterprise
58493B	Palo Alto Networks
5849BA	Chitai Electronic Corp.
584C19	Chongqing Guohong Technology Development Company Limited
584CEE	Digital One Technologies, Limited
585076	Linear Equipamentos Eletronicos SA
5850AB	TLS Corporation
5850E6	Best Buy Corporation
58528A	Mitsubishi Electric Corporation
5853C0	Beijing Guang Runtong Technology Development Company co.,Ltd
5855CA	Apple, Inc.
5856E8	ARRIS Group, Inc.
58570D	Danfoss Solar Inverters
58605F	HUAWEI TECHNOLOGIES CO.,LTD
586356	FN-LINK TECHNOLOGY LIMITED
58639A	TPL SYSTEMES
5865E6	INFOMARK CO., LTD.
5866BA	Hangzhou H3C Technologies Co., Limited
58671A	Barnes&Noble
58677F	Clare Controls Inc.
58685D	Tempo Australia Pty Ltd
58696C	Ruijie Networks Co.,LTD
5869F9	Fusion Transactive Ltd.
586AB1	Hangzhou H3C Technologies Co., Limited
586D8F	Cisco-Linksys, LLC
586ED6	Private
5870C6	Shanghai Xiaoyi Technology Co., Ltd.
587521	CJSC RTSoft
587675	Beijing ECHO Technologies Co.,Ltd
5876C5	DIGI I'S LTD
587A4D	Stonesoft Corporation
587BE9	AirPro Technology India Pvt. Ltd
587E61	Qingdao Hisense Communications Co.,Ltd.
587F57	Apple, Inc.
587F66	HUAWEI TECHNOLOGIES CO.,LTD
587FB7	SONAR INDUSTRIAL CO., LTD.
587FC8	S2m
58821D	H. Schomäcker GmbH
5882A8	Microsoft
5884E4	IP500 Alliance e.V.
58856E	QSC AG
58874C	LITE-ON CLEAN ENERGY TECHNOLOGY CORP.
5887E2	Shenzhen Coship Electronics Co., Ltd.
588BF3	ZyXEL Communications Corporation
588D09	Cisco Systems, Inc
5891CF	Intel Corporate
58920D	Kinetic Avionics Limited
589396	Ruckus Wireless
58946B	Intel Corporate
5894CF	Vertex Standard LMR, Inc.
58971E	Cisco Systems, Inc
5897BD	Cisco Systems, Inc
589835	Technicolor
58986F	Revolution Display
589B0B	Shineway Technologies, Inc.
589CFC	FreeBSD Foundation
58A2B5	LG Electronics (Mobile Communications)
58A76F	iD corporation
58A839	Intel Corporate
58AC78	Cisco Systems, Inc
58B035	Apple, Inc.
58B0D4	ZuniData Systems Inc.
58B633	Ruckus Wireless
58B961	SOLEM Electronique
58B9E1	Crystalfontz America, Inc.
58BC27	Cisco Systems, Inc
58BC8F	Cognitive Systems Corp.
58BDA3	Nintendo Co., Ltd.
58BDF9	Sigrand
58BFEA	Cisco Systems, Inc
58C232	NEC Corporation
58C38B	Samsung Electronics Co.,Ltd
58CF4B	Lufkin Industries
58D071	BW Broadcast
58D08F	IEEE 1904.1 Working Group
58D67A	Tcplink
58D6D3	Dairy Cheq Inc
58D9D5	Tenda Technology Co.,Ltd.Dongguan branch
58DB8D	Fast Co., Ltd.
58DC6D	Exceptional Innovation, Inc.
58E02C	Micro Technic A/S
58E16C	Ying Hua Information Technology (Shanghai)Co., LTD
58E326	Compass Technologies Inc.
58E476	CENTRON COMMUNICATIONS TECHNOLOGIES FUJIAN CO.,LTD
58E636	EVRsafe Technologies
58E747	Deltanet AG
58E808	AUTONICS CORPORATION
58E876	IEEE Registration Authority
58EB14	Proteus Digital Health
58ECE1	Newport Corporation
58EECE	Icon Time Systems
58EF68	Belkin International Inc.
58F102	BLU Products Inc.
58F387	Hccp
58F39C	Cisco Systems, Inc
58F496	Source Chain
58F67B	Xia Men UnionCore Technology LTD.
58F6BF	Kyoto University
58F98E	SECUDOS GmbH
58FB84	Intel Corporate
58FC73	Arria Live Media, Inc.
58FCDB	IEEE Registration Authority
58FD20	Bravida Sakerhet AB
5C026A	Applied Vision Corporation
5C076F	Thought Creator
5C0A5B	SAMSUNG ELECTRO MECHANICS CO., LTD.
5C0CBB	CELIZION Inc.
5C0E8B	Extreme Networks
5C1193	Seal One AG
5C1437	Thyssenkrupp Aufzugswerke GmbH
5C1515	Advan
5C15E1	AIDC TECHNOLOGY (S) PTE LTD
5C16C7	Big Switch Networks
5C1737	I-View Now, LLC.
5C17D3	Lge
5C18B5	Talon Communications
5C20D0	Asoni Communication Co., Ltd.
5C22C4	DAE EUN ELETRONICS CO., LTD
5C2443	O-Sung Telecom Co., Ltd.
5C2479	Baltech AG
5C254C	Avire Global Pte Ltd
5C260A	Dell Inc.
5C2AEF	Open Access Pty Ltd
5C2BF5	Vivint
5C2E59	Samsung Electronics Co.,Ltd
5C2ED2	ABC(XiSheng) Electronics Co.,Ltd
5C313E	Texas Instruments
5C3327	Spazio Italia srl
5C335C	Swissphone Telecom AG
5C338E	Alpha Networks Inc.
5C353B	Compal Broadband Networks, Inc.
5C35DA	There Corporation Oy
5C36B8	TCL King Electrical Appliances (Huizhou) Co., Ltd
5C38E0	Shanghai Super Electronics Technology Co.,LTD
5C3B35	Gehirn Inc.
5C3C27	Samsung Electronics Co.,Ltd
5C4058	Jefferson Audio Video Systems, Inc.
5C41E7	Wiatec International Ltd.
5C43D2	HAZEMEYER
5C4527	Juniper Networks
5C4979	AVM Audiovisuelles Marketing und Computersysteme GmbH
5C497D	Samsung Electronics Co.,Ltd
5C4A1F	SICHUAN TIANYI COMHEART TELECOMCO., LTD
5C4A26	Enguity Technology Corp
5C4CA9	HUAWEI TECHNOLOGIES CO.,LTD
5C5015	Cisco Systems, Inc
5C514F	Intel Corporate
5C5188	Motorola Mobility LLC, a Lenovo Company
5C56ED	3pleplay Electronics Private Limited
5C571A	ARRIS Group, Inc.
5C57C8	Nokia Corporation
5C5948	Apple, Inc.
5C5B35	Mist Systems, Inc.
5C5BC2	YIK Corporation
5C5EAB	Juniper Networks
5C63BF	TP-LINK TECHNOLOGIES CO.,LTD.
5C6984	Nuvico
5C6A7D	KENTKART EGE ELEKTRONIK SAN. VE TIC. LTD. STI.
5C6A80	ZyXEL Communications Corporation
5C6B32	Texas Instruments
5C6B4F	Hello Inc.
5C6D20	Hon Hai Precision Ind. Co.,Ltd.
5C6F4F	S.A. SISTEL
5C70A3	LG Electronics (Mobile Communications)
5C7757	Haivision Network Video
5C7D5E	HUAWEI TECHNOLOGIES CO.,LTD
5C838F	Cisco Systems, Inc
5C8486	Brightsource Industries Israel LTD
5C8613	Beijing Zhoenet Technology Co., Ltd
5C864A	Secret Labs LLC
5C8778	Cybertelbridge co.,ltd
5C899A	TP-LINK TECHNOLOGIES CO.,LTD.
5C89D4	Beijing Banner Electric Co.,Ltd
5C8A38	Hewlett Packard
5C8D4E	Apple, Inc.
5C8FE0	ARRIS Group, Inc.
5C93A2	Liteon Technology Corporation
5C95AE	Apple, Inc.
5C9656	AzureWave Technology Inc.
5C966A	Rtnet
5C969D	Apple, Inc.
5C97F3	Apple, Inc.
5C9960	Samsung Electronics Co.,Ltd
5C9AD8	FUJITSU LIMITED
5CA178	TableTop Media (dba Ziosk)
5CA39D	SAMSUNG ELECTRO MECHANICS CO., LTD.
5CA3EB	Lokel s.r.o.
5CA48A	Cisco Systems, Inc
5CA86A	HUAWEI TECHNOLOGIES CO.,LTD
5CA933	Luma Home
5CAAFD	Sonos, Inc.
5CAC4C	Hon Hai Precision Ind. Co.,Ltd.
5CADCF	Apple, Inc.
5CAF06	LG Electronics (Mobile Communications)
5CB066	ARRIS Group, Inc.
5CB395	HUAWEI TECHNOLOGIES CO.,LTD
5CB43E	HUAWEI TECHNOLOGIES CO.,LTD
5CB524	Sony Mobile Communications AB
5CB559	CNEX Labs
5CB6CC	NovaComm Technologies Inc.
5CB8CB	Allis Communications
5CB901	Hewlett Packard
5CBA37	Microsoft Corporation
5CBD9E	HONGKONG MIRACLE EAGLE TECHNOLOGY(GROUP) LIMITED
5CC213	Fr. Sauter AG
5CC5D4	Intel Corporate
5CC6D0	Skyworth Digital Technology(Shenzhen) Co.,Ltd
5CC6E9	Edifier International
5CC7D7	AZROAD TECHNOLOGY COMPANY LIMITED
5CC9D3	PALLADIUM ENERGY ELETRONICA DA AMAZONIA LTDA
5CCA1A	Microsoft Mobile Oy
5CCA32	Theben AG
5CCCA0	Gridwiz Inc.
5CCCFF	Techroutes Network Pvt Ltd
5CCEAD	CDYNE Corporation
5CCF7F	Espressif Inc.
5CD135	Xtreme Power Systems
5CD2E4	Intel Corporate
5CD41B	UCZOON Technology Co., LTD
5CD4AB	Zektor
5CD61F	Qardio, Inc
5CD998	D-Link Corporation
5CDAD4	Murata Manufacturing Co., Ltd.
5CDC96	Arcadyan Technology Corporation
5CDD70	Hangzhou H3C Technologies Co., Limited
5CE0C5	Intel Corporate
5CE0CA	FeiTian United (Beijing) System Technology Co., Ltd.
5CE0F6	NIC.br- Nucleo de Informacao e Coordenacao do Ponto BR
5CE223	Delphin Technology AG
5CE286	Nortel Networks
5CE2F4	AcSiP Technology Corp.
5CE30E	ARRIS Group, Inc.
5CE3B6	Fiberhome Telecommunication Technologies Co.,LTD
5CE7BF	New Singularity International Technical Development Co.,Ltd
5CE8EB	Samsung Electronics Co.,Ltd
5CEB4E	R. STAHL HMI Systems GmbH
5CEB68	Cheerstar Technology Co., Ltd
5CEE79	Global Digitech Co LTD
5CF207	Speco Technologies
5CF286	IEEE Registration Authority
5CF370	CC&C Technologies, Inc
5CF3FC	IBM Corp
5CF4AB	ZyXEL Communications Corporation
5CF50D	Institute of microelectronic applications
5CF5DA	Apple, Inc.
5CF6DC	Samsung Electronics Co.,Ltd
5CF7C3	SYNTECH (HK) TECHNOLOGY LIMITED
5CF7E6	Apple, Inc.
5CF821	Texas Instruments
5CF8A1	Murata Manufacturing Co., Ltd.
5CF938	Apple, Inc.
5CF96A	HUAWEI TECHNOLOGIES CO.,LTD
5CF9DD	Dell Inc.
5CF9F0	Atomos Engineering P/L
5CFC66	Cisco Systems, Inc
5CFF35	Wistron Corporation
5CFFFF	Shenzhen Kezhonglong Optoelectronic Technology Co., Ltd
600194	Espressif Inc.
600292	PEGATRON CORPORATION
6002B4	Wistron Neweb Corporation
600308	Apple, Inc.
600347	Billion Electric Co. Ltd.
600417	POSBANK CO.,LTD
600810	HUAWEI TECHNOLOGIES CO.,LTD
600837	ivvi Scientific(Nanchang)Co.Ltd
600B03	Hangzhou H3C Technologies Co., Limited
600F77	SilverPlus, Inc
601199	Siama Systems Inc
601283	Soluciones Tecnologicas para la Salud y el Bienestar SA
60128B	CANON INC.
601466	zte corporation
6014B3	CyberTAN Technology Inc.
6015C7	Idatech
60182E	ShenZhen Protruly Electronic Ltd co.
601888	zte corporation
60190C	Rramac
601929	VOLTRONIC POWER TECHNOLOGY(SHENZHEN) CORP.
601970	HUIZHOU QIAOXING ELECTRONICS TECHNOLOGY CO., LTD.
601971	ARRIS Group, Inc.
601D0F	Midnite Solar
601E02	EltexAlatau
602103	I4VINE, INC
6021C0	Murata Manufacturing Co., Ltd.
6024C1	Jiangsu Zhongxun Electronic Technology Co., Ltd
602A54	CardioTek B.V.
602AD0	Cisco SPVTG
603197	ZyXEL Communications Corporation
6032F0	Mplus technology
60334B	Apple, Inc.
603553	Buwon Technology
603696	The Sapling Company
6036DD	Intel Corporate
60380E	ALPS ELECTRIC CO.,LTD.
6038E0	Belkin International Inc.
60391F	ABB Ltd
603E7B	Gafachi, Inc.
603ECA	Cambridge Medical Robotics Ltd
603FC5	COX CO., LTD
60427F	SHENZHEN CHUANGWEI-RGB ELECTRONICS CO.,LTD
6044F5	Easy Digital Ltd.
60455E	Liptel s.r.o.
6045BD	Microsoft
6045CB	ASUSTek COMPUTER INC.
604616	XIAMEN VANN INTELLIGENT CO., LTD
6047D4	FORICS Electronic Technology Co., Ltd.
604826	Newbridge Technologies Int. Ltd.
6049C1	Avaya Inc
604A1C	SUYIN Corporation
604BAA	Private
6050C1	Kinetek Sports
60512C	TCT mobile ltd
6052D0	FACTS Engineering
605317	Sandstone Technologies
605464	Eyedro Green Solutions Inc.
605718	Intel Corporate
605BB4	AzureWave Technology Inc.
60601F	SZ DJI TECHNOLOGY CO.,LTD
6063F9	Ciholas, Inc.
6063FD	Transcend Communication Beijing Co.,Ltd.
606405	Texas Instruments
606453	AOD Co.,Ltd.
6064A1	RADiflow Ltd.
606720	Intel Corporate
606944	Apple, Inc.
60699B	isepos GmbH
606BBD	Samsung Electronics Co.,Ltd
606C66	Intel Corporate
606DC7	Hon Hai Precision Ind. Co.,Ltd.
60735C	Cisco Systems, Inc
6073BC	zte corporation
60748D	Atmaca Elektronik
607688	Velodyne
6077E2	Samsung Electronics Co.,Ltd
607EDD	Microsoft Mobile Oy
60812B	Custom Control Concepts
6081F9	Helium Systems, Inc
608334	HUAWEI TECHNOLOGIES CO.,LTD
6083B2	GkWare e.K.
60843B	Soladigm, Inc.
608645	Avery Weigh-Tronix, LLC
60893C	Thermo Fisher Scientific P.O.A.
6089B1	Key Digital Systems
6089B7	KAEL MÜHENDİSLİK ELEKTRONİK TİCARET SANAYİ LİMİTED ŞİRKETİ
608C2B	Hanson Technology
608D17	Sentrus Government Systems Division, Inc
608F5C	Samsung Electronics Co.,Ltd
609084	DSSD Inc
6091F3	vivo Mobile Communication Co., Ltd.
609217	Apple, Inc.
609620	Private
6099D1	Vuzix / Lenovo
609AA4	GVI SECURITY INC.
609AC1	Apple, Inc.
609C9F	Brocade Communications Systems, Inc.
609E64	Vivonic GmbH
609F9D	CloudSwitch
60A10A	Samsung Electronics Co.,Ltd
60A37D	Apple, Inc.
60A44C	ASUSTek COMPUTER INC.
60A4D0	Samsung Electronics Co.,Ltd
60A8FE	Nokia
60A9B0	Merchandising Technologies, Inc
60ACC8	KunTeng Inc.
60AF6D	Samsung Electronics Co.,Ltd
60B185	ATH system
60B387	Synergics Technologies GmbH
60B3C4	Elber Srl
60B4F7	Plume Design Inc
60B606	Phorus
60B617	Fiberhome Telecommunication Technologies Co.,LTD
60B933	Deutron Electronics Corp.
60B982	RO.VE.R. Laboratories S.p.A.
60BA18	nextLAP GmbH
60BB0C	Beijing HuaqinWorld Technology Co,Ltd
60BC4C	EWM Hightec Welding GmbH
60BD91	Move Innovation
60BEB5	Motorola Mobility LLC, a Lenovo Company
60C0BF	ON Semiconductor
60C1CB	Fujian Great Power PLC Equipment Co.,Ltd
60C397	2Wire Inc
60C547	Apple, Inc.
60C5A8	Beijing LT Honway Technology Co.,Ltd
60C5AD	Samsung Electronics Co.,Ltd
60C658	PHYTRONIX Co.,Ltd.
60C798	Verifone
60C980	Trymus
60CBFB	AirScape Inc.
60CDA9	Abloomy
60CDC5	Taiwan Carol Electronics., Ltd
60D0A9	Samsung Electronics Co.,Ltd
60D1AA	Vishal Telecommunications Pvt Ltd
60D262	Tzukuri Pty Ltd
60D2B9	REALAND BIO CO., LTD.
60D30A	Quatius Limited
60D7E3	IEEE Registration Authority
60D819	Hon Hai Precision Ind. Co.,Ltd.
60D9A0	Lenovo Mobile Communication Technology Ltd.
60D9C7	Apple, Inc.
60DA23	Estech Co.,Ltd
60DB2A	Hns
60DE44	HUAWEI TECHNOLOGIES CO.,LTD
60E00E	SHINSEI ELECTRONICS CO LTD
60E327	TP-LINK TECHNOLOGIES CO.,LTD.
60E3AC	LG Electronics (Mobile Communications)
60E6BC	Sino-Telecom Technology Co.,Ltd.
60E701	HUAWEI TECHNOLOGIES CO.,LTD
60E78A	Unisem
60E956	Ayla Networks, Inc
60EB69	QUANTA COMPUTER INC.
60EE5C	SHENZHEN FAST TECHNOLOGIES CO.,LTD
60EFC6	Shenzhen Chima Technologies Co Limited
60F13D	JABLOCOM s.r.o.
60F189	Murata Manufacturing Co., Ltd.
60F281	TRANWO TECHNOLOGY CO., LTD.
60F2EF	VisionVera International Co., Ltd.
60F3DA	Logic Way GmbH
60F445	Apple, Inc.
60F494	Hon Hai Precision Ind. Co.,Ltd.
60F59C	CRU-Dataport
60F673	TERUMO CORPORATION
60F81D	Apple, Inc.
60FACD	Apple, Inc.
60FB42	Apple, Inc.
60FD56	WOORISYSTEMS CO., Ltd
60FE1E	China Palms Telecom.Ltd
60FE20	2Wire Inc
60FEC5	Apple, Inc.
60FEF9	Thomas & Betts
60FFDD	C.E. ELECTRONICS, INC
64002D	Powerlinq Co., LTD
64006A	Dell Inc.
6400F1	Cisco Systems, Inc
6405BE	NEW LIGHT LED
64094C	Beijing Superbee Wireless Technology Co.,Ltd
640980	Xiaomi Communications Co Ltd
640B4A	Digital Telecom Technology Limited
640DCE	SHENZHEN MERCURY COMMUNICATION TECHNOLOGIES CO.,LTD.
640DE6	Petra Systems
640E36	Taztag
640E94	Pluribus Networks, Inc.
640F28	2Wire Inc
641084	HEXIUM Technical Development Co., Ltd.
641225	Cisco Systems, Inc
641269	ARRIS Group, Inc.
64136C	zte corporation
64167F	Polycom
64168D	Cisco Systems, Inc
6416F0	HUAWEI TECHNOLOGIES CO.,LTD
641A22	Heliospectra AB
641C67	DIGIBRAS INDUSTRIA DO BRASILS/A
641E81	Dowslake Microsystems
64200C	Apple, Inc.
642184	Nippon Denki Kagaku Co.,LTD
642216	Shandong Taixin Electronic co.,Ltd
642400	Xorcom Ltd.
642737	Hon Hai Precision Ind. Co.,Ltd.
642DB7	SEUNGIL ELECTRONICS
643150	Hewlett Packard
64317E	Dexin Corporation
643409	BITwave Pte Ltd
64351C	e-CON SYSTEMS INDIA PVT LTD
643AB1	SICHUAN TIANYI COMHEART TELECOMCO.,LTD
643E8C	HUAWEI TECHNOLOGIES CO.,LTD
643F5F	Exablaze
644214	Swisscom Energy Solutions AG
644346	GuangDong Quick Network Computer CO.,LTD
644BC3	Shanghai WOASiS Telecommunications Ltd., Co.
644BF0	CalDigit, Inc
644D70	dSPACE GmbH
644F74	LENUS Co., Ltd.
644FB0	Hyunjin.com
645106	Hewlett Packard
64517E	LONG BEN (DONGGUAN) ELECTRONIC TECHNOLOGY CO.,LTD.
645299	The Chamberlain Group, Inc
64535D	Frauscher Sensortechnik
645422	Equinox Payments
645563	Intelight Inc.
64557F	NSFOCUS Information Technology Co., Ltd.
6455B1	ARRIS Group, Inc.
645601	TP-LINK TECHNOLOGIES CO.,LTD.
6459F8	Vodafone Omnitel B.V.
645A04	Chicony Electronics Co., Ltd.
645D92	SICHUAN TIANYI COMHEART TELECOMCO.,LTD
645DD7	Shenzhen Lifesense Medical Electronics Co., Ltd.
645EBE	Yahoo! JAPAN
645FFF	Nicolet Neuro
646184	Velux
646223	Cellient Co., Ltd.
64649B	Juniper Networks
6465C0	Nuvon, Inc
6466B3	TP-LINK TECHNOLOGIES CO.,LTD.
646707	Beijing Omnific Technology, Ltd.
64680C	Comtrend Corporation
6469BC	Hytera Communications Co .,ltd
646A52	Avaya Inc
646A74	AUTH-SERVERS, LLC
646CB2	Samsung Electronics Co.,Ltd
646E6C	Radio Datacom LLC
646EEA	Iskratel d.o.o.
647002	TP-LINK TECHNOLOGIES CO.,LTD.
6472D8	GooWi Technology Co.,Limited
6473E2	Arbiter Systems, Inc.
6474F6	Shooter Detection Systems
647657	Innovative Security Designs
6476BA	Apple, Inc.
64777D	Hitron Technologies. Inc
647791	Samsung Electronics Co.,Ltd
6479A7	Phison Electronics Corp.
647BD4	Texas Instruments
647C34	Ubee Interactive Corp.
647D81	YOKOTA INDUSTRIAL CO,.LTD
647FDA	TEKTELIC Communications Inc.
64808B	VG Controls, Inc.
648099	Intel Corporate
648125	Alphatron Marine BV
648788	Juniper Networks
6487D7	ADB Broadband Italia
6488FF	Sichuan Changhong Electric Ltd.
64899A	LG Electronics (Mobile Communications)
648D9E	IVT Electronic Co.,Ltd
64995D	Lge
649968	Elentec
6499A0	AG Elektronik AB
649A12	P2 Mobile Technologies Limited
649ABE	Apple, Inc.
649B24	V Technology Co., Ltd.
649C81	Qualcomm Inc.
649C8E	Texas Instruments
649EF3	Cisco Systems, Inc
649FF7	Kone OYj
64A0E7	Cisco Systems, Inc
64A232	OOO Samlight
64A341	Wonderlan (Beijing) Technology Co., Ltd.
64A3CB	Apple, Inc.
64A5C3	Apple, Inc.
64A651	HUAWEI TECHNOLOGIES CO.,LTD
64A68F	Zhongshan Readboy Electronics Co.,Ltd
64A769	HTC Corporation
64A7DD	Avaya Inc
64A837	Juni Korea Co., Ltd
64AE0C	Cisco Systems, Inc
64AE88	Polytec GmbH
64B0A6	Apple, Inc.
64B21D	Chengdu Phycom Tech Co., Ltd.
64B310	Samsung Electronics Co.,Ltd
64B370	PowerComm Solutions LLC
64B473	Xiaomi Communications Co Ltd
64B64A	ViVOtech, Inc.
64B853	Samsung Electronics Co.,Ltd
64B9E8	Apple, Inc.
64BABD	SDJ Technologies, Inc.
64BC0C	LG Electronics (Mobile Communications)
64BC11	CombiQ AB
64C354	Avaya Inc
64C5AA	South African Broadcasting Corporation
64C667	Barnes&Noble
64C6AF	AXERRA Networks Ltd
64C944	LARK Technologies, Inc
64CC2E	Xiaomi Communications Co Ltd
64D02D	Next Generation Integration (NGI)
64D154	Routerboard.com
64D1A3	Sitecom Europe BV
64D241	Keith & Koep GmbH
64D4BD	ALPS ELECTRIC CO.,LTD.
64D4DA	Intel Corporate
64D814	Cisco Systems, Inc
64D912	Solidica, Inc.
64D954	Taicang T&W Electronics
64D989	Cisco Systems, Inc
64DAA0	Robert Bosch Smart Home GmbH
64DB18	OpenPattern
64DB43	Motorola (Wuhan) Mobility Technologies Communication Co., Ltd.
64DB81	Syszone Co., Ltd.
64DBA0	Select Comfort
64DC01	Static Systems Group PLC
64DE1C	Kingnetic Pte Ltd
64E161	DEP Corp.
64E599	EFM Networks
64E625	Woxu Wireless Co., Ltd
64E682	Apple, Inc.
64E84F	Serialway Communication Technology Co. Ltd
64E892	Morio Denki Co., Ltd.
64E8E6	global moisture management system
64E950	Cisco Systems, Inc
64EAC5	SiboTech Automation Co., Ltd.
64EB8C	Seiko Epson Corporation
64ED57	ARRIS Group, Inc.
64ED62	WOORI SYSTEMS Co., Ltd
64F242	Gerdes Aktiengesellschaft
64F50E	Kinion Technology Company Limited
64F69D	Cisco Systems, Inc
64F970	Kenade Electronics Technology Co.,LTD.
64F987	Avvasi Inc.
64FB81	IEEE Registration Authority
64FC8C	Zonar Systems
680235	Konten Networks Inc.
680571	Samsung Electronics Co.,Ltd
6805CA	Intel Corporate
680715	Intel Corporate
680927	Apple, Inc.
680AD7	Yancheng Kecheng Optoelectronic Technology Co., Ltd
68122D	Special Instrument Development Co., Ltd.
681295	Lupine Lighting Systems GmbH
681401	Hon Hai Precision Ind. Co.,Ltd.
681590	Sagemcom Broadband SAS
6815D3	Zaklady Elektroniki i Mechaniki Precyzyjnej R&G S.A.
681605	Systems And Electronic Development FZCO
681729	Intel Corporate
68193F	Digital Airways
681AB2	zte corporation
681CA2	Rosewill Inc.
681D64	Sunwave Communications Co., Ltd
681E8B	InfoSight Corporation
681FD8	Siemens Industry, Inc.
68234B	Nihon Dengyo Kousaku
68262A	SICHUAN TIANYI COMHEART TELECOMCO., LTD
682737	Samsung Electronics Co.,Ltd
6828BA	Dejai
6828F6	Vubiq Networks, Inc.
682DDC	Wuhan Changjiang Electro-Communication Equipment CO.,LTD
6831FE	Teladin Co.,Ltd.
683563	SHENZHEN LIOWN ELECTRONICS CO.,LTD.
6836B5	DriveScale, Inc.
6837E9	Amazon Technologies Inc.
683B1E	Countwise LTD
683C7D	Magic Intelligence Technology Limited
683E34	MEIZU Technology Co., Ltd.
683EEC	Ereca
684352	Bhuu Limited
684898	Samsung Electronics Co.,Ltd
684B88	Galtronics Telemetry Inc.
684CA8	Shenzhen Herotel Tech. Co., Ltd.
6851B7	PowerCloud Systems, Inc.
68536C	SPnS Co.,Ltd
685388	P&S Technology
6854C1	ColorTokens, Inc.
6854ED	Alcatel-               # Alcatel-Lucent
6854F5	enLighted Inc
6854FD	Amazon Technologies Inc.
6858C5	ZF TRW Automotive
68597F	Alcatel Lucent
685B35	Apple, Inc.
685B36	POWERTECH INDUSTRIAL CO., LTD.
685D43	Intel Corporate
685E6B	PowerRay Co., Ltd.
686359	Advanced Digital Broadcast SA
68644B	Apple, Inc.
68692E	Zycoo Co.,Ltd
686975	Angler Labs Inc
6869F2	ComAp s.r.o.
686E23	Wi3 Inc.
686E48	Prophet Electronic Technology Corp.,Ltd
687251	Ubiquiti Networks Inc.
6872DC	CETORY.TV Company Limited
68764F	Sony Mobile Communications AB
687848	Westunitis Co., Ltd.
68784C	Nortel Networks
687924	ELS-GmbH & Co. KG
6879ED	SHARP Corporation
687CC8	Measurement Systems S. de R.L.
687CD5	Y Soft Corporation, a.s.
687F74	Cisco-Linksys, LLC
68831A	Pandora Mobility Corporation
688470	eSSys Co.,Ltd
688540	IGI Mobile, Inc.
68856A	OuterLink Corporation
6886A7	Cisco Systems, Inc
6886E7	Orbotix, Inc.
68876B	INQ Mobile Limited
6889C1	HUAWEI TECHNOLOGIES CO.,LTD
688AB5	EDP Servicos
688AF0	zte corporation
688DB6	AETEK INC.
688F84	HUAWEI TECHNOLOGIES CO.,LTD
6891D0	IEEE Registration Authority
689234	Ruckus Wireless
689361	Integrated Device Technology (Malaysia) Sdn. Bhd.
689423	Hon Hai Precision Ind. Co.,Ltd.
68967B	Apple, Inc.
68974B	Shenzhen Costar Electronics Co. Ltd.
6897E8	Society of Motion Picture &amp; Television Engineers
6899CD	Cisco Systems, Inc
689AB7	Atelier Vision Corporation
689C5E	AcSiP Technology Corp.
689C70	Apple, Inc.
689CE2	Cisco Systems, Inc
689E19	Texas Instruments
689FF0	zte corporation
68A0F6	HUAWEI TECHNOLOGIES CO.,LTD
68A1B7	Honghao Mingchuan Technology (Beijing) CO.,Ltd.
68A378	FREEBOX SAS
68A3C4	Liteon Technology Corporation
68A40E	BSH Hausgeräte GmbH
68A828	HUAWEI TECHNOLOGIES CO.,LTD
68A86D	Apple, Inc.
68AAD2	DATECS LTD.,
68AB8A	RF IDeas
68AE20	Apple, Inc.
68AF13	Futura Mobility
68B094	INESA ELECTRON CO.,LTD
68B35E	Shenzhen Neostra Technology Co.Ltd
68B43A	WaterFurnace International, Inc.
68B599	Hewlett Packard
68B6FC	Hitron Technologies. Inc
68B8D9	Act KDE, Inc.
68B983	b-plus GmbH
68BC0C	Cisco Systems, Inc
68BDAB	Cisco Systems, Inc
68C44D	Motorola Mobility LLC, a Lenovo Company
68C90B	Texas Instruments
68CA00	Octopus Systems Limited
68CC6E	HUAWEI TECHNOLOGIES CO.,LTD
68CC9C	Mine Site Technologies
68CD0F	U Tek Company Limited
68CE4E	L-3 Communications Infrared Products
68D1FD	Shenzhen Trimax Technology Co.,Ltd
68D247	Portalis LC
68D925	ProSys Development Services
68D93C	Apple, Inc.
68DB67	Nantong Coship Electronics Co., Ltd
68DB96	OPWILL Technologies CO .,LTD
68DBCA	Apple, Inc.
68DCE8	PacketStorm Communications
68DFDD	Xiaomi Communications Co Ltd
68E166	Private
68E41F	Unglaube Identech GmbH
68E8EB	Linktel Technologies Co.,Ltd
68EBAE	Samsung Electronics Co.,Ltd
68EBC5	Angstrem Telecom
68EC62	YODO Technology Corp. Ltd.
68ED43	BlackBerry RTS
68EDA4	Shenzhen Seavo Technology Co.,Ltd
68EE96	Cisco SPVTG
68EFBD	Cisco Systems, Inc
68F06D	ALONG INDUSTRIAL CO., LIMITED
68F0BC	Shenzhen LiWiFi Technology Co., Ltd
68F125	Data Controls Inc.
68F728	LCFC(HeFei) Electronics Technology co., ltd
68F895	Redflow Limited
68F956	Objetivos y Servicio de Valor Añadido
68FB7E	Apple, Inc.
68FB95	Generalplus Technology Inc.
68FCB3	Next Level Security Systems, Inc.
6C0273	Shenzhen Jin Yun Video Equipment Co., Ltd.
6C0460	RBH Access Technologies Inc.
6C09D6	Digiquest Electronics LTD
6C0B84	Universal Global Scientific Industrial Co., Ltd.
6C0E0D	Sony Mobile Communications AB
6C0EE6	Chengdu Xiyida Electronic Technology Co,.Ltd
6C0F6A	JDC Tech Co., Ltd.
6C14F7	Erhardt+               # Erhardt+Leimer GmbH
6C15F9	Nautronix Limited
6C160E	ShotTracker
6C1811	Decatur Electronics
6C198F	D-Link International
6C19C0	Apple, Inc.
6C1E70	Guangzhou YBDS IT Co.,Ltd
6C1E90	Hansol Technics Co., Ltd.
6C2056	Cisco Systems, Inc
6C22AB	Ainsworth Game Technology
6C23B9	Sony Mobile Communications AB
6C2483	Microsoft Mobile Oy
6C25B9	BBK EDUCATIONAL ELECTRONICS CORP.,LTD.
6C2779	Microsoft Mobile Oy
6C2995	Intel Corporate
6C2C06	OOO NPP Systemotechnika-NN
6C2E33	Accelink Technologies Co.,Ltd.
6C2E72	B&B EXPORTING LIMITED
6C2E85	Sagemcom Broadband SAS
6C2F2C	Samsung Electronics Co.,Ltd
6C32DE	Indieon Technologies Pvt. Ltd.
6C33A9	Magicjack LP
6C38A1	Ubee Interactive Corp.
6C391D	Beijing ZhongHuaHun Network Information center
6C3A84	Shenzhen Aero-Startech. Co.Ltd
6C3B6B	Routerboard.com
6C3BE5	Hewlett Packard
6C3C53	SoundHawk Corp
6C3E6D	Apple, Inc.
6C3E9C	KE Knestel Elektronik GmbH
6C4008	Apple, Inc.
6C40C6	Nimbus Data Systems, Inc.
6C416A	Cisco Systems, Inc
6C4418	Zappware
6C4598	Antex Electronic Corp.
6C4A39	Bita
6C4B7F	Vossloh-               # Vossloh-Schwabe Deutschland GmbH
6C4B90	Liteon
6C504D	Cisco Systems, Inc
6C5779	Aclima, Inc.
6C5940	SHENZHEN MERCURY COMMUNICATION TECHNOLOGIES CO.,LTD.
6C5976	Shanghai Tricheer Technology Co.,Ltd.
6C5A34	Shenzhen Haitianxiong Electronic Co., Ltd.
6C5AB5	TCL Technoly Electronics (Huizhou) Co., Ltd.
6C5C14	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
6C5CDE	SunReports, Inc.
6C5D63	ShenZhen Rapoo Technology Co., Ltd.
6C5E7A	Ubiquitous Internet Telecom Co., Ltd
6C5F1C	Lenovo Mobile Communication Technology Ltd.
6C6126	Rinicom Holdings
6C626D	Micro-Star INT'L CO., LTD
6C641A	Penguin Computing
6C6EFE	Core Logic Inc.
6C6F18	Stereotaxis, Inc.
6C7039	Novar GmbH
6C709F	Apple, Inc.
6C71BD	EZELINK TELECOM
6C71D9	AzureWave Technology Inc.
6C7220	D-Link International
6C72E7	Apple, Inc.
6C750D	Wifisong
6C7660	KYOCERA Corporation
6C81FE	Mitsuba Corporation
6C8336	Samsung Electronics Co.,Ltd
6C8366	Nanjing SAC Power Grid Automation Co., Ltd.
6C8686	Technonia
6C8814	Intel Corporate
6C8B2F	zte corporation
6C8CDB	Otus Technologies Ltd
6C8D65	Wireless Glue Networks, Inc.
6C8DC1	Apple, Inc.
6C8FB5	Microsoft Mobile Oy
6C90B1	SanLogic Inc
6C92BF	Inspur Electronic Information Industry Co.,Ltd.
6C9354	Yaojin Technology (Shenzhen) Co., LTD.
6C94F8	Apple, Inc.
6C9522	Scalys
6C98EB	Riverbed Technology, Inc.
6C9989	Cisco Systems, Inc
6C9AC9	Valentine Research, Inc.
6C9B02	Nokia Corporation
6C9CE9	Nimble Storage
6C9CED	Cisco Systems, Inc
6CA100	Intel Corporate
6CA682	EDAM information & communications
6CA75F	zte corporation
6CA780	Nokia Corporation
6CA7FA	YOUNGBO ENGINEERING INC.
6CA849	Avaya Inc
6CA858	Fiberhome Telecommunication Technologies Co.,LTD
6CA906	Telefield Ltd
6CA96F	TransPacket AS
6CAAB3	Ruckus Wireless
6CAB31	Apple, Inc.
6CAB4D	Digital Payment Technologies
6CAC60	Venetex Corp
6CAD3F	Hubbell Building Automation, Inc.
6CADEF	KZ Broadband Technologies, Ltd.
6CADF8	AzureWave Technology Inc.
6CAE8B	IBM Corporation
6CB0CE	Netgear
6CB311	Shenzhen Lianrui Electronics Co.,Ltd
6CB350	Anhui comhigher tech co.,ltd
6CB4A7	Landauer, Inc.
6CB56B	HUMAX Co., Ltd.
6CB7F4	Samsung Electronics Co.,Ltd
6CB9C5	Delta Networks, Inc.
6CBEE9	Alcatel-               # Alcatel-Lucent IPD
6CBFB5	Noon Technology Co., Ltd
6CC1D2	ARRIS Group, Inc.
6CC217	Hewlett Packard
6CC26B	Apple, Inc.
6CCA08	ARRIS Group, Inc.
6CD032	LG Electronics
6CD146	Smartek d.o.o.
6CD1B0	WING SING ELECTRONICS HONG KONG LIMITED
6CD68A	LG Electronics (Mobile Communications)
6CDC6A	Promethean Limited
6CE01E	Modcam AB
6CE0B0	Sound4
6CE3B6	Nera Telecommunications Ltd.
6CE4CE	Villiger Security Solutions AG
6CE873	TP-LINK TECHNOLOGIES CO.,LTD.
6CE907	Nokia Corporation
6CE983	Gastron Co., LTD.
6CEBB2	Dongguan Sen DongLv Electronics Co.,Ltd
6CEC5A	Hon Hai Precision Ind. CO.,Ltd.
6CECA1	SHENZHEN CLOU ELECTRONICS CO. LTD.
6CECEB	Texas Instruments
6CEFC6	SHENZHEN TWOWING TECHNOLOGIES CO.,LTD.
6CF049	GIGA-BYTE TECHNOLOGY CO.,LTD.
6CF373	Samsung Electronics Co.,Ltd
6CF37F	Aruba Networks
6CF5E8	Mooredoll Inc.
6CF97C	Nanoptix Inc.
6CFA58	Avaya Inc
6CFA89	Cisco Systems, Inc
6CFAA7	AMPAK Technology, Inc.
6CFDB9	Proware Technologies Co Ltd.
6CFFBE	MPB Communications Inc.
700136	FATEK Automation Corporation
700258	01DB-METRAVIB
700514	LG Electronics (Mobile Communications)
700BC0	Dewav Technology Company
700FC7	SHENZHEN IKINLOOP TECHNOLOGY CO.,LTD.
700FEC	Poindus Systems Corp.
70105C	Cisco Systems, Inc
70106F	Hewlett Packard Enterprise
701124	Apple, Inc.
7011AE	Music Life LTD
701404	Limited Liability Company
7014A6	Apple, Inc.
70188B	Hon Hai Precision Ind. Co.,Ltd.
701A04	Liteon Technology Corporation
701AED	ADVAS CO., LTD.
701CE7	Intel Corporate
701D7F	Comtech Technology Co., Ltd.
701DC4	NorthStar Battery Company, LLC
702084	Hon Hai Precision Ind. Co., Ltd.
702393	fos4X GmbH
702526	Nokia
702559	CyberTAN Technology Inc.
70288B	Samsung Electronics Co.,Ltd
702900	Shenzhen ChipTrip Technology Co,Ltd
702A7D	EpSpot AB
702B1D	E-Domus International Limited
702C1F	Wisol
702D84	i4C Innovations
702DD1	Newings Communication CO., LTD.
702E22	zte corporation
702F4B	PolyVision Inc.
702F97	Aava Mobile Oy
703018	Avaya Inc
70305D	Ubiquoss Inc
70305E	Nanjing Zhongke Menglian Information Technology Co.,LTD
703187	ACX GmbH
7032D5	Athena Wireless Communications Inc
703811	Invensys Rail
7038B4	Low Tech Solutions
7038EE	Avaya Inc
703A0E	Aruba Networks
703ACB	Google, Inc.
703AD8	Shenzhen Afoundry Electronic Co., Ltd
703C03	RadiAnt Co.,Ltd
703C39	SEAWING Kft
703D15	Hangzhou H3C Technologies Co., Limited
703EAC	Apple, Inc.
7041B7	Edwards Lifesciences LLC
704642	CHYNG HONG ELECTRONIC CO., LTD.
70480F	Apple, Inc.
704AAE	Xstream Flow (Pty) Ltd
704AE4	Rinstrum Pty Ltd
704CA5	Fortinet, Inc.
704CED	TMRG, Inc.
704D7B	ASUSTek COMPUTER INC.
704E01	KWANGWON TECH CO., LTD.
704E66	SHENZHEN FAST TECHNOLOGIES CO.,LTD
704F57	TP-LINK TECHNOLOGIES CO.,LTD.
7050AF	BSkyB Ltd
7052C5	Avaya Inc
70533F	Alfa Instrumentos Eletronicos Ltda.
7054D2	PEGATRON CORPORATION
7054F5	HUAWEI TECHNOLOGIES CO.,LTD
705681	Apple, Inc.
705812	Panasonic AVC Networks Company
705957	Medallion Instrumentation Systems
705986	OOO TTV
705A0F	Hewlett Packard
705A9E	Technicolor CH USA Inc.
705AB6	COMPAL INFORMATION (KUNSHAN) CO., LTD.
705B2E	M2Communication Inc.
705CAD	Konami Gaming Inc
705EAA	Action Target, Inc.
7060DE	LaVision GmbH
706173	Calantec GmbH
7062B8	D-Link International
706417	ORBIS TECNOLOGIA ELECTRICA S.A.
706582	Suzhou Hanming Technologies Co., Ltd.
70661B	Sonova AG
706879	Saijo Denki International Co., Ltd.
706DEC	Wifi-soft LLC
706F81	Private
70700D	Apple, Inc.
70704C	Purple Communications, Inc
7071B3	Brain Corporation
7071BC	PEGATRON CORPORATION
70720D	Lenovo Mobile Communication Technology Ltd.
70723C	HUAWEI TECHNOLOGIES CO.,LTD
7072CF	EdgeCore Networks
7073CB	Apple, Inc.
707630	ARRIS Group, Inc.
7076DD	Oxyguard International A/S
7076F0	LevelOne Communications (India) Private Limited
7076FF	Kerlink
707781	Hon Hai Precision Ind. Co.,Ltd.
707938	Wuxi Zhanrui Electronic Technology Co.,LTD
707990	HUAWEI TECHNOLOGIES CO.,LTD
707BE8	HUAWEI TECHNOLOGIES CO.,LTD
707C18	ADATA Technology Co., Ltd
707C69	Avaya Inc
707E43	ARRIS Group, Inc.
707EDE	NASTEC LTD.
708105	Cisco Systems, Inc
7081EB	Apple, Inc.
70820E	as electronics GmbH
70828E	OleumTech Corporation
7085C2	ASRock Incorporation
7085C6	ARRIS Group, Inc.
70884D	JAPAN RADIO CO., LTD.
708A09	HUAWEI TECHNOLOGIES CO.,LTD
708B78	citygrow technology co., ltd
708BCD	ASUSTek COMPUTER INC.
708D09	Nokia Corporation
70918F	Weber-Stephen Products LLC
709383	Intelligent Optical Network High Tech CO.,LTD.
7093F8	Space Monkey, Inc.
709756	Happyelectronics Co.,Ltd
709A0B	Italian Institute of Technology
709BA5	Shenzhen Y&D Electronics Co.,LTD.
709BFC	Bryton Inc.
709C8F	Nero AG
709E29	Sony Interactive Entertainment Inc.
709E86	X6D Limited
709F2D	zte corporation
70A191	Trendsetter Medical, LLC
70A2B3	Apple, Inc.
70A41C	Advanced Wireless Dynamics S.L.
70A66A	Prox Dynamics AS
70A84C	MONAD., Inc.
70A8E3	HUAWEI TECHNOLOGIES CO.,LTD
70AAB2	BlackBerry RTS
70AD54	Malvern Instruments Ltd
70AF24	TP Vision Belgium NV
70AF25	Nishiyama Industry Co.,LTD.
70AF6A	SHENZHEN FENGLIAN TECHNOLOGY CO., LTD.
70B035	Shenzhen Zowee Technology Co., Ltd
70B08C	Shenou Communication Equipment Co.,Ltd
70B14E	ARRIS Group, Inc.
70B265	Hiltron s.r.l.
70B3D5	IEEE Registration Authority
70B599	Embedded Technologies s.r.o.
70B921	Fiberhome Telecommunication Technologies Co.,LTD
70BAEF	Hangzhou H3C Technologies Co., Limited
70BF3E	Charles River Laboratories
70C6AC	Bosch Automotive Aftermarket
70C76F	INNO S
70CA4D	Shenzhen lnovance Technology Co.,Ltd.
70CA9B	Cisco Systems, Inc
70CD60	Apple, Inc.
70D379	Cisco Systems, Inc
70D4F2	Rim
70D57E	Scalar Corporation
70D5E7	Wellcore Corporation
70D6B6	Metrum Technologies
70D880	Upos System sp. z o.o.
70D923	vivo Mobile Communication Co., Ltd.
70D931	Cambridge Industries(Group) Co.,Ltd.
70DA9C	Tecsen
70DB98	Cisco Systems, Inc
70DDA1	Tellabs
70DEE2	Apple, Inc.
70E027	HONGYU COMMUNICATION TECHNOLOGY LIMITED
70E139	3view Ltd
70E24C	SAE IT-systems GmbH & Co. KG
70E284	Wistron Infocomm (Zhongshan) Corporation
70E422	Cisco Systems, Inc
70E72C	Apple, Inc.
70E843	Beijing C&W Optical Communication Technology Co.,Ltd.
70ECE4	Apple, Inc.
70EE50	Netatmo
70F087	Apple, Inc.
70F176	Data Modul AG
70F196	Actiontec Electronics, Inc
70F1A1	Liteon Technology Corporation
70F1E5	Xetawave LLC
70F395	Universal Global Scientific Industrial Co., Ltd.
70F8E7	IEEE Registration Authority
70F927	Samsung Electronics Co.,Ltd
70F96D	Hangzhou H3C Technologies Co., Limited
70FC8C	OneAccess SA
70FF5C	Cheerzing Communication(Xiamen)Technology Co.,Ltd
70FF76	Texas Instruments
7403BD	BUFFALO.INC
74042B	Lenovo Mobile Communication (Wuhan) Company Limited
740ABC	JSJS Designs (Europe) Limited
740EDB	Optowiz Co., Ltd
741489	SRT Wireless
7415E2	Tri-Sen Systems Corporation
741865	Shanghai DareGlobal Technologies Co.,Ltd
7419F8	IEEE Registration Authority
741BB2	Apple, Inc.
741E93	Fiberhome Telecommunication Technologies Co.,LTD
741F4A	Hangzhou H3C Technologies Co., Limited
742344	Xiaomi Communications Co Ltd
74258A	Hangzhou H3C Technologies Co., Limited
7426AC	Cisco Systems, Inc
74273C	ChangYang Technology (Nanjing) Co., LTD
7427EA	Elitegroup Computer Systems Co.,Ltd.
7429AF	Hon Hai Precision Ind. Co.,Ltd.
742B0F	Infinidat Ltd.
742B62	FUJITSU LIMITED
742D0A	Norfolk Elektronik AG
742EFC	DirectPacket Research, Inc,
742F68	AzureWave Technology Inc.
743170	Arcadyan Technology Corporation
743256	NT-ware Systemprg GmbH
74372F	Tongfang Shenzhen Cloudcomputing Technology Co.,Ltd
743889	ANNAX Anzeigesysteme GmbH
743A65	NEC Corporation
743E2B	Ruckus Wireless
743ECB	Gentrice tech
744401	Netgear
74458A	Samsung Electronics Co.,Ltd
7446A0	Hewlett Packard
744AA4	zte corporation
744BE9	EXPLORER HYPERTECH CO.,LTD
744D79	Arrive Systems Inc.
7451BA	Xiaomi Communications Co Ltd
745327	COMMSEN CO., LIMITED
74547D	Cisco SPVTG
745612	ARRIS Group, Inc.
745798	TRUMPF Laser GmbH + Co. KG
745AAA	HUAWEI TECHNOLOGIES CO.,LTD
745C9F	TCT mobile ltd
745E1C	PIONEER CORPORATION
745F00	Samsung Semiconductor Inc.
745FAE	TSL PPL
74614B	Chongqing Huijiatong Information Technology Co., Ltd.
7463DF	VTS GmbH
7465D1	Atlinks
746630	Tmi Ytti
7467F7	Extreme Networks
746A3A	Aperi Corporation
746A89	Rezolt Corporation
746A8F	VS Vision Systems GmbH
746B82	Movek
746F19	ICARVISIONS (SHENZHEN) TECHNOLOGY CO., LTD.
746F3D	Contec GmbH
746FF7	Wistron Neweb Corporation
7472B0	Guangzhou Shiyuan Electronics Co., Ltd.
7472F2	Chipsip Technology Co., Ltd.
747336	MICRODIGTAL Inc
747548	Amazon Technologies Inc.
747818	Jurumani Solutions
747B7A	ETH Inc.
747DB6	Aliwei Communications, Inc
747E1A	Red Embedded Design Limited
747E2D	Beijing Thomson CITIC Digital Technology Co. LTD.
748114	Apple, Inc.
74852A	PEGATRON CORPORATION
74867A	Dell Inc.
7487A9	OCT Technology Co., Ltd.
74882A	HUAWEI TECHNOLOGIES CO.,LTD
74888B	ADB Broadband Italia
748A69	Korea Image Technology Co., Ltd
748D08	Apple, Inc.
748E08	Bestek Corp.
748EF8	Brocade Communications Systems, Inc.
748F1B	MasterImage 3D
748F4D	MEN Mikro Elektronik GmbH
749050	Renesas Electronics Corporation
74911A	Ruckus Wireless
7491BD	Four systems Co.,Ltd.
7493A4	Zebra Technologies Corp.
74943D	AgJunction
749637	Todaair Electronic Co., Ltd
749781	zte corporation
749975	IBM Corporation
749C52	Huizhou Desay SV Automotive Co., Ltd.
749CE3	KodaCloud Canada, Inc
749D8F	HUAWEI TECHNOLOGIES CO.,LTD
749DDC	2Wire Inc
74A02F	Cisco Systems, Inc
74A063	HUAWEI TECHNOLOGIES CO.,LTD
74A2E6	Cisco Systems, Inc
74A34A	ZIMI CORPORATION
74A4A7	QRS Music Technologies, Inc.
74A4B5	Powerleader Science and Technology Co. Ltd.
74A528	HUAWEI TECHNOLOGIES CO.,LTD
74A722	LG Electronics (Mobile Communications)
74A78E	zte corporation
74AC5F	Qiku Internet Network Scientific (Shenzhen) Co., Ltd.
74ADB7	China Mobile Group Device Co.,Ltd.
74AE76	iNovo Broadband, Inc.
74B00C	Network Video Technologies, Inc
74B472	Ciesse
74B57E	zte corporation
74B9EB	JinQianMao Technology Co.,Ltd.
74BADB	Longconn Electornics(shenzhen)Co.,Ltd
74BE08	ATEK Products, LLC
74BFA1	Hyunteck
74BFB7	Nusoft Corporation
74C246	Amazon Technologies Inc.
74C330	SHENZHEN FAST TECHNOLOGIES CO.,LTD
74C621	Zhejiang Hite Renewable Energy Co.,LTD
74C63B	AzureWave Technology Inc.
74C99A	Ericsson AB
74C9A3	Fiberhome Telecommunication Technologies Co.,LTD
74CA25	Calxeda, Inc.
74CC39	Fiberhome Telecommunication Technologies Co.,LTD
74CD0C	Smith Myers Communications Ltd.
74CE56	Packet Force Technology Limited Company
74D02B	ASUSTek COMPUTER INC.
74D0DC	ERICSSON AB
74D435	GIGA-BYTE TECHNOLOGY CO.,LTD.
74D675	WYMA Tecnologia
74D6EA	Texas Instruments
74D7CA	Panasonic Corporation Automotive
74D850	Evrisko Systems
74DA38	Edimax Technology Co. Ltd.
74DAEA	Texas Instruments
74DBD1	Ebay Inc
74DE2B	Liteon Technology Corporation
74DFBF	Liteon Technology Corporation
74E06E	Ergophone GmbH
74E14A	IEEE Registration Authority
74E1B6	Apple, Inc.
74E277	Vizmonet Pte Ltd
74E28C	Microsoft Corporation
74E2F5	Apple, Inc.
74E424	APISTE CORPORATION
74E50B	Intel Corporate
74E537	Radspin
74E543	Liteon Technology Corporation
74E6E2	Dell Inc.
74E7C6	ARRIS Group, Inc.
74EA3A	TP-LINK TECHNOLOGIES CO.,LTD.
74EAE8	ARRIS Group, Inc.
74ECF1	Acumen
74F06D	AzureWave Technology Inc.
74F07D	BnCOM Co.,Ltd
74F102	Beijing HCHCOM Technology Co., Ltd
74F413	Maxwell Forest
74F612	ARRIS Group, Inc.
74F726	Neuron Robotics
74F85D	Berkeley Nucleonics Corp
74F8DB	IEEE Registration Authority
74FDA0	Compupal (Group) Corporation
74FE48	ADVANTECH CO., LTD.
74FF4C	Skyworth Digital Technology(Shenzhen) Co.,Ltd
74FF7D	Wren Sound Systems, LLC
78009E	Samsung Electronics Co.,Ltd
78028F	Adaptive Spectrum and Signal Alignment (ASSIA), Inc.
7802B7	ShenZhen Ultra Easy Technology CO.,LTD
7802F8	Xiaomi Communications Co Ltd
780541	Queclink Wireless Solutions Co., Ltd
780738	Z.U.K. Elzab S.A.
780AC7	Baofeng TV Co., Ltd.
780CB8	Intel Corporate
781185	NBS Payment Solutions Inc.
7812B8	ORANTEK LIMITED
781881	AzureWave Technology Inc.
78192E	NASCENT Technology
7819F7	Juniper Networks
781C5A	SHARP Corporation
781DBA	HUAWEI TECHNOLOGIES CO.,LTD
781DFD	Jabil Inc
781FDB	Samsung Electronics Co.,Ltd
782079	ID Tech
78223D	Affirmed Networks
7823AE	ARRIS Group, Inc.
7824AF	ASUSTek COMPUTER INC.
782544	Omnima Limited
7825AD	Samsung Electronics Co.,Ltd
7828CA	Sonos, Inc.
782BCB	Dell Inc.
782EEF	Nokia Corporation
78303B	Stephen Technologies Co.,Limited
7830E1	UltraClenz, LLC
78312B	zte corporation
7831C1	Apple, Inc.
78324F	Millennium Group, Inc.
783A84	Apple, Inc.
783CE3	Kai-Ee
783D5B	TELNET Redes Inteligentes S.A.
783E53	BSkyB Ltd
783F15	EasySYNC Ltd.
7840E4	Samsung Electronics Co.,Ltd
784405	FUJITU(HONG KONG) ELECTRONIC Co.,LTD.
784476	Zioncom Electronics (Shenzhen) Ltd.
784561	CyberTAN Technology Inc.
7845C4	Dell Inc.
7846C4	DAEHAP HYPER-TECH
78471D	Samsung Electronics Co.,Ltd
784859	Hewlett Packard
78491D	The Will-Burt Company
784B08	f.robotics acquisitions ltd
784B87	Murata Manufacturing Co., Ltd.
784F43	Apple, Inc.
78510C	LiveU Ltd.
78521A	Samsung Electronics Co.,Ltd
785262	Shenzhen Hojy Software Co., Ltd.
7853F2	ROXTON Ltd.
78542E	D-Link International
785517	SankyuElectronics
785712	Mobile Integration Workgroup
7858F3	Vachen Co.,Ltd
78593E	RAFI GmbH & Co.KG
78595E	Samsung Electronics Co.,Ltd
785968	Hon Hai Precision Ind. Co.,Ltd.
785C72	Hioso Technology Co., Ltd.
785F4C	Argox Information Co., Ltd.
78617C	MITSUMI ELECTRIC CO.,LTD
7864E6	Green Motive Technology Limited
7866AE	ZTEC Instruments, Inc.
7868F7	YSTen Technology Co.,Ltd
786A89	HUAWEI TECHNOLOGIES CO.,LTD
786C1C	Apple, Inc.
78719C	ARRIS Group, Inc.
787D48	ITEL MOBILE LIMITED
787E61	Apple, Inc.
787F62	GiK mbH
78818F	Server Racks Australia Pty Ltd
78843C	Sony Corporation
7884EE	INDRA ESPACIO S.A.
78888A	CDR Sp. z o.o. Sp. k.
788973	Cmc
788A20	Ubiquiti Networks Inc.
788B77	Standar Telecom
788C54	Eltek Technologies LTD
788DF7	Hitron Technologies. Inc
788E33	Jiangsu SEUIC Technology Co.,Ltd
78923E	Nokia Corporation
78929C	Intel Corporate
7894B4	Sercomm Corporation.
789682	zte corporation
789684	ARRIS Group, Inc.
7898FD	Q9 Networks Inc.
78995C	Nationz Technologies Inc
789966	Musilab Electronics (DongGuan)Co.,Ltd.
78998F	MEDILINE ITALIA SRL
789C85	August Home, Inc.
789CE7	Shenzhen Aikede Technology Co., Ltd
789ED0	Samsung Electronics Co.,Ltd
789F4C	HOERBIGER Elektronik GmbH
789F70	Apple, Inc.
789F87	Siemens AG I IA PP PRM
78A051	iiNet Labs Pty Ltd
78A106	TP-LINK TECHNOLOGIES CO.,LTD.
78A183	Advidia
78A2A0	Nintendo Co., Ltd.
78A351	SHENZHEN ZHIBOTONG ELECTRONICS CO.,LTD
78A3E4	Apple, Inc.
78A504	Texas Instruments
78A5DD	Shenzhen Smarteye Digital Electronics Co., Ltd
78A683	Precidata
78A6BD	DAEYEON Control&Instrument Co,.Ltd
78A714	Amphenol
78A873	Samsung Electronics Co.,Ltd
78AB60	ABB Australia
78ABBB	Samsung Electronics Co.,Ltd
78ACBF	Igneous Systems
78ACC0	Hewlett Packard
78AE0C	Far South Networks
78AF58	GIMASI SA
78B3B9	ShangHai sunup lighting CO.,LTD
78B3CE	Elo touch solutions
78B5D2	Ever Treasure Industrial Limited
78B6C1	AOBO Telecom Co.,Ltd
78B81A	INTER SALES A/S
78B84B	SICHUAN TIANYI COMHEART TELECOMCO.,LTD
78BAD0	Shinybow Technology Co. Ltd.
78BAF9	Cisco Systems, Inc
78BDBC	Samsung Electronics Co.,Ltd
78BEB6	Enhanced Vision
78BEBD	STULZ GmbH
78C1A7	zte corporation
78C2C0	IEEE Registration Authority
78C3E9	Samsung Electronics Co.,Ltd
78C40E	H&D Wireless
78C4AB	Shenzhen Runsil Technology Co.,Ltd
78C5E5	Texas Instruments
78C6BB	Innovasic, Inc.
78CA04	Nokia Corporation
78CA39	Apple, Inc.
78CA5E	Elno
78CA83	IEEE Registration Authority
78CB33	DHC Software Co.,Ltd
78CB68	DAEHAP HYPER-TECH
78CD8E	SMC Networks Inc
78D004	Neousys Technology Inc.
78D129	Vicos
78D34F	Pace-O-Matic, Inc.
78D38D	HONGKONG YUNLINK TECHNOLOGY LIMITED
78D5B5	NAVIELEKTRO KY
78D66F	Aristocrat Technologies Australia Pty. Ltd.
78D6B2	Toshiba
78D6F0	SAMSUNG ELECTRO MECHANICS CO., LTD.
78D752	HUAWEI TECHNOLOGIES CO.,LTD
78D75F	Apple, Inc.
78D99F	NuCom HK Ltd.
78DA6E	Cisco Systems, Inc
78DAB3	GBO Technology
78DD08	Hon Hai Precision Ind. Co.,Ltd.
78DDD6	C-Scape
78DEE4	Texas Instruments
78E3B5	Hewlett Packard
78E400	Hon Hai Precision Ind. Co.,Ltd.
78E7D1	Hewlett Packard
78E8B6	zte corporation
78E980	RainUs Co.,Ltd
78EB14	SHENZHEN FAST TECHNOLOGIES CO.,LTD
78EB39	Instituto Nacional de Tecnología Industrial
78EC22	Shanghai Qihui Telecom Technology Co., LTD
78EC74	Kyland-USA
78EF4C	Unetconvergence Co., Ltd.
78F29E	PEGATRON CORPORATION
78F557	HUAWEI TECHNOLOGIES CO.,LTD
78F5E5	BEGA Gantenbrink-Leuchten KG
78F5FD	HUAWEI TECHNOLOGIES CO.,LTD
78F7BE	Samsung Electronics Co.,Ltd
78F7D0	Silverbrook Research
78F882	LG Electronics (Mobile Communications)
78F944	Private
78FC14	Family Zone Cyber Safety Ltd
78FD94	Apple, Inc.
78FE3D	Juniper Networks
78FE41	Socus networks
78FEE2	Shanghai Diveo Technology Co., Ltd
78FF57	Intel Corporate
78FFCA	TECNO MOBILE LIMITED
7C0187	Curtis Instruments, Inc.
7C0191	Apple, Inc.
7C02BC	Hansung Electronics Co. LTD
7C034C	Sagemcom Broadband SAS
7C03C9	Shenzhen YOUHUA Technology Co., Ltd
7C03D8	Sagemcom Broadband SAS
7C04D0	Apple, Inc.
7C0507	PEGATRON CORPORATION
7C051E	RAFAEL LTD.
7C0623	Ultra Electronics Sonar System Division
7C08D9	Shanghai B-Star Technology Co
7C092B	Bekey A/S
7C0A50	J-MEX Inc.
7C0BC6	Samsung Electronics Co.,Ltd
7C0ECE	Cisco Systems, Inc
7C1015	Brilliant Home Technology, Inc.
7C11BE	Apple, Inc.
7C11CB	HUAWEI TECHNOLOGIES CO.,LTD
7C11CD	QianTang Technology
7C1476	Damall Technologies SAS
7C160D	Saia-Burgess Controls AG
7C18CD	E-TRON Co.,Ltd.
7C1A03	8Locations Co., Ltd.
7C1AFC	Dalian Co-Edifice Video Technology Co., Ltd
7C1CF1	HUAWEI TECHNOLOGIES CO.,LTD
7C1DD9	Xiaomi Communications Co Ltd
7C1E52	Microsoft
7C1EB3	2N TELEKOMUNIKACE a.s.
7C2048	Koamtac
7C2064	Alcatel-               # Alcatel-Lucent IPD
7C2587	chaowifi.com
7C2634	ARRIS Group, Inc.
7C2664	Sagemcom Broadband SAS
7C2BE1	Shenzhen Ferex Electrical Co.,Ltd
7C2CF3	Secure Electrans Ltd
7C2E0D	Blackmagic Design
7C2F80	Gigaset Communications GmbH
7C336E	MEG Electronics Inc.
7C3548	Transcend Information
7C3866	Texas Instruments
7C386C	Real Time Logic
7C3920	SSOMA SECURITY
7C3BD5	Imago Group
7C3CB6	Shenzhen Homecare Technology Co.,Ltd.
7C3E9D	Patech
7C438F	E-Band Communications Corp.
7C444C	Entertainment Solutions, S.L.
7C4685	Motorola (Wuhan) Mobility Technologies Communication Co., Ltd.
7C477C	IEEE Registration Authority
7C49B9	Plexus Manufacturing Sdn Bhd
7C4A82	Portsmith LLC
7C4AA8	MindTree Wireless PVT Ltd
7C4B78	Red Sun Synthesis Pte Ltd
7C4C58	Scale Computing, Inc.
7C4CA5	BSkyB Ltd
7C4F7D	Sawwave
7C4FB5	Arcadyan Technology Corporation
7C5049	Apple, Inc.
7C534A	Metamako
7C55E7	YSI, Inc.
7C574E	COBI GmbH
7C5A1C	Sophos Ltd
7C5A67	JNC Systems, Inc.
7C5CF8	Intel Corporate
7C6097	HUAWEI TECHNOLOGIES CO.,LTD
7C6193	HTC Corporation
7C669D	Texas Instruments
7C67A2	Intel Corporate
7C69F6	Cisco Systems, Inc
7C6AB3	IBC TECHNOLOGIES INC.
7C6AC3	GatesAir, Inc
7C6ADB	SafeTone Technology Co.,Ltd
7C6AF3	Integrated Device Technology (Malaysia) Sdn. Bhd.
7C6B33	Tenyu Tech Co. Ltd.
7C6B52	Tigaro Wireless
7C6BF7	NTI co., ltd.
7C6C39	PIXSYS SRL
7C6C8F	AMS NEVE LTD
7C6D62	Apple, Inc.
7C6DF8	Apple, Inc.
7C6F06	Caterpillar Trimble Control Technologies
7C6FF8	ShenZhen ACTO Digital Video Technology Co.,Ltd.
7C70BC	IEEE Registration Authority
7C7176	Wuxi iData Technology Company Ltd.
7C72E4	Unikey Technologies
7C738B	Cocoon Alarm Ltd
7C7673	ENMAS GmbH
7C787E	Samsung Electronics Co.,Ltd
7C79E8	PayRange Inc.
7C7A53	Phytrex Technology Corp.
7C7A91	Intel Corporate
7C7B8B	Control Concepts, Inc.
7C7BE4	Z'SEDAI KENKYUSHO CORPORATION
7C7D3D	HUAWEI TECHNOLOGIES CO.,LTD
7C7D41	Jinmuyu Electronics Co., Ltd.
7C822D	Nortec
7C8274	Shenzhen Hikeen Technology CO.,LTD
7C8306	Glen Dimplex Nordic as
7C8D91	Shanghai Hongzhuo Information Technology co.,LTD
7C8EE4	Texas Instruments
7C9122	Samsung Electronics Co.,Ltd
7C94B2	Philips Healthcare PCCI
7C95B1	Aerohive Networks Inc.
7C95F3	Cisco Systems, Inc
7C9763	Openmatics s.r.o.
7C9A9B	VSE valencia smart energy
7CA15D	GN ReSound A/S
7CA237	King Slide Technology CO., LTD.
7CA23E	HUAWEI TECHNOLOGIES CO.,LTD
7CA29B	D.SignT GmbH & Co. KG
7CA61D	MHL, LLC
7CA97D	Objenious
7CAB25	MESMO TECHNOLOGY INC.
7CACB2	Bosch Software Innovations GmbH
7CAD74	Cisco Systems, Inc
7CB03E	OSRAM GmbH
7CB0C2	Intel Corporate
7CB15D	HUAWEI TECHNOLOGIES CO.,LTD
7CB177	Satelco AG
7CB21B	Cisco SPVTG
7CB232	Hui Zhou Gaoshengda Technology Co.,LTD
7CB25C	Acacia Communications
7CB542	ACES Technology
7CB733	ASKEY COMPUTER CORP
7CB77B	Paradigm Electronics Inc
7CB960	Shanghai X-Cheng telecom LTD
7CBB6F	Cosco Electronics Co., Ltd.
7CBB8A	Nintendo Co., Ltd.
7CBD06	AE REFUsol
7CBF88	Mobilicom LTD
7CBFB1	ARRIS Group, Inc.
7CC3A1	Apple, Inc.
7CC4EF	Devialet
7CC537	Apple, Inc.
7CC6C4	Kolff Computer Supplies b.v.
7CC709	SHENZHEN RF-LINK TECHNOLOGY CO.,LTD.
7CC8AB	Acro Associates, Inc.
7CC8D0	TIANJIN YAAN TECHNOLOGY CO., LTD.
7CC8D7	Damalisk
7CC95A	Emc
7CCB0D	Antaira Technologies, LLC
7CCBE2	IEEE Registration Authority
7CCC1F	SICHUAN TIANYI COMHEART TELECOMCO.,LTD
7CCCB8	Intel Corporate
7CCD11	MS-Magnet
7CCD3C	Guangzhou Juzing Technology Co., Ltd
7CCFCF	Shanghai SEARI Intelligent System Co., Ltd
7CD1C3	Apple, Inc.
7CD30A	INVENTEC Corporation
7CD762	Freestyle Technology Pty Ltd
7CD844	Enmotus Inc
7CD9FE	New Cosmos Electric Co., Ltd.
7CDA84	Dongnian Networks Inc.
7CDD11	Chongqing MAS SCI&TECH.Co.,Ltd
7CDD20	IOXOS Technologies S.A.
7CDD90	Shenzhen Ogemray Technology Co., Ltd.
7CE044	NEON Inc
7CE1FF	Computer Performance, Inc. DBA Digital Loggers, Inc.
7CE4AA	Private
7CE524	Quirky, Inc.
7CE56B	ESEN Optoelectronics Technology Co.,Ltd.
7CE97C	ITEL MOBILE LIMITED
7CE9D3	Hon Hai Precision Ind. Co.,Ltd.
7CEBAE	Ridgeline Instruments
7CEBEA	Asct
7CEC79	Texas Instruments
7CED8D	Microsoft
7CEF18	Creative Product Design Pty. Ltd.
7CEF8A	Inhon International Ltd.
7CF05F	Apple, Inc.
7CF098	Bee Beans Technologies, Inc.
7CF0BA	Linkwell Telesystems Pvt Ltd
7CF429	NUUO Inc.
7CF854	Samsung Electronics Co.,Ltd
7CF90E	Samsung Electronics Co.,Ltd
7CF95C	U.I. Lapp GmbH
7CFADF	Apple, Inc.
7CFC3C	Visteon Corporation
7CFE28	Salutron Inc.
7CFE4E	Shenzhen Safe vision Technology Co.,LTD
7CFE90	Mellanox Technologies, Inc.
7CFF62	Huizhou Super Electron Technology Co.,Ltd.
80000B	Intel Corporate
800010	AT&T [misrepresented as 080010? One source claims this is correct]
80006E	Apple, Inc.
800184	HTC Corporation
8002DF	ORA Inc.
8005DF	Montage Technology Group Limited
8007A2	Esson Technology Inc.
800902	Keysight Technologies, Inc.
800A06	COMTEC co.,ltd
800A80	IEEE Registration Authority
800B51	Chengdu XGimi Technology Co.,Ltd
800DD7	Latticework, Inc
800E24	ForgetBox
801382	HUAWEI TECHNOLOGIES CO.,LTD
801440	Sunlit System Technology Corp
8014A8	Guangzhou V-SOLUTION Electronic Technology Co., Ltd.
8016B7	Brunel University
80177D	Nortel Networks
801844	Dell Inc.
8018A7	Samsung Electronics Co.,Ltd
801934	Intel Corporate
801967	Shanghai Reallytek Information Technology  Co.,Ltd
8019FE	JianLing Technology CO., LTD
801DAA	Avaya Inc
801F02	Edimax Technology Co. Ltd.
8020AF	Trade FIDES, a.s.
802275	Beijing Beny Wave Technology Co Ltd
802689	D-Link International
802994	Technicolor CH USA Inc.
802AA8	Ubiquiti Networks Inc.
802AFA	Germaneers GmbH
802DE1	Solarbridge Technologies
802E14	azeti Networks AG
802FDE	Zurich Instruments AG
8030DC	Texas Instruments
803457	OT Systems Limited
803773	Netgear
803896	SHARP Corporation
8038BC	HUAWEI TECHNOLOGIES CO.,LTD
8038FD	LeapFrog Enterprises, Inc.
8039E5	PATLITE CORPORATION
803A0A	Integrated Device Technology (Malaysia) Sdn. Bhd.
803B2A	ABB Xiamen Low Voltage Equipment Co.,Ltd.
803B9A	ghe-ces electronic ag
803F5D	Winstars Technology Ltd
803FD6	bytes at work AG
80414E	BBK EDUCATIONAL ELECTRONICS CORP.,LTD.
80427C	Adolf Tedsen GmbH & Co. KG
804731	Packet Design, Inc.
8048A5	SICHUAN TIANYI COMHEART TELECOMCO.,LTD
804971	Apple, Inc.
804B20	Ventilation Control
804E81	Samsung Electronics Co.,Ltd
804F58	ThinkEco, Inc.
80501B	Nokia Corporation
805067	W & D TECHNOLOGY CORPORATION
8056F2	Hon Hai Precision Ind. Co.,Ltd.
805719	Samsung Electronics Co.,Ltd
8058C5	NovaTec Kommunikationstechnik GmbH
8058F8	Motorola Mobility LLC, a Lenovo Company
8059FD	Noviga
805A04	LG Electronics (Mobile Communications)
805EC0	YEALINK(XIAMEN) NETWORK TECHNOLOGY CO.,LTD.
806007	Rim
80618F	Shenzhen sangfei consumer communications co.,ltd
806459	Nimbus Inc.
80656D	Samsung Electronics Co.,Ltd
8065E9	BenQ Corporation
806629	Prescope Technologies CO.,LTD.
806AB0	Shenzhen TINNO Mobile Technology Corp.
806C1B	Motorola Mobility LLC, a Lenovo Company
806C8B	KAESER KOMPRESSOREN AG
806CBC	NET New Electronic Technology GmbH
80711F	Juniper Networks
80717A	HUAWEI TECHNOLOGIES CO.,LTD
80739F	KYOCERA Corporation
807459	K's Co.,Ltd.
807693	Newag SA
8079AE	ShanDong Tecsunrise  Co.,Ltd
807A7F	ABB Genway Xiamen Electrical Equipment CO., LTD
807ABF	HTC Corporation
807B1E	Corsair Components
807B85	IEEE Registration Authority
807D1B	Neosystem Co. Ltd.
807DE3	Chongqing Sichuan Instrument Microcircuit Co.LTD.
8081A5	TONGQING COMMUNICATION EQUIPMENT (SHENZHEN) Co.,Ltd
808287	ATCOM Technology Co.Ltd.
808698	Netronics Technologies Inc.
8086F2	Intel Corporate
808917	TP-LINK TECHNOLOGIES CO.,LTD.
808B5C	Shenzhen Runhuicheng Technology Co., Ltd
808C97	Kaonmedia CO., LTD.
80912A	Lih Rong electronic Enterprise Co., Ltd.
8091C0	AgileMesh, Inc.
80929F	Apple, Inc.
809393	Xapt GmbH
80946C	TOKYO RADAR CORPORATION
8096B1	ARRIS Group, Inc.
8096CA	Hon Hai Precision Ind. Co.,Ltd.
80971B	Altenergy Power System,Inc.
809B20	Intel Corporate
809FAB	Fiberhome Telecommunication Technologies Co.,LTD
80A1AB	Intellisis
80A1D7	Shanghai DareGlobal Technologies Co.,Ltd
80A589	AzureWave Technology Inc.
80A85D	Osterhout Design Group
80AAA4	Usag
80ACAC	Juniper Networks
80AD00	CNET Technology Inc. (Probably an error, see instead 0080AD)
80AD67	Kasda Networks Inc
80B219	ELEKTRON TECHNOLOGY UK LIMITED
80B289	Forworld Electronics Ltd.
80B32A	Alstom Grid
80B686	HUAWEI TECHNOLOGIES CO.,LTD
80B709	Viptela, Inc
80B95C	ELFTECH Co., Ltd.
80BAAC	TeleAdapt Ltd
80BAE6	Neets
80BBEB	Satmap Systems Ltd
80BE05	Apple, Inc.
80C16E	Hewlett Packard
80C5E6	Microsoft Corporation
80C63F	Remec Broadband Wireless , LLC
80C6AB	Technicolor CH USA Inc.
80C6CA	Endian s.r.l.
80C862	Openpeak, Inc
80CEB1	Theissen Training Systems GmbH
80CF41	Lenovo Mobile Communication Technology Ltd.
80D019	Embed, Inc
80D09B	HUAWEI TECHNOLOGIES CO.,LTD
80D160	Integrated Device Technology (Malaysia) Sdn. Bhd.
80D18B	Hangzhou I'converge Technology Co.,Ltd
80D21D	AzureWave Technology Inc.
80D433	LzLabs GmbH
80D4A5	HUAWEI TECHNOLOGIES CO.,LTD
80D605	Apple, Inc.
80D733	QSR Automations, Inc.
80DB31	Power Quotient International Co., Ltd.
80E01D	Cisco Systems, Inc
80E4DA	IEEE Registration Authority
80E650	Apple, Inc.
80E86F	Cisco Systems, Inc
80EA23	Wistron Neweb Corporation
80EA96	Apple, Inc.
80EACA	Dialog Semiconductor Hellas SA
80EB77	Wistron Corporation
80ED2C	Apple, Inc.
80EE73	Shuttle Inc.
80F25E	Kyynel
80F503	ARRIS Group, Inc.
80F593	IRCO Sistemas de Telecomunicación S.A.
80F62E	Hangzhou H3C Technologies Co., Limited
80F8EB	Raytight
80FA5B	CLEVO CO.
80FB06	HUAWEI TECHNOLOGIES CO.,LTD
80FFA8	Unidis
84002D	PEGATRON CORPORATION
8400D2	Sony Mobile Communications AB
8401A7	Greyware Automation Products, Inc
8404D2	Kirale Technologies SL
840B2D	SAMSUNG ELECTRO MECHANICS CO., LTD.
840F45	Shanghai GMT Digital Technologies Co., Ltd
84100D	Motorola Mobility LLC, a Lenovo Company
84119E	Samsung Electronics Co.,Ltd
8416F9	TP-LINK TECHNOLOGIES CO.,LTD.
841715	GP Electronics (HK) Ltd.
841766	Weifang GoerTek Electronics Co., Ltd
841826	Osram GmbH
84183A	Ruckus Wireless
841888	Juniper Networks
841B38	Shenzhen Excelsecu Data Technology Co.,Ltd
841B5E	Netgear
841E26	KERNEL-I Co.,LTD
842141	Shenzhen Ginwave Technologies Ltd.
8421F1	HUAWEI TECHNOLOGIES CO.,LTD
84248D	Zebra Technologies Inc
842519	Samsung Electronics
84253F	Silex Technology, Inc
8425A4	Tariox Limited
8425DB	Samsung Electronics Co.,Ltd
842615	ADB Broadband Italia
84262B	Nokia
842690	BEIJING THOUGHT SCIENCE CO.,LTD.
8427CE	Corporation of the Presiding Bishop of The Church of Jesus Christ of Latter-day Saints
84285A	Saffron Solutions Inc
842914	EMPORIA TELECOM Produktions- und VertriebsgesmbH & Co KG
842999	Apple, Inc.
842B2B	Dell Inc.
842B50	Huria Co.,Ltd.
842BBC	Modelleisenbahn GmbH
842E27	Samsung Electronics Co.,Ltd
842F75	Innokas Group
8430E5	SkyHawke Technologies, LLC
8432EA	ANHUI WANZTEN P&T CO., LTD
843497	Hewlett Packard
843611	hyungseul publishing networks
843835	Apple, Inc.
843838	SAMSUNG ELECTRO-MECHANICS(THAILAND)
843A4B	Intel Corporate
843DC6	Cisco Systems, Inc
843F4E	Tri-Tech Manufacturing, Inc.
844076	Drivenets
844464	ServerU Inc
844765	HUAWEI TECHNOLOGIES CO.,LTD
844823	WOXTER TECHNOLOGY Co. Ltd
844915	vArmour Networks, Inc.
844BB7	Beijing Sankuai Online Technology Co.,Ltd
844BF5	Hon Hai Precision Ind. Co.,Ltd.
844F03	Ablelink Electronics Ltd
845181	Samsung Electronics Co.,Ltd
8455A5	Samsung Electronics Co.,Ltd
84569C	Coho Data, Inc.,
845787	DVR C&C Co., Ltd.
845A81	Ffly4u
845B12	HUAWEI TECHNOLOGIES CO.,LTD
845C93	Chabrier Services
845DD7	Shenzhen Netcom Electronics Co.,Ltd
8461A0	ARRIS Group, Inc.
846223	Shenzhen Coship Electronics Co., Ltd.
8462A6	EuroCB (Phils), Inc.
8463D6	Microsoft Corporation
84683E	Intel Corporate
846AED	Wireless Tsukamoto.,co.LTD
846EB1	Park Assist LLC
847207	I&C Technology
847303	Letv Mobile and Intelligent Information Technology (Beijing) Corporation Ltd.
84742A	zte corporation
847616	Addat s.r.o.
847778	Cochlear Limited
84788B	Apple, Inc.
8478AC	Cisco Systems, Inc
847933	profichip GmbH
847973	Shanghai Baud Data Communication Co.,Ltd.
847A88	HTC Corporation
847BEB	Dell Inc.
847D50	Holley Metering Limited
847E40	Texas Instruments
84802D	Cisco Systems, Inc
8482F4	Beijing Huasun Unicreate Technology Co., Ltd
848319	Hangzhou Zero Zero Technology Co., Ltd.
848336	Newrun
848371	Avaya Inc
848433	Paradox Engineering SA
848506	Apple, Inc.
84850A	Hella Sonnen- und Wetterschutztechnik GmbH
8486F3	Greenvity Communications
8489AD	Apple, Inc.
848D84	Rajant Corporation
848DC7	Cisco SPVTG
848E0C	Apple, Inc.
848E96	Embertec Pty Ltd
848EDF	Sony Mobile Communications AB
848F69	Dell Inc.
849000	Arnold & Richter Cine Technik
84930C	InCoax Networks Europe AB
84948C	Hitron Technologies. Inc
849681	Cathay Communication Co.,Ltd
8496D8	ARRIS Group, Inc.
8497B8	Memjet Inc.
849866	Samsung Electronics Co.,Ltd
849CA6	Arcadyan Technology Corporation
849D64	SMC Corporation
849DC5	Centera Photonics Inc.
849FB5	HUAWEI TECHNOLOGIES CO.,LTD
84A134	Apple, Inc.
84A423	Sagemcom Broadband SAS
84A466	Samsung Electronics Co.,Ltd
84A6C8	Intel Corporate
84A783	Alcatel Lucent
84A788	Perples
84A8E4	HUAWEI TECHNOLOGIES CO.,LTD
84A991	Cyber Trans Japan Co.,Ltd.
84A9C4	HUAWEI TECHNOLOGIES CO.,LTD
84ACA4	Beijing Novel Super Digital TV Technology Co., Ltd
84ACFB	Crouzet Automatismes
84AD58	HUAWEI TECHNOLOGIES CO.,LTD
84AF1F	Beat System Service Co,. Ltd.
84AFEC	BUFFALO.INC
84B153	Apple, Inc.
84B261	Cisco Systems, Inc
84B517	Cisco Systems, Inc
84B541	Samsung Electronics Co.,Ltd
84B59C	Juniper Networks
84B802	Cisco Systems, Inc
84BA3B	CANON INC.
84BE52	HUAWEI TECHNOLOGIES CO.,LTD
84C1C1	Juniper Networks
84C2E4	Jiangsu Qinheng Co., Ltd.
84C3E8	Vaillant GmbH
84C727	Gnodal Ltd
84C7A9	C3PO S.A.
84C7EA	Sony Mobile Communications AB
84C8B1	Incognito Software Systems Inc.
84C9B2	D-Link International
84CD62	ShenZhen IDWELL Technology CO.,Ltd
84CFBF	Fairphone
84D32A	IEEE 1905.1
84D47E	Aruba Networks
84D4C8	Widex A/S
84D6D0	Amazon Technologies Inc.
84D931	Hangzhou H3C Technologies Co., Limited
84D9C8	Unipattern Co.,
84DB2F	Sierra Wireless Inc
84DBAC	HUAWEI TECHNOLOGIES CO.,LTD
84DBFC	Nokia
84DD20	Texas Instruments
84DDB7	Cilag GmbH International
84DE3D	Crystal Vision Ltd
84DF0C	NET2GRID BV
84DF19	Chuango Security Technology Corporation
84E058	ARRIS Group, Inc.
84E0F4	IEEE Registration Authority
84E323	Green Wave Telecommunication SDN BHD
84E4D9	Shenzhen NEED technology Ltd.
84E629	Bluwan SA
84E714	Liang Herng Enterprise,Co.Ltd.
84EA99	Vieworks
84EB18	Texas Instruments
84ED33	BBMC Co.,Ltd
84EF18	Intel Corporate
84F129	Metrascale Inc.
84F493	OMS spol. s.r.o.
84F64C	Cross Point BV
84F6FA	Miovision Technologies Incorporated
84FCAC	Apple, Inc.
84FCFE	Apple, Inc.
84FE9E	RTC Industries, Inc.
84FEDC	Borqs Beijing Ltd.
8801F2	Vitec System Engineering Inc.
880355	Arcadyan Technology Corporation
88074B	LG Electronics (Mobile Communications)
880905	MTMCommunications
8809AF	Masimo Corporation
880F10	Huami Information Technology Co.,Ltd.
880FB6	Jabil Circuits India Pvt Ltd,-EHTP unit
881036	Panodic(ShenZhen) Electronics Limted
88124E	Qualcomm Inc.
88142B	Protonic Holland
881544	Cisco Meraki
8818AE	Tamron Co., Ltd
881B99	SHENZHEN XIN FEI JIA ELECTRONIC CO. LTD.
881DFC	Cisco Systems, Inc
881FA1	Apple, Inc.
882012	LMI Technologies
8821E3	Nebusens, S.L.
882364	Watchnet DVR Inc
8823FE	TTTech Computertechnik AG
88252C	Arcadyan Technology Corporation
882593	TP-LINK TECHNOLOGIES CO.,LTD.
8828B3	HUAWEI TECHNOLOGIES CO.,LTD
882950	Dalian Netmoon Tech Develop Co.,Ltd
882BD7	ADDÉNERGIE  TECHNOLOGIES
882E5A	Storone
88308A	Murata Manufacturing Co., Ltd.
88329B	SAMSUNG ELECTRO-MECHANICS(THAILAND)
883314	Texas Instruments
8833BE	Ivenix, Inc.
88354C	Transics
883612	SRC Computers, LLC
88366C	EFM Networks
883B8B	Cheering Connection Co. Ltd.
883C1C	MERCURY CORPORATION
883FD3	HUAWEI TECHNOLOGIES CO.,LTD
884157	Shenzhen Atsmart Technology Co.,Ltd.
8841C1	ORBISAT DA AMAZONIA IND E AEROL SA
8841FC	AirTies Wireless Networks
8843E1	Cisco Systems, Inc
884477	HUAWEI TECHNOLOGIES CO.,LTD
8844F6	Nokia Corporation
88462A	Telechips Inc.
884AEA	Texas Instruments
884B39	Siemens AG, Healthcare Sector
884CCF	Pulzze Systems, Inc
8850DD	Infiniband Trade Association
8851FB	Hewlett Packard
88532E	Intel Corporate
885395	Apple, Inc.
8853D4	HUAWEI TECHNOLOGIES CO.,LTD
88576D	XTA Electronics Ltd
8857EE	BUFFALO.INC
885A92	Cisco Systems, Inc
885BDD	Aerohive Networks Inc.
885C47	Alcatel Lucent
885D90	IEEE Registration Authority
88615A	Siano Mobile Silicon Ltd.
8863DF	Apple, Inc.
886639	HUAWEI TECHNOLOGIES CO.,LTD
8866A5	Apple, Inc.
88685C	Shenzhen ChuangDao & Perpetual Eternal Technology Co.,Ltd
886AB1	vivo Mobile Communication Co., Ltd.
886B0F	Bluegiga Technologies OY
886B44	Sunnovo International Limited
886B6E	Apple, Inc.
886B76	CHINA HOPEFUL GROUP HOPEFUL ELECTRIC CO.,LTD
887033	Hangzhou Silan Microelectronic Inc
88708C	Lenovo Mobile Communication Technology Ltd.
8870EF	SC Professional Trading Co., Ltd.
8871E5	Amazon Technologies Inc.
887384	Toshiba
887398	K2E Tekpoint
887556	Cisco Systems, Inc
887873	Intel Corporate
88789C	Game Technologies SA
88795B	Konka Group Co., Ltd.
88797E	Motorola Mobility LLC, a Lenovo Company
887F03	Comper Technology Investment Limited
888322	Samsung Electronics Co.,Ltd
888603	HUAWEI TECHNOLOGIES CO.,LTD
8886A0	Simton Technologies, Ltd.
888717	CANON INC.
8887DD	DarbeeVision Inc.
888914	All Components Incorporated
888964	GSI Electronics Inc.
888B5D	Storage Appliance Corporation
888C19	Brady Corp Asia Pacific Ltd
88908D	Cisco Systems, Inc
889166	Viewcooper Corp.
8891DD	Racktivity
889471	Brocade Communications Systems, Inc.
88947E	Fiberhome Telecommunication Technologies Co.,LTD
8894F9	Gemicom Technology, Inc.
8895B9	Unified Packet Systems Crop
889676	TTC MARCONI s.r.o.
8896B6	Global Fire Equipment S.A.
8896F2	Valeo Schalter und Sensoren GmbH
8897DF	Entrypass Corporation Sdn. Bhd.
889821	Teraon
889B39	Samsung Electronics Co.,Ltd
889CA6	BTB Korea INC
889FFA	Hon Hai Precision Ind. Co.,Ltd.
88A084	Formation Data Systems
88A25E	Juniper Networks
88A2D7	HUAWEI TECHNOLOGIES CO.,LTD
88A3CC	Amatis Controls
88A5BD	QPCOM INC.
88A6C6	Sagemcom Broadband SAS
88A73C	Ragentek Technology Group
88ACC1	Generiton Co., Ltd.
88AD43	PEGATRON CORPORATION
88ADD2	Samsung Electronics Co.,Ltd
88AE1D	COMPAL INFORMATION (KUNSHAN) CO., LTD.
88B168	Delta Control GmbH
88B1E1	Mojo Networks, Inc.
88B627	Gembird Europe BV
88B8D0	Dongguan Koppo Electronic Co.,Ltd
88BA7F	Qfiednet Co., Ltd.
88BFD5	Simple Audio Ltd
88C242	Poynt Co.
88C255	Texas Instruments
88C36E	Beijing Ereneben lnformation Technology Limited
88C3B3	Sovico
88C626	Logitech, Inc
88C663	Apple, Inc.
88C9D0	LG Electronics (Mobile Communications)
88CB87	Apple, Inc.
88CBA5	Suzhou Torchstar Intelligent Technology Co.,Ltd
88CC45	Skyworth Digital Technology(Shenzhen) Co.,Ltd
88CEFA	HUAWEI TECHNOLOGIES CO.,LTD
88CF98	HUAWEI TECHNOLOGIES CO.,LTD
88D274	zte corporation
88D37B	FirmTek, LLC
88D50C	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
88D7BC	DEP Company
88D962	Canopus Systems US LLC
88DC96	SENAO Networks, Inc.
88DD79	Voltaire
88DEA9	Roku, Inc.
88E0A0	Shenzhen VisionSTOR Technologies Co., Ltd
88E0F3	Juniper Networks
88E161	Art Beijing Science and Technology Development Co., Ltd.
88E3AB	HUAWEI TECHNOLOGIES CO.,LTD
88E603	Avotek corporation
88E628	Shenzhen Kezhonglong Optoelectronic Technology Co.,Ltd
88E712	Whirlpool Corporation
88E7A6	iKnowledge Integration Corp.
88E87F	Apple, Inc.
88E8F8	YONG TAI ELECTRONIC (DONGGUAN) LTD.
88E917	Tamaggo
88ED1C	Cudo Communication Co., Ltd.
88F031	Cisco Systems, Inc
88F077	Cisco Systems, Inc
88F488	cellon communications technology(shenzhen)Co.,Ltd.
88F490	Jetmobile Pte Ltd
88F7C7	Technicolor CH USA Inc.
88FD15	LINEEYE CO., LTD
88FED6	ShangHai WangYong Software Co., Ltd.
8C006D	Apple, Inc.
8C04FF	Technicolor CH USA Inc.
8C0551	Koubachi AG
8C078C	FLOW DATA INC
8C088B	Remote Solution
8C09F4	ARRIS Group, Inc.
8C0C90	Ruckus Wireless
8C0CA3	Amper
8C0D76	HUAWEI TECHNOLOGIES CO.,LTD
8C0EE3	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
8C10D4	Sagemcom Broadband SAS
8C11CB	ABUS Security-Center GmbH & Co. KG
8C18D9	Shenzhen RF Technology Co., Ltd
8C192D	IEEE Registration Authority
8C1ABF	Samsung Electronics Co.,Ltd
8C1F94	RF Surgical System Inc.
8C210A	TP-LINK TECHNOLOGIES CO.,LTD.
8C271D	QuantHouse
8C278A	Vocollect Inc
8C2937	Apple, Inc.
8C2DAA	Apple, Inc.
8C2F39	IBA Dosimetry GmbH
8C2FA6	Solid Optics B.V.
8C3330	EmFirst Co., Ltd.
8C3357	HiteVision Digital Media Technology Co.,Ltd.
8C34FD	HUAWEI TECHNOLOGIES CO.,LTD
8C3AE3	LG Electronics (Mobile Communications)
8C3C07	Skiva Technologies, Inc.
8C3C4A	NAKAYO Inc
8C41F2	RDA Technologies Ltd.
8C4435	Shanghai BroadMobi Communication Technology Co., Ltd.
8C4AEE	GIGA TMS INC
8C4B59	3D Imaging & Simulations Corp
8C4CDC	PLANEX COMMUNICATIONS INC.
8C4DB9	Unmonday Ltd
8C4DEA	Cerio Corporation
8C5105	Shenzhen ireadygo Information Technology CO.,LTD.
8C53F7	A&D ENGINEERING CO., LTD.
8C541D	Lge
8C569D	Imaging Solutions Group
8C56C5	Nintendo Co., Ltd.
8C579B	Wistron Neweb Corporation
8C57FD	LVX Western
8C5877	Apple, Inc.
8C598B	C Technologies AB
8C59C3	ADB Italia
8C5AF0	Exeltech Solar Products
8C5CA1	d-broad,INC
8C5D60	UCI Corporation Co.,Ltd.
8C5FDF	Beijing Railway Signal Factory
8C604F	Cisco Systems, Inc
8C60E7	MPGIO CO.,LTD
8C6102	Beijing Baofengmojing Technologies Co., Ltd
8C640B	Beyond Devices d.o.o.
8C6422	Sony Mobile Communications AB
8C6878	Nortek-AS
8C6AE4	Viogem Limited
8C6D50	SHENZHEN MTC CO LTD
8C705A	Intel Corporate
8C71F8	Samsung Electronics Co.,Ltd
8C736E	FUJITSU LIMITED
8C76C1	Goden Tech Limited
8C7712	Samsung Electronics Co.,Ltd
8C7716	LONGCHEER TELECOMMUNICATION LIMITED
8C78D7	SHENZHEN FAST TECHNOLOGIES CO.,LTD
8C7967	zte corporation
8C7B9D	Apple, Inc.
8C7C92	Apple, Inc.
8C7CB5	Hon Hai Precision Ind. Co.,Ltd.
8C7CFF	Brocade Communications Systems, Inc.
8C7EB3	Lytro, Inc.
8C7F3B	ARRIS Group, Inc.
8C82A8	Insigma Technology Co.,Ltd
8C8401	Private
8C873B	Leica Camera AG
8C897A	Augtek
8C89A5	Micro-Star INT'L CO., LTD
8C8A6E	ESTUN AUTOMATION TECHNOLOY CO., LTD
8C8ABB	Beijing Orient View Technology Co., Ltd.
8C8B83	Texas Instruments
8C8E76	taskit GmbH
8C8EF2	Apple, Inc.
8C8FE9	Apple, Inc.
8C90D3	Nokia
8C9109	Toyoshima Electric Technoeogy(Suzhou) Co.,Ltd.
8C9236	Aus.Linx Technology Co., Ltd.
8C9351	Jigowatts Inc.
8C94CF	Encell Technology, Inc.
8C99E6	TCT mobile ltd
8CA048	Beijing NeTopChip Technology Co.,LTD
8CA2FD	Starry, Inc.
8CA5A1	Oregano-               # Oregano Systems - Design & Consulting GmbH
8CA6DF	TP-LINK TECHNOLOGIES CO.,LTD.
8CA982	Intel Corporate
8CAB8E	Shanghai Feixun Communication Co.,Ltd.
8CAE4C	Plugable Technologies
8CAE89	Y-cam Solutions Ltd
8CB094	Airtech I&C Co., Ltd
8CB64F	Cisco Systems, Inc
8CB7F7	Shenzhen UniStrong Science & Technology Co., Ltd
8CB82C	IPitomy Communications
8CB864	AcSiP Technology Corp.
8CBEBE	Xiaomi Communications Co Ltd
8CBF9D	Shanghai Xinyou Information Technology Ltd. Co.
8CBFA6	Samsung Electronics Co.,Ltd
8CC121	Panasonic Corporation AVC Networks Company
8CC5E1	ShenZhen Konka Telecommunication Technology Co.,Ltd
8CC661	Current, powered by GE
8CC7AA	Radinet Communications Inc.
8CC7D0	zhejiang ebang communication co.,ltd
8CC8CD	Samsung Electronics Co.,Ltd
8CC8F4	IEEE Registration Authority
8CCDA2	ACTP, Inc.
8CCDE8	Nintendo Co., Ltd.
8CCF5C	BEFEGA GmbH
8CD17B	CG Mobile
8CD2E9	NIPPON SMT Co.Ltｄ
8CD3A2	VisSim AS
8CD628	Ikor Metering
8CDB25	ESG Solutions
8CDCD4	Hewlett Packard
8CDD8D	Wifly-City System Inc.
8CDE52	ISSC Technologies Corp.
8CDE99	Comlab Inc.
8CDF9D	NEC Corporation
8CE081	zte corporation
8CE117	zte corporation
8CE2DA	Circle Media Inc
8CE748	Private
8CE78C	DK Networks
8CE7B3	Sonardyne International Ltd
8CEA1B	Edgecore Networks Corporation
8CEBC6	HUAWEI TECHNOLOGIES CO.,LTD
8CEEC6	Precepscion Pty. Ltd.
8CF228	SHENZHEN MERCURY COMMUNICATION TECHNOLOGIES CO.,LTD.
8CF5A3	SAMSUNG ELECTRO-MECHANICS(THAILAND)
8CF813	ORANGE POLSKA
8CF945	Power Automation pte Ltd
8CF9C9	MESADA Technology Co.,Ltd.
8CFABA	Apple, Inc.
8CFDF0	Qualcomm Inc.
90004E	Hon Hai Precision Ind. Co.,Ltd.
9000DB	Samsung Electronics Co.,Ltd
90013B	Sagemcom Broadband SAS
90028A	Shenzhen Shidean Legrand Electronic Products Co.,Ltd
9002A9	Zhejiang Dahua Technology Co., Ltd.
900325	HUAWEI TECHNOLOGIES CO.,LTD
9003B7	PARROT SA
900628	Samsung Electronics Co.,Ltd
900917	Far-sighted mobile
900A39	Wiio, Inc.
900A3A	PSG Plastic Service GmbH
900BC1	Sprocomm Technologies CO.,Ltd
900CB4	Alinket Electronic Technology Co., Ltd
900D66	Digimore Electronics Co., Ltd
900DCB	ARRIS Group, Inc.
900E83	Monico Monitoring, Inc.
901711	Hagenuk Marinekommunikation GmbH
90179B	Nanomegas
9017AC	HUAWEI TECHNOLOGIES CO.,LTD
90185E	Apex Tool Group GmbH & Co OHG
90187C	SAMSUNG ELECTRO MECHANICS CO., LTD.
9018AE	Shanghai Meridian Technologies, Co. Ltd.
901900	SCS SA
901ACA	ARRIS Group, Inc.
901B0E	Fujitsu Technology Solutions GmbH
901D27	zte corporation
901EDD	GREAT COMPUTER CORPORATION
90203A	BYD Precision Manufacture Co.,Ltd
902083	General Engine Management Systems Ltd.
902106	BSkyB Ltd
902155	HTC Corporation
902181	Shanghai Huaqin Telecom Technology Co.,Ltd
9023EC	Availink, Inc.
9027E4	Apple, Inc.
902B34	GIGA-BYTE TECHNOLOGY CO.,LTD.
902CC7	C-MAX Asia Limited
902E1C	Intel Corporate
902E87	Labjack
9031CD	Onyx Healthcare Inc.
90342B	Gatekeeper Systems, Inc.
9034FC	Hon Hai Precision Ind. Co.,Ltd.
90356E	Vodafone Omnitel N.V.
903809	Ericsson AB
9038DF	Changzhou Tiannengbo System Co. Ltd.
903AA0	Nokia
903AE6	PARROT SA
903C92	Apple, Inc.
903CAE	Yunnan KSEC Digital Technology Co.,Ltd.
903D5A	Shenzhen Wision Technology Holding Limited
903D6B	Zicon Technology Corp.
903EAB	ARRIS Group, Inc.
904506	Tokyo Boeki Medisys Inc.
9046A2	Tedipay UK Ltd
9046B7	Vadaro Pte Ltd
904716	RORZE CORPORATION
90489A	Hon Hai Precision Ind. Co.,Ltd.
9049FA	Intel Corporate
904CE5	Hon Hai Precision Ind. Co.,Ltd.
904D4A	Sagemcom Broadband SAS
904E2B	HUAWEI TECHNOLOGIES CO.,LTD
90505A	unGlue, Inc
90507B	Advanced PANMOBIL Systems GmbH & Co. KG
90513F	Elettronica Santerno SpA
905446	TES ELECTRONIC SOLUTIONS
9055AE	Ericsson, EAB/RWI/K
905682	Lenbrook Industries Limited
905692	Autotalks Ltd.
9059AF	Texas Instruments
905C44	Compal Broadband Networks, Inc.
905F2E	TCT mobile ltd
905F8D	modas GmbH
9060F1	Apple, Inc.
90610C	Fida International (S) Pte Ltd
906717	Alphion India Private Limited
90671C	HUAWEI TECHNOLOGIES CO.,LTD
9067B5	Alcatel-               # Alcatel-Lucent
9067F3	Alcatel Lucent
9068C3	Motorola Mobility LLC, a Lenovo Company
906CAC	Fortinet, Inc.
906DC8	DLG Automação Industrial Ltda
906EBB	Hon Hai Precision Ind. Co.,Ltd.
906F18	Private
906FA9	NANJING PUTIAN TELECOMMUNICATIONS TECHNOLOGY CO.,LTD.
907025	Garea Microsys Co.,Ltd.
907065	Texas Instruments
907240	Apple, Inc.
907282	Sagemcom Broadband SAS
907841	Inter Corporate  
907990	Benchmark Electronics Romania SRL
907A0A	Gebr. Bode GmbH & Co KG
907A28	Beijing Morncloud Information And Technology Co. Ltd.
907AF1	Wally
907EBA	UTEK TECHNOLOGY (SHENZHEN) CO.,LTD
907F61	Chicony Electronics Co., Ltd.
908260	IEEE 1904.1 Working Group
90837A	General Electric Water & Process Technologies
90840D	Apple, Inc.
90842B	LEGO System A/S
908674	SICHUAN TIANYI COMHEART TELECOMCO., LTD
9088A2	IONICS TECHNOLOGY ME LTDA
908C09	Total Phase
908C44	H.K ZONGMU TECHNOLOGY CO., LTD.
908C63	GZ Weedong Networks Technology Co. , Ltd
908D1D	GH Technologies
908D6C	Apple, Inc.
908D78	D-Link International
908FCF	UNO System Co., Ltd
90903C	TRISON TECHNOLOGY CORPORATION
909060	RSI VIDEO TECHNOLOGIES
9092B4	Diehl BGT Defence GmbH & Co. KG
9094E4	D-Link International
9097D5	Espressif Inc.
909864	Impex-Sat GmbH&amp;Co KG
909916	ELVEES NeoTek OJSC
909DE0	Newland Design + Assoc. Inc.
909F33	EFM Networks
909F43	Accutron Instruments Inc.
90A210	United Telecoms Ltd
90A2DA	GHEO SA
90A46A	SISNET CO., LTD
90A4DE	Wistron Neweb Corporation
90A62F	Naver
90A783	JSW PACIFIC CORPORATION
90A7C1	Pakedge Device and Software Inc.
90AC3F	BrightSign LLC
90AE1B	TP-LINK TECHNOLOGIES CO.,LTD.
90B0ED	Apple, Inc.
90B11C	Dell Inc.
90B134	ARRIS Group, Inc.
90B21F	Apple, Inc.
90B686	Murata Manufacturing Co., Ltd.
90B8D0	Joyent, Inc.
90B931	Apple, Inc.
90B97D	Johnson Outdoors Marine Electronics d/b/a Minnkota
90C115	Sony Mobile Communications AB
90C1C6	Apple, Inc.
90C35F	Nanjing Jiahao Technology Co., Ltd.
90C682	IEEE Registration Authority
90C792	ARRIS Group, Inc.
90C7D8	zte corporation
90C99B	Recore Systems
90CC24	Synaptics, Inc
90CDB6	Hon Hai Precision Ind. Co.,Ltd.
90CF15	Nokia Corporation
90CF6F	Dlogixs Co Ltd
90CF7D	Qingdao Hisense Communications Co.,Ltd.
90D11B	Palomar Medical Technologies
90D74F	Bookeen
90D7BE	Wavelab Global Inc.
90D7EB	Texas Instruments
90D852	Comtec Co., Ltd.
90D8F3	zte corporation
90D92C	HUG-WITSCHI AG
90DA4E	Avanu
90DA6A	FOCUS H&S Co., Ltd.
90DB46	E-LEAD ELECTRONIC CO., LTD
90DFB7	s.m.s smart microwave sensors GmbH
90DFFB	HOMERIDER SYSTEMS
90E0F0	IEEE 1722a Working Group
90E2BA	Intel Corporate
90E6BA	ASUSTek COMPUTER INC.
90E7C4	HTC Corporation
90EA60	SPI Lasers Ltd
90EED9	UNIVERSAL DE DESARROLLOS ELECTRÓNICOS, SA
90EF68	ZyXEL Communications Corporation
90F052	MEIZU Technology Co., Ltd.
90F1AA	Samsung Electronics Co.,Ltd
90F1B0	Hangzhou Anheng Info&Tech CO.,LTD
90F278	Radius Gateway
90F305	HUMAX Co., Ltd.
90F3B7	Kirisun Communications Co., Ltd.
90F4C1	Rand McNally
90F652	TP-LINK TECHNOLOGIES CO.,LTD.
90F72F	Phillips Machine & Welding Co., Inc.
90FB5B	Avaya Inc
90FBA6	Hon Hai Precision Ind. Co.,Ltd.
90FD61	Apple, Inc.
90FF79	Metro Ethernet Forum
940070	Nokia Corporation
940149	AutoHotBox
9401C2	Samsung Electronics Co.,Ltd
94049C	HUAWEI TECHNOLOGIES CO.,LTD
9405B6	Liling FullRiver Electronics & Technology Ltd
940937	HUMAX Co., Ltd.
940B2D	NetView Technologies(Shenzhen) Co., Ltd
940BD5	Himax Technologies, Inc
940C6D	TP-LINK TECHNOLOGIES CO.,LTD.
94103E	Belkin International Inc.
9411DA	ITF Fröschl GmbH
941673	Point Core SARL
941882	Hewlett Packard Enterprise
941D1C	TLab West Systems AB
942053	Nokia Corporation
942197	Stalmart Technology Limited
94236E	Shenzhen Junlan Electronic Ltd
942CB3	HUMAX Co., Ltd.
942E17	Schneider Electric Canada Inc
942E63	Finsécur
94319B	Alphatronics BV
9433DD	Taco Inc
94350A	Samsung Electronics Co.,Ltd
9436E0	Sichuan Bihong Broadcast &amp; Television New Technologies Co.,Ltd
9439E5	Hon Hai Precision Ind. Co.,Ltd.
943AF0	Nokia Corporation
943BB1	Kaonmedia CO., LTD.
943DC9	Asahi Net, Inc.
9440A2	Anywave Communication Technologies, Inc.
944444	LG Innotek
944452	Belkin International Inc.
944696	BaudTec Corporation
944A09	BitWise Controls
944A0C	Sercomm Corporation
945047	Rechnerbetriebsgruppe
945089	SimonsVoss Technologies GmbH
945103	Samsung Electronics Co.,Ltd
94513D	iSmart Alarm, Inc.
9451BF	Hyundai ESG
945330	Hon Hai Precision Ind. Co.,Ltd.
945493	Rigado, LLC
9457A5	Hewlett Packard
945907	Shanghai HITE-BELDEN Network Technology Co., Ltd.
94592D	EKE Building Technology Systems Ltd
945B7E	TRILOBIT LTDA.
94611E	Wata Electronics Co.,Ltd.
946124	Pason Systems
946269	ARRIS Group, Inc.
9463D1	Samsung Electronics Co.,Ltd
94652D	OnePlus Technology (Shenzhen) Co., Ltd
94659C	Intel Corporate
9466E7	WOM Engineering
9470D2	WINFIRM TECHNOLOGY
9471AC	TCT mobile ltd
94756E	QinetiQ North America
9476B7	Samsung Electronics Co.,Ltd
94772B	HUAWEI TECHNOLOGIES CO.,LTD
947C3E	Polewall Norge AS
9481A4	Azuray Technologies
94857A	Evantage Industries Corp
9486CD	SEOUL ELECTRONICS&TELECOM
9486D4	Surveillance Pro Corporation
94877C	ARRIS Group, Inc.
948815	Infinique Worldwide Inc
948854	Texas Instruments
94885E	Surfilter Network Technology Co., Ltd.
948B03	EAGET Innovation and Technology Co., Ltd.
948BC1	Samsung Electronics Co.,Ltd
948D50	Beamex Oy Ab
948E89	INDUSTRIAS UNIDAS SA DE CV
948FEE	Verizon Telematics
9492BC	SYNTECH(HK) TECHNOLOGY LIMITED
949426	Apple, Inc.
9495A0	Google, Inc.
9498A2	Shanghai LISTEN TECH.LTD
949901	Shenzhen YITOA Digital Appliance CO.,LTD
949AA9	Microsoft Corporation
949BFD	Trans New Technology, Inc.
949C55	Alta Data Technologies
949F3E	Sonos, Inc.
949F3F	Optek Digital Technology company limited
949FB4	ChengDu JiaFaAnTai Technology Co.,Ltd
94A04E	Bostex Technology Co., LTD
94A1A2	AMPAK Technology, Inc.
94A7B7	zte corporation
94A7BC	BodyMedia, Inc.
94AAB8	Joview(Beijing) Technology Co. Ltd.
94ABDE	OMX Technology - FZE
94ACCA	trivum technologies GmbH
94AE61	Alcatel Lucent
94AEE3	Belden Hirschmann Industries (Suzhou) Ltd.
94B10A	Samsung Electronics Co.,Ltd
94B2CC	PIONEER CORPORATION
94B40F	Aruba Networks
94B819	Nokia
94B8C5	RuggedCom Inc.
94B9B4	Aptos Technology
94BA31	Visiontec da Amazônia Ltda.
94BA56	Shenzhen Coship Electronics Co., Ltd.
94BBAE	Husqvarna AB
94BF1E	eflow Inc. / Smart Device Planning and Development Division
94BF95	Shenzhen Coship Electronics Co., Ltd
94C014	Sorter Sp. j. Konrad Grzeszczyk MichaA, Ziomek
94C038	Tallac Networks
94C150	2Wire Inc
94C3E4	SCA Schucker Gmbh & Co KG
94C4E9	PowerLayer Microsystems HongKong Limited
94C6EB	NOVA electronics, Inc.
94C7AF	Raylios Technology
94C960	Zhongshan B&T technology.co.,ltd
94C962	Teseq AG
94CA0F	Honeywell Analytics
94CCB9	ARRIS Group, Inc.
94CDAC	Creowave Oy
94CE2C	Sony Mobile Communications AB
94CE31	CTS Limited
94D019	Cydle Corp.
94D417	GPI KOREA INC.
94D469	Cisco Systems, Inc
94D60E	shenzhen yunmao information technologies co., ltd
94D723	Shanghai DareGlobal Technologies Co.,Ltd
94D771	Samsung Electronics Co.,Ltd
94D859	TCT mobile ltd
94D93C	Enelps
94DB49	Sitcorp
94DBC9	AzureWave Technology Inc.
94DBDA	HUAWEI TECHNOLOGIES CO.,LTD
94DD3F	A+V Link Technologies, Corp.
94DE0E	SmartOptics AS
94DE80	GIGA-BYTE TECHNOLOGY CO.,LTD.
94DF4E	Wistron InfoComm(Kunshan)Co.,Ltd.
94DF58	IJ Electron CO.,Ltd.
94E0D0	HealthStream Taiwan Inc.
94E226	D. ORtiz Consulting, LLC
94E2FD	Boge Kompressoren OTTO Boge GmbH & Co. KG
94E711	Xirka Dama Persada PT
94E848	FYLDE MICRO LTD
94E8C5	ARRIS Group, Inc.
94E96A	Apple, Inc.
94E979	Liteon Technology Corporation
94E98C	Nokia
94EB2C	Google, Inc.
94EBCD	BlackBerry RTS
94F19E	HUIZHOU MAORONG INTELLIGENT TECHNOLOGY CO.,LTD
94F278	Elma Electronic
94F551	Cadi Scientific Pte Ltd
94F665	Ruckus Wireless
94F692	Geminico co.,Ltd.
94F6A3	Apple, Inc.
94F720	Tianjin Deviser Electronics Instrument Co., Ltd
94FAE8	Shenzhen Eycom Technology Co., Ltd
94FB29	Zebra Technologies Inc.
94FBB2	Shenzhen Gongjin Electronics Co.,Ltd
94FD1D	WhereWhen Corp
94FD2E	Shanghai Uniscope Technologies Co.,Ltd
94FE22	HUAWEI TECHNOLOGIES CO.,LTD
94FEF4	Sagemcom Broadband SAS
9800C1	GuangZhou CREATOR Technology Co.,Ltd.(CHINA)
9801A7	Apple, Inc.
980284	Theobroma Systems GmbH
9802D8	IEEE Registration Authority
9803A0	ABB n.v. Power Quality Products
9803D8	Apple, Inc.
98072D	Texas Instruments
980C82	SAMSUNG ELECTRO MECHANICS CO., LTD.
980CA5	Motorola (Wuhan) Mobility Technologies Communication Co., Ltd.
980D2E	HTC Corporation
980EE4	Private
981094	Shenzhen Vsun communication technology Co.,ltd
9810E8	Apple, Inc.
981333	zte corporation
9816EC	IC Intracom
981DFA	Samsung Electronics Co.,Ltd
981E0F	Jeelan (Shanghai Jeelan Technology Information Inc
981FB1	Shenzhen Lemon Network Technology Co.,Ltd
98208E	Definium Technologies
98234E	Micromedia AG
98262A	Applied Research Associates, Inc
98291D	Jaguar de Mexico, SA de CV
98293F	Fujian Start Computer Equipment Co.,Ltd
982CBE	2Wire Inc
982D56	Resolution Audio
982DBA	Fibergate Inc.
982F3C	Sichuan Changhong Electric Ltd.
983000	Beijing KEMACOM Technologies Co., Ltd.
983071	DAIKYUNG VASCOM
98349D	Krauss Maffei Technologies GmbH
983571	Sub10 Systems Ltd
9835B8	Assembled Products Corporation
983713	PT.Navicom Indonesia
98398E	Samsung Electronics Co.,Ltd
983B16	AMPAK Technology, Inc.
983F9F	China SSJ (Suzhou) Network Technology Inc.
9840BB	Dell Inc.
984246	SOL INDUSTRY PTE., LTD
9843DA	INTERTECH
98473C	SHANGHAI SUNMON COMMUNICATION TECHNOGY CO.,LTD
984A47	CHG Hospital Beds
984B4A	ARRIS Group, Inc.
984BE1	Hewlett Packard
984C04	Zhangzhou Keneng Electrical Equipment Co Ltd
984CD3	Mantis Deposition
984E97	Starlight Marketing (H. K.) Ltd.
984FEE	Intel Corporate
9852B1	Samsung Electronics Co.,Ltd
98541B	Intel Corporate
9857D3	HON HAI-CCPBG  PRECISION IND.CO.,LTD.
98588A	SYSGRATION Ltd.
985945	Texas Instruments
985AEB	Apple, Inc.
985BB0	KMDATA INC.
985C93	SBG Systems SAS
985D46	PeopleNet Communication
985DAD	Texas Instruments
985E1B	ConversDigital Co., Ltd.
985FD3	Microsoft Corporation
986022	EMW Co., Ltd.
9866EA	Industrial Control Communications, Inc.
986B3D	ARRIS Group, Inc.
986C5C	Jiangxi Gosun Guard Security Co.,Ltd
986CF5	zte corporation
986D35	IEEE Registration Authority
986DC8	TOSHIBA MITSUBISHI-ELECTRIC INDUSTRIAL SYSTEMS CORPORATION
9870E8	INNATECH SDN BHD
9873C4	Sage Electronic Engineering LLC
98743D	Shenzhen Jun Kai Hengye Technology Co. Ltd
9874DA	Infinix mobility limited
9876B6	Adafruit
987770	Pep Digital Technology (Guangzhou) Co., Ltd
987BF3	Texas Instruments
987E46	Emizon Networks Limited
988217	Disruptive Ltd
988389	Samsung Electronics Co.,Ltd
9884E3	Texas Instruments
9886B1	Flyaudio corporation (China)
988744	Wuxi Hongda Science and Technology Co.,LTD
9889ED	Anadem Information Inc.
988B5D	Sagemcom Broadband SAS
988BAD	Corintech Ltd.
988E34	ZHEJIANG BOXSAM ELECTRONIC CO.,LTD
988E4A	NOXUS(BEIJING) TECHNOLOGY CO.,LTD
988EDD	TE Connectivity Limerick
989080	Linkpower Network System Inc Ltd.
989096	Dell Inc.
9893CC	LG ELECTRONICS INC
989449	Skyworth Wireless Technology Ltd.
9897D1	MitraStar Technology Corp.
989E63	Apple, Inc.
98A40E	Snap, Inc.
98A7B0	MCST ZAO
98AA3C	Will i-tech Co., Ltd.
98AAD7	BLUE WAVE NETWORKING CO LTD
98AAFC	IEEE Registration Authority
98B039	Nokia
98B6E9	Nintendo Co.,Ltd
98B8E3	Apple, Inc.
98BB1E	BYD Precision Manufacture Company Ltd.
98BC57	SVA TECHNOLOGIES CO.LTD
98BC99	Edeltech Co.,Ltd.
98BE94	Ibm
98C0EB	Global Regency Ltd
98C845	PacketAccess
98CB27	Galore Networks Pvt. Ltd.
98CDB4	Virident Systems, Inc.
98CF53	BBK EDUCATIONAL ELECTRONICS CORP.,LTD.
98D293	Google, Inc.
98D331	Shenzhen Bolutek Technology Co.,Ltd.
98D3D2	MEKRA Lang GmbH & Co. KG
98D686	Chyi Lee industry Co., ltd.
98D6BB	Apple, Inc.
98D6F7	LG Electronics (Mobile Communications)
98D88C	Nortel Networks
98DA92	Vuzix Corporation
98DCD9	UNITEC Co., Ltd.
98DDEA	Infinix mobility limited
98DED0	TP-LINK TECHNOLOGIES CO.,LTD.
98E0D9	Apple, Inc.
98E165	Accutome
98E476	Zentan
98E79A	Foxconn(NanJing) Communication Co.,Ltd.
98E7F4	Hewlett Packard
98E7F5	HUAWEI TECHNOLOGIES CO.,LTD
98E848	Axiim
98EC65	Cosesy ApS
98EECB	Wistron Infocomm (Zhongshan) Corporation
98F058	Lynxspring, Incl.
98F0AB	Apple, Inc.
98F170	Murata Manufacturing Co., Ltd.
98F199	NEC Platforms, Ltd.
98F428	zte corporation
98F537	zte corporation
98F5A9	OHSUNG ELECTRONICS CO.,LTD.
98F8C1	IDT Technology Limited
98F8DB	Marini Impianti Industriali s.r.l.
98FAE3	Xiaomi Communications Co Ltd
98FB12	Grand Electronics (HK) Ltd
98FC11	Cisco-Linksys, LLC
98FD74	ACT.CO.LTD
98FDB4	Primax Electronics Ltd.
98FE03	Ericsson - North America
98FE94	Apple, Inc.
98FF6A	OTEC(Shanghai)Technology Co.,Ltd.
98FFD0	Lenovo Mobile Communication Technology Ltd.
9C0111	Shenzhen Newabel Electronic Co., Ltd.
9C0298	Samsung Electronics Co.,Ltd
9C039E	Beijing Winchannel Software Technology Co., Ltd
9C0473	Tecmobile (International) Ltd.
9C04EB	Apple, Inc.
9C061B	Hangzhou H3C Technologies Co., Limited
9C066E	Hytera Communications Corporation Limited
9C0DAC	Tymphany HK Limited
9C0E4A	Shenzhen Vastking Electronic Co.,Ltd.
9C13AB	Chanson Water Co., Ltd.
9C1465	Edata Elektronik San. ve Tic. A.Ş.
9C1874	Nokia Danmark A/S
9C1C12	Aruba Networks
9C1D58	Texas Instruments
9C1E95	Actiontec Electronics, Inc
9C1FDD	Accupix Inc.
9C207B	Apple, Inc.
9C216A	TP-LINK TECHNOLOGIES CO.,LTD.
9C220E	TASCAN Systems GmbH
9C2840	Discovery Technology,LTD..
9C28BF	Continental Automotive Czech Republic s.r.o.
9C28EF	HUAWEI TECHNOLOGIES CO.,LTD
9C293F	Apple, Inc.
9C2A70	Hon Hai Precision Ind. Co.,Ltd.
9C2A83	Samsung Electronics Co.,Ltd
9C3066	RWE Effizienz GmbH
9C3178	Foshan Huadian Intelligent Communications Teachnologies Co.,Ltd
9C31B6	Kulite Semiconductor Products Inc
9C32A9	SICHUAN TIANYI COMHEART TELECOMCO., LTD
9C3426	ARRIS Group, Inc.
9C3583	Nipro Diagnostics, Inc
9C35EB	Apple, Inc.
9C37F4	HUAWEI TECHNOLOGIES CO.,LTD
9C3AAF	Samsung Electronics Co.,Ltd
9C3DCF	Netgear
9C3EAA	EnvyLogic Co.,Ltd.
9C417C	Hame  Technology Co.,  Limited
9C443D	CHENGDU XUGUANG TECHNOLOGY CO, LTD
9C44A6	SwiftTest, Inc.
9C4563	DIMEP Sistemas
9C4A7B	Nokia Corporation
9C4CAE	Mesa Labs
9C4E20	Cisco Systems, Inc
9C4E36	Intel Corporate
9C4E8E	ALT Systems Ltd
9C4EBF	Boxcast
9C4FDA	Apple, Inc.
9C50EE	Cambridge Industries(Group) Co.,Ltd.
9C52F8	HUAWEI TECHNOLOGIES CO.,LTD
9C53CD	ENGICAM s.r.l.
9C541C	Shenzhen My-power Technology Co.,Ltd
9C54CA	Zhengzhou VCOM Science and Technology Co.,Ltd
9C55B4	I.S.E. S.r.l.
9C5711	Feitian Xunda(Beijing) Aeronautical Information Technology Co., Ltd.
9C57AD	Cisco Systems, Inc
9C5B96	NMR Corporation
9C5C8D	FIREMAX INDÚSTRIA E COMÉRCIO DE PRODUTOS ELETRÔNICOS  LTDA
9C5C8E	ASUSTek COMPUTER INC.
9C5CF9	Sony Mobile Communications AB
9C5D12	Aerohive Networks Inc.
9C5D95	VTC Electronics Corp.
9C5E73	Calibre UK LTD
9C611D	Omni-ID USA, Inc.
9C6121	SICHUAN TIANYI COMHEART TELECOMCO.,LTD
9C62AB	Sumavision Technologies Co.,Ltd
9C645E	Harman Consumer Group
9C65B0	Samsung Electronics Co.,Ltd
9C65F9	AcSiP Technology Corp.
9C6650	Glodio Technolies Co.,Ltd Tianjin Branch
9C685B	Octonion SA
9C6ABE	QEES ApS.
9C6C15	Microsoft Corporation
9C741A	HUAWEI TECHNOLOGIES CO.,LTD
9C7514	Wildix srl
9C77AA	Nadasnv
9C79AC	Suntec Software(Shanghai) Co., Ltd.
9C7A03	Ciena Corporation
9C7BD2	NEOLAB Convergence
9C7DA3	HUAWEI TECHNOLOGIES CO.,LTD
9C807D	SYSCABLE Korea Inc.
9C80DF	Arcadyan Technology Corporation
9C83BF	PRO-VISION, Inc.
9C84BF	Apple, Inc.
9C86DA	Phoenix Geophysics Ltd.
9C8888	Simac Techniek NV
9C88AD	Fiberhome Telecommunication Technologies Co.,LTD
9C8BA0	Apple, Inc.
9C8BF1	The Warehouse Limited
9C8D1A	INTEG process group inc
9C8D7C	ALPS ELECTRIC CO.,LTD.
9C8DD3	Leonton Technologies
9C8E99	Hewlett Packard
9C8ECD	Amcrest Technologies
9C8EDC	Teracom Limited
9C934E	Xerox Corporation
9C93E4	Private
9C95F8	SmartDoor Systems, LLC
9C9726	Technicolor
9C9811	Guangzhou Sunrise Electronics Development Co., Ltd
9C99A0	Xiaomi Communications Co Ltd
9C9C1D	Starkey Labs Inc.
9C9D5D	Raden Inc
9CA10A	SCLE SFE
9CA134	Nike, Inc.
9CA3A9	Guangzhou Juan Optical and Electronical Tech Joint Stock Co., Ltd
9CA3BA	SAKURA Internet Inc.
9CA577	Osorno Enterprises Inc.
9CA5C0	vivo Mobile Communication Co., Ltd.
9CA69D	Whaley Technology Co.Ltd
9CA9E4	zte corporation
9CAC6D	Universal Electronics, Inc.
9CAD97	Hon Hai Precision Ind. Co.,Ltd.
9CADEF	Obihai Technology, Inc.
9CAED3	Seiko Epson Corporation
9CAF6F	ITEL MOBILE LIMITED
9CAFCA	Cisco Systems, Inc
9CB008	Ubiquitous Computing Technology Corporation
9CB206	PROCENTEC
9CB2B2	HUAWEI TECHNOLOGIES CO.,LTD
9CB654	Hewlett Packard
9CB6D0	Rivet Networks
9CB70D	Liteon Technology Corporation
9CB793	Creatcomm Technology Inc.
9CBB98	Shen Zhen RND Electronic Co.,LTD
9CBD9D	SkyDisk, Inc.
9CBEE0	Biosoundlab Co., Ltd.
9CC077	PrintCounts, LLC
9CC0D2	Conductix-Wampfler GmbH
9CC172	HUAWEI TECHNOLOGIES CO.,LTD
9CC7A6	AVM GmbH
9CC7D1	SHARP Corporation
9CC8AE	Becton, Dickinson  and Company
9CCAD9	Nokia Corporation
9CCC83	Juniper Networks
9CCD82	CHENG UEI PRECISION INDUSTRY CO.,LTD
9CD21E	Hon Hai Precision Ind. Co.,Ltd.
9CD24B	zte corporation
9CD332	PLC Technology Ltd
9CD35B	Samsung Electronics Co.,Ltd
9CD36D	Netgear
9CD48B	Innolux Technology Europe BV
9CD643	D-Link International
9CD917	Motorola Mobility LLC, a Lenovo Company
9CD9CB	Lesira Manufacturing Pty Ltd
9CDA3E	Intel Corporate
9CDC71	Hewlett Packard Enterprise
9CDD1F	Intelligent Steward Co.,Ltd
9CDF03	Harman/Becker Automotive Systems GmbH
9CDFB1	Shenzhen Crave Communication Co., LTD
9CE10E	NCTech Ltd
9CE1D6	Junger Audio-Studiotechnik GmbH
9CE230	JULONG CO,.LTD.
9CE374	HUAWEI TECHNOLOGIES CO.,LTD
9CE635	Nintendo Co., Ltd.
9CE6E7	Samsung Electronics Co.,Ltd
9CE7BD	Winduskorea co., Ltd
9CE951	Shenzhen Sang Fei Consumer Communications Ltd., Co.
9CEBE8	BizLink (Kunshan) Co.,Ltd
9CEFD5	Panda Wireless, Inc.
9CF387	Apple, Inc.
9CF48E	Apple, Inc.
9CF61A	UTC Fire and Security
9CF67D	Ricardo Prague, s.r.o.
9CF8DB	shenzhen eyunmei technology co,.ltd
9CF938	AREVA NP GmbH
9CFBD5	vivo Mobile Communication Co., Ltd.
9CFBF1	MESOMATIC GmbH & Co.KG
9CFC01	Apple, Inc.
9CFCD1	Aetheris Technology (Shanghai) Co., Ltd.
9CFFBE	OTSL Inc.
A002DC	Amazon Technologies Inc.
A00363	Robert Bosch Healthcare GmbH
A0043E	Parker Hannifin Manufacturing Germany GmbH & Co. KG
A00460	Netgear
A00627	NEXPA System
A00798	Samsung Electronics Co.,Ltd
A007B6	Advanced Technical Support, Inc.
A0086F	HUAWEI TECHNOLOGIES CO.,LTD
A009ED	Avaya Inc
A00ABF	Wieson Technologies Co., Ltd.
A00BBA	SAMSUNG ELECTRO MECHANICS CO., LTD.
A00CA1	SKTB SKiT
A01081	Samsung Electronics Co.,Ltd
A01290	Avaya Inc
A012DB	TABUCHI ELECTRIC CO.,LTD
A0133B	HiTi Digital, Inc.
A013CB	Fiberhome Telecommunication Technologies Co.,LTD
A0143D	PARROT SA
A0165C	Triteka LTD
A01828	Apple, Inc.
A01859	Shenzhen Yidashi Electronics Co Ltd
A01917	Bertel S.p.a.
A01B29	Sagemcom Broadband SAS
A01C05	NIMAX TELECOM CO.,LTD.
A01D48	Hewlett Packard
A01E0B	MINIX Technology Limited
A020A6	Espressif Inc.
A02195	Samsung Electronics Co.,Ltd
A021B7	Netgear
A0231B	TeleComp R&D Corp.
A02BB8	Hewlett Packard
A02C36	FN-LINK TECHNOLOGY LIMITED
A02EF3	United Integrated Services Co., Led.
A03299	Lenovo (Beijing) Co., Ltd.
A0369F	Intel Corporate
A036F0	Comprehensive Power
A036FA	Ettus Research LLC
A039F7	LG Electronics (Mobile Communications)
A03A75	PSS Belgium N.V.
A03B1B	Inspire Tech
A03BE3	Apple, Inc.
A03D6F	Cisco Systems, Inc
A03E6B	IEEE Registration Authority
A04025	Actioncable, Inc.
A04041	SAMWONFA Co.,Ltd.
A040A0	Netgear
A0415E	Opsens Solution Inc.
A041A7	NL Ministry of Defense
A0423F	Tyan Computer Corp
A043DB	Sitael S.p.A.
A0481C	Hewlett Packard
A04C5B	Shenzhen TINNO Mobile Technology Corp.
A04CC1	Helixtech Corp.
A04E01	CENTRAL ENGINEERING co.,ltd.
A04E04	Nokia Corporation
A04FD4	ADB Broadband Italia
A051C6	Avaya Inc
A0554F	Cisco Systems, Inc
A055DE	ARRIS Group, Inc.
A056B2	Harman/Becker Automotive Systems GmbH
A0593A	V.D.S. Video Display Systems srl
A05AA4	Grand Products Nevada, Inc.
A05B21	ENVINET GmbH
A05DC1	TMCT Co., LTD.
A05DE7	DIRECTV, Inc.
A05E6B	MELPER Co., Ltd.
A06090	Samsung Electronics Co.,Ltd
A06391	Netgear
A06518	VNPT TECHNOLOGY
A067BE	Sicon srl
A06986	Wellav Technologies Ltd
A06A00	Verilink Corporation
A06CEC	Rim
A06D09	Intelcan Technosystems Inc.
A06E50	Nanotek Elektronik Sistemler Ltd. Sti.
A06FAA	LG Innotek
A071A9	Nokia Corporation
A0722C	HUMAX Co., Ltd.
A07332	Cashmaster International Limited
A073FC	Rancore Technologies Private Limited
A07591	Samsung Electronics Co.,Ltd
A07771	Vialis BV
A078BA	Pantech Co., Ltd.
A0821F	Samsung Electronics Co.,Ltd
A082AC	Linear DMS Solutions Sdn. Bhd.
A082C7	P.T.I Co.,LTD
A084CB	SonicSensory,Inc.
A0861D	Chengdu Fuhuaxin Technology co.,Ltd
A086C6	Xiaomi Communications Co Ltd
A086EC	SAEHAN HITEC Co., Ltd
A08869	Intel Corporate
A088B4	Intel Corporate
A089E4	Skyworth Digital Technology(Shenzhen) Co.,Ltd
A08A87	HuiZhou KaiYue Electronic Co.,Ltd
A08C15	Gerhard D. Wempe KG
A08C9B	Xtreme Technologies Corp
A08CF8	HUAWEI TECHNOLOGIES CO.,LTD
A08CFD	Hewlett Packard
A08D16	HUAWEI TECHNOLOGIES CO.,LTD
A08E78	Sagemcom Broadband SAS
A090DE	VEEDIMS,LLC
A09169	LG Electronics (Mobile Communications)
A091C8	zte corporation
A09347	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
A09805	OpenVox Communication Co Ltd
A098ED	Shandong Intelligent Optical Communication Development Co., Ltd.
A0999B	Apple, Inc.
A09A5A	Time Domain
A09BBD	Total Aviation Solutions Pty Ltd
A09D91	SoundBridge
A09E1A	Polar Electro Oy
A0A130	DLI Taiwan Branch office
A0A23C	Gpms
A0A33B	HUAWEI TECHNOLOGIES CO.,LTD
A0A3E2	Actiontec Electronics, Inc
A0A65C	Supercomputing Systems AG
A0A763	Polytron Vertrieb GmbH
A0A8CD	Intel Corporate
A0AAFD	EraThink Technologies Corp.
A0AB1B	D-Link International
A0ADA1	JMR Electronics, Inc
A0B100	ShenZhen Cando Electronics Co.,Ltd
A0B3CC	Hewlett Packard
A0B437	GD Mission Systems
A0B4A5	Samsung Electronics Co.,Ltd
A0B5DA	HongKong THTF Co., Ltd
A0B662	Acutvista Innovation Co., Ltd.
A0B8F8	Amgen U.S.A. Inc.
A0B9ED	Skytap
A0BAB8	Pixon Imaging
A0BB3E	IEEE Registration Authority
A0BF50	S.C. ADD-PRODUCTION S.R.L.
A0BFA5	Coresys
A0C2DE	Costar Video Systems
A0C3DE	Triton Electronic Systems Ltd.
A0C4A5	SYGN HOUSE CO.,LTD
A0C562	ARRIS Group, Inc.
A0C589	Intel Corporate
A0C6EC	ShenZhen ANYK Technology Co.,LTD
A0CBFD	Samsung Electronics Co.,Ltd
A0CC2B	Murata Manufacturing Co., Ltd.
A0CEC8	CE LINK LIMITED
A0CF5B	Cisco Systems, Inc
A0D12A	AXPRO Technology Inc.
A0D37A	Intel Corporate
A0D385	AUMA Riester GmbH & Co. KG
A0D3C1	Hewlett Packard
A0D795	Apple, Inc.
A0DA92	Nanjing Glarun Atten Technology Co. Ltd.
A0DC04	Becker-Antriebe GmbH
A0DD97	PolarLink Technologies, Ltd
A0DDE5	SHARP Corporation
A0DE05	JSC Irbis-T
A0E0AF	Cisco Systems, Inc
A0E201	AVTrace Ltd.(China)
A0E25A	Amicus SK, s.r.o.
A0E295	DAT System Co.,Ltd
A0E453	Sony Mobile Communications AB
A0E4CB	ZyXEL Communications Corporation
A0E534	Stratec Biomedical AG
A0E5E9	enimai Inc
A0E6F8	Texas Instruments
A0E9DB	Ningbo FreeWings Technologies Co.,Ltd
A0EB76	AirCUVE Inc.
A0EC80	zte corporation
A0ECF9	Cisco Systems, Inc
A0EDCD	Apple, Inc.
A0EF84	Seine Image Int'l Co., Ltd
A0F217	GE Medical System(China) Co., Ltd.
A0F3C1	TP-LINK TECHNOLOGIES CO.,LTD.
A0F3E4	Alcatel-               # Alcatel-Lucent IPD
A0F419	Nokia Corporation
A0F450	HTC Corporation
A0F459	FN-LINK TECHNOLOGY LIMITED
A0F479	HUAWEI TECHNOLOGIES CO.,LTD
A0F6FD	Texas Instruments
A0F849	Cisco Systems, Inc
A0F895	Shenzhen TINNO Mobile Technology Corp.
A0F9E0	VIVATEL COMPANY LIMITED
A0FC6E	Telegrafia a.s.
A0FE91	AVAT Automation GmbH
A40130	ABIsystems Co., LTD
A402B9	Intel Corporate
A4059E	STA Infinity LLP
A408EA	Murata Manufacturing Co., Ltd.
A408F5	Sagemcom Broadband SAS
A409CB	Alfred Kaercher GmbH &amp; Co KG
A40BED	Carry Technology Co.,Ltd
A40CC3	Cisco Systems, Inc
A40DBC	Xiamen Intretech Inc.
A41163	IEEE Registration Authority
A41242	NEC Platforms, Ltd.
A4134E	Luxul
A41437	Hangzhou Hikvision Digital Technology Co.,Ltd.
A41566	Wei Fang Goertek Electronics Co.,Ltd
A41588	ARRIS Group, Inc.
A41731	Hon Hai Precision Ind. Co.,Ltd.
A41875	Cisco Systems, Inc
A41BC0	Fastec Imaging Corporation
A41F72	Dell Inc.
A4218A	Nortel Networks
A42305	Open Networking Laboratory
A424B3	FlatFrog Laboratories AB
A424DD	Cambrionix Ltd
A4251B	Avaya Inc
A42940	Shenzhen YOUHUA Technology Co., Ltd
A42983	Boeing Defence Australia
A429B7	Bluesky
A42B8C	Netgear
A42BB0	TP-LINK TECHNOLOGIES CO.,LTD.
A42C08	Masterwork Automodules
A43111	Ziv
A43135	Apple, Inc.
A433D1	Fibrlink Communications Co.,Ltd.
A434D9	Intel Corporate
A43831	RF elements s.r.o.
A438FC	Plastic Logic
A43A69	Vers Inc
A43BFA	IEEE Registration Authority
A43D78	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
A444D1	Wingtech Group (HongKong）Limited
A4466B	EOC Technology
A446FA	AmTRAN Video Corporation
A44AD3	ST Electronics(Shanghai) Co.,Ltd
A44B15	Sun Cupid Technology (HK) LTD
A44C11	Cisco Systems, Inc
A44E2D	Adaptive Wireless Solutions, LLC
A44E31	Intel Corporate
A44F29	IEEE Registration Authority
A45055	busware.de
A4516F	Microsoft Mobile Oy
A4526F	ADB Broadband Italia
A45385	Weifang GoerTek Electronics Co., Ltd.
A45602	fenglian Technology Co.,Ltd.
A4561B	MCOT Corporation
A45630	Cisco Systems, Inc
A4580F	IEEE Registration Authority
A45A1C	smart-electronic GmbH
A45C27	Nintendo Co., Ltd.
A45D36	Hewlett Packard
A45DA1	ADB Broadband Italia
A45E60	Apple, Inc.
A46011	Verifone
A46032	MRV Communications (Networks) LTD
A462DF	DS Global. Co., LTD
A46706	Apple, Inc.
A468BC	Private
A46C2A	Cisco Systems, Inc
A46CC1	LTi REEnergy GmbH
A46E79	DFT System Co.Ltd
A470D6	Motorola Mobility LLC, a Lenovo Company
A47174	HUAWEI TECHNOLOGIES CO.,LTD
A47733	Google, Inc.
A47760	Nokia Corporation
A479E4	KLINFO Corp
A47AA4	ARRIS Group, Inc.
A47ACF	VIBICOM COMMUNICATIONS INC.
A47B2C	Nokia
A47B85	ULTIMEDIA Co Ltd,
A47C14	ChargeStorm AB
A47C1F	Cobham plc
A47E39	zte corporation
A481EE	Nokia Corporation
A48269	Datrium, Inc.
A48431	Samsung Electronics Co.,Ltd
A4856B	Q Electronics Ltd
A4895B	ARK INFOSOLUTIONS PVT LTD
A48CDB	Lenovo
A48D3B	Vizio, Inc
A48E0A	DeLaval International AB
A49005	CHINA GREATWALL COMPUTER SHENZHEN CO.,LTD
A4934C	Cisco Systems, Inc
A497BB	Hitachi Industrial Equipment Systems Co.,Ltd
A49947	HUAWEI TECHNOLOGIES CO.,LTD
A49981	FuJian Elite Power Tech CO.,LTD.
A49A58	Samsung Electronics Co.,Ltd
A49B13	Digital Check
A49BF5	Hybridserver Tec GmbH
A49D49	Ketra, Inc.
A49EDB	AutoCrib, Inc.
A49F85	Lyve Minds, Inc
A49F89	Shanghai Rui Rui Communication Technology Co.Ltd.
A4A1C2	Ericsson AB
A4A1E4	Innotube, Inc.
A4A24A	Cisco SPVTG
A4A4D3	Bluebank Communication Technology Co.Ltd
A4A6A9	Private
A4A80F	Shenzhen Coship Electronics Co., Ltd.
A4AD00	Ragsdale Technology
A4ADB8	Vitec Group, Camera Dynamics Ltd
A4AE9A	Maestro Wireless Solutions ltd.
A4B121	Arantia 2010 S.L.
A4B197	Apple, Inc.
A4B1E9	Technicolor
A4B1EE	H. ZANDER GmbH & Co. KG
A4B2A7	Adaxys Solutions AG
A4B36A	JSC SDO Chromatec
A4B805	Apple, Inc.
A4B818	PENTA Gesellschaft für elektronische Industriedatenverarbeitung mbH
A4B980	Parking BOXX Inc.
A4BA76	HUAWEI TECHNOLOGIES CO.,LTD
A4BADB	Dell Inc.
A4BBAF	Lime Instruments
A4BE61	EutroVision System, Inc.
A4BF01	Intel Corporate
A4C0C7	ShenZhen Hitom Communication Technology Co..LTD
A4C0E1	Nintendo Co., Ltd.
A4C138	Telink Semiconductor (Taipei) Co. Ltd.
A4C2AB	Hangzhou LEAD-IT Information & Technology Co.,Ltd
A4C361	Apple, Inc.
A4C494	Intel Corporate
A4C64F	HUAWEI TECHNOLOGIES CO.,LTD
A4C7DE	Cambridge Industries(Group) Co.,Ltd.
A4CAA0	HUAWEI TECHNOLOGIES CO.,LTD
A4CC32	Inficomm Co., Ltd
A4D094	Erwin Peters Systemtechnik GmbH
A4D18C	Apple, Inc.
A4D18F	Shenzhen Skyee Optical Fiber Communication Technology Ltd.
A4D1D1	ECOtality North America
A4D1D2	Apple, Inc.
A4D3B5	GLITEL Stropkov, s.r.o.
A4D578	Texas Instruments
A4D856	Gimbal, Inc
A4D8CA	HONG KONG WATER WORLD TECHNOLOGY CO. LIMITED
A4D9A4	neXus ID Solutions AB
A4DA3F	Bionics Corp.
A4DB2E	Kingspan Environmental Ltd
A4DB30	Liteon Technology Corporation
A4DCBE	HUAWEI TECHNOLOGIES CO.,LTD
A4DE50	Total Walther GmbH
A4DEC9	QLove Mobile Intelligence Information Technology (W.H.) Co. Ltd.
A4E0E6	FILIZOLA S.A. PESAGEM E AUTOMACAO
A4E32E	Silicon & Software Systems Ltd.
A4E391	DENY FONTAINE
A4E4B8	BlackBerry RTS
A4E597	Gessler GmbH
A4E6B1	Shanghai Joindata Technology Co.,Ltd.
A4E731	Nokia Corporation
A4E7E4	Connex GmbH
A4E991	SISTEMAS AUDIOVISUALES ITELSIS S.L.
A4E9A3	Honest Technology Co., Ltd
A4EBD3	Samsung Electronics Co.,Ltd
A4ED4E	ARRIS Group, Inc.
A4EE57	Seiko Epson Corporation
A4EF52	Telewave Co., Ltd.
A4F1E8	Apple, Inc.
A4F3C1	Open Source Robotics Foundation, Inc.
A4F522	CHOFU SEISAKUSHO CO.,LTD
A4F7D0	LAN Accessories Co., Ltd.
A4FB8D	Hangzhou Dunchong Technology Co.Ltd
A4FCCE	Security Expert Ltd.
A80180	IMAGO Technologies GmbH
A80600	Samsung Electronics Co.,Ltd
A80C0D	Cisco Systems, Inc
A80CCA	Shenzhen Sundray Technologies Company Limited
A811FC	ARRIS Group, Inc.
A81374	Panasonic Corporation AVC Networks Company
A8154D	TP-LINK TECHNOLOGIES CO.,LTD.
A81559	Breathometer, Inc.
A815D6	Shenzhen Meione Technology CO., LTD
A816B2	LG Electronics (Mobile Communications)
A81758	Elektronik System i Umeå AB
A81B18	XTS CORP
A81B5A	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
A81B5D	Foxtel Management Pty Ltd
A81B6A	Texas Instruments
A81D16	AzureWave Technology Inc.
A81E84	QUANTA COMPUTER INC.
A81FAF	KRYPTON POLSKA
A82066	Apple, Inc.
A824EB	ZAO NPO Introtest
A826D9	HTC Corporation
A8294C	Precision Optical Transceivers, Inc.
A82BD6	Shina System Co., Ltd
A830AD	Wei Fang Goertek Electronics Co.,Ltd
A8329A	Digicom Futuristic Technologies Ltd.
A83944	Actiontec Electronics, Inc
A84041	Dragino Technology Co., Limited
A84481	Nokia Corporation
A845CD	Siselectron Technology LTD.
A845E9	Firich Enterprises CO., LTD.
A8474A	Hon Hai Precision Ind. Co.,Ltd.
A849A5	Lisantech Co., Ltd.
A84E3F	Hitron Technologies. Inc
A854B2	Wistron Neweb Corporation
A8556A	Pocketnet Technology Inc.
A8574E	TP-LINK TECHNOLOGIES CO.,LTD.
A85840	Cambridge Industries(Group) Co.,Ltd.
A85B78	Apple, Inc.
A85BB0	Shenzhen Dehoo Technology Co.,Ltd
A85BF3	Audivo GmbH
A85EE4	12Sided Technology, LLC
A860B6	Apple, Inc.
A861AA	Cloudview Limited
A862A2	JIWUMEDIA CO., LTD.
A863DF	DISPLAIRE CORPORATION
A863F2	Texas Instruments
A86405	nimbus 9, Inc
A865B2	DONGGUAN YISHANG ELECTRONIC TECHNOLOGY CO., LIMITED
A8667F	Apple, Inc.
A86A6F	Rim
A86AC1	HanbitEDS Co., Ltd.
A86BAD	Hon Hai Precision Ind. Co.,Ltd.
A870A5	UniComm Inc.
A87285	IDT, INC.
A8741D	PHOENIX CONTACT Electronics GmbH
A875D6	FreeTek International Co., Ltd.
A875E2	Aventura Technologies, Inc.
A8776F	Zonoff
A87B39	Nokia Corporation
A87C01	Samsung Electronics Co.,Ltd
A87E33	Nokia Danmark A/S
A88038	ShenZhen MovingComm Technology Co., Limited
A88195	Samsung Electronics Co.,Ltd
A881F1	BMEYE B.V.
A8827F	CIBN Oriental Network(Beijing) CO.,Ltd
A886DD	Apple, Inc.
A88792	Broadband Antenna Tracking Systems
A887ED	ARC Wireless LLC
A88808	Apple, Inc.
A88CEE	MicroMade Galka i Drozdz sp.j.
A88D7B	SunDroid Global limited.
A88E24	Apple, Inc.
A89008	Beijing Yuecheng Technology Co. Ltd.
A8922C	LG Electronics (Mobile Communications)
A89352	SHANGHAI ZHONGMI COMMUNICATION TECHNOLOGY CO.,LTD
A893E6	JIANGXI JINGGANGSHAN CKING COMMUNICATION TECHNOLOGY CO.,LTD
A895B0	Aker Subsea Ltd
A8968A	Apple, Inc.
A897DC	Ibm
A898C6	Shinbo Co., Ltd.
A8995C	aizo ag
A89B10	inMotion Ltd.
A89D21	Cisco Systems, Inc
A89DD2	Shanghai DareGlobal Technologies Co.,Ltd
A89FBA	Samsung Electronics Co.,Ltd
A8A089	Tactical Communications
A8A198	TCT mobile ltd
A8A5E2	MSF-Vathauer Antriebstechnik GmbH & Co KG
A8A648	Qingdao Hisense Communications Co.,Ltd.
A8A668	zte corporation
A8A795	Hon Hai Precision Ind. Co.,Ltd.
A8AD3D	Alcatel-               # Alcatel-Lucent Shanghai Bell Co., Ltd
A8B0AE	Leoni
A8B1D4	Cisco Systems, Inc
A8B86E	LG Electronics (Mobile Communications)
A8B9B3	Essys
A8BB50	WiZ IoT Company Limited
A8BBCF	Apple, Inc.
A8BD1A	Honey Bee (Hong Kong) Limited
A8BD27	Hewlett Packard Enterprise
A8BD3A	UNIONMAN TECHNOLOGY CO.,LTD
A8C222	TM-Research Inc.
A8C83A	HUAWEI TECHNOLOGIES CO.,LTD
A8C87F	Roqos, Inc.
A8CA7B	HUAWEI TECHNOLOGIES CO.,LTD
A8CB95	EAST BEST CO., LTD.
A8CCC5	Saab AB (publ)
A8CE90	Cvc
A8D0E3	Systech Electronics Ltd.
A8D0E5	Juniper Networks
A8D236	Lightware Visual Engineering
A8D3C8	Wachendorff Elektronik  GmbH & Co. KG
A8D3F7	Arcadyan Technology Corporation
A8D409	USA 111 Inc
A8D579	Beijing Chushang Science and Technology Co.,Ltd
A8D828	Ascensia Diabetes Care
A8D88A	Wyconn
A8E018	Nokia Corporation
A8E3EE	Sony Interactive Entertainment Inc.
A8E539	Moimstone Co.,Ltd
A8E705	Fiberhome Telecommunication Technologies Co.,LTD
A8EF26	Tritonwave
A8F038	SHEN ZHEN SHI JIN HUA TAI ELECTRONICS CO.,LTD
A8F274	Samsung Electronics Co.,Ltd
A8F470	Fujian Newland Communication Science Technologies Co.,Ltd.
A8F7E0	PLANET Technology Corporation
A8F94B	Eltex Enterprise Ltd.
A8FAD8	Apple, Inc.
A8FB70	WiseSec L.t.d
A8FCB7	Consolidated Resource Imaging
AA0000	DEC				obsolete
AA0001	DEC				obsolete
AA0002	DEC				obsolete
AA0003	DEC				Global physical address for some DEC machines
AA0004	DEC				Local logical address for DECNET systems
AC0142	Uriel Technologies SIA
AC02CA	HI Solutions, Inc.
AC02CF	RW Tecnologia Industria e Comercio Ltda
AC02EF	Comsis
AC040B	Peloton Interactive, Inc
AC0481	Jiangsu Huaxing Electronics Co., Ltd.
AC0613	Senselogix Ltd
AC06C7	ServerNet S.r.l.
AC0A61	Labor S.r.L.
AC0D1B	LG Electronics (Mobile Communications)
AC0DFE	Ekon GmbH - myGEKKO
AC11D3	Suzhou HOTEK  Video Technology Co. Ltd
AC1461	ATAW  Co., Ltd.
AC14D2	wi-daq, inc.
AC162D	Hewlett Packard
AC1702	Fibar Group sp. z o.o.
AC1826	Seiko Epson Corporation
AC199F	SUNGROW POWER SUPPLY CO.,LTD.
AC1F6B	Super Micro Computer, Inc.
AC1FD7	Real Vision Technology Co.,Ltd.
AC202E	Hitron Technologies. Inc
AC20AA	DMATEK Co., Ltd.
AC220B	ASUSTek COMPUTER INC.
AC233F	Shenzhen Minew Technologies Co., Ltd.
AC293A	Apple, Inc.
AC2A0C	CSR ZHUZHOU INSTITUTE CO.,LTD.
AC2B6E	Intel Corporate
AC2DA3	TXTR GmbH
AC2FA8	Humannix Co.,Ltd.
AC319D	Shenzhen TG-NET Botone Technology Co.,Ltd.
AC34CB	Shanhai GBCOM Communication Technology Co. Ltd
AC3613	Samsung Electronics Co.,Ltd
AC3743	HTC Corporation
AC3870	Lenovo Mobile Communication Technology Ltd.
AC3A7A	Roku, Inc.
AC3C0B	Apple, Inc.
AC3CB4	Nilan A/S
AC3D05	Instorescreen Aisa
AC3D75	HANGZHOU ZHIWAY TECHNOLOGIES CO.,LTD.
AC3FA4	TAIYO YUDEN CO.,LTD
AC40EA	C&T Solution Inc.
AC4122	Eclipse Electronic Systems Inc.
AC44F2	YAMAHA CORPORATION
AC4723	Genelec
AC482D	Ralinwi Nanjing Electronic Technology Co., Ltd.
AC4AFE	Hisense Broadband Multimedia Technology Co.,Ltd.
AC4BC8	Juniper Networks
AC4E91	HUAWEI TECHNOLOGIES CO.,LTD
AC4FFC	SVS-VISTEK GmbH
AC5036	Pi-Coral Inc
AC5135	MPI TECH
AC51EE	Cambridge Communication Systems Ltd
AC54EC	IEEE P1823 Standards Working Group
AC562C	LAVA INTERNATIONAL(H.K) LIMITED
AC583B	Human Assembler, Inc.
AC587B	JCT Healthcare
AC5A14	Samsung Electronics Co.,Ltd
AC5D10	Pace Americas
AC5E8C	Utillink
AC5F3E	SAMSUNG ELECTRO-MECHANICS(THAILAND)
AC60B6	Ericsson AB
AC6123	Drivven, Inc.
AC6175	HUAWEI TECHNOLOGIES CO.,LTD
AC61EA	Apple, Inc.
AC620D	Jabil Circuit(Wuxi) Co.,Ltd
AC63BE	Amazon Technologies Inc.
AC6462	zte corporation
AC64DD	IEEE Registration Authority
AC6706	Ruckus Wireless
AC676F	Electrocompaniet A.S.
AC6B0F	CADENCE DESIGN SYSTEMS INC
AC6BAC	Jenny Science AG
AC6E1A	Shenzhen Gongjin Electronics Co.,Ltd
AC6F4F	Enspert Inc
AC6FBB	TATUNG Technology Inc.
AC6FD9	Valueplus Inc.
AC7236	Lexking Technology Co., Ltd.
AC7289	Intel Corporate
AC7409	Hangzhou H3C Technologies Co., Limited
AC7A42	iConnectivity
AC7A4D	ALPS ELECTRIC CO.,LTD.
AC7BA1	Intel Corporate
AC7E8A	Cisco Systems, Inc
AC7F3E	Apple, Inc.
AC80D6	Hexatronic AB
AC8112	Gemtek Technology Co., Ltd.
AC81F3	Nokia Corporation
AC8317	Shenzhen Furtunetel Communication Co., Ltd
AC83F0	ImmediaTV Corporation
AC83F3	AMPAK Technology, Inc.
AC84C9	Sagemcom Broadband SAS
AC853D	HUAWEI TECHNOLOGIES CO.,LTD
AC8674	Open Mesh, Inc.
AC867E	Create New Technology (HK) Limited Company
AC87A3	Apple, Inc.
AC8995	AzureWave Technology Inc.
AC8ACD	ROGER D.Wensker, G.Wensker sp.j.
AC8D14	Smartrove Inc
AC932F	Nokia Corporation
AC9403	Envision Peripherals Inc
AC9A22	NXP Semiconductors
AC9A96	Lantiq Deutschland GmbH
AC9B0A	Sony Corporation
AC9B84	Smak Tecnologia e Automacao
AC9CE4	Alcatel-               # Alcatel-Lucent Shanghai Bell Co., Ltd
AC9E17	ASUSTek COMPUTER INC.
ACA016	Cisco Systems, Inc
ACA213	Shenzhen Bilian electronic CO.,LTD
ACA22C	Baycity Technologies Ltd
ACA31E	Aruba Networks
ACA430	Peerless AV
ACA919	TrekStor GmbH
ACA9A0	Audioengine, Ltd.
ACAB2E	Beijing LasNubes Technology Co., Ltd.
ACAB8D	Lyngso Marine A/S
ACABBF	AthenTek Inc.
ACB313	ARRIS Group, Inc.
ACB57D	Liteon Technology Corporation
ACB74F	METEL s.r.o.
ACB859	Uniband Electronic Corp,
ACBC32	Apple, Inc.
ACBD0B	IMAC CO.,LTD
ACBE75	Ufine Technologies Co.,Ltd.
ACBEB6	Visualedge Technology Co., Ltd.
ACC1EE	Xiaomi Communications Co Ltd
ACC2EC	CLT INT'L IND. CORP.
ACC33A	Samsung Electronics Co.,Ltd
ACC51B	Zhuhai Pantum Electronics Co., Ltd.
ACC595	Graphite Systems
ACC662	MitraStar Technology Corp.
ACC698	Kohzu Precision Co., Ltd.
ACC73F	VITSMO CO., LTD.
ACC935	Ness Corporation
ACCA54	Telldus Technologies AB
ACCA8E	ODA Technologies
ACCAAB	Virtual Electric Inc
ACCABA	Midokura Co., Ltd.
ACCB09	Hefcom Metering (Pty) Ltd
ACCC8E	Axis Communications AB
ACCE8F	HWA YAO TECHNOLOGIES CO., LTD
ACCF23	Hi-flying electronics technology Co.,Ltd
ACCF5C	Apple, Inc.
ACCF85	HUAWEI TECHNOLOGIES CO.,LTD
ACD074	Espressif Inc.
ACD180	Crexendo Business Solutions, Inc.
ACD1B8	Hon Hai Precision Ind. Co.,Ltd.
ACD364	ABB SPA, ABB SACE DIV.
ACD657	Shaanxi GuoLian Digital TV Technology Co.,Ltd.
ACD9D6	tci GmbH
ACDBDA	Shenzhen Geniatech Inc, Ltd
ACDCE5	Procter & Gamble Company
ACDE48	Private
ACE010	Liteon Technology Corporation
ACE069	ISAAC Instruments
ACE215	HUAWEI TECHNOLOGIES CO.,LTD
ACE348	MadgeTech, Inc
ACE42E	SK hynix
ACE5F0	Doppler Labs
ACE64B	Shenzhen Baojia Battery Technology Co., Ltd.
ACE77B	SICHUAN TIANYI COMHEART TELECOMCO.,LTD
ACE87B	HUAWEI TECHNOLOGIES CO.,LTD
ACE87E	Bytemark Computer Consulting Ltd
ACE97F	IoT Tech Limited
ACE9AA	Hay Systems Ltd
ACEA6A	GENIX INFOCOMM CO., LTD.
ACEC80	ARRIS Group, Inc.
ACEE3B	6harmonics Inc
ACEE9E	Samsung Electronics Co.,Ltd
ACF0B2	Becker Electronics Taiwan Ltd.
ACF1DF	D-Link International
ACF2C5	Cisco Systems, Inc
ACF7F3	Xiaomi Communications Co Ltd
ACF85C	Private
ACF97E	ELESYS INC.
ACFD93	Weifang GoerTek Electronics Co., Ltd.
ACFDCE	Intel Corporate
ACFDEC	Apple, Inc.
B000B4	Cisco Systems, Inc
B00594	Liteon Technology Corporation
B008BF	Vital Connect, Inc.
B009D3	Avizia
B01041	Hon Hai Precision Ind. Co.,Ltd.
B01203	Dynamics Hong Kong Limited
B01266	Futaba-Kikaku
B01408	LIGHTSPEED INTERNATIONAL CO.
B01743	EDISON GLOBAL CIRCUITS LLC
B01B7C	Ontrol A.S.
B01BD2	Le Shi Zhi Xin Electronic Technology (Tianjin) Limited
B01C91	Elim Co
B01F81	IEEE Registration Authority
B024F3	Progeny Systems
B025AA	Private
B02628	Broadcom Limited
B03495	Apple, Inc.
B0358D	Nokia Corporation
B0359F	Intel Corporate
B03829	Siliconware Precision Industries Co., Ltd.
B03850	Nanjing CAS-ZDC IOT SYSTEM CO.,LTD
B03D96	Vision Valley FZ LLC
B03EB0	MICRODIA Ltd.
B04089	Senient Systems LTD
B0411D	ITTIM Technologies
B0435D	NuLEDs, Inc.
B04515	mira fitness,LLC.
B04519	TCT mobile ltd
B04545	YACOUB Automation GmbH
B046FC	MitraStar Technology Corp.
B047BF	Samsung Electronics Co.,Ltd
B0481A	Apple, Inc.
B0487A	TP-LINK TECHNOLOGIES CO.,LTD.
B0495F	OMRON HEALTHCARE Co., Ltd.
B04BBF	PT HAN SUNG ELECTORONICS INDONESIA
B04C05	Fresenius Medical Care Deutschland GmbH
B050BC	SHENZHEN BASICOM ELECTRONIC CO.,LTD.
B0518E	Holl technology CO.Ltd.
B05216	Hon Hai Precision Ind. Co.,Ltd.
B05706	Vallox Oy
B058C4	Broadcast Microwave Services, Inc
B05947	Shenzhen Qihu Intelligent Technology Company Limited
B05ADA	Hewlett Packard
B05B1F	THERMO FISHER SCIENTIFIC S.P.A.
B05B67	HUAWEI TECHNOLOGIES CO.,LTD
B05CE5	Nokia Corporation
B061C7	Ericsson-LG Enterprise
B06563	Shanghai Railway Communication Factory
B065BD	Apple, Inc.
B068B6	Hangzhou OYE Technology Co. Ltd
B06971	DEI Sales, Inc.
B06CBF	3ality Digital Systems GmbH
B0702D	Apple, Inc.
B072BF	Murata Manufacturing Co., Ltd.
B0750C	QA Cafe
B0754D	Nokia
B075D5	zte corporation
B077AC	ARRIS Group, Inc.
B07870	Wi-NEXT, Inc.
B078F0	Beijing HuaqinWorld Technology Co.,Ltd.
B07908	Cummings Engineering
B0793C	Revolv Inc
B07994	Motorola Mobility LLC, a Lenovo Company
B07D47	Cisco Systems, Inc
B07D62	Dipl.-Ing. H. Horstmann GmbH
B07E70	Zadara Storage Ltd.
B07FB9	Netgear
B0808C	Laser Light Engines
B081D8	I-sys Corp
B083FE	Dell Inc.
B0869E	Chloride S.r.L
B08807	Strata Worldwide
B08900	HUAWEI TECHNOLOGIES CO.,LTD
B08991	Lge
B08E1A	URadio Systems Co., Ltd
B09074	Fulan Electronics Limited
B09122	Texas Instruments
B09134	Taleo
B09137	ISis ImageStream Internet Solutions, Inc
B0958E	TP-LINK TECHNOLOGIES CO.,LTD.
B0966C	Lanbowan Technology Ltd.
B0973A	E-Fuel Corporation
B0989F	LG CNS
B09928	FUJITSU LIMITED
B09AE2	STEMMER IMAGING GmbH
B09BD4	GNH Software India Private Limited
B09FBA	Apple, Inc.
B0A10A	Pivotal Systems Corporation
B0A2E7	Shenzhen TINNO Mobile Technology Corp.
B0A37E	Qingdao Haier Telecom Co.，Ltd
B0A72A	Ensemble Designs, Inc.
B0A737	Roku, Inc.
B0A86E	Juniper Networks
B0AA36	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
B0AA77	Cisco Systems, Inc
B0ACFA	FUJITSU LIMITED
B0ADAA	Avaya Inc
B0B28F	Sagemcom Broadband SAS
B0B2DC	ZyXEL Communications Corporation
B0B32B	Slican Sp. z o.o.
B0B448	Texas Instruments
B0B8D5	Nanjing Nengrui Auto Equipment CO.,Ltd
B0B98A	Netgear
B0BD6D	Echostreams Innovative Solutions
B0BDA1	ZAKLAD ELEKTRONICZNY SIMS
B0BF99	WIZITDONGDO
B0C090	Chicony Electronics Co., Ltd.
B0C128	Adler ELREHA GmbH
B0C205	Bionime
B0C287	Technicolor CH USA Inc.
B0C46C	Senseit
B0C4E7	Samsung Electronics Co.,Ltd
B0C554	D-Link International
B0C559	Samsung Electronics Co.,Ltd
B0C5CA	IEEE Registration Authority
B0C69A	Juniper Networks
B0C745	BUFFALO.INC
B0C83F	Jiangsu Cynray IOT Co., Ltd.
B0C8AD	People Power Company
B0C95B	Beijing Symtech CO.,LTD
B0CE18	Zhejiang shenghui lighting co.,Ltd
B0CF4D	MI-Zone Technology Ireland
B0D09C	Samsung Electronics Co.,Ltd
B0D2F5	Vello Systems, Inc.
B0D59D	Shenzhen Zowee Technology Co., Ltd
B0D5CC	Texas Instruments
B0D7C5	Logipix Ltd
B0D7CC	Tridonic GmbH & Co KG
B0DA00	CERA ELECTRONIQUE
B0DF3A	Samsung Electronics Co.,Ltd
B0E03C	TCT mobile ltd
B0E235	Xiaomi Communications Co Ltd
B0E2E5	Fiberhome Telecommunication Technologies Co.,LTD
B0E39D	CAT SYSTEM CO.,LTD.
B0E50E	NRG SYSTEMS INC
B0E5ED	HUAWEI TECHNOLOGIES CO.,LTD
B0E754	2Wire Inc
B0E892	Seiko Epson Corporation
B0E97E	Advanced Micro Peripherals
B0EC71	Samsung Electronics Co.,Ltd
B0EC8F	GMX SAS
B0ECE1	Private
B0EE45	AzureWave Technology Inc.
B0EE7B	Roku, Inc
B0F1A3	Fengfan (BeiJing) Technology Co., Ltd.
B0F1BC	Dhemax Ingenieros Ltda
B0F1EC	AMPAK Technology, Inc.
B0F893	Shanghai MXCHIP Information Technology Co., Ltd.
B0F963	Hangzhou H3C Technologies Co., Limited
B0FAEB	Cisco Systems, Inc
B0FEBD	Private
B4009C	CableWorld Ltd.
B40142	GCI Science & Technology Co.,LTD
B40418	Smartchip Integrated Inc.
B40566	SP Best Corporation Co., LTD.
B407F9	SAMSUNG ELECTRO MECHANICS CO., LTD.
B40832	TC Communications
B40AC6	DEXON Systems Ltd.
B40B44	Smartisan Technology Co., Ltd.
B40B7A	Brusa Elektronik AG
B40C25	Palo Alto Networks
B40E96	Heran
B40EDC	LG-Ericsson Co.,Ltd.
B41489	Cisco Systems, Inc
B41513	HUAWEI TECHNOLOGIES CO.,LTD
B41780	DTI Group Ltd
B418D1	Apple, Inc.
B41DEF	Internet Laboratories, Inc.
B4211D	Beijing GuangXin Technology Co., Ltd
B4218A	Dog Hunter LLC
B424E7	Codetek Technology Co.,Ltd
B428F1	E-Prime Co., Ltd.
B4293D	Shenzhen Urovo Technology Co.,Ltd.
B42A0E	Technicolor CH USA Inc.
B42A39	ORBIT MERRET, spol. s r. o.
B42C92	Zhejiang Weirong Electronic Co., Ltd
B42CBE	Direct Payment Solutions Limited
B43052	HUAWEI TECHNOLOGIES CO.,LTD
B431B8	Aviwest
B4346C	MATSUNICHI DIGITAL TECHNOLOGY (HONG KONG) LIMITED
B43564	Fujian Tian Cheng Electron Science & Technical Development Co.,Ltd.
B435F7	Zhejiang Pearmain Electronics Co.ltd.
B436A9	Fibocom Wireless Inc.
B436E3	KBVISION GROUP
B43741	Consert, Inc.
B437D1	IEEE Registration Authority
B43934	Pen Generations, Inc.
B439D6	ProCurve Networking by HP
B43A28	Samsung Electronics Co.,Ltd
B43DB2	Degreane Horizon
B43E3B	Viableware, Inc
B4417A	SHENZHEN GONGJIN ELECTRONICS CO.,LT
B4430D	Broadlink Pty Ltd
B4475E	Avaya Inc
B44BD2	Apple, Inc.
B44CC2	NR ELECTRIC CO., LTD
B451F9	NB Software
B45253	Seagate Technology
B4527D	Sony Mobile Communications AB
B4527E	Sony Mobile Communications AB
B45570	Borea
B456B9	Teraspek Technologies Co.,Ltd
B45861	CRemote, LLC
B45CA4	Thing-talk Wireless Communication Technologies Corporation Limited
B45D50	Aruba Networks
B461FF	Lumigon A/S
B46238	Exablox
B46293	Samsung Electronics Co.,Ltd
B462AD	Elysia Germany GmbH
B46698	Zealabs srl
B467E9	Qingdao GoerTek Technology Co., Ltd.
B46D35	Dalian Seasky Automation Co;Ltd
B46D83	Intel Corporate
B47356	Hangzhou Treebear Networking Co., Ltd.
B47443	Samsung Electronics Co.,Ltd
B47447	Coreos
B4749F	ASKEY COMPUTER CORP
B4750E	Belkin International Inc.
B479A7	SAMSUNG ELECTRO-MECHANICS(THAILAND)
B47C29	Shenzhen Guzidi Technology Co.,Ltd
B47C9C	Amazon Technologies Inc.
B47F5E	Foresight Manufacture (S) Pte Ltd
B48255	Research Products Corporation
B4827B	AKG Acoustics GmbH
B482C5	Relay2, Inc.
B482FE	ASKEY COMPUTER CORP
B48547	Amptown System Company GmbH
B48910	Coster T.E. S.P.A.
B48B19	Apple, Inc.
B4944E	WeTelecom Co., Ltd.
B49691	Intel Corporate
B49842	zte corporation
B4994C	Texas Instruments
B499BA	Hewlett Packard
B49CDF	Apple, Inc.
B49D0B	Bq
B49DB4	Axion Technologies Inc.
B49EAC	Imagik Int'l Corp
B49EE6	SHENZHEN TECHNOLOGY CO LTD
B4A4B5	Zen Eye Co.,Ltd
B4A4E3	Cisco Systems, Inc
B4A5A9	MODI GmbH
B4A5EF	Sercomm Corporation.
B4A828	Shenzhen Concox Information Technology Co., Ltd
B4A82B	Histar Digital Electronics Co., Ltd.
B4A95A	Avaya Inc
B4A984	Symantec Corporation
B4A9FE	GHIA Technology (Shenzhen) LTD
B4AA4D	Ensequence, Inc.
B4AB2C	MtM Technology Corporation
B4AE2B	Microsoft
B4AE6F	Circle Reliance, Inc DBA Cranberry Networks
B4B017	Avaya Inc
B4B15A	Siemens AG Energy Management Division
B4B265	DAEHO I&T
B4B362	zte corporation
B4B384	ShenZhen Figigantic Electronic Co.,Ltd
B4B52F	Hewlett Packard
B4B542	Hubbell Power Systems, Inc.
B4B5AF	Minsung Electronics
B4B676	Intel Corporate
B4B859	Texa Spa
B4B88D	Thuh Company
B4C44E	VXL eTech Pvt Ltd
B4C6F8	Axilspot Communication
B4C799	Extreme Networks
B4C810	UMPI Elettronica
B4CCE9	Prosyst
B4CEF6	HTC Corporation
B4CFDB	Shenzhen Jiuzhou Electric Co.,LTD
B4D135	Cloudistics
B4D5BD	Intel Corporate
B4D8A9	BetterBots
B4D8DE	iota Computing, Inc.
B4DD15	ControlThings Oy Ab
B4DF3B	Chromlech
B4DFFA	Litemax Electronics Inc.
B4E0CD	Fusion-io, Inc
B4E10F	Dell Inc.
B4E1C4	Microsoft Mobile Oy
B4E1EB	Private
B4E782	Vivalnk
B4E9B0	Cisco Systems, Inc
B4ED19	Pie Digital, Inc.
B4ED54	Wohler Technologies
B4EEB4	ASKEY COMPUTER CORP
B4EED4	Texas Instruments
B4EF04	DAIHAN Scientific Co., Ltd.
B4EF39	Samsung Electronics Co.,Ltd
B4EFFA	Lemobile Information Technology (Beijing) Co., Ltd.
B4F0AB	Apple, Inc.
B4F2E8	ARRIS Group, Inc.
B4F323	PETATEL INC.
B4F81E	Kinova
B4FBE4	Ubiquiti Networks Inc.
B4FC75	SEMA Electronics(HK) CO.,LTD
B4FE8C	Centro Sicurezza Italia SpA
B80018	Htel
B80305	Intel Corporate
B80415	Bayan Audio
B805AB	zte corporation
B808CF	Intel Corporate
B808D7	HUAWEI TECHNOLOGIES CO.,LTD
B8098A	Apple, Inc.
B80B9D	ROPEX Industrie-Elektronik GmbH
B813E9	Trace Live Network
B81413	Keen High Holding(HK) Ltd.
B81619	ARRIS Group, Inc.
B816DB	CHANT SINCERE CO.,LTD
B817C2	Apple, Inc.
B8186F	ORIENTAL MOTOR CO., LTD.
B81999	Nesys
B81DAA	LG Electronics (Mobile Communications)
B820E7	Guangzhou Horizontal Information & Network Integration Co. Ltd
B8224F	SICHUAN TIANYI COMHEART TELECOMCO., LTD
B82410	Magneti Marelli Slovakia s.r.o.
B8241A	SWEDA INFORMATICA LTDA
B824F0	SOYO Technology Development Co., Ltd.
B8266C	ANOV France
B826D4	Furukawa Industrial S.A. Produtos Elétricos
B827EB	Raspberry Pi Foundation
B8288B	Parker Hannifin Manufacturing (UK) Ltd
B829F7	Blaster Tech
B82A72	Dell Inc.
B82ADC	EFR Europäische Funk-Rundsteuerung GmbH
B82CA0	Honeywell HomMed
B830A8	Road-Track Telematics Development
B83241	Wuhan Tianyu Information Industry Co., Ltd.
B836D8	Videoswitch
B83765	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
B83861	Cisco Systems, Inc
B838CA	Kyokko Tsushin System CO.,LTD
B83A08	Tenda Technology Co.,Ltd.Dongguan branch
B83A7B	Worldplay (Canada) Inc.
B83A9D	Alarm.com
B83D4E	Shenzhen Cultraview Digital Technology Co.,Ltd Shanghai Branch
B83E59	Roku, Inc.
B8415F	ASP AG
B843E4	Vlatacom
B844D9	Apple, Inc.
B847C6	SanJet Technology Corp.
B84FD5	Microsoft Corporation
B85001	Extreme Networks
B853AC	Apple, Inc.
B85510	Zioncom Electronics (Shenzhen) Ltd.
B856BD	ITT LLC
B857D8	Samsung Electronics Co.,Ltd
B85810	NUMERA, INC.
B85A73	Samsung Electronics Co.,Ltd
B85AF7	Ouya, Inc
B85AFE	Handaer Communication Technology (Beijing) Co., Ltd
B85E7B	Samsung Electronics Co.,Ltd
B86091	Onnet Technologies and Innovations LLC
B8616F	Accton Technology Corp
B8621F	Cisco Systems, Inc
B863BC	ROBOTIS, Co, Ltd
B86491	CK Telecom Ltd
B8653B	Bolymin, Inc.
B869C2	Sunitec Enterprise Co., Ltd.
B86B23	Toshiba
B86CE8	Samsung Electronics Co.,Ltd
B870F4	COMPAL INFORMATION (KUNSHAN) CO., LTD.
B87424	Viessmann Elektronik GmbH
B87447	Convergence Technologies
B875C0	PayPal, Inc.
B8763F	Hon Hai Precision Ind. Co.,Ltd.
B877C3	Decagon Devices, Inc.
B8782E	Apple, Inc.
B87879	Roche Diagnostics GmbH
B8797E	Secure Meters (UK) Limited
B87AC9	Siemens Ltd.
B87CF2	Aerohive Networks Inc.
B88198	Intel Corporate
B88687	Liteon Technology Corporation
B8871E	Good Mind Industries Co., Ltd.
B887A8	Step Ahead Innovations Inc.
B888E3	COMPAL INFORMATION (KUNSHAN) CO., LTD.
B88981	Chengdu InnoThings Technology Co., Ltd.
B889CA	ILJIN ELECTRIC Co., Ltd.
B88A60	Intel Corporate
B88D12	Apple, Inc.
B88E3A	Infinite Technologies JLT
B88EC6	Stateless Networks
B88EDF	Zencheer Communication Technology Co., Ltd.
B88F14	Analytica GmbH
B8921D	BG T&A
B894D2	Retail Innovation HTT AB
B89674	AllDSP GmbH & Co. KG
B8975A	BIOSTAR Microtech Int'l Corp.
B898B0	Atlona Inc.
B898F7	Gionee Communication Equipment Co,Ltd.ShenZhen
B89919	7signal Solutions, Inc
B899B0	Cohere Technologies
B89ACD	ELITE OPTOELECTRONIC(ASIA)CO.,LTD
B89AED	OceanServer Technology, Inc
B89BC9	SMC Networks Inc
B89BE4	ABB Power Systems Power Generation
B8A175	Roku, Inc.
B8A386	D-Link International
B8A3E0	BenRui Technology Co.,Ltd
B8A8AF	Logic S.p.A.
B8AC6F	Dell Inc.
B8AD3E	Bluecom
B8AE6E	Nintendo Co., Ltd.
B8AEED	Elitegroup Computer Systems Co.,Ltd.
B8AF67	Hewlett Packard
B8B1C7	BT&COM CO.,LTD
B8B2EB	Googol Technology (HK) Limited
B8B3DC	DEREK (SHAOGUAN) LIMITED
B8B42E	Gionee Communication Equipment Co,Ltd.ShenZhen
B8B7D7	2GIG Technologies
B8B81E	Intel Corporate
B8B94E	Shenzhen iBaby Labs, Inc.
B8BA68	Xi'an Jizhong Digital Communication Co.,Ltd
B8BA72	Cynove
B8BB23	Guangdong Nufront CSC Co., Ltd
B8BB6D	ENERES Co.,Ltd.
B8BBAF	Samsung Electronics Co.,Ltd
B8BC1B	HUAWEI TECHNOLOGIES CO.,LTD
B8BD79	TrendPoint Systems
B8BEBF	Cisco Systems, Inc
B8BF83	Intel Corporate
B8C1A2	Dragon Path Technologies Co., Limited
B8C3BF	Henan Chengshi NetWork Technology Co.，Ltd
B8C46F	PRIMMCON INDUSTRIES INC
B8C68E	Samsung Electronics Co.,Ltd
B8C716	Fiberhome Telecommunication Technologies Co.,LTD
B8C75D	Apple, Inc.
B8C855	Shanghai GBCOM Communication Technology Co.,Ltd.
B8CA3A	Dell Inc.
B8CD93	Penetek, Inc
B8CDA7	Maxeler Technologies Ltd.
B8D06F	GUANGZHOU HKUST FOK YING TUNG RESEARCH INSTITUTE
B8D49D	M Seven System Ltd.
B8D50B	Sunitec Enterprise Co.,Ltd
B8D7AF	Murata Manufacturing Co., Ltd.
B8D812	IEEE Registration Authority
B8D9CE	Samsung Electronics Co.,Ltd
B8DAF1	Strahlenschutz- Entwicklungs- und Ausruestungsgesellschaft mbH
B8DAF7	Advanced Photonics, Inc.
B8DC87	IAI Corporation
B8DF6B	SpotCam Co., Ltd.
B8E589	Payter BV
B8E625	2Wire Inc
B8E779	9Solutions Oy
B8E856	Apple, Inc.
B8E937	Sonos, Inc.
B8EAAA	ICG NETWORKS CO.,ltd
B8ECA3	ZyXEL Communications Corporation
B8EE65	Liteon Technology Corporation
B8EE79	YWire Technologies, Inc.
B8F080	SPS, INC.
B8F317	iSun Smasher Communications Private Limited
B8F4D0	Herrmann Ultraschalltechnik GmbH & Co. Kg
B8F5E7	WayTools, LLC
B8F6B1	Apple, Inc.
B8F732	Aryaka Networks Inc
B8F828	Changshu Gaoshida Optoelectronic Technology Co. Ltd.
B8F883	TP-LINK TECHNOLOGIES CO.,LTD.
B8F8BE	Bluecom
B8F934	Sony Mobile Communications AB
B8FC9A	Le Shi Zhi Xin Electronic Technology (Tianjin) Limited
B8FD32	Zhejiang ROICX Microelectronics
B8FF61	Apple, Inc.
B8FF6F	Shanghai Typrotech Technology Co.Ltd
B8FFB3	MitraStar Technology Corp.
B8FFFE	Texas Instruments
BC0200	Stewart Audio
BC024A	HMD Global Oy
BC0543	AVM GmbH
BC0DA5	Texas Instruments
BC0F2B	FORTUNE TECHGROUP CO.,LTD
BC0F64	Intel Corporate
BC125E	Beijing  WisVideo  INC.
BC1401	Hitron Technologies. Inc
BC1485	Samsung Electronics Co.,Ltd
BC14EF	ITON Technology Limited
BC15A6	Taiwan Jantek Electronics,Ltd.
BC15AC	Vodafone Italia S.p.A.
BC1665	Cisco Systems, Inc
BC16F5	Cisco Systems, Inc
BC1A67	YF Technology Co., Ltd
BC20A4	Samsung Electronics Co.,Ltd
BC20BA	Inspur (Shandong) Electronic Information Co., Ltd
BC25E0	HUAWEI TECHNOLOGIES CO.,LTD
BC25F0	3D Display Technologies Co., Ltd.
BC261D	HONG KONG TECON TECHNOLOGY
BC282C	e-Smart Systems Pvt. Ltd
BC2846	NextBIT Computing Pvt. Ltd.
BC28D6	Rowley Associates Limited
BC2B6B	Beijing Haier IC Design Co.,Ltd
BC2BD7	Revogi Innovation Co., Ltd.
BC2C55	Bear Flag Design, Inc.
BC2D98	ThinGlobal LLC
BC2F3D	vivo Mobile Communication Co., Ltd.
BC305B	Dell Inc.
BC307D	Wistron Neweb Corporation
BC307E	Wistron Neweb Corporation
BC3400	IEEE Registration Authority
BC35E5	Hydro Systems Company
BC38D2	Pandachip Limited
BC39A6	CSUN System Technology Co.,LTD
BC39D9	Z-Tec
BC3AEA	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
BC3BAF	Apple, Inc.
BC3E13	Accordance Systems Inc.
BC3F8F	HUAWEI TECHNOLOGIES CO.,LTD
BC4100	CODACO ELECTRONIC s.r.o.
BC4377	Hang Zhou Huite Technology Co.,ltd.
BC4434	Shenzhen TINNO Mobile Technology Corp.
BC4486	Samsung Electronics Co.,Ltd
BC44B0	Elastifile
BC452E	Knowledge Development for POF S.L.
BC4699	TP-LINK TECHNOLOGIES CO.,LTD.
BC4760	Samsung Electronics Co.,Ltd
BC4B79	SensingTek
BC4CC4	Apple, Inc.
BC4DFB	Hitron Technologies. Inc
BC4E3C	CORE STAFF CO., LTD.
BC4E5D	ZhongMiao Technology Co., Ltd.
BC51FE	Swann communications Pty Ltd
BC52B4	Nokia
BC52B7	Apple, Inc.
BC5436	Apple, Inc.
BC54F9	Drogoo Technology Co., Ltd.
BC5C4C	ELECOM CO.,LTD.
BC5FF4	ASRock Incorporation
BC5FF6	SHENZHEN MERCURY COMMUNICATION TECHNOLOGIES CO.,LTD.
BC6010	Qingdao Hisense Communications Co.,Ltd.
BC60A7	Sony Interactive Entertainment Inc.
BC620E	HUAWEI TECHNOLOGIES CO.,LTD
BC629F	Telenet Systems P. Ltd.
BC644B	ARRIS Group, Inc.
BC6641	IEEE Registration Authority
BC66DE	Shadow Creator Information Technology Co.,Ltd.
BC671C	Cisco Systems, Inc
BC6778	Apple, Inc.
BC6784	Environics Oy
BC6A16	Tdvine
BC6A29	Texas Instruments
BC6A2F	Henge Docks LLC
BC6A44	Commend International GmbH
BC6B4D	Nokia
BC6C21	Apple, Inc.
BC6E64	Sony Mobile Communications AB
BC6E76	Green Energy Options Ltd
BC71C1	XTrillion, Inc.
BC72B1	Samsung Electronics Co.,Ltd
BC74D7	HangZhou JuRu Technology CO.,LTD
BC7574	HUAWEI TECHNOLOGIES CO.,LTD
BC764E	Rackspace US, Inc.
BC765E	Samsung Electronics Co.,Ltd
BC7670	HUAWEI TECHNOLOGIES CO.,LTD
BC7737	Intel Corporate
BC779F	SBM Co., Ltd.
BC79AD	Samsung Electronics Co.,Ltd
BC7DD1	Radio Data Comms
BC811F	Ingate Systems
BC8199	BASIC Co.,Ltd.
BC8385	Microsoft Corporation
BC83A7	SHENZHEN CHUANGWEI-RGB ELECTRONICS CO.,LTD
BC851F	Samsung Electronics Co.,Ltd
BC8556	Hon Hai Precision Ind. Co.,Ltd.
BC8893	VILLBAU Ltd.
BC8AA3	NHN Entertainment
BC8AE8	QING DAO HAIER TELECOM CO.,LTD.
BC8B55	NPP ELIKS America Inc. DBA T&M Atlantic
BC8CCD	SAMSUNG ELECTRO-MECHANICS(THAILAND)
BC8D0E	Nokia
BC926B	Apple, Inc.
BC9680	Shenzhen Gongjin Electronics Co.,Ltd
BC9889	Fiberhome Telecommunication Technologies Co.,LTD
BC99BC	FonSee Technology Inc.
BC9C31	HUAWEI TECHNOLOGIES CO.,LTD
BC9CC5	Beijing Huafei Technology Co., Ltd.
BC9DA5	DASCOM Europe GmbH
BC9FEF	Apple, Inc.
BCA042	SHANGHAI FLYCO ELECTRICAL APPLIANCE CO.,LTD
BCA4E1	Nabto
BCA8A6	Intel Corporate
BCA920	Apple, Inc.
BCA9D6	Cyber-Rain, Inc.
BCAD28	Hangzhou Hikvision Digital Technology Co.,Ltd.
BCADAB	Avaya Inc
BCAEC5	ASUSTek COMPUTER INC.
BCB181	SHARP CORPORATION
BCB1F3	Samsung Electronics Co.,Ltd
BCB308	HONGKONG RAGENTEK COMMUNICATION TECHNOLOGY CO.,LIMITED
BCB852	Cybera, Inc.
BCBAE1	AREC Inc.
BCBBC9	Kellendonk Elektronik GmbH
BCBC46	SKS Welding Systems GmbH
BCC00F	Fiberhome Telecommunication Technologies Co.,LTD
BCC168	DinBox Sverige AB
BCC23A	Thomson Video Networks
BCC342	Panasonic System Networks Co., Ltd.
BCC493	Cisco Systems, Inc
BCC61A	SPECTRA EMBEDDED SYSTEMS
BCC6DB	Nokia Corporation
BCC810	Cisco SPVTG
BCCAB5	ARRIS Group, Inc.
BCCD45	Voismart
BCCFCC	HTC Corporation
BCD11F	Samsung Electronics Co.,Ltd
BCD165	Cisco SPVTG
BCD177	TP-LINK TECHNOLOGIES CO.,LTD.
BCD1D3	Shenzhen TINNO Mobile Technology Corp.
BCD5B6	d2d technologies
BCD940	ASR Co,.Ltd.
BCE09D	Eoslink
BCE59F	WATERWORLD Technology Co.,LTD
BCE63F	Samsung Electronics Co.,Ltd
BCE767	Quanzhou  TDX Electronics Co., Ltd
BCEA2B	CityCom GmbH
BCEAFA	Hewlett Packard
BCEB5F	Fujian Beifeng Telecom Technology Co., Ltd.
BCEC23	SHENZHEN CHUANGWEI-RGB ELECTRONICS CO.,LTD
BCEC5D	Apple, Inc.
BCEE7B	ASUSTek COMPUTER INC.
BCF1F2	Cisco Systems, Inc
BCF2AF	devolo AG
BCF5AC	LG Electronics (Mobile Communications)
BCF61C	Geomodeling Wuxi Technology Co. Ltd.
BCF685	D-Link International
BCF811	Xiamen DNAKE Technology Co.,Ltd
BCFE8C	Altronic, LLC
BCFFAC	TOPCON CORPORATION
C00000	Western Digital (may be reversed 00 00 C0?)
C0028D	WINSTAR Display CO.,Ltd
C005C2	ARRIS Group, Inc.
C00D7E	Additech, Inc.
C01173	Samsung Electronics Co.,Ltd
C011A6	Fort-Telecom ltd.
C01242	Alpha Security Products
C0143D	Hon Hai Precision Ind. Co.,Ltd.
C01885	Hon Hai Precision Ind. Co.,Ltd.
C01ADA	Apple, Inc.
C01E9B	Pixavi AS
C0210D	SHENZHEN RF-LINK TECHNOLOGY CO.,LTD.
C02250	Private
C02506	AVM GmbH
C0255C	Cisco Systems, Inc
C02567	Nexxt Solutions
C025A2	NEC Platforms, Ltd.
C025E9	TP-LINK TECHNOLOGIES CO.,LTD.
C027B9	Beijing National Railway Research & Design Institute  of Signal & Communication Co., Ltd.
C0288D	Logitech, Inc
C02973	Audyssey Laboratories Inc.
C029F3	Xysystem
C02BFC	iNES. applied informatics GmbH
C02C7A	Shenzhen Horn Audio Co.,Ltd.
C02DEE	Cuff
C02FF1	Volta Networks
C0335E	Microsoft
C034B4	Gigastone Corporation
C03580	A&R TECH
C035BD	Velocytech Aps
C035C5	Prosoft Systems LTD
C03896	Hon Hai Precision Ind. Co.,Ltd.
C038F9	Nokia Danmark A/S
C03B8F	Minicom Digital Signage
C03D46	Shanghai Sango Network Technology Co.,Ltd
C03E0F	BSkyB Ltd
C03F0E	Netgear
C03F2A	Biscotti, Inc.
C03FD5	Elitegroup Computer Systems Co.,Ltd.
C041F6	LG ELECTRONICS INC
C04301	Epec Oy
C044E3	Shenzhen Sinkna Electronics Co., LTD
C0493D	MAITRISE TECHNOLOGIQUE
C04A00	TP-LINK TECHNOLOGIES CO.,LTD.
C04A09	Zhejiang Everbright Communication Equip. Co,. Ltd
C04DF7	Serelec
C05627	Belkin International Inc.
C056E3	Hangzhou Hikvision Digital Technology Co.,Ltd.
C057BC	Avaya Inc
C058A7	Pico Systems Co., Ltd.
C05E6F	V. Stonkaus firma Kodinis Raktas
C05E79	SHENZHEN HUAXUN ARK TECHNOLOGIES CO.,LTD
C06118	TP-LINK TECHNOLOGIES CO.,LTD.
C0626B	Cisco Systems, Inc
C06394	Apple, Inc.
C064C6	Nokia Corporation
C06599	Samsung Electronics Co.,Ltd
C067AF	Cisco Systems, Inc
C06C0F	Dobbs Stanford
C06C6D	MagneMotion, Inc.
C07009	HUAWEI TECHNOLOGIES CO.,LTD
C07BBC	Cisco Systems, Inc
C07CD1	PEGATRON CORPORATION
C07E40	SHENZHEN XDK COMMUNICATION EQUIPMENT CO.,LTD
C08170	Effigis GeoSolutions
C0830A	2Wire Inc
C0847A	Apple, Inc.
C08488	Finis Inc
C0854C	Ragentek Technology Group
C0885B	SnD Tech Co., Ltd.
C08997	Samsung Electronics Co.,Ltd
C08ADE	Ruckus Wireless
C08B6F	S I Sistemas Inteligentes Eletrônicos Ltda
C08C60	Cisco Systems, Inc
C09132	Patriot Memory
C09134	ProCurve Networking by HP
C09727	SAMSUNG ELECTRO-MECHANICS(THAILAND)
C09879	Acer Inc.
C098E5	University of Michigan
C09A71	XIAMEN MEITU MOBILE TECHNOLOGY CO.LTD
C09C04	Shaanxi GuoLian Digital TV Technology Co.,Ltd.
C09C92	Coby
C09D26	Topicon HK Lmd.
C09F05	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
C09F42	Apple, Inc.
C0A0BB	D-Link International
C0A0C7	FAIRFIELD INDUSTRIES
C0A0DE	Multi Touch Oy
C0A0E2	Eden Innovations
C0A1A2	MarqMetrix
C0A26D	Abbott Point of Care
C0A364	3D Systems Massachusetts
C0A39E	EarthCam, Inc.
C0AA68	OSASI Technos Inc.
C0AC54	Sagemcom Broadband SAS
C0B339	Comigo Ltd.
C0B357	Yoshiki Electronics Industry Ltd.
C0B713	Beijing Xiaoyuer Technology Co. Ltd.
C0B8B1	BitBox Ltd
C0BAE6	Application Solutions (Electronics and Vision) Ltd
C0BD42	ZPA Smart Energy a.s.
C0BDD1	SAMSUNG ELECTRO-MECHANICS(THAILAND)
C0BFC0	HUAWEI TECHNOLOGIES CO.,LTD
C0C1C0	Cisco-Linksys, LLC
C0C3B6	Automatic Systems
C0C520	Ruckus Wireless
C0C522	ARRIS Group, Inc.
C0C569	SHANGHAI LYNUC CNC TECHNOLOGY CO.,LTD
C0C687	Cisco SPVTG
C0C946	MITSUYA LABORATORIES INC.
C0C976	Shenzhen TINNO Mobile Technology Corp.
C0CB38	Hon Hai Precision Ind. Co.,Ltd.
C0CCF8	Apple, Inc.
C0CECD	Apple, Inc.
C0CFA3	Creative Electronics & Software, Inc.
C0D012	Apple, Inc.
C0D044	Sagemcom Broadband SAS
C0D391	IEEE Registration Authority
C0D3C0	Samsung Electronics Co.,Ltd
C0D962	ASKEY COMPUTER CORP
C0D9F7	ShanDong Domor Intelligent S&T CO.,Ltd
C0DA74	Hangzhou Sunyard Technology Co., Ltd.
C0DC6A	Qingdao Eastsoft Communication Technology Co.,LTD
C0DF77	Conrad Electronic SE
C0E422	Texas Instruments
C0E42D	TP-LINK TECHNOLOGIES CO.,LTD.
C0E54E	ARIES Embedded GmbH
C0EAE4	Sonicwall
C0EE40	Laird Technologies
C0EEFB	OnePlus Tech (Shenzhen) Ltd
C0F1C4	Pacidal Corporation Ltd.
C0F2FB	Apple, Inc.
C0F636	Hangzhou Kuaiyue Technologies, Ltd.
C0F79D	Powercode
C0F8DA	Hon Hai Precision Ind. Co.,Ltd.
C0F945	Toshiba Toko Meter Systems Co., LTD.
C0F991	GME Standard Communications P/L
C0FFD4	Netgear
C40006	Lipi Data Systems Ltd.
C40049	Kamama
C40142	MaxMedia Technology Limited
C4017C	Ruckus Wireless
C401B1	SeekTech INC
C401CE	PRESITION (2000) CO., LTD.
C40415	Netgear
C4047B	Shenzhen YOUHUA Technology Co., Ltd
C40528	HUAWEI TECHNOLOGIES CO.,LTD
C4072F	HUAWEI TECHNOLOGIES CO.,LTD
C4084A	Nokia
C40880	Shenzhen UTEPO Tech Co., Ltd.
C40938	FUJIAN STAR-NET COMMUNICATION CO.,LTD
C40ACB	Cisco Systems, Inc
C40BCB	Xiaomi Communications Co Ltd
C40E45	ACK Networks,Inc.
C40F09	Hermes electronic GmbH
C4108A	Ruckus Wireless
C411E0	Bull Group Co., Ltd
C412F5	D-Link International
C413E2	Aerohive Networks Inc.
C4143C	Cisco Systems, Inc
C416FA	Prysm Inc
C417FE	Hon Hai Precision Ind. Co.,Ltd.
C4198B	Dominion Voting Systems Corporation
C419EC	Qualisys AB
C41CFF	Vizio, Inc
C41ECE	HMI Sources Ltd.
C421C8	KYOCERA Corporation
C4237A	WhizNets Inc.
C4242E	Galvanic Applied Sciences Inc
C42628	Airo Wireless
C42795	Technicolor CH USA Inc.
C4282D	Embedded Intellect Pty Ltd
C4291D	KLEMSAN ELEKTRIK ELEKTRONIK SAN.VE TIC.AS.
C42C03	Apple, Inc.
C42F90	Hangzhou Hikvision Digital Technology Co.,Ltd.
C43018	MCS Logic Inc.
C4346B	Hewlett Packard
C43655	Shenzhen Fenglian Technology Co., Ltd.
C4366C	LG Innotek
C436DA	Rusteletech Ltd.
C438D3	TAGATEC CO.,LTD
C4393A	SMC Networks Inc
C43A9F	Siconix Inc.
C43ABE	Sony Mobile Communications AB
C43C3C	CYBELEC SA
C43DC7	Netgear
C44044	RackTop Systems Inc.
C44202	Samsung Electronics Co.,Ltd
C4438F	LG Electronics (Mobile Communications)
C44567	SAMBON PRECISON and ELECTRONICS
C445EC	Shanghai Yali Electron Co.,LTD
C44619	Hon Hai Precision Ind. Co.,Ltd.
C4473F	HUAWEI TECHNOLOGIES CO.,LTD
C44838	Satcom Direct, Inc.
C449BB	MITSUMI ELECTRIC CO.,LTD.
C44AD0	FIREFLIES SYSTEMS
C44B44	Omniprint Inc.
C44BD1	Wallys Communications  Teachnologies Co.,Ltd.
C44E1F	Bluen
C44EAC	Shenzhen Shiningworth Technology Co., Ltd.
C45006	Samsung Electronics Co.,Ltd
C45444	QUANTA COMPUTER INC.
C455A6	Cadac Holdings Ltd
C455C2	Bach-Simpson
C45600	Galleon Embedded Computing
C456FE	Lava International Ltd.
C4576E	Samsung Electronics Co.,Ltd
C458C2	Shenzhen TATFOOK Technology Co., Ltd.
C45976	Fugoo Coorporation
C45DD8	HDMI Forum
C46044	Everex Electronics Limited
C4626B	ZPT Vigantice
C462EA	Samsung Electronics Co.,Ltd
C46354	U-Raku, Inc.
C46413	Cisco Systems, Inc
C46699	vivo Mobile Communication Co., Ltd.
C467B5	Libratone A/S
C4693E	Turbulence Design Inc.
C46AB7	Xiaomi Communications Co Ltd
C46BB4	Myidkey
C46DF1	DataGravity
C46E1F	TP-LINK TECHNOLOGIES CO.,LTD.
C4700B	GUANGZHOU CHIP TECHNOLOGIES CO.,LTD
C47130	Fon Technology S.L.
C471FE	Cisco Systems, Inc
C47295	Cisco Systems, Inc
C4731E	Samsung Electronics Co.,Ltd
C477AB	Beijing ASU Tech Co.,Ltd
C47B2F	Beijing JoinHope Image Technology Ltd.
C47BA3	NAVIS Inc.
C47C8D	IEEE Registration Authority
C47D46	FUJITSU LIMITED
C47D4F	Cisco Systems, Inc
C47DCC	Zebra Technologies Inc
C47DFE	A.N. Solutions GmbH
C47F51	Inventek Systems
C4823F	Fujian Newland Auto-ID Tech. Co,.Ltd.
C4824E	Changzhou Uchip Electronics Co., LTD.
C4836F	Ciena Corporation
C48508	Intel Corporate
C486E9	HUAWEI TECHNOLOGIES CO.,LTD
C488E5	Samsung Electronics Co.,Ltd
C48E8F	Hon Hai Precision Ind. Co.,Ltd.
C48F07	Shenzhen Yihao Hulian Science and Technology Co., Ltd.
C4913A	Shenzhen Sanland Electronic Co., ltd.
C4924C	KEISOKUKI CENTER CO.,LTD.
C49300	8devices
C49313	100fio networks technology llc
C49380	Speedytel technology
C495A2	SHENZHEN WEIJIU INDUSTRY AND TRADE DEVELOPMENT CO., LTD
C49805	Minieum Networks, Inc
C49A02	LG Electronics (Mobile Communications)
C49DED	Microsoft Corporation
C49E41	G24 Power Limited
C49FF3	Mciao Technologies, Inc.
C4A366	zte corporation
C4A81D	D-Link International
C4AAA1	SUMMIT DEVELOPMENT, spol.s r.o.
C4ABB2	vivo Mobile Communication Co., Ltd.
C4AD21	MEDIAEDGE Corporation
C4ADF1	GOPEACE Inc.
C4AE12	Samsung Electronics Co.,Ltd
C4B301	Apple, Inc.
C4B512	General Electric Digital Energy
C4B9CD	Cisco Systems, Inc
C4BA99	I+ME Actia Informatik und Mikro-Elektronik GmbH
C4BAA3	Beijing Winicssec Technologies Co., Ltd.
C4BB4C	Zebra Information Tech Co. Ltd
C4BBEA	Pakedge Device and Software Inc
C4BD6A	SKF GmbH
C4BE84	Texas Instruments
C4BED4	Avaya Inc
C4C0AE	MIDORI ELECTRONIC CO., LTD.
C4C19F	National Oilwell Varco Instrumentation, Monitoring, and Optimization (NOV IMO)
C4C755	Beijing HuaqinWorld Technology Co.,Ltd
C4C919	Energy Imports Ltd
C4C9EC	Gugaoo   HK Limited
C4CAD9	Hangzhou H3C Technologies Co., Limited
C4CD45	Beijing Boomsense Technology CO.,LTD.
C4D197	Ventia Utility Services
C4D489	JiangSu Joyque Information Industry Co.,Ltd
C4D655	Tercel technology co.,ltd
C4D987	Intel Corporate
C4DA26	NOBLEX SA
C4DA7D	Ivium Technologies B.V.
C4E032	IEEE 1904.1 Working Group
C4E17C	U2S co.
C4E510	Mechatro, Inc.
C4E7BE	SCSpro Co.,Ltd
C4E92F	AB Sciex
C4E984	TP-LINK TECHNOLOGIES CO.,LTD.
C4EA1D	Technicolor
C4EBE3	RRCN SAS
C4EDBA	Texas Instruments
C4EEAE	VSS Monitoring
C4EEF5	II-VI Incorporated
C4EF70	Home Skinovations
C4F081	HUAWEI TECHNOLOGIES CO.,LTD
C4F1D1	BEIJING SOGOU TECHNOLOGY DEVELOPMENT CO., LTD.
C4F464	Spica international
C4F57C	Brocade Communications Systems, Inc.
C4F5A5	Kumalift Co., Ltd.
C4FCE4	DishTV NZ Ltd
C4FF1F	HUAWEI TECHNOLOGIES CO.,LTD
C80084	Cisco Systems, Inc
C80210	LG Innotek
C80258	ITW GSE ApS
C8028F	Nova Electronics (Shanghai) Co., Ltd.
C802A6	Beijing Newmine Technology
C80718	Tdsi
C808E9	LG Electronics
C80AA9	QUANTA COMPUTER INC.
C80CC8	HUAWEI TECHNOLOGIES CO.,LTD
C80E14	AVM Audiovisuelles Marketing und Computersysteme GmbH
C80E77	Le Shi Zhi Xin Electronic Technology (Tianjin) Limited
C80E95	OmniLync Inc.
C81073	CENTURY OPTICOMM CO.,LTD
C81451	HUAWEI TECHNOLOGIES CO.,LTD
C81479	Samsung Electronics Co.,Ltd
C816A5	Masimo Corporation
C816BD	Qingdao Hisense Communications Co.,Ltd.
C819F7	Samsung Electronics Co.,Ltd
C81AFE	DLOGIC GmbH
C81B5C	Bctech
C81B6B	Innova Security
C81E8E	ADV Security (S) Pte Ltd
C81EE7	Apple, Inc.
C81F66	Dell Inc.
C81FBE	HUAWEI TECHNOLOGIES CO.,LTD
C8208E	Storagedata
C82158	Intel Corporate
C825E1	Lemobile Information Technology (Beijing) Co., Ltd
C8292A	Barun Electronics
C82A14	Apple, Inc.
C82E94	Halfa Enterprise Co., Ltd.
C83168	eZEX corporation
C83232	Hunting Innova
C8334B	Apple, Inc.
C8348E	Intel Corporate
C835B8	Ericsson, EAB/RWI/K
C83870	Samsung Electronics Co.,Ltd
C83A35	Tenda Technology Co., Ltd.
C83A6B	Roku, Inc
C83B45	Jri
C83D97	Nokia Corporation
C83DD4	CyberTAN Technology Inc.
C83DFC	Pioneer DJ Corporation
C83E99	Texas Instruments
C83EA7	KUNBUS GmbH
C83F26	Microsoft Corporation
C83FB4	ARRIS Group, Inc.
C84529	IMK Networks Co.,Ltd
C84544	Asia Pacific CIS (Wuxi) Co, Ltd
C8458F	Wyler AG
C8478C	Beken Corporation
C848F5	MEDISON Xray Co., Ltd
C84C75	Cisco Systems, Inc
C85195	HUAWEI TECHNOLOGIES CO.,LTD
C85645	Intermas France
C85663	Sunflex Europe GmbH
C85B76	LCFC(HeFei) Electronics Technology co., ltd
C86000	ASUSTek COMPUTER INC.
C864C7	zte corporation
C8662C	Beijing Haitai Fangyuan High Technology Co,.Ltd.
C8665D	Aerohive Networks Inc.
C8675E	Aerohive Networks Inc.
C869CD	Apple, Inc.
C86C1E	Display Systems Ltd
C86C87	ZyXEL Communications Corporation
C86CB6	Optcom Co., Ltd.
C86F1D	Apple, Inc.
C87248	Aplicom Oy
C87324	Sow Cheng Technology Co. Ltd.
C8755B	Quantify Technology Pty. Ltd.
C8778B	Themis Computer
C87B5B	zte corporation
C87CBC	Valink Co., Ltd.
C87D77	Shenzhen Kingtech Communication Equipment Co.,Ltd
C87E75	Samsung Electronics Co.,Ltd
C88439	Sunrise Technologies
C88447	Beautiful Enterprise Co., Ltd
C88550	Apple, Inc.
C88722	Lumenpulse
C8873B	Net Optics
C88A83	Dongguan HuaHong Electronics Co.,Ltd
C88B47	Nolangroup S.P.A con Socio Unico
C88D83	HUAWEI TECHNOLOGIES CO.,LTD
C88ED1	IEEE Registration Authority
C8903E	Pakton Technologies
C891F9	Sagemcom Broadband SAS
C89346	MXCHIP Company Limited
C89383	Embedded Automation, Inc.
C894BB	HUAWEI TECHNOLOGIES CO.,LTD
C894D2	Jiangsu Datang  Electronic Products Co., Ltd
C8979F	Nokia Corporation
C89C1D	Cisco Systems, Inc
C89CDC	Elitegroup Computer Systems Co.,Ltd.
C89F1D	SHENZHEN COMMUNICATION TECHNOLOGIES CO.,LTD
C89F42	VDII Innovation AB
C8A030	Texas Instruments
C8A1B6	Shenzhen Longway Technologies Co., Ltd
C8A1BA	Neul Ltd
C8A2CE	Oasis Media Systems LLC
C8A620	Nebula, Inc
C8A70A	Verizon Business
C8A729	SYStronics Co., Ltd.
C8A823	Samsung Electronics Co.,Ltd
C8A9FC	Goyoo Networks Inc.
C8AA21	ARRIS Group, Inc.
C8AA55	Hunan Comtom Electronic Incorporated Co.,Ltd
C8AACC	Private
C8AE9C	Shanghai TYD Elecronic Technology Co. Ltd
C8AF40	marco Systemanalyse und Entwicklung GmbH
C8AFE3	Hefei Radio Communication Technology Co., Ltd
C8B21E	CHIPSEA TECHNOLOGIES (SHENZHEN) CORP.
C8B373	Cisco-Linksys, LLC
C8B5AD	Hewlett Packard Enterprise
C8B5B7	Apple, Inc.
C8BA94	SAMSUNG ELECTRO-MECHANICS(THAILAND)
C8BBD3	Embrane
C8BCC8	Apple, Inc.
C8BE19	D-Link International
C8C126	ZPM Industria e Comercio Ltda
C8C13C	RuggedTek Hangzhou Co., Ltd
C8C2C6	Shanghai Airm2m Communication Technology Co., Ltd
C8C50E	Shenzhen Primestone Network Technologies.Co., Ltd.
C8C791	Zero1.tv GmbH
C8CBB8	Hewlett Packard
C8CD72	Sagemcom Broadband SAS
C8D019	Shanghai Tigercel Communication Technology Co.,Ltd
C8D10B	Nokia Corporation
C8D15E	HUAWEI TECHNOLOGIES CO.,LTD
C8D1D1	AGAiT Technology Corporation
C8D2C1	Jetlun (Shenzhen) Corporation
C8D3A3	D-Link International
C8D3FF	Hewlett Packard
C8D429	Muehlbauer AG
C8D590	FLIGHT DATA SYSTEMS
C8D5FE	Shenzhen Zowee Technology Co., Ltd
C8D719	Cisco-Linksys, LLC
C8D779	Qingdao Haier Telecom Co.，Ltd
C8DDC9	Lenovo Mobile Communication Technology Ltd.
C8DE51	Integra Networks, Inc.
C8DF7C	Nokia Corporation
C8E0EB	Apple, Inc.
C8E130	Milkyway Group Ltd
C8E1A7	Vertu Corporation Limited
C8E42F	Technical Research Design and Development
C8E776	PTCOM Technology
C8E7D8	SHENZHEN MERCURY COMMUNICATION TECHNOLOGIES CO.,LTD.
C8EE08	TANGTOP TECHNOLOGY CO.,LTD
C8EE75	Pishion International Co. Ltd
C8EEA6	Shenzhen SHX Technology Co., Ltd
C8EF2E	Beijing Gefei Tech. Co., Ltd
C8F230	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
C8F36B	Yamato Scale Co.,Ltd.
C8F386	Shenzhen Xiaoniao Technology Co.,Ltd
C8F406	Avaya Inc
C8F650	Apple, Inc.
C8F68D	S.E.TECHNOLOGIES LIMITED
C8F704	Building Block Video
C8F733	Intel Corporate
C8F86D	Alcatel-               # Alcatel-Lucent Shanghai Bell Co., Ltd
C8F946	LOCOSYS Technology Inc.
C8F981	Seneca s.r.l.
C8F9C8	NewSharp Technology(SuZhou)Co,Ltd
C8F9F9	Cisco Systems, Inc
C8FB26	Cisco SPVTG
C8FD19	Texas Instruments
C8FE30	Bejing DAYO Mobile Communication Technology Ltd.
C8FF28	Liteon Technology Corporation
C8FF77	Dyson Limited
CC0080	BETTINI SRL
CC03FA	Technicolor CH USA Inc.
CC047C	G-WAY Microwave
CC04B4	Select Comfort
CC051B	Samsung Electronics Co.,Ltd
CC07AB	Samsung Electronics Co.,Ltd
CC07E4	Lenovo Mobile Communication Technology Ltd.
CC088D	Apple, Inc.
CC08E0	Apple, Inc.
CC09C8	IMAQLIQ LTD
CC0CDA	Miljovakt AS
CC0DEC	Cisco SPVTG
CC10A3	Beijing Nan Bao Technology Co., Ltd.
CC14A6	Yichun MyEnergy Domain, Inc
CC167E	Cisco Systems, Inc
CC187B	Manzanita Systems, Inc.
CC19A8	PT Inovação e Sistemas SA
CC1AFA	zte corporation
CC1BE0	IEEE Registration Authority
CC1EFF	Metrological Group BV
CC1FC4	Invue
CC20E8	Apple, Inc.
CC2218	InnoDigital Co., Ltd.
CC25EF	Apple, Inc.
CC262D	Verifi, LLC
CC29F5	Apple, Inc.
CC2A80	Micro-Biz intelligence solutions Co.,Ltd
CC2D21	Tenda Technology Co.,Ltd.Dongguan branch
CC2D83	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
CC2D8C	LG ELECTRONICS INC
CC3080	VAIO Corporation
CC33BB	Sagemcom Broadband SAS
CC3429	TP-LINK TECHNOLOGIES CO.,LTD.
CC34D7	GEWISS S.P.A.
CC3540	Technicolor CH USA Inc.
CC37AB	Edgecore Networks Corportation
CC398C	Shiningtek
CC3A61	SAMSUNG ELECTRO MECHANICS CO., LTD.
CC3ADF	Private
CC3B3E	Lester Electrical
CC3C3F	SA.S.S. Datentechnik AG
CC3D82	Intel Corporate
CC3E5F	Hewlett Packard
CC3F1D	Intesis Software SL
CC43E3	Trump s.a.
CC4463	Apple, Inc.
CC46D6	Cisco Systems, Inc
CC4703	Intercon Systems Co., Ltd.
CC4AE1	Fourtec-               # fourtec -Fourier Technologies
CC4BFB	Hellberg Safety AB
CC4E24	Brocade Communications Systems, Inc.
CC4EEC	HUMAX Co., Ltd.
CC500A	Fiberhome Telecommunication Technologies Co.,LTD
CC501C	KVH Industries, Inc.
CC5076	Ocom Communications, Inc.
CC52AF	Universal Global Scientific Industrial Co., Ltd.
CC53B5	HUAWEI TECHNOLOGIES CO.,LTD
CC5459	OnTime Networks AS
CC55AD	Rim
CC593E	TOUMAZ LTD
CC5C75	Weightech Com. Imp. Exp. Equip. Pesagem Ltda
CC5D4E	ZyXEL Communications Corporation
CC5D57	Information  System Research Institute,Inc.
CC5FBF	Topwise 3G Communication Co., Ltd.
CC60BB	Empower RF Systems
CC61E5	Motorola Mobility LLC, a Lenovo Company
CC65AD	ARRIS Group, Inc.
CC69B0	Global Traffic Technologies, LLC
CC6B98	Minetec Wireless Technologies
CC6BF1	Sound Masking Inc.
CC6DA0	Roku, Inc.
CC6DEF	TJK Tietolaite Oy
CC720F	Viscount Systems Inc.
CC7314	HONG KONG WHEATEK TECHNOLOGY LIMITED
CC7498	Filmetrics Inc.
CC7669	Seetech
CC785F	Apple, Inc.
CC78AB	Texas Instruments
CC794A	BLU Products Inc.
CC79CF	SHENZHEN RF-LINK TECHNOLOGY CO.,LTD.
CC7A30	CMAX Wireless Co., Ltd.
CC7B35	zte corporation
CC7D37	ARRIS Group, Inc.
CC7EE7	Panasonic AVC Networks Company
CC81DA	SHANGHAI PHICOMM COMMUNICATION CO.,LTD
CC82EB	KYOCERA CORPORATION
CC856C	SHENZHEN MDK DIGITAL TECHNOLOGY CO.,LTD
CC89FD	Nokia Corporation
CC8CDA	Shenzhen Wei Da Intelligent Technology Go.,Ltd
CC8CE3	Texas Instruments
CC9093	Hansong Tehnologies
CC90E8	Shenzhen YOUHUA Technology Co., Ltd
CC912B	TE Connectivity Touch Solutions
CC944A	Pfeiffer Vacuum GmbH
CC9470	Kinestral Technologies, Inc.
CC95D7	Vizio, Inc
CC9635	LVS Co.,Ltd.
CC96A0	HUAWEI TECHNOLOGIES CO.,LTD
CC9E00	Nintendo Co., Ltd.
CC9F35	Transbit Sp. z o.o.
CC9F7A	Chiun Mai Communication Systems, Inc
CCA0E5	DZG Metering GmbH
CCA219	SHENZHEN ALONG INVESTMENT CO.,LTD
CCA223	HUAWEI TECHNOLOGIES CO.,LTD
CCA260	SICHUAN TIANYI COMHEART TELECOMCO.,LTD
CCA374	Guangdong Guanglian Electronic Technology Co.Ltd
CCA462	ARRIS Group, Inc.
CCA4AF	Shenzhen Sowell Technology Co., LTD
CCA614	AIFA TECHNOLOGY CORP.
CCAF78	Hon Hai Precision Ind. Co.,Ltd.
CCB0DA	Liteon Technology Corporation
CCB11A	Samsung Electronics Co.,Ltd
CCB255	D-Link International
CCB3AB	shenzhen Biocare Bio-Medical Equipment Co.,Ltd.
CCB3F8	FUJITSU ISOTEC LIMITED
CCB55A	Fraunhofer ITWM
CCB691	NECMagnusCommunications
CCB888	AnB Securite s.a.
CCB8A8	AMPAK Technology, Inc.
CCB8F1	EAGLE KINGDOM TECHNOLOGIES LIMITED
CCBD35	Steinel GmbH
CCBDD3	Ultimaker B.V.
CCBE59	Calix Inc.
CCBE71	OptiLogix BV
CCC104	Applied Technical Systems
CCC3EA	Motorola Mobility LLC, a Lenovo Company
CCC50A	SHENZHEN DAJIAHAO TECHNOLOGY CO.,LTD
CCC5EF	Co-Comm Servicios Telecomunicaciones S.L.
CCC62B	Tri-Systems Corporation
CCC760	Apple, Inc.
CCC8D7	CIAS Elettronica srl
CCCC4E	Sun Fountainhead USA. Corp
CCCC81	HUAWEI TECHNOLOGIES CO.,LTD
CCCD64	SM-Electronic GmbH
CCCE1E	AVM Audiovisuelles Marketing und Computersysteme GmbH
CCCE40	Janteq Corp
CCD29B	Shenzhen Bopengfa Elec&Technology CO.,Ltd
CCD31E	IEEE Registration Authority
CCD3E2	Jiangsu Yinhe  Electronics Co.,Ltd.
CCD539	Cisco Systems, Inc
CCD811	Aiconn Technology Corporation
CCD8C1	Cisco Systems, Inc
CCD9E9	SCR Engineers Ltd.
CCE0C3	Mangstor, Inc.
CCE17F	Juniper Networks
CCE1D5	BUFFALO.INC
CCE798	My Social Stuff
CCE7DF	American Magnetics, Inc.
CCE8AC	SOYEA Technology Co.,Ltd.
CCEA1C	DCONWORKS  Co., Ltd
CCEED9	VAHLE DETO GmbH
CCEF48	Cisco Systems, Inc
CCF3A5	Chi Mei Communication Systems, Inc
CCF407	EUKREA ELECTROMATIQUE SARL
CCF538	3isysnetworks
CCF67A	Ayecka Communication Systems LTD
CCF841	Lumewave
CCF8F0	Xi'an HISU Multimedia Technology Co.,Ltd.
CCF954	Avaya Inc
CCF9E8	Samsung Electronics Co.,Ltd
CCFA00	LG Electronics (Mobile Communications)
CCFB65	Nintendo Co., Ltd.
CCFC6D	RIZ TRANSMITTERS
CCFCB1	Wireless Technology, Inc.
CCFD17	TCT mobile ltd
CCFE3C	Samsung Electronics Co.,Ltd
D0034B	Apple, Inc.
D00492	Fiberhome Telecommunication Technologies Co.,LTD
D0052A	Arcadyan Corporation
D00790	Texas Instruments
D00AAB	Yokogawa Digital Computer Corporation
D00EA4	Porsche Cars North America
D00ED9	Taicang T&W Electronics
D00F6D	T&W Electronics Company
D01242	BIOS Corporation
D0131E	Sunrex Technology Corp
D013FD	LG Electronics (Mobile Communications)
D0154A	zte corporation
D0176A	Samsung Electronics Co.,Ltd
D017C2	ASUSTek COMPUTER INC.
D01AA7	Uniprint
D01CBB	Beijing Ctimes Digital Technology Co., Ltd.
D02212	IEEE Registration Authority
D022BE	SAMSUNG ELECTRO-MECHANICS(THAILAND)
D023DB	Apple, Inc.
D02516	SHENZHEN MERCURY COMMUNICATION TECHNOLOGIES CO.,LTD.
D02544	SAMSUNG ELECTRO-MECHANICS(THAILAND)
D02598	Apple, Inc.
D02788	Hon Hai Precision Ind. Co.,Ltd.
D02C45	littleBits Electronics, Inc.
D02DB3	HUAWEI TECHNOLOGIES CO.,LTD
D03110	Ingenic Semiconductor Co.,Ltd
D03311	Apple, Inc.
D03742	Yulong Computer Telecommunication Scientific (Shenzhen) Co.,Ltd
D03761	Texas Instruments
D03972	Texas Instruments
D039B3	ARRIS Group, Inc.
D03DC3	AQ Corporation
D03E5C	HUAWEI TECHNOLOGIES CO.,LTD
D0431E	Dell Inc.
D046DC	Southwest Research Institute
D048F3	DATTUS Inc
D0498B	ZOOM SERVER
D04CC1	SINTRONES Technology Corp.
D04D2C	Roku, Inc.
D04F7E	Apple, Inc.
D05099	ASRock Incorporation
D05162	Sony Mobile Communications AB
D052A8	Physical Graph Corporation
D05349	Liteon Technology Corporation
D0542D	Cambridge Industries(Group) Co.,Ltd.
D055B2	Integrated Device Technology (Malaysia) Sdn. Bhd.
D0574C	Cisco Systems, Inc
D0577B	Intel Corporate
D05785	Pantech Co., Ltd.
D057A1	Werma Signaltechnik GmbH & Co. KG
D05875	Active Control Technology Inc.
D058A8	zte corporation
D059C3	CeraMicro Technology Corporation
D059E4	Samsung Electronics Co.,Ltd
D05A0F	I-BT DIGITAL CO.,LTD
D05AF1	Shenzhen Pulier Tech CO.,Ltd
D05BA8	zte corporation
D05C7A	Sartura d.o.o.
D05FB8	Texas Instruments
D05FCE	Hitachi Data Systems
D0608C	zte corporation
D062A0	China Essence Technology (Zhumadian) Co., Ltd.
D0634D	Meiko Maschinenbau GmbH &amp; Co. KG
D063B4	SolidRun Ltd.
D065CA	HUAWEI TECHNOLOGIES CO.,LTD
D0667B	Samsung Electronics Co.,Ltd
D067E5	Dell Inc.
D0699E	LUMINEX Lighting Control Equipment
D069D0	Verto Medical Solutions, LLC
D06A1F	BSE CO.,LTD.
D06F4A	TOPWELL INTERNATIONAL HOLDINGS LIMITED
D06F82	HUAWEI TECHNOLOGIES CO.,LTD
D071C4	zte corporation
D072DC	Cisco Systems, Inc
D0737F	Mini-Circuits
D0738E	DONG OH PRECISION CO., LTD.
D073D5	LIFI LABS MANAGEMENT PTY LTD
D075BE	Reno A&E
D07650	IEEE Registration Authority
D07AB5	HUAWEI TECHNOLOGIES CO.,LTD
D07C2D	Leie IOT technology Co., Ltd
D07DE5	Forward Pay Systems, Inc.
D07E28	Hewlett Packard
D07E35	Intel Corporate
D083D4	XTel ApS
D084B0	Sagemcom Broadband SAS
D087E2	Samsung Electronics Co.,Ltd
D08999	APCON, Inc.
D08A55	Skullcandy
D08B7E	Passif Semiconductor
D08CB5	Texas Instruments
D08CFF	UPWIS AB
D0929E	Microsoft Corporation
D09380	Ducere Technologies Pvt. Ltd.
D093F8	Stonestreet One LLC
D095C7	Pantech Co., Ltd.
D099D5	Alcatel-               # Alcatel-Lucent
D09B05	Emtronix
D09C30	Foster Electric Company, Limited
D09D0A	Linkcom
D09DAB	TCT mobile ltd
D0A0D6	Chengdu TD Tech Ltd.
D0A311	Neuberger Gebäudeautomation GmbH
D0A4B1	Sonifex Ltd.
D0A5A6	Cisco Systems, Inc
D0A637	Apple, Inc.
D0AEEC	Alpha Networks Inc.
D0AFB6	Linktop Technology Co., LTD
D0B0CD	Moen
D0B2C4	Technicolor CH USA Inc.
D0B33F	Shenzhen TINNO Mobile Technology Corp.
D0B498	Robert Bosch LLC Automotive Electronics
D0B523	Bestcare Cloucal Corp.
D0B53D	SEPRO ROBOTIQUE
D0B5C2	Texas Instruments
D0BAE4	Shanghai MXCHIP Information Technology Co., Ltd.
D0BB80	SHL Telemedicine International Ltd.
D0BD01	DS International
D0BE2C	CNSLink Co., Ltd.
D0BF9C	Hewlett Packard
D0C0BF	Actions Microelectronics Co., Ltd
D0C193	SKYBELL, INC
D0C1B1	Samsung Electronics Co.,Ltd
D0C282	Cisco Systems, Inc
D0C42F	Tamagawa Seiki Co.,Ltd.
D0C5F3	Apple, Inc.
D0C789	Cisco Systems, Inc
D0C7C0	TP-LINK TECHNOLOGIES CO.,LTD.
D0CDE1	Scientech Electronics
D0CF5E	Energy Micro AS
D0D04B	HUAWEI TECHNOLOGIES CO.,LTD
D0D0FD	Cisco Systems, Inc
D0D212	K2NET Co.,Ltd.
D0D286	Beckman Coulter K.K.
D0D3FC	Mios, Ltd.
D0D412	ADB Broadband Italia
D0D471	MVTECH co., Ltd
D0D6CC	Wintop
D0D94F	IEEE Registration Authority
D0DB32	Nokia Corporation
D0DF9A	Liteon Technology Corporation
D0DFB2	Genie Networks Limited
D0DFC7	Samsung Electronics Co.,Ltd
D0E140	Apple, Inc.
D0E347	Yoga
D0E40B	Wearable Inc.
D0E44A	Murata Manufacturing Co., Ltd.
D0E54D	ARRIS Group, Inc.
D0E782	AzureWave Technology Inc.
D0EB03	Zhehua technology limited
D0EB9E	Seowoo Inc.
D0F0DB	Ericsson
D0F27F	SteadyServ Technoligies, LLC
D0F73B	Helmut Mauell GmbH Werk Weida
D0F88C	Motorola (Wuhan) Mobility Technologies Communication Co., Ltd.
D0FA1D	Qihoo  360  Technology Co.,Ltd
D0FCCC	Samsung Electronics Co.,Ltd
D0FF50	Texas Instruments
D0FF98	HUAWEI TECHNOLOGIES CO.,LTD
D4000D	Phoenix Broadband Technologies, LLC.
D40057	MC Technologies GmbH
D40129	Broadcom
D4016D	TP-LINK TECHNOLOGIES CO.,LTD.
D4024A	Delphian Systems LLC
D404CD	ARRIS Group, Inc.
D404FF	Juniper Networks
D40598	ARRIS Group, Inc.
D40AA9	ARRIS Group, Inc.
D40B1A	HTC Corporation
D40BB9	Solid Semecs bv.
D40FB2	Applied Micro Electronics AME bv
D41090	iNFORM Systems AG
D410CF	Huanshun Network Science and Technology Co., Ltd.
D411D6	ShotSpotter, Inc.
D41296	Anobit Technologies Ltd.
D412BB	Quadrant Components Inc. Ltd
D4136F	Asia Pacific Brands
D41C1C	RCF S.P.A.
D41D71	Palo Alto Networks
D41E35	TOHO Electronics INC.
D41F0C	JAI Oy
D4206D	HTC Corporation
D42122	Sercomm Corporation
D4223F	Lenovo Mobile Communication Technology Ltd.
D4224E	Alcatel Lucent
D42751	Infopia Co., Ltd
D428B2	ioBridge, Inc.
D428D5	TCT mobile ltd
D429EA	Zimory GmbH
D42C0F	ARRIS Group, Inc.
D42C3D	Sky Light Digital Limited
D42C44	Cisco Systems, Inc
D42F23	Akenori PTE Ltd
D4319D	Sinwatec
D43266	Fike Corporation
D43639	Texas Instruments
D436DB	Jiangsu Toppower Automotive Electronics Co., Ltd
D437D7	zte corporation
D43A65	IGRS Engineering Lab Ltd.
D43AE9	DONGGUAN ipt INDUSTRIAL CO., LTD
D43D67	Carma Industries Inc.
D43D7E	Micro-Star Int'l Co, Ltd
D440F0	HUAWEI TECHNOLOGIES CO.,LTD
D44165	SICHUAN TIANYI COMHEART TELECOMCO.,LTD
D443A8	Changzhou Haojie Electric Co., Ltd.
D445E8	Jiangxi Hongpai Technology Co., Ltd.
D44B5E	TAIYO YUDEN CO., LTD.
D44C24	Vuppalamritha Magnetic Components LTD
D44C9C	Shenzhen YOOBAO Technology Co.Ltd
D44CA7	Informtekhnika & Communication, LLC
D44F80	Kemper Digital GmbH
D4503F	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
D4507A	CEIVA Logic, Inc
D4522A	TangoWiFi.com
D45251	IBT Ingenieurbureau Broennimann Thun
D45297	nSTREAMS Technologies, Inc.
D453AF	VIGO System S.A.
D45556	Fiber Mountain Inc.
D455BE	SHENZHEN FAST TECHNOLOGIES CO.,LTD
D45AB2	Galleon Systems
D45C70	Wi-Fi Alliance
D45D42	Nokia Corporation
D45F25	Shenzhen YOUHUA Technology Co., Ltd
D4612E	HUAWEI TECHNOLOGIES CO.,LTD
D46132	Pro Concept Manufacturer Co.,Ltd.
D4619D	Apple, Inc.
D461FE	Hangzhou H3C Technologies Co., Limited
D463FE	Arcadyan Corporation
D464F7	CHENGDU USEE DIGITAL TECHNOLOGY CO., LTD
D466A8	Riedo Networks GmbH
D46761	SAHAB TECHNOLOGY
D467E7	Fiberhome Telecommunication Technologies Co.,LTD
D4684D	Ruckus Wireless
D46867	Neoventus Design Group
D468BA	Shenzhen Sundray Technologies Company Limited
D46A6A	Hon Hai Precision Ind. Co.,Ltd.
D46A91	Snap AV
D46AA8	HUAWEI TECHNOLOGIES CO.,LTD
D46CBF	Goodrich ISR
D46CDA	CSM GmbH
D46D50	Cisco Systems, Inc
D46E0E	TP-LINK TECHNOLOGIES CO.,LTD.
D46E5C	HUAWEI TECHNOLOGIES CO.,LTD
D46F42	WAXESS USA Inc
D47208	Bragi GmbH
D476EA	zte corporation
D47856	Avaya Inc
D479C3	Cameronet GmbH & Co. KG
D47AE2	Samsung Electronics Co.,Ltd
D47B35	NEO Monitors AS
D47B75	HARTING Electronics GmbH
D47BB0	ASKEY COMPUTER CORP
D47DFC	TECNO MOBILE LIMITED
D481CA	iDevices, LLC
D481D7	Dell Inc.
D4823E	Argosy Technologies, Ltd.
D48304	SHENZHEN FAST TECHNOLOGIES CO.,LTD
D48564	Hewlett Packard
D487D8	Samsung Electronics Co.,Ltd
D4883F	HDPRO CO., LTD.
D48890	Samsung Electronics Co.,Ltd
D48CB5	Cisco Systems, Inc
D48DD9	Meld Technology, Inc
D48F33	Microsoft Corporation
D48FAA	Sogecam Industrial, S.A.
D490E0	Wachendorff Automation GmbH & Co KG
D491AF	Electroacustica General Iberica, S.A.
D49398	Nokia Corporation
D493A0	Fidelix Oy
D4945A	COSMO CO., LTD
D494A1	Texas Instruments
D494E8	HUAWEI TECHNOLOGIES CO.,LTD
D49524	Clover Network, Inc.
D496DF	SUNGJIN C&T CO.,LTD
D4970B	Xiaomi Communications Co Ltd
D49A20	Apple, Inc.
D49B5C	Chongqing Miedu Technology Co., Ltd.
D49C28	JayBird LLC
D49C8E	University of FUKUI
D49E6D	Wuhan Zhongyuan Huadian Science & Technology Co.,
D4A02A	Cisco Systems, Inc
D4A148	HUAWEI TECHNOLOGIES CO.,LTD
D4A425	SMAX Technology Co., Ltd.
D4A499	InView Technology Corporation
D4A928	GreenWave Reality Inc
D4AAFF	MICRO WORLD
D4AC4E	BODi rS, LLC
D4AD2D	Fiberhome Telecommunication Technologies Co.,LTD
D4AE05	Samsung Electronics Co.,Ltd
D4AE52	Dell Inc.
D4B110	HUAWEI TECHNOLOGIES CO.,LTD
D4B169	Le Shi Zhi Xin Electronic Technology (Tianjin) Limited
D4B43E	Messcomp Datentechnik GmbH
D4B8FF	Home Control Singapore Pte Ltd
D4BED9	Dell Inc.
D4BF2D	SE Controls Asia Pacific Ltd
D4BF7F	Upvel
D4C1C8	zte corporation
D4C1FC	Nokia Corporation
D4C766	Acentic GmbH
D4C8B0	Prime Electronics & Satellitics Inc.
D4C9B2	Quanergy Systems Inc
D4C9EF	Hewlett Packard
D4CA6D	Routerboard.com
D4CA6E	u-blox AG
D4CBAF	Nokia Corporation
D4CEB8	Enatel LTD
D4CF37	Symbolic IO
D4CFF9	Shenzhen Sen5 Technology Co., Ltd.
D4D184	ADB Broadband Italia
D4D249	Power Ethernet
D4D50D	Southwest Microwave, Inc
D4D748	Cisco Systems, Inc
D4D7A9	Shanghai Kaixiang Info Tech LTD
D4D898	Korea CNO Tech Co., Ltd
D4D919	Gopro
D4DCCD	Apple, Inc.
D4DF57	Alpinion Medical Systems
D4E08E	ValueHD Corporation
D4E32C	S. Siedle & Sohne
D4E33F	Nokia
D4E8B2	Samsung Electronics Co.,Ltd
D4E90B	CVT CO.,LTD
D4EA0E	Avaya Inc
D4EC0C	Harley-Davidson Motor Company
D4EC86	LinkedHope Intelligent Technologies Co., Ltd
D4EE07	HIWIFI Co., Ltd.
D4F027	Navetas Energy Management
D4F0B4	Napco Security Technologies
D4F143	IPROAD.,Inc
D4F207	DIAODIAO(Beijing)Technology CO.,Ltd
D4F46F	Apple, Inc.
D4F4BE	Palo Alto Networks
D4F513	Texas Instruments
D4F63F	IEA S.R.L.
D4F9A1	HUAWEI TECHNOLOGIES CO.,LTD
D8004D	Apple, Inc.
D8052E	Skyviia Corporation
D806D1	Honeywell Fire System (Shanghai) Co,. Ltd.
D808F5	Arcadia Networks Co. Ltd.
D809C3	Cercacor Labs
D80CCF	C.G.V. S.A.S.
D80DE3	FXI TECHNOLOGIES AS
D80F99	Hon Hai Precision Ind. Co.,Ltd.
D814D6	SURE SYSTEM Co Ltd
D8150D	TP-LINK TECHNOLOGIES CO.,LTD.
D8160A	Nippon Electro-Sensory Devices
D816C1	DEWAV (HK) ELECTRONICS LIMITED
D8182B	Conti Temic Microelectronic GmbH
D8197A	Nuheara Ltd
D819CE	Telesquare
D81BFE	TWINLINX CORPORATION
D81C14	Compacta International, Ltd.
D81D72	Apple, Inc.
D81EDE	B&W Group Ltd
D81FCC	Brocade Communications Systems, Inc.
D8209F	Cubro Acronet GesmbH
D824BD	Cisco Systems, Inc
D82522	ARRIS Group, Inc.
D825B0	Rockeetech Systems Co.,Ltd.
D826B9	Guangdong Coagent Electronics S&amp;T Co.,Ltd.
D8270C	MaxTronic International Co., Ltd.
D828C9	General Electric Consumer and Industrial
D82916	Ascent Communication Technology
D82986	Best Wish Technology LTD
D82A15	Leitner SpA
D82A7E	Nokia Corporation
D82D9B	Shenzhen G.Credit Communication Technology Co., Ltd
D82DE1	Tricascade Inc.
D83062	Apple, Inc.
D831CF	Samsung Electronics Co.,Ltd
D83214	Tenda Technology Co.,Ltd.Dongguan branch
D8325A	Shenzhen YOUHUA Technology Co., Ltd
D8337F	Office FA.com Co.,Ltd.
D837BE	Shanghai Gongjing Telecom Technology Co,LTD
D8380D	SHENZHEN IP-COM Network Co.,Ltd
D838FC	Ruckus Wireless
D83C69	Shenzhen TINNO Mobile Technology Corp.
D842AC	Shanghai Feixun Communication Co.,Ltd.
D842E2	Canary Connect, Inc.
D8452B	Integrated Device Technology (Malaysia) Sdn. Bhd.
D84606	Silicon Valley Global Marketing
D84710	Sichuan Changhong Electric Ltd.
D848EE	Hangzhou Xueji Technology Co., Ltd.
D8490B	HUAWEI TECHNOLOGIES CO.,LTD
D8492F	CANON INC.
D84A87	OI ELECTRIC CO.,LTD
D84B2A	Cognitas Technologies, Inc.
D84FB8	LG ELECTRONICS
D850E6	ASUSTek COMPUTER INC.
D8543A	Texas Instruments
D854A2	Aerohive Networks Inc.
D855A3	zte corporation
D857EF	Samsung Electronics Co.,Ltd
D858D7	CZ.NIC, z.s.p.o.
D85B2A	Samsung Electronics Co.,Ltd
D85D4C	TP-LINK TECHNOLOGIES CO.,LTD.
D85D84	CAx soft GmbH
D85DE2	Hon Hai Precision Ind. Co.,Ltd.
D85DEF	Busch-Jaeger Elektro GmbH
D85DFB	Private
D860B0	bioMérieux Italia S.p.A.
D860B3	Guangdong Global Electronic Technology CO.，LTD
D86194	Objetivos y Sevicios de Valor Añadido
D862DB	Eno Inc.
D86595	Toy's Myth Inc.
D866C6	Shenzhen Daystar Technology Co.,ltd
D866EE	BOXIN COMMUNICATION CO.,LTD.
D867D9	Cisco Systems, Inc
D86960	Steinsvik
D86BF7	Nintendo Co., Ltd.
D86C02	Huaqin Telecom Technology Co.,Ltd
D86CE9	Sagemcom Broadband SAS
D87157	Lenovo Mobile Communication Technology Ltd.
D87495	zte corporation
D87533	Nokia Corporation
D8760A	Escort, Inc.
D878E5	KUHN SA
D87988	Hon Hai Precision Ind. Co.,Ltd.
D87CDD	SANIX INCORPORATED
D87EB1	x.o.ware, inc.
D88039	Microchip Technology Inc.
D8803C	Anhui Huami Information Technology Company Limited
D881CE	AHN INC.
D88466	Extreme Networks
D887D5	Leadcore Technology CO.,LTD
D888CE	RF Technology Pty Ltd
D88A3B	Unit-Em
D88B4C	KingTing Tech.
D88D5C	Elentec
D890E8	Samsung Electronics Co.,Ltd
D89341	General Electric Global Research
D89403	Hewlett Packard Enterprise
D8952F	Texas Instruments
D89685	Gopro
D89695	Apple, Inc.
D896E0	Alibaba Cloud Computing Ltd.
D8973B	Artesyn Embedded Technologies
D89760	C2 Development, Inc.
D8977C	Grey Innovation
D897BA	PEGATRON CORPORATION
D89A34	Beijing SHENQI Technology Co., Ltd.
D89D67	Hewlett Packard
D89DB9	eMegatech International Corp.
D89E3F	Apple, Inc.
D8A105	Syslane, Co., Ltd.
D8A25E	Apple, Inc.
D8ADDD	Sonavation, Inc.
D8AE90	Itibia Technologies
D8AF3B	Hangzhou Bigbright Integrated communications system Co.,Ltd
D8AFF1	Panasonic Appliances Company
D8B02E	Guangzhou Zonerich Business Machine Co., LTD.
D8B04C	Jinan USR IOT Technology Co., Ltd.
D8B12A	Panasonic Mobile Communications Co., Ltd.
D8B190	Cisco Systems, Inc
D8B377	HTC Corporation
D8B6B7	Comtrend Corporation
D8B6C1	NetworkAccountant, Inc.
D8B6D6	Blu Tether Limited
D8B8F6	Nantworks
D8B90E	Triple Domain Vision Co.,Ltd.
D8BB2C	Apple, Inc.
D8BF4C	Victory Concept Electronics Limited
D8C068	Netgenetech.co.,ltd.
D8C06A	Hunantv.com Interactive Entertainment Media Co.,Ltd.
D8C3FB	Detracom
D8C46A	Murata Manufacturing Co., Ltd.
D8C4E9	Samsung Electronics Co.,Ltd
D8C691	Hichan Technology Corp.
D8C771	HUAWEI TECHNOLOGIES CO.,LTD
D8C7C8	Aruba Networks
D8C8E9	Phicomm (Shanghai) Co., Ltd.
D8C99D	EA DISPLAY LIMITED
D8CB8A	Micro-Star INTL CO., LTD.
D8CF9C	Apple, Inc.
D8D1CB	Apple, Inc.
D8D27C	JEMA ENERGY, SA
D8D385	Hewlett Packard
D8D43C	Sony Corporation
D8D5B9	Rainforest Automation, Inc.
D8D67E	GSK CNC EQUIPMENT CO.,LTD
D8D723	IDS, Inc
D8D866	SHENZHEN TOZED TECHNOLOGIES CO.,LTD.
D8DA52	APATOR S.A.
D8DCE9	Kunshan Erlab ductless filtration system Co.,Ltd
D8DD5F	BALMUDA Inc.
D8DDFD	Texas Instruments
D8DECE	ISUNG CO.,LTD
D8DF0D	beroNet GmbH
D8E0B8	BULAT LLC
D8E0E1	Samsung Electronics Co.,Ltd
D8E3AE	CIRTEC MEDICAL SYSTEMS
D8E56D	TCT mobile ltd
D8E72B	NetScout Systems, Inc.
D8E743	Wush, Inc
D8E952	Keopsys
D8EB97	TRENDnet, Inc.
D8EE78	Moog Protokraft
D8EFCD	Nokia
D8F0F2	Zeebo Inc
D8F710	Libre Wireless Technologies Inc.
D8FB11	Axacore
D8FB5E	ASKEY COMPUTER CORP
D8FB68	Cloud Corner Ltd.
D8FC38	Giantec Semiconductor Inc
D8FC93	Intel Corporate
D8FE8F	IDFone Co., Ltd.
D8FEE3	D-Link International
DC0077	TP-LINK TECHNOLOGIES CO.,LTD.
DC0265	Meditech Kft
DC028E	zte corporation
DC052F	National Products Inc.
DC0575	SIEMENS ENERGY AUTOMATION
DC05ED	Nabtesco  Corporation
DC07C1	HangZhou QiYang Technology Co.,Ltd.
DC0856	Alcatel-               # Alcatel-Lucent Enterprise
DC0914	Talk-A-Phone Co.
DC094C	HUAWEI TECHNOLOGIES CO.,LTD
DC0B1A	ADB Broadband Italia
DC0B34	LG Electronics (Mobile Communications)
DC0C5C	Apple, Inc.
DC0D30	Shenzhen Feasycom Technology Co., Ltd.
DC0EA1	COMPAL INFORMATION (KUNSHAN) CO., LTD.
DC15DB	Ge Ruili Intelligent Technology ( Beijing ) Co., Ltd.
DC16A2	Medtronic Diabetes
DC175A	Hitachi High-Technologies Corporation
DC1792	Captivate Network
DC1A01	Ecoliv Technology ( Shenzhen ) Ltd.
DC1AC5	vivo Mobile Communication Co., Ltd.
DC1D9F	U & B tech
DC1DD4	Microstep-MIS spol. s r.o.
DC1EA3	Accensus LLC
DC2008	ASD Electronics Ltd
DC293A	Shenzhen Nuoshi Technology Co., LTD.
DC2A14	Shanghai Longjing Technology Co.
DC2B2A	Apple, Inc.
DC2B61	Apple, Inc.
DC2B66	InfoBLOCK S.A. de C.V.
DC2BCA	Zera GmbH
DC2C26	Iton Technology Limited
DC2DCB	Beijing Unis HengYue Technology Co., Ltd.
DC2E6A	HCT. Co., Ltd.
DC2F03	Step forward Group Co., Ltd.
DC309C	Heyrex Limited
DC330D	Qingdao Haier Telecom Co.，Ltd
DC3350	TechSAT GmbH
DC35F1	Positivo Informática SA.
DC3714	Apple, Inc.
DC3752	Ge
DC37D2	Hunan HKT Electronic Technology Co., Ltd
DC38E1	Juniper Networks
DC3979	Skyport Systems
DC3A5E	Roku, Inc.
DC3C2E	Manufacturing System Insights, Inc.
DC3C84	Ticom Geomatics, Inc.
DC3CF6	Atomic Rules LLC
DC3E51	Solberg & Andersen AS
DC3EF8	Nokia Corporation
DC415F	Apple, Inc.
DC4427	IEEE Registration Authority
DC446D	Allwinner Technology Co., Ltd
DC4517	ARRIS Group, Inc.
DC49C9	CASCO SIGNAL LTD
DC4A3E	Hewlett Packard
DC4D23	MRV Comunications
DC4EDE	SHINYEI TECHNOLOGY CO., LTD.
DC5360	Intel Corporate
DC537C	Compal Broadband Networks, Inc.
DC56E6	Shenzhen Bococom Technology Co.,LTD
DC5726	Power-One
DC5E36	Paterson Technology
DC60A1	Teledyne DALSA Professional Imaging
DC647C	C.R.S. iiMotion GmbH
DC64B8	Shenzhen JingHanDa Electronics Co.Ltd
DC663A	Apacer Technology Inc.
DC6672	Samsung Electronics Co.,Ltd
DC6DCD	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
DC6F00	Livescribe, Inc.
DC6F08	Bay Storage Technology
DC7014	Private
DC7144	SAMSUNG ELECTRO MECHANICS CO., LTD.
DC7834	LOGICOM SA
DC7B94	Cisco Systems, Inc
DC7FA4	2Wire Inc
DC825B	JANUS, spol. s r.o.
DC82F6	Iport
DC85DE	AzureWave Technology Inc.
DC86D8	Apple, Inc.
DC9A8E	Nanjing Cocomm electronics co., LTD
DC9B1E	Intercom, Inc.
DC9B9C	Apple, Inc.
DC9C52	Sapphire Technology Limited.
DC9C9F	Shenzhen YOUHUA Technology Co., Ltd
DC9FA4	Nokia Corporation
DC9FDB	Ubiquiti Networks Inc.
DCA3AC	RBcloudtech
DCA4CA	Apple, Inc.
DCA5F4	Cisco Systems, Inc
DCA6BD	Beijing Lanbo Technology Co., Ltd.
DCA7D9	Compressor Controls Corp
DCA8CF	New Spin Golf, LLC.
DCA904	Apple, Inc.
DCA971	Intel Corporate
DCA989	Macandc
DCAD9E	GreenPriz
DCAE04	CELOXICA Ltd
DCB058	Bürkert Werke GmbH
DCB3B4	Honeywell Environmental & Combustion Controls (Tianjin) Co., Ltd.
DCB4C4	Microsoft XCG
DCBF90	HUIZHOU QIAOXING TELECOMMUNICATION INDUSTRY CO.,LTD.
DCC0DB	Shenzhen Kaiboer Technology Co., Ltd.
DCC0EB	ASSA ABLOY CÔTE PICARDE
DCC101	SOLiD Technologies, Inc.
DCC422	Systembase Limited
DCC622	BUHEUNG SYSTEM
DCC64B	HUAWEI TECHNOLOGIES CO.,LTD
DCC793	Nokia Corporation
DCCBA8	Explora Technologies Inc
DCCE41	FE GLOBAL HONG KONG LIMITED
DCCEBC	Shenzhen JSR Technology Co.,Ltd.
DCCEC1	Cisco Systems, Inc
DCCF94	Beijing Rongcheng Hutong Technology Co., Ltd.
DCCF96	Samsung Electronics Co.,Ltd
DCD0F7	Bentek Systems Ltd.
DCD255	Kinpo Electronics, Inc.
DCD2FC	HUAWEI TECHNOLOGIES CO.,LTD
DCD321	HUMAX Co., Ltd.
DCD52A	Sunny Heart Limited
DCD87C	Beijing Jingdong Century Trading Co., LTD.
DCD87F	Shenzhen JoinCyber Telecom Equipment Ltd
DCD916	HUAWEI TECHNOLOGIES CO.,LTD
DCDA4F	GETCK TECHNOLOGY,  INC
DCDB70	Tonfunk Systementwicklung und Service GmbH
DCDC07	TRP Systems BV
DCDECA	Akyllor
DCE026	Patrol Tag, Inc
DCE1AD	Shenzhen Wintop Photoelectric Technology Co., Ltd
DCE2AC	Lumens Digital Optics Inc.
DCE578	Experimental Factory of Scientific Engineering and Special Design Department
DCE71C	AUG Elektronik GmbH
DCE838	CK Telecom (Shenzhen) Limited
DCEB94	Cisco Systems, Inc
DCEC06	Heimi Network Technology Co., Ltd.
DCEE06	HUAWEI TECHNOLOGIES CO.,LTD
DCEF09	Netgear
DCEFCA	Murata Manufacturing Co., Ltd.
DCF05D	Letta Teknoloji
DCF090	Private
DCF110	Nokia Corporation
DCF755	Sitronik
DCF858	Lorent Networks, Inc.
DCFAD5	STRONG Ges.m.b.H.
DCFB02	BUFFALO.INC
DCFE07	PEGATRON CORPORATION
DCFE18	TP-LINK TECHNOLOGIES CO.,LTD.
E00370	ShenZhen Continental Wireless Technology Co., Ltd.
E005C5	TP-LINK TECHNOLOGIES CO.,LTD.
E006E6	Hon Hai Precision Ind. Co.,Ltd.
E0071B	Hewlett Packard Enterprise
E00B28	Inovonics
E00C7F	Nintendo Co., Ltd.
E00DB9	Cree, Inc.
E00EDA	Cisco Systems, Inc
E0107F	Ruckus Wireless
E0143E	Modoosis Inc.
E01877	FUJITSU LIMITED
E0191D	HUAWEI TECHNOLOGIES CO.,LTD
E01AEA	Allied Telesis, Inc.
E01C41	Aerohive Networks Inc.
E01CEE	Bravo Tech, Inc.
E01D38	Beijing HuaqinWorld Technology Co.,Ltd
E01D3B	Cambridge Industries(Group) Co.,Ltd.
E01E07	Anite Telecoms  US. Inc
E01F0A	Xslent Energy Technologies. LLC
E02202	ARRIS Group, Inc.
E0247F	HUAWEI TECHNOLOGIES CO.,LTD
E02538	Titan Pet Products
E02630	Intrigue Technologies, Inc.
E02636	Nortel Networks
E0271A	TtcNext-               # TTC Next-generation Home Network System WG
E02861	HUAWEI TECHNOLOGIES CO.,LTD
E0286D	AVM Audiovisuelles Marketing und Computersysteme GmbH
E02A82	Universal Global Scientific Industrial Co., Ltd.
E02CB2	Lenovo Mobile Communication (Wuhan) Company Limited
E02CF3	MRS Electronic GmbH
E02F6D	Cisco Systems, Inc
E03005	Alcatel-               # Alcatel-Lucent Shanghai Bell Co., Ltd
E0319E	Valve Corporation
E031D0	SZ Telstar CO., LTD
E034E4	Feit Electric Company, Inc.
E03560	Challenger Supply Holdings, LLC
E03676	HUAWEI TECHNOLOGIES CO.,LTD
E036E3	Stage One International Co., Ltd.
E037BF	Wistron Neweb Corporation
E039D7	Plexxi, Inc.
E03C5B	SHENZHEN JIAXINJIE ELECTRON CO.,LTD
E03E44	Broadcom
E03E4A	Cavanagh Group International
E03E7D	data-complex GmbH
E03F49	ASUSTek COMPUTER INC.
E04136	MitraStar Technology Corp.
E043DB	Shenzhen ViewAt Technology Co.,Ltd.
E0469A	Netgear
E048AF	Premietech Limited
E04B45	Hi-P Electronics Pte Ltd
E04F43	Universal Global Scientific Industrial Co., Ltd.
E04FBD	SICHUAN TIANYI COMHEART TELECOMCO.,LTD
E0508B	Zhejiang Dahua Technology Co., Ltd.
E05124	NXP Semiconductors
E05163	Arcadyan Corporation
E0553D	Cisco Meraki
E05597	Emergent Vision Technologies Inc.
E056F4	AxesNetwork Solutions inc.
E0589E	Laerdal Medical
E05B70	Innovid, Co., Ltd.
E05DA6	Detlef Fink Elektronik & Softwareentwicklung
E05F45	Apple, Inc.
E05FB9	Cisco Systems, Inc
E06066	Sercomm Corporation
E061B2	HANGZHOU ZENOINTEL TECHNOLOGY CO., LTD
E06290	Jinan Jovision Science & Technology Co., Ltd.
E063E5	Sony Mobile Communications AB
E064BB	DigiView S.r.l.
E06678	Apple, Inc.
E067B3	C-Data Technology Co., Ltd
E0686D	Raybased AB
E06995	PEGATRON CORPORATION
E0750A	ALPS ELECTRIC CO.,LTD.
E0757D	Motorola Mobility LLC, a Lenovo Company
E076D0	AMPAK Technology, Inc.
E078A3	Shanghai Winner Information Technology Co.,Inc
E07C13	zte corporation
E07C62	Whistle Labs, Inc.
E07F53	TECHBOARD SRL
E07F88	EVIDENCE Network SIA
E08177	GreenBytes, Inc.
E087B1	Nata-Info Ltd.
E0885D	Technicolor CH USA Inc.
E0899D	Cisco Systems, Inc
E08A7E	Exponent
E08E3C	Aztech Electronics Pte Ltd
E08FEC	REPOTEC CO., LTD.
E09153	XAVi Technologies Corp.
E091F5	Netgear
E09467	Intel Corporate
E09579	ORTHOsoft inc, d/b/a Zimmer CAS
E09796	HUAWEI TECHNOLOGIES CO.,LTD
E097F2	Atomax Inc.
E09861	Motorola Mobility LLC, a Lenovo Company
E09971	Samsung Electronics Co.,Ltd
E09D31	Intel Corporate
E09DB8	PLANEX COMMUNICATIONS INC.
E09DFA	Wanan Hongsheng Electronic Co.Ltd
E0A198	NOJA Power Switchgear Pty Ltd
E0A1D7	Sfr
E0A30F	Pevco
E0A3AC	HUAWEI TECHNOLOGIES CO.,LTD
E0A670	Nokia Corporation
E0A700	Verkada Inc
E0A8B8	Le Shi Zhi Xin Electronic Technology (Tianjin) Limited
E0AAB0	GENERAL VISION ELECTRONICS CO. LTD.
E0ABFE	Orb Networks, Inc.
E0ACCB	Apple, Inc.
E0ACF1	Cisco Systems, Inc
E0AE5E	ALPS ELECTRIC CO.,LTD.
E0AEB2	Bender GmbH &amp; Co.KG
E0AEED	Loenk
E0AF4B	Pluribus Networks, Inc.
E0B2F1	FN-LINK TECHNOLOGY LIMITED
E0B52D	Apple, Inc.
E0B6F5	IEEE Registration Authority
E0B70A	ARRIS Group, Inc.
E0B7B1	ARRIS Group, Inc.
E0B94D	SHENZHEN BILIAN ELECTRONIC CO.，LTD
E0B9A5	AzureWave Technology Inc.
E0B9BA	Apple, Inc.
E0B9E5	Technicolor
E0BC43	C2 Microsystems, Inc.
E0C0D1	CK Telecom (Shenzhen) Limited
E0C286	Aisai Communication Technology Co., Ltd.
E0C2B7	Masimo Corporation
E0C3F3	zte corporation
E0C6B3	MilDef AB
E0C767	Apple, Inc.
E0C79D	Texas Instruments
E0C86A	SHENZHEN TW-SCIE Co., Ltd
E0C922	Jireh Energy Tech., Ltd.
E0C97A	Apple, Inc.
E0CA4D	Shenzhen Unistar Communication Co.,LTD
E0CA94	ASKEY COMPUTER CORP
E0CB1D	Private
E0CB4E	ASUSTek COMPUTER INC.
E0CBEE	Samsung Electronics Co.,Ltd
E0CDFD	Beijing E3Control Technology Co, LTD
E0CEC3	ASKEY COMPUTER CORP
E0CF2D	Gemintek Corporation
E0D10A	Katoudenkikougyousyo co ltd
E0D173	Cisco Systems, Inc
E0D1E6	Aliph dba Jawbone
E0D31A	EQUES Technology Co., Limited
E0D55E	GIGA-BYTE TECHNOLOGY CO.,LTD.
E0D7BA	Texas Instruments
E0D9A2	Hippih aps
E0D9E3	Eltex Enterprise Ltd.
E0DADC	JVC KENWOOD Corporation
E0DB10	Samsung Electronics Co.,Ltd
E0DB55	Dell Inc.
E0DB88	Open Standard Digital-IF Interface for SATCOM Systems
E0DCA0	Siemens Industrial Automation Products Ltd Chengdu
E0DDC0	vivo Mobile Communication Co., Ltd.
E0E5CF	Texas Instruments
E0E631	SNB TECHNOLOGIES LIMITED
E0E751	Nintendo Co., Ltd.
E0E7BB	Nureva, Inc.
E0E8E8	Olive Telecommunication Pvt. Ltd
E0ED1A	vastriver Technology Co., Ltd
E0EDC7	Shenzhen Friendcom Technology Development Co., Ltd
E0EE1B	Panasonic Automotive Systems Company of America
E0EF25	Lintes Technology Co., Ltd.
E0F211	Digitalwatt
E0F379	Vaddio
E0F5C6	Apple, Inc.
E0F5CA	CHENG UEI PRECISION INDUSTRY CO.,LTD.
E0F847	Apple, Inc.
E0F9BE	Cloudena Corp.
E0FAEC	Platan sp. z o.o. sp. k.
E0FFF7	Softiron Inc.
E20C0F	Kingston Technologies
E4029B	Intel Corporate
E40439	TomTom Software Ltd
E4115B	Hewlett Packard
E41218	ShenZhen Rapoo Technology Co., Ltd.
E4121D	Samsung Electronics Co.,Ltd
E41289	topsystem Systemhaus GmbH
E417D8	8BITDO TECHNOLOGY HK LIMITED
E4186B	ZyXEL Communications Corporation
E41A2C	ZPE Systems, Inc.
E41C4B	V2 TECHNOLOGY, INC.
E41D2D	Mellanox Technologies, Inc.
E41F13	IBM Corp
E422A5	PLANTRONICS, INC.
E42354	SHENZHEN FUZHI SOFTWARE TECHNOLOGY CO.,LTD
E425E7	Apple, Inc.
E425E9	Color-Chip
E42771	Smartlabs
E42AD3	Magneti Marelli S.p.A. Powertrain
E42C56	Lilee Systems, Ltd.
E42D02	TCT mobile ltd
E42F26	Fiberhome Telecommunication Technologies Co.,LTD
E42F56	OptoMET GmbH
E42FF6	Unicore communication Inc.
E432CB	Samsung Electronics Co.,Ltd
E43593	Hangzhou GoTo technology Co.Ltd
E435C8	HUAWEI TECHNOLOGIES CO.,LTD
E435FB	Sabre Technology (Hull) Ltd
E437D7	HENRI DEPAEPE S.A.S.
E438F2	Advantage Controls
E43ED7	Arcadyan Corporation
E43FA2	Wuxi DSP Technologies Inc.
E440E2	Samsung Electronics Co.,Ltd
E441E6	Ottec Technology GmbH
E442A6	Intel Corporate
E446BD	C&C TECHNIC TAIWAN CO., LTD.
E44790	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
E448C7	Cisco SPVTG
E44C6C	Shenzhen Guo Wei Electronic Co,. Ltd.
E44E18	Gardasoft VisionLimited
E44F29	MA Lighting Technology GmbH
E44F5F	EDS Elektronik Destek San.Tic.Ltd.Sti
E4509A	HW Communications Ltd
E455EA	Dedicated Computing
E45614	Suttle Apparatus
E45740	ARRIS Group, Inc.
E457A8	Stuart Manufacturing, Inc.
E458B8	Samsung Electronics Co.,Ltd
E458E7	Samsung Electronics Co.,Ltd
E45AA2	vivo Mobile Communication Co., Ltd.
E45D51	Sfr
E45D52	Avaya Inc
E45D75	Samsung Electronics Co.,Ltd
E46251	HAO CHENG GROUP LIMITED
E46449	ARRIS Group, Inc.
E467BA	Danish Interpretation Systems A/S
E468A3	HUAWEI TECHNOLOGIES CO.,LTD
E4695A	Dictum Health, Inc.
E46C21	messMa GmbH
E46F13	D-Link International
E47185	Securifi Ltd
E4751E	Getinge Sterilization AB
E47723	zte corporation
E4776B	AARTESYS AG
E477D4	Minrray Industry Co.,Ltd
E47B3F	BEIJING CO-CLOUD TECHNOLOGY LTD.
E47CF9	Samsung Electronics Co.,Ltd
E47D5A	Beijing Hanbang Technology Corp.
E47DBD	Samsung Electronics Co.,Ltd
E47DEB	Shanghai Notion Information Technology CO.,LTD.
E47E66	HUAWEI TECHNOLOGIES CO.,LTD
E47FB2	FUJITSU LIMITED
E48184	Nokia
E481B3	Shenzhen ACT Industrial Co.,Ltd.
E48399	ARRIS Group, Inc.
E48501	Geberit International AG
E48AD5	RF WINDOW CO., LTD.
E48B7F	Apple, Inc.
E48C0F	Discovery Insure
E48D8C	Routerboard.com
E49069	Rockwell Automation
E4907E	Motorola Mobility LLC, a Lenovo Company
E492E7	Gridlink Tech. Co.,Ltd.
E492FB	Samsung Electronics Co.,Ltd
E4956E	IEEE Registration Authority
E496AE	ALTOGRAPHICS Inc.
E497F0	Shanghai VLC Technologies Ltd. Co.
E498D1	Microsoft Mobile Oy
E498D6	Apple, Inc.
E49A79	Apple, Inc.
E49E12	FREEBOX SAS
E4A1E6	Alcatel-               # Alcatel-Lucent Shanghai Bell Co., Ltd
E4A32F	Shanghai Artimen Technology Co., Ltd.
E4A387	Control Solutions LLC
E4A471	Intel Corporate
E4A5EF	TRON LINK ELECTRONICS CO., LTD.
E4A749	Palo Alto Networks
E4A7A0	Intel Corporate
E4A7FD	Cellco Partnership
E4A8B6	HUAWEI TECHNOLOGIES CO.,LTD
E4AA5D	Cisco Systems, Inc
E4AB46	UAB Selteka
E4AD7D	SCL Elements
E4AFA1	Hes-So
E4B005	Beijing IQIYI Science & Technology Co., Ltd.
E4B021	Samsung Electronics Co.,Ltd
E4B318	Intel Corporate
E4BAD9	360 Fly Inc.
E4BEED	Netcore Technology Inc.
E4C146	Objetivos y Servicios de Valor A
E4C1F1	SHENZHEN SPOTMAU INFORMATION TECHNOLIGY CO., Ltd
E4C2D1	HUAWEI TECHNOLOGIES CO.,LTD
E4C62B	Airware
E4C63D	Apple, Inc.
E4C6E6	Mophie, LLC
E4C722	Cisco Systems, Inc
E4C801	BLU Products Inc
E4C806	Ceiec Electric Technology Inc.
E4CE02	WyreStorm Technologies Ltd
E4CE70	Health & Life co., Ltd.
E4CE8F	Apple, Inc.
E4D332	TP-LINK TECHNOLOGIES CO.,LTD.
E4D3F1	Cisco Systems, Inc
E4D53D	Hon Hai Precision Ind. Co.,Ltd.
E4D71D	Oraya Therapeutics
E4DD79	En-Vision America, Inc.
E4E0C5	Samsung Electronics Co.,Ltd
E4E409	LEIFHEIT AG
E4E4AB	Apple, Inc.
E4EC10	Nokia Corporation
E4EEFD	MR&D Manufacturing
E4F365	Time-O-Matic, Inc.
E4F3E3	Shanghai iComhome Co.,Ltd.
E4F3F5	SHENZHEN MERCURY COMMUNICATION TECHNOLOGIES CO.,LTD.
E4F4C6	Netgear
E4F7A1	Datafox GmbH
E4F89C	Intel Corporate
E4F8EF	Samsung Electronics Co.,Ltd
E4F939	Minxon Hotel Technology INC.
E4FA1D	PAD Peripheral Advanced Design Inc.
E4FAED	Samsung Electronics Co.,Ltd
E4FAFD	Intel Corporate
E4FB8F	MOBIWIRE MOBILES (NINGBO) CO.,LTD
E4FED9	EDMI Europe Ltd
E4FFDD	ELECTRON INDIA
E80036	Befs co,. ltd
E8039A	Samsung Electronics Co.,Ltd
E8040B	Apple, Inc.
E80410	Private
E80462	Cisco Systems, Inc
E804F3	Throughtek Co., Ltd.
E8056D	Nortel Networks
E80688	Apple, Inc.
E80734	Champion Optical Network Engineering, LLC
E807BF	SHENZHEN BOOMTECH INDUSTRY CO.,LTD
E8088B	HUAWEI TECHNOLOGIES CO.,LTD
E80945	Integrated Device Technology (Malaysia) Sdn. Bhd.
E80959	Guoguang Electric Co.,Ltd
E80B13	Akib Systems Taiwan, INC
E80C38	DAEYOUNG INFORMATION SYSTEM CO., LTD
E80C75	Syncbak, Inc.
E8102E	Really Simple Software, Inc
E81132	Samsung Electronics Co.,Ltd
E811CA	SHANDONG KAER ELECTRIC.CO.,LTD
E81324	GuangZhou Bonsoninfo System CO.,LTD
E81363	Comstock RD, Inc.
E81367	AIRSOUND Inc.
E8150E	Nokia Corporation
E8162B	IDEO Security Co., Ltd.
E817FC	NIFTY Corporation
E81863	IEEE Registration Authority
E82877	TMY Co., Ltd.
E828D5	Cots Technology
E82AEA	Intel Corporate
E82E24	Out of the Fog Research LLC
E83381	ARRIS Group, Inc.
E8343E	Beijing Infosec Technologies Co., LTD.
E8377A	ZyXEL Communications Corporation
E83935	Hewlett Packard
E839DF	ASKEY COMPUTER CORP
E83A12	Samsung Electronics Co.,Ltd
E83A97	Toshiba Corporation
E83EB6	Rim
E83EFB	GEODESIC LTD.
E83EFC	ARRIS Group, Inc.
E84040	Cisco Systems, Inc
E840F2	PEGATRON CORPORATION
E843B6	QNAP Systems, Inc.
E8447E	Bitdefender SRL
E8481F	Advanced Automotive Antennas
E84DD0	HUAWEI TECHNOLOGIES CO.,LTD
E84E06	EDUP INTERNATIONAL (HK) CO., LTD
E84E84	Samsung Electronics Co.,Ltd
E84ECE	Nintendo Co., Ltd.
E8508B	SAMSUNG ELECTRO-MECHANICS(THAILAND)
E8516E	TSMART Inc.
E8519D	Yeonhab Precision Co.,LTD
E85484	NEO Information Systems Co., Ltd.
E855B4	SAI Technology Inc.
E85659	Advanced-Connectek Inc.
E856D6	NCTech Ltd
E85AA7	LLC Emzior
E85B5B	LG ELECTRONICS INC
E85BF0	Imaging Diagnostics
E85D6B	Luminate Wireless
E85E53	Infratec Datentechnik GmbH
E8611F	Dawning Information Industry Co.,Ltd
E8617E	Liteon Technology Corporation
E86183	Black Diamond Advanced Technology, LLC
E861BE	Melec Inc.
E86549	Cisco Systems, Inc
E865D4	Tenda Technology Co.,Ltd.Dongguan branch
E866C4	Diamanti
E86CDA	Supercomputers and Neurocomputers Research Center
E86D52	ARRIS Group, Inc.
E86D54	Digit Mobile Inc
E86D6E	voestalpine SIGNALING Fareham Ltd.
E8718D	Elsys Equipamentos Eletronicos Ltda
E874E6	ADB Broadband Italia
E8757F	FIRS Technologies(Shenzhen) Co., Ltd
E878A1	BEOVIEW INTERCOM DOO
E87AF3	S5 Tech S.r.l.
E8802E	Apple, Inc.
E880D8	GNTEK Electronics Co.,Ltd.
E887A3	Loxley Public Company Limited
E8886C	Shenzhen SC Technologies Co.,LTD
E8892C	ARRIS Group, Inc.
E88D28	Apple, Inc.
E88DF5	ZNYX Networks, Inc.
E88E60	NSD Corporation
E89120	Motorola Mobility LLC, a Lenovo Company
E89218	Arcontia International AB
E892A4	LG Electronics (Mobile Communications)
E89309	Samsung Electronics Co.,Ltd
E8944C	Cogent Healthcare Systems Ltd
E894F6	TP-LINK TECHNOLOGIES CO.,LTD.
E89606	testo Instruments (Shenzhen) Co., Ltd.
E8995A	PiiGAB, Processinformation i Goteborg AB
E899C4	HTC Corporation
E89A8F	QUANTA COMPUTER INC.
E89AFF	Fujian Landi Commercial Equipment Co.,Ltd
E89D87	Toshiba
E89E0C	Private
E89EB4	Hon Hai Precision Ind. Co.,Ltd.
E89FEC	CHENGDU KT ELECTRONIC HI-TECH CO.,LTD
E8A364	Signal Path International / Peachtree Audio
E8A4C1	Deep Sea Electronics PLC
E8A7F2	Straffic
E8ABFA	Shenzhen Reecam Tech.Ltd.
E8B1FC	Intel Corporate
E8B2AC	Apple, Inc.
E8B4AE	Shenzhen C&D Electronics Co.,Ltd
E8B4C8	Samsung Electronics Co.,Ltd
E8B748	Cisco Systems, Inc
E8BA70	Cisco Systems, Inc
E8BB3D	Sino Prime-Tech Limited
E8BBA8	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
E8BDD1	HUAWEI TECHNOLOGIES CO.,LTD
E8BE81	Sagemcom Broadband SAS
E8C1D7	Philips
E8C229	H-Displays (MSC) Bhd
E8C320	Austco Communication Systems Pty Ltd
E8C74F	Liteon Technology Corporation
E8CBA1	Nokia Corporation
E8CC18	D-Link International
E8CC32	Micronet  LTD
E8CD2D	HUAWEI TECHNOLOGIES CO.,LTD
E8CE06	SkyHawke Technologies, LLC.
E8D0FA	MKS Instruments Deutschland GmbH
E8D11B	ASKEY COMPUTER CORP
E8D483	ULTIMATE Europe Transportation Equipment GmbH
E8D4E0	Beijing BenyWave Technology Co., Ltd.
E8DA96	Zhuhai Tianrui Electrical Power Tech. Co., Ltd.
E8DAAA	VideoHome Technology Corp.
E8DE27	TP-LINK TECHNOLOGIES CO.,LTD.
E8DE8E	Integrated Device Technology (Malaysia) Sdn. Bhd.
E8DED6	Intrising Networks, Inc.
E8DFF2	PRF Co., Ltd.
E8E08F	GRAVOTECH MARKING SAS
E8E0B7	Toshiba
E8E1E2	Energotest
E8E5D6	Samsung Electronics Co.,Ltd
E8E732	Alcatel-               # Alcatel-Lucent Enterprise
E8E770	Warp9 Tech Design, Inc.
E8E776	Shenzhen Kootion Technology Co., Ltd
E8E875	iS5 Communications Inc.
E8EA6A	StarTech.com
E8EADA	Denkovi Assembly Electronics LTD
E8EB11	Texas Instruments
E8ED05	ARRIS Group, Inc.
E8EDF3	Cisco Systems, Inc
E8EF89	OPMEX Tech.
E8F1B0	Sagemcom Broadband SAS
E8F226	MILLSON CUSTOM SOLUTIONS INC.
E8F2E2	LG Innotek
E8F2E3	Starcor Beijing Co.,Limited
E8F724	Hewlett Packard Enterprise
E8F928	RFTECH SRL
E8FC60	ELCOM Innovations Private Limited
E8FCAF	Netgear
E8FD72	SHANGHAI LINGUO TECHNOLOGY CO., LTD.
E8FD90	Turbostor
E8FDE8	CeLa Link Corporation
EC0133	TRINUS SYSTEMS INC.
EC01E2	FOXCONN INTERCONNECT TECHNOLOGY
EC01EE	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
EC086B	TP-LINK TECHNOLOGIES CO.,LTD.
EC0D9A	Mellanox Technologies, Inc.
EC0EC4	Hon Hai Precision Ind. Co.,Ltd.
EC0ED6	ITECH INSTRUMENTS SAS
EC1000	Enance Source Co., Ltd.	PC clones(?)
EC107B	Samsung Electronics Co.,Ltd
EC1120	FloDesign Wind Turbine Corporation
EC1127	Texas Instruments
EC13B2	Netonix
EC13DB	Juniper Networks
EC14F6	BioControl AS
EC172F	TP-LINK TECHNOLOGIES CO.,LTD.
EC1766	Research Centre Module
EC1A59	Belkin International Inc.
EC1D7F	zte corporation
EC1F72	SAMSUNG ELECTRO-MECHANICS(THAILAND)
EC219F	VidaBox LLC
EC21E5	Toshiba
EC2257	JiangSu NanJing University Electronic Information Technology Co.,Ltd
EC2280	D-Link International
EC233D	HUAWEI TECHNOLOGIES CO.,LTD
EC2368	IntelliVoice Co.,Ltd.
EC237B	zte corporation
EC24B8	Texas Instruments
EC26CA	TP-LINK TECHNOLOGIES CO.,LTD.
EC26FB	TECC CO.,LTD.
EC2AF0	Ypsomed AG
EC2C49	University of Tokyo
EC2E4E	Hitachi-               # HITACHI-LG DATA STORAGE INC
EC3091	Cisco Systems, Inc
EC3586	Apple, Inc.
EC363F	Markov Corporation
EC388F	HUAWEI TECHNOLOGIES CO.,LTD
EC3BF0	Novelsat
EC3C5A	SHEN ZHEN HENG SHENG HUI DIGITAL TECHNOLOGY CO.,LTD
EC3C88	MCNEX Co.,Ltd.
EC3E09	PERFORMANCE DESIGNED PRODUCTS, LLC
EC3EF7	Juniper Networks
EC3F05	Institute 706, The Second Academy China Aerospace Science & Industry Corp
EC42F0	ADL Embedded Solutions, Inc.
EC438B	Yaptv
EC43E6	AWCER Ltd.
EC43F6	ZyXEL Communications Corporation
EC4476	Cisco Systems, Inc
EC4644	TTK SAS
EC4670	Meinberg Funkuhren GmbH & Co. KG
EC473C	Redwire, LLC
EC4993	Qihan Technology Co., Ltd
EC4C4D	ZAO NPK RoTeK
EC4D47	HUAWEI TECHNOLOGIES CO.,LTD
EC4F82	Calix Inc.
EC52DC	WORLD MEDIA AND TECHNOLOGY Corp.
EC542E	Shanghai XiMei Electronic Technology Co. Ltd
EC55F9	Hon Hai Precision Ind. Co.,Ltd.
EC59E7	Microsoft Corporation
EC5A86	Yulong Computer Telecommunication Scientific (Shenzhen) Co.,Ltd
EC5C69	MITSUBISHI HEAVY INDUSTRIES MECHATRONICS SYSTEMS,LTD.
EC5F23	Qinghai Kimascend Electronics Technology Co. Ltd.
EC60E0	AVI-ON LABS
EC6264	Global411 Internet Services, LLC
EC63E5	ePBoard Design LLC
EC64E7	MOCACARE Corporation
EC66D1	B&W Group LTD
EC6881	Palo Alto Networks
EC6C9F	Chengdu Volans Technology CO.,LTD
EC71DB	Shenzhen Baichuan Digital Technology Co., Ltd.
EC74BA	Hirschmann Automation and Control GmbH
EC7C74	Justone Technologies Co., Ltd.
EC7D9D	Mei
EC8009	NovaSparks
EC836C	RM Tech Co., Ltd.
EC852F	Apple, Inc.
EC888F	TP-LINK TECHNOLOGIES CO.,LTD.
EC8892	Motorola Mobility LLC, a Lenovo Company
EC89F5	Lenovo Mobile Communication Technology Ltd.
EC8A4C	zte corporation
EC8CA2	Ruckus Wireless
EC8EAD	Dlx
EC8EAE	Nagravision SA
EC8EB5	Hewlett Packard
EC9233	Eddyfi NDT Inc
EC9327	Memmert+               # MEMMERT GmbH + Co. KG
EC93ED	DDoS-Guard LTD
EC9681	2276427 Ontario Inc
EC986C	Lufft Mess- und Regeltechnik GmbH
EC98C1	Beijing Risbo Network Technology Co.,Ltd
EC9A74	Hewlett Packard
EC9B5B	Nokia Corporation
EC9BF3	SAMSUNG ELECTRO-MECHANICS(THAILAND)
EC9ECD	Artesyn Embedded Technologies
ECA29B	Kemppi Oy
ECA86B	Elitegroup Computer Systems Co.,Ltd.
ECA9FA	GUANGDONG GENIUS TECHNOLOGY CO.,LTD.
ECAAA0	PEGATRON CORPORATION
ECADB8	Apple, Inc.
ECB106	Acuro Networks, Inc
ECB1D7	Hewlett Packard
ECB541	SHINANO E and E Co.Ltd.
ECB870	Beijing Heweinet Technology Co.,Ltd.
ECB907	CloudGenix Inc
ECBAFE	Giroptic
ECBBAE	Digivoice Tecnologia em Eletronica Ltda
ECBD09	FUSION Electronics Ltd
ECBD1D	Cisco Systems, Inc
ECC38A	Accuenergy (CANADA) Inc
ECC882	Cisco Systems, Inc
ECCB30	HUAWEI TECHNOLOGIES CO.,LTD
ECCD6D	Allied Telesis, Inc.
ECD00E	MiraeRecognition Co., Ltd.
ECD040	GEA Farm Technologies GmbH
ECD19A	Zhuhai Liming Industries Co., Ltd
ECD68A	Shenzhen JMicron Intelligent Technology Developmen
ECD925	Rami
ECD950	IRT SA
ECD9D1	Shenzhen TG-NET Botone Technology Co.,Ltd.
ECDE3D	Lamprey Networks, Inc.
ECDF3A	vivo Mobile Communication Co., Ltd.
ECE09B	Samsung Electronics Co.,Ltd
ECE154	Beijing Unisound Information Technology Co.,Ltd.
ECE1A9	Cisco Systems, Inc
ECE2FD	SKG Electric Group(Thailand) Co., Ltd.
ECE512	tado GmbH
ECE555	Hirschmann Automation
ECE744	Omntec mfg. inc
ECE90B	SISTEMA SOLUCOES ELETRONICAS LTDA - EASYTECH
ECE915	STI Ltd
ECE9F8	Guang Zhou TRI-SUN Electronics Technology  Co., Ltd
ECEA03	DARFON LIGHTING CORP
ECEED8	ZTLX Network Technology Co.,Ltd
ECF00E	Abocom
ECF236	NEOMONTANA ELECTRONICS
ECF342	GUANGDONG OPPO MOBILE TELECOMMUNICATIONS CORP.,LTD
ECF35B	Nokia Corporation
ECF4BB	Dell Inc.
ECF72B	HD DIGITAL TECH CO., LTD.
ECFAAA	The IMS Company
ECFC55	A. Eberle GmbH & Co. KG
ECFE7E	BlueRadios, Inc.
F0007F	Janz - Contadores de Energia, SA
F0022B	Chrontel
F00248	SmarteBuilding
F0038C	AzureWave Technology Inc.
F00786	Shandong Bittel Electronics Co., Ltd
F008F1	Samsung Electronics Co.,Ltd
F00D5C	JinQianMao  Technology Co.,Ltd.
F013C3	SHENZHEN FENDA TECHNOLOGY CO., LTD
F015A0	KyungDong One Co., Ltd.
F015B9	PlayFusion Limited
F0182B	LG Chem
F01B6C	vivo Mobile Communication Co., Ltd.
F01C13	LG Electronics (Mobile Communications)
F01C2D	Juniper Networks
F01DBC	Microsoft Corporation
F01E34	ORICO Technologies Co., Ltd
F01FAF	Dell Inc.
F0219D	Cal-Comp Electronics & Communications Company Ltd.
F0224E	Esan electronic co.
F02329	SHOWA DENKI CO.,LTD.
F02405	OPUS High Technology Corporation
F02408	Talaris (Sweden) AB
F02475	Apple, Inc.
F02572	Cisco Systems, Inc
F025B7	SAMSUNG ELECTRO-MECHANICS(THAILAND)
F02624	WAFA TECHNOLOGIES CO., LTD.
F0264C	Dr. Sigrist AG
F0272D	Amazon Technologies Inc.
F02745	F-Secure Corporation
F02765	Murata Manufacturing Co., Ltd.
F02929	Cisco Systems, Inc
F02A23	Creative Next Design
F02A61	Waldo Networks, Inc.
F02FA7	HUAWEI TECHNOLOGIES CO.,LTD
F02FD8	Bi2-Vision
F0321A	Mita-Teknik A/S
F03404	TCT mobile ltd
F037A1	Huike Electronics (SHENZHEN) CO., LTD.
F03A4B	Bloombase, Inc.
F03A55	Omega Elektronik AS
F03D29	Actility
F03E90	Ruckus Wireless
F03EBF	GOGORO TAIWAN LIMITED
F03FF8	R L Drake
F0407B	Fiberhome Telecommunication Technologies Co.,LTD
F0421C	Intel Corporate
F04335	DVN(Shanghai)Ltd.
F04347	HUAWEI TECHNOLOGIES CO.,LTD
F04A2B	PYRAMID Computer GmbH
F04B6A	Scientific Production Association Siberian Arsenal, Ltd.
F04BF2	JTECH Communications, Inc.
F04DA2	Dell Inc.
F04F7C	Private
F05849	CareView Communications
F05A09	Samsung Electronics Co.,Ltd
F05B7B	Samsung Electronics Co.,Ltd
F05C19	Aruba Networks
F05D89	Dycon Limited
F05DC8	Duracell Powermat
F05F5A	Getriebebau NORD GmbH and Co. KG
F06130	Advantage Pharmacy Services, LLC
F0620D	Shenzhen Egreat Tech Corp.,Ltd
F06281	ProCurve Networking by HP
F065DD	Primax Electronics Ltd.
F06853	Integrated Corporation
F06BCA	Samsung Electronics Co.,Ltd
F06E32	MICROTEL INNOVATION S.R.L.
F0728C	Samsung Electronics Co.,Ltd
F073AE	PEAK-System Technik
F074E4	Thundercomm Technology Co., Ltd
F0761C	COMPAL INFORMATION (KUNSHAN) CO., LTD.
F07765	Sourcefire, Inc
F077D0	Xcellen
F07816	Cisco Systems, Inc
F07959	ASUSTek COMPUTER INC.
F07960	Apple, Inc.
F07BCB	Hon Hai Precision Ind. Co.,Ltd.
F07D68	D-Link Corporation
F07F06	Cisco Systems, Inc
F07F0C	Leopold Kostal GmbH &Co. KG
F081AF	IRZ AUTOMATION TECHNOLOGIES LTD
F08261	Sagemcom Broadband SAS
F0842F	ADB Broadband Italia
F084C9	zte corporation
F08A28	JIANGSU HENGSION ELECTRONIC S and T CO.,LTD
F08BFE	COSTEL.,CO.LTD
F08CFB	Fiberhome Telecommunication Technologies Co.,LTD
F08EDB	VeloCloud Networks
F0921C	Hewlett Packard
F0933A	NxtConect
F093C5	Garland Technology
F097E5	TAMIO, INC
F09838	HUAWEI TECHNOLOGIES CO.,LTD
F099BF	Apple, Inc.
F09A51	Shanghai Viroyal Electronic Technology Company Limited
F09CBB	RaonThink Inc.
F09CE9	Aerohive Networks Inc.
F09E63	Cisco Systems, Inc
F09FC2	Ubiquiti Networks Inc.
F0A225	Private
F0A764	GST Co., Ltd.
F0AB54	MITSUMI ELECTRIC CO.,LTD.
F0ACA4	HBC-radiomatic
F0ACD7	IEEE Registration Authority
F0AD4E	Globalscale Technologies, Inc.
F0AE51	Xi3 Corp
F0B052	Ruckus Wireless
F0B0E7	Apple, Inc.
F0B2E5	Cisco Systems, Inc
F0B429	Xiaomi Communications Co Ltd
F0B479	Apple, Inc.
F0B6EB	Poslab Technology Co., Ltd.
F0BCC8	MaxID (Pty) Ltd
F0BDF1	Sipod Inc.
F0BF97	Sony Corporation
F0C1F1	Apple, Inc.
F0C24C	Zhejiang FeiYue Digital Technology Co., Ltd
F0C27C	Mianyang Netop Telecom Equipment Co.,Ltd.
F0C77F	Texas Instruments
F0C850	HUAWEI TECHNOLOGIES CO.,LTD
F0C88C	LeddarTech Inc.
F0CBA1	Apple, Inc.
F0D14F	LINEAR LLC
F0D1A9	Apple, Inc.
F0D1B8	Ledvance
F0D2F1	Amazon Technologies Inc.
F0D3A7	CobaltRay Co., Ltd
F0D3E7	Sensometrix SA
F0D5BF	Intel Corporate
F0D657	Echosens
F0D767	Axema Passagekontroll AB
F0D7AA	Motorola Mobility LLC, a Lenovo Company
F0D9B2	EXO S.A.
F0DA7C	RLH INDUSTRIES,INC.
F0DB30	Yottabyte
F0DBE2	Apple, Inc.
F0DBF8	Apple, Inc.
F0DCE2	Apple, Inc.
F0DE71	Shanghai EDO Technologies Co.,Ltd.
F0DEB9	ShangHai Y&Y Electronics Co., Ltd
F0DEF1	Wistron Infocomm (Zhongshan) Corporation
F0E5C3	Drägerwerk AG & Co. KG aA
F0E77E	Samsung Electronics Co.,Ltd
F0EBD0	Shanghai Feixun Communication Co.,Ltd.
F0EC39	Essec
F0ED1E	Bilkon Bilgisayar Kontrollu Cih. Im.Ltd.
F0EE10	Samsung Electronics Co.,Ltd
F0EE58	PACE Telematics GmbH
F0EEBB	VIPAR GmbH
F0F002	Hon Hai Precision Ind. Co.,Ltd.
F0F249	Hitron Technologies. Inc
F0F260	Mobitec AB
F0F336	TP-LINK TECHNOLOGIES CO.,LTD.
F0F5AE	Adaptrum Inc.
F0F61C	Apple, Inc.
F0F644	Whitesky Science & Technology Co.,Ltd.
F0F669	Motion Analysis Corporation
F0F755	Cisco Systems, Inc
F0F7B3	Phorm
F0F842	KEEBOX, Inc.
F0F9F7	IES GmbH & Co. KG
F0FDA0	Acurix Networks Pty Ltd
F0FE6B	Shanghai High-Flying Electronics Technology Co., Ltd
F40304	Google, Inc.
F40321	BeNeXt B.V.
F4032F	Reduxio Systems
F40343	Hewlett Packard Enterprise
F4044C	ValenceTech Limited
F40669	Intel Corporate
F4068D	devolo AG
F406A5	Hangzhou Bianfeng Networking Technology Co., Ltd.
F409D8	SAMSUNG ELECTRO-MECHANICS(THAILAND)
F40A4A	INDUSNET Communication Technology Co.,LTD
F40B93	BlackBerry RTS
F40E11	IEEE Registration Authority
F40E22	Samsung Electronics Co.,Ltd
F40F1B	Cisco Systems, Inc
F40F24	Apple, Inc.
F40F9B	Wavelink
F41535	SPON Communication Technology Co.,Ltd
F41563	F5 Networks, Inc.
F415FD	Shanghai Pateo Electronic Equipment Manufacturing Co., Ltd.
F41BA1	Apple, Inc.
F41E26	Simon-Kaloi Engineering
F41F0B	YAMABISHI Corporation
F41F88	zte corporation
F41FC2	Cisco Systems, Inc
F42012	Cuciniale GmbH
F42833	MMPC Inc.
F42853	Zioncom Electronics (Shenzhen) Ltd.
F42896	SPECTO PAINEIS ELETRONICOS LTDA
F42981	vivo Mobile Communication Co., Ltd.
F42B48	Ubiqam
F42C56	SENOR TECH CO LTD
F431C3	Apple, Inc.
F436E1	Abilis Systems SARL
F437B7	Apple, Inc.
F43814	Shanghai Howell Electronic Co.,Ltd
F43D80	FAG Industrial Services GmbH
F43E61	SHENZHEN GONGJIN ELECTRONICS CO.,LT
F43E9D	Benu Networks, Inc.
F44227	S & S Research Inc.
F4428F	Samsung Electronics Co.,Ltd
F44450	BND Co., Ltd.
F445ED	Portable Innovation Technology Ltd.
F44713	Leading Public Performance Co., Ltd.
F4472A	Nanjing Rousing Sci. and Tech. Industrial Co., Ltd
F44848	Amscreen Group Ltd
F44B2A	Cisco SPVTG
F44C7F	HUAWEI TECHNOLOGIES CO.,LTD
F44D17	GOLDCARD HIGH-TECH CO.,LTD.
F44D30	Elitegroup Computer Systems Co.,Ltd.
F44E05	Cisco Systems, Inc
F44EFD	Actions Semiconductor Co.,Ltd.(Cayman Islands)
F450EB	Telechips Inc
F45214	Mellanox Technologies, Inc.
F45433	Rockwell Automation
F45595	HENGBAO Corporation LTD.
F4559C	HUAWEI TECHNOLOGIES CO.,LTD
F455E0	Niceway CNC Technology Co.,Ltd.Hunan Province
F4573E	Fiberhome Telecommunication Technologies Co.,LTD
F45842	Boxx TV Ltd
F45B73	Wanjiaan Interconnected Technology Co., Ltd
F45C89	Apple, Inc.
F45EAB	Texas Instruments
F45F69	Matsufu Electronics distribution Company
F45FD4	Cisco SPVTG
F45FF7	DQ Technology Inc.
F4600D	Panoptic Technology, Inc
F462D0	Not for Radio, LLC
F46349	Diffon Corporation
F4645D	Toshiba
F4672D	ShenZhen Topstar Technology Company
F46A92	SHENZHEN FAST TECHNOLOGIES CO.,LTD
F46ABC	Adonit Corp. Ltd.
F46D04	ASUSTek COMPUTER INC.
F46DE2	zte corporation
F470AB	vivo Mobile Communication Co., Ltd.
F473CA	Conversion Sound Inc.
F47626	Viltechmeda UAB
F47A4E	Woojeon&               # Woojeon&Handan
F47ACC	SolidFire, Inc.
F47B5E	Samsung Electronics Co.,Ltd
F47F35	Cisco Systems, Inc
F48139	CANON INC.
F483CD	TP-LINK TECHNOLOGIES CO.,LTD.
F483E1	Shanghai Clouder Semiconductor Co.,Ltd
F485C6	FDT Technologies
F48771	Infoblox
F48B32	Xiaomi Communications Co Ltd
F48C50	Intel Corporate
F48E09	Nokia Corporation
F48E38	Dell Inc.
F48E92	HUAWEI TECHNOLOGIES CO.,LTD
F490CA	Tensorcom
F490EA	Deciso B.V.
F4911E	ZHUHAI EWPE INFORMATION TECHNOLOGY INC
F49461	NexGen Storage
F49466	CountMax,  ltd
F49634	Intel Corporate
F49651	NAKAYO Inc
F499AC	WEBER Schraubautomaten GmbH
F49EEF	Taicang T&W Electronics
F49F54	Samsung Electronics Co.,Ltd
F49FF3	HUAWEI TECHNOLOGIES CO.,LTD
F4A294	EAGLE WORLD DEVELOPMENT CO., LIMITED
F4A52A	Hawa Technologies Inc
F4A739	Juniper Networks
F4ACC1	Cisco Systems, Inc
F4B164	Lightning Telecommunications Technology Co. Ltd
F4B381	WindowMaster A/S
F4B52F	Juniper Networks
F4B549	Xiamen Yeastar Information Technology Co., Ltd.
F4B6E5	TerraSem Co.,Ltd
F4B72A	TIME INTERCONNECT LTD
F4B7E2	Hon Hai Precision Ind. Co.,Ltd.
F4B85E	Texas Instruments
F4B8A7	zte corporation
F4BD7C	Chengdu jinshi communication Co., LTD
F4C447	Coagent International Enterprise Limited
F4C4D6	Shenzhen Xinfa Electronic Co.,ltd
F4C613	Alcatel-               # Alcatel-Lucent Shanghai Bell Co., Ltd
F4C6D7	blackned GmbH
F4C714	HUAWEI TECHNOLOGIES CO.,LTD
F4C795	WEY Elektronik AG
F4CA24	FreeBit Co., Ltd.
F4CAE5	FREEBOX SAS
F4CB52	HUAWEI TECHNOLOGIES CO.,LTD
F4CC55	Juniper Networks
F4CD90	Vispiron Rotec GmbH
F4CE46	Hewlett Packard
F4CFE2	Cisco Systems, Inc
F4D032	Yunnan Ideal Information&Technology.,Ltd
F4D261	SEMOCON Co., Ltd
F4D9FB	Samsung Electronics Co.,Ltd
F4DC41	YOUNGZONE CULTURE (SHANGHAI) CORP
F4DC4D	Beijing CCD Digital Technology Co., Ltd
F4DCDA	Zhuhai Jiahe Communication Technology Co., limited
F4DCF9	HUAWEI TECHNOLOGIES CO.,LTD
F4DD9E	Gopro
F4DE0C	ESPOD Ltd.
F4E142	Delta Elektronika BV
F4E3FB	HUAWEI TECHNOLOGIES CO.,LTD
F4E4AD	zte corporation
F4E6D7	Solar Power Technologies, Inc.
F4E926	Tianjin Zanpu Technology Inc.
F4E9D4	QLogic Corporation
F4EA67	Cisco Systems, Inc
F4EB38	Sagemcom Broadband SAS
F4EC38	TP-LINK TECHNOLOGIES CO.,LTD.
F4ED5F	SHENZHEN KTC TECHNOLOGY GROUP
F4EE14	SHENZHEN MERCURY COMMUNICATION TECHNOLOGIES CO.,LTD.
F4EF9E	SGSG SCIENCE & TECHNOLOGY CO. LTD
F4F15A	Apple, Inc.
F4F1E1	Motorola Mobility LLC, a Lenovo Company
F4F26D	TP-LINK TECHNOLOGIES CO.,LTD.
F4F524	Motorola Mobility LLC, a Lenovo Company
F4F5A5	Nokia Corporation
F4F5D8	Google, Inc.
F4F5E8	Google, Inc.
F4F646	Dediprog Technology Co. Ltd.
F4F951	Apple, Inc.
F4FC32	Texas Instruments
F4FCB1	JJ Corp
F4FD2B	ZOYI Company
F80113	HUAWEI TECHNOLOGIES CO.,LTD
F80278	IEEE Registration Authority
F80332	Khomp
F80377	Apple, Inc.
F8042E	SAMSUNG ELECTRO-MECHANICS(THAILAND)
F8051C	DRS Imaging and Targeting Solutions
F80BBE	ARRIS Group, Inc.
F80BCB	Cisco Systems, Inc
F80BD0	Datang Telecom communication terminal (Tianjin) Co., Ltd.
F80CF3	LG Electronics (Mobile Communications)
F80D43	Hon Hai Precision Ind. Co.,Ltd.
F80D60	CANON INC.
F80DEA	ZyCast Technology Inc.
F80F41	Wistron Infocomm (Zhongshan) Corporation
F80F84	Natural Security SAS
F81037	Atopia Systems, LP
F81547	Avaya Inc
F81654	Intel Corporate
F81897	2Wire Inc
F81A67	TP-LINK TECHNOLOGIES CO.,LTD.
F81CE5	Telefonbau Behnke GmbH
F81D78	IEEE Registration Authority
F81D93	Longdhua(Beijing) Controls Technology Co.,Ltd
F81EDF	Apple, Inc.
F82285	Cypress Technology CO., LTD.
F823B2	HUAWEI TECHNOLOGIES CO.,LTD
F82441	Yeelink
F82793	Apple, Inc.
F82BC8	Jiangsu Switter Co., Ltd
F82C18	2Wire Inc
F82EDB	RTW GmbH & Co. KG
F82F08	Molex
F82F5B	eGauge Systems LLC
F82FA8	Hon Hai Precision Ind. Co.,Ltd.
F83094	Alcatel-               # Alcatel-Lucent Telecom Limited
F8313E	endeavour GmbH
F832E4	ASUSTek COMPUTER INC.
F83376	Good Mind Innovation Co., Ltd.
F83553	Magenta Research Ltd.
F835DD	Gemtek Technology Co., Ltd.
F83D4E	Softlink Automation System Co., Ltd
F83DFF	HUAWEI TECHNOLOGIES CO.,LTD
F83F51	Samsung Electronics Co.,Ltd
F842FB	Yasuda Joho Co.,ltd.
F845AD	Konka Group Co., Ltd.
F8461C	Sony Interactive Entertainment Inc.
F8462D	SYNTEC Incorporation
F8472D	X2gen Digital Corp. Ltd
F84897	Hitachi, Ltd.
F84A73	EUMTECH CO., LTD
F84A7F	Innometriks Inc
F84ABF	HUAWEI TECHNOLOGIES CO.,LTD
F84F57	Cisco Systems, Inc
F85063	Verathon
F8516D	Denwa Technology Corp.
F852DF	VNL Europe AB
F854AF	ECI Telecom Ltd.
F8572E	Core Brands, LLC
F85971	Intel Corporate
F85A00	Sanford LP
F85B9C	SB SYSTEMS Co.,Ltd
F85BC9	M-Cube Spa
F85C45	IC Nexus Co. Ltd.
F85C4D	Nokia
F85F2A	Nokia Corporation
F86214	Apple, Inc.
F862AA	xn systems
F8633F	Intel Corporate
F86601	Suzhou Chi-tek information technology Co., Ltd
F866D1	Hon Hai Precision Ind. Co.,Ltd.
F866F2	Cisco Systems, Inc
F86971	Seibu Electric Co.,
F86ECF	Arcx Inc
F871FE	The Goldman Sachs Group, Inc.
F872EA	Cisco Systems, Inc
F87394	Netgear
F873A2	Avaya Inc
F87588	HUAWEI TECHNOLOGIES CO.,LTD
F8769B	Neopis Co., Ltd.
F877B8	Samsung Electronics Co.,Ltd
F87AEF	Rosonix Technology, Inc.
F87B62	FASTWEL INTERNATIONAL CO., LTD. Taiwan Branch
F87B7A	ARRIS Group, Inc.
F87B8C	Amped Wireless
F88096	Elsys Equipamentos Eletrônicos Ltda
F8811A	Overkiz
F88479	Yaojin Technology(Shenzhen)Co.,Ltd
F884F2	Samsung Electronics Co.,Ltd
F88C1C	KAISHUN ELECTRONIC TECHNOLOGY CO., LTD. BEIJING
F88DEF	Tenebraex
F88E85	Comtrend Corporation
F88FCA	Google, Inc.
F8912A	GLP German Light Products GmbH
F893F3	Volans
F894C2	Intel Corporate
F89550	Proton Products Chengdu Ltd
F895C7	LG Electronics (Mobile Communications)
F897CF	Daeshin-               # DAESHIN-INFORMATION TECHNOLOGY CO., LTD.
F8983A	Leeman International (HongKong) Limited
F898B9	HUAWEI TECHNOLOGIES CO.,LTD
F89955	Fortress Technology Inc
F89D0D	Control Technology Inc.
F89FB8	YAZAKI Energy System Corporation
F8A03D	Dinstar Technologies Co., Ltd.
F8A097	ARRIS Group, Inc.
F8A188	LED Roadway Lighting
F8A2B4	RHEWA-WAAGENFABRIK August Freudewald GmbH &amp;Co. KG
F8A34F	zte corporation
F8A45F	Xiaomi Communications Co Ltd
F8A5C5	Cisco Systems, Inc
F8A963	COMPAL INFORMATION (KUNSHAN) CO., LTD.
F8A9D0	LG Electronics (Mobile Communications)
F8A9DE	PUISSANCE PLUS
F8AA8A	Axview Technology (Shenzhen) Co.,Ltd
F8AB05	Sagemcom Broadband SAS
F8AC6D	Deltenna Ltd
F8B156	Dell Inc.
F8B2F3	GUANGZHOU BOSMA TECHNOLOGY CO.,LTD
F8B599	Guangzhou CHNAVS Digital Technology Co.,Ltd
F8BBBF	eero inc.
F8BC12	Dell Inc.
F8BC41	Rosslare Enterprises Limited
F8BE0D	A2UICT Co.,Ltd.
F8BF09	HUAWEI TECHNOLOGIES CO.,LTD
F8C001	Juniper Networks
F8C091	Highgates Technology
F8C288	Cisco Systems, Inc
F8C372	TSUZUKI DENKI
F8C397	NZXT Corp. Ltd.
F8C678	Carefusion
F8C96C	Fiberhome Telecommunication Technologies Co.,LTD
F8CAB8	Dell Inc.
F8CFC5	Motorola Mobility LLC, a Lenovo Company
F8D027	Seiko Epson Corporation
F8D0AC	Sony Interactive Entertainment Inc.
F8D0BD	Samsung Electronics Co.,Ltd
F8D111	TP-LINK TECHNOLOGIES CO.,LTD.
F8D3A9	AXAN Networks
F8D462	Pumatronix Equipamentos Eletronicos Ltda.
F8D756	Simm Tronic Limited
F8D7BF	REV Ritter GmbH
F8DA0C	Hon Hai Precision Ind. Co.,Ltd.
F8DADF	EcoTech, Inc.
F8DAE2	Beta LaserMike
F8DAF4	Taishan Online Technology Co., Ltd.
F8DB4C	PNY Technologies, INC.
F8DB7F	HTC Corporation
F8DB88	Dell Inc.
F8DC7A	Variscite LTD
F8DFA8	zte corporation
F8E079	Motorola Mobility LLC, a Lenovo Company
F8E4FB	Actiontec Electronics, Inc
F8E61A	Samsung Electronics Co.,Ltd
F8E71E	Ruckus Wireless
F8E7B5	µTech Tecnologia LTDA
F8E811	HUAWEI TECHNOLOGIES CO.,LTD
F8E903	D-Link International
F8E968	Egker Kft.
F8EA0A	Dipl.-Math. Michael Rauch
F8EDA5	ARRIS Group, Inc.
F8F005	Newport Media Inc.
F8F014	RackWare Inc.
F8F082	NAG LLC
F8F1B6	Motorola Mobility LLC, a Lenovo Company
F8F25A	G-Lab GmbH
F8F464	Rawe Electonic GmbH
F8F7D3	International Communications Corporation
F8F7FF	SYN-TECH SYSTEMS INC
F8FB2F	Santur Corporation
F8FE5C	Reciprocal Labs Corp
F8FEA8	Technico Japan Corporation
F8FF0B	Electronic Technology Inc.
F8FF5F	Shenzhen Communication Technology Co.,Ltd
FC0012	Toshiba Samsung Storage Technolgoy Korea Corporation
FC019E	Vievu
FC01CD	FUNDACION TEKNIKER
FC0647	Cortland Research, LLC
FC07A0	LRE Medical GmbH
FC084A	FUJITSU LIMITED
FC0877	Prentke Romich Company
FC09D8	ACTEON Group
FC09F6	GUANGDONG TONZE ELECTRIC CO.,LTD
FC0A81	Extreme Networks
FC0F4B	Texas Instruments
FC0FE6	Sony Interactive Entertainment Inc.
FC10BD	Control Sistematizado S.A.
FC10C6	Taicang T&W Electronics
FC1186	Logic3 plc
FC1349	Global Apps Corp.
FC15B4	Hewlett Packard
FC1607	Taian Technology(Wuxi) Co.,Ltd.
FC1794	InterCreative Co., Ltd
FC1910	Samsung Electronics Co.,Ltd
FC19D0	Cloud Vision Networks Technology Co.,Ltd.
FC1A11	vivo Mobile Communication Co., Ltd.
FC1BFF	V-ZUG AG
FC1D59	I Smart Cities HK Ltd
FC1D84	Autobase
FC1E16	IPEVO corp
FC1F19	SAMSUNG ELECTRO MECHANICS CO., LTD.
FC1FC0	Eurecam
FC229C	Han Kyung I Net Co.,Ltd.
FC2325	EosTek (Shenzhen) Co., Ltd.
FC253F	Apple, Inc.
FC27A2	TRANS ELECTRIC CO., LTD.
FC2A54	Connected Data, Inc.
FC2D5E	zte corporation
FC2E2D	Lorom Industrial Co.LTD.
FC2F40	Calxeda, Inc.
FC2FAA	Nokia
FC2FEF	UTT Technologies Co., Ltd.
FC3288	CELOT Wireless Co., Ltd
FC335F	Polyera
FC3598	Favite Inc.
FC35E6	Visteon corp
FC372B	SICHUAN TIANYI COMHEART TELECOMCO.,LTD
FC3CE9	Tsingtong Technologies Co, Ltd.
FC3D93	LONGCHEER TELECOMMUNICATION LIMITED
FC3F7C	HUAWEI TECHNOLOGIES CO.,LTD
FC3FAB	Henan Lanxin Technology Co., Ltd
FC3FDB	Hewlett Packard
FC4203	Samsung Electronics Co.,Ltd
FC4463	Universal Audio, Inc
FC4499	Swarco LEA d.o.o.
FC455F	JIANGXI SHANSHUI OPTOELECTRONIC TECHNOLOGY CO.,LTD
FC4596	COMPAL INFORMATION (KUNSHAN) CO., LTD.
FC48EF	HUAWEI TECHNOLOGIES CO.,LTD
FC4AE9	Castlenet Technology Inc.
FC4B1C	INTERSENSOR S.R.L.
FC4BBC	Sunplus Technology Co., Ltd.
FC4DD4	Universal Global Scientific Industrial Co., Ltd.
FC5090	SIMEX Sp. z o.o.
FC51A4	ARRIS Group, Inc.
FC528D	Technicolor CH USA Inc.
FC52CE	Control iD
FC539E	Shanghai Wind Technologies Co.,Ltd
FC55DC	Baltic Latvian Universal Electronics LLC
FC58FA	Shen Zhen Shi Xin Zhong Xin Technology Co.,Ltd.
FC5B24	Weibel Scientific A/S
FC5B26	MikroBits
FC5B39	Cisco Systems, Inc
FC6018	Zhejiang Kangtai Electric Co., Ltd.
FC6198	NEC Personal Products, Ltd
FC626E	Beijing MDC Telecom
FC62B9	ALPS ELECTRIC CO.,LTD.
FC64BA	Xiaomi Communications Co Ltd
FC683E	Directed Perception, Inc
FC6C31	LXinstruments GmbH
FC6DC0	BME CORPORATION
FC6FB7	ARRIS Group, Inc.
FC7516	D-Link International
FC75E6	Handreamnet
FC790B	Hitachi High Technologies America, Inc.
FC7CE7	FCI USA LLC
FC8329	Trei technics
FC8399	Avaya Inc
FC83C6	N-Radio Technologies Co., Ltd.
FC8B97	Shenzhen Gongjin Electronics Co.,Ltd
FC8E7E	ARRIS Group, Inc.
FC8F90	Samsung Electronics Co.,Ltd
FC8FC4	Intelligent Technology Inc.
FC9114	Technicolor CH USA Inc.
FC923B	Nokia Corporation
FC946C	Ubivelox
FC94E3	Technicolor CH USA Inc.
FC9947	Cisco Systems, Inc
FC9AFA	Motus Global Inc.
FC9FAE	Fidus Systems Inc
FC9FE1	CONWIN.Tech. Ltd
FCA13E	Samsung Electronics Co.,Ltd
FCA22A	PT. Callysta Multi Engineering
FCA386	SHENZHEN CHUANGWEI-RGB ELECTRONICS CO.,LTD
FCA841	Avaya Inc
FCA89A	Sunitec Enterprise Co.,Ltd
FCA9B0	MIARTECH (SHANGHAI),INC.
FCAA14	GIGA-BYTE TECHNOLOGY CO.,LTD.
FCAD0F	QTS NETWORKS
FCAF6A	Qulsar Inc
FCAFAC	Socionext Inc.
FCB0C4	Shanghai DareGlobal Technologies Co.,Ltd
FCB4E6	ASKEY COMPUTER CORP
FCB58A	Wapice Ltd.
FCB698	Cambridge Industries(Group) Co.,Ltd.
FCBBA1	Shenzhen Minicreate Technology Co.,Ltd
FCBC9C	Vimar Spa
FCC233	Private
FCC23D	Atmel Corporation
FCC2DE	Murata Manufacturing Co., Ltd.
FCC734	Samsung Electronics Co.,Ltd
FCC897	zte corporation
FCCAC4	LifeHealth, LLC
FCCCE4	Ascon Ltd.
FCCF43	HUIZHOU CITY HUIYANG DISTRICT MEISIQI INDUSTRY DEVELOPMENT CO,.LTD
FCCF62	IBM Corp
FCD4F2	The Coca Cola Company
FCD4F6	Messana Air.Ray Conditioning s.r.l.
FCD5D9	Shenzhen SDMC Technology Co., Ltd.
FCD6BD	Robert Bosch GmbH
FCD733	TP-LINK TECHNOLOGIES CO.,LTD.
FCD817	Beijing Hesun Technologies Co.Ltd.
FCD848	Apple, Inc.
FCDB96	ENERVALLEY CO., LTD
FCDBB3	Murata Manufacturing Co., Ltd.
FCDC4A	G-Wearables Corp.
FCDD55	Shenzhen WeWins wireless Co.,Ltd
FCE186	A3M Co., LTD
FCE192	Sichuan Jinwangtong Electronic Science&Technology Co,.Ltd
FCE1D9	Stable Imaging Solutions LLC
FCE1FB	Array Networks
FCE23F	CLAY PAKY SPA
FCE33C	HUAWEI TECHNOLOGIES CO.,LTD
FCE557	Nokia Corporation
FCE892	Hangzhou Lancable Technology Co.,Ltd
FCE998	Apple, Inc.
FCECDA	Ubiquiti Networks Inc.
FCEDB9	Arrayent
FCF136	Samsung Electronics Co.,Ltd
FCF152	Sony Corporation
FCF1CD	OPTEX-FA CO.,LTD.
FCF528	ZyXEL Communications Corporation
FCF647	Fiberhome Telecommunication Technologies Co.,LTD
FCF8AE	Intel Corporate
FCF8B7	TRONTEQ Electronic
FCFAF7	Shanghai Baud Data Communication Co.,Ltd.
FCFBFB	Cisco Systems, Inc
FCFC48	Apple, Inc.
FCFE77	Hitachi Reftechno, Inc.
FCFEC2	Invensys Controls UK Limited
FCFFAA	IEEE Registration Authority
""".split('\n')

def search_vendor(mac):
    mac_vendor_part = mac.split(':')[0:3]
    mac_vendor_part = ''.join(mac_vendor_part).upper()
    pattern = re.compile(f"^{mac_vendor_part}\t(.+)$", re.IGNORECASE)
    for line in vendors:
        match = pattern.match(line)
        if match:
            return match.group(1)
    return None

def is_valid_mac(mac):
    return re.match(r'^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$', mac)

def main(arg):
    if not is_valid_mac(arg):
        print('Invalid MAC address')
        sys.exit(1)
    mac = arg.replace('-', ':').upper()
    vendor = search_vendor(mac)
    if vendor:
        print(f'MAC address : {mac}')
        print(f'Vendor      : {vendor}')
    else:
        print('Vendor not found')

if __name__ == '__main__':    
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <mac-address>')
        sys.exit(1)
    main(sys.argv[1])